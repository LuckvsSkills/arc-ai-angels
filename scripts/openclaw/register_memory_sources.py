from pathlib import Path
import sqlite3
import hashlib

BASE = Path("/home/prime/arc_ai_angels")
DB_PATH = BASE / "data" / "system.db"

MEMORY_ROOTS = {
    "nova": BASE / "agents" / "nova" / "workspace" / "memory",
    "flux": BASE / "agents" / "flux" / "workspace" / "memory",
    "__shared__": BASE / "memory" / "shared",
}

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def detect_source_type(path: Path) -> str:
    parts = set(path.parts)
    if "inbox" in parts:
        return "inbox"
    if "notes" in parts:
        return "note"
    if "summaries" in parts:
        return "summary"
    if "registry" in parts:
        return "registry"
    if "global" in parts:
        return "shared-global"
    if "operational" in parts:
        return "shared-operational"
    if "project" in parts:
        return "shared-project"
    return "unknown"

def detect_visibility(agent_name: str) -> str:
    return "shared" if agent_name == "__shared__" else "private"

def normalized_agent_name(agent_name: str) -> str:
    return "shared" if agent_name == "__shared__" else agent_name

def main():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    total = 0

    for agent_name, root in MEMORY_ROOTS.items():
        if not root.exists():
            print(f"[WARN] missing memory root for {agent_name}: {root}")
            continue

        for path in sorted(root.rglob("*")):
            if not path.is_file():
                continue
            if path.name.startswith("."):
                continue

            checksum = sha256_file(path)
            source_type = detect_source_type(path)
            visibility = detect_visibility(agent_name)
            owner = normalized_agent_name(agent_name)

            cur.execute("""
                INSERT INTO memory_sources (
                    agent_name,
                    source_path,
                    source_type,
                    checksum,
                    is_active,
                    visibility
                )
                VALUES (?, ?, ?, ?, 1, ?)
                ON CONFLICT(source_path) DO UPDATE SET
                    agent_name=excluded.agent_name,
                    source_type=excluded.source_type,
                    checksum=excluded.checksum,
                    is_active=1,
                    visibility=excluded.visibility,
                    updated_at=CURRENT_TIMESTAMP
            """, (
                owner,
                str(path),
                source_type,
                checksum,
                visibility,
            ))

            total += 1
            print(f"[OK] registered {owner}: {path}")

    conn.commit()
    conn.close()
    print(f"\nRegistered/updated {total} memory source file(s).")

if __name__ == "__main__":
    main()
