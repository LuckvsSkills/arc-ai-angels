from pathlib import Path
import sqlite3

DB_PATH = Path("/home/prime/arc_ai_angels/data/system.db")

ACCESS_RULES = [
    ("nova", "global", 1, 0),
    ("nova", "operational", 1, 0),
    ("nova", "project", 1, 0),
    ("flux", "global", 1, 0),
    ("flux", "operational", 1, 0),
    ("flux", "project", 1, 0),
]

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

for row in ACCESS_RULES:
    cur.execute("""
        INSERT INTO shared_memory_access (agent_name, shared_scope, can_read, can_write)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(agent_name, shared_scope) DO UPDATE SET
            can_read=excluded.can_read,
            can_write=excluded.can_write
    """, row)

conn.commit()
conn.close()

print("Shared memory access rules registered.")
