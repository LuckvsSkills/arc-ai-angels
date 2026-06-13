#!/usr/bin/env python3
"""
Analyseer website map structuur
"""

from pathlib import Path

WEBSITE = Path.home() / "arc_ai_angels" / "website"

def analyze():
    print("=" * 70)
    print("WEBSITE MAP ANALYSE")
    print("=" * 70)
    
    if not WEBSITE.exists():
        print("FOUT: Website map niet gevonden!")
        return
    
    all_files = list(WEBSITE.iterdir())
    
    # Categoriseer
    empty_files = [f for f in all_files if f.is_file() and f.stat().st_size == 0]
    backup_files = [f for f in all_files if f.is_file() and ('.bak.' in f.name or '.rollback.' in f.name or '_old' in f.name)]
    build_scripts = [f for f in all_files if f.is_file() and f.name.startswith(('build_', 'rebuild_', 'upgrade_'))]
    html_files = [f for f in all_files if f.is_file() and f.suffix == '.html']
    py_scripts = [f for f in all_files if f.is_file() and f.suffix == '.py' and f not in build_scripts]
    dirs = [f for f in all_files if f.is_dir()]
    
    print(f"\n📊 STATISTIEKEN:")
    print(f"   Totaal items: {len(all_files)}")
    print(f"   Lege bestanden (0 bytes): {len(empty_files)}")
    print(f"   Backup/oude versies: {len(backup_files)}")
    print(f"   Bouwscripts: {len(build_scripts)}")
    print(f"   HTML bestanden: {len(html_files)}")
    print(f"   Overige Python scripts: {len(py_scripts)}")
    print(f"   Mappen: {len(dirs)}")
    
    if empty_files:
        print(f"\n🗑️  LEGE BESTANDEN (veilig te verwijderen):")
        for f in empty_files[:10]:
            print(f"   • {f.name}")
        if len(empty_files) > 10:
            print(f"   ... en {len(empty_files)-10} meer")
    
    if backup_files:
        print(f"\n📦 BACKUP/OUDE VERSIES:")
        for f in backup_files:
            size = f.stat().st_size
            print(f"   • {f.name} ({size/1024:.1f} KB)")
    
    if build_scripts:
        print(f"\n🔨 BOUWSCRIPTS:")
        for f in build_scripts:
            print(f"   • {f.name}")
    
    if html_files:
        print(f"\n🌐 HTML BESTANDEN (output):")
        for f in html_files:
            print(f"   • {f.name}")

if __name__ == "__main__":
    analyze()
