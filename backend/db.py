import sqlite3
from datetime import datetime
import json

class MemoryDB:
    def __init__(self, db_path="memories.db"):
        self.db_path = db_path
        self.init_db()

    def init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS memories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    client_id TEXT NOT NULL,
                    content TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    type TEXT NOT NULL
                )
            """)
            conn.commit()

    def store_memory(self, client_id: str, content: str, type: str = "conversation"):
        print(f"[MemoryDB] Storing {type} memory for client {client_id[:8]}...")
        print(f"[MemoryDB] Content preview: {content[:100]}...")
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT INTO memories (client_id, content, type) VALUES (?, ?, ?)",
                (client_id, content, type)
            )
            conn.commit()

    def get_recent_memories(self, client_id: str, limit: int = 5):
        print(f"[MemoryDB] Fetching {limit} recent memories for client {client_id[:8]}...")
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT content, timestamp FROM memories WHERE client_id = ? ORDER BY timestamp DESC LIMIT ?",
                (client_id, limit)
            )
            memories = cursor.fetchall()
            print(f"[MemoryDB] Found {len(memories)} memories")
            return memories

    def clear_memories(self, client_id: str):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("DELETE FROM memories WHERE client_id = ?", (client_id,))
            conn.commit()
