#!/usr/bin/env python3
import json
import sys
from pathlib import Path

VALID = {"planned", "started", "finished"}

if len(sys.argv) != 3:
    print("Usage: set_block_status.py <block_id> <planned|started|finished>")
    sys.exit(1)

block_id = sys.argv[1].strip()
new_status = sys.argv[2].strip().lower()

if new_status not in VALID:
    print(f"Invalid status: {new_status}")
    print("Valid: planned, started, finished")
    sys.exit(1)

path = Path.home() / "arc_strategic_control_center" / "data" / "project_structure.json"
data = json.loads(path.read_text(encoding="utf-8"))

found = False

for chapter in data.get("chapters", []):
    for cluster in chapter.get("clusters", []):
        for block in cluster.get("blocks", []):
            if block.get("id") == block_id:
                old = block.get("status", "planned")
                block["status"] = new_status
                found = True
                print(f"Updated {block_id}: {old} -> {new_status}")

                # cluster status recalculatie
                statuses = [b.get("status", "planned") for b in cluster.get("blocks", [])]
                if all(s == "finished" for s in statuses):
                    cluster["status"] = "finished"
                elif any(s == "started" for s in statuses) or any(s == "finished" for s in statuses):
                    cluster["status"] = "started"
                else:
                    cluster["status"] = "planned"

                # chapter status recalculatie
                chapter_statuses = []
                for cl in chapter.get("clusters", []):
                    chapter_statuses.append(cl.get("status", "planned"))
                if all(s == "finished" for s in chapter_statuses):
                    chapter["status"] = "finished"
                elif any(s == "started" for s in chapter_statuses) or any(s == "finished" for s in chapter_statuses):
                    chapter["status"] = "started"
                else:
                    chapter["status"] = "planned"

if not found:
    print(f"Block not found: {block_id}")
    sys.exit(1)

path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Saved {path}")
