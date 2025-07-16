"""
RAG (Retrieval-Augmented Generation) Implementation using ChromaDB

This module provides a ChromaRag class that implements RAG functionality by:
1. Loading and splitting markdown documents
2. Creating embeddings using Ollama
3. Storing documents and embeddings in ChromaDB
4. Retrieving relevant context for queries

The implementation is specifically tailored for D&D campaign documents but can be used
for any markdown-based knowledge base that largely utlizes markdown headers.
"""

import os
import re
import shutil
from chromadb import PersistentClient
import ollama
from langchain.text_splitter import MarkdownHeaderTextSplitter
from langchain_community.document_loaders import TextLoader, DirectoryLoader


class ChromaRag:
    """
    Implements RAG using ChromaDB for document storage and Ollama for embeddings.

    This class handles the complete RAG pipeline from document ingestion to retrieval:
    - Loads markdown files from a directory
    - Splits documents based on markdown headers
    - Creates embeddings using Ollama
    - Stores documents and embeddings in ChromaDB
    - Retrieves relevant documents for queries

    Attributes:
        source_directory (str): Directory containing markdown files
        collection_name (str): Name of the ChromaDB collection
        db_path (str): Path to store the ChromaDB database
        model_name (str): Name of the Ollama model for embeddings
        collection: ChromaDB collection instance
    """

    def __init__(self, source_directory, collection_name, db_path, model_name):
        """
        Initialize the RAG system.

        Args:
            source_directory (str): Path to directory containing markdown files
            collection_name (str): Name for the ChromaDB collection
            db_path (str): Path where ChromaDB will store its files
            model_name (str): Name of the Ollama model to use for embeddings
        """

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
        """
        Normalize a string for use as a collection or chunk ID.

        Args:
            name (str): String to normalize

        Returns:
            str: Normalized string with special characters replaced by hyphens
        """
        return re.sub(r"[-_. ]+", "-", name).lower()

    def create_rag(self):
        """
        Create the RAG knowledge base from markdown files.

        This method:
        1. Loads all markdown files from the source directory
        2. Splits them based on headers
        3. Processes metadata and content
        4. Creates embeddings
        5. Stores everything in ChromaDB
        """

        headers_to_split_on = [
            ("#", "Header 1"),
            ("##", "Header 2"),
            ("###", "Header 3"),
            ("####", "Header 4"),
            ("#####", "Header 4"),
        ]

        markdown_splitter = MarkdownHeaderTextSplitter(
            headers_to_split_on, strip_headers=False
        )

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

            for i, split in enumerate(splits):

                source_basename = self.normalize(os.path.basename(source)).replace(
                    ".md", ""
                )
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
        """
        Create embeddings for text using Ollama.

        Args:
            text (str): Text to embed

        Returns:
            List[float]: Vector embedding of the text
        """

        resp = ollama.embed(model=self.model_name, input=text)
        return resp["embeddings"]

    def embed_and_store(self, chunk_triples):
        """
        Embed and store document chunks in ChromaDB.

        Args:
            chunk_triples: List of tuples containing (text, metadata, id)
        """

        for text, metadata, id in chunk_triples:
            embeddings = self.embed_text(text)
            self.collection.add(
                ids=[id], embeddings=embeddings, documents=[text], metadatas=[metadata]
            )

    def retrieve(self, query, k=5):
        """
        Retrieve relevant documents for a query.

        Args:
            query (str): Query text to search for
            k (int): Number of documents to retrieve (default: 5)

        Returns:
            Tuple containing:
            - List[str]: Retrieved documents
            - List[str]: Document IDs
            - List[Dict[str, Any]]: Document metadata
        """

        query_embedding = self.embed_text(query)
        results = self.collection.query(query_embeddings=query_embedding, n_results=k)

        return results["documents"][0], results["ids"][0], results["metadatas"][0]

    def inspect_db(self, limit=None):
        """
        Inspect the contents of the ChromaDB collection.

        Args:
            limit (Optional[int]): Maximum number of documents to return

        Returns:
            Dict containing:
            - total_documents: Total number of documents in the collection
            - documents: List of documents (up to limit if specified)
            - sample_shown: Number of documents returned
        """

        count = self.collection.count()
        results = self.collection.get()
        documents = results["documents"]

        if limit:
            documents = documents[:limit]

        return {
            "total_documents": count,
            "documents": documents,
            "sample_shown": len(documents),
        }

