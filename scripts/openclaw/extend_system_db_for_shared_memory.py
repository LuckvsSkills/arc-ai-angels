from pathlib import Path
import sqlite3

DB_PATH = Path("/home/prime/arc_ai_angels/data/system.db")

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.execute("PRAGMA table_info(memory_sources)")
cols = [row[1] for row in cur.fetchall()]

if "visibility" not in cols:
    cur.execute("ALTER TABLE memory_sources ADD COLUMN visibility TEXT DEFAULT 'private'")

cur.execute("""
CREATE TABLE IF NOT EXISTS shared_memory_access (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    agent_name TEXT NOT NULL,
    shared_scope TEXT NOT NULL,
    can_read INTEGER DEFAULT 1,
    can_write INTEGER DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(agent_name, shared_scope)
)
""")

conn.commit()
conn.close()

print("Shared memory schema is ready.")
