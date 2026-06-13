#!/usr/bin/env python3
"""
Voeg sidebar toe aan alle chapter HTML bestanden
"""

import json
import re
from pathlib import Path

BASE = Path.home() / "arc_ai_angels" / "website"

def load_progress():
    progress_file = BASE / "data" / "progress.json"
    with open(progress_file) as f:
        return json.load(f)

def generate_sidebar(progress, current_chapter=None):
    """Genereer HTML sidebar met alle chapters en blocks"""
    
    sidebar_html = '''
    <nav class="sidebar">
        <div class="sidebar-header">
            <h2><a href="../index.html">Arc AI Angels</a></h2>
        </div>
        <div class="sidebar-content">
'''
    
    for chapter in progress.get("chapters", []):
        chapter_id = chapter["id"]
        chapter_title = chapter.get("title", chapter_id)
        
        # Active chapter?
        is_active = 'active' if chapter_id == current_chapter else ''
        
        sidebar_html += f'''
            <div class="chapter {is_active}">
                <h3><a href="{chapter_id}.html">{chapter_title}</a></h3>
                <ul class="block-list">
'''
        
        for cluster in chapter.get("clusters", []):
            for block in cluster.get("blocks", []):
                block_id = block["id"]
                block_title = block.get("title", block_id)
                
                # Bepaal nieuwe bestandsnaam
                match = re.match(r'([a-z])(\d+)', block_id)
                if match:
                    num = int(match.group(2))
                    safe_title = re.sub(r'[^\w\s-]', '', block_title).replace(' ', '-').lower()[:40]
                    block_file = f"block-{num:02d}-{safe_title}.html"
                    
                    sidebar_html += f'''
                    <li><a href="blocks/{chapter_id}/{block_file}">Block {num:02d}: {block_title}</a></li>
'''
        
        sidebar_html += '''
                </ul>
            </div>
'''
    
    sidebar_html += '''
        </div>
    </nav>
'''
    return sidebar_html

def generate_sidebar_css():
    """CSS voor de sidebar"""
    return '''
<style>
.sidebar {
    position: fixed;
    left: 0;
    top: 0;
    width: 280px;
    height: 100vh;
    background: var(--panel, #1a1a2e);
    border-right: 1px solid var(--line, rgba(255,255,255,.1));
    overflow-y: auto;
    z-index: 100;
    padding: 20px;
    box-sizing: border-box;
}

.sidebar-header h2 {
    margin: 0 0 20px 0;
    font-size: 18px;
}

.sidebar-header a {
    color: var(--accent, #d6b35e);
    text-decoration: none;
}

.chapter {
    margin-bottom: 20px;
    padding: 10px;
    border-radius: 8px;
}

.chapter.active {
    background: rgba(214, 179, 94, 0.1);
    border-left: 3px solid var(--accent, #d6b35e);
}

.chapter h3 {
    margin: 0 0 10px 0;
    font-size: 14px;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.chapter h3 a {
    color: var(--text, #eef4fb);
    text-decoration: none;
}

.block-list {
    list-style: none;
    margin: 0;
    padding: 0;
}

.block-list li {
    margin: 5px 0;
    font-size: 13px;
}

.block-list a {
    color: var(--muted, #a8b7d1);
    text-decoration: none;
    display: block;
    padding: 5px 10px;
    border-radius: 4px;
    transition: all 0.2s;
}

.block-list a:hover {
    color: var(--accent, #d6b35e);
    background: rgba(255,255,255,0.05);
}

/* Main content moet naar rechts schuiven */
body {
    margin-left: 280px !important;
}
</style>
'''

def add_sidebar_to_file(filepath, sidebar_html, css):
    """Voeg sidebar toe aan een HTML bestand"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check of sidebar al bestaat
        if 'class="sidebar"' in content:
            print(f"  ℹ️  Sidebar al aanwezig in {filepath.name}")
            return False
        
        # Voeg CSS toe in <head>
        if '</head>' in content:
            content = content.replace('</head>', f'{css}\n</head>')
        
        # Voeg sidebar toe na <body>
        if '<body>' in content:
            content = content.replace('<body>', f'<body>\n{sidebar_html}')
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True
        
    except Exception as e:
        print(f"  ❌ Fout bij {filepath}: {e}")
        return False

def main():
    print("=== SIDEBAR TOEVOEGEN ===")
    
    progress = load_progress()
    sidebar_css = generate_sidebar_css()
    
    chapters_dir = BASE / "chapters"
    chapter_files = list(chapters_dir.glob("*.html"))
    
    added = 0
    for chapter_file in chapter_files:
        chapter_id = chapter_file.stem  # filename zonder .html
        
        sidebar_html = generate_sidebar(progress, chapter_id)
        
        if add_sidebar_to_file(chapter_file, sidebar_html, sidebar_css):
            print(f"  ✓ Sidebar toegevoegd: {chapter_file.name}")
            added += 1
        else:
            print(f"  - {chapter_file.name}")
    
    print(f"\n✅ Klaar! {added} bestanden met sidebar.")

if __name__ == "__main__":
    main()
