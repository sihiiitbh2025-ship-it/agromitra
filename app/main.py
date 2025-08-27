from __future__ import annotations
import os
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

from .memory import MemoryStore
from .providers import EchoProvider, OpenAIProvider, OllamaProvider

load_dotenv()

app = FastAPI(title="My Chatbot")

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

class ChatRequest(BaseModel):
    message: str
    session_id: str

class ClearRequest(BaseModel):
    session_id: str

memory = MemoryStore()

def get_provider_name() -> str:
    return os.getenv("PROVIDER", "echo").lower()

def get_provider():
    provider = get_provider_name()
    if provider == "openai":
        return OpenAIProvider()
    if provider == "ollama":
        return OllamaProvider()
    return EchoProvider()

@app.get("/")
def root():
    index_path = os.path.join(static_dir, "index.html")
    return FileResponse(index_path)

@app.post("/api/chat")
def chat(req: ChatRequest):
    provider = get_provider()
    history = memory.get_history(req.session_id)

    # Append user message
    memory.append(req.session_id, "user", req.message)

    # Generate reply
    try:
        reply = provider.generate(history=history, user_message=req.message)
    except Exception as e:
        reply = f"Provider error: {e}"

    # Append assistant reply
    memory.append(req.session_id, "assistant", reply)

    return JSONResponse({"reply": reply})

@app.post("/api/clear")
def clear(req: ClearRequest):
    memory.clear(req.session_id)
    return JSONResponse({"ok": True})
