from __future__ import annotations
import os
from typing import List, Dict, Any
from dotenv import load_dotenv

load_dotenv()


class BaseProvider:
    def __init__(self):
        self.model = os.getenv("MODEL", "gpt-4o-mini")
        self.system_prompt = os.getenv(
            "SYSTEM_PROMPT",
            "You are a helpful, concise assistant. Answer clearly."
        )

    def generate(self, history: List[Dict[str, str]], user_message: str) -> str:
        raise NotImplementedError


class EchoProvider(BaseProvider):
    """A dummy provider that just echoes the input message."""
    def generate(self, history: List[Dict[str, str]], user_message: str) -> str:
        return f"(echo) You said: {user_message}"


class OpenAIProvider(BaseProvider):
    """Uses OpenAI-compatible APIs (including custom OpenAI endpoints)."""
    def __init__(self):
        super().__init__()
        from openai import OpenAI  # optional import
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        # Optional: os.environ["OPENAI_BASE_URL"] can point to custom OpenAI-compatible servers

    def generate(self, history: List[Dict[str, str]], user_message: str) -> str:
        # Build messages: include system + prior turns + new user message
        messages = [{"role": "system", "content": self.system_prompt}]
        messages.extend(history)
        messages.append({"role": "user", "content": user_message})

        resp = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.7,
        )
        return resp.choices[0].message.content.strip()


class OllamaProvider(BaseProvider):
    """Uses a locally running Ollama server."""
    def __init__(self):
        super().__init__()
        import requests  # local import so requests is optional
        self.requests = requests
        self.host = os.getenv("OLLAMA_HOST", "http://localhost:11434")

    def generate(self, history: List[Dict[str, str]], user_message: str) -> str:
        # Build OpenAI-style chat messages
        messages = [{"role": "system", "content": self.system_prompt}]
        messages.extend(history)
        messages.append({"role": "user", "content": user_message})

        url = f"{self.host}/api/chat"
        r = self.requests.post(
            url,
            json={"model": self.model, "messages": messages, "stream": False}  # 👈 important fix
        )
        r.raise_for_status()
        data = r.json()

        # Parse Ollama’s reply
        if "message" in data and "content" in data["message"]:
            return data["message"]["content"].strip()
        return str(data)
