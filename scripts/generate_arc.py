#!/usr/bin/env python3
import os, json

BASE_DIR = os.path.expanduser("~/arc_strategic_control_center/output")
os.makedirs(BASE_DIR, exist_ok=True)
os.makedirs(f"{BASE_DIR}/css", exist_ok=True)
os.makedirs(f"{BASE_DIR}/js", exist_ok=True)

# Data structuur
CHAPTERS = [
    {"id": "ch1", "title": "Foundation", "blocks": [
        {"id": "b01", "title": "System Architecture Overview"},
        {"id": "b02", "title": "Hardware Requirements"},
        {"id": "b03", "title": "Network Topology"},
    ]},
    {"id": "ch2", "title": "Platform & Runtime", "blocks": [
        {"id": "b08", "title": "Runtime Environment"},
        {"id": "b09", "title": "Container Orchestration"},
    ]},
]

# CSS
CSS = """* { box-sizing: border-box; margin: 0; padding: 0; }
:root { --primary: #FFD700; --bg: #0f0f1a; --bg-light: #1a1a2e; --text: #e0e0e0; --text-muted: #888; }
body { font-family: system-ui, sans-serif; background: var(--bg); color: var(--text); }
.topbar { background: var(--bg-light); padding: 1rem; display: flex; justify-content: space-between; }
.logo { color: var(--primary); font-size: 1.5rem; font-weight: bold; text-decoration: none; }
.container { display: flex; }
.sidebar { width: 300px; background: var(--bg-light); padding: 1rem; height: calc(100vh - 60px); }
.nav-chapter { margin-bottom: 1rem; }
.chapter-title { color: var(--primary); font-weight: bold; margin-bottom: 0.5rem; }
.block-link { display: block; color: var(--text-muted); text-decoration: none; padding: 0.25rem 0; font-size: 0.85rem; }
.block-link:hover { color: var(--primary); }
.block-id { color: var(--primary); font-family: monospace; margin-right: 0.5rem; }
.main { flex: 1; padding: 2rem; }
h1 { color: var(--primary); }"""

# Genereer CSS
with open(f"{BASE_DIR}/css/style.css", "w") as f:
    f.write(CSS)

# Genereer index.html
html = """<!DOCTYPE html>
<html>
<head>
    <title>ARC Strategic Control Center</title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
    <div class="topbar">
        <a href="index.html" class="logo">ARC SCC</a>
    </div>
    <div class="container">
        <div class="sidebar">"""
        
for ch in CHAPTERS:
    html += f'<div class="nav-chapter"><div class="chapter-title">{ch["title"]}</div>'
    for block in ch["blocks"]:
        html += f'<a href="block_{block["id"]}.html" class="block-link"><span class="block-id">{block["id"]}</span>{block["title"]}</a>'
    html += '</div>'

html += """</div>
        <div class="main">
            <h1>Dashboard</h1>
            <p>Welkom! Klik op een block in de sidebar.</p>
        </div>
    </div>
</body>
</html>"""

with open(f"{BASE_DIR}/index.html", "w") as f:
    f.write(html)

# Genereer block pagina's
for ch in CHAPTERS:
    for block in ch["blocks"]:
        block_html = f"""<!DOCTYPE html>
<html>
<head>
    <title>{block["title"]} - ARC SCC</title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
    <div class="topbar">
        <a href="index.html" class="logo">ARC SCC</a>
    </div>
    <div class="container">
        <div class="sidebar">"""
        
        for ch2 in CHAPTERS:
            block_html += f'<div class="nav-chapter"><div class="chapter-title">{ch2["title"]}</div>'
            for b in ch2["blocks"]:
                active = " style='color: var(--primary);'" if b["id"] == block["id"] else ""
                block_html += f'<a href="block_{b["id"]}.html" class="block-link"{active}><span class="block-id">{b["id"]}</span>{b["title"]}</a>'
            block_html += '</div>'
        
        block_html += f"""</div>
        <div class="main">
            <h1><span style="color: var(--primary); font-family: monospace;">{block["id"]}</span> {block["title"]}</h1>
            <p>Dit is de inhoud van {block["title"]}.</p>
            <p><a href="index.html" style="color: var(--primary);">← Terug naar dashboard</a></p>
        </div>
    </div>
</body>
</html>"""
        
        with open(f"{BASE_DIR}/block_{block['id']}.html", "w") as f:
            f.write(block_html)

print(f"✅ Website gegenereerd in {BASE_DIR}")
print("🚀 Start met: cd ~/arc_strategic_control_center/output && python3 -m http.server 8888")
