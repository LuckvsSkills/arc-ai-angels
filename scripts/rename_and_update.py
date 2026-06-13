#!/usr/bin/env python3
"""
Hernoem blocks en update alle links
"""

import json
import re
import shutil
from pathlib import Path

BASE = Path.home() / "arc_ai_angels" / "website"
BACKUP_DIR = BASE / "_rename_backup"

def load_progress():
    progress_file = BASE / "data" / "progress.json"
    with open(progress_file) as f:
        return json.load(f)

def get_all_blocks(progress):
    """Verzamel alle block info: chapter, old_file, new_name, title"""
    all_blocks = []
    
    for chapter in progress.get("chapters", []):
        chapter_id = chapter["id"]
        
        for cluster in chapter.get("clusters", []):
            for block in cluster.get("blocks", []):
                block_id = block["id"]  # b01, m01, c01, etc.
                title = block["title"]
                
                # Bepaal nummer en oud formaat
                match = re.match(r'([a-z])(\d+)', block_id)
                if match:
                    prefix = match.group(1)
                    num = int(match.group(2))
                    
                    # Oude bestandsnaam (kan b01, m01, of c01 zijn)
                    old_file = f"{block_id}.html"
                    
                    # Nieuwe naam
                    safe_title = re.sub(r'[^\w\s-]', '', title).replace(' ', '-').lower()[:40]
                    new_name = f"block-{num:02d}-{safe_title}.html"
                    
                    all_blocks.append({
                        'chapter': chapter_id,
                        'old': old_file,
                        'new': new_name,
                        'title': title,
                        'num': num
                    })
    
    return all_blocks

def main():
    print("=== BLOCK HERNOEMING & LINK UPDATE ===")
    
    # Backup maken
    BACKUP_DIR.mkdir(exist_ok=True)
    print(f"Backup in: {BACKUP_DIR}")
    
    progress = load_progress()
    blocks = get_all_blocks(progress)
    
    print(f"\nTotaal blocks: {len(blocks)}")
    print("\nOverzicht:")
    
    for b in blocks:
        print(f"  {b['chapter']}/{b['old']} → {b['new']}")
    
    # Vraag bevestiging
    print(f"\n{'='*60}")
    resp = input("Type 'JA' om door te gaan met hernoemen: ")
    
    if resp != "JA":
        print("Geannuleerd.")
        return
    
    # Hernoem bestanden
    print("\n📝 Bestanden hernoemen...")
    renamed_map = {}  # old -> new voor link updates
    
    for b in blocks:
        chapter_dir = BASE / "chapters" / "blocks" / b['chapter']
        old_path = chapter_dir / b['old']
        new_path = chapter_dir / b['new']
        
        if old_path.exists():
            # Backup
            shutil.copy2(old_path, BACKUP_DIR / f"{b['chapter']}_{b['old']}")
            # Hernoem
            shutil.move(str(old_path), str(new_path))
            print(f"  ✓ {b['chapter']}/{b['old']} → {b['new']}")
            renamed_map[f"{b['chapter']}/{b['old']}"] = f"{b['chapter']}/{b['new']}"
        else:
            print(f"  ⚠️  Niet gevonden: {b['chapter']}/{b['old']}")
    
    print(f"\n✅ Hernoeming klaar!")
    print(f"Backup staat in: {BACKUP_DIR}")
    print(f"\nVolgende stap: Links updaten in chapter HTML bestanden...")

if __name__ == "__main__":
    main()
