#!/usr/bin/env python3
import sys
print("START DEBUG", file=sys.stderr)

try:
    import json
    import re
    from pathlib import Path
    print("✓ Imports OK", file=sys.stderr)
    
    BASE = Path.home() / "arc_ai_angels" / "website"
    print(f"✓ BASE path: {BASE}", file=sys.stderr)
    
    progress_file = BASE / "data" / "progress.json"
    print(f"✓ Progress file: {progress_file}", file=sys.stderr)
    print(f"✓ Exists: {progress_file.exists()}", file=sys.stderr)
    
    with open(progress_file) as f:
        progress = json.load(f)
    print(f"✓ JSON loaded, chapters: {len(progress.get('chapters', []))}", file=sys.stderr)
    
    # Maak simpele HTML
    html = f"""<!DOCTYPE html>
<html>
<head><title>TEST</title></head>
<body>
<h1>WORKS!</h1>
<p>Chapters: {len(progress.get('chapters', []))}</p>
<p>Overall: {progress.get('overall', {}).get('progress_percent', 0)}%</p>
</body>
</html>"""
    
    index_file = BASE / "index.html"
    with open(index_file, 'w') as f:
        f.write(html)
    
    print(f"✓ File written: {index_file}", file=sys.stderr)
    print("SUCCESS!")
    
except Exception as e:
    print(f"✗ ERROR: {e}", file=sys.stderr)
    import traceback
    traceback.print_exc(file=sys.stderr)
    print(f"FAILED: {e}")
