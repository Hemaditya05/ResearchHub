# ResearchHub AI

## Overview

ResearchHub AI is an intelligent research paper discovery, summarization, and workspace management platform powered by AI. The system helps students, researchers, and professionals efficiently discover, organize, analyze, and interact with academic research papers.

The platform combines:

* AI-powered research assistance
* Research paper discovery
* PDF upload and document processing
* Semantic search using embeddings
* Workspace-based organization
* AI-generated summaries and insights
* Conversational interaction with research papers

The project integrates a FastAPI backend, Streamlit frontend, vector embeddings, and Groq-powered LLaMA models to create a complete academic research assistant.

---

# Features

## AI-Powered Research Assistant

* Ask questions about uploaded research papers
* Generate contextual AI responses
* Extract insights from academic documents
* Support research understanding and analysis

## Research Paper Discovery

* Search research papers using keywords or topics
* Discover papers from external sources such as arXiv
* Retrieve relevant academic content dynamically

## PDF Upload and Processing

* Upload research papers in PDF format
* Extract document text automatically
* Process content for summarization and AI interaction

## Research Paper Summarization

* Generate concise summaries of papers
* Extract key points and findings
* Reduce manual reading effort

## Semantic Search

* Generate embeddings using Sentence Transformers
* Store embeddings in ChromaDB
* Perform similarity-based research search

## Workspace Management

* Create separate workspaces for research topics
* Organize papers, summaries, and notes
* Maintain structured research collections

---

# Tech Stack

## Frontend

* Streamlit
* React concepts
* HTML
* CSS

## Backend

* FastAPI
* Python

## AI and NLP

* Groq API
* LLaMA 3.3 70B Versatile
* Sentence Transformers

## Database and Storage

* ChromaDB

## Document Processing

* PyPDF
* PDF text extraction libraries

---

# Project Architecture

The system follows a modular architecture:

1. User uploads or discovers research papers
2. Backend extracts and processes document text
3. Embeddings are generated and stored in ChromaDB
4. AI services process prompts and generate responses
5. Frontend displays summaries, chat responses, and workspace content

---

# Project Structure

```text
ResearchHub/
│
├── backend/
│   ├── assistant_router.py
│   ├── chat.py
│   ├── discovery.py
│   ├── discovery_router.py
│   ├── embeddings.py
│   ├── main.py
│   ├── summarize_router.py
│   ├── upload.py
│   ├── workspace.py
│   └── workspace_router.py
│
├── frontend/
│   ├── app.py
│   └── pages/
│       ├── chat.py
│       ├── home.py
│       └── uploads.py
│
├── requirements.txt
├── .env
└── README.md
```

---

# Installation

## Clone the Repository

```bash
git clone <repository-url>
cd ResearchHub
```

## Create Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

---

# Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file in the root directory.

```env
GROQ_API_KEY=your_groq_api_key
```

Generate your API key from:

* [https://console.groq.com/keys](https://console.groq.com/keys)

---

# Backend Setup

Run the FastAPI backend:

```bash
uvicorn backend.main:app --reload
```

Backend URL:

```text
http://127.0.0.1:8000
```

---

# Frontend Setup

Run the Streamlit frontend:

```bash
streamlit run frontend/app.py
```

Frontend URL:

```text
http://localhost:8501
```

---

# Core Backend Modules

## upload.py

* Handles PDF uploads
* Extracts research paper text
* Sends documents for processing

## embeddings.py

* Generates vector embeddings
* Stores embeddings in ChromaDB
* Enables semantic similarity search

## chat.py

* Handles AI chat interactions
* Answers questions from uploaded papers
* Generates contextual responses

## discovery.py

* Fetches research papers from external sources
* Supports topic-based discovery
* Integrates with arXiv APIs

## summarize_router.py

* Generates AI-powered paper summaries
* Returns concise research overviews

## assistant_router.py

* Handles AI research assistance
* Supports question answering and analysis

## workspace.py

* Manages research workspaces
* Organizes papers and summaries

## main.py

* Main FastAPI entry point
* Registers backend routes
* Initializes API server

---

# Frontend Pages

## home.py

* Dashboard page
* Displays overview and statistics
* Shows uploaded papers and workspace details

## uploads.py

* Upload interface for PDFs
* Sends files to backend APIs

## chat.py

* Conversational AI interface
* Displays AI-generated responses

## app.py

* Main frontend controller
* Handles navigation and session state

---

# System Workflow

1. User enters the platform
2. User creates or opens a workspace
3. User uploads PDFs or discovers papers
4. Backend extracts and processes content
5. Embeddings are generated for semantic search
6. AI generates summaries and answers
7. Results are stored in the workspace

---

# API Features

The backend provides APIs for:

* PDF uploads
* AI chat interactions
* Research paper discovery
* Semantic search
* Summarization
* Workspace management

---

# Future Improvements

* Multi-user collaboration
* Advanced semantic search
* Citation generation
* Research recommendation engine
* Cloud storage integration
* Research graph visualization
* Authentication and access control

---

# Learning Requirements

Before working on this project, knowledge of the following is recommended:

* Python programming
* FastAPI or Flask
* Streamlit
* React basics
* AI APIs and LLMs
* Prompt engineering
* PDF processing
* Vector embeddings
* Semantic search

---

# Conclusion

ResearchHub AI demonstrates how modern AI systems can improve academic research workflows through intelligent discovery, summarization, semantic search, and conversational interaction with research papers.

The platform acts as a centralized research workspace that helps users manage and understand academic literature more efficiently while reducing manual effort.
