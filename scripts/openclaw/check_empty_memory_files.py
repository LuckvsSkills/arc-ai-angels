from pathlib import Path

ROOTS = [
    Path("/home/prime/arc_ai_angels/agents/nova/workspace/memory"),
    Path("/home/prime/arc_ai_angels/agents/flux/workspace/memory"),
    Path("/home/prime/arc_ai_angels/memory/shared"),
]

count = 0

for root in ROOTS:
    if not root.exists():
        print(f"[WARN] missing root: {root}")
        continue

    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        if path.name.startswith("."):
            continue
        try:
            size = path.stat().st_size
        except FileNotFoundError:
            continue
        if size == 0:
            count += 1
            print(f"[EMPTY] {path}")

print(f"\nEmpty memory file count: {count}")
