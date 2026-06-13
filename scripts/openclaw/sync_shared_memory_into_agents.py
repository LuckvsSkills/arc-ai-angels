from pathlib import Path
import os
import shutil

BASE = Path("/home/prime/arc_ai_angels")
SHARED_ROOT = BASE / "memory" / "shared"

AGENT_MEMORY_ROOTS = {
    "nova": BASE / "agents" / "nova" / "workspace" / "memory",
    "flux": BASE / "agents" / "flux" / "workspace" / "memory",
}

def ensure_dir(path: Path):
    path.mkdir(parents=True, exist_ok=True)

def safe_unlink(path: Path):
    if path.is_symlink() or path.is_file():
        path.unlink()
    elif path.is_dir():
        shutil.rmtree(path)

def main():
    if not SHARED_ROOT.exists():
        raise SystemExit(f"Shared root does not exist: {SHARED_ROOT}")

    total = 0

    for agent, memory_root in AGENT_MEMORY_ROOTS.items():
        if not memory_root.exists():
            print(f"[WARN] missing memory root for {agent}: {memory_root}")
            continue

        target_root = memory_root / "_shared"
        ensure_dir(target_root)

        for src in sorted(SHARED_ROOT.rglob("*")):
            rel = src.relative_to(SHARED_ROOT)
            dst = target_root / rel

            if src.is_dir():
                ensure_dir(dst)
                continue

            if dst.exists() or dst.is_symlink():
                safe_unlink(dst)

            ensure_dir(dst.parent)
            os.symlink(src, dst)
            total += 1
            print(f"[OK] linked for {agent}: {dst} -> {src}")

    print(f"\nShared memory sync complete. Linked {total} file(s).")

if __name__ == "__main__":
    main()
