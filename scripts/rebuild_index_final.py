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

def generate_sidebar(progress):
    chapter_items = ""
    for chapter in progress.get("chapters", []):
        chapter_id = chapter["id"]
        chapter_title = chapter.get("title", chapter_id)
        color = get_color_for_chapter(chapter_id)
        total_blocks = chapter.get("total_blocks", 0)
        done_blocks = chapter.get("done_blocks", 0)
        
        chapter_items += f'''
        <div class="nav-item" data-chapter="{chapter_id}" data-color="{color}" onclick="toggleChapter(this)">
            <div class="nav-chapter-header">
                <span class="chapter-indicator" style="background:{color}"></span>
                <span class="chapter-title-text">{chapter_title}</span>
                <span class="chapter-stats">{done_blocks}/{total_blocks}</span>
                <svg class="chevron" width="12" height="12" viewBox="0 0 12 12">
                    <path d="M3 4.5L6 7.5L9 4.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
            </div>
            <ul class="block-list collapsed">
                <li class="view-all"><a href="chapters/{chapter_id}.html" onclick="event.stopPropagation()">→ View Chapter Overview</a></li>
'''
        
        for cluster in chapter.get("clusters", []):
            for block in cluster.get("blocks", []):
                block_id = block["id"]
                block_title = block.get("title", block_id)
                match = re.match(r'[a-z]+(\d+)', block_id, re.IGNORECASE)
                if match:
                    num = int(match.group(1))
                    safe_title = re.sub(r'[^\w\s-]', '', block_title).replace(' ', '-').lower()[:40]
                    block_file = f"block-{num:02d}-{safe_title}.html"
                    chapter_items += f'<li data-chapter="{chapter_id}" data-color="{color}"><a href="chapters/blocks/{chapter_id}/{block_file}" onclick="event.stopPropagation()">Block {num:02d}: {block_title}</a></li>\n'
        
        chapter_items += '''
            </ul>
        </div>
'''
    
    overall = progress.get("overall", {})
    overall_pct = overall.get("progress_percent", 54)
    
    return f'''
<nav class="sidebar">
    <div class="sidebar-brand">
        <div class="brand-icon">◈</div>
        <div class="brand-text">
            <div class="brand-title">Arc Control Center</div>
            <div class="brand-subtitle">Strategic Architecture Hub</div>
        </div>
    </div>
    
    <div class="theme-selector-native">
        <label for="themeSelect">Appearance</label>
        <select id="themeSelect" onchange="changeTheme(this.value)">
            <optgroup label="Mode">
                <option value="dark">Dark Mode</option>
                <option value="light">Light Mode</option>
            </optgroup>
            <optgroup label="Accent Color">
                <option value="obsidian_gold">Gold</option>
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
            <div class="nav-section-title">Chapters</div>
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
function changeTheme(value) {{
    if (value === 'dark' || value === 'light') {{
        document.documentElement.setAttribute('data-theme', value);
        localStorage.setItem('theme', value);
    }} else {{
        document.documentElement.setAttribute('data-preset', value);
        localStorage.setItem('preset', value);
    }}
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
    
    const select = document.getElementById('themeSelect');
    if (savedPreset !== 'obsidian_gold') {{
        select.value = savedPreset;
    }} else {{
        select.value = savedTheme;
    }}
    
    const firstChapter = document.querySelector('.nav-item');
    if (firstChapter) {{
        toggleChapter(firstChapter);
    }}
}});
</script>
'''
