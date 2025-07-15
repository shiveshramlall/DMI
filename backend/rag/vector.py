import os
import re
import shutil
from chromadb import PersistentClient
import ollama
from langchain.text_splitter import MarkdownHeaderTextSplitter
from langchain_community.document_loaders import TextLoader, DirectoryLoader

class ChromaRag():

    def __init__(self, source_directory, collection_name, db_path, model_name):

        self.source_directory = source_directory
        self.collection_name = collection_name
        self.collection_name = self.normalize(collection_name)
        self.db_path = db_path
        self.model_name = model_name

        try:
            shutil.rmtree(self.db_path)
        except:
            pass 

        os.makedirs(self.db_path, exist_ok=True)
        
        client = PersistentClient(path=db_path)
        self.collection = client.get_or_create_collection(name=self.collection_name)
        self.create_rag()

    def normalize(self, name):
        return re.sub(r"[-_. ]+", "-", name).lower()

    def create_rag(self):
        
        headers_to_split_on = [
            ("#", "Header 1"),
            ("##", "Header 2"),
            ("###", "Header 3"),
            ("####", "Header 4"),
            ("#####", "Header 4"),
        ]

        markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on, strip_headers=False)

        loader = DirectoryLoader(
            self.source_directory,
            glob="**/*.md",
            loader_cls=TextLoader,
            loader_kwargs={"encoding": "utf-8"},
        )
        docs = loader.load()

        chunks = []
        for doc in docs:

            text = doc.page_content
            splits = markdown_splitter.split_text(text)
            source = doc.metadata.get("source")
            # splits = [f"SOURCE FILE: {source}\n\nCONTENT (page_content and metadata about page): \n{split}" for split in splits]
            # chunks.extend(splits)

            for i, split in enumerate(splits):

                source_basename = self.normalize(os.path.basename(source)).replace('.md', '')
                chunk_id = f"{self.normalize(source_basename).replace('.md', '')}-{i+1}"

                page_content = split.page_content
                header_metadata = split.metadata

                title = header_metadata.get("Header 1", "Untitled")
                section = header_metadata.get("Header 2", "Untitled")
                subsection = header_metadata.get("Header 3", "Untitled")

                header_metadata["source"] = source
                header_metadata["source_basename"] = source_basename
                header_metadata["chunk_id"] = chunk_id

                formatted = (
                    f"Title: {title}\n"
                    f"Section: {section}\n"
                    f"Subsection: {subsection}\n"
                    f"Source: {source_basename}\n\n"
                    f"Content:\n{page_content.strip()}"
                )

                chunks.append((formatted, header_metadata, chunk_id))

        self.embed_and_store(chunks)
    
    def embed_text(self, text):
        
        resp = ollama.embed(model=self.model_name, input=text)
        return resp["embeddings"]
    
    def embed_and_store(self, chunk_triples):
        for text, metadata, id in chunk_triples:
            embeddings = self.embed_text(text)
            self.collection.add(
                ids=[id],
                embeddings=embeddings,
                documents=[text],
                metadatas=[metadata]
            )
    
    def retrieve(self, query, k=5):
        """Retrieve relevant documents for a query"""
        query_embedding = self.embed_text(query)
        results = self.collection.query(
            query_embeddings=query_embedding,
            n_results=k
        )

        return results["documents"][0], results["ids"][0], results["metadatas"][0]
    
    def inspect_db(self, limit=None):
        

        count = self.collection.count()
        results = self.collection.get()
        documents = results['documents']
        
        if limit:
            documents = documents[:limit]
        
        return {
            "total_documents": count,
            "documents": documents,
            "sample_shown": len(documents)
        }

def run_ollama_chat(system_prompt, user_prompt, model):
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]
    resp = ollama.chat(model=model, messages=messages)
    return resp["message"]["content"]

if __name__ == "__main__":

    # --- Testing ---

    SYSTEM_PROMPT = (
    """"You are a virtual assistant for a Dungeon Master running Dungeons & Dragons (D&D) sessions.

    Your tasks include:

    - Helping prepare and run sessions by providing ideas, rules clarifications, encounter design, and narrative suggestions.

    - Answering questions using provided campaign documents, focusing only on the relevant content.

    - If no documents are provided, rely on your general D&D knowledge (primarily 5th Edition unless specified).

    Be accurate, concise, and helpful. Prioritize clarity and creativity when assisting with gameplay and storytelling.
    """
    )

    MODEL_EMBED = "mxbai-embed-large"
    MODEL_CHAT = "llama3.1:8b"
    DB_PATH = "markdown_db"
    SOURCE_DIR = r"C:\Users\shive\OneDrive\Documents\DnD\Adventures\Stone-Heart Hollow"
    TOP_K = 5

    collection_name = os.path.basename(SOURCE_DIR)
    chroma_rag = ChromaRag(
        source_directory=SOURCE_DIR,
        collection_name=collection_name,
        db_path=DB_PATH,
        model_name=MODEL_EMBED
    )

    while True:
        print("\n-------------------------------")
        question = input("Ask your question (q to quit): ")
        if question.strip().lower() == "q":
            break

        # docs = chroma_rag.retrieve(question, k=25)
        docs, ids, meta = chroma_rag.retrieve(question, k=25)
        docs_text = "\n---\n".join(docs)

        result = run_ollama_chat(
            system_prompt=SYSTEM_PROMPT,
            user_prompt=f"Here are some relevant information:\n{docs_text}\n\nHere is the query:\n{question}",
            model=MODEL_CHAT
        )

        print(f"\nDMI: {result}")
