from pathlib import Path
import sqlite3

DB_PATH = Path("/home/prime/arc_ai_angels/data/system.db")

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.execute("PRAGMA table_info(memory_sources)")
columns = cur.fetchall()
column_names = [c[1] for c in columns]

if "source_path" not in column_names:
    raise RuntimeError("memory_sources table missing source_path")

cur.execute("PRAGMA index_list(memory_sources)")
indexes = cur.fetchall()
index_names = [idx[1] for idx in indexes]

if "idx_memory_sources_source_path_unique" not in index_names:
    cur.execute("""
        CREATE UNIQUE INDEX IF NOT EXISTS idx_memory_sources_source_path_unique
        ON memory_sources(source_path)
    """)

conn.commit()
conn.close()

print("Database repaired: unique index on memory_sources(source_path) is ready.")
