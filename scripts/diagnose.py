#!/usr/bin/env python3
import os
import json

print("=== DIAGNOSE ARC AI ANGELS ===\n")

# Check directories
website_dir = os.path.expanduser('~/arc_ai_angels/website')
data_dir = os.path.expanduser('~/arc_ai_angels/website/data')
chapters_dir = os.path.expanduser('~/arc_ai_angels/website/chapters')

print("1. DIRECTORY STRUCTUUR:")
print(f"   Website dir bestaat: {os.path.exists(website_dir)}")
print(f"   Data dir bestaat: {os.path.exists(data_dir)}")
print(f"   Chapters dir bestaat: {os.path.exists(chapters_dir)}")

# Check files
index_path = os.path.join(website_dir, 'index.html')
progress_path = os.path.join(data_dir, 'progress.json')

print(f"\n2. BESTANDEN:")
print(f"   index.html bestaat: {os.path.exists(index_path)}")
if os.path.exists(index_path):
    size = os.path.getsize(index_path)
    print(f"   index.html grootte: {size} bytes")
    
    # Read first 500 chars to see what version
    with open(index_path, 'r') as f:
        content = f.read(500)
        if 'Arc AI Angels' in content and 'chapter-header' in content:
            print("   → LIJKT de nieuwe layout te zijn")
        elif 'Arc AI Angels' in content:
            print("   → Bevat Arc AI Angels titel")
        else:
            print("   → Onbekende inhoud")

print(f"\n   progress.json bestaat: {os.path.exists(progress_path)}")

# Check permissions
print(f"\n3. PERMISSIES:")
print(f"   Website dir writable: {os.access(website_dir, os.W_OK)}")
print(f"   index.html writable: {os.access(index_path, os.W_OK) if os.path.exists(index_path) else 'N/A'}")

# Try to write a test file
print(f"\n4. SCHRIJF TEST:")
test_file = os.path.join(website_dir, 'test_write.txt')
try:
    with open(test_file, 'w') as f:
        f.write("TEST")
    print(f"   ✓ Kan schrijven naar website dir")
    os.remove(test_file)
    print(f"   ✓ Test bestand verwijderd")
except Exception as e:
    print(f"   ✗ FOUT bij schrijven: {e}")

# Check current working directory
print(f"\n5. HUIDIGE WORKING DIRECTORY:")
print(f"   {os.getcwd()}")

print(f"\n6. PROBEER INDEX.HTML TE SCHRIJVEN...")
simple_html = '''<!DOCTYPE html>
<html>
<head><title>TEST - Arc AI Angels</title></head>
<body>
<h1>DEZE TEKST MOET ZICHTBAAR WORDEN</h1>
<p>Als je dit ziet, werkt het schrijven van bestanden!</p>
<p>Tijd: ''' + str(__import__('datetime').datetime.now()) + '''</p>
</body>
</html>'''

try:
    with open(index_path, 'w') as f:
        f.write(simple_html)
    print("   ✓ index.html succesvol geschreven!")
    print("   → Refresh nu je browser, je zou 'DEZE TEKST MOET ZICHTBAAR WORDEN' moeten zien")
except Exception as e:
    print(f"   ✗ FOUT: {e}")

print("\n=== EINDE DIAGNOSE ===")
