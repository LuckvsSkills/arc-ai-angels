#!/usr/bin/env python3
"""
Voeg sidebar toe aan alle BLOCK HTML bestanden (niet alleen chapters)
"""

import json
import re
from pathlib import Path

BASE = Path.home() / "arc_ai_angels" / "website"

def load_progress():
    progress_file = BASE / "data" / "progress.json"
    with open(progress_file) as f:
        return json.load(f)

def get_block_chapter_mapping(progress):
    """Maak mapping van block filename -> chapter_id"""
    mapping = {}
    for chapter in progress.get("chapters", []):
        chapter_id = chapter["id"]
        for cluster in chapter.get("clusters", []):
            for block in cluster.get("blocks", []):
                block_id = block["id"]
                match = re.match(r'([a-z])(\d+)', block_id)
                if match:
                    num = int(match.group(2))
                    safe_title = re.sub(r'[^\w\s-]', '', block["title"]).replace(' ', '-').lower()[:40]
                    block_file = f"block-{num:02d}-{safe_title}.html"
                    mapping[block_file] = chapter_id
    return mapping

def generate_sidebar(progress, current_chapter=None):
    """Genereer HTML sidebar met alle chapters en blocks"""
    sidebar_html = '''
    <nav class="sidebar">
        <div class="sidebar-header">
            <h2><a href="../../index.html">Arc AI Angels</a></h2>
        </div>
        <div class="sidebar-content">
'''
    
    for chapter in progress.get("chapters", []):
        chapter_id = chapter["id"]
        chapter_title = chapter.get("title", chapter_id)
        is_active = 'active' if chapter_id == current_chapter else ''
        
        sidebar_html += f'''
            <div class="chapter {is_active}">
                <h3><a href="../{chapter_id}.html">{chapter_title}</a></h3>
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
                    sidebar_html += f'''
                    <li><a href="{block_file}">Block {num:02d}: {block_title}</a></li>
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
.sidebar-header h2 { margin: 0 0 20px 0; font-size: 18px; }
.sidebar-header a { color: var(--accent, #d6b35e); text-decoration: none; }
.chapter { margin-bottom: 20px; padding: 10px; border-radius: 8px; }
.chapter.active { background: rgba(214, 179, 94, 0.1); border-left: 3px solid var(--accent, #d6b35e); }
.chapter h3 { margin: 0 0 10px 0; font-size: 14px; text-transform: uppercase; letter-spacing: 1px; }
.chapter h3 a { color: var(--text, #eef4fb); text-decoration: none; }
.block-list { list-style: none; margin: 0; padding: 0; }
.block-list li { margin: 5px 0; font-size: 13px; }
.block-list a { color: var(--muted, #a8b7d1); text-decoration: none; display: block; padding: 5px 10px; border-radius: 4px; transition: all 0.2s; }
.block-list a:hover { color: var(--accent, #d6b35e); background: rgba(255,255,255,0.05); }
body { margin-left: 280px !important; }
</style>
'''

def add_sidebar_to_block(filepath, chapter_id, sidebar_html, css):
    """Voeg sidebar toe aan een block HTML bestand"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if 'class="sidebar"' in content:
            return False
        
        if '</head>' in content:
            content = content.replace('</head>', f'{css}\n</head>')
        
        if '<body>' in content:
            content = content.replace('<body>', f'<body>\n{sidebar_html}')
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True
    except Exception as e:
        print(f"  ❌ Fout bij {filepath}: {e}")
        return False

def main():
    print("=== SIDEBAR TOEVOEGEN AAN BLOCKS ===")
    
    progress = load_progress()
    block_mapping = get_block_chapter_mapping(progress)
    sidebar_css = generate_sidebar_css()
    
    blocks_dir = BASE / "chapters" / "blocks"
    added = 0
    
    for chapter_dir in blocks_dir.iterdir():
        if not chapter_dir.is_dir():
            continue
        
        chapter_id = chapter_dir.name
        
        for block_file in chapter_dir.glob("block-*.html"):
            block_name = block_file.name
            
            # Genereer sidebar voor dit specifieke block
            sidebar_html = generate_sidebar(progress, chapter_id)
            
            if add_sidebar_to_block(block_file, chapter_id, sidebar_html, sidebar_css):
                print(f"  ✓ Sidebar toegevoegd: {chapter_id}/{block_name}")
                added += 1
    
    print(f"\n✅ Klaar! {added} block bestanden met sidebar.")

if __name__ == "__main__":
    main()
