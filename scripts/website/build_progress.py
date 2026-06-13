#!/usr/bin/env python3
import json
from pathlib import Path

base = Path.home() / "arc_strategic_control_center"
src = base / "data" / "project_structure.json"
dst = base / "data" / "progress.json"

data = json.loads(src.read_text(encoding="utf-8"))

def pct(done, total):
    return 0 if total == 0 else round((done / total) * 100)

project_out = {
    "project": data.get("project", "The Arc Strategic Control Center"),
    "chapters": []
}

total_blocks = 0
total_done = 0

for ch in data.get("chapters", []):
    chapter_blocks = 0
    chapter_done = 0
    clusters_out = []

    for cl in ch.get("clusters", []):
        blocks = cl.get("blocks", [])
        cluster_total = len(blocks)
        cluster_done = sum(1 for b in blocks if b.get("status") == "finished")
        cluster_started = sum(1 for b in blocks if b.get("status") == "started")
        cluster_planned = sum(1 for b in blocks if b.get("status") == "planned")

        chapter_blocks += cluster_total
        chapter_done += cluster_done

        clusters_out.append({
            "id": cl["id"],
            "title": cl["title"],
            "status": cl["status"],
            "total_blocks": cluster_total,
            "done_blocks": cluster_done,
            "started_blocks": cluster_started,
            "planned_blocks": cluster_planned,
            "progress_percent": pct(cluster_done, cluster_total),
            "blocks": blocks
        })

    total_blocks += chapter_blocks
    total_done += chapter_done

    project_out["chapters"].append({
        "id": ch["id"],
        "title": ch["title"],
        "status": ch["status"],
        "color": ch.get("color", "ui"),
        "total_blocks": chapter_blocks,
        "done_blocks": chapter_done,
        "progress_percent": pct(chapter_done, chapter_blocks),
        "clusters": clusters_out
    })

project_out["overall"] = {
    "total_blocks": total_blocks,
    "done_blocks": total_done,
    "progress_percent": pct(total_done, total_blocks)
}

dst.write_text(json.dumps(project_out, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Built {dst}")
