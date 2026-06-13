#!/usr/bin/env python3
"""
Unify alle pagina's met index.html styling + sidebar
"""

import json
import re
from pathlib import Path

BASE = Path.home() / "arc_ai_angels" / "website"

def load_progress():
    with open(BASE / "data" / "progress.json") as f:
        return json.load(f)

def get_master_css():
    """Lees master.css"""
    with open(BASE / "assets" / "css" / "master.css", 'r') as f:
        return f.read()

def get_sidebar_css():
    """Lees sidebar.css"""
    with open(BASE / "assets" / "css" / "sidebar.css", 'r') as f:
        return f.read()

def generate_sidebar_html(progress, current_chapter=None, is_block=False):
    """Genereer sidebar HTML"""
    prefix = "../../" if is_block else "../"
    chapter_prefix = "../" if is_block else ""
    
    html = f'''
<nav class="sidebar">
    <div class="sidebar-header">
        <h2><a href="{prefix}index.html">The Arc Strategic Control Center</a></h2>
        <div class="logo-sub">Architecture, Governance & Deployment Hub</div>
    </div>
    <div class="sidebar-content">
'''
    
    for chapter in progress.get("chapters", []):
        chapter_id = chapter["id"]
        chapter_title = chapter.get("title", chapter_id)
        is_active = 'active' if chapter_id == current_chapter else ''
        
        html += f'''
        <div class="chapter {is_active}">
            <h3><a href="{chapter_prefix}{chapter_id}.html">{chapter_title}</a></h3>
            <ul class="block-list">
'''
        
        for cluster in chapter.get("clusters", []):
            for block in cluster.get("blocks", []):
                block_id = block["id"]
                block_title = block.get("title", block_id)
                match = re.match(r'([a-z])(\d+)', block_id)
                if match:
                    num = int(match.group(2))
                    safe_title = re.sub(r'[^\w\s-]', '', block_title).replace(' ', '-').lower()[:40]
                    block_file = f"block-{num:02d}-{safe_title}.html"
                    
                    if is_block:
                        # In block pagina: link naar zelfde map
                        link = block_file
                    else:
                        # In chapter pagina: link naar blocks/map
                        link = f"blocks/{chapter_id}/{block_file}"
                    
                    html += f'''
                <li><a href="{link}">Block {num:02d}: {block_title}</a></li>
'''
        
        html += '''
            </ul>
        </div>
'''
    
    html += '''
    </div>
</nav>
'''
    return html

def create_topbar():
    """Maak consistente topbar"""
    return '''
<div class="topbar">
  <div class="wrap">
    <div class="topbar-inner">
      <div>
        <div class="logo">The Arc Strategic Control Center</div>
        <div class="logo-sub">Architecture, Governance & Deployment Hub</div>
      </div>
      <div class="nav">
        <a href="../index.html">Home</a>
        <a href="#chapters">Chapters</a>
        <a href="#roadmap">Roadmap</a>
      </div>
    </div>
  </div>
</div>
'''

def update_chapter_page(filepath, progress, master_css, sidebar_css):
    """Update een chapter pagina"""
    chapter_id = filepath.stem
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Bewaar de body inhoud (wat er in staat)
    body_match = re.search(r'<body[^>]*>(.*?)</body>', content, re.DOTALL)
    if body_match:
        original_body = body_match.group(1)
        # Haal oude sidebar eruit als die er is
        original_body = re.sub(r'<nav class="sidebar">.*?</nav>', '', original_body, flags=re.DOTALL)
        # Haal oude style tags eruit
        original_body = re.sub(r'<style>.*?</style>', '', original_body, flags=re.DOTALL)
    else:
        original_body = "<h1>Error: geen body gevonden</h1>"
    
    # Bouw nieuwe pagina
    sidebar_html = generate_sidebar_html(progress, chapter_id, False)
    topbar = create_topbar()
    
    new_html = f'''<!DOCTYPE html>
<html lang="en" data-theme="dark" data-preset="obsidian_gold">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{chapter_id.replace("_", " ").title()} — The Arc Strategic Control Center</title>
<style>
{master_css}
{sidebar_css}
</style>
</head>
<body class="with-sidebar">
{sidebar_html}
{topbar}
<div class="wrap" style="padding-top: 100px;">
{original_body}
</div>
</body>
</html>
'''
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_html)
    
    return True

def update_block_page(filepath, chapter_id, progress, master_css, sidebar_css):
    """Update een block pagina"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Haal titel uit h1 of title tag
    title_match = re.search(r'<title>(.*?)</title>', content)
    if title_match:
        title = title_match.group(1).split('—')[-1].strip()
    else:
        title = filepath.stem
    
    # Haal body inhoud
    body_match = re.search(r'<body[^>]*>(.*?)</body>', content, re.DOTALL)
    if body_match:
        original_body = body_match.group(1)
        # Haal oude sidebar eruit
        original_body = re.sub(r'<nav class="sidebar">.*?</nav>', '', original_body, flags=re.DOTALL)
        # Haal oude style tags eruit
        original_body = re.sub(r'<style>.*?</style>', '', original_body, flags=re.DOTALL)
    else:
        original_body = f"<h1>{title}</h1><p>Content loading...</p>"
    
    # Bouw nieuwe pagina
    sidebar_html = generate_sidebar_html(progress, chapter_id, True)
    topbar = create_topbar()
    
    new_html = f'''<!DOCTYPE html>
<html lang="en" data-theme="dark" data-preset="obsidian_gold">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — The Arc Strategic Control Center</title>
<style>
{master_css}
{sidebar_css}
</style>
</head>
<body class="with-sidebar">
{sidebar_html}
{topbar}
<div class="wrap" style="padding-top: 100px;">
{original_body}
</div>
</body>
</html>
'''
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_html)
    
    return True

def main():
    print("=== UNIFY STYLING ===")
    
    progress = load_progress()
    master_css = get_master_css()
    sidebar_css = get_sidebar_css()
    
    # Update chapters
    chapters_dir = BASE / "chapters"
    chapter_count = 0
    for chapter_file in chapters_dir.glob("*.html"):
        if chapter_file.name == "index.html":
            continue
        if update_chapter_page(chapter_file, progress, master_css, sidebar_css):
            print(f"  ✓ Chapter: {chapter_file.name}")
            chapter_count += 1
    
    # Update blocks
    blocks_dir = BASE / "chapters" / "blocks"
    block_count = 0
    for chapter_dir in blocks_dir.iterdir():
        if not chapter_dir.is_dir():
            continue
        
        chapter_id = chapter_dir.name
        for block_file in chapter_dir.glob("block-*.html"):
            if update_block_page(block_file, chapter_id, progress, master_css, sidebar_css):
                print(f"  ✓ Block: {chapter_id}/{block_file.name}")
                block_count += 1
    
    print(f"\n✅ Klaar!")
    print(f"   {chapter_count} chapters geüpdatet")
    print(f"   {block_count} blocks geüpdatet")
    print(f"\nTest: http://172.24.162.255:9000/chapters/model_runtime.html")

if __name__ == "__main__":
    main()
