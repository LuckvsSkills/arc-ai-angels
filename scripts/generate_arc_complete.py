#!/usr/bin/env python3
import os, json

BASE_DIR = os.path.expanduser("~/arc_strategic_control_center/output")
os.makedirs(BASE_DIR, exist_ok=True)
os.makedirs(f"{BASE_DIR}/css", exist_ok=True)
os.makedirs(f"{BASE_DIR}/js", exist_ok=True)

# Complete data structuur - 8 chapters, 54 blocks
CHAPTERS = [
    {"id": "ch1", "title": "Foundation", "blocks": [
        {"id": "b01", "title": "System Architecture Overview", "type": "concept"},
        {"id": "b02", "title": "Hardware Requirements", "type": "spec"},
        {"id": "b03", "title": "Network Topology", "type": "diagram"},
        {"id": "b04", "title": "Base Configuration", "type": "config"},
        {"id": "b05", "title": "Installation Procedures", "type": "procedure"},
        {"id": "b06", "title": "Initial Setup", "type": "guide"},
        {"id": "b07", "title": "Core Services", "type": "service"}
    ]},
    {"id": "ch2", "title": "Platform & Runtime", "blocks": [
        {"id": "b08", "title": "Runtime Environment", "type": "concept"},
        {"id": "b09", "title": "Container Orchestration", "type": "diagram"},
        {"id": "b10", "title": "Service Mesh", "type": "architecture"},
        {"id": "b11", "title": "Load Balancing", "type": "config"},
        {"id": "b12", "title": "Auto-scaling", "type": "feature"},
        {"id": "b13", "title": "Resource Management", "type": "guide"},
        {"id": "b14", "title": "Monitoring Stack", "type": "service"}
    ]},
    {"id": "ch3", "title": "Security Hardening", "blocks": [
        {"id": "b15", "title": "Threat Model", "type": "analysis"},
        {"id": "b16", "title": "Access Control", "type": "policy"},
        {"id": "b17", "title": "Encryption Standards", "type": "standard"},
        {"id": "b18", "title": "Firewall Configuration", "type": "config"},
        {"id": "b19", "title": "Intrusion Detection", "type": "service"},
        {"id": "b20", "title": "Audit Logging", "type": "procedure"},
        {"id": "b21", "title": "Vulnerability Management", "type": "process"}
    ]},
    {"id": "ch4", "title": "Data Management", "blocks": [
        {"id": "b22", "title": "Data Architecture", "type": "diagram"},
        {"id": "b23", "title": "Storage Solutions", "type": "comparison"},
        {"id": "b24", "title": "Backup Strategy", "type": "plan"},
        {"id": "b25", "title": "Data Pipeline", "type": "flow"},
        {"id": "b26", "title": "ETL Processes", "type": "procedure"},
        {"id": "b27", "title": "Data Governance", "type": "policy"},
        {"id": "b28", "title": "Disaster Recovery", "type": "plan"}
    ]},
    {"id": "ch5", "title": "API & Integration", "blocks": [
        {"id": "b29", "title": "API Design Principles", "type": "standard"},
        {"id": "b30", "title": "REST Endpoints", "type": "reference"},
        {"id": "b31", "title": "GraphQL Schema", "type": "schema"},
        {"id": "b32", "title": "Authentication Flow", "type": "diagram"},
        {"id": "b33", "title": "Rate Limiting", "type": "config"},
        {"id": "b34", "title": "Webhook Integration", "type": "guide"},
        {"id": "b35", "title": "Third-party Connectors", "type": "integration"}
    ]},
    {"id": "ch6", "title": "Deployment & CI/CD", "blocks": [
        {"id": "b36", "title": "Deployment Pipeline", "type": "diagram"},
        {"id": "b37", "title": "Build Automation", "type": "config"},
        {"id": "b38", "title": "Testing Strategy", "type": "plan"},
        {"id": "b39", "title": "Release Management", "type": "process"},
        {"id": "b40", "title": "Rollback Procedures", "type": "procedure"},
        {"id": "b41", "title": "Environment Promotion", "type": "flow"},
        {"id": "b42", "title": "Version Control", "type": "guide"}
    ]},
    {"id": "ch7", "title": "Operations & Monitoring", "blocks": [
        {"id": "b43", "title": "Operations Runbook", "type": "procedure"},
        {"id": "b44", "title": "Alerting Rules", "type": "config"},
        {"id": "b45", "title": "Incident Response", "type": "process"},
        {"id": "b46", "title": "Performance Tuning", "type": "guide"},
        {"id": "b47", "title": "Capacity Planning", "type": "analysis"},
        {"id": "b48", "title": "SLA Management", "type": "policy"},
        {"id": "b49", "title": "Maintenance Windows", "type": "schedule"}
    ]},
    {"id": "ch8", "title": "Compliance & Governance", "blocks": [
        {"id": "b50", "title": "Compliance Framework", "type": "standard"},
        {"id": "b51", "title": "Audit Procedures", "type": "procedure"},
        {"id": "b52", "title": "Risk Assessment", "type": "analysis"},
        {"id": "b53", "title": "Policy Enforcement", "type": "config"},
        {"id": "b54", "title": "Documentation Standards", "type": "standard"}
    ]}
]

# Professionele CSS met alle features
CSS = """/* ARC Strategic Control Center - Complete CSS */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
:root { 
    --primary: #FFD700; --primary-dark: #B8860B; --primary-light: #FFF8DC;
    --secondary: #1a1a2e; --accent: #ff6b6b; --bg: #0f0f1a; --bg-light: #1a1a2e;
    --text: #e0e0e0; --text-muted: #888; --border: rgba(255, 215, 0, 0.2);
    --card-bg: rgba(26, 26, 46, 0.8); --hover-bg: rgba(255, 215, 0, 0.1);
    --font-main: 'Segoe UI', system-ui, -apple-system, sans-serif;
    --font-mono: 'Fira Code', 'Consolas', monospace;
    --shadow: rgba(0, 0, 0, 0.5);
}
[data-theme="cyan"] { --primary: #00CED1; --border: rgba(0, 206, 209, 0.2); --hover-bg: rgba(0, 206, 209, 0.1); }
[data-theme="purple"] { --primary: #9370DB; --border: rgba(147, 112, 219, 0.2); --hover-bg: rgba(147, 112, 219, 0.1); }
[data-theme="teal"] { --primary: #20B2AA; --border: rgba(32, 178, 170, 0.2); --hover-bg: rgba(32, 178, 170, 0.1); }
[data-theme="light"] { --bg: #f5f5f5; --bg-light: #ffffff; --text: #333; --text-muted: #666; --card-bg: rgba(255, 255, 255, 0.9); --shadow: rgba(0, 0, 0, 0.1); --border: rgba(0, 0, 0, 0.1); }

body { font-family: var(--font-main); background: var(--bg); color: var(--text); line-height: 1.6; min-height: 100vh; }
.app-container { display: flex; min-height: 100vh; }

/* Topbar */
.topbar { position: fixed; top: 0; left: 0; right: 0; height: 60px; background: var(--bg-light); border-bottom: 1px solid var(--border); display: flex; align-items: center; justify-content: space-between; padding: 0 2rem; z-index: 1000; box-shadow: 0 2px 10px var(--shadow); }
.logo { font-size: 1.5rem; font-weight: bold; color: var(--primary); text-decoration: none; display: flex; align-items: center; gap: 0.5rem; }
.logo::before { content: "◆"; color: var(--primary); }
.topbar-controls { display: flex; align-items: center; gap: 1rem; }

/* Theme Switcher */
.theme-switcher { display: flex; gap: 0.5rem; }
.theme-btn { width: 24px; height: 24px; border-radius: 50%; border: 2px solid transparent; cursor: pointer; transition: all 0.3s ease; }
.theme-btn:hover, .theme-btn.active { border-color: var(--text); transform: scale(1.1); }
.theme-btn.gold { background: #FFD700; } .theme-btn.cyan { background: #00CED1; } .theme-btn.purple { background: #9370DB; } .theme-btn.teal { background: #20B2AA; }

/* Mode Toggle */
.mode-toggle { background: var(--card-bg); border: 1px solid var(--border); color: var(--text); padding: 0.5rem 1rem; border-radius: 20px; cursor: pointer; font-size: 0.9rem; transition: all 0.3s ease; }
.mode-toggle:hover { background: var(--hover-bg); border-color: var(--primary); }

/* Sidebar */
.sidebar { position: fixed; top: 60px; left: 0; width: 320px; height: calc(100vh - 60px); background: var(--bg-light); border-right: 1px solid var(--border); overflow-y: auto; padding: 1.5rem; z-index: 100; }
.sidebar-header { font-size: 0.75rem; text-transform: uppercase; letter-spacing: 2px; color: var(--text-muted); margin-bottom: 1.5rem; padding-bottom: 0.75rem; border-bottom: 1px solid var(--border); }
.nav-list { list-style: none; }
.nav-chapter { margin-bottom: 1rem; }
.chapter-toggle { display: flex; align-items: center; justify-content: space-between; width: 100%; padding: 0.75rem 1rem; background: var(--card-bg); border: 1px solid var(--border); border-radius: 8px; cursor: pointer; color: var(--text); font-size: 0.95rem; font-weight: 600; transition: all 0.3s ease; }
.chapter-toggle:hover { background: var(--hover-bg); border-color: var(--primary); }
.chapter-toggle::after { content: "▼"; font-size: 0.7rem; transition: transform 0.3s ease; }
.nav-chapter.expanded .chapter-toggle::after { transform: rotate(180deg); }
.chapter-blocks { display: none; list-style: none; padding-left: 0.5rem; margin-top: 0.5rem; }
.nav-chapter.expanded .chapter-blocks { display: block; }
.block-link { display: flex; align-items: center; padding: 0.6rem 0.75rem; color: var(--text-muted); text-decoration: none; border-radius: 6px; font-size: 0.9rem; transition: all 0.2s ease; margin-bottom: 0.25rem; border-left: 3px solid transparent; }
.block-link:hover { background: var(--hover-bg); color: var(--primary); border-left-color: var(--primary); }
.block-link.active { background: var(--hover-bg); color: var(--primary); border-left-color: var(--primary); }
.block-id { font-family: var(--font-mono); font-size: 0.8rem; color: var(--primary); min-width: 35px; }
.block-title { margin-left: 0.5rem; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }

/* Main Content */
.main-content { margin-left: 320px; margin-top: 60px; padding: 2rem; flex: 1; min-height: calc(100vh - 60px); }

/* Page Header */
.page-header { margin-bottom: 2rem; padding-bottom: 1rem; border-bottom: 2px solid var(--border); }
.page-title { font-size: 2.2rem; font-weight: 700; color: var(--primary); margin-bottom: 0.5rem; }
.page-subtitle { color: var(--text-muted); font-size: 1.1rem; }

/* Breadcrumbs */
.breadcrumbs { display: flex; align-items: center; gap: 0.5rem; margin-bottom: 1.5rem; font-size: 0.9rem; color: var(--text-muted); }
.breadcrumbs a { color: var(--primary); text-decoration: none; }
.breadcrumbs a:hover { text-decoration: underline; }

/* Progress Container */
.progress-container { background: var(--card-bg); border: 1px solid var(--border); border-radius: 12px; padding: 1.5rem; margin-bottom: 2rem; }
.progress-header { display: flex; justify-content: space-between; margin-bottom: 0.75rem; font-weight: 600; }
.progress-bar { width: 100%; height: 10px; background: var(--bg); border-radius: 5px; overflow: hidden; }
.progress-fill { height: 100%; background: linear-gradient(90deg, var(--primary), var(--primary-dark)); border-radius: 5px; transition: width 0.5s ease; }

/* Cards */
.card-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 1.5rem; margin-top: 2rem; }
.card { background: var(--card-bg); border: 1px solid var(--border); border-radius: 12px; padding: 1.75rem; transition: all 0.3s ease; cursor: pointer; text-decoration: none; color: var(--text); display: block; position: relative; overflow: hidden; }
.card::before { content: ""; position: absolute; top: 0; left: 0; width: 4px; height: 100%; background: var(--primary); opacity: 0; transition: opacity 0.3s ease; }
.card:hover { transform: translateY(-5px); box-shadow: 0 15px 35px var(--shadow); border-color: var(--primary); }
.card:hover::before { opacity: 1; }
.card-title { font-size: 1.3rem; font-weight: 600; color: var(--primary); margin-bottom: 0.75rem; }
.card-subtitle { color: var(--text-muted); font-size: 0.95rem; line-height: 1.5; }
.card-meta { display: flex; gap: 1rem; margin-top: 1.25rem; font-size: 0.85rem; color: var(--text-muted); }

/* Chapter List */
.chapter-list { display: flex; flex-direction: column; gap: 1.5rem; }
.chapter-item { background: var(--card-bg); border: 1px solid var(--border); border-radius: 12px; padding: 2rem; transition: all 0.3s ease; }
.chapter-item:hover { border-color: var(--primary); box-shadow: 0 10px 30px var(--shadow); }
.chapter-item-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; }
.chapter-item-title { font-size: 1.6rem; color: var(--primary); text-decoration: none; font-weight: 600; }
.chapter-item-title:hover { text-decoration: underline; }
.chapter-item-meta { font-size: 0.9rem; color: var(--text-muted); background: var(--hover-bg); padding: 0.25rem 0.75rem; border-radius: 20px; }
.chapter-blocks-preview { display: flex; flex-wrap: wrap; gap: 0.5rem; margin-top: 1.25rem; }
.block-tag { background: var(--hover-bg); border: 1px solid var(--border); padding: 0.4rem 0.8rem; border-radius: 20px; font-size: 0.8rem; color: var(--text-muted); text-decoration: none; transition: all 0.2s ease; }
.block-tag:hover { background: var(--primary); color: var(--secondary); }

/* Block Page */
.block-container { max-width: 900px; margin: 0 auto; }
.block-header { background: var(--card-bg); border: 1px solid var(--border); border-radius: 12px; padding: 2.5rem; margin-bottom: 2rem; text-align: center; }
.block-id-badge { display: inline-block; background: var(--primary); color: var(--secondary); padding: 0.4rem 1rem; border-radius: 20px; font-family: var(--font-mono); font-size: 0.9rem; font-weight: 700; margin-bottom: 1rem; text-transform: uppercase; letter-spacing: 1px; }
.block-title-large { font-size: 2.5rem; font-weight: 700; margin-bottom: 1rem; color: var(--text); line-height: 1.2; }
.block-type-badge { display: inline-block; background: var(--hover-bg); border: 1px solid var(--border); padding: 0.5rem 1.25rem; border-radius: 6px; font-size: 0.85rem; color: var(--primary); text-transform: uppercase; letter-spacing: 2px; font-weight: 600; }
.block-content { background: var(--card-bg); border: 1px solid var(--border); border-radius: 12px; padding: 2.5rem; line-height: 1.8; font-size: 1rem; }
.block-content h2 { color: var(--primary); margin-top: 2.5rem; margin-bottom: 1.25rem; font-size: 1.6rem; border-bottom: 1px solid var(--border); padding-bottom: 0.5rem; }
.block-content h3 { color: var(--primary-dark); margin-top: 2rem; margin-bottom: 1rem; font-size: 1.3rem; }
.block-content p { margin-bottom: 1.25rem; color: var(--text); }
.block-content ul, .block-content ol { margin-left: 2rem; margin-bottom: 1.5rem; }
.block-content li { margin-bottom: 0.75rem; }
.block-content strong { color: var(--primary); }
.block-content code { background: var(--bg); padding: 0.2rem 0.5rem; border-radius: 4px; font-family: var(--font-mono); font-size: 0.9em; color: var(--primary); border: 1px solid var(--border); }
.block-content pre { background: var(--bg); padding: 1.25rem; border-radius: 8px; overflow-x: auto; margin: 1.5rem 0; border: 1px solid var(--border); font-family: var(--font-mono); font-size: 0.9rem; line-height: 1.6; }
.block-content pre code { background: none; padding: 0; border: none; color: var(--text); }

/* Mermaid */
.mermaid-container { background: var(--bg); border: 2px solid var(--border); border-radius: 12px; padding: 2rem; margin: 2.5rem 0; text-align: center; position: relative; }
.mermaid-container::before { content: "Architecture Diagram"; position: absolute; top: -12px; left: 20px; background: var(--card-bg); padding: 0.25rem 0.75rem; font-size: 0.8rem; color: var(--primary); text-transform: uppercase; letter-spacing: 2px; font-weight: 600; border: 1px solid var(--border); border-radius: 4px; }
.mermaid { font-family: var(--font-main) !important; }
.mermaid svg { max-width: 100%; height: auto; font-family: var(--font-main) !important; }
.mermaid svg text { font-family: var(--font-main) !important; fill: var(--text) !important; }

/* Navigation Footer */
.block-nav { display: flex; justify-content: space-between; margin-top: 2.5rem; padding-top: 2rem; border-top: 2px solid var(--border); }
.block-nav a { color: var(--primary); text-decoration: none; font-weight: 600; display: flex; align-items: center; gap: 0.5rem; transition: all 0.3s ease; }
.block-nav a:hover { transform: translateX(5px); }
.block-nav a[href="#"] { visibility: hidden; }

/* Responsive */
@media (max-width: 1024px) { .sidebar { transform: translateX(-100%); } .main-content { margin-left: 0; } }
@media (max-width: 768px) { .card-grid { grid-template-columns: 1fr; } .page-title { font-size: 1.75rem; } .block-title-large { font-size: 1.75rem; } }
"""

# JavaScript met Mermaid support
JS = """// ARC Strategic Control Center - Complete JavaScript
(function() {
    'use strict';
    
    // Theme Manager
    const ThemeManager = {
        currentTheme: 'gold', currentMode: 'dark',
        init() {
            this.loadSavedTheme();
            this.setupEventListeners();
            this.applyTheme();
        },
        loadSavedTheme() {
            this.currentTheme = localStorage.getItem('arc-theme') || 'gold';
            this.currentMode = localStorage.getItem('arc-mode') || 'dark';
        },
        setupEventListeners() {
            document.querySelectorAll('.theme-btn').forEach(btn => {
                btn.addEventListener('click', (e) => this.setTheme(e.target.dataset.theme));
            });
            const modeToggle = document.getElementById('mode-toggle');
            if (modeToggle) modeToggle.addEventListener('click', () => this.toggleMode());
        },
        setTheme(theme) {
            this.currentTheme = theme;
            localStorage.setItem('arc-theme', theme);
            this.applyTheme();
            this.updateActiveButtons();
        },
        toggleMode() {
            this.currentMode = this.currentMode === 'dark' ? 'light' : 'dark';
            localStorage.setItem('arc-mode', this.currentMode);
            this.applyTheme();
            this.updateModeButton();
        },
        applyTheme() {
            document.documentElement.setAttribute('data-theme', this.currentTheme);
            document.documentElement.setAttribute('data-mode', this.currentMode);
        },
        updateActiveButtons() {
            document.querySelectorAll('.theme-btn').forEach(btn => {
                btn.classList.toggle('active', btn.dataset.theme === this.currentTheme);
            });
        },
        updateModeButton() {
            const btn = document.getElementById('mode-toggle');
            if (btn) btn.textContent = this.currentMode === 'dark' ? '☀️ Light' : '🌙 Dark';
        }
    };

    // Navigation Manager
    const NavigationManager = {
        init() {
            this.setupChapterExpansion();
            this.highlightCurrentPage();
        },
        setupChapterExpansion() {
            document.querySelectorAll('.chapter-toggle').forEach(toggle => {
                toggle.addEventListener('click', (e) => {
                    const chapter = e.target.closest('.nav-chapter');
                    chapter.classList.toggle('expanded');
                    const chapterId = chapter.dataset.chapter;
                    const isExpanded = chapter.classList.contains('expanded');
                    localStorage.setItem(`nav-${chapterId}`, isExpanded);
                });
            });
            // Restore expansion state
            document.querySelectorAll('.nav-chapter').forEach(chapter => {
                const chapterId = chapter.dataset.chapter;
                if (localStorage.getItem(`nav-${chapterId}`) === 'true') {
                    chapter.classList.add('expanded');
                }
            });
        },
        highlightCurrentPage() {
            const currentFile = window.location.pathname.split('/').pop() || 'index.html';
            document.querySelectorAll('.block-link').forEach(link => {
                if (link.getAttribute('href') === currentFile) {
                    link.classList.add('active');
                    const chapter = link.closest('.nav-chapter');
                    if (chapter) chapter.classList.add('expanded');
                }
            });
        }
    };

    // Mermaid Manager
    const MermaidManager = {
        initialized: false,
        init() {
            if (this.initialized || typeof mermaid === 'undefined') return;
            this.initialized = true;
            
            const isFirefox = navigator.userAgent.toLowerCase().includes('firefox');
            
            mermaid.initialize({
                startOnLoad: false,
                theme: document.documentElement.getAttribute('data-mode') === 'dark' ? 'dark' : 'default',
                securityLevel: 'loose',
                fontFamily: 'Segoe UI, system-ui, sans-serif',
                flowchart: { useMaxWidth: true, htmlLabels: !isFirefox, curve: 'basis' },
                sequence: { useMaxWidth: true },
                gantt: { useMaxWidth: true }
            });
            
            this.renderDiagrams();
        },
        renderDiagrams() {
            document.querySelectorAll('.mermaid').forEach((element, index) => {
                if (element.getAttribute('data-processed') === 'true') return;
                
                const graphDefinition = element.textContent.trim();
                if (!graphDefinition) return;
                
                const id = `mermaid-${index}-${Date.now()}`;
                
                try {
                    mermaid.render(id, graphDefinition).then(result => {
                        element.innerHTML = result.svg;
                        element.setAttribute('data-processed', 'true');
                        
                        const svg = element.querySelector('svg');
                        if (svg) {
                            svg.style.maxWidth = '100%';
                            svg.style.height = 'auto';
                            svg.setAttribute('width', '100%');
                            svg.removeAttribute('height');
                            
                            svg.querySelectorAll('text').forEach(text => {
                                text.style.fontFamily = 'Segoe UI, system-ui, sans-serif';
                                if (!text.getAttribute('fill')) {
                                    text.setAttribute('fill', 'var(--text)');
                                }
                            });
                        }
                    }).catch(err => {
                        console.error('Mermaid error:', err);
                        element.innerHTML = '<div style="color: #ff6b6b; padding: 1rem;">Diagram render error</div>';
                    });
                } catch (err) {
                    console.error('Mermaid error:', err);
                }
            });
        }
    };

    // Initialize
    function init() {
        ThemeManager.init();
        NavigationManager.init();
        
        if (document.querySelectorAll('.mermaid').length > 0) {
            setTimeout(() => MermaidManager.init(), 300);
        }
        
        console.log('🚀 ARC Strategic Control Center initialized');
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
"""

def generate_sidebar(active_block=None):
    html = '<aside class="sidebar" id="sidebar">\n'
    html += '<div class="sidebar-header">Navigation</div>\n<nav><ul class="nav-list">\n'
    
    for chapter in CHAPTERS:
        chapter_id = chapter["id"]
        is_expanded = "expanded" if chapter_id == "ch1" else ""
        html += f'<li class="nav-chapter {is_expanded}" data-chapter="{chapter_id}">\n'
        html += f'<button class="chapter-toggle">{chapter["title"]}</button>\n'
        html += '<ul class="chapter-blocks">\n'
        
        for block in chapter["blocks"]:
            block_id = block["id"]
            block_title = block["title"]
            is_active = "active" if active_block == block_id else ""
            html += f'<li><a href="block_{block_id}.html" class="block-link {is_active}">'
            html += f'<span class="block-id">{block_id}</span>'
            html += f'<span class="block-title">{block_title}</span></a></li>\n'
        
        html += '</ul>\n</li>\n'
    
    html += '</ul></nav>\n</aside>\n'
    return html

def generate_topbar():
    return '''<header class="topbar">
    <a href="index.html" class="logo">ARC Strategic Control Center</a>
    <div class="topbar-controls">
        <div class="theme-switcher">
            <button class="theme-btn gold active" data-theme="gold" title="Gold Theme"></button>
            <button class="theme-btn cyan" data-theme="cyan" title="Cyan Theme"></button>
            <button class="theme-btn purple" data-theme="purple" title="Purple Theme"></button>
            <button class="theme-btn teal" data-theme="teal" title="Teal Theme"></button>
        </div>
        <button id="mode-toggle" class="mode-toggle">☀️ Light</button>
    </div>
</header>\n'''

def get_prev_next_block(current_block_id):
    all_blocks = [b for ch in CHAPTERS for b in ch["blocks"]]
    current_idx = next((i for i, b in enumerate(all_blocks) if b["id"] == current_block_id), None)
    
    prev_block = all_blocks[current_idx - 1] if current_idx > 0 else None
    next_block = all_blocks[current_idx + 1] if current_idx < len(all_blocks) - 1 else None
    
    return prev_block, next_block

def generate_block_content(block, chapter_title):
    block_id = block["id"]
    title = block["title"]
    block_type = block["type"]
    
    content = f"""
<h2>Overview</h2>
<p>This block covers <strong>{title}</strong> within the {chapter_title} domain. 
It is a critical component of the enterprise architecture and requires careful implementation.</p>

<h2>Objectives</h2>
<ul>
    <li>Understand core concepts of {title}</li>
    <li>Implementation guidelines and best practices</li>
    <li>Integration with other system components</li>
    <li>Monitoring and maintenance procedures</li>
</ul>

<h2>Architecture Diagram</h2>
<div class="mermaid-container">
<div class="mermaid">
flowchart TD
    A[{title} Entry] --> B{{Validation Layer}}
    B -->|Valid| C[Processing Unit]
    B -->|Invalid| D[Error Handler]
    C --> E[Data Storage]
    D --> F[Audit Logger]
    E --> G[Output Interface]
    F --> G
    style A fill:var(--primary),stroke:#333,stroke-width:2px
    style G fill:#90EE90,stroke:#333,stroke-width:2px
</div>
</div>

<h2>Implementation</h2>
<h3>Configuration</h3>
<pre><code># Configuration for {title}
{block_id}:
  enabled: true
  version: "1.0"
  environment: production
  settings:
    retry_attempts: 3
    timeout_seconds: 30
    logging_level: info</code></pre>

<h3>Code Example</h3>
<pre><code>// {title} implementation
class {title.replace(' ', '')}Manager {{
    constructor() {{
        this.config = loadConfig('{block_id}');
        this.initialized = false;
    }}
    
    async initialize() {{
        await this.validatePrerequisites();
        await this.connect();
        this.initialized = true;
    }}
    
    async process(data) {{
        if (!this.initialized) throw new Error('Not initialized');
        return await this.transform(data);
    }}
}}</code></pre>

<h2>Best Practices</h2>
<ol>
    <li><strong>Security:</strong> Validate all inputs before processing</li>
    <li><strong>Performance:</strong> Implement caching where appropriate</li>
    <li><strong>Monitoring:</strong> Log all critical operations</li>
    <li><strong>Scalability:</strong> Design for horizontal scaling</li>
</ol>

<h2>Troubleshooting</h2>
<table style="width:100%; border-collapse: collapse; margin: 1.5rem 0;">
    <tr style="background: var(--bg);">
        <th style="padding: 0.75rem; border: 1px solid var(--border); text-align: left; color: var(--primary);">Issue</th>
        <th style="padding: 0.75rem; border: 1px solid var(--border); text-align: left; color: var(--primary);">Cause</th>
        <th style="padding: 0.75rem; border: 1px solid var(--border); text-align: left; color: var(--primary);">Solution</th>
    </tr>
    <tr>
        <td style="padding: 0.75rem; border: 1px solid var(--border);">Timeout errors</td>
        <td style="padding: 0.75rem; border: 1px solid var(--border);">Network latency</td>
        <td style="padding: 0.75rem; border: 1px solid var(--border);">Increase timeout value</td>
    </tr>
    <tr>
        <td style="padding: 0.75rem; border: 1px solid var(--border);">Connection failed</td>
        <td style="padding: 0.75rem; border: 1px solid var(--border);">Service unavailable</td>
        <td style="padding: 0.75rem; border: 1px solid var(--border);">Check service status</td>
    </tr>
</table>
"""
    return content

# Genereer CSS
with open(f"{BASE_DIR}/css/arc-scc.css", "w") as f:
    f.write(CSS)
print("✅ CSS gegenereerd")

# Genereer JS
with open(f"{BASE_DIR}/js/arc-scc.js", "w") as f:
    f.write(JS)
print("✅ JavaScript gegenereerd")

# Genereer index.html
index_html = f'''<!DOCTYPE html>
<html lang="en" data-theme="gold" data-mode="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard - ARC Strategic Control Center</title>
    <link rel="stylesheet" href="css/arc-scc.css">
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
    <script src="js/arc-scc.js" defer></script>
</head>
<body>
    <div class="app-container">
        {generate_topbar()}
        {generate_sidebar()}
        <main class="main-content">
            <div class="page-header">
                <h1 class="page-title">Dashboard</h1>
                <p class="page-subtitle">Overview of all chapters and progress</p>
            </div>
            
            <div class="progress-container">
                <div class="progress-header">
                    <span>Total Progress</span>
                    <span>100% (54/54 blocks)</span>
                </div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: 100%;"></div>
                </div>
            </div>
            
            <h2 style="color: var(--primary); margin: 2rem 0 1rem;">Chapters</h2>
            <div class="card-grid">
'''

for chapter in CHAPTERS:
    block_count = len(chapter["blocks"])
    index_html += f'''
                <a href="chapters.html#{chapter["id"]}" class="card">
                    <h3 class="card-title">{chapter["title"]}</h3>
                    <p class="card-subtitle">{chapter["blocks"][0]["title"]} and {block_count-1} more blocks...</p>
                    <div class="card-meta">
                        <span>📦 {block_count} blocks</span>
                        <span>✅ Complete</span>
                    </div>
                </a>
'''

index_html += '''
            </div>
            
            <h2 style="color: var(--primary); margin: 2rem 0 1rem;">Quick Links</h2>
            <div class="card-grid">
                <a href="chapters.html" class="card">
                    <h3 class="card-title">📚 All Chapters</h3>
                    <p class="card-subtitle">View all chapters and their blocks</p>
                </a>
                <a href="timeline.html" class="card">
                    <h3 class="card-title">📅 Timeline</h3>
                    <p class="card-subtitle">Project roadmap and milestones</p>
                </a>
                <a href="about.html" class="card">
                    <h3 class="card-title">ℹ️ About</h3>
                    <p class="card-subtitle">Information about this project</p>
                </a>
            </div>
        </main>
    </div>
</body>
</html>
'''

with open(f"{BASE_DIR}/index.html", "w") as f:
    f.write(index_html)
print("✅ index.html gegenereerd")

# Genereer chapters.html
chapters_html = f'''<!DOCTYPE html>
<html lang="en" data-theme="gold" data-mode="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chapters - ARC Strategic Control Center</title>
    <link rel="stylesheet" href="css/arc-scc.css">
    <script src="js/arc-scc.js" defer></script>
</head>
<body>
    <div class="app-container">
        {generate_topbar()}
        {generate_sidebar()}
        <main class="main-content">
            <div class="breadcrumbs">
                <a href="index.html">Dashboard</a>
                <span>/</span>
                <span>Chapters</span>
            </div>
            
            <div class="page-header">
                <h1 class="page-title">Chapters</h1>
                <p class="page-subtitle">All 8 chapters with their blocks</p>
            </div>
            
            <div class="chapter-list">
'''

for chapter in CHAPTERS:
    chapters_html += f'''
                <div id="{chapter["id"]}" class="chapter-item">
                    <div class="chapter-item-header">
                        <a href="#" class="chapter-item-title">{chapter["title"]}</a>
                        <span class="chapter-item-meta">{len(chapter["blocks"])} blocks</span>
                    </div>
                    <p style="color: var(--text-muted); margin-bottom: 1rem;">Chapter blocks:</p>
                    <div class="chapter-blocks-preview">
'''
    for block in chapter["blocks"]:
        chapters_html += f'                        <a href="block_{block["id"]}.html" class="block-tag">{block["id"]}: {block["title"]}</a>\n'
    
    chapters_html += '''                    </div>
                </div>
'''

chapters_html += '''
            </div>
        </main>
    </div>
</body>
</html>
'''

with open(f"{BASE_DIR}/chapters.html", "w") as f:
    f.write(chapters_html)
print("✅ chapters.html gegenereerd")

# Genereer about.html en timeline.html (korte versies)
about_html = f'''<!DOCTYPE html>
<html lang="en" data-theme="gold" data-mode="dark">
<head>
    <meta charset="UTF-8">
    <title>About - ARC Strategic Control Center</title>
    <link rel="stylesheet" href="css/arc-scc.css">
    <script src="js/arc-scc.js" defer></script>
</head>
<body>
    <div class="app-container">
        {generate_topbar()}
        {generate_sidebar()}
        <main class="main-content">
            <div class="breadcrumbs">
                <a href="index.html">Dashboard</a>
                <span>/</span>
                <span>About</span>
            </div>
            <div class="page-header">
                <h1 class="page-title">About ARC Strategic Control Center</h1>
            </div>
            <div class="block-content">
                <p>Comprehensive documentation and architecture platform covering 8 chapters with 54 blocks.</p>
                <div class="card-grid" style="margin-top: 2rem;">
                    <div class="card"><h3 class="card-title">8</h3><p class="card-subtitle">Chapters</p></div>
                    <div class="card"><h3 class="card-title">54</h3><p class="card-subtitle">Blocks</p></div>
                    <div class="card"><h3 class="card-title">4</h3><p class="card-subtitle">Themes</p></div>
                </div>
            </div>
        </main>
    </div>
</body>
</html>
'''

with open(f"{BASE_DIR}/about.html", "w") as f:
    f.write(about_html)

# Genereer ALLE block pagina's
all_blocks = [b for ch in CHAPTERS for b in ch["blocks"]]

for i, block in enumerate(all_blocks):
    block_id = block["id"]
    title = block["title"]
    block_type = block["type"]
    chapter = next(ch for ch in CHAPTERS if any(b["id"] == block_id for b in ch["blocks"]))
    chapter_title = chapter["title"]
    
    prev_block = all_blocks[i - 1] if i > 0 else None
    next_block = all_blocks[i + 1] if i < len(all_blocks) - 1 else None
    
    content = generate_block_content(block, chapter_title)
    
    block_html = f'''<!DOCTYPE html>
<html lang="en" data-theme="gold" data-mode="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} ({block_id}) - ARC Strategic Control Center</title>
    <link rel="stylesheet" href="css/arc-scc.css">
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
    <script src="js/arc-scc.js" defer></script>
</head>
<body>
    <div class="app-container">
        {generate_topbar()}
        {generate_sidebar(active_block=block_id)}
        <main class="main-content">
            <div class="breadcrumbs">
                <a href="index.html">Dashboard</a>
                <span>/</span>
                <a href="chapters.html">Chapters</a>
                <span>/</span>
                <a href="chapters.html#{chapter["id"]}">{chapter_title}</a>
                <span>/</span>
                <span>{title}</span>
            </div>
            
            <div class="block-container">
                <div class="block-header">
                    <span class="block-id-badge">{block_id}</span>
                    <h1 class="block-title-large">{title}</h1>
                    <span class="block-type-badge">{block_type}</span>
                </div>
                
                <div class="block-content" id="block-content" data-block-id="{block_id}">
                    {content}
                </div>
                
                <div class="block-nav">
                    {f'<a href="block_{prev_block["id"]}.html">← {prev_block["title"]}</a>' if prev_block else '<a href="#"></a>'}
                    {f'<a href="block_{next_block["id"]}.html">{next_block["title"]} →</a>' if next_block else '<a href="#"></a>'}
                </div>
            </div>
        </main>
    </div>
</body>
</html>
'''
    
    with open(f"{BASE_DIR}/block_{block_id}.html", "w") as f:
        f.write(block_html)

print(f"✅ {len(all_blocks)} block pagina's gegenereerd")
print(f"\n🎉 COMPLETE WEBSITE GEGENEREERD in {BASE_DIR}")
print("=" * 60)
print("Start de server:")
print("  cd ~/arc_strategic_control_center/output && python3 -m http.server 8888")
print("\nOpen in Chrome:")
print("  google-chrome http://localhost:8888/")
print("=" * 60)
