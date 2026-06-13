#!/usr/bin/env python3
"""
Haal CSS uit index.html en maak master stylesheet
"""

from pathlib import Path
import re

BASE = Path.home() / "arc_ai_angels" / "website"

def extract_css_from_index():
    """Haal inline CSS uit index.html"""
    index_file = BASE / "index.html"
    
    with open(index_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Zoek style tag inhoud
    match = re.search(r'<style[^>]*>(.*?)</style>', content, re.DOTALL)
    if match:
        css = match.group(1)
        
        # Sla op als extern CSS bestand
        css_file = BASE / "assets" / "css" / "master.css"
        css_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(css_file, 'w', encoding='utf-8') as f:
            f.write(css)
        
        print(f"✅ CSS geëxtraheerd naar: {css_file}")
        print(f"   Grootte: {len(css)} karakters")
        return True
    
    print("❌ Geen inline CSS gevonden in index.html")
    return False

def create_sidebar_css_addon():
    """Maak extra CSS voor sidebar die samenwerkt met master CSS"""
    sidebar_css = '''
/* Sidebar addon voor master.css */
.sidebar {
    position: fixed;
    left: 0;
    top: 0;
    width: 280px;
    height: 100vh;
    background: var(--panel, #1a1a2e);
    border-right: 1px solid var(--line, rgba(255,255,255,.1));
    overflow-y: auto;
    z-index: 1000;
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

/* Body shift voor sidebar */
body.with-sidebar {
    margin-left: 280px !important;
}

/* Topbar fix voor sidebar */
.topbar {
    margin-left: 280px !important;
    width: calc(100% - 280px) !important;
}
'''
    
    css_file = BASE / "assets" / "css" / "sidebar.css"
    with open(css_file, 'w', encoding='utf-8') as f:
        f.write(sidebar_css)
    
    print(f"✅ Sidebar CSS gemaakt: {css_file}")
    return True

def main():
    print("=== MASTER CSS EXTRAHEREN ===")
    extract_css_from_index()
    create_sidebar_css_addon()
    print("\nKlaar! Nu kunnen we alle pagina's updaten om deze CSS te gebruiken.")

if __name__ == "__main__":
    main()
