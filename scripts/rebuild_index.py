#!/usr/bin/env python3
"""
Bouw index.html compleet opnieuw met professionele structuur
"""

import json
from pathlib import Path

BASE = Path.home() / "arc_ai_angels" / "website"

def load_progress():
    with open(BASE / "data" / "progress.json") as f:
        return json.load(f)

def get_color_for_chapter(chapter_id):
    colors = {
        "platform_runtime": "#36c9ff",
        "security_hardening": "#3fe3b5", 
        "model_runtime": "#9b7cff",
        "agent_logic": "#ff4d6d",
        "data_memory": "#4ea8de",
        "observability": "#ff9f43",
        "control_center": "#d6b35e",
        "mission_control_ops": "#7fb8ff"
    }
    return colors.get(chapter_id, "#d6b35e")

def generate_sidebar(progress):
    """Professionele sidebar met theme dropdown"""
    
    # Genereer chapter items
    chapter_items = ""
    for chapter in progress.get("chapters", []):
        chapter_id = chapter["id"]
        chapter_title = chapter.get("title", chapter_id)
        color = get_color_for_chapter(chapter_id)
        total_blocks = chapter.get("total_blocks", 0)
        done_blocks = chapter.get("done_blocks", 0)
        
        chapter_items += f'''
        <div class="nav-item" onclick="toggleChapter(this)">
            <div class="nav-chapter-header">
                <span class="chapter-indicator" style="background:{color}"></span>
                <span class="chapter-title-text">{chapter_title}</span>
                <span class="chapter-stats">{done_blocks}/{total_blocks}</span>
                <svg class="chevron" width="12" height="12" viewBox="0 0 12 12"><path d="M3 4.5L6 7.5L9 4.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
            </div>
            <ul class="block-list collapsed">
                <li class="view-all"><a href="chapters/{chapter_id}.html" onclick="event.stopPropagation()">→ View Chapter Overview</a></li>
'''
        
        for cluster in chapter.get("clusters", []):
            for block in cluster.get("blocks", []):
                block_id = block["id"]
                block_title = block.get("title", block_id)
                import re
                match = re.match(r'([a-z])(\d+)', block_id)
                if match:
                    num = int(match.group(2))
                    safe_title = re.sub(r'[^\w\s-]', '', block_title).replace(' ', '-').lower()[:40]
                    block_file = f"block-{num:02d}-{safe_title}.html"
                    chapter_items += f'<li><a href="chapters/blocks/{chapter_id}/{block_file}" onclick="event.stopPropagation()">Block {num:02d}: {block_title}</a></li>\n'
        
        chapter_items += '''
            </ul>
        </div>
'''
    
    return f'''
<nav class="sidebar">
    <div class="sidebar-brand">
        <div class="brand-icon">◈</div>
        <div>
            <div class="brand-title">Arc Control Center</div>
            <div class="brand-subtitle">Strategic Architecture Hub</div>
        </div>
    </div>
    
    <!-- THEME SELECTOR DROPDOWN -->
    <div class="theme-selector">
        <div class="theme-label">Appearance</div>
        <select id="themeSelect" onchange="changeTheme(this.value)">
            <optgroup label="Theme">
                <option value="dark">🌙 Dark Mode</option>
                <option value="light">☀️ Light Mode</option>
            </optgroup>
            <optgroup label="Accent Color">
                <option value="obsidian_gold">Gold (Default)</option>
                <option value="graphite_cyan">Cyan</option>
                <option value="midnight_purple">Purple</option>
                <option value="slate_teal">Teal</option>
            </optgroup>
        </select>
    </div>
    
    <div class="sidebar-nav">
        <div class="nav-section">
            <div class="nav-section-title">Navigation</div>
            <a href="#home" class="nav-link active">
                <svg width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M2 6.5L8 2L14 6.5V13.5C14 13.7761 13.7761 14 13.5 14H2.5C2.22386 14 2 13.7761 2 13.5V6.5Z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/><path d="M6 14V10H10V14" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
                Dashboard
            </a>
            <a href="#roadmap" class="nav-link">
                <svg width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M2 4H14M2 8H14M2 12H10" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>
                Roadmap
            </a>
            <a href="prompts.html" class="nav-link">
                <svg width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M8 2L2 7L8 12L14 7L8 2Z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/><path d="M2 12L8 17L14 12" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" transform="translate(0, -3)"/></svg>
                Prompts
            </a>
        </div>
        
        <div class="nav-section">
            <div class="nav-section-title">Chapters</div>
            {chapter_items}
        </div>
    </div>
    
    <div class="sidebar-footer">
        <div class="progress-mini">
            <div class="progress-mini-label">Overall Progress</div>
            <div class="progress-mini-bar">
                <div class="progress-mini-fill" style="width: 54%"></div>
            </div>
            <div class="progress-mini-text">54% Complete</div>
        </div>
    </div>
</nav>

<script>
function toggleChapter(element) {{
    const blockList = element.querySelector('.block-list');
    const chevron = element.querySelector('.chevron');
    const isCollapsed = blockList.classList.contains('collapsed');
    
    document.querySelectorAll('.block-list').forEach(list => {{
        if (list !== blockList) {{
            list.classList.add('collapsed');
            list.closest('.nav-item').querySelector('.chevron').style.transform = 'rotate(0deg)';
        }}
    }});
    
    if (isCollapsed) {{
        blockList.classList.remove('collapsed');
        chevron.style.transform = 'rotate(180deg)';
    }} else {{
        blockList.classList.add('collapsed');
        chevron.style.transform = 'rotate(0deg)';
    }}
}}

function changeTheme(value) {{
    if (value === 'dark' || value === 'light') {{
        document.documentElement.setAttribute('data-theme', value);
        localStorage.setItem('theme', value);
    }} else {{
        document.documentElement.setAttribute('data-preset', value);
        localStorage.setItem('preset', value);
    }}
}}

// Load saved preferences
const savedTheme = localStorage.getItem('theme') || 'dark';
const savedPreset = localStorage.getItem('preset') || 'obsidian_gold';
document.documentElement.setAttribute('data-theme', savedTheme);
document.documentElement.setAttribute('data-preset', savedPreset);
document.getElementById('themeSelect').value = savedPreset === 'obsidian_gold' && savedTheme === 'dark' ? 'dark' : savedPreset;

document.addEventListener('DOMContentLoaded', function() {{
    const firstChapter = document.querySelector('.nav-item');
    if (firstChapter) {{
        toggleChapter(firstChapter);
    }}
}});
</script>
'''

def generate_main_content(progress):
    """Genereer main content area - JIJ MAG DIT AANPASSEN"""
    
    # Tel totalen
    total_chapters = len(progress.get("chapters", []))
    total_blocks = sum(ch.get("total_blocks", 0) for ch in progress.get("chapters", []))
    done_blocks = sum(ch.get("done_blocks", 0) for ch in progress.get("chapters", []))
    progress_pct = int((done_blocks / total_blocks * 100)) if total_blocks > 0 else 0
    
    # Chapter cards
    chapter_cards = ""
    for chapter in progress.get("chapters", []):
        chapter_id = chapter["id"]
        chapter_title = chapter.get("title", chapter_id)
        color = get_color_for_chapter(chapter_id)
        done = chapter.get("done_blocks", 0)
        total = chapter.get("total_blocks", 0)
        pct = int((done / total * 100)) if total > 0 else 0
        
        chapter_cards += f'''
<a href="chapters/{chapter_id}.html" class="chapter-card" style="--chapter-color: {color};">
  <div class="chapter-card-header">
    <span class="chapter-card-icon" style="background: {color}20; color: {color};">◈</span>
    <div class="chapter-card-meta">
      <h3>{chapter_title}</h3>
      <span class="chapter-card-status">{done}/{total} blocks</span>
    </div>
  </div>
  <div class="chapter-card-progress">
    <div class="progress-bar-bg"><div class="progress-bar-fill" style="width: {pct}%; background: {color};"></div></div>
    <span class="progress-text">{pct}%</span>
  </div>
</a>
'''
    
    return f'''
<div class="main-content">
  <!-- HERO SECTION -->
  <section class="hero">
    <div class="hero-content">
      <h1>The Arc Strategic Control Center</h1>
      <p class="hero-subtitle">Architecture, Governance & Deployment Hub for AI Systems</p>
      <div class="hero-stats">
        <div class="stat">
          <span class="stat-value">{total_chapters}</span>
          <span class="stat-label">Chapters</span>
        </div>
        <div class="stat">
          <span class="stat-value">{done_blocks}/{total_blocks}</span>
          <span class="stat-label">Blocks Complete</span>
        </div>
        <div class="stat">
          <span class="stat-value">{progress_pct}%</span>
          <span class="stat-label">Overall Progress</span>
        </div>
      </div>
    </div>
  </section>

  <!-- CHAPTERS GRID -->
  <section class="chapters-section" id="chapters">
    <div class="section-header">
      <h2>Chapters</h2>
      <p>Explore the architecture through structured chapters</p>
    </div>
    <div class="chapters-grid">
      {chapter_cards}
    </div>
  </section>

  <!-- JIJ KUNT HIER MEER SECTIES TOEVOEGEN -->
  <!-- Bijvoorbeeld: Recent Activity, Favorite Blocks, Quick Links, etc. -->
  
  <section class="info-section">
    <div class="info-card">
      <h3>🚀 Getting Started</h3>
      <p>New to The Arc? Start with the Platform & Runtime chapter to understand the foundation.</p>
      <a href="chapters/platform_runtime.html" class="btn-primary">Start Learning →</a>
    </div>
    <div class="info-card">
      <h3>📚 Documentation</h3>
      <p>Access detailed documentation for every block, including implementation guides.</p>
      <a href="#docs" class="btn-secondary">View Docs</a>
    </div>
    <div class="info-card">
      <h3>💡 Prompts</h3>
      <p>Browse the prompt library for AI-assisted development and system operations.</p>
      <a href="prompts.html" class="btn-secondary">Browse Prompts</a>
    </div>
  </section>
</div>
'''

def generate_css():
    """Complete CSS voor nieuwe layout"""
    return '''
/* ===== CSS VARIABLES ===== */
:root{
  --bg0:#0b0b0c;
  --bg1:#0f0f11;
  --panel:#161618;
  --panel2:#1c1c20;
  --card:#232329;
  --line:rgba(255,255,255,.10);
  --text:#eef4fb;
  --muted:#c3d0e3;
  --muted2:#95a7c2;
  --accent:#d6b35e;
  --accent2:#f0d18a;
  --accentGlow:rgba(240,209,138,.20);
}

[data-theme="light"]{
  --bg0:#f8fbff;
  --bg1:#f2f7fd;
  --panel:#ffffff;
  --panel2:#edf4fb;
  --card:#ffffff;
  --line:rgba(16,24,40,.10);
  --text:#132033;
  --muted:#51627b;
  --muted2:#6d7f99;
  --accentGlow:rgba(214,179,94,.10);
}

[data-preset="obsidian_gold"]{ --accent:#d6b35e; --accent2:#f0d18a; --accentGlow:rgba(240,209,138,.20); }
[data-preset="graphite_cyan"]{ --accent:#36c9ff; --accent2:#92e8ff; --accentGlow:rgba(54,201,255,.14); }
[data-preset="midnight_purple"]{ --accent:#9b7cff; --accent2:#c9b8ff; --accentGlow:rgba(155,124,255,.14); }
[data-preset="slate_teal"]{ --accent:#2fd3c5; --accent2:#93fff4; --accentGlow:rgba(47,211,197,.12); }

/* ===== BASE ===== */
*{box-sizing:border-box}
html,body{height:100%;margin:0}
body{
  margin-left: 300px;
  font-family: Inter, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif;
  color:var(--text);
  background: radial-gradient(1200px 700px at 85% -10%, var(--accentGlow), transparent 60%), linear-gradient(180deg, var(--bg0), var(--bg1));
}

/* ===== SIDEBAR ===== */
.sidebar{
  position:fixed; left:0; top:0; width:300px; height:100vh;
  background: linear-gradient(180deg, #0f0f11 0%, #161618 100%);
  border-right:1px solid rgba(255,255,255,0.08);
  display:flex; flex-direction:column; z-index:1000;
}

.sidebar-brand{padding:24px 20px 16px; border-bottom:1px solid rgba(255,255,255,0.06); display:flex; align-items:center; gap:12px;}
.brand-icon{width:40px; height:40px; background:linear-gradient(135deg, var(--accent) 0%, var(--accent2) 100%); border-radius:10px; display:flex; align-items:center; justify-content:center; font-size:20px; color:#0f0f11; font-weight:700;}
.brand-title{font-size:16px; font-weight:700; color:#eef4fb;}
.brand-subtitle{font-size:12px; color:#95a7c2; margin-top:2px;}

/* THEME SELECTOR */
.theme-selector{padding:16px 20px; border-bottom:1px solid rgba(255,255,255,0.06);}
.theme-label{font-size:11px; font-weight:600; text-transform:uppercase; letter-spacing:1px; color:#6d7f99; margin-bottom:8px;}
.theme-selector select{width:100%; padding:10px 12px; border-radius:8px; border:1px solid rgba(255,255,255,0.1); background:rgba(255,255,255,0.05); color:var(--text); font-size:13px; cursor:pointer;}
.theme-selector select:hover{border-color:rgba(255,255,255,0.2);}
.theme-selector select:focus{outline:none; border-color:var(--accent);}

.sidebar-nav{flex:1; overflow-y:auto; padding:16px 12px;}
.nav-section{margin-bottom:24px;}
.nav-section-title{font-size:11px; font-weight:600; text-transform:uppercase; letter-spacing:1px; color:#6d7f99; padding:0 8px; margin-bottom:8px;}

.nav-link{display:flex; align-items:center; gap:12px; padding:10px 12px; margin:2px 0; border-radius:8px; color:#c3d0e3; text-decoration:none; font-size:14px; font-weight:500; transition:all 0.2s;}
.nav-link:hover{background:rgba(255,255,255,0.04); color:#eef4fb;}
.nav-link.active{background:rgba(214,179,94,0.12); color:var(--accent);}

.nav-item{margin:4px 0; border-radius:8px; cursor:pointer; transition:background 0.2s;}
.nav-item:hover{background:rgba(255,255,255,0.02);}
.nav-chapter-header{display:flex; align-items:center; gap:10px; padding:12px; border-radius:8px;}
.chapter-indicator{width:4px; height:32px; border-radius:2px; flex-shrink:0;}
.chapter-title-text{flex:1; font-size:14px; font-weight:600; color:#eef4fb;}
.chapter-stats{font-size:12px; color:#6d7f99; font-weight:500;}
.chevron{color:#6d7f99; transition:transform 0.3s; flex-shrink:0;}

.block-list{list-style:none; margin:0; padding:0 12px 12px 36px; overflow:hidden; transition:all 0.3s;}
.block-list.collapsed{max-height:0; opacity:0; padding-bottom:0;}
.block-list:not(.collapsed){max-height:500px; opacity:1;}
.block-list li{margin:2px 0;}
.block-list a{display:block; padding:8px 12px; color:#95a7c2; text-decoration:none; font-size:13px; border-radius:6px; transition:all 0.2s; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;}
.block-list a:hover{background:rgba(255,255,255,0.04); color:var(--accent);}
.view-all a{color:var(--accent); font-weight:600; font-size:12px;}

.sidebar-footer{padding:16px; border-top:1px solid rgba(255,255,255,0.06); background:rgba(0,0,0,0.2);}
.progress-mini-label{font-size:11px; color:#6d7f99; text-transform:uppercase; letter-spacing:0.5px; margin-bottom:8px;}
.progress-mini-bar{height:4px; background:rgba(255,255,255,0.1); border-radius:2px; overflow:hidden; margin-bottom:6px;}
.progress-mini-fill{height:100%; background:linear-gradient(90deg, var(--accent), var(--accent2)); border-radius:2px;}
.progress-mini-text{font-size:12px; color:var(--accent); font-weight:600;}

/* ===== MAIN CONTENT ===== */
.main-content{padding:40px 48px; max-width:1400px;}

/* HERO */
.hero{margin-bottom:48px;}
.hero-content h1{font-size:42px; font-weight:800; margin:0 0 16px 0; letter-spacing:-0.5px;}
.hero-subtitle{font-size:18px; color:var(--muted); margin:0 0 32px 0; max-width:600px; line-height:1.5;}
.hero-stats{display:flex; gap:48px;}
.stat{display:flex; flex-direction:column;}
.stat-value{font-size:32px; font-weight:700; color:var(--accent);}
.stat-label{font-size:13px; color:var(--muted2); text-transform:uppercase; letter-spacing:0.5px; margin-top:4px;}

/* SECTIONS */
.section-header{margin-bottom:24px;}
.section-header h2{font-size:24px; font-weight:700; margin:0 0 8px 0;}
.section-header p{color:var(--muted); margin:0;}

/* CHAPTERS GRID */
.chapters-grid{display:grid; grid-template-columns:repeat(auto-fill, minmax(320px, 1fr)); gap:20px; margin-bottom:48px;}
.chapter-card{background:var(--panel); border:1px solid var(--line); border-radius:16px; padding:24px; text-decoration:none; transition:all 0.2s; display:block;}
.chapter-card:hover{transform:translateY(-2px); border-color:var(--chapter-color);}
.chapter-card-header{display:flex; align-items:center; gap:16px; margin-bottom:20px;}
.chapter-card-icon{width:48px; height:48px; border-radius:12px; display:flex; align-items:center; justify-content:center; font-size:24px;}
.chapter-card-meta h3{margin:0 0 4px 0; font-size:18px; color:var(--text);}
.chapter-card-meta .chapter-card-status{font-size:13px; color:var(--muted);}
.chapter-card-progress{display:flex; align-items:center; gap:12px;}
.progress-bar-bg{flex:1; height:6px; background:rgba(255,255,255,0.1); border-radius:3px; overflow:hidden;}
.progress-bar-fill{height:100%; border-radius:3px;}
.progress-text{font-size:13px; color:var(--muted); font-weight:600; min-width:40px; text-align:right;}

/* INFO SECTION */
.info-section{display:grid; grid-template-columns:repeat(auto-fit, minmax(300px, 1fr)); gap:20px;}
.info-card{background:var(--panel); border:1px solid var(--line); border-radius:16px; padding:24px;}
.info-card h3{margin:0 0 12px 0; font-size:18px;}
.info-card p{margin:0 0 20px 0; color:var(--muted); line-height:1.6; font-size:14px;}
.btn-primary, .btn-secondary{display:inline-flex; padding:10px 20px; border-radius:8px; text-decoration:none; font-weight:600; font-size:14px; transition:all 0.2s;}
.btn-primary{background:var(--accent); color:#0f0f11;}
.btn-primary:hover{background:var(--accent2);}
.btn-secondary{background:rgba(255,255,255,0.05); color:var(--text); border:1px solid var(--line);}
.btn-secondary:hover{background:rgba(255,255,255,0.1);}

/* SCROLLBAR */
.sidebar-nav::-webkit-scrollbar{width:6px;}
.sidebar-nav::-webkit-scrollbar-track{background:transparent;}
.sidebar-nav::-webkit-scrollbar-thumb{background:rgba(255,255,255,0.1); border-radius:3px;}
'''

def main():
    print("=== INDEX.HTML REBUILD ===")
    
    progress = load_progress()
    
    sidebar = generate_sidebar(progress)
    main_content = generate_main_content(progress)
    css = generate_css()
    
    # Bouw complete HTML
    html = f'''<!DOCTYPE html>
<html lang="en" data-theme="dark" data-preset="obsidian_gold">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>The Arc Strategic Control Center</title>
<style>
{css}
</style>
</head>
<body>
{sidebar}
{main_content}
</body>
</html>
'''
    
    # Schrijf naar bestand
    index_file = BASE / "index.html"
    with open(index_file, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print("✅ Nieuwe index.html gebouwd!")
    print("\nWat is er nieuw:")
    print("  • Theme selector DROPDOWN onder 'Arc Control Center'")
    print("  • Geen topbar meer")
    print("  • Geen Quick Read meer")
    print("  • Hero section met stats")
    print("  • Chapter cards met progress bars")
    print("  • Info cards sectie (jij kunt dit aanpassen!)")
    print("\nTest: http://172.24.162.255:9000/index.html")
    print("\n💡 JIJ KUNT NU AANGEVEN:")
    print("  - Wat moet er anders in de layout?")
    print("  - Welke secties wil je toevoegen/verwijderen?")
    print("  - Moeten de chapter cards anders?")

if __name__ == "__main__":
    main()
