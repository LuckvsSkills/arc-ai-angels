#!/usr/bin/env python3
"""
Hernoem blocks met echte titels uit progress.json
"""

import json
import re
from pathlib import Path

BASE = Path.home() / "arc_ai_angels" / "website"

def load_progress():
    """Laad progress.json met alle titels"""
    progress_file = BASE / "data" / "progress.json"
    with open(progress_file) as f:
        return json.load(f)

def get_block_info(progress):
    """Maak mapping van block_id -> titel per chapter"""
    blocks_map = {}
    
    for chapter in progress.get("chapters", []):
        chapter_id = chapter["id"]
        blocks_map[chapter_id] = {}
        
        for cluster in chapter.get("clusters", []):
            for block in cluster.get("blocks", []):
                block_id = block["id"]  # b01, b02, etc.
                title = block["title"]
                blocks_map[chapter_id][block_id] = title
    
    return blocks_map

def sanitize_filename(text):
    """Maak tekst veilig voor bestandsnaam"""
    # Verwijder speciale tekens, behoud letters/cijfers/spaties
    safe = re.sub(r'[^\w\s-]', '', text)
    # Vervang spaties door koppeltekens
    safe = safe.replace(' ', '-')
    # Kleine letters
    safe = safe.lower()
    # Max lengte
    return safe[:40]

def main():
    print("=== BLOCK HERNOEMING v2 ===")
    print("Laad progress.json...")
    
    progress = load_progress()
    blocks_map = get_block_info(progress)
    
    print(f"Chapters gevonden: {len(blocks_map)}")
    
    # Toon wat we gaan doen (dry run)
    for chapter_id, blocks in blocks_map.items():
        print(f"\n📁 {chapter_id}")
        
        for block_id, title in blocks.items():
            # Bepaal of het b01 of m01 formaat is
            if block_id.startswith('b'):
                num = int(block_id[1:])
                old_pattern = f"b{num:02d}.html"
            elif block_id.startswith('m'):
                num = int(block_id[1:])
                old_pattern = f"m{num:02d}.html"
            else:
                continue
            
            # Maak nieuwe naam
            safe_title = sanitize_filename(title)
            new_name = f"block-{num:02d}-{safe_title}.html"
            
            print(f"   {old_pattern} → {new_name}")
            print(f"      Titel: {title}")

if __name__ == "__main__":
    main()
