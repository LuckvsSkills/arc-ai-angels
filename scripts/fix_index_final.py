#!/usr/bin/env python3
"""
Final index.html fixes: theme switcher, remove topbar/quickread, add better content
"""

import re
from pathlib import Path

BASE = Path.home() / "arc_ai_angels" / "website"

def fix_index():
    index_file = BASE / "index.html"
    
    with open(index_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. VERWIJDER TOPBAR
    content = re.sub(
        r'<div class="topbar">.*?</div>\s*</div>\s*</div>\s*</div>',
        '',
        content,
        flags=re.DOTALL
    )
    
    # 2. VERWIJDER QUICK READ SECTIE
    # Zoek de quick read sectie (meestal heeft het class="panel" met quick read erin)
    content = re.sub(
        r'<div class="panel">\s*<h3[^>]*>Quick Read.*?</div>\s*</div>',
        '',
        content,
        flags=re.DOTALL
    )
    
    # 3. VOEG THEME SWITCHER TOE AAN SIDEBAR (voor de </nav> tag)
    theme_switcher = '''
    <div class="theme-section">
        <div class="theme-section-title">Appearance</div>
        <div class="theme-toggle">
            <button class="theme-btn active" onclick="setTheme('dark')" title="Dark">
                <svg width="14" height="14" viewBox="0 0 16 16" fill="none"><path d="M8 1V2M8 14V15M15 8H14M2 8H1M12.5 3.5L11.8 4.2M4.2 11.8L3.5 12.5M12.5 12.5L11.8 11.8M4.2 4.2L3.5 3.5M8 12C5.23858 12 3 9.76142 3 7C3 5.4193 3.7544 4.01418 4.9716 3.11591C5.29173 2.88327 5.7106 3.13133 5.67624 3.51382C5.58315 4.56226 5.97715 5.65966 6.78985 6.47235C7.60254 7.28505 8.69994 7.67905 9.74838 7.58596C10.1309 7.5516 10.3789 7.97047 10.1463 8.2906C9.24799 9.5078 7.84287 10.2622 6.26217 10.2622C6.1758 10.2622 6.09007 10.2591 6.005 10.253C6.27687 11.3716 7.0559 12.2939 8.11767 12.7293C8.45367 12.8661 8.47303 13.3336 8.15003 13.4969C8.10228 13.5204 8.05228 13.5406 8.00028 13.5574C8.00019 13.5574 8.00009 13.5574 8 13.5574C9.65685 13.5574 11.1571 12.8489 12.1966 11.7322C11.6358 11.9061 11.0318 12 10.404 12C7.08934 12 4.2985 9.53284 3.95623 6.31783C3.9173 5.94203 4.34008 5.68764 4.67114 5.883C5.21268 6.20795 5.83537 6.39286 6.50566 6.39286C8.98646 6.39286 11 8.4064 11 10.8872C11 11.0941 10.9916 11.2987 10.9752 11.5007C11.6318 10.7786 12 9.87918 12 8.90909C12 6.30828 9.89177 4.2 7.29095 4.2C6.57207 4.2 5.89304 4.37032 5.28757 4.67432C5.65203 2.71297 7.37976 1.2 9.45455 1.2C9.8287 1.2 10.1928 1.24912 10.5406 1.34195C10.0686 1.11745 9.54792 1 9 1C5.68629 1 3 3.68629 3 7C3 10.3137 5.68629 13 9 13C9.54792 13 10.0686 12.8826 10.5406 12.6581C10.1928 12.7509 9.8287 12.8 9.45455 12.8C8.30545 12.8 7.22727 12.4636 6.31783 11.8768C7.08934 12.6252 8.12358 13.0769 9.26364 13.0769C11.9706 13.0769 14.1636 10.8839 14.1636 8.17692C14.1636 7.39545 13.975 6.65682 13.6364 6.00001L13.6364 6" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
            </button>
            <button class="theme-btn" onclick="setTheme('light')" title="Light">
                <svg width="14" height="14" viewBox="0 0 16 16" fill="none"><circle cx="8" cy="8" r="3.5" stroke="currentColor" stroke-width="1.5"/><path d="M8 1.5V2.5M8 13.5V14.5M14.5 8H13.5M2.5 8H1.5M12.5 3.5L11.8 4.2M4.2 11.8L3.5 12.5M12.5 12.5L11.8 11.8M4.2 4.2L3.5 3.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>
            </button>
        </div>
        <div class="color-presets">
            <button class="color-btn active" onclick="setColor('obsidian_gold')" style="background: #d6b35e;" title="Gold"></button>
            <button class="color-btn" onclick="setColor('graphite_cyan')" style="background: #36c9ff;" title="Cyan"></button>
            <button class="color-btn" onclick="setColor('midnight_purple')" style="background: #9b7cff;" title="Purple"></button>
            <button class="color-btn" onclick="setColor('slate_teal')" style="background: #2fd3c5;" title="Teal"></button>
        </div>
    </div>
    
    <script>
    function setTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        localStorage.setItem('theme', theme);
        document.querySelectorAll('.theme-btn').forEach(btn => btn.classList.remove('active'));
        event.target.closest('.theme-btn').classList.add('active');
    }
    
    function setColor(preset) {
        document.documentElement.setAttribute('data-preset', preset);
        localStorage.setItem('preset', preset);
        document.querySelectorAll('.color-btn').forEach(btn => btn.classList.remove('active'));
        event.target.classList.add('active');
    }
    
    // Load saved preferences
    const savedTheme = localStorage.getItem('theme') || 'dark';
    const savedPreset = localStorage.getItem('preset') || 'obsidian_gold';
    document.documentElement.setAttribute('data-theme', savedTheme);
    document.documentElement.setAttribute('data-preset', savedPreset);
    </script>
</nav>
'''
    
    # Vervang </nav> met theme switcher + </nav>
    content = content.replace('</nav>', theme_switcher, 1)
    
    # 4. VOEG THEME CSS TOE
    theme_css = '''
/* Theme Section in Sidebar */
.theme-section {
    padding: 16px;
    border-top: 1px solid rgba(255,255,255,0.06);
    margin-top: auto;
}

.theme-section-title {
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: #6d7f99;
    margin-bottom: 12px;
}

.theme-toggle {
    display: flex;
    gap: 8px;
    margin-bottom: 12px;
}

.theme-btn {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
    padding: 8px;
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 6px;
    background: rgba(255,255,255,0.02);
    color: #95a7c2;
    cursor: pointer;
    transition: all 0.2s;
    font-size: 12px;
}

.theme-btn:hover {
    background: rgba(255,255,255,0.06);
    border-color: rgba(255,255,255,0.2);
}

.theme-btn.active {
    background: rgba(214, 179, 94, 0.15);
    border-color: #d6b35e;
    color: #d6b35e;
}

.color-presets {
    display: flex;
    gap: 8px;
}

.color-btn {
    width: 28px;
    height: 28px;
    border-radius: 50%;
    border: 2px solid transparent;
    cursor: pointer;
    transition: all 0.2s;
    position: relative;
}

.color-btn:hover {
    transform: scale(1.1);
}

.color-btn.active {
    border-color: #fff;
    box-shadow: 0 0 0 2px rgba(0,0,0,0.5);
}

.color-btn.active::after {
    content: "✓";
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    color: #000;
    font-size: 12px;
    font-weight: bold;
    text-shadow: 0 0 2px rgba(255,255,255,0.5);
}
'''
    
    # Voeg theme CSS toe aan bestaande sidebar CSS
    content = content.replace('</style>', f'{theme_css}</style>', 1)
    
    # 5. VERVANG QUICK READ MET WELKOMST PANEL
    welcome_panel = '''
<div class="panel welcome-panel" style="background: linear-gradient(135deg, rgba(214,179,94,0.1) 0%, rgba(214,179,94,0.02) 100%); border: 1px solid rgba(214,179,94,0.2);">
  <div style="display: flex; align-items: flex-start; gap: 20px;">
    <div style="font-size: 48px; line-height: 1;">◈</div>
    <div>
      <h2 style="margin: 0 0 12px 0; font-size: 24px; color: var(--text);">Welcome to The Arc</h2>
      <p style="margin: 0 0 16px 0; color: var(--muted); line-height: 1.6; font-size: 15px;">
        Strategic Control Center for AI Architecture, Governance & Deployment. 
        Navigate through chapters using the sidebar, track progress, and access detailed block documentation.
      </p>
      <div style="display: flex; gap: 12px; flex-wrap: wrap;">
        <a href="#chapters" style="display: inline-flex; align-items: center; gap: 8px; padding: 10px 20px; background: var(--accent); color: #0f0f11; text-decoration: none; border-radius: 8px; font-weight: 600; font-size: 14px;">
          Explore Chapters →
        </a>
        <a href="prompts.html" style="display: inline-flex; align-items: center; gap: 8px; padding: 10px 20px; background: rgba(255,255,255,0.05); color: var(--text); text-decoration: none; border-radius: 8px; font-weight: 500; font-size: 14px; border: 1px solid var(--line);">
          View Prompts
        </a>
      </div>
    </div>
  </div>
</div>
'''
    
    # Vervang eerste panel na hero-grid met welcome panel
    content = re.sub(
        r'(<div class="hero-grid">.*?<div class="panel">)(.*?)(</div>\s*<div class="panel">)',
        r'\1' + welcome_panel + r'</div>\s*<div class="panel">',
        content,
        flags=re.DOTALL,
        count=1
    )
    
    with open(index_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Index.html aangepast:")
    print("   - Topbar verwijderd")
    print("   - Quick Read verwijderd")
    print("   - Theme switcher toegevoegd (Dark/Light + 4 kleuren)")
    print("   - Welcome panel toegevoegd")
    print("   - Preferences worden onthouden in localStorage")

if __name__ == "__main__":
    fix_index()
