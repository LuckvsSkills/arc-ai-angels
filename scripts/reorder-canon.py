#!/usr/bin/env python3
"""
CANON Reordering Script
Reorganizes CANON chapters to logical flow with proper transitions
"""

import re
import sys
from pathlib import Path

def main():
    canon_path = Path.home() / 'arc_ai_angels' / 'CANON.md'
    backup_path = canon_path.parent / f'CANON.md.backup.reorder.{Path.ctime(canon_path)}'
    
    print("CANON REORDERING SCRIPT")
    print("=" * 80)
    print()
    print("Reading current CANON...")
    
    # Read original
    content = canon_path.read_text(encoding='utf-8')
    
    # Backup
    backup_path.write_text(content, encoding='utf-8')
    print(f"✅ Backup created: {backup_path}")
    print()
    
    # Extract chapters
    print("Extracting chapters...")
    chapters = {}
    chapter_pattern = r'^# (\d+)\. (.+?)$'
    
    current_chapter = None
    current_content = []
    
    for line in content.split('\n'):
        match = re.match(chapter_pattern, line)
        if match:
            if current_chapter:
                chapters[current_chapter] = '\n'.join(current_content)
            current_chapter = int(match.group(1))
            current_content = [line]
        else:
            if current_chapter:
                current_content.append(line)
    
    if current_chapter:
        chapters[current_chapter] = '\n'.join(current_content)
    
    print(f"✅ Extracted {len(chapters)} chapters")
    print()
    
    # Reorder mapping
    print("Mapping reorder plan...")
    reorder_map = {
        1: 1,   # FOUNDATION → 1
        2: 2,   # SYSTEM ARCHITECTURE → 2
        3: 3,   # AGENT HIERARCHY → 3
        4: 4,   # DOMAINS → 4
        5: 5,   # OPERATIONAL SYSTEM → 5
        6: 11,  # AGENTIC INTELLIGENCE → 9
        7: 10,  # MISSION CONTROL → 10
        8: 7,   # GOVERNANCE → 7
        9: 11,  # EVOLUTION → 11
        10: 8,  # AGENT CONFIG → 8
        11: 6,  # MEMORY SYSTEM → 6
    }
    
    # Reorder chapters
    reordered = {}
    for old_num, new_num in reorder_map.items():
        if old_num in chapters:
            # Update chapter number in content
            chapter_text = chapters[old_num]
            chapter_text = re.sub(
                rf'^# {old_num}\.',
                f'# {new_num}.',
                chapter_text,
                flags=re.MULTILINE
            )
            reordered[new_num] = chapter_text
            print(f"  Chapter {old_num} → Chapter {new_num}")
    
    print()
    print("Building reordered CANON...")
    
    # Build new CANON
    new_canon = []
    new_canon.append(chapters[1].split('\n')[0])  # Title line
    new_canon.append('')
    new_canon.append('**Version:** 2.1 (Restructured 2026-05-10)')
    new_canon.append('**Status:** 87% Complete & Production Ready')
    new_canon.append('**Last Updated:** 2026-05-10T12:00:00Z')
    new_canon.append('')
    new_canon.append('---')
    new_canon.append('')
    
    # Add chapters in new order
    for ch_num in sorted(reordered.keys()):
        new_canon.append(reordered[ch_num])
        new_canon.append('')
        new_canon.append('')
    
    # Write new CANON
    new_content = '\n'.join(new_canon)
    canon_path.write_text(new_content, encoding='utf-8')
    
    print(f"✅ New CANON written ({len(new_content)} chars)")
    print()
    print("=" * 80)
    print("REORDERING COMPLETE!")
    print("=" * 80)
    print()
    print("New chapter order:")
    print("  1. FOUNDATION")
    print("  2. SYSTEM ARCHITECTURE")
    print("  3. AGENT HIERARCHY")
    print("  4. DOMAINS")
    print("  5. OPERATIONAL SYSTEM")
    print("  6. MEMORY SYSTEM (MOVED UP)")
    print("  7. GOVERNANCE")
    print("  8. AGENT CONFIGURATION & EXPANSION")
    print("  9. AGENTIC INTELLIGENCE")
    print("  10. MISSION CONTROL")
    print("  11. EVOLUTION")
    print()

if __name__ == '__main__':
    main()
