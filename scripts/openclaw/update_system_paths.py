from pathlib import Path
import sqlite3

DB_PATH = Path("/home/prime/arc_ai_angels/data/system.db")

ROWS = [
    ("/home/prime/arc_ai_angels/memory/shared", "shared-memory-root", 0, "Canonical shared multi-agent memory root"),
    ("/home/prime/arc_ai_angels/memory/shared/global", "shared-memory-scope", 0, "Global shared memory scope"),
    ("/home/prime/arc_ai_angels/memory/shared/operational", "shared-memory-scope", 0, "Operational shared memory scope"),
    ("/home/prime/arc_ai_angels/memory/shared/project", "shared-memory-scope", 0, "Project shared memory scope"),
    ("/home/prime/arc_ai_angels/memory/shared/summaries", "shared-memory-scope", 0, "Shared summaries scope"),
    ("/home/prime/arc_ai_angels/memory/shared/registry", "shared-memory-scope", 0, "Shared registry scope"),
    ("/home/prime/arc_ai_angels/memory/archive", "memory-archive", 0, "Archive-only memory storage"),
]

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

for row in ROWS:
    cur.execute("""
        INSERT OR IGNORE INTO system_paths (path, role, is_source_of_truth, notes)
        VALUES (?, ?, ?, ?)
    """, row)

conn.commit()
conn.close()

print("System paths updated.")
