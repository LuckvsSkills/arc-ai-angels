#!/usr/bin/env python3
"""
Verbeter index.html sidebar - uitklapbaar, mooi, professioneel
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

def generate_improved_sidebar(progress):
    """Genereer verbeterde sidebar met uitklapbare chapters"""
    
    # Bouw chapter items
    chapter_items = ""
    for i, chapter in enumerate(progress.get("chapters", [])):
        chapter_id = chapter["id"]
        chapter_title = chapter.get("title", chapter_id)
        color = get_color_for_chapter(chapter_id)
        
        # Tel blocks
        total_blocks = chapter.get("total_blocks", 0)
        done_blocks = chapter.get("done_blocks", 0)
        
        # Genereer block list
        block_items = ""
        for cluster in chapter.get("clusters", []):
            for block in cluster.get("blocks", []):
                block_id = block["id"]
                block_title = block.get("title", block_id)
                match = re.match(r'([a-z])(\d+)', block_id)
                if match:
                    num = int(match.group(2))
                    safe_title = re.sub(r'[^\w\s-]', '', block_title).replace(' ', '-').lower()[:40]
                    block_file = f"block-{num:02d}-{safe_title}.html"
                    block_items += f'<li><a href="chapters/blocks/{chapter_id}/{block_file}" onclick="event.stopPropagation()">Block {num:02d}: {block_title}</a></li>\n'
        
        chapter_items += f'''
        <div class="nav-item" onclick="toggleChapter(this)">
            <div class="nav-chapter-header">
                <span class="chapter-indicator" style="background:{color}"></span>
                <span class="chapter-title-text">{chapter_title}</span>
                <span class="chapter-stats">{done_blocks}/{total_blocks}</span>
                <svg class="chevron" width="12" height="12" viewBox="0 0 12 12" fill="none">
                    <path d="M3 4.5L6 7.5L9 4.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
            </div>
            <ul class="block-list collapsed">
                <li class="view-all"><a href="chapters/{chapter_id}.html" onclick="event.stopPropagation()">→ View Chapter Overview</a></li>
                {block_items}
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
    
    <div class="sidebar-nav">
        <div class="nav-section">
            <div class="nav-section-title">Navigation</div>
            <a href="#home" class="nav-link active" onclick="setActive(this)">
                <svg width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M2 6.5L8 2L14 6.5V13.5C14 13.7761 13.7761 14 13.5 14H2.5C2.22386 14 2 13.7761 2 13.5V6.5Z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/><path d="M6 14V10H10V14" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
                Dashboard
            </a>
            <a href="#roadmap" class="nav-link" onclick="setActive(this)">
                <svg width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M2 4H14M2 8H14M2 12H10" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>
                Roadmap
            </a>
            <a href="prompts.html" class="nav-link" onclick="setActive(this)">
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
    
    // Close all others
    document.querySelectorAll('.block-list').forEach(list => {{
        if (list !== blockList) {{
            list.classList.add('collapsed');
            list.closest('.nav-item').querySelector('.chevron').style.transform = 'rotate(0deg)';
        }}
    }});
    
    // Toggle current
    if (isCollapsed) {{
        blockList.classList.remove('collapsed');
        chevron.style.transform = 'rotate(180deg)';
    }} else {{
        blockList.classList.add('collapsed');
        chevron.style.transform = 'rotate(0deg)';
    }}
}}

function setActive(element) {{
    document.querySelectorAll('.nav-link').forEach(link => link.classList.remove('active'));
    element.classList.add('active');
}}

// Open first chapter by default
document.addEventListener('DOMContentLoaded', function() {{
    const firstChapter = document.querySelector('.nav-item');
    if (firstChapter) {{
        toggleChapter(firstChapter);
    }}
}});
</script>
'''

def generate_sidebar_css():
    """Professionele sidebar CSS"""
    return '''
/* ===== SIDEBAR ===== */
.sidebar {
    position: fixed;
    left: 0;
    top: 0;
    width: 300px;
    height: 100vh;
    background: linear-gradient(180deg, #0f0f11 0%, #161618 100%);
    border-right: 1px solid rgba(255,255,255,0.08);
    display: flex;
    flex-direction: column;
    z-index: 1000;
    font-family: Inter, system-ui, -apple-system, sans-serif;
}

/* Brand */
.sidebar-brand {
    padding: 24px 20px 20px;
    border-bottom: 1px solid rgba(255,255,255,0.06);
    display: flex;
    align-items: center;
    gap: 12px;
}

.brand-icon {
    width: 40px;
    height: 40px;
    background: linear-gradient(135deg, #d6b35e 0%, #f0d18a 100%);
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
    color: #0f0f11;
    font-weight: 700;
}

.brand-title {
    font-size: 16px;
    font-weight: 700;
    color: #eef4fb;
    letter-spacing: -0.3px;
}

.brand-subtitle {
    font-size: 12px;
    color: #95a7c2;
    margin-top: 2px;
}

/* Navigation */
.sidebar-nav {
    flex: 1;
    overflow-y: auto;
    padding: 16px 12px;
}

.nav-section {
    margin-bottom: 24px;
}

.nav-section-title {
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: #6d7f99;
    padding: 0 8px;
    margin-bottom: 8px;
}

.nav-link {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 10px 12px;
    margin: 2px 0;
    border-radius: 8px;
    color: #c3d0e3;
    text-decoration: none;
    font-size: 14px;
    font-weight: 500;
    transition: all 0.2s;
}

.nav-link:hover {
    background: rgba(255,255,255,0.04);
    color: #eef4fb;
}

.nav-link.active {
    background: rgba(214, 179, 94, 0.12);
    color: #d6b35e;
}

.nav-link svg {
    opacity: 0.7;
}

/* Chapter Items */
.nav-item {
    margin: 4px 0;
    border-radius: 8px;
    cursor: pointer;
    transition: background 0.2s;
}

.nav-item:hover {
    background: rgba(255,255,255,0.02);
}

.nav-chapter-header {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 12px;
    border-radius: 8px;
}

.chapter-indicator {
    width: 4px;
    height: 32px;
    border-radius: 2px;
    flex-shrink: 0;
}

.chapter-title-text {
    flex: 1;
    font-size: 14px;
    font-weight: 600;
    color: #eef4fb;
}

.chapter-stats {
    font-size: 12px;
    color: #6d7f99;
    font-weight: 500;
}

.chevron {
    color: #6d7f99;
    transition: transform 0.3s ease;
    flex-shrink: 0;
}

/* Block List */
.block-list {
    list-style: none;
    margin: 0;
    padding: 0 12px 12px 36px;
    overflow: hidden;
    transition: all 0.3s ease;
}

.block-list.collapsed {
    max-height: 0;
    opacity: 0;
    padding-bottom: 0;
}

.block-list:not(.collapsed) {
    max-height: 500px;
    opacity: 1;
}

.block-list li {
    margin: 2px 0;
}

.block-list a {
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
}

.block-list a:hover {
    background: rgba(255,255,255,0.04);
    color: #d6b35e;
}

.view-all a {
    color: #d6b35e;
    font-weight: 600;
    font-size: 12px;
}

/* Footer */
.sidebar-footer {
    padding: 16px;
    border-top: 1px solid rgba(255,255,255,0.06);
    background: rgba(0,0,0,0.2);
}

.progress-mini-label {
    font-size: 11px;
    color: #6d7f99;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 8px;
}

.progress-mini-bar {
    height: 4px;
    background: rgba(255,255,255,0.1);
    border-radius: 2px;
    overflow: hidden;
    margin-bottom: 6px;
}

.progress-mini-fill {
    height: 100%;
    background: linear-gradient(90deg, #d6b35e, #f0d18a);
    border-radius: 2px;
    transition: width 0.3s;
}

.progress-mini-text {
    font-size: 12px;
    color: #d6b35e;
    font-weight: 600;
}

/* Body shift */
body {
    margin-left: 300px !important;
}

/* Topbar aanpassing */
.topbar {
    margin-left: 300px !important;
    width: calc(100% - 300px) !important;
}

/* Scrollbar styling */
.sidebar-nav::-webkit-scrollbar {
    width: 6px;
}

.sidebar-nav::-webkit-scrollbar-track {
    background: transparent;
}

.sidebar-nav::-webkit-scrollbar-thumb {
    background: rgba(255,255,255,0.1);
    border-radius: 3px;
}
'''

def fix_index():
    """Vervang de oude sidebar met de nieuwe"""
    index_file = BASE / "index.html"
    
    with open(index_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Verwijder oude sidebar als die er is
    content = re.sub(r'<nav class="sidebar">.*?</nav>\s*', '', content, flags=re.DOTALL)
    content = re.sub(r'<style class="sidebar-fallback">.*?</style>\s*', '', content, flags=re.DOTALL)
    content = re.sub(r'<script>.*?(toggleChapter|setActive).*?</script>\s*', '', content, flags=re.DOTALL)
    
    # Verwijder oude sidebar CSS
    content = re.sub(r'/\* Sidebar.*?(?=</style>|/\* |</head>)', '', content, flags=re.DOTALL)
    
    progress = load_progress()
    new_sidebar = generate_improved_sidebar(progress)
    sidebar_css = generate_sidebar_css()
    
    # Voeg nieuwe CSS toe
    if '</head>' in content:
        content = content.replace('</head>', f'<style>{sidebar_css}</style>\n</head>')
    
    # Voeg nieuwe sidebar toe na body
    if '<body>' in content:
        content = content.replace('<body>', f'<body>\n{new_sidebar}')
    
    with open(index_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Index.html sidebar volledig vernieuwd!")
    print("   - Uitklapbare chapters")
    print("   - Progress indicator")
    print("   - Professionele styling")
    print("   - Icons in navigatie")

if __name__ == "__main__":
    fix_index()
