# DMI Frontend

A React-based frontend for Dungeon Master Intelligence (DMI), providing an intuitive interface for an AI-powered Dungeons and Dragons writing assistant for Dungeon Masters.

## Features

- **Echo of Delphi**: AI-powered question answering about your campaign
- **Echo Forge**: Generate NPCs, locations, items, and more
- **RAG Integration**: Direct connection to your campaign documents
- **Themed Interface**: D&D-inspired design with scroll textures and fantasy typography
- **Responsive Layout**: Collapsible sidebar and adaptive content areas

## Getting Started

### Prerequisites

- Node.js 18+
- npm or yarn
- Backend server running (see ./backend/README.md)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/shiveshramlall/DMI.git
cd dmi/frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The app will be available at `http://localhost:5173`

## Project Structure

```
frontend/
├── src/
│   ├── components/        # React components
│   │   ├── EchoForge      # Content generation interface
│   │   ├── EchoOfDelphi   # Question answering interface
│   │   ├── RAGSetup       # Configuration component
│   │   └── Sidebar        # Navigation component
│   ├── App.jsx            # Main application component
│   └── main.jsx           # Application entry point
├── public/                # Static assets
└── index.html             # HTML template
```

## Components

### RAGSetup
- Initial configuration for RAG system
- Model selection and document source setup

### EchoOfDelphi
- Campaign knowledge query interface
- Context-aware responses with source references

### EchoForge
- D&D content generation tools
- Support for NPCs, locations, items, puzzles, etc.

### Sidebar
- Navigation between components
- Collapsible interface
- Campaign source indicator and reloader

## Styling

- Uses custom CSS with fantasy-themed design
- Fonts: Cinzel, Cinzel Decorative, and Spectral
- Scroll textures and parchment backgrounds

## Dependencies

- Windows 11 (not tested on any other OS)
  - This should only really imapct how CUDA is setup if you wish to utilize custom configurations on your GPU, for the LLM model.
- React 19.1.0
- Vite 7.0.4
- Axios for API calls
- Lucide React for icons
- React Markdown for text rendering
