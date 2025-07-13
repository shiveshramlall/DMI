from langchain.text_splitter import MarkdownHeaderTextSplitter
from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
import os


def markdown_rag(
    source_directory,
    collection_name,
    db_path="markdown_db",
    model_name: str = "mxbai-embed-large",
):

    add_documents = not os.path.exists(db_path)
    embeddings = OllamaEmbeddings(model="mxbai-embed-large")

    chunks = []
    if add_documents:

        headers_to_split_on = [
            ("#", "Header 1"),
            ("##", "Header 2"),
            ("###", "Header 3"),
            ("####", "Header 4"),
            ("#####", "Header 4"),
        ]
        markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on, strip_headers=False,)

        loader = DirectoryLoader(
            source_directory,
            glob="**/*.md",
            loader_cls=TextLoader,
            loader_kwargs={"encoding": "utf-8"},
        )
        docs = loader.load()
        
        for doc in docs:

            text = doc.page_content
            splits = markdown_splitter.split_text(text)
            chunks.extend(splits)

        vector_store = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory=db_path,
            collection_name=collection_name,
        )

    vector_store = Chroma(
        collection_name=collection_name,
        persist_directory=db_path,
        embedding_function=embeddings,
    )

    if add_documents:
        vector_store.add_documents(documents=chunks)

    retriever = vector_store.as_retriever(search_kwargs={"k": 5})
    return retriever