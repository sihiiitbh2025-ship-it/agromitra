# My Chatbot (FastAPI + Pluggable LLM Provider)

A minimal, step-by-step chatbot you can run locally. Choose a provider:
- **OpenAI-compatible API** (easiest if you have an API key)
- **Ollama** (run open-source models locally)
- **Echo** (development fallback that just repeats your input)

## 1) Prerequisites
- Python 3.10+
- (If using OpenAI) An API key
- (If using Ollama) Install and run Ollama (https://ollama.com), e.g. `ollama run llama3.1:8b`

## 2) Setup
```bash
python -m venv .venv
# On macOS/Linux
source .venv/bin/activate
# On Windows (PowerShell)
.venv\Scripts\Activate.ps1

pip install -r requirements.txt
cp .env.example .env
```

Open `.env` and set:
- `PROVIDER=openai` **or** `PROVIDER=ollama` **or** `PROVIDER=echo`
- For OpenAI: set `OPENAI_API_KEY` and `MODEL` (e.g. `gpt-4o-mini`)
- For Ollama: set `MODEL` (e.g. `llama3.1:8b`) and optionally `OLLAMA_HOST` (default `http://localhost:11434`)

## 3) Run
```bash
uvicorn app.main:app --reload
```
Open http://localhost:8000 in your browser.

## 4) Project Structure
```
my-chatbot/
├─ app/
│  ├─ main.py           # FastAPI app & routes
│  ├─ providers.py      # LLM provider implementations (OpenAI, Ollama, Echo)
│  └─ memory.py         # Simple in-memory conversation store (swap for DB later)
├─ static/
│  ├─ index.html        # Minimal chat UI
│  └─ app.js            # Frontend logic
├─ .env.example         # Copy to .env and configure
├─ requirements.txt     # Python dependencies
└─ Dockerfile           # Optional: containerize for deployment
```

## 5) Next Steps (Phase 2: optional enhancements)
- **Persistence**: Replace in-memory memory with SQLite/Redis.
- **RAG**: Add embeddings + vector DB (FAISS, Chroma, Weaviate) to ground answers in your docs.
- **Auth & Roles**: Protect endpoints, add admin panel.
- **Multi-user**: Use session IDs + DB to isolate chat histories.
- **Telemetry**: Log prompts/responses and measure latency & costs.
- **Integrations**: Wire into Telegram, Slack, Discord via their APIs.

Happy building! 🚀
