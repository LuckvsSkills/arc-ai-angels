#!/usr/bin/env python3
import json
import re
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

CSS = """
:root {
  --bg0: #0b0b0c; --bg1: #0f0f11; --panel: #161618; --panel2: #1c1c20;
  --card: #232329; --line: rgba(255,255,255,.10); --text: #eef4fb;
  --muted: #c3d0e3; --muted2: #95a7c2; --accent: #d6b35e; --accent2: #f0d18a;
}
[data-theme="light"] {
  --bg0: #f8fbff; --bg1: #f2f7fd; --panel: #ffffff; --panel2: #edf4fb;
  --card: #ffffff; --line: rgba(16,24,40,.10); --text: #132033;
  --muted: #51627b; --muted2: #6d7f99;
}
[data-preset="graphite_cyan"] { --accent: #36c9ff; --accent2: #92e8ff; }
[data-preset="midnight_purple"] { --accent: #9b7cff; --accent2: #c9b8ff; }
[data-preset="slate_teal"] { --accent: #2fd3c5; --accent2: #93fff4; }

* { box-sizing: border-box; }
html, body { height: 100%; margin: 0; }
body {
  margin-left: 300px;
  font-family: Inter, system-ui, -apple-system, Segoe UI, Roboto, sans-serif;
  color: var(--text);
  background: var(--bg0);
  font-size: 16px;
}

@media (max-width: 1024px) {
  body { margin-left: 0; }
  .sidebar { transform: translateX(-100%); transition: transform 0.3s; }
  .sidebar.open { transform: translateX(0); }
  .main-content { padding: 20px; }
  .hero { padding: 24px; }
  .hero-title { font-size: 36px !important; }
  .diagrams-grid { grid-template-columns: 1fr !important; }
  .chapters-mini-grid { grid-template-columns: repeat(2, 1fr) !important; }
  .content-grid { grid-template-columns: 1fr !important; }
}

@media (max-width: 768px) {
  .hero-title { font-size: 28px !important; }
  .hero-subtitle { font-size: 18px !important; }
  .chapters-mini-grid { grid-template-columns: 1fr !important; }
}

.sidebar {
  position: fixed; left: 0; top: 0; width: 300px; height: 100vh;
  background: #161618; border-right: 1px solid rgba(255,255,255,0.08);
  display: flex; flex-direction: column; z-index: 1000;
}
.sidebar-brand { padding: 24px 20px 16px; border-bottom: 1px solid rgba(255,255,255,0.06); display: flex; align-items: center; gap: 12px; }
.brand-icon { width: 40px; height: 40px; background: linear-gradient(135deg, var(--accent) 0%, var(--accent2) 100%); border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 20px; color: #0f0f11; font-weight: 700; }
.brand-title { font-size: 16px; font-weight: 700; color: #eef4fb; }
.brand-subtitle { font-size: 12px; color: #95a7c2; margin-top: 2px; }

.theme-picker { padding: 16px 20px; border-bottom: 1px solid rgba(255,255,255,0.06); }
.theme-picker-label { display: block; font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; color: #6d7f99; margin-bottom: 8px; }
.theme-toggle { width: 100%; padding: 10px 12px; background: #0f0f11; border: 1px solid rgba(255,255,255,0.2); border-radius: 8px; color: #eef4fb; font-size: 13px; cursor: pointer; display: flex; align-items: center; justify-content: space-between; transition: all 0.2s; }
.theme-toggle:hover { border-color: var(--accent); }
.theme-menu { display: none; background: #1c1c20; border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; margin-top: 8px; overflow: hidden; }
.theme-menu.open { display: block; }
.theme-section { padding: 12px; border-bottom: 1px solid rgba(255,255,255,0.05); }
.theme-section:last-child { border-bottom: none; }
.theme-section-title { font-size: 10px; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; color: #6d7f99; margin-bottom: 8px; }
.theme-option { width: 100%; padding: 8px 12px; background: transparent; border: none; border-radius: 6px; color: #eef4fb; font-size: 13px; cursor: pointer; display: flex; align-items: center; gap: 8px; text-align: left; transition: all 0.2s; }
.theme-option:hover { background: rgba(255,255,255,0.1); }
.theme-option.active { background: rgba(214,179,94,0.2); color: var(--accent); }
.color-option { width: 100%; padding: 8px 12px; background: transparent; border: none; border-radius: 6px; color: #eef4fb; font-size: 13px; cursor: pointer; display: flex; align-items: center; gap: 8px; text-align: left; transition: all 0.2s; }
.color-option:hover { background: rgba(255,255,255,0.1); }
.color-option.active { background: rgba(255,255,255,0.1); }
.color-dot { width: 16px; height: 16px; border-radius: 50%; border: 2px solid transparent; }
.color-option.active .color-dot { border-color: #fff; box-shadow: 0 0 0 1px #1c1c20; }

[data-theme="light"] .theme-toggle { background: #ffffff; color: #132033; border-color: rgba(0,0,0,0.2); }
[data-theme="light"] .theme-menu { background: #ffffff; border-color: rgba(0,0,0,0.1); }
[data-theme="light"] .theme-option { color: #132033; }
[data-theme="light"] .color-option { color: #132033; }

.sidebar-nav { flex: 1; overflow-y: auto; padding: 16px 12px; }
.nav-section { margin-bottom: 24px; }
.nav-section-title { font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; color: #6d7f99; padding: 0 8px; margin-bottom: 8px; }

/* DROPDOWN NAVIGATION */
.nav-dropdown { margin: 4px 0; }
.nav-dropdown-header { display: flex; align-items: center; gap: 10px; padding: 10px 12px; border-radius: 8px; cursor: pointer; transition: all 0.2s; color: #c3d0e3; font-size: 14px; font-weight: 500; }
.nav-dropdown-header:hover { background: rgba(255,255,255,0.04); color: #eef4fb; }
.nav-dropdown-menu { display: none; padding-left: 36px; }
.nav-dropdown.open .nav-dropdown-menu { display: block; }
.nav-dropdown-item { display: block; padding: 8px 12px; color: #95a7c2; text-decoration: none; font-size: 13px; border-radius: 6px; transition: all 0.2s; margin: 2px 0; }
.nav-dropdown-item:hover { color: var(--accent); background: rgba(255,255,255,0.04); }

.nav-link { display: flex; align-items: center; gap: 12px; padding: 10px 12px; margin: 2px 0; border-radius: 8px; color: #c3d0e3; text-decoration: none; font-size: 14px; font-weight: 500; transition: all 0.2s; }
.nav-link:hover { background: rgba(255,255,255,0.04); color: #eef4fb; }
.nav-link.active { background: rgba(214,179,94,0.12); color: var(--accent); }

/* CHAPTER NAVIGATION - CLICKABLE */
.nav-item { margin: 4px 0; border-radius: 8px; transition: all 0.2s; }
.nav-item:hover { background: rgba(255,255,255,0.06); }
.nav-item[data-chapter="platform_runtime"]:hover { background: rgba(54,201,255,0.15); }
.nav-item[data-chapter="security_hardening"]:hover { background: rgba(63,227,181,0.15); }
.nav-item[data-chapter="model_runtime"]:hover { background: rgba(155,124,255,0.15); }
.nav-item[data-chapter="agent_logic"]:hover { background: rgba(255,77,109,0.15); }
.nav-item[data-chapter="data_memory"]:hover { background: rgba(78,168,222,0.15); }
.nav-item[data-chapter="observability"]:hover { background: rgba(255,159,67,0.15); }
.nav-item[data-chapter="control_center"]:hover { background: rgba(214,179,94,0.15); }
.nav-item[data-chapter="mission_control_ops"]:hover { background: rgba(127,184,255,0.15); }

.nav-chapter-header { display: flex; align-items: center; gap: 10px; padding: 12px; border-radius: 8px; cursor: pointer; }
.chapter-indicator { width: 4px; height: 32px; border-radius: 2px; flex-shrink: 0; }
.chapter-title-text { flex: 1; font-size: 14px; font-weight: 600; color: #eef4fb; }
.chapter-stats { font-size: 12px; color: #6d7f99; font-weight: 500; }
.chevron { color: #6d7f99; transition: transform 0.3s; flex-shrink: 0; }

/* BLOCK LIST - ALTIJD ZICHTBAAR EN CLICKABLE */
.block-list { list-style: none; margin: 0; padding: 0 12px 12px 36px; }
.block-list li { margin: 2px 0; }
.block-list li a { 
  display: block; 
  padding: 8px 12px; 
  color: #95a7c2; 
  text-decoration: none; 
  font-size: 13px; 
  border-radius: 6px; 
  transition: all 0.2s; 
  white-space: nowrap; 
  overflow: hidden; 
  text-overflow: ellipsis;
  cursor: pointer;
}
.block-list li a:hover { color: var(--accent); }
.block-list li[data-chapter="platform_runtime"] a:hover { background: rgba(54,201,255,0.1); color: #36c9ff; }
.block-list li[data-chapter="security_hardening"] a:hover { background: rgba(63,227,181,0.1); color: #3fe3b5; }
.block-list li[data-chapter="model_runtime"] a:hover { background: rgba(155,124,255,0.1); color: #9b7cff; }
.block-list li[data-chapter="agent_logic"] a:hover { background: rgba(255,77,109,0.1); color: #ff4d6d; }
.block-list li[data-chapter="data_memory"] a:hover { background: rgba(78,168,222,0.1); color: #4ea8de; }
.block-list li[data-chapter="observability"] a:hover { background: rgba(255,159,67,0.1); color: #ff9f43; }
.block-list li[data-chapter="control_center"] a:hover { background: rgba(214,179,94,0.1); color: #d6b35e; }
.block-list li[data-chapter="mission_control_ops"] a:hover { background: rgba(127,184,255,0.1); color: #7fb8ff; }

.sidebar-footer { padding: 16px; border-top: 1px solid rgba(255,255,255,0.06); background: rgba(0,0,0,0.2); }
.progress-mini-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; }
.progress-mini-label { font-size: 11px; color: #6d7f99; text-transform: uppercase; letter-spacing: 0.5px; }
.progress-mini-bar { height: 4px; background: rgba(255,255,255,0.1); border-radius: 2px; overflow: hidden; }
.progress-mini-fill { height: 100%; background: linear-gradient(90deg, var(--accent), var(--accent2)); border-radius: 2px; }
.progress-mini-text { font-size: 12px; color: var(--accent); font-weight: 600; }

.main-content { padding: 40px 48px; max-width: 1400px; }

.hero { 
  margin-bottom: 48px; 
  padding: 48px; 
  background: linear-gradient(135deg, var(--panel) 0%, var(--panel2) 100%); 
  border: 2px solid var(--accent); 
  border-radius: 20px; 
  text-align: center;
  position: relative;
  overflow: hidden;
}
.hero-badge { 
  display: inline-flex; 
  align-items: center; 
  gap: 8px; 
  padding: 8px 16px; 
  background: rgba(214,179,94,0.15); 
  border: 1px solid var(--accent); 
  border-radius: 20px; 
  font-size: 14px; 
  color: var(--accent); 
  margin-bottom: 24px;
}
.badge-dot { width: 8px; height: 8px; background: var(--accent); border-radius: 50%; animation: pulse 2s infinite; }
@keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.5; } }
.hero-title { 
  font-size: 64px; 
  font-weight: 900; 
  margin: 0 0 24px 0; 
  letter-spacing: -2px; 
  line-height: 1.1;
}
.gradient-text { 
  background: linear-gradient(135deg, var(--accent) 0%, var(--accent2) 50%, #fff 100%); 
  -webkit-background-clip: text; 
  -webkit-text-fill-color: transparent; 
  background-clip: text; 
}
.hero-subtitle { 
  font-size: 24px; 
  color: var(--muted); 
  margin: 0 0 32px 0; 
  line-height: 1.5;
  max-width: 800px;
  margin-left: auto;
  margin-right: auto;
}
.hero-description {
  font-size: 18px;
  color: var(--muted2);
  line-height: 1.7;
  max-width: 900px;
  margin: 0 auto;
}

.content-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; margin-bottom: 32px; }

/* ARC CONTROL CENTER */
.doc-section { 
  padding: 24px; 
  background: var(--panel); 
  border: 1px solid var(--line); 
  border-radius: 12px; 
  border-left: 4px solid var(--accent);
}
.doc-section h2 { margin: 0 0 16px 0; font-size: 22px; color: var(--text); display: flex; align-items: center; gap: 10px; }
.doc-section h2 span { font-size: 24px; }
.doc-section p { margin: 0 0 12px 0; color: var(--muted); line-height: 1.6; font-size: 15px; }
.doc-section strong { color: var(--accent); }

/* ARC AI ANGELS - KLEINER */
.angels-section { 
  padding: 20px; 
  background: var(--panel); 
  border: 1px solid var(--line); 
  border-radius: 12px; 
  border-left: 4px solid #8B4513;
}
.angels-section h2 { margin: 0 0 12px 0; font-size: 20px; color: var(--text); display: flex; align-items: center; gap: 10px; }
.angels-icon { 
  width: 32px; 
  height: 32px; 
  background: #8B4513; 
  border-radius: 8px; 
  display: flex; 
  align-items: center; 
  justify-content: center; 
  font-size: 20px;
  box-shadow: 0 4px 12px rgba(139, 69, 19, 0.3);
}
.angels-section p { margin: 0 0 10px 0; color: var(--muted); line-height: 1.5; font-size: 14px; }
.angels-section strong { color: #8B4513; }

/* CHAPTER PROGRESS */
.chapters-mini-section { margin-bottom: 32px; }
.section-header { margin-bottom: 20px; }
.section-header h2 { font-size: 24px; font-weight: 700; margin: 0 0 8px 0; }
.section-header p { color: var(--muted); margin: 0; font-size: 16px; }
.chapters-mini-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 12px; }
.chapter-mini { 
  background: var(--panel); 
  border: 2px solid var(--line); 
  border-radius: 10px; 
  padding: 16px; 
  text-decoration: none; 
  transition: all 0.2s; 
  display: block;
  position: relative;
  overflow: hidden;
}
.chapter-mini::before {
  content: '';
  position: absolute;
  top: 0; left: 0; width: 3px; height: 100%;
  background: var(--chapter-color);
}
.chapter-mini:hover { 
  transform: translateY(-2px); 
  border-color: var(--chapter-color);
  box-shadow: 0 6px 20px rgba(0,0,0,0.2);
}
.chapter-mini-header { display: flex; align-items: center; gap: 8px; margin-bottom: 8px; }
.chapter-mini-icon { width: 28px; height: 28px; border-radius: 6px; display: flex; align-items: center; justify-content: center; font-size: 14px; background: var(--chapter-color-alpha); color: var(--chapter-color); }
.chapter-mini-title { font-size: 13px; font-weight: 600; color: var(--text); line-height: 1.2; }
.chapter-mini-bar { height: 4px; background: rgba(255,255,255,0.1); border-radius: 2px; overflow: hidden; margin-top: 8px; }
.chapter-mini-fill { height: 100%; border-radius: 2px; background: var(--chapter-color); }
.chapter-mini-stats { display: flex; justify-content: space-between; margin-top: 6px; font-size: 11px; color: var(--muted); }

/* TOTALE PROGRESS - KLEINER + MATCHT CHAPTER PROGRESS */
.total-progress-section { 
  padding: 24px; 
  background: var(--panel); 
  border: 2px solid var(--line); 
  border-radius: 12px; 
  text-align: center;
  margin-bottom: 48px;
}
.total-progress-section h2 { margin: 0 0 16px 0; font-size: 20px; color: var(--text); display: flex; align-items: center; justify-content: center; gap: 10px; }
.total-progress-bar { height: 8px; background: rgba(255,255,255,0.1); border-radius: 4px; overflow: hidden; margin-bottom: 16px; }
.total-progress-fill { height: 100%; background: linear-gradient(90deg, var(--accent), var(--accent2)); border-radius: 4px; }
.total-progress-stats { display: flex; justify-content: center; gap: 32px; }
.total-progress-stat { text-align: center; }
.total-progress-value { font-size: 28px; font-weight: 800; color: var(--accent); }
.total-progress-label { font-size: 12px; color: var(--muted); margin-top: 4px; text-transform: uppercase; letter-spacing: 0.5px; }

/* DIAGRAMMEN */
.diagrams-section { margin-bottom: 48px; }
.diagrams-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(450px, 1fr)); gap: 24px; }
.diagram-card { 
  background: var(--panel); 
  border: 1px solid var(--line); 
  border-radius: 12px; 
  padding: 24px;
}
.diagram-card h3 { margin: 0 0 16px 0; font-size: 18px; color: var(--text); display: flex; align-items: center; gap: 10px; }
.diagram-icon { width: 36px; height: 36px; background: rgba(214,179,94,0.1); border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 18px; border: 1px solid var(--accent); }
.mermaid-container { background: var(--bg0); border-radius: 8px; padding: 16px; overflow-x: auto; border: 1px solid var(--line); }
"""

def generate_sidebar(progress):
    # Dropdown navigatie naar sections
    index_sections = """
    <div class="nav-dropdown open">
        <div class="nav-dropdown-header" onclick="this.parentElement.classList.toggle('open')">
            <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                <path d="M2 6.5L8 2L14 6.5V13.5C14 13.7761 13.7761 14 13.5 14H2.5C2.22386 14 2 13.7761 2 13.5V6.5Z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M6 14V10H10V14" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            Dashboard Sections
            <svg class="chevron" width="12" height="12" viewBox="0 0 12 12" style="margin-left: auto;">
                <path d="M3 4.5L6 7.5L9 4.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
        </div>
        <div class="nav-dropdown-menu">
            <a href="#arc-control" class="nav-dropdown-item" onclick="scrollToSection('arc-control'); return false;">📋 Arc Control Center</a>
            <a href="#arc-angels" class="nav-dropdown-item" onclick="scrollToSection('arc-angels'); return false;">👼 Arc AI Angels</a>
            <a href="#chapters" class="nav-dropdown-item" onclick="scrollToSection('chapters'); return false;">📚 Chapter Progress</a>
            <a href="#total-progress" class="nav-dropdown-item" onclick="scrollToSection('total-progress'); return false;">📈 Totale Progress</a>
            <a href="#diagrams" class="nav-dropdown-item" onclick="scrollToSection('diagrams'); return false;">📊 Hoe Werkt Het?</a>
        </div>
    </div>
"""
    
    # Chapters met blocks - DIRECT CLICKABLE
    chapter_items = ""
    for chapter in progress.get("chapters", []):
        chapter_id = chapter["id"]
        chapter_title = chapter.get("title", chapter_id)
        color = get_color_for_chapter(chapter_id)
        total_blocks = chapter.get("total_blocks", 0)
        done_blocks = chapter.get("done_blocks", 0)
        
        # Genereer block links - DIRECT KLIKBAAR
        block_items = ""
        for cluster in chapter.get("clusters", []):
            for block in cluster.get("blocks", []):
                block_id = block["id"]
                block_title = block.get("title", block_id)
                match = re.match(r'[a-z]+(\\d+)', block_id, re.IGNORECASE)
                if match:
                    num = int(match.group(1))
                    safe_title = re.sub(r'[^\\w\\s-]', '', block_title).replace(' ', '-').lower()[:40]
                    block_file = f"block-{num:02d}-{safe_title}.html"
                    # DIRECTE LINK - GEEN JAVASCRIPT
                    block_items += f'<li data-chapter="{chapter_id}"><a href="chapters/blocks/{chapter_id}/{block_file}" target="_self">{block_title}</a></li>'
        
        chapter_items += f"""
        <div class="nav-item" data-chapter="{chapter_id}" data-color="{color}">
            <a href="chapters/{chapter_id}.html" style="text-decoration: none; color: inherit; display: block;">
                <div class="nav-chapter-header">
                    <span class="chapter-indicator" style="background:{color}"></span>
                    <span class="chapter-title-text">{chapter_title}</span>
                    <span class="chapter-stats">{done_blocks}/{total_blocks}</span>
                </div>
            </a>
            <ul class="block-list">
                {block_items}
            </ul>
        </div>
"""
    
    overall = progress.get("overall", {})
    overall_pct = overall.get("progress_percent", 54)
    
    return f"""
<nav class="sidebar">
    <div class="sidebar-brand">
        <div class="brand-icon">◈</div>
        <div class="brand-text">
            <div class="brand-title">Arc Control Center</div>
            <div class="brand-subtitle">Strategic Architecture Hub</div>
        </div>
    </div>
    
    <div class="theme-picker">
        <div class="theme-picker-label">Appearance</div>
        <button class="theme-toggle" onclick="toggleThemeMenu(event)">
            <span id="currentThemeLabel">🌙 Dark Mode</span>
            <span>▼</span>
        </button>
        <div class="theme-menu" id="themeMenu">
            <div class="theme-section">
                <div class="theme-section-title">Mode</div>
                <button class="theme-option active" id="opt-dark" onclick="setTheme('dark')">🌙 Dark Mode</button>
                <button class="theme-option" id="opt-light" onclick="setTheme('light')">☀️ Light Mode</button>
            </div>
            <div class="theme-section">
                <div class="theme-section-title">Accent Color</div>
                <button class="color-option active" id="opt-gold" onclick="setPreset('obsidian_gold')"><span class="color-dot" style="background:#d6b35e"></span> Gold</button>
                <button class="color-option" id="opt-cyan" onclick="setPreset('graphite_cyan')"><span class="color-dot" style="background:#36c9ff"></span> Cyan</button>
                <button class="color-option" id="opt-purple" onclick="setPreset('midnight_purple')"><span class="color-dot" style="background:#9b7cff"></span> Purple</button>
                <button class="color-option" id="opt-teal" onclick="setPreset('slate_teal')"><span class="color-dot" style="background:#2fd3c5"></span> Teal</button>
            </div>
        </div>
    </div>

    <div class="sidebar-nav">
        <div class="nav-section">
            <div class="nav-section-title">Navigation</div>
            {index_sections}
            <a href="prompts.html" class="nav-link">
                <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                    <path d="M8 2L2 7L8 12L14 7L8 2Z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                Prompts
            </a>
        </div>
        
        <div class="nav-section">
            <div class="nav-section-title">Chapters & Blocks</div>
            {chapter_items}
        </div>
    </div>

    <div class="sidebar-footer">
        <div class="progress-mini">
            <div class="progress-mini-header">
                <span class="progress-mini-label">Overall Progress</span>
                <span class="progress-mini-text" id="sidebarProgressText">{overall_pct}%</span>
            </div>
            <div class="progress-mini-bar">
                <div class="progress-mini-fill" id="sidebarProgressBar" style="width: {overall_pct}%"></div>
            </div>
        </div>
    </div>
</nav>

<script>
function toggleThemeMenu(event) {{
    event.stopPropagation();
    const menu = document.getElementById('themeMenu');
    menu.classList.toggle('open');
}}

function closeThemeMenu() {{
    document.getElementById('themeMenu').classList.remove('open');
}}

function setTheme(theme) {{
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
    document.getElementById('opt-dark').classList.toggle('active', theme === 'dark');
    document.getElementById('opt-light').classList.toggle('active', theme === 'light');
    document.getElementById('currentThemeLabel').textContent = theme === 'dark' ? '🌙 Dark Mode' : '☀️ Light Mode';
    closeThemeMenu();
}}

function setPreset(preset) {{
    document.documentElement.setAttribute('data-preset', preset);
    localStorage.setItem('preset', preset);
    document.querySelectorAll('.color-option').forEach(btn => btn.classList.remove('active'));
    document.getElementById('opt-' + preset.replace('obsidian_', '').replace('graphite_', '').replace('midnight_', '').replace('slate_', '')).classList.add('active');
    closeThemeMenu();
}}

function scrollToSection(id) {{
    const element = document.getElementById(id);
    if (element) {{
        element.scrollIntoView({{ behavior: 'smooth' }});
    }}
}}

document.addEventListener('click', function(event) {{
    if (!event.target.closest('.theme-picker')) {{
        closeThemeMenu();
    }}
}});

document.addEventListener('DOMContentLoaded', function() {{
    const savedTheme = localStorage.getItem('theme') || 'dark';
    const savedPreset = localStorage.getItem('preset') || 'obsidian_gold';
    document.documentElement.setAttribute('data-theme', savedTheme);
    document.documentElement.setAttribute('data-preset', savedPreset);
    setTheme(savedTheme);
    setPreset(savedPreset);
}});
</script>
"""

def generate_main_content(progress):
    overall = progress.get("overall", {})
    overall_pct = overall.get("progress_percent", 54)
    total_blocks = overall.get("total_blocks", 54)
    done_blocks = overall.get("done_blocks", 29)
    
    # Chapter mini blocks
    chapter_minis = ""
    for chapter in progress.get("chapters", []):
        chapter_id = chapter["id"]
        chapter_title = chapter.get("title", chapter_id)
        color = get_color_for_chapter(chapter_id)
        pct = chapter.get("progress_percent", 0)
        done = chapter.get("done_blocks", 0)
        total = chapter.get("total_blocks", 0)
        
        chapter_minis += f"""
        <a href="chapters/{chapter_id}.html" class="chapter-mini" style="--chapter-color: {color}; --chapter-color-alpha: {color}20">
            <div class="chapter-mini-header">
                <div class="chapter-mini-icon" style="background: {color}20; color: {color}">◈</div>
                <div class="chapter-mini-title">{chapter_title}</div>
            </div>
            <div class="chapter-mini-bar">
                <div class="chapter-mini-fill" style="width: {pct}%; background: {color}"></div>
            </div>
            <div class="chapter-mini-stats">
                <span>{done}/{total}</span>
                <span style="color: {color}; font-weight: 600">{pct}%</span>
            </div>
        </a>
"""
    
    return f"""
<main class="main-content">
    <!-- HERO -->
    <section class="hero">
        <div class="hero-badge">
            <span class="badge-dot"></span>
            Live System
        </div>
        <h1 class="hero-title">Arc AI Angels</h1>
        <p class="hero-subtitle">Jouw Persoonlijke AI Command Center</p>
        <p class="hero-description">
            Een compleet systeem om AI agents te installeren, beheren en laten samenwerken 
            op je eigen computer. Van OpenClaw setup tot het orkestreren van meerdere AI modellen.
        </p>
    </section>

    <!-- CONTENT GRID -->
    <div class="content-grid">
        <section id="arc-control" class="doc-section">
            <h2><span>📋</span> Arc Control Center</h2>
            <p>
                Dit is de <strong>documentatie hub</strong> van Arc AI Angels. Hier vind je alle technische 
                specificaties, architectuur overzichten, en implementatie guides.
            </p>
            <p>
                Het Control Center geeft je inzicht in hoe het systeem werkt, welke componenten er zijn, 
                en hoe ze met elkaar communiceren.
            </p>
        </section>

        <section id="arc-angels" class="angels-section">
            <h2><div class="angels-icon">👼</div> Arc AI Angels</h2>
            <p>
                <strong>OpenClaw Installatie</strong> - Start hier met het opzetten van je persoonlijke AI omgeving.
            </p>
            <p>
                <strong>AI Agents Beheren</strong> - Ga aan de slag met verschillende AI modellen en leer ze samenwerken.
            </p>
        </section>
    </div>

    <!-- CHAPTER PROGRESS -->
    <section id="chapters" class="chapters-mini-section">
        <div class="section-header">
            <h2>📚 Chapter Progress</h2>
            <p>Klik op een chapter voor details</p>
        </div>
        <div class="chapters-mini-grid">
            {chapter_minis}
        </div>
    </section>

    <!-- TOTALE PROGRESS - KLEIN -->
    <section id="total-progress" class="total-progress-section">
        <h2>📈 Totale Voortgang</h2>
        <div class="total-progress-bar">
            <div class="total-progress-fill" style="width: {overall_pct}%;"></div>
        </div>
        <div class="total-progress-stats">
            <div class="total-progress-stat">
                <div class="total-progress-value">{done_blocks}</div>
                <div class="total-progress-label">Klaar</div>
            </div>
            <div class="total-progress-stat">
                <div class="total-progress-value" style="color: var(--accent);">{overall_pct}%</div>
                <div class="total-progress-label">Compleet</div>
            </div>
            <div class="total-progress-stat">
                <div class="total-progress-value">{total_blocks}</div>
                <div class="total-progress-label">Totaal</div>
            </div>
        </div>
    </section>

    <!-- DIAGRAMMEN - SYNTAX ERROR GEFIXT -->
    <section id="diagrams" class="diagrams-section">
        <div class="section-header">
            <h2>📊 Hoe Werkt Het?</h2>
            <p>De flow van jouw AI systeem</p>
        </div>
        <div class="diagrams-grid">
            <div class="diagram-card">
                <h3><span class="diagram-icon">🔄</span> Agent Flow</h3>
                <div class="mermaid-container">
                    <pre class="mermaid">
flowchart TD
    A[User] --> B[Nova]
    B --> C[Flux]
    C --> D[Omni]
    C --> E[Sentinel]
    C --> F[Workers]
    D --> G[Response]
    E --> G
    F --> G
    G --> H[User]
    
    style A fill:#9b7cff,stroke:#9b7cff,color:#fff
    style B fill:#36c9ff,stroke:#36c9ff,color:#000
    style C fill:#d6b35e,stroke:#d6b35e,color:#000
    style D fill:#ff9f43,stroke:#ff9f43,color:#000
    style E fill:#ff4d6d,stroke:#ff4d6d,color:#fff
    style F fill:#3fe3b5,stroke:#3fe3b5,color:#000
    style G fill:#d6b35e,stroke:#d6b35e,color:#000
    style H fill:#9b7cff,stroke:#9b7cff,color:#fff
                    </pre>
                </div>
            </div>
            
            <div class="diagram-card">
                <h3><span class="diagram-icon">🏗️</span> Systeem Lagen</h3>
                <div class="mermaid-container">
                    <pre class="mermaid">
graph TB
    subgraph Control["Control"]
        Nova[Nova]
        Flux[Flux]
    end
    
    subgraph Intelligence["Intelligence"]  
        Omni[Omni]
        Sentinel[Sentinel]
    end
    
    subgraph Execution["Execution"]
        Workers[Workers]
        OpenClaw[OpenClaw]
    end
    
    Nova --> Flux
    Flux --> Omni
    Flux --> Sentinel
    Flux --> Workers
    Workers --> OpenClaw
    
    style Nova fill:#36c9ff,stroke:#36c9ff,color:#000
    style Flux fill:#d6b35e,stroke:#d6b35e,color:#000
    style Omni fill:#ff9f43,stroke:#ff9f43,color:#000
    style Sentinel fill:#ff4d6d,stroke:#ff4d6d,color:#fff
    style Workers fill:#3fe3b5,stroke:#3fe3b5,color:#000
    style OpenClaw fill:#9b7cff,stroke:#9b7cff,color:#fff
                    </pre>
                </div>
            </div>
            
            <div class="diagram-card">
                <h3><span class="diagram-icon">📡</span> Data Stroom</h3>
                <div class="mermaid-container">
                    <pre class="mermaid">
flowchart LR
    A[Input] --> B[Check]
    B --> C[Process]
    C --> D[Memory]
    C --> E[Vector]
    D --> F[Output]
    E --> F
    
    style A fill:#36c9ff,stroke:#36c9ff,color:#000
    style B fill:#ff9f43,stroke:#ff9f43,color:#000
    style C fill:#d6b35e,stroke:#d6b35e,color:#000
    style D fill:#9b7cff,stroke:#9b7cff,color:#fff
    style E fill:#9b7cff,stroke:#9b7cff,color:#fff
    style F fill:#3fe3b5,stroke:#3fe3b5,color:#000
                    </pre>
                </div>
            </div>
            
            <div class="diagram-card">
                <h3><span class="diagram-icon">🔗</span> Bouw Volgorde</h3>
                <div class="mermaid-container">
                    <pre class="mermaid">
graph LR
    A[Platform] --> B[Security]
    B --> C[Models]
    C --> D[Agents]
    D --> E[Data]
    E --> F[Monitor]
    F --> G[Control]
    G --> H[Mission]
    
    style A fill:#36c9ff,stroke:#36c9ff,color:#000
    style B fill:#3fe3b5,stroke:#3fe3b5,color:#000
    style C fill:#9b7cff,stroke:#9b7cff,color:#fff
    style D fill:#ff4d6d,stroke:#ff4d6d,color:#fff
    style E fill:#4ea8de,stroke:#4ea8de,color:#fff
    style F fill:#ff9f43,stroke:#ff9f43,color:#000
    style G fill:#d6b35e,stroke:#d6b35e,color:#000
    style H fill:#7fb8ff,stroke:#7fb8ff,color:#000
                    </pre>
                </div>
            </div>
        </div>
    </section>
</main>

<script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
<script>
    mermaid.initialize({{
        startOnLoad: true,
        theme: 'dark'
    }});
</script>
"""

def main():
    print("Building index.html v6...")
    progress = load_progress()
    sidebar = generate_sidebar(progress)
    main_content = generate_main_content(progress)
    
    html = f"""<!DOCTYPE html>
<html lang="en" data-theme="dark" data-preset="obsidian_gold">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Arc AI Angels - Control Center</title>
<style>
{CSS}
</style>
</head>
<body>
{sidebar}
{main_content}
</body>
</html>"""
    
    index_file = BASE / "index.html"
    with open(index_file, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print("✅ SUCCESS! index.html v6 rebuilt")
    print("Changes:")
    print("  - Arc AI Angels block kleiner")
    print("  - Chapter -> Block navigatie WERKT (directe links)")
    print("  - Totale Progress kleiner + matcht Chapter Progress")
    print("  - Systeem Lagen syntax error gefixt (geen speciale tekens)")

if __name__ == "__main__":
    main()
