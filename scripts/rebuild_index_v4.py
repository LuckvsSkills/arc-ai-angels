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

.sidebar {
  position: fixed; left: 0; top: 0; width: 300px; height: 100vh;
  background: #161618; border-right: 1px solid rgba(255,255,255,0.08);
  display: flex; flex-direction: column; z-index: 1000;
}
.sidebar-brand { padding: 24px 20px 16px; border-bottom: 1px solid rgba(255,255,255,0.06); display: flex; align-items: center; gap: 12px; }
.brand-icon { width: 40px; height: 40px; background: linear-gradient(135deg, var(--accent) 0%, var(--accent2) 100%); border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 20px; color: #0f0f11; font-weight: 700; }
.brand-title { font-size: 16px; font-weight: 700; color: #eef4fb; }
.brand-subtitle { font-size: 12px; color: #95a7c2; margin-top: 2px; }

/* THEME PICKER */
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
.nav-link { display: flex; align-items: center; gap: 12px; padding: 10px 12px; margin: 2px 0; border-radius: 8px; color: #c3d0e3; text-decoration: none; font-size: 14px; font-weight: 500; transition: all 0.2s; }
.nav-link:hover { background: rgba(255,255,255,0.04); color: #eef4fb; }
.nav-link.active { background: rgba(214,179,94,0.12); color: var(--accent); }

/* CHAPTER NAVIGATION - BLOCKS DIRECT ZICHTBAAR */
.nav-item { margin: 4px 0; border-radius: 8px; cursor: pointer; transition: all 0.2s; }
.nav-item:hover { background: rgba(255,255,255,0.06); }
.nav-item[data-chapter="platform_runtime"]:hover { background: rgba(54,201,255,0.15); }
.nav-item[data-chapter="security_hardening"]:hover { background: rgba(63,227,181,0.15); }
.nav-item[data-chapter="model_runtime"]:hover { background: rgba(155,124,255,0.15); }
.nav-item[data-chapter="agent_logic"]:hover { background: rgba(255,77,109,0.15); }
.nav-item[data-chapter="data_memory"]:hover { background: rgba(78,168,222,0.15); }
.nav-item[data-chapter="observability"]:hover { background: rgba(255,159,67,0.15); }
.nav-item[data-chapter="control_center"]:hover { background: rgba(214,179,94,0.15); }
.nav-item[data-chapter="mission_control_ops"]:hover { background: rgba(127,184,255,0.15); }

.nav-chapter-header { display: flex; align-items: center; gap: 10px; padding: 12px; border-radius: 8px; }
.chapter-indicator { width: 4px; height: 32px; border-radius: 2px; flex-shrink: 0; }
.chapter-title-text { flex: 1; font-size: 14px; font-weight: 600; color: #eef4fb; }
.chapter-stats { font-size: 12px; color: #6d7f99; font-weight: 500; }
.chevron { color: #6d7f99; transition: transform 0.3s; flex-shrink: 0; }

/* BLOCKS ALTIJD ZICHTBAAR */
.block-list { list-style: none; margin: 0; padding: 0 12px 12px 36px; }
.block-list li { margin: 2px 0; }
.block-list li a { display: block; padding: 8px 12px; color: #95a7c2; text-decoration: none; font-size: 13px; border-radius: 6px; transition: all 0.2s; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
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

/* MAIN CONTENT - GROTERE LETTERTYPES */
.main-content { padding: 40px 48px; max-width: 1400px; }

/* HERO - GROOT EN KRACHTIG */
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
.hero::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
  background: radial-gradient(circle at top right, var(--accentGlow), transparent 50%);
  pointer-events: none;
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
  position: relative;
  z-index: 1;
}
.badge-dot { width: 8px; height: 8px; background: var(--accent); border-radius: 50%; animation: pulse 2s infinite; }
@keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.5; } }
.hero-title { 
  font-size: 64px; 
  font-weight: 900; 
  margin: 0 0 24px 0; 
  letter-spacing: -2px; 
  line-height: 1.1;
  position: relative;
  z-index: 1;
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
  position: relative;
  z-index: 1;
}
.hero-description {
  font-size: 18px;
  color: var(--muted2);
  line-height: 1.7;
  max-width: 900px;
  margin: 0 auto 32px auto;
  position: relative;
  z-index: 1;
}

/* GROTE PROGRESS BAR IN HERO */
.hero-progress { margin-top: 32px; position: relative; z-index: 1; }
.hero-progress-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; }
.hero-progress-label { font-size: 14px; font-weight: 600; color: var(--muted); text-transform: uppercase; letter-spacing: 1px; }
.hero-progress-value { font-size: 32px; font-weight: 800; color: var(--accent); }
.hero-progress-bar { height: 12px; background: rgba(255,255,255,0.1); border-radius: 6px; overflow: hidden; }
.hero-progress-fill { height: 100%; background: linear-gradient(90deg, var(--accent), var(--accent2)); border-radius: 6px; transition: width 0.5s ease; box-shadow: 0 0 20px var(--accentGlow); }

/* ARC AI ANGELS SECTION */
.angels-section { margin-bottom: 48px; padding: 32px; background: var(--panel); border: 1px solid var(--line); border-radius: 16px; border-left: 4px solid var(--accent); }
.angels-section h2 { margin: 0 0 20px 0; font-size: 32px; color: var(--text); display: flex; align-items: center; gap: 12px; }
.angels-section h2 span { font-size: 36px; }
.angels-section p { margin: 0 0 16px 0; color: var(--muted); line-height: 1.7; font-size: 18px; }
.angels-section strong { color: var(--accent); }
.angels-section ul { margin: 0; padding-left: 24px; color: var(--muted2); font-size: 17px; }
.angels-section li { margin: 12px 0; }

/* DIAGRAMMEN - LEVENDIGER */
.diagrams-section { margin-bottom: 48px; }
.section-header { margin-bottom: 32px; }
.section-header h2 { font-size: 32px; font-weight: 800; margin: 0 0 12px 0; }
.section-header p { color: var(--muted); margin: 0; font-size: 18px; }
.diagrams-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(450px, 1fr)); gap: 32px; }
.diagram-card { 
  background: linear-gradient(145deg, var(--panel) 0%, var(--panel2) 100%); 
  border: 1px solid var(--line); 
  border-radius: 16px; 
  padding: 28px;
  transition: all 0.3s;
}
.diagram-card:hover {
  transform: translateY(-4px);
  border-color: var(--accent);
  box-shadow: 0 12px 40px rgba(0,0,0,0.3);
}
.diagram-card h3 { margin: 0 0 20px 0; font-size: 20px; color: var(--text); display: flex; align-items: center; gap: 12px; }
.diagram-icon { width: 40px; height: 40px; background: var(--accentGlow); border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 20px; border: 1px solid var(--accent); }
.mermaid-container { background: var(--bg0); border-radius: 12px; padding: 20px; overflow-x: auto; border: 1px solid var(--line); }

/* CHAPTER MINI BLOCKS */
.chapters-mini-section { margin-bottom: 48px; }
.chapters-mini-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 16px; }
.chapter-mini { 
  background: var(--panel); 
  border: 2px solid var(--line); 
  border-radius: 12px; 
  padding: 20px; 
  text-decoration: none; 
  transition: all 0.2s; 
  display: block;
  position: relative;
  overflow: hidden;
}
.chapter-mini::before {
  content: '';
  position: absolute;
  top: 0; left: 0; width: 4px; height: 100%;
  background: var(--chapter-color);
}
.chapter-mini:hover { 
  transform: translateY(-2px); 
  border-color: var(--chapter-color);
  box-shadow: 0 8px 24px rgba(0,0,0,0.2);
}
.chapter-mini-header { display: flex; align-items: center; gap: 12px; margin-bottom: 12px; }
.chapter-mini-icon { width: 36px; height: 36px; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 18px; background: var(--chapter-color-alpha); color: var(--chapter-color); }
.chapter-mini-title { font-size: 15px; font-weight: 700; color: var(--text); line-height: 1.3; }
.chapter-mini-progress { margin-top: 12px; }
.chapter-mini-bar { height: 6px; background: rgba(255,255,255,0.1); border-radius: 3px; overflow: hidden; }
.chapter-mini-fill { height: 100%; border-radius: 3px; background: var(--chapter-color); }
.chapter-mini-stats { display: flex; justify-content: space-between; margin-top: 8px; font-size: 13px; color: var(--muted); }
"""

def generate_sidebar(progress):
    chapter_items = ""
    for chapter in progress.get("chapters", []):
        chapter_id = chapter["id"]
        chapter_title = chapter.get("title", chapter_id)
        color = get_color_for_chapter(chapter_id)
        total_blocks = chapter.get("total_blocks", 0)
        done_blocks = chapter.get("done_blocks", 0)
        
        # Blocks direct zichtbaar (niet collapsed)
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
                    block_items += f'<li data-chapter="{chapter_id}" data-color="{color}"><a href="chapters/blocks/{chapter_id}/{block_file}">Block {num:02d}: {block_title}</a></li>'
        
        chapter_items += f"""
        <div class="nav-item" data-chapter="{chapter_id}" data-color="{color}">
            <div class="nav-chapter-header" onclick="toggleChapter(this.parentElement)">
                <span class="chapter-indicator" style="background:{color}"></span>
                <span class="chapter-title-text">{chapter_title}</span>
                <span class="chapter-stats">{done_blocks}/{total_blocks}</span>
                <svg class="chevron" width="12" height="12" viewBox="0 0 12 12" style="transform: rotate(180deg)">
                    <path d="M3 4.5L6 7.5L9 4.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
            </div>
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
            <a href="#home" class="nav-link active">
                <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                    <path d="M2 6.5L8 2L14 6.5V13.5C14 13.7761 13.7761 14 13.5 14H2.5C2.22386 14 2 13.7761 2 13.5V6.5Z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M6 14V10H10V14" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                Dashboard
            </a>
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

function toggleChapter(element) {{
    const blockList = element.querySelector('.block-list');
    const chevron = element.querySelector('.chevron');
    const isVisible = blockList.style.display !== 'none';
    
    if (isVisible) {{
        blockList.style.display = 'none';
        chevron.style.transform = 'rotate(0deg)';
    }} else {{
        blockList.style.display = 'block';
        chevron.style.transform = 'rotate(180deg)';
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
            <div class="chapter-mini-progress">
                <div class="chapter-mini-bar">
                    <div class="chapter-mini-fill" style="width: {pct}%; background: {color}"></div>
                </div>
                <div class="chapter-mini-stats">
                    <span>{done}/{total} blocks</span>
                    <span style="color: {color}; font-weight: 600">{pct}%</span>
                </div>
            </div>
        </a>
"""
    
    return f"""
<main class="main-content">
    <!-- HERO - GROOT EN DUODELIJK -->
    <section class="hero">
        <div class="hero-badge">
            <span class="badge-dot"></span>
            Live System
        </div>
        <h1 class="hero-title">Arc AI Angels</h1>
        <p class="hero-subtitle">Jouw Persoonlijke AI Command Center</p>
        <p class="hero-description">
            <strong>Wat is dit?</strong> Een compleet systeem om AI agents te installeren, beheren en laten samenwerken 
            op je eigen computer. Van OpenClaw setup tot het orkestreren van meerdere AI modellen - 
            alles gestructureerd en onder controle.
        </p>
        
        <!-- GROTE PROGRESS BAR -->
        <div class="hero-progress">
            <div class="hero-progress-header">
                <span class="hero-progress-label">Total Progress</span>
                <span class="hero-progress-value">{overall_pct}%</span>
            </div>
            <div class="hero-progress-bar">
                <div class="hero-progress-fill" style="width: {overall_pct}%;"></div>
            </div>
        </div>
    </section>

    <!-- ARC AI ANGELS - OPENCLAW FOCUS -->
    <section class="angels-section">
        <h2><span>👼</span> Arc AI Angels</h2>
        <p>
            <strong>OpenClaw Installatie</strong> - Start hier met het opzetten van je persoonlijke AI omgeving. 
            We installeren OpenClaw, configureren de runtime, en zorgen dat alles veilig staat.
        </p>
        <p>
            <strong>AI Agents Beheren</strong> - Na de installatie gaan we aan de slag met verschillende AI modellen 
            (Nova, Flux, Omni, Sentinel) en leren we ze samenwerken via een duidelijke structuur.
        </p>
        <ul>
            <li><strong>Platform & Runtime:</strong> De basis installeren en veilig maken</li>
            <li><strong>Security:</strong> Alles afschermen en monitoren</li>
            <li><strong>Model Runtime:</strong> AI modellen koppelen en configureren</li>
            <li><strong>Agent Logic:</strong> Agents taken laten uitvoeren en samenwerken</li>
            <li><strong>Data & Memory:</strong> Informatie opslaan en hergebruiken</li>
            <li><strong>Observability:</strong> Bijhouden wat er gebeurt en kosten controleren</li>
        </ul>
    </section>

    <!-- DIAGRAMMEN - LEVENDIG -->
    <section class="diagrams-section">
        <div class="section-header">
            <h2>📊 Hoe Werkt Het?</h2>
            <p>De flow van jouw AI systeem - van vraag tot antwoord</p>
        </div>
        <div class="diagrams-grid">
            <div class="diagram-card">
                <h3><span class="diagram-icon">🔄</span> Agent Flow</h3>
                <div class="mermaid-container">
                    <pre class="mermaid">
%%{{init: {{'theme': 'dark', 'themeVariables': {{'primaryColor': '#d6b35e', 'primaryTextColor': '#fff', 'primaryBorderColor': '#d6b35e', 'lineColor': '#36c9ff', 'secondaryColor': '#1c1c20', 'tertiaryColor': '#161618'}}}}}}%%
flowchart TD
    A[👤 Jouw Vraag] -->|🔌| B[Nova Gateway]
    B -->|📋| C{{Flux Orchestrator}}
    C -->|🧠| D[Omni Intelligence]
    C -->|🛡️| E[Sentinel Team]
    C -->|⚡| F[Execution Workers]
    D -->|📊| G[Antwoord]
    E -->|✅| G
    F -->|📝| G
    G -->|💬| H[Jij]
    
    style A fill:#9b7cff,stroke:#9b7cff,stroke-width:2px,color:#fff
    style B fill:#36c9ff,stroke:#36c9ff,stroke-width:2px,color:#000
    style C fill:#d6b35e,stroke:#d6b35e,stroke-width:3px,color:#000
    style D fill:#ff9f43,stroke:#ff9f43,stroke-width:2px,color:#000
    style E fill:#ff4d6d,stroke:#ff4d6d,stroke-width:2px,color:#fff
    style F fill:#3fe3b5,stroke:#3fe3b5,stroke-width:2px,color:#000
    style G fill:#d6b35e,stroke:#d6b35e,stroke-width:2px,color:#000
    style H fill:#9b7cff,stroke:#9b7cff,stroke-width:2px,color:#fff
                    </pre>
                </div>
            </div>
            
            <div class="diagram-card">
                <h3><span class="diagram-icon">🏗️</span> Systeem Lagen</h3>
                <div class="mermaid-container">
                    <pre class="mermaid">
%%{{init: {{'theme': 'dark', 'themeVariables': {{'primaryColor': '#d6b35e', 'primaryTextColor': '#fff', 'primaryBorderColor': '#d6b35e', 'lineColor': '#95a7c2', 'secondaryColor': '#1c1c20', 'tertiaryColor': '#161618'}}}}}}%%
graph TB
    subgraph Control["🎮 Control Laag"]
        Nova[Nova Gateway<br/>🔌 Ontvangt vragen]
        Flux[Flux Orchestrator<br/>📋 Verdeelt taken]
    end
    
    subgraph Intelligence["🧠 Intelligence Laag"]  
        Omni[Omni Intelligence<br/>🤔 Denkt na]
        Sentinel[Sentinel Team<br/>🛡️ Controleert]
    end
    
    subgraph Execution["⚡ Execution Laag"]
        Workers[Execution Workers<br/>🔨 Voert uit]
        OpenClaw[OpenClaw Runtime<br/>🖥️ Jouw Systeem]
    end
    
    Nova -.->|Stuurt door| Flux
    Flux -.->|Vraagt advies| Omni
    Flux -.->|Laat checken| Sentinel
    Flux -.->|Geeft opdracht| Workers
    Workers -.->|Draait op| OpenClaw
    
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
%%{{init: {{'theme': 'dark', 'themeVariables': {{'primaryColor': '#d6b35e', 'primaryTextColor': '#fff', 'primaryBorderColor': '#d6b35e', 'lineColor': '#36c9ff', 'secondaryColor': '#1c1c20', 'tertiaryColor': '#161618'}}}}}}%%
flowchart LR
    A[📥 Input] -->|✓| B[✓ Check]
    B -->|⚙️| C[⚙️ Verwerking]
    C -->|💾| D[💾 Geheugen]
    C -->|🔍| E[🔍 Vectoren]
    D -->|📝| F[📝 Antwoord]
    E -->|📝| F
    F -->|📤| G[📤 Output]
    
    style A fill:#36c9ff,stroke:#36c9ff,color:#000
    style B fill:#ff9f43,stroke:#ff9f43,color:#000
    style C fill:#d6b35e,stroke:#d6b35e,color:#000
    style D fill:#9b7cff,stroke:#9b7cff,color:#fff
    style E fill:#9b7cff,stroke:#9b7cff,color:#fff
    style F fill:#3fe3b5,stroke:#3fe3b5,color:#000
    style G fill:#ff4d6d,stroke:#ff4d6d,color:#fff
                    </pre>
                </div>
            </div>
            
            <div class="diagram-card">
                <h3><span class="diagram-icon">🔗</span> Bouw Volgorde</h3>
                <div class="mermaid-container">
                    <pre class="mermaid">
%%{{init: {{'theme': 'dark', 'themeVariables': {{'primaryColor': '#d6b35e', 'primaryTextColor': '#fff', 'primaryBorderColor': '#d6b35e', 'lineColor': '#95a7c2', 'secondaryColor': '#1c1c20', 'tertiaryColor': '#161618'}}}}}}%%
graph LR
    A[1️⃣ Platform] -->|✓| B[2️⃣ Security]
    B -->|✓| C[3️⃣ Models]
    C -->|✓| D[4️⃣ Agents]
    D -->|✓| E[5️⃣ Data]
    E -->|✓| F[6️⃣ Monitor]
    F -->|✓| G[7️⃣ Control]
    G -->|✓| H[8️⃣ Mission]
    
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

    <!-- CHAPTER MINI BLOCKS -->
    <section class="chapters-mini-section">
        <div class="section-header">
            <h2>📚 Chapter Progress</h2>
            <p>Klik op een chapter voor details</p>
        </div>
        <div class="chapters-mini-grid">
            {chapter_minis}
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
    print("Building index.html v4...")
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
    
    print("✅ SUCCESS! index.html v4 rebuilt")
    print("Changes:")
    print("  - Appearance dropdown sluit na keuze")
    print("  - Blocks direct zichtbaar in sidebar")
    print("  - Grote hero met duidelijke uitleg")
    print("  - Arc AI Angels sectie met OpenClaw focus")
    print("  - Levendige gekleurde diagrammen")
    print("  - Chapter mini blocks met progress")
    print("  - Grotere lettertypes overal")

if __name__ == "__main__":
    main()
