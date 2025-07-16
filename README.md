# DMI (Dungeon Master Intelligence)

DMI is an AI-powered assistant for Dungeon Masters running D&D games. It combines RAG (Retrieval-Augmented Generation) with LLMs to provide intelligent responses from your campaign documents and generate D&D ideas, inspiration and content.

### Backend
- Flask for API server
- ChromaDB for vector storage
- Instructor for structured LLM outputs
- Langchain for document processing
- Ollama and llama.cpp (allows more configuration) for LLM inference

### Frontend
- React with Vite
- Axios for API calls
- Custom themed CSS
- React Markdown
- Lucide icons

![DMI Interface](frontend/public/DMI-Home.png)

## Features

### 🎭 Echo of Delphi
- AI-powered question answering about your campaign
- Context-aware responses using your campaign documents
- Source references for answers
- Adjustable context depth
- Can be used to help supplement the writing process of adventures

### ⚒️ Echo Forge
- Generate D&D content with campaign context:
  - NPCs with personalities and secrets
  - Locations with descriptions and rumors
  - Puzzles with solutions and hints
  - Magic items with effects
  - Local rumors and plot hooks
  - Fantasy names with cultural context

### 📚 RAG System
- Document indexing and retrieval using ChromaDB
- Markdown-based campaign document integration
- Smart context selection for queries
- Header-based document chunking

## Getting Started

### Prerequisites

- Python 3.12+ for backend
- Node.js 18+ for frontend
- CUDA-capable GPU (optional, for local models)
- Ollama or local GGUF models

### Installation

1. Clone the repository:
```bash
git clone [your-repo-url]
cd dmi
```

2. Set up the backend:
```bash
cd backend
pip install -r requirements.txt
```

3. Set up the frontend:
```bash
cd frontend
npm install
```

### Configuration

1. Start Ollama and download models:
```bash
ollama pull mxbai-embed-large
ollama pull llama3.1:8b
```

2. Start the backend server:
```bash
cd backend
python server.py
```

3. Start the frontend:
```bash
cd frontend
npm run dev
```

4. Access the UI at `http://localhost:5173`

## Project Structure

```
dmi/
├── backend/                # Flask server and AI components
│   ├── llm/               # LLM interaction models
│   ├── rag/               # RAG implementation
│   └── server.py          # Flask API
└── frontend/              # React application
    ├── src/
    │   ├── components/    # React components
    │   └── App.jsx        # Main app
    └── public/            # Static assets
```

## Technologies Used

### Backend
- Flask for API server
- ChromaDB for vector storage
- Instructor for structured LLM outputs
- Langchain for document processing
- Ollama/llama.cpp for LLM inference

### Frontend
- React with Vite
- Axios for API calls
- Custom themed CSS
- React Markdown
- Lucide icons

## Development

### Backend Development
```bash
cd backend
python server.py
```

### Frontend Development
```bash
cd frontend
npm run dev
```

## Example - Echo of Delphi

![Echo of Delphi](frontend/public/DMI-Delphi-Example.png)

## Example - Echo Forge

![Echo Forge](frontend/public/DMI-Forge-Example.png)