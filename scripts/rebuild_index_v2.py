#!/usr/bin/env python3
"""
Arc Control Center - Professionele Index Generator v2
- Custom theme dropdown (niet native select)
- Quick Read verwijderd
- Betere layout structuur
"""

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

def get_status_info(chapter):
    """Bepaal status text en class op basis van progress"""
    pct = chapter.get("progress_percent", 0)
    status = chapter.get("status", "")
    
    if pct == 100 or status in ["finished", "completed"]:
        return ("Complete", "complete")
    elif pct > 0 or status == "started":
        return ("In Progress", "in-progress")
    else:
        return ("Planned", "planned")

def generate_sidebar(progress):
    """Sidebar met custom theme dropdown"""
    
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
                # Extract number from b01, m02, etc.
                match = re.match(r'[a-z]+(\d+)', block_id, re.IGNORECASE)
                if match:
                    num = int(match.group(1))
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
        <div class="brand-text">
            <div class="brand-title">Arc Control Center</div>
            <div class="brand-subtitle">Strategic Architecture Hub</div>
        </div>
    </div>
    
    <!-- CUSTOM THEME DROPDOWN -->
    <div class="theme-selector">
        <button class="theme-dropdown-btn" onclick="toggleThemeDropdown()">
            <span class="theme-icon">🎨</span>
            <span class="theme-label-text">Appearance</span>
            <svg class="theme-chevron" width="12" height="12" viewBox="0 0 12 12">
                <path d="M3 4.5L6 7.5L9 4.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
        </button>
        <div class="theme-dropdown-menu" id="themeDropdown">
            <div class="theme-section">
                <div class="theme-section-title">Mode</div>
                <button class="theme-option" onclick="setTheme('dark')">
                    <span class="option-icon">🌙</span>
                    <span>Dark Mode</span>
                    <span class="checkmark" id="check-dark">✓</span>
                </button>
                <button class="theme-option" onclick="setTheme('light')">
                    <span class="option-icon">☀️</span>
                    <span>Light Mode</span>
                    <span class="checkmark" id="check-light">✓</span>
                </button>
            </div>
            <div class="theme-divider"></div>
            <div class="theme-section">
                <div class="theme-section-title">Accent Color</div>
                <button class="theme-option" onclick="setPreset('obsidian_gold')">
                    <span class="color-dot" style="background:#d6b35e"></span>
                    <span>Obsidian Gold</span>
                    <span class="checkmark" id="check-obsidian_gold">✓</span>
                </button>
                <button class="theme-option" onclick="setPreset('graphite_cyan')">
                    <span class="color-dot" style="background:#36c9ff"></span>
                    <span>Graphite Cyan</span>
                    <span class="checkmark" id="check-graphite_cyan">✓</span>
                </button>
                <button class="theme-option" onclick="setPreset('midnight_purple')">
                    <span class="color-dot" style="background:#9b7cff"></span>
                    <span>Midnight Purple</span>
                    <span class="checkmark" id="check-midnight_purple">✓</span>
                </button>
                <button class="theme-option" onclick="setPreset('slate_teal')">
                    <span class="color-dot" style="background:#2fd3c5"></span>
                    <span>Slate Teal</span>
                    <span class="checkmark" id="check-slate_teal">✓</span>
                </button>
            </div>
        </div>
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
            <div class="progress-mini-header">
                <span class="progress-mini-label">Overall Progress</span>
                <span class="progress-mini-text" id="sidebarProgressText">0%</span>
            </div>
            <div class="progress-mini-bar">
                <div class="progress-mini-fill" id="sidebarProgressBar" style="width: 0%"></div>
            </div>
        </div>
    </div>
</nav>

<script>
// Theme Dropdown
function toggleThemeDropdown() {{
    const dropdown = document.getElementById('themeDropdown');
    const chevron = document.querySelector('.theme-chevron');
    const isOpen = dropdown.classList.contains('open');
    
    if (!isOpen) {{
        dropdown.classList.add('open');
        chevron.style.transform = 'rotate(180deg)';
    }} else {{
        dropdown.classList.remove('open');
        chevron.style.transform = 'rotate(0deg)';
    }}
}}

document.addEventListener('click', function(e) {{
    if (!e.target.closest('.theme-selector')) {{
        document.getElementById('themeDropdown').classList.remove('open');
        document.querySelector('.theme-chevron').style.transform = 'rotate(0deg)';
    }}
}});

function setTheme(theme) {{
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
    updateCheckmarks();
}}

function setPreset(preset) {{
    document.documentElement.setAttribute('data-preset', preset);
    localStorage.setItem('preset', preset);
    updateCheckmarks();
}}

function updateCheckmarks() {{
    const currentTheme = localStorage.getItem('theme') || 'dark';
    const currentPreset = localStorage.getItem('preset') || 'obsidian_gold';
    document.querySelectorAll('.checkmark').forEach(c => c.style.opacity = '0');
    document.getElementById('check-' + currentTheme).style.opacity = '1';
    document.getElementById('check-' + currentPreset).style.opacity = '1';
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
    updateCheckmarks();
    
    const firstChapter = document.querySelector('.nav-item');
    if (firstChapter) {{
        toggleChapter(firstChapter);
    }}
    
    // Sync sidebar progress
    const heroProgress = document.querySelector('.hero-progress-value');
    if (heroProgress) {{
        const pct = heroProgress.textContent;
        document.getElementById('sidebarProgressText').textContent = pct;
        document.getElementById('sidebarProgressBar').style.width = pct;
    }}
}});
</script>
'''
