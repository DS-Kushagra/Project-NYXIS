# Project‑NYXIS

[![Status: In Development](https://img.shields.io/badge/status-in%20development-yellow.svg)](#)

**Project‑NYXIS** is an open‑source, multi‑modal AI assistant framework that ingests text, documents, images, and more, indexes them in a vector store, and empowers semantic search, RAG‑powered chat, and autonomous agent workflows. Built with FastAPI, LangChain (with Chroma), React/Vite, TailwindCSS, and Hugging Face Transformers, it’s designed as a playground for rapidly prototyping next‑generation AI capabilities—all on free, open‑source tooling.

---

## 🔍 Table of Contents

- [Features](#features)  
- [Architecture & Tech Stack](#architecture--tech-stack)  
- [Getting Started](#getting-started)  
  - [Prerequisites](#prerequisites)  
  - [Backend Setup](#backend-setup)  
  - [Frontend Setup](#frontend-setup)  
- [Usage](#usage)  
  - [Health Check](#health-check)  
  - [Ingest Text & Files](#ingest-text--files)  
  - [Semantic Search](#semantic-search)  
  - [RAG‑Powered Chat](#rag-powered-chat)  
  - [Agent Playground](#agent-playground)  
- [Roadmap](#roadmap)  
- [Contributing](#contributing)  
- [License](#license)

---

## ✨ Features

- **Vector Ingestion**:  
  - Raw text  
  - File uploads (PDF, TXT, MD)  
- **Semantic Search** via Chroma & Sentence‑Transformer embeddings  
- **Retrieval‑Augmented Generation (RAG)** chat using a local Flan‑T5 model  
- **Agent Framework** for chaining tools (search, chat) in autonomous workflows  
- **React/Vite Frontend** with:  
  - Health check  
  - Ingestion forms  
  - Search & chat UIs  
  - Agent playground  
- **Open‑Source‑First**: no paid APIs—fully runnable on CPU/GPU with free libraries  

---

## 🏗 Architecture & Tech Stack

| Layer          | Technology                                     |
| -------------- | ----------------------------------------------:|
| **Backend**    | Python 3.10, FastAPI, Uvicorn                  |
| **AI Core**    | LangChain, Chroma (via `langchain_chroma`), Hugging Face Transformers (Flan‑T5‑small) |
| **Embeddings** | `sentence-transformers/all-MiniLM-L6-v2`       |
| **Frontend**   | React, TypeScript, Vite, TailwindCSS           |
| **Dev Tools**  | Git, GitHub, VS Code                           |

**High‑Level Flow**  
1. User uploads text or files →  
2. FastAPI + LangChain loaders chunk & embed →  
3. Chroma vector DB persists embeddings →  
4. Frontend calls semantic search, chat, or agent endpoints →  
5. Transformers pipeline generates responses or agents orchestrate tools.

---

## 🚀 Getting Started

### Prerequisites

- **Git & GitHub** account  
- **Python 3.10+**  
- **Node.js 16+ & npm**  
- (Optional) GPU + CUDA for faster model inference  

### Backend Setup

```bash
# 1. Clone & enter
git clone git@github.com:<your-username>/project-nyxis.git
cd project-nyxis/backend

# 2. Create venv & install
python -m venv venv
source venv/bin/activate         # (Windows: venv\Scripts\activate)
pip install -r requirements.txt  # or manually install fastapi, uvicorn, langchain, langchain_chroma, transformers, pypdf, nltk, etc.

# 3. (Optional) NLTK punkt
python - <<EOF
import nltk; nltk.download("punkt")
EOF

# 4. Start the API
./run.sh
````

### Frontend Setup

```bash
cd project-nyxis/frontend

# 1. Install deps
npm install

# 2. Start dev server
npm run start
```

Visit the frontend at `http://localhost:5173` (auto‑proxied to `http://localhost:8000` for API calls).

---

## ⚙️ Usage

### Health Check

* **Endpoint**: `GET /health`
* **Frontend**: Dashboard shows “Backend Health: ok” in green.

### Ingest Text & Files

* **Text**: Paste into **Ingest Text** form → POST `/api/ingest`
* **File**: Upload PDF/TXT → multipart POST `/api/ingest-file`

### Semantic Search

* **Form**: **Semantic Search** → query + `k` → GET `/api/query?q=…&k=…`
* **Output**: Top‑k document chunks with metadata.

### RAG‑Powered Chat

* **Form**: **Chat with NYXIS** → send question → POST `/api/chat`
* **Engine**: Retrieves context + generates answer via Flan‑T5 local pipeline.

### Agent Playground

* **Form**: **Agent Playground** → define goal → POST `/api/agent`
* **Tools**: `search_docs`, `chat_rag`
* **Output**: Final agent result (with step logging to be added in future).

---

## 📅 Roadmap

1. **Day 7+**:

   * Formalize agent step logging (callbacks & custom tools)
   * Add proactive triggers (schedules, webhooks)
2. **Document & Media**:

   * Image ingestion (OCR + embeddings)
   * Audio/video ingestion (Whisper)
3. **Persistence & UI Polishing**:

   * User sessions & Memory
   * Interactive timelines & usage analytics
4. **Deployment & CI/CD**:

   * Dockerization
   * GitHub Actions for tests & deploy

*Project is currently paused while foundational concepts are mastered. Expect updates as development resumes.*

---

## 🤝 Contributing

We welcome collaborators! Please:

1. Fork the repo
2. Create a feature branch (`git checkout -b feature/xyz`)
3. Commit your changes & push
4. Open a Pull Request describing your improvements

Refer to [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.

---

## 📜 License

This project is released under the [MIT License](LICENSE).
