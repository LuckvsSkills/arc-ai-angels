from pathlib import Path
import sqlite3

DB_PATH = Path("/home/prime/arc_ai_angels/data/system.db")

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

print("=== agents ===")
for row in cur.execute("SELECT id, name, workspace_path, memory_path, created_at FROM agents ORDER BY name"):
    print(row)

print("\n=== system_paths ===")
for row in cur.execute("SELECT id, path, role, is_source_of_truth, notes FROM system_paths ORDER BY id"):
    print(row)

print("\n=== memory_sources ===")
for row in cur.execute("""
    SELECT id, agent_name, source_type, visibility, source_path, substr(checksum,1,12), is_active, created_at, updated_at
    FROM memory_sources
    ORDER BY agent_name, source_path
"""):
    print(row)

print("\n=== shared_memory_access ===")
for row in cur.execute("""
    SELECT id, agent_name, shared_scope, can_read, can_write, created_at
    FROM shared_memory_access
    ORDER BY agent_name, shared_scope
"""):
    print(row)

conn.close()
