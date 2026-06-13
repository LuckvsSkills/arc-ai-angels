#!/usr/bin/env python3
"""
Fix sidebar visibility issues - voegt fallback CSS toe
"""

from pathlib import Path

BASE = Path.home() / "arc_ai_angels" / "website"

def fix_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check of er al fallback CSS is
        if 'sidebar-fallback' in content:
            print(f"  ℹ️  Al gefixt: {filepath.name}")
            return False
        
        # Voeg fallback CSS toe voor als CSS variabelen niet werken
        fallback_css = '''
<style class="sidebar-fallback">
/* Fallback als CSS variabelen niet werken */
.sidebar {
    background: #1a1a2e !important;
    color: #eef4fb !important;
}
.sidebar-header a { color: #d6b35e !important; }
.block-list a { color: #a8b7d1 !important; }
.block-list a:hover { color: #d6b35e !important; background: rgba(255,255,255,0.1) !important; }
.chapter.active { background: rgba(214, 179, 94, 0.2) !important; border-left: 3px solid #d6b35e !important; }
</style>
'''
        
        # Plaats voor de sluitende </head> tag
        if '</head>' in content:
            content = content.replace('</head>', f'{fallback_css}\n</head>')
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  ✓ Fallback CSS toegevoegd: {filepath.name}")
            return True
        return False
        
    except Exception as e:
        print(f"  ❌ Fout bij {filepath}: {e}")
        return False

def main():
    print("=== SIDEBAR VISIBILITY FIX ===")
    
    # Fix chapters
    chapters_dir = BASE / "chapters"
    fixed = 0
    for html_file in chapters_dir.glob("*.html"):
        if fix_file(html_file):
            fixed += 1
    
    print(f"\n✅ {fixed} bestanden gefixt")
    print("\nTest nu opnieuw in browser!")
    print("URL: http://172.24.162.255:8080/chapters/model_runtime.html")

if __name__ == "__main__":
    main()
