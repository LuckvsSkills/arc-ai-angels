#!/usr/bin/env python3
"""
Fix index.html - simpelere aanpak
"""

from pathlib import Path

BASE = Path.home() / "arc_ai_angels" / "website"

def fix_index():
    index_file = BASE / "index.html"
    
    with open(index_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Verwijder de topbar (zoek naar <div class="topbar"> en verwijder tot </div> met juiste nesting)
    # We doen dit door te zoeken naar het patroon en handmatig te verwijderen
    
    topbar_start = content.find('<div class="topbar">')
    if topbar_start != -1:
        # Vind het bijbehorende sluitende </div>
        # De topbar heeft structuur: <div class="topbar"><div class="wrap"><div class="topbar-inner">...</div></div></div>
        topbar_end = content.find('</div>', topbar_start)
        # We moeten 3 levels van </div> vinden
        for _ in range(2):
            topbar_end = content.find('</div>', topbar_end + 6)
        topbar_end = content.find('</div>', topbar_end + 6) + 6
        
        content = content[:topbar_start] + content[topbar_end:]
        print("✅ Topbar verwijderd")
    
    # 2. Verwijder Quick Read panel (zoek naar "Quick Read" in h3)
    quick_start = content.find('<h3>Quick Read')
    if quick_start != -1:
        # Ga terug naar begin van <div class="panel">
        panel_start = content.rfind('<div class="panel">', 0, quick_start)
        # Vind einde van dit panel
        panel_end = content.find('</div>', quick_start) + 6
        
        content = content[:panel_start] + content[panel_end:]
        print("✅ Quick Read verwijderd")
    
    # 3. Voeg theme switcher toe aan sidebar (voor de laatste </nav>)
    nav_end = content.rfind('</nav>')
    if nav_end != -1:
        theme_section = '''
    <div class="theme-section">
        <div class="theme-section-title">Appearance</div>
        <div class="theme-toggle">
            <button class="theme-btn active" onclick="setTheme('dark')" title="Dark">🌙</button>
            <button class="theme-btn" onclick="setTheme('light')" title="Light">☀️</button>
        </div>
        <div class="color-presets">
            <button class="color-btn active" onclick="setColor('obsidian_gold')" style="background:#d6b35e" title="Gold">●</button>
            <button class="color-btn" onclick="setColor('graphite_cyan')" style="background:#36c9ff" title="Cyan">●</button>
            <button class="color-btn" onclick="setColor('midnight_purple')" style="background:#9b7cff" title="Purple">●</button>
            <button class="color-btn" onclick="setColor('slate_teal')" style="background:#2fd3c5" title="Teal">●</button>
        </div>
    </div>
    
    <script>
    function setTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        localStorage.setItem('theme', theme);
        document.querySelectorAll('.theme-btn').forEach(btn => btn.classList.remove('active'));
        event.target.classList.add('active');
    }
    function setColor(preset) {
        document.documentElement.setAttribute('data-preset', preset);
        localStorage.setItem('preset', preset);
        document.querySelectorAll('.color-btn').forEach(btn => btn.classList.remove('active'));
        event.target.classList.add('active');
    }
    const savedTheme = localStorage.getItem('theme') || 'dark';
    const savedPreset = localStorage.getItem('preset') || 'obsidian_gold';
    document.documentElement.setAttribute('data-theme', savedTheme);
    document.documentElement.setAttribute('data-preset', savedPreset);
    </script>
'''
        
        content = content[:nav_end] + theme_section + content[nav_end:]
        print("✅ Theme switcher toegevoegd")
    
    # 4. Voeg theme CSS toe
    theme_css = '''
/* Theme Switcher */
.theme-section { padding:16px; border-top:1px solid rgba(255,255,255,0.06); margin-top:auto; }
.theme-section-title { font-size:11px; font-weight:600; text-transform:uppercase; letter-spacing:1px; color:#6d7f99; margin-bottom:12px; }
.theme-toggle { display:flex; gap:8px; margin-bottom:12px; }
.theme-btn { flex:1; padding:10px; border:1px solid rgba(255,255,255,0.1); border-radius:6px; background:rgba(255,255,255,0.02); color:#95a7c2; cursor:pointer; font-size:16px; transition:all 0.2s; }
.theme-btn:hover { background:rgba(255,255,255,0.06); }
.theme-btn.active { background:rgba(214,179,94,0.15); border-color:#d6b35e; color:#d6b35e; }
.color-presets { display:flex; gap:8px; }
.color-btn { width:32px; height:32px; border-radius:50%; border:2px solid transparent; cursor:pointer; font-size:10px; display:flex; align-items:center; justify-content:center; color:transparent; transition:all 0.2s; }
.color-btn:hover { transform:scale(1.1); }
.color-btn.active { border-color:#fff; box-shadow:0 0 0 2px rgba(0,0,0,0.5); color:#000; }
'''
    
    # Vind </style> in sidebar en voeg theme_css toe
    style_end = content.find('</style>', content.find('class="sidebar"'))
    if style_end != -1:
        content = content[:style_end] + theme_css + content[style_end:]
        print("✅ Theme CSS toegevoegd")
    
    # 5. Vervang eerste panel met welcome panel
    # Zoek naar hero-grid en vervang het eerste panel daarin
    hero_start = content.find('<div class="hero-grid">')
    if hero_start != -1:
        # Zoek het eerste panel in hero-grid
        first_panel_start = content.find('<div class="panel">', hero_start)
        if first_panel_start != -1:
            # Vind einde van dit panel
            panel_content_start = first_panel_start + len('<div class="panel">')
            panel_end = content.find('</div>', panel_content_start)
            
            # Maak welcome panel
            welcome = '''<div class="panel" style="background:linear-gradient(135deg,rgba(214,179,94,0.1) 0%,rgba(214,179,94,0.02) 100%);border:1px solid rgba(214,179,94,0.2);">
  <div style="display:flex;align-items:flex-start;gap:20px;">
    <div style="font-size:48px;">◈</div>
    <div>
      <h2 style="margin:0 0 12px 0;font-size:24px;color:var(--text);">Welcome to The Arc</h2>
      <p style="margin:0 0 16px 0;color:var(--muted);line-height:1.6;font-size:15px;">
        Strategic Control Center for AI Architecture, Governance & Deployment.
        Navigate through chapters using the sidebar, track progress, and access detailed block documentation.
      </p>
      <div style="display:flex;gap:12px;">
        <a href="#chapters" style="padding:10px 20px;background:var(--accent);color:#0f0f11;text-decoration:none;border-radius:8px;font-weight:600;font-size:14px;">Explore Chapters →</a>
        <a href="prompts.html" style="padding:10px 20px;background:rgba(255,255,255,0.05);color:var(--text);text-decoration:none;border-radius:8px;font-weight:500;font-size:14px;border:1px solid var(--line);">View Prompts</a>
      </div>
    </div>
  </div>
</div>'''
            
            content = content[:first_panel_start] + welcome + content[panel_end+6:]
            print("✅ Welcome panel toegevoegd")
    
    with open(index_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("\n✅ Index.html volledig aangepast!")

if __name__ == "__main__":
    fix_index()
