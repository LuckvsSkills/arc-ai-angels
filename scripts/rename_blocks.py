#!/usr/bin/env python3
"""
Hernoem blocks van b01, b02 → Block 01 - Titel
"""

import json
import re
from pathlib import Path

BASE = Path.home() / "arc_ai_angels" / "website"

def get_block_title(md_file):
    """Lees titel uit markdown bestand (eerste # heading)"""
    try:
        with open(md_file, 'r') as f:
            for line in f:
                if line.startswith('# '):
                    return line[2:].strip()
    except:
        pass
    return None

def main():
    print("=== BLOCK HERNOEMING ===")
    
    # Laad chapter meta
    meta_file = BASE / "data" / "chapter_meta.json"
    if meta_file.exists():
        with open(meta_file) as f:
            meta = json.load(f)
            print(f"Chapters gevonden: {len(meta.get('chapters', []))}")
    
    # Vind alle block mappen
    blocks_dir = BASE / "chapters" / "blocks"
    if not blocks_dir.exists():
        print("Geen blocks map gevonden!")
        return
    
    for chapter_dir in blocks_dir.iterdir():
        if not chapter_dir.is_dir():
            continue
            
        print(f"\n📁 {chapter_dir.name}")
        
        # Vind alle block bestanden
        for block_file in sorted(chapter_dir.glob("b*.html")):
            # Parse nummer uit bestandsnaam
            match = re.match(r'b(\d+)\.html', block_file.name)
            if match:
                num = int(match.group(1))
                
                # Zoek bijbehorende markdown voor titel
                md_file = BASE / "data" / "block_content" / chapter_dir.name / f"b{num:02d}.md"
                title = get_block_title(md_file) or f"Block {num:02d}"
                
                # Maak nieuwe naam
                safe_title = re.sub(r'[^\w\s-]', '', title).replace(' ', '-').lower()[:30]
                new_name = f"block-{num:02d}-{safe_title}.html"
                
                print(f"   {block_file.name} → {new_name}")
                # Hier later daadwerkelijk hernoemen

if __name__ == "__main__":
    main()
