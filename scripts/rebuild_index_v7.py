#!/usr/bin/env python3
import json
import os

# Create directories
os.makedirs('~/arc_ai_angels/website/data', exist_ok=True)
os.makedirs('~/arc_ai_angels/website/chapters', exist_ok=True)

# Complete chapters data with ALL blocks
chapters_data = {
    "chapters": [
        {
            "id": "intro",
            "title": "Introductie",
            "color": "#3B82F6",
            "description": "Wat is Arc AI Angels en waarom OpenClaw?",
            "completed": True,
            "blocks": [
                {"id": "intro-1", "title": "Wat is Arc AI Angels?", "completed": True},
                {"id": "intro-2", "title": "Waarom OpenClaw kiezen?", "completed": True},
                {"id": "intro-3", "title": "Architectuur overzicht", "completed": True}
            ]
        },
        {
            "id": "platform",
            "title": "Platform & Runtime",
            "color": "#8B5CF6",
            "description": "OpenClaw installatie & AI agents beheren op je eigen systeem",
            "completed": True,
            "blocks": [
                {"id": "plat-1", "title": "Systeem vereisten", "completed": True},
                {"id": "plat-2", "title": "Docker & Podman setup", "completed": True},
                {"id": "plat-3", "title": "OpenClaw installatie", "completed": True},
                {"id": "plat-4", "title": "Runtime configuratie", "completed": True},
                {"id": "plat-5", "title": "Agent deployment", "completed": True},
                {"id": "plat-6", "title": "Monitoring & logging", "completed": True}
            ]
        },
        {
            "id": "agents",
            "title": "AI Agents",
            "color": "#10B981",
            "description": "Verschillende agent types en hun mogelijkheden",
            "completed": False,
            "blocks": [
                {"id": "agent-1", "title": "Code agents", "completed": True},
                {"id": "agent-2", "title": "Research agents", "completed": True},
                {"id": "agent-3", "title": "Creative agents", "completed": False},
                {"id": "agent-4", "title": "Analysis agents", "completed": False}
            ]
        },
        {
            "id": "orchestration",
            "title": "Orchestratie",
            "color": "#F59E0B",
            "description": "Multi-agent workflows en samenwerking",
            "completed": False,
            "blocks": [
                {"id": "orch-1", "title": "Workflow design", "completed": True},
                {"id": "orch-2", "title": "Agent communicatie", "completed": False},
                {"id": "orch-3", "title": "Task scheduling", "completed": False},
                {"id": "orch-4", "title": "Foutafhandeling", "completed": False}
            ]
        },
        {
            "id": "security",
            "title": "Security & Privacy",
            "color": "#EF4444",
            "description": "Veilige AI deployment en data bescherming",
            "completed": False,
            "blocks": [
                {"id": "sec-1", "title": "Lokale processing", "completed": True},
                {"id": "sec-2", "title": "API key management", "completed": False},
                {"id": "sec-3", "title": "Data isolatie", "completed": False},
                {"id": "sec-4", "title": "Audit logging", "completed": False}
            ]
        },
        {
            "id": "advanced",
            "title": "Advanced Topics",
            "color": "#EC4899",
            "description": "Geavanceerde configuraties en tuning",
            "completed": False,
            "blocks": [
                {"id": "adv-1", "title": "Custom models", "completed": False},
                {"id": "adv-2", "title": "Performance tuning", "completed": False},
                {"id": "adv-3", "title": "Integration patterns", "completed": False}
            ]
        }
    ]
}

# Write progress.json
with open(os.path.expanduser('~/arc_ai_angels/website/data/progress.json'), 'w') as f:
    json.dump(chapters_data, f, indent=2)

# Calculate totals
total_blocks = sum(len(c["blocks"]) for c in chapters_data["chapters"])
completed_blocks = sum(sum(1 for b in c["blocks"] if b["completed"]) for c in chapters_data["chapters"])
completed_chapters = sum(1 for c in chapters_data["chapters"] if c["completed"])

# Generate index.html
html_content = '''<!DOCTYPE html>
<html lang="nl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Arc AI Angels - Strategisch Architectuur Platform</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-primary: #0f172a;
            --bg-secondary: #1e293b;
            --bg-tertiary: #334155;
            --text-primary: #f8fafc;
            --text-secondary: #94a3b8;
            --accent: #3b82f6;
        }
        
        body {
            font-family: 'Inter', sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
        }
        
        .font-mono { font-family: 'JetBrains Mono', monospace; }
        
        /* Custom Scrollbar */
        ::-webkit-scrollbar { width: 8px; height: 8px; }
        ::-webkit-scrollbar-track { background: var(--bg-secondary); }
        ::-webkit-scrollbar-thumb { background: var(--bg-tertiary); border-radius: 4px; }
        ::-webkit-scrollbar-thumb:hover { background: #475569; }
        
        /* Glassmorphism */
        .glass {
            background: rgba(30, 41, 59, 0.7);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .glass-strong {
            background: rgba(15, 23, 42, 0.9);
            backdrop-filter: blur(16px);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        /* Glow effects */
        .glow { box-shadow: 0 0 20px rgba(59, 130, 246, 0.3); }
        .glow-text { text-shadow: 0 0 30px rgba(59, 130, 246, 0.5); }
        
        /* Chapter hover effects */
        .chapter-item {
            transition: all 0.3s ease;
            border-left: 3px solid transparent;
        }
        
        .chapter-item:hover {
            background: rgba(255, 255, 255, 0.05);
            transform: translateX(4px);
        }
        
        .chapter-item.active {
            background: rgba(255, 255, 255, 0.1);
            border-left-color: var(--accent);
        }
        
        /* Block styles */
        .block-link {
            transition: all 0.2s ease;
            border-radius: 6px;
        }
        
        .block-link:hover {
            background: rgba(255, 255, 255, 0.1);
            transform: translateX(8px);
        }
        
        .block-completed {
            opacity: 0.6;
            text-decoration: line-through;
        }
        
        /* Progress bars */
        .progress-bar {
            background: linear-gradient(90deg, var(--chapter-color, #3b82f6) 0%, rgba(59, 130, 246, 0.3) 100%);
            height: 4px;
            border-radius: 2px;
            transition: width 0.5s ease;
        }
        
        /* Mermaid */
        .mermaid {
            background: transparent !important;
        }
        
        .mermaid svg {
            max-width: 100%;
            height: auto;
        }
        
        /* Theme picker */
        .theme-picker {
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 1000;
        }
        
        .theme-btn {
            width: 32px;
            height: 32px;
            border-radius: 50%;
            border: 2px solid rgba(255, 255, 255, 0.3);
            cursor: pointer;
            transition: all 0.2s;
        }
        
        .theme-btn:hover { transform: scale(1.1); border-color: white; }
        .theme-btn.active { border-color: white; box-shadow: 0 0 10px currentColor; }
        
        /* Chapter color hover effects */
        .chapter-header:hover {
            filter: brightness(1.3);
        }
        
        /* Compact Arc AI Angels block */
        .arc-ai-angels-compact {
            background: linear-gradient(135deg, rgba(59, 130, 246, 0.2) 0%, rgba(139, 92, 246, 0.2) 100%);
            border: 1px solid rgba(59, 130, 246, 0.3);
        }
        
        /* Grid background */
        .grid-bg {
            background-image: 
                linear-gradient(rgba(59, 130, 246, 0.1) 1px, transparent 1px),
                linear-gradient(90deg, rgba(59, 130, 246, 0.1) 1px, transparent 1px);
            background-size: 50px 50px;
        }
    </style>
</head>
<body class="min-h-screen grid-bg">
    <!-- Theme Picker -->
    <div class="theme-picker glass rounded-full p-2 flex gap-2">
        <button class="theme-btn active" style="background: #0f172a;" onclick="setTheme('dark')" title="Dark"></button>
        <button class="theme-btn" style="background: #f8fafc;" onclick="setTheme('light')" title="Light"></button>
        <button class="theme-btn" style="background: #1e1b4b;" onclick="setTheme('midnight')" title="Midnight"></button>
        <button class="theme-btn" style="background: #064e3b;" onclick="setTheme('forest')" title="Forest"></button>
    </div>

    <div class="flex h-screen overflow-hidden">
        <!-- Sidebar -->
        <aside class="w-80 glass-strong flex flex-col overflow-hidden">
            <!-- Logo -->
            <div class="p-6 border-b border-white/10">
                <h1 class="text-2xl font-bold font-mono glow-text bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
                    Arc AI Angels
                </h1>
                <p class="text-xs text-gray-400 mt-1">Strategisch Architectuur Platform</p>
            </div>
            
            <!-- Arc AI Angels Compact Block -->
            <div class="arc-ai-angels-compact p-4 m-4 rounded-lg">
                <div class="flex items-center gap-3 mb-2">
                    <div class="w-8 h-8 rounded-lg bg-blue-500/20 flex items-center justify-center">
                        <svg class="w-5 h-5 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/>
                        </svg>
                    </div>
                    <div>
                        <h3 class="font-semibold text-sm text-blue-300">Arc AI Angels</h3>
                        <p class="text-xs text-gray-400">OpenClaw installatie & AI agents beheren op je eigen systeem</p>
                    </div>
                </div>
                <div class="flex gap-2 mt-2">
                    <span class="text-xs px-2 py-1 rounded bg-blue-500/20 text-blue-300">Self-hosted</span>
                    <span class="text-xs px-2 py-1 rounded bg-purple-500/20 text-purple-300">Multi-agent</span>
                </div>
            </div>
            
            <!-- Navigation -->
            <nav class="flex-1 overflow-y-auto p-4 space-y-2" id="sidebar-nav">
                <!-- Chapters will be loaded here -->
            </nav>
            
            <!-- Total Progress -->
            <div class="p-4 border-t border-white/10">
                <div class="flex justify-between text-sm mb-2">
                    <span class="text-gray-400">Totale Voortgang</span>
                    <span class="font-mono text-blue-400" id="total-percentage">0%</span>
                </div>
                <div class="h-2 bg-gray-700 rounded-full overflow-hidden">
                    <div class="h-full bg-gradient-to-r from-blue-500 to-purple-500 transition-all duration-500" 
                         id="total-progress" style="width: 0%"></div>
                </div>
                <div class="flex justify-between text-xs text-gray-500 mt-2">
                    <span id="completed-chapters">0 chapters</span>
                    <span id="completed-blocks">0 blocks</span>
                </div>
            </div>
        </aside>

        <!-- Main Content -->
        <main class="flex-1 overflow-y-auto">
            <!-- Hero -->
            <section class="relative py-16 px-8 border-b border-white/10">
                <div class="max-w-6xl mx-auto">
                    <div class="flex items-center gap-4 mb-6">
                        <div class="w-16 h-16 rounded-2xl bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center glow">
                            <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                                      d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"/>
                            </svg>
                        </div>
                        <div>
                            <h1 class="text-5xl font-bold font-mono glow-text">Arc AI Angels</h1>
                            <p class="text-xl text-gray-400 mt-2">Strategisch Architectuur Platform voor AI Agent Orchestration</p>
                        </div>
                    </div>
                    
                    <p class="text-gray-300 max-w-3xl leading-relaxed">
                        Een compleet framework voor het opzetten, beheren en orchestreren van AI agents op je eigen infrastructuur. 
                        Gebruikmakend van OpenClaw voor maximale controle, privacy en flexibiliteit.
                    </p>
                </div>
            </section>

            <!-- Two Column Layout -->
            <section class="p-8">
                <div class="max-w-6xl mx-auto grid md:grid-cols-2 gap-8">
                    <!-- Arc Control Center -->
                    <div class="glass rounded-2xl p-6">
                        <div class="flex items-center gap-3 mb-4">
                            <div class="w-10 h-10 rounded-xl bg-cyan-500/20 flex items-center justify-center">
                                <svg class="w-5 h-5 text-cyan-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                                </svg>
                            </div>
                            <h2 class="text-2xl font-bold">Arc Control Center</h2>
                        </div>
                        <p class="text-gray-400 mb-6">Documentatie en architectuur overzicht</p>
                        
                        <div class="space-y-3" id="control-center-chapters">
                            <!-- Chapter progress blocks -->
                        </div>
                    </div>

                    <!-- Arc AI Angels -->
                    <div class="glass rounded-2xl p-6">
                        <div class="flex items-center gap-3 mb-4">
                            <div class="w-10 h-10 rounded-xl bg-purple-500/20 flex items-center justify-center">
                                <svg class="w-5 h-5 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/>
                                </svg>
                            </div>
                            <h2 class="text-2xl font-bold">Arc AI Angels</h2>
                        </div>
                        <p class="text-gray-400 mb-6">OpenClaw focus - Self-hosted AI agents</p>
                        
                        <div class="space-y-3" id="ai-angels-chapters">
                            <!-- Chapter progress blocks -->
                        </div>
                    </div>
                </div>
            </section>

            <!-- Mermaid Diagrams -->
            <section class="p-8 border-t border-white/10">
                <div class="max-w-6xl mx-auto">
                    <h2 class="text-3xl font-bold mb-8 font-mono">Architectuur Diagrammen</h2>
                    
                    <div class="grid md:grid-cols-2 gap-8">
                        <!-- Agent Flow -->
                        <div class="glass rounded-2xl p-6">
                            <h3 class="text-lg font-semibold mb-4 text-blue-400">Agent Flow</h3>
                            <div class="mermaid">
%%{init: {'theme': 'dark', 'themeVariables': { 'primaryColor': '#3b82f6', 'primaryTextColor': '#fff', 'primaryBorderColor': '#3b82f6', 'lineColor': '#64748b', 'secondaryColor': '#8b5cf6', 'tertiaryColor': '#10b981'}}}%%
flowchart TB
    A[User Request] --> B{Orchestrator}
    B --> C[Code Agent]
    B --> D[Research Agent]
    B --> E[Creative Agent]
    C --> F[Result Aggregator]
    D --> F
    E --> F
    F --> G[Response]
                            </div>
                        </div>

                        <!-- System Layers -->
                        <div class="glass rounded-2xl p-6">
                            <h3 class="text-lg font-semibold mb-4 text-purple-400">Systeem Lagen</h3>
                            <div class="mermaid">
%%{init: {'theme': 'dark', 'themeVariables': { 'primaryColor': '#8b5cf6', 'primaryTextColor': '#fff', 'primaryBorderColor': '#8b5cf6', 'lineColor': '#64748b'}}}%%
graph LR
    A[Presentation] --> B[Orchestration]
    B --> C[Agent Runtime]
    C --> D[Models]
    D --> E[Infrastructure]
    style A fill:#3b82f6
    style B fill:#8b5cf6
    style C fill:#10b981
    style D fill:#f59e0b
    style E fill:#ef4444
                            </div>
                        </div>

                        <!-- Data Flow -->
                        <div class="glass rounded-2xl p-6">
                            <h3 class="text-lg font-semibold mb-4 text-green-400">Data Stroom</h3>
                            <div class="mermaid">
%%{init: {'theme': 'dark'}}%%
flowchart LR
    Input[Input Data] --> Process[Processing]
    Process --> Vector[Vector Store]
    Process --> Cache[Cache Layer]
    Vector --> Output[Output]
    Cache --> Output
                            </div>
                        </div>

                        <!-- Build Sequence -->
                        <div class="glass rounded-2xl p-6">
                            <h3 class="text-lg font-semibold mb-4 text-amber-400">Bouw Volgorde</h3>
                            <div class="mermaid">
%%{init: {'theme': 'dark'}}%%
graph TD
    A[Setup] --> B[Configure]
    B --> C[Deploy]
    C --> D[Test]
    D --> E[Monitor]
    D -.->|Rollback| B
    E --> F[Scale]
                            </div>
                        </div>
                    </div>
                </div>
            </section>
        </main>
    </div>

    <script>
        // Theme management
        const themes = {
            dark: { bg: '#0f172a', secondary: '#1e293b', text: '#f8fafc', accent: '#3b82f6' },
            light: { bg: '#f8fafc', secondary: '#e2e8f0', text: '#0f172a', accent: '#3b82f6' },
            midnight: { bg: '#020617', secondary: '#0f172a', text: '#e2e8f0', accent: '#6366f1' },
            forest: { bg: '#022c22', secondary: '#064e3b', text: '#ecfdf5', accent: '#10b981' }
        };

        function setTheme(themeName) {
            const theme = themes[themeName];
            document.documentElement.style.setProperty('--bg-primary', theme.bg);
            document.documentElement.style.setProperty('--bg-secondary', theme.secondary);
            document.documentElement.style.setProperty('--text-primary', theme.text);
            document.documentElement.style.setProperty('--accent', theme.accent);
            
            document.querySelectorAll('.theme-btn').forEach(btn => btn.classList.remove('active'));
            event.target.classList.add('active');
            
            // Re-render mermaid with new theme
            mermaid.initialize({ theme: themeName === 'light' ? 'default' : 'dark', startOnLoad: true });
            location.reload();
        }

        // Load and render chapters
        async function loadChapters() {
            try {
                const response = await fetch('data/progress.json');
                const data = await response.json();
                const chapters = data.chapters;
                
                // Render sidebar navigation
                const sidebarNav = document.getElementById('sidebar-nav');
                sidebarNav.innerHTML = '';
                
                chapters.forEach(chapter => {
                    const completedCount = chapter.blocks.filter(b => b.completed).length;
                    const totalCount = chapter.blocks.length;
                    const percentage = Math.round((completedCount / totalCount) * 100);
                    
                    // Chapter header with hover effect
                    const chapterDiv = document.createElement('div');
                    chapterDiv.className = 'mb-4';
                    chapterDiv.innerHTML = `
                        <div class="chapter-header cursor-pointer p-3 rounded-lg mb-1 transition-all"
                             style="background: ${chapter.color}20; border-left: 3px solid ${chapter.color};"
                             onclick="toggleChapter('${chapter.id}')">
                            <div class="flex items-center justify-between">
                                <div class="flex items-center gap-2">
                                    <span class="w-2 h-2 rounded-full" style="background: ${chapter.color}"></span>
                                    <span class="font-medium text-sm">${chapter.title}</span>
                                </div>
                                <svg class="w-4 h-4 transform transition-transform chapter-chevron" id="chevron-${chapter.id}" 
                                     fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
                                </svg>
                            </div>
                            <div class="mt-2 flex items-center gap-2">
                                <div class="flex-1 h-1 bg-gray-700 rounded-full overflow-hidden">
                                    <div class="h-full rounded-full" style="width: ${percentage}%; background: ${chapter.color}"></div>
                                </div>
                                <span class="text-xs text-gray-400">${completedCount}/${totalCount}</span>
                            </div>
                        </div>
                        <div id="blocks-${chapter.id}'" class="ml-4 space-y-1 hidden chapter-blocks">
                            <a href="chapters/${chapter.id}.html" class="block-link block p-2 text-xs text-gray-400 hover:text-white rounded flex items-center gap-2">
                                <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h7"/>
                                </svg>
                                Chapter Overview
                            </a>
                            ${chapter.blocks.map(block => `
                                <a href="chapters/${chapter.id}.html#${block.id}" 
                                   class="block-link block p-2 text-xs rounded flex items-center gap-2 ${block.completed ? 'block-completed text-gray-500' : 'text-gray-300 hover:text-white'}">
                                    <span class="w-1.5 h-1.5 rounded-full ${block.completed ? 'bg-green-500' : 'bg-gray-500'}"></span>
                                    ${block.title}
                                </a>
                            `).join('')}
                        </div>
                    `;
                    sidebarNav.appendChild(chapterDiv);
                });
                
                // Render Control Center chapters (first 3)
                const controlCenter = document.getElementById('control-center-chapters');
                chapters.slice(0, 3).forEach(chapter => {
                    const completedCount = chapter.blocks.filter(b => b.completed).length;
                    const totalCount = chapter.blocks.length;
                    controlCenter.innerHTML += createChapterProgressBlock(chapter, completedCount, totalCount);
                });
                
                // Render AI Angels chapters (last 3)
                const aiAngels = document.getElementById('ai-angels-chapters');
                chapters.slice(3).forEach(chapter => {
                    const completedCount = chapter.blocks.filter(b => b.completed).length;
                    const totalCount = chapter.blocks.length;
                    aiAngels.innerHTML += createChapterProgressBlock(chapter, completedCount, totalCount);
                });
                
                // Update totals
                const totalBlocks = chapters.reduce((sum, c) => sum + c.blocks.length, 0);
                const completedBlocks = chapters.reduce((sum, c) => sum + c.blocks.filter(b => b.completed).length, 0);
                const completedChapters = chapters.filter(c => c.completed).length;
                const totalPercentage = Math.round((completedBlocks / totalBlocks) * 100);
                
                document.getElementById('total-percentage').textContent = totalPercentage + '%';
                document.getElementById('total-progress').style.width = totalPercentage + '%';
                document.getElementById('completed-chapters').textContent = completedChapters + ' chapters';
                document.getElementById('completed-blocks').textContent = completedBlocks + '/' + totalBlocks + ' blocks';
                
            } catch (error) {
                console.error('Error loading chapters:', error);
            }
        }
        
        function createChapterProgressBlock(chapter, completed, total) {
            const percentage = Math.round((completed / total) * 100);
            return `
                <div class="p-4 rounded-xl transition-all hover:scale-[1.02] cursor-pointer"
                     style="background: ${chapter.color}15; border: 1px solid ${chapter.color}30;"
                     onclick="location.href='chapters/${chapter.id}.html'">
                    <div class="flex items-center justify-between mb-2">
                        <div class="flex items-center gap-2">
                            <span class="w-3 h-3 rounded-full" style="background: ${chapter.color}"></span>
                            <span class="font-semibold text-sm">${chapter.title}</span>
                        </div>
                        <span class="text-xs font-mono" style="color: ${chapter.color}">${percentage}%</span>
                    </div>
                    <div class="h-2 bg-gray-700 rounded-full overflow-hidden mb-2">
                        <div class="h-full rounded-full transition-all duration-500" 
                             style="width: ${percentage}%; background: ${chapter.color}"></div>
                    </div>
                    <div class="flex justify-between text-xs text-gray-400">
                        <span>${completed} van ${total} blocks</span>
                        <span>${chapter.completed ? '✓ Compleet' : 'In progress'}</span>
                    </div>
                </div>
            `;
        }
        
        function toggleChapter(chapterId) {
            const blocks = document.getElementById(`blocks-${chapterId}'`);
            const chevron = document.getElementById(`chevron-${chapterId}`);
            if (blocks.classList.contains('hidden')) {
                blocks.classList.remove('hidden');
                chevron.style.transform = 'rotate(180deg)';
            } else {
                blocks.classList.add('hidden');
                chevron.style.transform = 'rotate(0deg)';
            }
        }
        
        // Initialize
        document.addEventListener('DOMContentLoaded', () => {
            mermaid.initialize({ 
                theme: 'dark',
                startOnLoad: true,
                securityLevel: 'loose'
            });
            loadChapters();
        });
    </script>
</body>
</html>
'''

# Write index.html
with open(os.path.expanduser('~/arc_ai_angels/website/index.html'), 'w') as f:
    f.write(html_content)

# Generate chapter pages
chapter_template = '''<!DOCTYPE html>
<html lang="nl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - Arc AI Angels</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    <style>
        :root {{
            --chapter-color: {color};
            --bg-primary: #0f172a;
            --bg-secondary: #1e293b;
            --bg-tertiary: #334155;
            --text-primary: #f8fafc;
            --text-secondary: #94a3b8;
        }}
        
        body {{
            font-family: 'Inter', sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
        }}
        
        .font-mono {{ font-family: 'JetBrains Mono', monospace; }}
        
        ::-webkit-scrollbar {{ width: 8px; }}
        ::-webkit-scrollbar-track {{ background: var(--bg-secondary); }}
        ::-webkit-scrollbar-thumb {{ background: var(--bg-tertiary); border-radius: 4px; }}
        
        .glass {{
            background: rgba(30, 41, 59, 0.7);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }}
        
        .glass-strong {{
            background: rgba(15, 23, 42, 0.9);
            backdrop-filter: blur(16px);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }}
        
        .chapter-header {{
            background: linear-gradient(135deg, {color}20 0%, {color}05 100%);
            border: 1px solid {color}40;
        }}
        
        .block-card {{
            background: {color}10;
            border: 1px solid {color}30;
            transition: all 0.3s ease;
        }}
        
        .block-card:hover {{
            background: {color}20;
            border-color: {color}60;
            transform: translateY(-2px);
        }}
        
        .block-completed {{
            opacity: 0.6;
            border-color: #10b981;
        }}
        
        .mermaid svg {{
            max-width: 100%;
            height: auto;
        }}
        
        .grid-bg {{
            background-image: 
                linear-gradient(rgba(59, 130, 246, 0.05) 1px, transparent 1px),
                linear-gradient(90deg, rgba(59, 130, 246, 0.05) 1px, transparent 1px);
            background-size: 50px 50px;
        }}
        
        .progress-ring {{
            transform: rotate(-90deg);
        }}
        
        .progress-ring-circle {{
            transition: stroke-dashoffset 0.5s ease;
        }}
        
        /* Chapter color accents */
        .text-chapter {{ color: {color}; }}
        .bg-chapter {{ background-color: {color}; }}
        .border-chapter {{ border-color: {color}; }}
        
        /* Hover brightness for chapter color */
        .hover-chapter:hover {{
            filter: brightness(1.3);
        }}
    </style>
</head>
<body class="min-h-screen grid-bg">
    <div class="flex h-screen overflow-hidden">
        <!-- Sidebar - Same as index.html -->
        <aside class="w-80 glass-strong flex flex-col overflow-hidden">
            <div class="p-6 border-b border-white/10">
                <a href="../index.html" class="text-2xl font-bold font-mono glow-text bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent hover:opacity-80 transition-opacity">
                    Arc AI Angels
                </a>
                <p class="text-xs text-gray-400 mt-1">Strategisch Architectuur Platform</p>
            </div>
            
            <nav class="flex-1 overflow-y-auto p-4 space-y-2" id="sidebar-nav">
                <!-- Chapters loaded via JS -->
            </nav>
            
            <div class="p-4 border-t border-white/10">
                <a href="../index.html" class="flex items-center gap-2 text-sm text-gray-400 hover:text-white transition-colors">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"/>
                    </svg>
                    Terug naar overzicht
                </a>
            </div>
        </aside>

        <!-- Main Content -->
        <main class="flex-1 overflow-y-auto">
            <!-- Chapter Header -->
            <section class="chapter-header p-8 border-b border-white/10">
                <div class="max-w-6xl mx-auto">
                    <div class="flex items-center gap-4 mb-4">
                        <div class="w-12 h-12 rounded-xl flex items-center justify-center" style="background: {color}30;">
                            <span class="text-2xl font-bold" style="color: {color};">{index}</span>
                        </div>
                        <div>
                            <h1 class="text-4xl font-bold font-mono" style="color: {color};">{title}</h1>
                            <p class="text-gray-400 mt-1">{description}</p>
                        </div>
                    </div>
                    
                    <div class="flex items-center gap-6 mt-6">
                        <div class="flex items-center gap-2">
                            <div class="w-32 h-2 bg-gray-700 rounded-full overflow-hidden">
                                <div class="h-full rounded-full transition-all duration-500" 
                                     style="width: {percentage}%; background: {color};"></div>
                            </div>
                            <span class="text-sm font-mono" style="color: {color};">{percentage}%</span>
                        </div>
                        <span class="text-sm text-gray-400">{completed_blocks} van {total_blocks} blocks voltooid</span>
                        {completed_badge}
                    </div>
                </div>
            </section>

            <!-- Blocks Grid -->
            <section class="p-8">
                <div class="max-w-6xl mx-auto">
                    <h2 class="text-2xl font-bold mb-6 font-mono">Blocks</h2>
                    <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
                        {blocks_html}
                    </div>
                </div>
            </section>

            <!-- Chapter Diagram (if applicable) -->
            {diagram_section}
        </main>
    </div>

    <script>
        // Load sidebar chapters
        async function loadSidebar() {{
            try {{
                const response = await fetch('../data/progress.json');
                const data = await response.json();
                const sidebarNav = document.getElementById('sidebar-nav');
                
                data.chapters.forEach(chapter => {{
                    const isActive = chapter.id === '{id}';
                    const completedCount = chapter.blocks.filter(b => b.completed).length;
                    const totalCount = chapter.blocks.length;
                    
                    const div = document.createElement('div');
                    div.className = 'chapter-item rounded-lg mb-1 ' + (isActive ? 'active' : '');
                    div.innerHTML = `
                        <a href="${{chapter.id}}.html" class="block p-3 rounded-lg" 
                           style="background: ${{isActive ? chapter.color + '30' : 'transparent'}}; 
                                  border-left: 3px solid ${{isActive ? chapter.color : 'transparent'}};">
                            <div class="flex items-center gap-2 mb-2">
                                <span class="w-2 h-2 rounded-full" style="background: ${{chapter.color}}"></span>
                                <span class="font-medium text-sm ${{isActive ? 'text-white' : 'text-gray-400'}}">${{chapter.title}}</span>
                            </div>
                            <div class="flex items-center gap-2">
                                <div class="flex-1 h-1 bg-gray-700 rounded-full">
                                    <div class="h-full rounded-full" 
                                         style="width: ${{Math.round((completedCount/totalCount)*100)}}%; background: ${{chapter.color}}"></div>
                                </div>
                                <span class="text-xs text-gray-500">${{completedCount}}/${{totalCount}}</span>
                            </div>
                        </a>
                    `;
                    sidebarNav.appendChild(div);
                }});
            }} catch (error) {{
                console.error('Error loading sidebar:', error);
            }}
        }}
        
        // Initialize mermaid
        document.addEventListener('DOMContentLoaded', () => {{
            mermaid.initialize({{ 
                theme: 'dark',
                startOnLoad: true,
                securityLevel: 'loose'
            }});
            loadSidebar();
        }});
    </script>
</body>
</html>
'''

# Generate each chapter page
for idx, chapter in enumerate(chapters_data['chapters'], 1):
    completed = sum(1 for b in chapter['blocks'] if b['completed'])
    total = len(chapter['blocks'])
    percentage = round((completed / total) * 100) if total > 0 else 0
    
    # Generate blocks HTML
    blocks_html = ''
    for block in chapter['blocks']:
        status_class = 'block-completed' if block['completed'] else ''
        status_icon = '✓' if block['completed'] else '○'
        status_color = '#10b981' if block['completed'] else chapter['color']
        
        # Determine if this block should have a diagram
        diagram_html = ''
        if chapter['id'] == 'platform' and block['id'] == 'plat-3':
            diagram_html = '''
            <div class="mt-4 p-4 bg-black/20 rounded-lg">
                <div class="mermaid">
flowchart TB
    A[Download OpenClaw] --> B[Configure Environment]
    B --> C[Start Services]
    C --> D[Verify Installation]
                </div>
            </div>'''
        elif chapter['id'] == 'agents' and block['id'] == 'agent-1':
            diagram_html = '''
            <div class="mt-4 p-4 bg-black/20 rounded-lg">
                <div class="mermaid">
flowchart LR
    A[Code Input] --> B[LLM Analysis]
    B --> C[Code Generation]
    C --> D[Review & Test]
                </div>
            </div>'''
        
        blocks_html += f'''
        <div class="block-card {status_class} rounded-xl p-6" id="{block['id']}">
            <div class="flex items-start justify-between mb-4">
                <div class="w-10 h-10 rounded-lg flex items-center justify-center text-lg font-bold"
                     style="background: {status_color}20; color: {status_color};">
                    {status_icon}
                </div>
                <span class="text-xs px-2 py-1 rounded bg-gray-700 text-gray-300">
                    {block['id']}
                </span>
            </div>
            <h3 class="text-lg font-semibold mb-2">{block['title']}</h3>
            <p class="text-sm text-gray-400 mb-4">
                {'Dit block is voltooid en bevat alle benodigde documentatie en voorbeelden.' if block['completed'] else 'Dit block is nog in ontwikkeling. Check later voor updates.'}
            </p>
            {diagram_html}
            <div class="mt-4 pt-4 border-t border-white/10 flex justify-between items-center">
                <span class="text-xs text-gray-500">{'Voltooid' if block['completed'] else 'In progress'}</span>
                <button class="text-sm px-4 py-2 rounded-lg transition-all hover:opacity-80"
                        style="background: {chapter['color']}20; color: {chapter['color']}; border: 1px solid {chapter['color']}40;">
                    {'Herbekijk' if block['completed'] else 'Start'}
                </button>
            </div>
        </div>
        '''

    # Determine if chapter needs a diagram section
    diagram_section = ''
    if chapter['id'] == 'platform':
        diagram_section = '''
            <section class="p-8 border-t border-white/10">
                <div class="max-w-6xl mx-auto">
                    <h2 class="text-2xl font-bold mb-6 font-mono">Platform Architectuur</h2>
                    <div class="glass rounded-2xl p-6">
                        <div class="mermaid">
%%{init: {'theme': 'dark'}}%%
graph TB
    subgraph "User Layer"
        A[Web Interface]
        B[CLI Tool]
    end
    
    subgraph "Orchestration Layer"
        C[OpenClaw Core]
        D[Agent Manager]
    end
    
    subgraph "Runtime Layer"
        E[Docker Containers]
        F[Model Endpoints]
    end
    
    subgraph "Storage Layer"
        G[Vector DB]
        H[File System]
    end
    
    A --> C
    B --> C
    C --> D
    D --> E
    D --> F
    E --> G
    E --> H
                        </div>
                    </div>
                </div>
            </section>
        '''
    elif chapter['id'] == 'orchestration':
        diagram_section = '''
            <section class="p-8 border-t border-white/10">
                <div class="max-w-6xl mx-auto">
                    <h2 class="text-2xl font-bold mb-6 font-mono">Orchestratie Flow</h2>
                    <div class="glass rounded-2xl p-6">
                        <div class="mermaid">
%%{init: {'theme': 'dark'}}%%
sequenceDiagram
    participant U as User
    participant O as Orchestrator
    participant A1 as Agent 1
    participant A2 as Agent 2
    participant S as Store
    
    U->>O: Submit Task
    O->>O: Analyze & Plan
    O->>A1: Assign Sub-task
    A1->>S: Query Data
    S-->>A1: Return Data
    A1-->>O: Result 1
    O->>A2: Assign Next Task
    A2-->>O: Result 2
    O->>O: Aggregate
    O-->>U: Final Response
                        </div>
                    </div>
                </div>
            </section>
        '''

    completed_badge = '<span class="px-3 py-1 rounded-full bg-green-500/20 text-green-400 text-sm font-medium border border-green-500/30">✓ Chapter Compleet</span>' if chapter['completed'] else ''

    chapter_html = chapter_template.format(
        id=chapter['id'],
        title=chapter['title'],
        description=chapter['description'],
        color=chapter['color'],
        index=idx,
        percentage=percentage,
        completed_blocks=completed,
        total_blocks=total,
        blocks_html=blocks_html,
        diagram_section=diagram_section,
        completed_badge=completed_badge
    )
    
    with open(os.path.expanduser(f'~/arc_ai_angels/website/chapters/{chapter["id"]}.html'), 'w') as f:
        f.write(chapter_html)

# Generate chapters index page (overview)
chapters_index_html = '''<!DOCTYPE html>
<html lang="nl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Alle Chapters - Arc AI Angels</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-primary: #0f172a;
            --bg-secondary: #1e293b;
            --bg-tertiary: #334155;
            --text-primary: #f8fafc;
            --text-secondary: #94a3b8;
        }
        
        body {
            font-family: 'Inter', sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
        }
        
        .font-mono { font-family: 'JetBrains Mono', monospace; }
        
        ::-webkit-scrollbar { width: 8px; }
        ::-webkit-scrollbar-track { background: var(--bg-secondary); }
        ::-webkit-scrollbar-thumb { background: var(--bg-tertiary); border-radius: 4px; }
        
        .glass {
            background: rgba(30, 41, 59, 0.7);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .chapter-card {
            transition: all 0.3s ease;
        }
        
        .chapter-card:hover {
            transform: translateY(-4px);
        }
        
        .block-mini {
            transition: all 0.2s ease;
        }
        
        .block-mini:hover {
            transform: translateX(4px);
        }
        
        .grid-bg {
            background-image: 
                linear-gradient(rgba(59, 130, 246, 0.05) 1px, transparent 1px),
                linear-gradient(90deg, rgba(59, 130, 246, 0.05) 1px, transparent 1px);
            background-size: 50px 50px;
        }
    </style>
</head>
<body class="min-h-screen grid-bg">
    <div class="flex h-screen overflow-hidden">
        <!-- Sidebar -->
        <aside class="w-80 glass flex flex-col overflow-hidden border-r border-white/10">
            <div class="p-6 border-b border-white/10">
                <a href="index.html" class="text-2xl font-bold font-mono glow-text bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent hover:opacity-80 transition-opacity">
                    Arc AI Angels
                </a>
                <p class="text-xs text-gray-400 mt-1">Strategisch Architectuur Platform</p>
            </div>
            
            <nav class="flex-1 overflow-y-auto p-4 space-y-2" id="sidebar-nav">
                <!-- Loaded via JS -->
            </nav>
            
            <div class="p-4 border-t border-white/10">
                <div class="text-xs text-gray-500 text-center">
                    Arc AI Angels v1.0
                </div>
            </div>
        </aside>

        <!-- Main Content -->
        <main class="flex-1 overflow-y-auto p-8">
            <div class="max-w-7xl mx-auto">
                <!-- Header -->
                <div class="mb-8">
                    <h1 class="text-4xl font-bold font-mono mb-2">Alle Chapters & Blocks</h1>
                    <p class="text-gray-400">Compleet overzicht van het Arc AI Angels curriculum</p>
                </div>

                <!-- Stats -->
                <div class="grid grid-cols-4 gap-4 mb-8">
                    <div class="glass rounded-xl p-4 text-center">
                        <div class="text-3xl font-bold text-blue-400" id="stat-chapters">6</div>
                        <div class="text-sm text-gray-400">Chapters</div>
                    </div>
                    <div class="glass rounded-xl p-4 text-center">
                        <div class="text-3xl font-bold text-purple-400" id="stat-blocks">0</div>
                        <div class="text-sm text-gray-400">Total Blocks</div>
                    </div>
                    <div class="glass rounded-xl p-4 text-center">
                        <div class="text-3xl font-bold text-green-400" id="stat-completed">0</div>
                        <div class="text-sm text-gray-400">Voltooid</div>
                    </div>
                    <div class="glass rounded-xl p-4 text-center">
                        <div class="text-3xl font-bold text-amber-400" id="stat-progress">0%</div>
                        <div class="text-sm text-gray-400">Voortgang</div>
                    </div>
                </div>

                <!-- Chapters Grid -->
                <div id="chapters-container" class="grid lg:grid-cols-2 xl:grid-cols-3 gap-6">
                    <!-- Chapters loaded via JS -->
                </div>
            </div>
        </main>
    </div>

    <script>
        async function loadChapters() {
            try {
                const response = await fetch('data/progress.json');
                const data = await response.json();
                const container = document.getElementById('chapters-container');
                const sidebarNav = document.getElementById('sidebar-nav');
                
                let totalBlocks = 0;
                let completedBlocks = 0;
                
                data.chapters.forEach((chapter, idx) => {
                    const chapterCompleted = chapter.blocks.filter(b => b.completed).length;
                    const chapterTotal = chapter.blocks.length;
                    const percentage = Math.round((chapterCompleted / chapterTotal) * 100);
                    
                    totalBlocks += chapterTotal;
                    completedBlocks += chapterCompleted;
                    
                    // Main card
                    const card = document.createElement('div');
                    card.className = 'chapter-card glass rounded-2xl overflow-hidden';
                    card.innerHTML = `
                        <div class="p-6" style="background: linear-gradient(135deg, ${chapter.color}20 0%, transparent 100%);">
                            <div class="flex items-center justify-between mb-4">
                                <div class="flex items-center gap-3">
                                    <div class="w-12 h-12 rounded-xl flex items-center justify-center text-xl font-bold"
                                         style="background: ${chapter.color}30; color: ${chapter.color};">
                                        ${idx + 1}
                                    </div>
                                    <div>
                                        <h2 class="text-xl font-bold" style="color: ${chapter.color};">${chapter.title}</h2>
                                        <p class="text-xs text-gray-400">${chapter.description}</p>
                                    </div>
                                </div>
                                <div class="text-right">
                                    <div class="text-2xl font-bold font-mono" style="color: ${chapter.color};">${percentage}%</div>
                                    <div class="text-xs text-gray-500">${chapterCompleted}/${chapterTotal} blocks</div>
                                </div>
                            </div>
                            
                            <div class="h-2 bg-gray-700 rounded-full overflow-hidden mb-4">
                                <div class="h-full rounded-full transition-all duration-500" 
                                     style="width: ${percentage}%; background: ${chapter.color};"></div>
                            </div>
                            
                            <div class="space-y-1 max-h-48 overflow-y-auto">
                                ${chapter.blocks.map(block => `
                                    <a href="${chapter.id}.html#${block.id}" 
                                       class="block-mini flex items-center gap-3 p-2 rounded-lg ${block.completed ? 'opacity-60' : ''}"
                                       style="background: ${chapter.color}10; border-left: 3px solid ${block.completed ? '#10b981' : chapter.color};">
                                        <span class="w-2 h-2 rounded-full" style="background: ${block.completed ? '#10b981' : chapter.color};"></span>
                                        <span class="text-sm ${block.completed ? 'line-through text-gray-500' : 'text-gray-300'}">${block.title}</span>
                                        ${block.completed ? '<span class="ml-auto text-green-500 text-xs">✓</span>' : ''}
                                    </a>
                                `).join('')}
                            </div>
                            
                            <div class="mt-4 pt-4 border-t border-white/10 flex justify-between items-center">
                                <span class="text-xs text-gray-500">${chapter.completed ? '✓ Chapter compleet' : 'In progress'}</span>
                                <a href="${chapter.id}.html" class="px-4 py-2 rounded-lg text-sm font-medium transition-all hover:opacity-80"
                                   style="background: ${chapter.color}20; color: ${chapter.color}; border: 1px solid ${chapter.color}40;">
                                    Open Chapter →
                                </a>
                            </div>
                        </div>
                    `;
                    container.appendChild(card);
                    
                    // Sidebar item
                    const sidebarItem = document.createElement('div');
                    sidebarItem.innerHTML = `
                        <a href="${chapter.id}.html" class="chapter-item block p-3 rounded-lg mb-1 hover:bg-white/5 transition-all">
                            <div class="flex items-center gap-2">
                                <span class="w-2 h-2 rounded-full" style="background: ${chapter.color}"></span>
                                <span class="text-sm text-gray-400 hover:text-white">${chapter.title}</span>
                            </div>
                        </a>
                    `;
                    sidebarNav.appendChild(sidebarItem);
                });
                
                // Update stats
                document.getElementById('stat-blocks').textContent = totalBlocks;
                document.getElementById('stat-completed').textContent = completedBlocks;
                document.getElementById('stat-progress').textContent = Math.round((completedBlocks / totalBlocks) * 100) + '%';
                
            } catch (error) {
                console.error('Error loading chapters:', error);
            }
        }
        
        document.addEventListener('DOMContentLoaded', loadChapters);
    </script>
</body>
</html>
'''

with open(os.path.expanduser('~/arc_ai_angels/website/chapters/index.html'), 'w') as f:
    f.write(chapters_index_html)

print("✅ Arc AI Angels website rebuilt successfully!")
print(f"📄 Generated: index.html with Arc AI Angels compact block")
print(f"📊 Chapters: {len(chapters_data['chapters'])} chapters with {total_blocks} total blocks")
print(f"📁 Chapter pages: {len(chapters_data['chapters'])} individual chapter pages")
print(f"📑 Chapters index: chapters/index.html (overview page)")
print(f"🎨 Features: Colored blocks per chapter, direct block links, diagrams in blocks")
print("")
print("Next steps:")
print("1. Run: python3 ~/arc_ai_angels/rebuild_index_v7.py")
print("2. Refresh browser at http://172.24.162.255:9000/index.html")
print("3. Test clicking blocks directly from sidebar")
print("4. Visit http://172.24.162.255:9000/chapters/ for overview")
