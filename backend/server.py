"""
Flask Server for D&D Master Interface (DMI)

This module provides a REST API for the DMI application, handling:
1. RAG (Retrieval-Augmented Generation) operations
2. LLM (Language Model) interactions
3. D&D content generation endpoints

The server uses Flask and connects to ChromaDB for document retrieval and
Ollama or llama.cpp for text generation.

Routes:
    /setup: Initialize global variables and objects
    /ask: General question answering
    /gen/*: Content generation endpoints for NPCs, locations, etc.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from rag import ChromaRag
from llm import (
    InstructorAssistant,
    Answer,
    NPCList,
    LocationList,
    PuzzleList,
    ItemList,
    RumourList,
    GeneratedNameList,
)
import os
from typing import Type, TypeVar
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)

app = Flask(__name__)
CORS(app)

# Global variables for maintaining state
model_embed = None
model_chat = None
db_path = None
source_dir = None
chroma_rag = None
instructor_assistant = None


def llm_rag_call(
    request: str,
    instructor_assistant: InstructorAssistant,
    chroma_rag: ChromaRag,
    response_model: Type[T],
    generator=False,
):
    """
    Handle RAG-based LLM queries with structured responses.

    Args:
        request: Flask request object containing query parameters
        instructor_assistant: LLM interface instance
        chroma_rag: RAG system instance
        response_model: Pydantic model for response structure (imported from llm)
        generator: Whether this is a generation request (adds creativity prompt)

    Returns:
        Tuple containing:
        - JSON response dictionary
        - HTTP status code

    Raises:
        400: If no query is provided
        500: For processing errors
    """

    data = request.get_json()
    query = data.get("query")

    if not query:
        return jsonify({"error": "No query provided"}), 400

    try:
        top_k = int(data.get("top_k", 5))

        if generator:
            query = f"This query requires creativity and imagination to generate the following: {query}"

        # saving ids and metadata for later use cases
        docs, ids, metadata = chroma_rag.retrieve(query, k=top_k)
        response = instructor_assistant.ask(
            query=query, context=docs, response_model=response_model
        )
        return jsonify(response.model_dump())

    except Exception as e:
        return jsonify({"error": str(e)}), 500


def check_initialization():
    """
    Check if required global objects are initialized.

    Returns:
        Tuple[Dict, int]: Error response and status code if not initialized,
                         None if initialization check passes
    """
    if chroma_rag is None or instructor_assistant is None:
        return (
            jsonify({"error": "Globals not initialized. Please call /setup first."}),
            400,
        )
    return None


@app.route("/setup", methods=["POST"])
def setup_globals():
    """
    Initialize global variables and objects for the application.

    Expected JSON payload:
        model_embed: Name of embedding model (default: "mxbai-embed-large")
        model_chat: Name of chat model (default: "llama3.1:8b")
        db_path: Path to ChromaDB directory (default: "markdown_db")
        source_dir: Path to markdown documents directory

    Returns:
        Tuple containing:
        - Success message
        - HTTP status code 200
    """

    global model_embed, model_chat, db_path, source_dir
    global chroma_rag, instructor_assistant

    data = request.get_json()

    # Will remove defaults later, but for now, they are useful for testing
    model_embed = data.get("model_embed", "mxbai-embed-large")
    model_chat = data.get("model_chat", "llama3.1:8b")
    db_path = data.get("db_path", "markdown_db")
    source_dir = data.get(
        "source_dir",
        r"C:\Users\shive\OneDrive\Documents\DnD\Adventures\Stone-Heart Hollow",
    )
    print(source_dir)
    # Initialize objects with the new global variables
    collection_name = os.path.basename(source_dir)
    chroma_rag = ChromaRag(
        source_directory=source_dir,
        collection_name=collection_name,
        db_path=db_path,
        model_name=model_embed,
    )

    instructor_assistant = InstructorAssistant(model=model_chat)

    return jsonify({"message": "Globals set successfully"}), 200


@app.route("/", methods=["GET"])
def index():
    return "RAG API is running."


@app.route("/ask", methods=["POST"])
def ask_query():
    """
    Handle general questions using RAG and LLM.

    Expected JSON payload:
        query: Question or prompt to process
        top_k: Number of documents to retrieve (optional, default: 5)

    Returns:
        JSON response with answer and references or error message
    """

    error = check_initialization()
    if error:
        return error

    return llm_rag_call(request, instructor_assistant, chroma_rag, Answer)


# Route handlers for content generation endpoints

"""
All routes below use the same pattern:

Generate details using RAG context.

Expected JSON payload:
    query: NPC generation prompt
    top_k: Number of documents to retrieve (optional, default: 5)

Returns:
    JSON response with NPC details or error message
"""


@app.route("/gen/npc", methods=["POST"])
def gen_npc():
    error = check_initialization()
    if error:
        return error

    return llm_rag_call(
        request, instructor_assistant, chroma_rag, NPCList, generator=True
    )


@app.route("/gen/location", methods=["POST"])
def gen_location():
    error = check_initialization()
    if error:
        return error

    return llm_rag_call(
        request, instructor_assistant, chroma_rag, LocationList, generator=True
    )


@app.route("/gen/puzzle", methods=["POST"])
def gen_puzzle():
    error = check_initialization()
    if error:
        return error

    return llm_rag_call(
        request, instructor_assistant, chroma_rag, PuzzleList, generator=True
    )


@app.route("/gen/item", methods=["POST"])
def gen_item():
    error = check_initialization()
    if error:
        return error

    return llm_rag_call(
        request, instructor_assistant, chroma_rag, ItemList, generator=True
    )


@app.route("/gen/rumour", methods=["POST"])
def gen_rumour():
    error = check_initialization()
    if error:
        return error

    return llm_rag_call(
        request, instructor_assistant, chroma_rag, RumourList, generator=True
    )


@app.route("/gen/name", methods=["POST"])
def gen_name():
    error = check_initialization()
    if error:
        return error

    return llm_rag_call(
        request, instructor_assistant, chroma_rag, GeneratedNameList, generator=True
    )


if __name__ == "__main__":
    app.run(debug=True, port=5000)
