from flask import Flask, request, jsonify
from flask_cors import CORS
from rag.vector import ChromaRag
from llm.responses import InstructorAssistant, Answer, NPCList, LocationList, PuzzleList, ItemList, RumourList, GeneratedNameList
import os
from typing import Type, TypeVar
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)

app = Flask(__name__)
CORS(app) 

model_embed = None
model_chat = None
db_path = None
source_dir = None
chroma_rag = None
instructor_assistant = None

def llm_rag_call(request: str, instructor_assistant: InstructorAssistant, chroma_rag: ChromaRag, response_model: Type[T], generator = False):

    data = request.get_json()
    query = data.get("query")

    if not query:
        return jsonify({"error": "No query provided"}), 400

    try:
        top_k = int(data.get("top_k", 5))

        if generator:
            query = f"This query requires creativity and imagination to generate the following: {query}"

        docs, ids, metadata = chroma_rag.retrieve(query, k=top_k)
        response = instructor_assistant.ask(query=query, context=docs, response_model=response_model)
        return jsonify(response.model_dump())

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/setup", methods=["POST"])
def setup_globals():
    global model_embed, model_chat, db_path, source_dir
    global chroma_rag, instructor_assistant

    data = request.get_json()

    # Extract from React payload, validate as needed
    model_embed = data.get("model_embed", "mxbai-embed-large")
    model_chat = data.get("model_chat", "llama3.1:8b")
    db_path = data.get("db_path", "markdown_db")
    source_dir = data.get("source_dir", r"C:\Users\shive\OneDrive\Documents\DnD\Adventures\Stone-Heart Hollow")
    print(source_dir)
    # Initialize objects with the new global variables
    collection_name = os.path.basename(source_dir)
    chroma_rag = ChromaRag(
        source_directory=source_dir,
        collection_name=collection_name,
        db_path=db_path,
        model_name=model_embed
    )

    instructor_assistant = InstructorAssistant(model=model_chat)

    return jsonify({"message": "Globals set successfully"}), 200

@app.route("/", methods=["GET"])
def index():
    return "RAG API is running."

@app.route("/ask", methods=["POST"])
def ask_query():
    global chroma_rag, instructor_assistant

    if chroma_rag is None or instructor_assistant is None:
        return jsonify({"error": "Globals not initialized. Please call /setup first."}), 400

    return llm_rag_call(request, instructor_assistant, chroma_rag, Answer)

@app.route("/gen/npc", methods=["POST"])
def gen_npc():
    global chroma_rag, instructor_assistant

    if chroma_rag is None or instructor_assistant is None:
        return jsonify({"error": "Globals not initialized. Please call /setup first."}), 400

    return llm_rag_call(request, instructor_assistant, chroma_rag, NPCList)

@app.route("/gen/location", methods=["POST"])
def gen_location():
    global chroma_rag, instructor_assistant

    if chroma_rag is None or instructor_assistant is None:
        return jsonify({"error": "Globals not initialized. Please call /setup first."}), 400

    return llm_rag_call(request, instructor_assistant, chroma_rag, LocationList)

@app.route("/gen/puzzle", methods=["POST"])
def gen_puzzle():
    global chroma_rag, instructor_assistant

    if chroma_rag is None or instructor_assistant is None:
        return jsonify({"error": "Globals not initialized. Please call /setup first."}), 400
    
    return llm_rag_call(request, instructor_assistant, chroma_rag, PuzzleList)

@app.route("/gen/item", methods=["POST"])
def gen_item():
    global chroma_rag, instructor_assistant

    if chroma_rag is None or instructor_assistant is None:
        return jsonify({"error": "Globals not initialized. Please call /setup first."}), 400

    return llm_rag_call(request, instructor_assistant, chroma_rag, ItemList)

@app.route("/gen/rumour", methods=["POST"])
def gen_rumour():
    global chroma_rag, instructor_assistant

    if chroma_rag is None or instructor_assistant is None:
        return jsonify({"error": "Globals not initialized. Please call /setup first."}), 400

    return llm_rag_call(request, instructor_assistant, chroma_rag, RumourList)

@app.route("/gen/name", methods=["POST"])
def gen_name():
    global chroma_rag, instructor_assistant

    if chroma_rag is None or instructor_assistant is None:
        return jsonify({"error": "Globals not initialized. Please call /setup first."}), 400

    return llm_rag_call(request, instructor_assistant, chroma_rag, GeneratedNameList)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
