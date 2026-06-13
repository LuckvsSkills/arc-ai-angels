#!/usr/bin/env python3
"""
Arc Strategic Control Center - Website Generator
WERKT MET: Chapter → Cluster → Block structuur
"""

import os
import json
import re
from pathlib import Path

# Configuration
BASE_PATH = Path.home() / "arc_strategic_control_center"
DATA_PATH = BASE_PATH / "data"
CONTENT_PATH = DATA_PATH / "block_content"
OUTPUT_PATH = BASE_PATH / "output"
CSS_PATH = OUTPUT_PATH / "css"

# Status mappings (jouw status → onze status)
STATUS_MAP = {
    "finished": "completed",
    "completed": "completed", 
    "started": "in-progress",
    "in-progress": "in-progress",
    "planned": "pending",
    "pending": "pending"
}

def load_progress_data():
    """Load progress.json with chapters/clusters/blocks structure"""
    progress_file = DATA_PATH / "progress.json"
    
    if not progress_file.exists():
        print(f"❌ Error: {progress_file} niet gevonden!")
        return None
    
    try:
        with open(progress_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Tel alle blocks in chapters/clusters
        total_blocks = 0
        for chapter in data.get('chapters', []):
            for cluster in chapter.get('clusters', []):
                total_blocks += len(cluster.get('blocks', []))
        
        print(f"✅ Progress data geladen: {len(data.get('chapters', []))} chapters, {total_blocks} blocks")
        return data
    except Exception as e:
        print(f"❌ Error bij laden progress.json: {e}")
        return None

def get_all_blocks(data):
    """Flatten chapters/clusters/blocks naar een platte lijst"""
    blocks = []
    block_counter = 1
    
    for chapter in data.get('chapters', []):
        chapter_id = chapter.get('id', '')
        chapter_title = chapter.get('title', '')
        chapter_color = chapter.get('color', 'cyan')
        
        for cluster in chapter.get('clusters', []):
            cluster_id = cluster.get('id', '')
            cluster_title = cluster.get('title', '')
            
            for block in cluster.get('blocks', []):
                block_id = block.get('id', f'b{block_counter:02d}')
                title = block.get('title', f'Block {block_counter}')
                status = block.get('status', 'planned')
                
                # Bereken progress op basis van status
                if status in ['finished', 'completed']:
                    progress = 100
                elif status == 'started':
                    progress = 50  # Geschat
                else:
                    progress = 0
                
                blocks.append({
                    'num_id': block_counter,  # 1, 2, 3...
                    'id': block_id,  # b01, m02, etc.
                    'title': title,
                    'status': STATUS_MAP.get(status, 'pending'),
                    'original_status': status,
                    'progress': progress,
                    'chapter': chapter_title,
                    'chapter_id': chapter_id,
                    'chapter_color': chapter_color,
                    'cluster': cluster_title
                })
                block_counter += 1
    
    return blocks

def load_markdown_content(block_id):
    """Load markdown content for a specific block"""
    # Probeer verschillende formaten: b01.md, block_1.md, etc.
    possible_files = [
        CONTENT_PATH / f"{block_id}.md",
        CONTENT_PATH / f"block_{block_id}.md",
        CONTENT_PATH / f"block_{int(block_id[1:]) if block_id[1:].isdigit() else block_id}.md"
    ]
    
    for md_file in possible_files:
        if md_file.exists():
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    return f.read()
            except Exception as e:
                print(f"⚠️  Warning: Kon {md_file} niet laden: {e}")
    
    return None

def extract_mermaid_diagrams(markdown_content):
    """Extract mermaid diagrams from markdown"""
    if not markdown_content:
        return []
    
    pattern = r'```mermaid\s*(.*?)```'
    matches = re.findall(pattern, markdown_content, re.DOTALL)
    return [m.strip() for m in matches]

def markdown_to_html(markdown_content):
    """Simple markdown to HTML conversion"""
    if not markdown_content:
        return "<p>Geen content beschikbaar / No content available</p>"
    
    html = markdown_content
    
    # Headers
    html = re.sub(r'^### (.*?)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.*?)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^# (.*?)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
    
    # Bold and italic
    html = re.sub(r'\*\*\*(.*?)\*\*\*', r'<strong><em>\1</em></strong>', html)
    html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html)
    html = re.sub(r'\*(.*?)\*', r'<em>\1</em>', html)
    
    # Code blocks (non-mermaid)
    html = re.sub(r'```(?!mermaid)(.*?)```', r'<pre><code>\1</code></pre>', html, flags=re.DOTALL)
    
    # Inline code
    html = re.sub(r'`(.*?)`', r'<code>\1</code>', html)
    
    # Remove mermaid blocks (handled separately)
    html = re.sub(r'```mermaid.*?```', '', html, flags=re.DOTALL)
    
    # Lists
    lines = html.split('\n')
    result = []
    in_list = False
    
    for line in lines:
        if line.strip().startswith('- ') or line.strip().startswith('* '):
            if not in_list:
                result.append('<ul>')
                in_list = True
            content = line.strip()[2:]
            result.append(f'<li>{content}</li>')
        else:
            if in_list:
                result.append('</ul>')
                in_list = False
            result.append(line)
    
    if in_list:
        result.append('</ul>')
    
    html = '\n'.join(result)
    
    # Paragraphs
    paragraphs = html.split('\n\n')
    new_paragraphs = []
    for p in paragraphs:
        p = p.strip()
        if p and not p.startswith('<') and not p.startswith('\n<'):
            p = f'<p>{p}</p>'
        new_paragraphs.append(p)
    html = '\n\n'.join(new_paragraphs)
    
    # Line breaks
    html = html.replace('\n', '<br>\n')
    
    return html

def generate_css():
    """Generate CSS with all themes"""
    
    css = """
:root {
    --primary: #00d4ff;
    --secondary: #0099cc;
    --accent: #0077aa;
    --glow: rgba(0, 212, 255, 0.3);
    --bg-primary: #0a0e17;
    --bg-secondary: #0d1320;
    --bg-card: #111827;
    --bg-sidebar: #080c14;
    --text-primary: #e0f7ff;
    --text-secondary: #8b9bb4;
    --text-muted: #5a6a7d;
    --border-color: rgba(0, 212, 255, 0.15);
    --success: #00ff88;
    --warning: #ffaa00;
    --danger: #ff3366;
    --info: #4488ff;
}

[data-theme="gold"] {
    --primary: #ffd700;
    --secondary: #ffaa00;
    --accent: #ff8c00;
    --glow: rgba(255, 215, 0, 0.3);
    --border-color: rgba(255, 215, 0, 0.15);
}

[data-theme="cyan"] {
    --primary: #00d4ff;
    --secondary: #0099cc;
    --accent: #0077aa;
    --glow: rgba(0, 212, 255, 0.3);
    --border-color: rgba(0, 212, 255, 0.15);
}

[data-theme="purple"] {
    --primary: #b829dd;
    --secondary: #8a1fb8;
    --accent: #6b1699;
    --glow: rgba(184, 41, 221, 0.3);
    --border-color: rgba(184, 41, 221, 0.15);
}

[data-theme="teal"] {
    --primary: #00ffaa;
    --secondary: #00cc88;
    --accent: #009966;
    --glow: rgba(0, 255, 170, 0.3);
    --border-color: rgba(0, 255, 170, 0.15);
}

[data-mode="light"] {
    --bg-primary: #f0f4f8;
    --bg-secondary: #e2e8f0;
    --bg-card: #ffffff;
    --bg-sidebar: #d1d5db;
    --text-primary: #1a202c;
    --text-secondary: #4a5568;
    --text-muted: #718096;
    --border-color: rgba(0, 0, 0, 0.1);
}

* { margin: 0; padding: 0; box-sizing: border-box; }

body {
    font-family: 'Segoe UI', system-ui, sans-serif;
    background: var(--bg-primary);
    color: var(--text-primary);
    line-height: 1.6;
    overflow-x: hidden;
    transition: background 0.3s, color 0.3s;
}

::-webkit-scrollbar { width: 8px; }
::-webkit-scrollbar-track { background: var(--bg-secondary); }
::-webkit-scrollbar-thumb { background: var(--secondary); border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: var(--primary); }

.app-container { display: flex; min-height: 100vh; }

.sidebar {
    width: 280px;
    background: var(--bg-sidebar);
    border-right: 1px solid var(--border-color);
    display: flex;
    flex-direction: column;
    position: fixed;
    height: 100vh;
    overflow-y: auto;
    z-index: 100;
    transition: transform 0.3s;
}

.sidebar-header {
    padding: 1.5rem;
    border-bottom: 1px solid var(--border-color);
    text-align: center;
}

.logo {
    font-size: 1.5rem;
    font-weight: bold;
    color: var(--primary);
    text-shadow: 0 0 10px var(--glow);
    margin-bottom: 0.5rem;
}

.logo-subtitle {
    font-size: 0.75rem;
    color: var(--text-secondary);
    text-transform: uppercase;
    letter-spacing: 1px;
}

.sidebar-nav { flex: 1; padding: 1rem 0; }

.nav-section { margin-bottom: 1.5rem; }

.nav-title {
    padding: 0 1.5rem;
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    color: var(--text-muted);
    margin-bottom: 0.5rem;
}

.nav-list { list-style: none; }

.nav-item a {
    display: flex;
    align-items: center;
    padding: 0.75rem 1.5rem;
    color: var(--text-secondary);
    text-decoration: none;
    transition: all 0.2s;
    border-left: 3px solid transparent;
}

.nav-item a:hover, .nav-item a.active {
    color: var(--primary);
    background: linear-gradient(90deg, var(--glow), transparent);
    border-left-color: var(--primary);
}

.nav-icon { width: 20px; margin-right: 0.75rem; text-align: center; }

.sidebar-footer {
    padding: 1rem 1.5rem;
    border-top: 1px solid var(--border-color);
    font-size: 0.75rem;
    color: var(--text-muted);
    text-align: center;
}

.main-content {
    flex: 1;
    margin-left: 280px;
    display: flex;
    flex-direction: column;
}

.topbar {
    height: 64px;
    background: var(--bg-secondary);
    border-bottom: 1px solid var(--border-color);
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 2rem;
    position: sticky;
    top: 0;
    z-index: 50;
}

.topbar-left { display: flex; align-items: center; gap: 1rem; }

.menu-toggle {
    display: none;
    background: none;
    border: none;
    color: var(--text-primary);
    font-size: 1.25rem;
    cursor: pointer;
}

.breadcrumb { color: var(--text-secondary); font-size: 0.9rem; }
.breadcrumb span { color: var(--primary); }

.topbar-right { display: flex; align-items: center; gap: 1rem; }

.theme-selector {
    display: flex;
    gap: 0.5rem;
    background: var(--bg-card);
    padding: 0.25rem;
    border-radius: 20px;
    border: 1px solid var(--border-color);
}

.theme-btn {
    width: 24px;
    height: 24px;
    border-radius: 50%;
    border: 2px solid transparent;
    cursor: pointer;
    transition: transform 0.2s;
}

.theme-btn:hover { transform: scale(1.1); }
.theme-btn.active { border-color: var(--text-primary); transform: scale(1.15); }

.theme-btn.gold { background: linear-gradient(135deg, #ffd700, #ffaa00); }
.theme-btn.cyan { background: linear-gradient(135deg, #00d4ff, #0099cc); }
.theme-btn.purple { background: linear-gradient(135deg, #b829dd, #8a1fb8); }
.theme-btn.teal { background: linear-gradient(135deg, #00ffaa, #00cc88); }

.mode-toggle {
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: 20px;
    padding: 0.25rem 0.75rem;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    color: var(--text-secondary);
    transition: all 0.2s;
}

.mode-toggle:hover { border-color: var(--primary); color: var(--primary); }

.content { flex: 1; padding: 2rem; max-width: 1400px; width: 100%; margin: 0 auto; }

.page-header { margin-bottom: 2rem; padding-bottom: 1rem; border-bottom: 1px solid var(--border-color); }

.page-title {
    font-size: 2rem;
    color: var(--primary);
    margin-bottom: 0.5rem;
    display: flex;
    align-items: center;
    gap: 0.75rem;
}

.page-subtitle { color: var(--text-secondary); font-size: 1rem; }

.card {
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
    transition: all 0.3s;
    position: relative;
    overflow: hidden;
}

.card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; width: 100%; height: 2px;
    background: linear-gradient(90deg, var(--primary), transparent);
    opacity: 0.5;
}

.card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 24px var(--glow);
    border-color: var(--primary);
}

.card-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; }

.card-title { font-size: 1.25rem; color: var(--primary); display: flex; align-items: center; gap: 0.5rem; }

.grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 1.5rem; }
.grid-2 { grid-template-columns: repeat(2, 1fr); }
.grid-3 { grid-template-columns: repeat(3, 1fr); }
.grid-4 { grid-template-columns: repeat(4, 1fr); }

@media (max-width: 1200px) { .grid-4 { grid-template-columns: repeat(3, 1fr); } }
@media (max-width: 900px) { .grid-3, .grid-4 { grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 600px) { .grid, .grid-2, .grid-3, .grid-4 { grid-template-columns: 1fr; } }

.status {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.35rem 0.75rem;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.status::before { content: ''; width: 8px; height: 8px; border-radius: 50%; animation: pulse 2s infinite; }

.status.completed { background: rgba(0, 255, 136, 0.15); color: var(--success); border: 1px solid var(--success); }
.status.completed::before { background: var(--success); }

.status.in-progress { background: rgba(255, 170, 0, 0.15); color: var(--warning); border: 1px solid var(--warning); }
.status.in-progress::before { background: var(--warning); }

.status.pending { background: rgba(255, 51, 102, 0.15); color: var(--danger); border: 1px solid var(--danger); }
.status.pending::before { background: var(--danger); }

.progress-container { margin-top: 1rem; }

.progress-bar {
    width: 100%;
    height: 8px;
    background: var(--bg-secondary);
    border-radius: 4px;
    overflow: hidden;
    position: relative;
}

.progress-fill {
    height: 100%;
    background: linear-gradient(90deg, var(--primary), var(--secondary));
    border-radius: 4px;
    transition: width 0.5s ease;
    position: relative;
    overflow: hidden;
}

.progress-fill::after {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
    animation: shimmer 2s infinite;
}

.progress-text { display: flex; justify-content: space-between; margin-top: 0.5rem; font-size: 0.85rem; color: var(--text-secondary); }

.mermaid-container {
    background: var(--bg-secondary);
    border: 1px solid var(--border-color);
    border-radius: 8px;
    padding: 1rem;
    margin: 1rem 0;
    overflow-x: auto;
}

.mermaid { text-align: center; }

@keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.5; } }
@keyframes shimmer { 0% { transform: translateX(-100%); } 100% { transform: translateX(100%); } }
@keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }

.fade-in { animation: fadeIn 0.5s ease forwards; }

@media (max-width: 768px) {
    .sidebar { transform: translateX(-100%); }
    .sidebar.open { transform: translateX(0); }
    .main-content { margin-left: 0; }
    .menu-toggle { display: block; }
    .topbar { padding: 0 1rem; }
    .content { padding: 1rem; }
}

.text-center { text-align: center; }
.mt-1 { margin-top: 0.5rem; }
.mt-2 { margin-top: 1rem; }
.mb-1 { margin-bottom: 0.5rem; }
.mb-2 { margin-bottom: 1rem; }
.mb-3 { margin-bottom: 1.5rem; }

.block-meta {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1rem;
    margin-bottom: 2rem;
}

.meta-item {
    background: var(--bg-secondary);
    padding: 1rem;
    border-radius: 8px;
    border: 1px solid var(--border-color);
}

.meta-label {
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: var(--text-muted);
    margin-bottom: 0.25rem;
}

.meta-value { font-size: 1.1rem; color: var(--primary); font-weight: 600; }

.content-body h1, .content-body h2, .content-body h3 { color: var(--primary); margin: 1.5rem 0 0.75rem 0; }
.content-body p { margin-bottom: 1rem; line-height: 1.8; }
.content-body ul { margin: 1rem 0; padding-left: 1.5rem; }
.content-body li { margin-bottom: 0.5rem; }
.content-body code { background: var(--bg-secondary); padding: 0.2rem 0.4rem; border-radius: 4px; font-family: monospace; font-size: 0.9em; color: var(--primary); }

.chapter-section { margin-bottom: 3rem; }

.chapter-header {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 1.5rem;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid var(--border-color);
}

.chapter-title { font-size: 1.5rem; color: var(--primary); font-weight: bold; }

.chapter-stats { display: flex; gap: 1rem; margin-left: auto; }

.chapter-stat {
    text-align: center;
    padding: 0.5rem 1rem;
    background: var(--bg-secondary);
    border-radius: 8px;
    border: 1px solid var(--border-color);
}

.chapter-stat-value { font-size: 1.25rem; font-weight: bold; color: var(--primary); }
.chapter-stat-label { font-size: 0.7rem; color: var(--text-muted); text-transform: uppercase; }
"""
    
    CSS_PATH.mkdir(parents=True, exist_ok=True)
    with open(CSS_PATH / "arc-scc.css", 'w', encoding='utf-8') as f:
        f.write(css)
    print("✅ CSS gegenereerd")

def generate_navigation(blocks, active_page="dashboard"):
    nav_items = [
        ("dashboard", "🏠", "Dashboard"),
        ("chapters", "📚", "Hoofdstukken"),
        ("timeline", "📅", "Tijdlijn"),
        ("about", "ℹ️", "Over"),
    ]
    
    # Group blocks by chapter
    chapters = {}
    for block in blocks:
        chapter = block['chapter']
        if chapter not in chapters:
            chapters[chapter] = []
        chapters[chapter].append(block)
    
    chapter_nav = ""
    for chapter_name, chapter_blocks in chapters.items():
        chapter_nav += '<div class="nav-section">' + "\n"
        chapter_nav += f'<div class="nav-title">{chapter_name[:20]}</div>' + "\n"
        chapter_nav += '<ul class="nav-list">' + "\n"
        for block in chapter_blocks[:5]:  # Max 5 per chapter in sidebar
            active = "active" if active_page == f"block_{block['num_id']}" else ""
            block_num = block['num_id']
            block_id = block['id']
            chapter_nav += f'<li class="nav-item"><a href="block_{block_num}.html" class="{active}"><span class="nav-icon">🔷</span> {block_id}</a></li>' + "\n"
        if len(chapter_blocks) > 5:
            chapter_nav += f'<li class="nav-item" style="color: var(--text-muted); padding-left: 1.5rem; font-size: 0.8rem;">+ {len(chapter_blocks) - 5} more...</li>' + "\n"
        chapter_nav += '</ul>' + "\n</div>\n"
    
    main_nav = ""
    for page, icon, title in nav_items:
        active = "active" if active_page == page else ""
        main_nav += f'<li class="nav-item"><a href="{page}.html" class="{active}"><span class="nav-icon">{icon}</span> {title}</a></li>' + "\n"
    
    return f"""
<aside class="sidebar" id="sidebar">
    <div class="sidebar-header">
        <div class="logo">⚡ Arc SCC</div>
        <div class="logo-subtitle">Strategic Control Center</div>
    </div>
    <nav class="sidebar-nav">
        <div class="nav-section">
            <div class="nav-title">Hoofdmenu</div>
            <ul class="nav-list">{main_nav}</ul>
        </div>
        {chapter_nav}
    </nav>
    <div class="sidebar-footer">
        <div>Arc SCC v1.0</div>
        <div style="margin-top: 0.25rem;">54 Blocks</div>
    </div>
</aside>
"""

def generate_topbar(page_title, theme="cyan", mode="dark"):
    return f"""
<header class="topbar">
    <div class="topbar-left">
        <button class="menu-toggle" onclick="toggleSidebar()">☰</button>
        <div class="breadcrumb">Arc SCC / <span>{page_title}</span></div>
    </div>
    <div class="topbar-right">
        <div class="theme-selector">
            <button class="theme-btn gold {'active' if theme == 'gold' else ''}" onclick="setTheme('gold')" title="Gold"></button>
            <button class="theme-btn cyan {'active' if theme == 'cyan' else ''}" onclick="setTheme('cyan')" title="Cyan"></button>
            <button class="theme-btn purple {'active' if theme == 'purple' else ''}" onclick="setTheme('purple')" title="Purple"></button>
            <button class="theme-btn teal {'active' if theme == 'teal' else ''}" onclick="setTheme('teal')" title="Teal"></button>
        </div>
        <button class="mode-toggle" onclick="toggleMode()">
            <span id="mode-icon">{'☀️' if mode == 'dark' else '🌙'}</span>
            <span id="mode-text">{'Light' if mode == 'dark' else 'Dark'}</span>
        </button>
    </div>
</header>
"""

def generate_js():
    js = """
function setTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('arc-theme', theme);
    document.querySelectorAll('.theme-btn').forEach(btn => btn.classList.remove('active'));
    document.querySelector(`.theme-btn.${theme}`).classList.add('active');
}

function toggleMode() {
    const current = document.documentElement.getAttribute('data-mode') || 'dark';
    const newMode = current === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-mode', newMode);
    localStorage.setItem('arc-mode', newMode);
    const icon = document.getElementById('mode-icon');
    const text = document.getElementById('mode-text');
    if (icon && text) {
        icon.textContent = newMode === 'dark' ? '☀️' : '🌙';
        text.textContent = newMode === 'dark' ? 'Light' : 'Dark';
    }
}

function toggleSidebar() {
    document.getElementById('sidebar').classList.toggle('open');
}

document.addEventListener('DOMContentLoaded', function() {
    const savedTheme = localStorage.getItem('arc-theme') || 'cyan';
    setTheme(savedTheme);
    const savedMode = localStorage.getItem('arc-mode') || 'dark';
    document.documentElement.setAttribute('data-mode', savedMode);
    const icon = document.getElementById('mode-icon');
    const text = document.getElementById('mode-text');
    if (icon && text) {
        icon.textContent = savedMode === 'dark' ? '☀️' : '🌙';
        text.textContent = savedMode === 'dark' ? 'Light' : 'Dark';
    }
    if (typeof mermaid !== 'undefined') {
        mermaid.initialize({ startOnLoad: true, theme: savedMode === 'dark' ? 'dark' : 'default', securityLevel: 'loose' });
    }
    document.querySelectorAll('.card').forEach((card, i) => {
        card.style.opacity = '0';
        card.style.animation = `fadeIn 0.5s ease ${i * 0.1}s forwards`;
    });
});

document.addEventListener('click', function(e) {
    const sidebar = document.getElementById('sidebar');
    const toggle = document.querySelector('.menu-toggle');
    if (window.innerWidth <= 768 && sidebar && sidebar.classList.contains('open') && !sidebar.contains(e.target) && !toggle.contains(e.target)) {
        sidebar.classList.remove('open');
    }
});
"""
    with open(OUTPUT_PATH / "arc-scc.js", 'w', encoding='utf-8') as f:
        f.write(js)
    print("✅ JavaScript gegenereerd")

def generate_base_template(title, content, blocks, active_page, theme="cyan", mode="dark"):
    sidebar = generate_navigation(blocks, active_page)
    topbar = generate_topbar(title, theme, mode)
    return f"""<!DOCTYPE html>
<html lang="nl" data-theme="{theme}" data-mode="{mode}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | Arc SCC</title>
    <link rel="stylesheet" href="css/arc-scc.css">
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
</head>
<body>
    <div class="app-container">
        {sidebar}
        <div class="main-content">
            {topbar}
            <main class="content">{content}</main>
        </div>
    </div>
    <script src="arc-scc.js"></script>
</body>
</html>
"""

def generate_dashboard(data, blocks):
    total = len(blocks)
    completed = sum(1 for b in blocks if b['status'] == 'completed')
    in_progress = sum(1 for b in blocks if b['status'] == 'in-progress')
    pending = sum(1 for b in blocks if b['status'] == 'pending')
    
    overall = data.get('overall', {})
    avg_progress = overall.get('progress_percent', 0)
    
    chapters_html = ""
    for chapter in data.get('chapters', []):
        title = chapter.get('title', '')
        status = chapter.get('status', 'planned')
        progress = chapter.get('progress_percent', 0)
        done = chapter.get('done_blocks', 0)
        total_ch = chapter.get('total_blocks', 0)
        color = chapter.get('color', 'cyan')
        
        status_class = STATUS_MAP.get(status, 'pending')
        status_text = {'completed': 'Voltooid', 'finished': 'Voltooid', 'in-progress': 'Bezig', 'started': 'Gestart', 'planned': 'Gepland'}.get(status, status)
        
        chapters_html += f"""
    <div class="card">
        <div class="card-header">
            <div class="card-title" style="color: var(--{color if color in ['gold', 'cyan', 'purple', 'teal'] else 'primary'});">📁 {title}</div>
            <span class="status {status_class}">{status_text}</span>
        </div>
        <div class="progress-container">
            <div class="progress-bar">
                <div class="progress-fill" style="width: {progress}%"></div>
            </div>
            <div class="progress-text">
                <span>{done}/{total_ch} blocks</span>
                <span>{progress}%</span>
            </div>
        </div>
    </div>
"""
    
    stats_html = f"""
<div class="grid grid-4 mb-3">
    <div class="card text-center">
        <div class="meta-label">Totaal Blocks</div>
        <div style="font-size: 2.5rem; color: var(--primary); font-weight: bold;">{total}</div>
    </div>
    <div class="card text-center">
        <div class="meta-label">Voltooid</div>
        <div style="font-size: 2.5rem; color: var(--success); font-weight: bold;">{completed}</div>
    </div>
    <div class="card text-center">
        <div class="meta-label">In Ontwikkeling</div>
        <div style="font-size: 2.5rem; color: var(--warning); font-weight: bold;">{in_progress}</div>
    </div>
    <div class="card text-center">
        <div class="meta-label">Totaal Voortgang</div>
        <div style="font-size: 2.5rem; color: var(--info); font-weight: bold;">{avg_progress}%</div>
    </div>
</div>
"""
    
    progress_html = f"""
<div class="card mb-3">
    <div class="card-header">
        <div class="card-title">📊 Project Voortgang</div>
        <span class="status {'completed' if avg_progress == 100 else 'in-progress' if avg_progress > 0 else 'pending'}">
            {'Voltooid' if avg_progress == 100 else 'Bezig' if avg_progress > 0 else 'Wachtend'}
        </span>
    </div>
    <div class="progress-container">
        <div class="progress-bar">
            <div class="progress-fill" style="width: {avg_progress}%"></div>
        </div>
        <div class="progress-text">
            <span>Project Start</span>
            <span>{avg_progress}%</span>
            <span>Project Complete</span>
        </div>
    </div>
</div>
"""
    
    content = f"""
<div class="page-header">
    <h1 class="page-title">🏠 Dashboard</h1>
    <p class="page-subtitle">The Arc Strategic Control Center - Overzicht</p>
</div>
{stats_html}
{progress_html}
<h2 style="color: var(--primary); margin: 2rem 0 1rem 0;">📁 Chapters</h2>
<div class="grid">
{chapters_html}
</div>
<h2 style="color: var(--primary); margin: 2rem 0 1rem 0;">🔷 Recent Blocks</h2>
<div class="grid">
"""
    
    for block in blocks[-6:]:
        block_id = block['id']
        block_title = block['title']
        block_status = block['status']
        block_orig_status = block['original_status']
        block_chapter = block['chapter']
        block_num = block['num_id']
        content += f"""
    <div class="card">
        <div class="card-header">
            <div class="card-title">🔷 {block_id}: {block_title[:25]}...</div>
            <span class="status {block_status}">{block_orig_status}</span>
        </div>
        <p style="color: var(--text-secondary); font-size: 0.9rem;">📁 {block_chapter}</p>
        <div style="margin-top: 1rem; text-align: right;">
            <a href="block_{block_num}.html" style="color: var(--primary);">Details →</a>
        </div>
    </div>
"""
    content += "</div>"
    
    return generate_base_template("Dashboard", content, blocks, "dashboard")

def generate_chapters_page(data, blocks):
    content = """
<div class="page-header">
    <h1 class="page-title">📚 Hoofdstukken / Chapters</h1>
    <p class="page-subtitle">Alle project chapters en hun status</p>
</div>
"""
    
    for chapter in data.get('chapters', []):
        title = chapter.get('title', '')
        status = chapter.get('status', 'planned')
        progress = chapter.get('progress_percent', 0)
        done = chapter.get('done_blocks', 0)
        total = chapter.get('total_blocks', 0)
        
        status_text = {'completed': 'Voltooid', 'finished': 'Voltooid', 'in-progress': 'Bezig', 'started': 'Gestart', 'planned': 'Gepland'}.get(status, status)
        
        content += f"""
<div class="chapter-section">
    <div class="chapter-header">
        <div class="chapter-title">📁 {title}</div>
        <div class="chapter-stats">
            <div class="chapter-stat">
                <div class="chapter-stat-value">{done}</div>
                <div class="chapter-stat-label">Done</div>
            </div>
            <div class="chapter-stat">
                <div class="chapter-stat-value">{total}</div>
                <div class="chapter-stat-label">Total</div>
            </div>
            <div class="chapter-stat">
                <div class="chapter-stat-value">{progress}%</div>
                <div class="chapter-stat-label">Progress</div>
            </div>
        </div>
        <span class="status {STATUS_MAP.get(status, 'pending')}">{status_text}</span>
    </div>
    <div class="progress-container mb-3">
        <div class="progress-bar">
            <div class="progress-fill" style="width: {progress}%"></div>
        </div>
    </div>
</div>
"""
    
    return generate_base_template("Hoofdstukken", content, blocks, "chapters")

def generate_timeline(blocks):
    content = """
<div class="page-header">
    <h1 class="page-title">📅 Tijdlijn / Timeline</h1>
    <p class="page-subtitle">Project mijlpalen</p>
</div>
<div class="card">
    <div style="position: relative; padding-left: 2rem;">
        <div style="position: absolute; left: 0; top: 0; bottom: 0; width: 2px; background: linear-gradient(to bottom, var(--primary), var(--secondary));"></div>
        
        <div style="position: relative; margin-bottom: 2rem; padding-left: 1.5rem;">
            <div style="position: absolute; left: -1.6rem; top: 0.25rem; width: 12px; height: 12px; background: var(--success); border-radius: 50%; border: 2px solid var(--bg-card); box-shadow: 0 0 0 2px var(--success);"></div>
            <h3 style="color: var(--success);">Q1 2024 - Fundatie</h3>
            <span class="status completed">Voltooid</span>
            <p style="color: var(--text-secondary);">Platform & Runtime, Security Hardening</p>
        </div>
        
        <div style="position: relative; margin-bottom: 2rem; padding-left: 1.5rem;">
            <div style="position: absolute; left: -1.6rem; top: 0.25rem; width: 12px; height: 12px; background: var(--warning); border-radius: 50%; border: 2px solid var(--bg-card); box-shadow: 0 0 0 2px var(--warning);" class="pulse"></div>
            <h3 style="color: var(--warning);">Q2 2024 - Ontwikkeling</h3>
            <span class="status in-progress">Bezig</span>
            <p style="color: var(--text-secondary);">Model Runtime, Agent Logic, Control Center UI</p>
        </div>
        
        <div style="position: relative; padding-left: 1.5rem;">
            <div style="position: absolute; left: -1.6rem; top: 0.25rem; width: 12px; height: 12px; background: var(--text-muted); border-radius: 50%; border: 2px solid var(--bg-card);"></div>
            <h3 style="color: var(--text-secondary);">Q3 2024 - Toekomst</h3>
            <span class="status pending">Gepland</span>
            <p style="color: var(--text-secondary);">Observability, Mission Control</p>
        </div>
    </div>
</div>
"""
    return generate_base_template("Tijdlijn", content, blocks, "timeline")

def generate_about(blocks):
    content = """
<div class="page-header">
    <h1 class="page-title">ℹ️ Over / About</h1>
    <p class="page-subtitle">Arc Strategic Control Center</p>
</div>
<div class="grid grid-2">
    <div class="card">
        <h2 style="color: var(--primary);">🎯 Project</h2>
        <p style="color: var(--text-secondary);">Het Arc Strategic Control Center is een geavanceerd management systeem voor AI agent orchestratie, monitoring en control.</p>
    </div>
    <div class="card">
        <h2 style="color: var(--primary);">✨ Features</h2>
        <ul style="color: var(--text-secondary); list-style: none;">
            <li>⚡ Multi-agent orchestratie</li>
            <li>🔒 Security hardening</li>
            <li>📊 Real-time monitoring</li>
            <li>🎨 4 themes + Dark/Light</li>
        </ul>
    </div>
</div>
"""
    return generate_base_template("Over", content, blocks, "about")

def generate_block_page(block, blocks, data):
    block_id_num = block['num_id']
    name = block['title']
    status = block['status']
    original_status = block['original_status']
    progress = block['progress']
    chapter = block['chapter']
    cluster = block['cluster']
    block_id_str = block['id']
    
    md_content = load_markdown_content(block_id_str)
    mermaid_diagrams = extract_mermaid_diagrams(md_content)
    html_content = markdown_to_html(md_content)
    
    mermaid_html = ""
    for i, diagram in enumerate(mermaid_diagrams):
        mermaid_html += f'<div class="mermaid-container"><div class="meta-label">Diagram {i+1}</div><div class="mermaid">{diagram}</div></div>'
    
    if not mermaid_html:
        mermaid_html = '<p style="color: var(--text-muted);">Geen diagrammen beschikbaar</p>'
    
    content = f"""
<div class="page-header">
    <h1 class="page-title">🔷 {name}</h1>
    <p class="page-subtitle">Block {block_id_str} | {chapter} &gt; {cluster}</p>
</div>

<div class="block-meta">
    <div class="meta-item">
        <div class="meta-label">Block ID</div>
        <div class="meta-value">{block_id_str}</div>
    </div>
    <div class="meta-item">
        <div class="meta-label">Status</div>
        <div class="meta-value"><span class="status {status}">{original_status}</span></div>
    </div>
    <div class="meta-item">
        <div class="meta-label">Voortgang</div>
        <div class="meta-value">{progress}%</div>
    </div>
    <div class="meta-item">
        <div class="meta-label">Chapter</div>
        <div class="meta-value">{chapter}</div>
    </div>
</div>

<div class="card">
    <div class="card-header">
        <div class="card-title">📊 Voortgang</div>
    </div>
    <div class="progress-container">
        <div class="progress-bar">
            <div class="progress-fill" style="width: {progress}%"></div>
        </div>
        <div class="progress-text">
            <span>Start</span>
            <span>{progress}% Compleet</span>
            <span>Finish</span>
        </div>
    </div>
</div>

<div class="grid grid-2">
    <div class="card">
        <div class="card-header">
            <div class="card-title">📝 Documentatie</div>
        </div>
        <div class="content-body">{html_content}</div>
    </div>
    <div class="card">
        <div class="card-header">
            <div class="card-title">📐 Diagrammen</div>
        </div>
        {mermaid_html}
    </div>
</div>

<div style="margin-top: 2rem; text-align: center;">
    <a href="index.html" style="display: inline-flex; align-items: center; gap: 0.5rem; padding: 0.75rem 1.5rem; background: var(--bg-secondary); color: var(--primary); text-decoration: none; border-radius: 8px; border: 1px solid var(--border-color);">
        ← Terug naar Dashboard
    </a>
</div>
"""
    return generate_base_template(name, content, blocks, f"block_{block_id_num}")

def main():
    print("🚀 Arc SCC Website Generator")
    print("=" * 50)
    
    OUTPUT_PATH.mkdir(parents=True, exist_ok=True)
    CSS_PATH.mkdir(parents=True, exist_ok=True)
    CONTENT_PATH.mkdir(parents=True, exist_ok=True)
    
    data = load_progress_data()
    if not data:
        print("\n❌ Geen data gevonden.")
        return
    
    blocks = get_all_blocks(data)
    print(f"✅ {len(blocks)} blocks gevonden")
    
    print("\n📁 Genereren van assets...")
    generate_css()
    generate_js()
    
    print("\n📄 Genereren van pagina's...")
    
    pages = [
        ("index.html", generate_dashboard(data, blocks)),
        ("chapters.html", generate_chapters_page(data, blocks)),
        ("timeline.html", generate_timeline(blocks)),
        ("about.html", generate_about(blocks)),
    ]
    
    for filename, html in pages:
        with open(OUTPUT_PATH / filename, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"   ✅ {filename}")
    
    print("\n🔷 Genereren van block pagina's...")
    for block in blocks:
        html = generate_block_page(block, blocks, data)
        with open(OUTPUT_PATH / f"block_{block['num_id']}.html", 'w', encoding='utf-8') as f:
            f.write(html)
    print(f"   ✅ {len(blocks)} block pagina's")
    
    total_pages = len(pages) + len(blocks)
    print("\n" + "=" * 50)
    print("✅ Website generatie voltooid!")
    print(f"📂 Locatie: {OUTPUT_PATH}")
    print(f"📊 Totaal: {total_pages} pagina's")
    print("\n🌐 Open de website in Chrome:")
    print("   google-chrome output/index.html")
    print("=" * 50)

if __name__ == "__main__":
    main()
