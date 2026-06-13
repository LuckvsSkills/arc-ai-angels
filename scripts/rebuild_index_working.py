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

/* CUSTOM THEME PICKER - WERKT 100% */
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

/* LIGHT MODE */
[data-theme="light"] .theme-toggle { background: #ffffff; color: #132033; border-color: rgba(0,0,0,0.2); }
[data-theme="light"] .theme-menu { background: #ffffff; border-color: rgba(0,0,0,0.1); }
[data-theme="light"] .theme-option { color: #132033; }
[data-theme="light"] .theme-option:hover { background: rgba(0,0,0,0.05); }
[data-theme="light"] .color-option { color: #132033; }
[data-theme="light"] .theme-section-title { color: #6d7f99; }

.sidebar-nav { flex: 1; overflow-y: auto; padding: 16px 12px; }
.nav-section { margin-bottom: 24px; }
.nav-section-title { font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; color: #6d7f99; padding: 0 8px; margin-bottom: 8px; }
.nav-link { display: flex; align-items: center; gap: 12px; padding: 10px 12px; margin: 2px 0; border-radius: 8px; color: #c3d0e3; text-decoration: none; font-size: 14px; font-weight: 500; transition: all 0.2s; }
.nav-link:hover { background: rgba(255,255,255,0.04); color: #eef4fb; }
.nav-link.active { background: rgba(214,179,94,0.12); color: var(--accent); }

/* HOVER EFFECTS 30% LICHTER */
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

.block-list { list-style: none; margin: 0; padding: 0 12px 12px 36px; overflow: hidden; transition: all 0.3s; }
.block-list.collapsed { max-height: 0; opacity: 0; padding-bottom: 0; }
.block-list:not(.collapsed) { max-height: 500px; opacity: 1; }
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
.view-all a { color: var(--accent); font-weight: 600; font-size: 12px; }

.sidebar-footer { padding: 16px; border-top: 1px solid rgba(255,255,255,0.06); background: rgba(0,0,0,0.2); }
.progress-mini-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; }
.progress-mini-label { font-size: 11px; color: #6d7f99; text-transform: uppercase; letter-spacing: 0.5px; }
.progress-mini-bar { height: 4px; background: rgba(255,255,255,0.1); border-radius: 2px; overflow: hidden; }
.progress-mini-fill { height: 100%; background: linear-gradient(90deg, var(--accent), var(--accent2)); border-radius: 2px; }
.progress-mini-text { font-size: 12px; color: var(--accent); font-weight: 600; }

.main-content { padding: 40px 48px; max-width: 1400px; }
.hero { margin-bottom: 48px; padding: 32px; background: var(--panel); border: 1px solid var(--line); border-radius: 16px; }
.hero-badge { display: inline-flex; align-items: center; gap: 8px; padding: 6px 12px; background: rgba(214,179,94,0.1); border: 1px solid rgba(214,179,94,0.2); border-radius: 20px; font-size: 12px; color: var(--accent); margin-bottom: 16px; }
.badge-dot { width: 6px; height: 6px; background: var(--accent); border-radius: 50%; animation: pulse 2s infinite; }
@keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.5; } }
.hero-title { font-size: 42px; font-weight: 800; margin: 0 0 16px 0; letter-spacing: -0.5px; line-height: 1.2; }
.gradient-text { background: linear-gradient(135deg, var(--accent) 0%, var(--accent2) 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }
.hero-subtitle { font-size: 18px; color: var(--muted); margin: 0 0 32px 0; max-width: 600px; line-height: 1.5; }

.intro-section { margin-bottom: 48px; padding: 24px; background: var(--panel); border: 1px solid var(--line); border-radius: 12px; border-left: 4px solid var(--accent); }
.intro-section h2 { margin: 0 0 12px 0; font-size: 20px; color: var(--text); }
.intro-section p { margin: 0 0 16px 0; color: var(--muted); line-height: 1.6; }
.intro-section ul { margin: 0; padding-left: 20px; color: var(--muted2); }
.intro-section li { margin: 8px 0; }

.diagrams-section { margin-bottom: 48px; }
.section-header { margin-bottom: 24px; }
.section-header h2 { font-size: 24px; font-weight: 700; margin: 0 0 8px 0; }
.section-header p { color: var(--muted); margin: 0; }
.diagrams-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(400px, 1fr)); gap: 24px; }
.diagram-card { background: var(--panel); border: 1px solid var(--line); border-radius: 12px; padding: 24px; }
.diagram-card h3 { margin: 0 0 16px 0; font-size: 16px; color: var(--text); display: flex; align-items: center; gap: 8px; }
.diagram-icon { width: 32px; height: 32px; background: rgba(214,179,94,0.1); border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 16px; }
.mermaid-container { background: var(--bg0); border-radius: 8px; padding: 16px; overflow-x: auto; }

.chapters-section { margin-bottom: 48px; }
.chapters-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 20px; }
.chapter-card { background: var(--panel); border: 1px solid var(--line); border-radius: 16px; padding: 24px; text-decoration: none; transition: all 0.2s; display: block; }
.chapter-card:hover { transform: translateY(-2px); border-color: var(--chapter-color); box-shadow: 0 8px 24px rgba(0,0,0,0.2); }
.chapter-card-header { display: flex; align-items: center; gap: 16px; margin-bottom: 20px; }
.chapter-card-icon { width: 48px; height: 48px; border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 24px; }
.chapter-card-meta h3 { margin: 0 0 4px 0; font-size: 18px; color: var(--text); }
.chapter-card-status { font-size: 13px; padding: 2px 8px; border-radius: 4px; font-weight: 500; }
.chapter-card-status.complete { background: rgba(63,227,181,0.15); color: #3fe3b5; }
.chapter-card-status.in-progress { background: rgba(255,159,67,0.15); color: #ff9f43; }
.chapter-card-status.planned { background: rgba(149,167,194,0.15); color: #95a7c2; }
.chapter-card-progress { display: flex; align-items: center; gap: 12px; }
.progress-bar-bg { flex: 1; height: 6px; background: rgba(255,255,255,0.1); border-radius: 3px; overflow: hidden; }
.progress-bar-fill { height: 100%; border-radius: 3px; transition: width 0.3s; }
.progress-text { font-size: 13px; color: var(--muted); font-weight: 600; min-width: 40px; text-align: right; }
"""

def generate_sidebar(progress):
    chapter_items = ""
    for chapter in progress.get("chapters", []):
        chapter_id = chapter["id"]
        chapter_title = chapter.get("title", chapter_id)
        color = get_color_for_chapter(chapter_id)
        total_blocks = chapter.get("total_blocks", 0)
        done_blocks = chapter.get("done_blocks", 0)
        
        chapter_items += f"""
        <div class=\"nav-item\" data-chapter=\"{chapter_id}\" data-color=\"{color}\" onclick=\"toggleChapter(this)\">
            <div class=\"nav-chapter-header\">
                <span class=\"chapter-indicator\" style=\"background:{color}\"></span>
                <span class=\"chapter-title-text\">{chapter_title}</span>
                <span class=\"chapter-stats\">{done_blocks}/{total_blocks}</span>
                <svg class=\"chevron\" width=\"12\" height=\"12\" viewBox=\"0 0 12 12\">
                    <path d=\"M3 4.5L6 7.5L9 4.5\" stroke=\"currentColor\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"/>
                </svg>
            </div>
            <ul class=\"block-list collapsed\">
                <li class=\"view-all\"><a href=\"chapters/{chapter_id}.html\" onclick=\"event.stopPropagation()\">→ View Chapter Overview</a></li>
"""
        
        for cluster in chapter.get("clusters", []):
            for block in cluster.get("blocks", []):
                block_id = block["id"]
                block_title = block.get("title", block_id)
                match = re.match(r'[a-z]+(\\d+)', block_id, re.IGNORECASE)
                if match:
                    num = int(match.group(1))
                    safe_title = re.sub(r'[^\\w\\s-]', '', block_title).replace(' ', '-').lower()[:40]
                    block_file = f"block-{num:02d}-{safe_title}.html"
                    chapter_items += f'<li data-chapter=\"{chapter_id}\" data-color=\"{color}\"><a href=\"chapters/blocks/{chapter_id}/{block_file}\" onclick=\"event.stopPropagation()\">Block {num:02d}: {block_title}</a></li>\n'
        
        chapter_items += """
            </ul>
        </div>
"""
    
    overall = progress.get("overall", {})
    overall_pct = overall.get("progress_percent", 54)
    
    return f"""
<nav class=\"sidebar\">
    <div class=\"sidebar-brand\">
        <div class=\"brand-icon\">◈</div>
        <div class=\"brand-text\">
            <div class=\"brand-title\">Arc Control Center</div>
            <div class=\"brand-subtitle\">Strategic Architecture Hub</div>
        </div>
    </div>
    
    <!-- CUSTOM THEME PICKER -->
    <div class=\"theme-picker\">
        <div class=\"theme-picker-label\">Appearance</div>
        <button class=\"theme-toggle\" onclick=\"toggleThemeMenu()\">
            <span id=\"currentThemeLabel\">🌙 Dark Mode</span>
            <span>▼</span>
        </button>
        <div class=\"theme-menu\" id=\"themeMenu\">
            <div class=\"theme-section\">
                <div class=\"theme-section-title\">Mode</div>
                <button class=\"theme-option active\" id=\"opt-dark\" onclick=\"setTheme('dark')\">🌙 Dark Mode</button>
                <button class=\"theme-option\" id=\"opt-light\" onclick=\"setTheme('light')\">☀️ Light Mode</button>
            </div>
            <div class=\"theme-section\">
                <div class=\"theme-section-title\">Accent Color</div>
                <button class=\"color-option active\" id=\"opt-gold\" onclick=\"setPreset('obsidian_gold')\"><span class=\"color-dot\" style=\"background:#d6b35e\"></span> Gold</button>
                <button class=\"color-option\" id=\"opt-cyan\" onclick=\"setPreset('graphite_cyan')\"><span class=\"color-dot\" style=\"background:#36c9ff\"></span> Cyan</button>
                <button class=\"color-option\" id=\"opt-purple\" onclick=\"setPreset('midnight_purple')\"><span class=\"color-dot\" style=\"background:#9b7cff\"></span> Purple</button>
                <button class=\"color-option\" id=\"opt-teal\" onclick=\"setPreset('slate_teal')\"><span class=\"color-dot\" style=\"background:#2fd3c5\"></span> Teal</button>
            </div>
        </div>
    </div>

    <div class=\"sidebar-nav\">
        <div class=\"nav-section\">
            <div class=\"nav-section-title\">Navigation</div>
            <a href=\"#home\" class=\"nav-link active\">
                <svg width=\"16\" height=\"16\" viewBox=\"0 0 16 16\" fill=\"none\">
                    <path d=\"M2 6.5L8 2L14 6.5V13.5C14 13.7761 13.7761 14 13.5 14H2.5C2.22386 14 2 13.7761 2 13.5V6.5Z\" stroke=\"currentColor\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"/>
                    <path d=\"M6 14V10H10V14\" stroke=\"currentColor\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"/>
                </svg>
                Dashboard
            </a>
            <a href=\"prompts.html\" class=\"nav-link\">
                <svg width=\"16\" height=\"16\" viewBox=\"0 0 16 16\" fill=\"none\">
                    <path d=\"M8 2L2 7L8 12L14 7L8 2Z\" stroke=\"currentColor\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"/>
                </svg>
                Prompts
            </a>
        </div>
        
        <div class=\"nav-section\">
            <div class=\"nav-section-title\">Chapters</div>
            {chapter_items}
        </div>
    </div>

    <div class=\"sidebar-footer\">
        <div class=\"progress-mini\">
            <div class=\"progress-mini-header\">
                <span class=\"progress-mini-label\">Overall Progress</span>
                <span class=\"progress-mini-text\" id=\"sidebarProgressText\">{overall_pct}%</span>
            </div>
            <div class=\"progress-mini-bar\">
                <div class=\"progress-mini-fill\" id=\"sidebarProgressBar\" style=\"width: {overall_pct}%\"></div>
            </div>
        </div>
    </div>
</nav>

<script>
function toggleThemeMenu() {{
    document.getElementById('themeMenu').classList.toggle('open');
}}

function setTheme(theme) {{
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
    document.getElementById('opt-dark').classList.toggle('active', theme === 'dark');
    document.getElementById('opt-light').classList.toggle('active', theme === 'light');
    document.getElementById('currentThemeLabel').textContent = theme === 'dark' ? '🌙 Dark Mode' : '☀️ Light Mode';
}}

function setPreset(preset) {{
    document.documentElement.setAttribute('data-preset', preset);
    localStorage.setItem('preset', preset);
    document.querySelectorAll('.color-option').forEach(btn => btn.classList.remove('active'));
    document.getElementById('opt-' + preset.replace('obsidian_', '').replace('graphite_', '').replace('midnight_', '').replace('slate_', '')).classList.add('active');
}}

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

document.addEventListener('DOMContentLoaded', function() {{
    const savedTheme = localStorage.getItem('theme') || 'dark';
    const savedPreset = localStorage.getItem('preset') || 'obsidian_gold';
    document.documentElement.setAttribute('data-theme', savedTheme);
    document.documentElement.setAttribute('data-preset', savedPreset);
    setTheme(savedTheme);
    setPreset(savedPreset);
    
    const firstChapter = document.querySelector('.nav-item');
    if (firstChapter) {{
        toggleChapter(firstChapter);
    }}
}});
</script>
"""

def generate_main_content(progress):
    chapter_cards = ""
    for chapter in progress.get("chapters", []):
        chapter_id = chapter["id"]
        chapter_title = chapter.get("title", chapter_id)
        color = get_color_for_chapter(chapter_id)
        pct = chapter.get("progress_percent", 0)
        status = chapter.get("status", "planned")
        
        if pct == 100 or status in ["finished", "completed"]:
            status_class = "complete"; status_text = "Complete"
        elif pct > 0 or status == "started":
            status_class = "in-progress"; status_text = "In Progress"
        else:
            status_class = "planned"; status_text = "Planned"
        
        chapter_cards += f"""
        <a href=\"chapters/{chapter_id}.html\" class=\"chapter-card\" style=\"--chapter-color: {color}\">
            <div class=\"chapter-card-header\">
                <div class=\"chapter-card-icon\" style=\"background: {color}15; color: {color}\">◈</div>
                <div class=\"chapter-card-meta\">
                    <h3>{chapter_title}</h3>
                    <span class=\"chapter-card-status {status_class}\">{status_text}</span>
                </div>
            </div>
            <div class=\"chapter-card-progress\">
                <div class=\"progress-bar-bg\">
                    <div class=\"progress-bar-fill\" style=\"width: {pct}%; background: {color}\"></div>
                </div>
                <span class=\"progress-text\">{pct}%</span>
            </div>
        </a>
"""
    
    return f"""
<main class=\"main-content\">
    <section class=\"hero\">
        <div class=\"hero-badge\">
            <span class=\"badge-dot\"></span>
            Strategic Architecture Hub
        </div>
        <h1 class=\"hero-title\">The Arc<br><span class=\"gradient-text\">Control Center</span></h1>
        <p class=\"hero-subtitle\">Architecture, Governance & Deployment Hub for Enterprise AI Systems</p>
    </section>

    <section class=\"intro-section\">
        <h2>🚀 Welcome to The Arc</h2>
        <p>
            The Arc is een strategisch architectuurplatform voor het bouwen, beheren en schalen van 
            enterprise AI systemen. Het biedt een gestructureerde aanpak voor AI agent orchestration, 
            security hardening, en operationele controle.
        </p>
        <p><strong>Navigatie:</strong></p>
        <ul>
            <li><strong>Dashboard:</strong> Overzicht van alle chapters en voortgang</li>
            <li><strong>Chapters:</strong> Klik op een hoofdstuk in de sidebar om de blocks te zien</li>
            <li><strong>Prompts:</strong> Bibliotheek met AI prompts voor development</li>
            <li><strong>Appearance:</strong> Pas thema en accentkleur aan in de sidebar</li>
        </ul>
    </section>

    <section class=\"diagrams-section\">
        <div class=\"section-header\">
            <h2>📊 Architecture Diagrams</h2>
            <p>Visualisatie van de AI agent flow en systeemarchitectuur</p>
        </div>
        <div class=\"diagrams-grid\">
            <div class=\"diagram-card\">
                <h3><span class=\"diagram-icon\">🔄</span> Agent Flow</h3>
                <div class=\"mermaid-container\">
                    <pre class=\"mermaid\">
flowchart TD
    A[User Request] --> B[Nova Gateway]
    B --> C{{Flux Orchestrator}}
    C --> D[Omni Intelligence]
    C --> E[Sentinel Team]
    C --> F[Execution Workers]
    D --> G[Response]
    E --> G
    F --> G
    G --> H[User]
                    </pre>
                </div>
            </div>
            
            <div class=\"diagram-card\">
                <h3><span class=\"diagram-icon\">🏗️</span> System Architecture</h3>
                <div class=\"mermaid-container\">
                    <pre class=\"mermaid\">
graph TB
    subgraph \"Control Layer\"
        Nova[Nova Gateway]
        Flux[Flux Orchestrator]
    end
    
    subgraph \"Intelligence Layer\"  
        Omni[Omni Intelligence]
        Sentinel[Sentinel Team]
    end
    
    subgraph \"Execution Layer\"
        Workers[Execution Workers]
        OpenClaw[OpenClaw Runtime]
    end
    
    Nova --> Flux
    Flux --> Omni
    Flux --> Sentinel
    Flux --> Workers
    Workers --> OpenClaw
                    </pre>
                </div>
            </div>
            
            <div class=\"diagram-card\">
                <h3><span class=\"diagram-icon\">📡</span> Data Flow</h3>
                <div class=\"mermaid-container\">
                    <pre class=\"mermaid\">
flowchart LR
    A[Input] --> B[Validation]
    B --> C[Processing]
    C --> D[Memory Store]
    C --> E[Vector DB]
    D --> F[Response Gen]
    E --> F
    F --> G[Output]
                    </pre>
                </div>
            </div>
            
            <div class=\"diagram-card\">
                <h3><span class=\"diagram-icon\">🔗</span> Block Dependencies</h3>
                <div class=\"mermaid-container\">
                    <pre class=\"mermaid\">
graph TD
    A[Platform Runtime] --> B[Security]
    B --> C[Model Runtime]
    C --> D[Agent Logic]
    D --> E[Data Memory]
    E --> F[Observability]
    F --> G[Control Center]
    G --> H[Mission Control]
                    </pre>
                </div>
            </div>
        </div>
    </section>

    <section class=\"chapters-section\">
        <div class=\"section-header\">
            <h2>📚 Chapters</h2>
            <p>Explore the architecture through structured learning paths</p>
        </div>
        <div class=\"chapters-grid\">
            {chapter_cards}
        </div>
    </section>
</main>

<script src=\"https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js\"></script>
<script>
    mermaid.initialize({{
        startOnLoad: true,
        theme: 'dark',
        themeVariables: {{
            primaryColor: '#d6b35e',
            primaryTextColor: '#eef4fb',
            primaryBorderColor: '#d6b35e',
            lineColor: '#95a7c2',
            secondaryColor: '#161618',
            tertiaryColor: '#232329'
        }}
    }});
</script>
"""

def main():
    print("Building index.html...")
    progress = load_progress()
    sidebar = generate_sidebar(progress)
    main_content = generate_main_content(progress)
    
    html = f"""<!DOCTYPE html>
<html lang=\"en\" data-theme=\"dark\" data-preset=\"obsidian_gold\">
<head>
<meta charset=\"utf-8\">
<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
<title>The Arc Strategic Control Center</title>
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
    
    print("✅ SUCCESS! index.html rebuilt")
    print("Features:")
    print("  - Custom theme picker (click 'Appearance')")
    print("  - Hover effects on chapters (30% lighter)")
    print("  - Intro section with navigation guide")
    print("  - 4 Mermaid diagrams")
    print("  - Overall progress: 54%")

if __name__ == "__main__":
    main()
