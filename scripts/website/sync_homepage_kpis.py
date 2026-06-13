import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PROGRESS = ROOT / "data" / "progress.json"
INDEX = ROOT / "index.html"

if not PROGRESS.exists() or not INDEX.exists():
    raise SystemExit("progress.json of index.html ontbreekt")

progress = json.loads(PROGRESS.read_text())
chapters = progress.get("chapters", progress if isinstance(progress, list) else [])
if not isinstance(chapters, list):
    chapters = []

total_blocks = 0
done_blocks = 0

for ch in chapters:
    if isinstance(ch, dict):
        total_blocks += int(ch.get("total_blocks", 0))
        done_blocks += int(ch.get("done_blocks", 0))

overall = round((done_blocks / total_blocks) * 100) if total_blocks else 0

current_focus = None
for ch in chapters:
    if isinstance(ch, dict) and ch.get("status") == "started":
        current_focus = ch
        break
if current_focus is None:
    for ch in chapters:
        if isinstance(ch, dict) and ch.get("status") == "planned":
            current_focus = ch
            break
if current_focus is None and chapters:
    current_focus = chapters[0]

current_focus_title = current_focus.get("title", "-") if isinstance(current_focus, dict) else "-"

active_block = "-"
if isinstance(current_focus, dict):
    for cluster in current_focus.get("clusters", []):
        if not isinstance(cluster, dict):
            continue
        for block in cluster.get("blocks", []):
            if isinstance(block, dict) and block.get("status") == "started":
                active_block = block.get("title", "-")
                break
        if active_block != "-":
            break

    if active_block == "-":
        for cluster in current_focus.get("clusters", []):
            if not isinstance(cluster, dict):
                continue
            for block in cluster.get("blocks", []):
                if isinstance(block, dict) and block.get("status") == "planned":
                    active_block = block.get("title", "-")
                    break
            if active_block != "-":
                break

html = INDEX.read_text()

patterns = [
    (
        r'(<div class="kpi-label">Overall Progress</div>\s*<div class="kpi-value">)(.*?)(</div>)',
        f'\\g<1>{overall}%\\g<3>'
    ),
    (
        r'(<div class="kpi-label">Current Focus</div>\s*<div class="kpi-value">)(.*?)(</div>)',
        f'\\g<1>{current_focus_title}\\g<3>'
    ),
    (
        r'(<div class="kpi-label">Active Block</div>\s*<div class="kpi-value">)(.*?)(</div>)',
        f'\\g<1>{active_block}\\g<3>'
    ),
    (
        r'(<div class="kpi-label">Active Cluster</div>\s*<div class="kpi-value">)(.*?)(</div>)',
        f'\\g<1>{active_block}\\g<3>'
    ),
]

for pattern, repl in patterns:
    html = re.sub(pattern, repl, html, count=1, flags=re.S)

INDEX.write_text(html)
print(f"Homepage KPI sync klaar: overall={overall}%, focus={current_focus_title}, active_block={active_block}")
