# DMI Backend

Dungeon Master Intelligence (DMI) is a Flask-based backend service that provides AI-powered tools for Dungeon Masters creating and running D&D games. It combines RAG (Retrieval-Augmented Generation) with LLMs to generate D&D content and answer campaign-specific questions.

## Table of Contents
- [DMI Backend](#dmi-backend)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Configuration](#configuration)
    - [Custom Model Requirements](#custom-model-requirements)
  - [Installation](#installation)
  - [API Endpoints](#api-endpoints)
    - [Setup](#setup)
    - [Question Answering](#question-answering)
    - [Content Generation](#content-generation)
  - [Project Structure](#project-structure)
  - [Usage Example](#usage-example)
  - [Development](#development)

## Features

- 📚 **RAG System**: Uses ChromaDB for document storage and retrieval
- 🤖 **LLM Integration**: Supports both Ollama and llama.cpp models
- 🎲 **D&D Content Generation**: NPCs, locations, items, puzzles, and more
- 📝 **Campaign Document Integration**: Uses your markdown files as context
- 🔍 **Smart Query System**: Retrieves relevant context for accurate responses

## Configuration

The system requires:
- Source location of markdown files for campaign documents
- An embedding model (download via Ollama)
- A chat model (download via Ollama)
  - Alternatively, a custom model can be ran with llama-cpp. You can download the gguf file via LMStudio. 
  - Modify the llm/responses.py accordingly. Configuration will have to be tested and done on your machine.

### Custom Model Requirements
- [CUDA](https://developer.nvidia.com/cuda-downloads)
- [MS Build Tools](https://visualstudio.microsoft.com/downloads/?q=build+tools)
  - Desktop development with C++
  - CMake support and Windows 10/11 SDK
> Note: I had to do a workaround to get this to run properly, as my CUDA toolset was not being detected properly

Copy files from :
`C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.x\extras\visual_studio_integration\MSBuildExtensions`
To: `C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\MSBuild\Microsoft\VC\v170\BuildCustomizations`

Then, set these commands before pip installing requirements.txt:
```bash
$env:CMAKE_ARGS="-DGGML_CUDA=on"
$env:CUDACXX="C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.x\bin\nvcc.exe"
```

## Installation

1. Clone the repository:
```bash
git clone [your-repo-url]
cd dmi/backend
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

Note: For CUDA support with llama-cpp-python, use:
```bash
pip install llama-cpp-python==0.3.13 -C cmake.args="-DGGML_CUDA=on"
```

If needed: 
```bash
pip install llama-cpp-python --force-reinstall --upgrade --no-cache-dir --verbose
```


## API Endpoints

### Setup
- `POST /setup`: Initialize the system
```json
{
    "model_embed": "mxbai-embed-large",
    "model_chat": "llama3.1:8b",
    "db_path": "markdown_db",
    "source_dir": "path/to/markdown/files"
}
```

### Question Answering
- `POST /ask`: General queries about campaign content
```json
{
    "query": "What happened in Evermere?",
    "top_k": 5
}
```

### Content Generation
All generation endpoints accept:
```json
{
    "query": "A generation prompt to create something",
    "top_k": 5
}
```

Available endpoints:
- `POST /gen/npc`: Generate NPCs
- `POST /gen/location`: Generate locations
- `POST /gen/puzzle`: Generate puzzles
- `POST /gen/item`: Generate items
- `POST /gen/rumour`: Generate rumors
- `POST /gen/name`: Generate fantasy names

## Project Structure

```
backend/
├── llm/                    # LLM interaction models
│   ├── __init__.py
│   └── responses.py        # Pydantic models for responses
├── rag/                    # RAG implementation
│   ├── __init__.py
│   └── vector.py           # ChromaDB integration
├── requirements.txt        # Project dependencies
└── server.py               # Flask API server
```

## Usage Example

1. Start the server:
```bash
python server.py
```

2. Initialize the system:
```bash
curl -X POST http://localhost:5000/setup -H "Content-Type: application/json" -d '{
    "source_dir": "path/to/campaign/docs"
}'
```

3. Generate an NPC:
```bash
curl -X POST http://localhost:5000/gen/npc -H "Content-Type: application/json" -d '{
    "query": "Generate a mysterious tavern keeper"
}'
```

## Development

- Built with python 3.12.0 (on a Windows 11 machine)
- Flask for the REST API
- Pydantic (via Instructor) for data validation and structured LLM outputs
- ChromaDB for vector storage
- Langchain for Markdown file parsing, chunking by section headers
- Ollama and llama-cpp-python for chat completions