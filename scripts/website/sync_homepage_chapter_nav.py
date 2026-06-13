#!/usr/bin/env python3
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
INDEX = ROOT / "index.html"
PROGRESS = ROOT / "data" / "progress.json"
TIME = ROOT / "data" / "time_tracking.json"

progress = json.loads(PROGRESS.read_text())
time_data = json.loads(TIME.read_text()) if TIME.exists() else {}

chapters = {c["id"]: c for c in progress.get("chapters", [])}

file_to_id = {
    "platform_runtime": "platform_runtime",
    "security_hardening": "security_hardening",
    "model_runtime": "model_runtime",
    "data_memory": "data_memory",
    "agent_logic": "agent_logic",
    "observability": "observability",
    "control_center": "control_center",
}

html = INDEX.read_text()

card_re = re.compile(
    r'(<a class="chapter-card" href="\./chapters/(?P<file>[^"]+)\.html"[^>]*>\s*)'
    r'(?P<body>.*?)'
    r'(\s*</a>)',
    re.DOTALL
)

meta_re = re.compile(
    r'<div class="meta"><span>\d+h</span><span>\d+%</span></div>\s*'
    r'<div class="pbar"><div style="width:\d+%"></div></div>',
    re.DOTALL
)

def patch_card(match):
    file_stem = match.group("file")
    chapter_id = file_to_id.get(file_stem)
    if not chapter_id:
        return match.group(0)

    chapter = chapters.get(chapter_id)
    if not chapter:
        return match.group(0)

    pct = int(chapter.get("progress_percent", 0))
    hours = int(time_data.get(chapter_id, {}).get("actual_hours", 0))

    new_meta = (
        f'<div class="meta"><span>{hours}h</span><span>{pct}%</span></div>\n'
        f'        <div class="pbar"><div style="width:{pct}%"></div></div>'
    )

    body = match.group("body")
    if not meta_re.search(body):
        return match.group(0)

    body = meta_re.sub(new_meta, body, count=1)
    return match.group(1) + body + match.group(4)

new_html = card_re.sub(patch_card, html)
INDEX.write_text(new_html)
print("Updated homepage chapter navigation from progress.json + time_tracking.json")

import subprocess
subprocess.run(["python3", "sync_homepage_kpis.py"], check=False)
