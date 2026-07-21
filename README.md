# helixops-agentic-rag

**HelixOps Agentic RAG** — self-correcting Retrieval-Augmented Generation powered by Google Gemini 2.5 Flash and LangGraph.

Built by **Abdul Ismail** · https://github.com/ismailubts

---

## Overview

HelixOps RAG is a production-style agentic pipeline that retrieves documents, grades them for relevance, and automatically recovers via a web-search fallback when context is weak. The demo knowledge base uses fictional **HelixOps AI** corporate docs so you can exercise the full loop without external data.

| Capability | Detail |
|------------|--------|
| LLM | Gemini 2.5 Flash |
| Orchestration | LangGraph state machine |
| Store | ChromaDB-compatible JSON seed |
| Reliability | Document grading + self-correction loop |

---

## Architecture

```
Query → Retrieve → Grade
                     │
            relevant?├── yes → Generate → End
                     └── no  → Web Search → Retrieve → Generate → End
```

---

## Stack

- **LLM / Embeddings**: Google Gemini 2.5 Flash + Google native embeddings
- **Framework**: LangChain + LangGraph
- **Vector store**: ChromaDB (seeded JSON under `./chroma_db`)
- **Runtime**: Python 3.10+

---

## Project layout

```
helixops-agentic-rag/
├── requirements.txt
├── state.py                 # AgentState definition
├── nodes.py                 # retrieve / grade / generate / web_search
├── main.py                  # Live Gemini graph entrypoint
├── main_fixed.py            # Mock graph (no API key required)
├── mock_main.py             # Multi-query mock runner
├── seed_db.py               # HelixOps knowledge base seeder
├── mock_seed_db.py          # Offline mock seeder
├── test_self_correction.py  # Self-correction test cases
├── .env.example
└── README.md
```

---

## Setup

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate

pip install -r requirements.txt
cp .env.example .env
# Set GOOGLE_API_KEY in .env for live Gemini runs
```

### Seed the knowledge base

```bash
python seed_db.py
```

### Run (live — needs `GOOGLE_API_KEY`)

```bash
python main.py
```

### Run (mock — no API key)

```bash
python main_fixed.py
# or
python mock_main.py
```

### Tests

```bash
python test_self_correction.py
python test_migration_query.py
```

---

## Demo company data

Seeded documents describe **HelixOps AI** (fictional): architecture, specs, self-correction algorithm, deployment options, 2026 Gemini migration notes, and case studies. Collection name: `helixops_documents`.

Sample query used by the runners:

> Tell me about HelixOps AI's RAG architecture

---

## Configuration sketch

```python
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0,
)

vector_store = {
    "collection_name": "helixops_documents",
    "persist_directory": "./chroma_db",
}
```

---

## Author

**Abdul Ismail**  
Repository: https://github.com/ismailubts/helixops-agentic-rag  

---

HelixOps RAG — agentic retrieval with a self-correction loop.
