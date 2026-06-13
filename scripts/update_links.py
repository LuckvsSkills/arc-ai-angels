#!/usr/bin/env python3
"""
Update alle links in chapter HTML bestanden naar nieuwe block namen
"""

import json
import re
from pathlib import Path

BASE = Path.home() / "arc_ai_angels" / "website"

def load_progress():
    progress_file = BASE / "data" / "progress.json"
    with open(progress_file) as f:
        return json.load(f)

def get_rename_mapping(progress):
    """Maak mapping van oude link -> nieuwe link"""
    mapping = {}
    
    for chapter in progress.get("chapters", []):
        chapter_id = chapter["id"]
        
        for cluster in chapter.get("clusters", []):
            for block in cluster.get("blocks", []):
                block_id = block["id"]
                
                # Oude link formaten (b01.html, m01.html, etc.)
                match = re.match(r'([a-z])(\d+)', block_id)
                if match:
                    num = int(match.group(2))
                    old_file = f"{block_id}.html"
                    
                    # Nieuwe naam (zoals we die gemaakt hebben)
                    safe_title = re.sub(r'[^\w\s-]', '', block["title"]).replace(' ', '-').lower()[:40]
                    new_file = f"block-{num:02d}-{safe_title}.html"
                    
                    # Mapping voor links
                    old_link = f"blocks/{chapter_id}/{old_file}"
                    new_link = f"blocks/{chapter_id}/{new_file}"
                    mapping[old_link] = new_link
                    
                    # Ook zonder 'blocks/' prefix (voor verschillende link formaten)
                    mapping[f"{chapter_id}/{old_file}"] = f"{chapter_id}/{new_file}"
    
    return mapping

def update_file_links(filepath, mapping):
    """Update links in een HTML bestand"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        
        # Vervang alle oude links met nieuwe
        for old_link, new_link in mapping.items():
            content = content.replace(old_link, new_link)
        
        # Check of er wijzigingen zijn
        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
        
    except Exception as e:
        print(f"  ❌ Fout bij {filepath}: {e}")
        return False

def main():
    print("=== LINKS UPDATEN ===")
    
    progress = load_progress()
    mapping = get_rename_mapping(progress)
    
    print(f"Link mappings: {len(mapping)}")
    
    # Vind alle chapter HTML bestanden
    chapters_dir = BASE / "chapters"
    chapter_files = list(chapters_dir.glob("*.html"))
    
    print(f"\nChapter bestanden gevonden: {len(chapter_files)}")
    
    updated = 0
    for chapter_file in chapter_files:
        if update_file_links(chapter_file, mapping):
            print(f"  ✓ Updated: {chapter_file.name}")
            updated += 1
        else:
            print(f"  - Geen wijzigingen: {chapter_file.name}")
    
    # Update ook hoofd index.html
    index_file = BASE / "index.html"
    if index_file.exists():
        if update_file_links(index_file, mapping):
            print(f"  ✓ Updated: index.html")
            updated += 1
    
    print(f"\n✅ Klaar! {updated} bestanden bijgewerkt.")

if __name__ == "__main__":
    main()
