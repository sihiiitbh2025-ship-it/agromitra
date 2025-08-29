from __future__ import annotations
import os
from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

from .memory import MemoryStore
from .providers import EchoProvider, OpenAIProvider, OllamaProvider

# 🔹 Import RAG
from .rag import RAG

load_dotenv()

app = FastAPI(title="AgroMitra Chatbot")

# CORS (open by default; tighten for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files (frontend)
static_dir = os.path.join(os.path.dirname(__file__), "..", "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Schemas
class ChatRequest(BaseModel):
    message: str
    session_id: str

class ClearRequest(BaseModel):
    session_id: str

# Global memory + RAG
memory = MemoryStore()
rag = RAG()  # will use knowledge.txt internally

# Provider selection
def get_provider_name() -> str:
    return os.getenv("PROVIDER", "echo").lower()

def get_provider():
    provider = get_provider_name()
    if provider == "openai":
        return OpenAIProvider()
    if provider == "ollama":
        return OllamaProvider()
    return EchoProvider()

# Routes
@app.get("/")
def root():
    index_path = os.path.join(static_dir, "index.html")
    return FileResponse(index_path)

@app.post("/api/chat")
def chat(req: ChatRequest):
    provider = get_provider()
    history = memory.get_history(req.session_id)

    # Store user message
    memory.append(req.session_id, "user", req.message)

    # 🔹 Query RAG
    results = rag.query(req.message, k=5)

    # 🔹 Debug: print retrieved documents
    print("=== RAG Retrieved Documents ===")
    for i, r in enumerate(results, 1):
        doc_text = r["doc"] if isinstance(r, dict) else str(r)
        print(f"{i}: {doc_text}")
    print("===============================")

    # 🔹 Combine context for the provider
    context = "\n".join([r["doc"] if isinstance(r, dict) else str(r) for r in results])
    augmented_message = f"""
    Use the following context to answer the user.

    Context:
    {context}

    User: {req.message}
    """

    # Provider response
    try:
        reply = provider.generate(history=history, user_message=augmented_message)
    except Exception as e:
        reply = f"Provider error: {e}"

    # Store assistant reply
    memory.append(req.session_id, "assistant", reply)

    return JSONResponse({
        "reply": reply,
        # 🔹 Optional: return RAG docs to frontend for testing
        "rag_docs": [r["doc"] if isinstance(r, dict) else str(r) for r in results]
    })

@app.post("/api/clear")
def clear(req: ClearRequest):
    memory.clear(req.session_id)
    return JSONResponse({"ok": True})
