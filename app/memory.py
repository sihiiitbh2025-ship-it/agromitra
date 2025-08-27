from __future__ import annotations
from typing import Dict, List

# Very simple in-memory memory store.
# Replace with SQLite/Redis for persistence.
class MemoryStore:
    def __init__(self):
        self._sessions: Dict[str, List[dict]] = {}

    def get_history(self, session_id: str) -> List[dict]:
        return self._sessions.get(session_id, [])

    def append(self, session_id: str, role: str, content: str) -> None:
        self._sessions.setdefault(session_id, []).append({"role": role, "content": content})

    def clear(self, session_id: str) -> None:
        self._sessions.pop(session_id, None)
