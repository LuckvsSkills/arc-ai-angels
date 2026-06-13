from pathlib import Path
import sqlite3

BASE = Path("/home/prime/arc_ai_angels")
DB_PATH = BASE / "data" / "system.db"
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS agents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    workspace_path TEXT NOT NULL,
    memory_path TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS memory_sources (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    agent_name TEXT NOT NULL,
    source_path TEXT NOT NULL,
    source_type TEXT,
    checksum TEXT,
    is_active INTEGER DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS memory_chunks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_id INTEGER NOT NULL,
    chunk_index INTEGER NOT NULL,
    content_preview TEXT,
    embedding_backend TEXT,
    embedding_model TEXT,
    vector_store_ref TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(source_id) REFERENCES memory_sources(id)
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS memory_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    agent_name TEXT NOT NULL,
    event_type TEXT NOT NULL,
    content TEXT,
    source_path TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS system_paths (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    path TEXT UNIQUE NOT NULL,
    role TEXT NOT NULL,
    is_source_of_truth INTEGER DEFAULT 0,
    notes TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

agents = [
    (
        "nova",
        "/home/prime/arc_ai_angels/agents/nova/workspace",
        "/home/prime/arc_ai_angels/agents/nova/workspace/memory",
    ),
    (
        "flux",
        "/home/prime/arc_ai_angels/agents/flux/workspace",
        "/home/prime/arc_ai_angels/agents/flux/workspace/memory",
    ),
]

for row in agents:
    cur.execute("""
    INSERT OR IGNORE INTO agents (name, workspace_path, memory_path)
    VALUES (?, ?, ?)
    """, row)

paths = [
    ("/home/prime/arc_ai_angels", "project-root", 1, "Primary source of truth"),
    ("/home/prime/.openclaw", "runtime-cache", 0, "OpenClaw runtime/index/cache only"),
    ("/home/prime/arc_ai_angels/agents/nova/workspace/memory", "agent-memory", 0, "Active retrieval memory for Nova"),
    ("/home/prime/arc_ai_angels/agents/flux/workspace/memory", "agent-memory", 0, "Active retrieval memory for Flux"),
    ("/home/prime/arc_ai_angels/data/system.db", "structured-storage", 0, "Structured state and memory metadata"),
]

for row in paths:
    cur.execute("""
    INSERT OR IGNORE INTO system_paths (path, role, is_source_of_truth, notes)
    VALUES (?, ?, ?, ?)
    """, row)

conn.commit()
conn.close()

print(f"Database initialized at: {DB_PATH}")
