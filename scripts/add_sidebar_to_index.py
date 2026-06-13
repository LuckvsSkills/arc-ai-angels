#!/usr/bin/env python3
"""
Voeg sidebar toe aan index.html
"""

import json
import re
from pathlib import Path

BASE = Path.home() / "arc_ai_angels" / "website"

def load_progress():
    with open(BASE / "data" / "progress.json") as f:
        return json.load(f)

def generate_sidebar_html(progress):
    """Genereer sidebar HTML voor index"""
    html = '''
<nav class="sidebar">
    <div class="sidebar-header">
        <h2>The Arc Strategic Control Center</h2>
        <div class="logo-sub">Architecture, Governance & Deployment Hub</div>
    </div>
    <div class="sidebar-content">
'''
    
    for chapter in progress.get("chapters", []):
        chapter_id = chapter["id"]
        chapter_title = chapter.get("title", chapter_id)
        
        html += f'''
        <div class="chapter">
            <h3><a href="chapters/{chapter_id}.html">{chapter_title}</a></h3>
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
                    html += f'''
                <li><a href="chapters/blocks/{chapter_id}/{block_file}">Block {num:02d}: {block_title}</a></li>
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

def generate_sidebar_css():
    """CSS voor sidebar die samenwerkt met bestaande index CSS"""
    return '''
/* Sidebar styles */
.sidebar {
    position: fixed;
    left: 0;
    top: 0;
    width: 280px;
    height: 100vh;
    background: var(--panel, #161618);
    border-right: 1px solid var(--line, rgba(255,255,255,.10));
    overflow-y: auto;
    z-index: 100;
    padding: 20px;
    box-sizing: border-box;
}

.sidebar-header h2 {
    margin: 0 0 8px 0;
    font-size: 16px;
    color: var(--text, #eef4fb);
    line-height: 1.3;
}

.sidebar-header .logo-sub {
    font-size: 12px;
    color: var(--muted2, #95a7c2);
    margin-bottom: 24px;
    line-height: 1.4;
}

.chapter {
    margin-bottom: 20px;
    padding: 12px;
    border-radius: 8px;
    background: rgba(255,255,255,0.02);
}

.chapter h3 {
    margin: 0 0 10px 0;
    font-size: 13px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.chapter h3 a {
    color: var(--accent, #d6b35e);
    text-decoration: none;
    font-weight: 600;
}

.block-list {
    list-style: none;
    margin: 0;
    padding: 0;
}

.block-list li {
    margin: 4px 0;
    font-size: 12px;
    line-height: 1.4;
}

.block-list a {
    color: var(--muted, #c3d0e3);
    text-decoration: none;
    display: block;
    padding: 4px 8px;
    border-radius: 4px;
    transition: all 0.2s;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.block-list a:hover {
    color: var(--accent, #d6b35e);
    background: rgba(255,255,255,0.05);
}

/* Shift main content for sidebar */
body {
    margin-left: 280px !important;
}

/* Adjust topbar for sidebar */
.topbar {
    margin-left: 280px !important;
    width: calc(100% - 280px) !important;
}

/* Ensure wrap accounts for sidebar */
.wrap {
    max-width: calc(1320px - 280px) !important;
}
'''

def add_sidebar_to_index():
    """Voeg sidebar toe aan index.html"""
    index_file = BASE / "index.html"
    
    with open(index_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check of sidebar al bestaat
    if 'class="sidebar"' in content:
        print("ℹ️  Sidebar al aanwezig in index.html")
        return False
    
    progress = load_progress()
    sidebar_html = generate_sidebar_html(progress)
    sidebar_css = generate_sidebar_css()
    
    # Voeg CSS toe in head
    if '</head>' in content:
        content = content.replace('</head>', f'<style>{sidebar_css}</style>\n</head>')
    
    # Voeg sidebar toe na body tag
    if '<body>' in content:
        content = content.replace('<body>', f'<body>\n{sidebar_html}')
    
    with open(index_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Sidebar toegevoegd aan index.html")
    return True

if __name__ == "__main__":
    add_sidebar_to_index()
