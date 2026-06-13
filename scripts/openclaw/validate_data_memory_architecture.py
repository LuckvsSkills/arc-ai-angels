from pathlib import Path
import sqlite3
import sys

BASE = Path("/home/prime/arc_ai_angels")
DB_PATH = BASE / "data" / "system.db"

REQUIRED_DIRS = [
    BASE / "data",
    BASE / "memory",
    BASE / "memory" / "shared",
    BASE / "memory" / "shared" / "global",
    BASE / "memory" / "shared" / "operational",
    BASE / "memory" / "shared" / "project",
    BASE / "memory" / "shared" / "summaries",
    BASE / "memory" / "shared" / "registry",
    BASE / "memory" / "archive",
    BASE / "agents" / "nova" / "workspace" / "memory",
    BASE / "agents" / "flux" / "workspace" / "memory",
    BASE / "agents" / "nova" / "workspace" / "memory" / "inbox",
    BASE / "agents" / "nova" / "workspace" / "memory" / "notes",
    BASE / "agents" / "nova" / "workspace" / "memory" / "summaries",
    BASE / "agents" / "nova" / "workspace" / "memory" / "registry",
    BASE / "agents" / "flux" / "workspace" / "memory" / "inbox",
    BASE / "agents" / "flux" / "workspace" / "memory" / "notes",
    BASE / "agents" / "flux" / "workspace" / "memory" / "summaries",
    BASE / "agents" / "flux" / "workspace" / "memory" / "registry",
]

REQUIRED_FILES = [
    BASE / "agents" / "nova" / "workspace" / "memory" / "notes" / "system-baseline.md",
    BASE / "agents" / "flux" / "workspace" / "memory" / "notes" / "system-baseline.md",
    BASE / "memory" / "shared" / "global" / "data-memory-policy.md",
    BASE / "memory" / "shared" / "operational" / "current-system-state.md",
    BASE / "memory" / "shared" / "project" / "project-baseline.md",
]

REQUIRED_TABLES = {
    "agents",
    "memory_sources",
    "memory_chunks",
    "memory_events",
    "system_paths",
    "shared_memory_access",
}

REQUIRED_SYSTEM_PATHS = {
    "/home/prime/arc_ai_angels",
    "/home/prime/.openclaw",
    "/home/prime/arc_ai_angels/data/system.db",
    "/home/prime/arc_ai_angels/memory/shared",
    "/home/prime/arc_ai_angels/memory/shared/global",
    "/home/prime/arc_ai_angels/memory/shared/operational",
    "/home/prime/arc_ai_angels/memory/shared/project",
    "/home/prime/arc_ai_angels/memory/shared/summaries",
    "/home/prime/arc_ai_angels/memory/shared/registry",
    "/home/prime/arc_ai_angels/memory/archive",
}

def fail(msg):
    print(f"[FAIL] {msg}")

def ok(msg):
    print(f"[OK] {msg}")

errors = 0

for path in REQUIRED_DIRS:
    if path.exists() and path.is_dir():
        ok(f"dir exists: {path}")
    else:
        errors += 1
        fail(f"missing dir: {path}")

for path in REQUIRED_FILES:
    if path.exists() and path.is_file():
        ok(f"file exists: {path}")
    else:
        errors += 1
        fail(f"missing file: {path}")

if DB_PATH.exists():
    ok(f"database exists: {DB_PATH}")
else:
    errors += 1
    fail(f"missing database: {DB_PATH}")

if DB_PATH.exists():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = {row[0] for row in cur.fetchall()}
    for table in sorted(REQUIRED_TABLES):
        if table in tables:
            ok(f"table exists: {table}")
        else:
            errors += 1
            fail(f"missing table: {table}")

    cur.execute("SELECT path FROM system_paths")
    system_paths = {row[0] for row in cur.fetchall()}
    for p in sorted(REQUIRED_SYSTEM_PATHS):
        if p in system_paths:
            ok(f"system path registered: {p}")
        else:
            errors += 1
            fail(f"system path missing from DB: {p}")

    cur.execute("SELECT COUNT(*) FROM memory_sources WHERE visibility='shared'")
    shared_count = cur.fetchone()[0]
    if shared_count >= 3:
        ok(f"shared memory sources registered: {shared_count}")
    else:
        errors += 1
        fail(f"expected at least 3 shared memory sources, got {shared_count}")

    cur.execute("SELECT COUNT(*) FROM shared_memory_access")
    access_count = cur.fetchone()[0]
    if access_count >= 6:
        ok(f"shared memory access rules registered: {access_count}")
    else:
        errors += 1
        fail(f"expected at least 6 shared access rows, got {access_count}")

    conn.close()

shared_links = [
    BASE / "agents" / "nova" / "workspace" / "memory" / "_shared",
    BASE / "agents" / "flux" / "workspace" / "memory" / "_shared",
]

for path in shared_links:
    if path.exists() and path.is_dir():
        ok(f"shared mirror exists: {path}")
    else:
        errors += 1
        fail(f"missing shared mirror: {path}")

print(f"\nValidation complete. Errors: {errors}")
sys.exit(1 if errors else 0)
