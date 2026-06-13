#!/usr/bin/env python3

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
        
        ::-webkit-scrollbar { width: 8px; height: 8px; }
        ::-webkit-scrollbar-track { background: var(--bg-secondary); }
        ::-webkit-scrollbar-thumb { background: var(--bg-tertiary); border-radius: 4px; }
        
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
        
        .glow { box-shadow: 0 0 20px rgba(59, 130, 246, 0.3); }
        .glow-text { text-shadow: 0 0 30px rgba(59, 130, 246, 0.5); }
        
        .chapter-header {
            transition: all 0.3s ease;
            border-left: 3px solid transparent;
        }
        
        .chapter-header:hover {
            filter: brightness(1.3);
            transform: translateX(4px);
        }
        
        .mermaid {
            background: transparent !important;
        }
        
        .mermaid svg {
            max-width: 100%;
            height: auto;
        }
        
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
        
        .arc-ai-angels-compact {
            background: linear-gradient(135deg, rgba(59, 130, 246, 0.2) 0%, rgba(139, 92, 246, 0.2) 100%);
            border: 1px solid rgba(59, 130, 246, 0.3);
        }
        
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
                <!-- Chapters loaded via JS -->
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
graph LR
    A[Presentation] --> B[Orchestration]
    B --> C[Agent Runtime]
    C --> D[Models]
    D --> E[Infrastructure]
                            </div>
                        </div>

                        <!-- Data Flow -->
                        <div class="glass rounded-2xl p-6">
                            <h3 class="text-lg font-semibold mb-4 text-green-400">Data Stroom</h3>
                            <div class="mermaid">
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
graph TD
    A[Setup] --> B[Configure]
    B --> C[Deploy]
    C --> D[Test]
    D --> E[Monitor]
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
                    
                    const chapterDiv = document.createElement('div');
                    chapterDiv.className = 'mb-2';
                    chapterDiv.innerHTML = `
                        <div class="chapter-header cursor-pointer p-3 rounded-lg"
                             style="background: ${chapter.color}20; border-left: 3px solid ${chapter.color};">
                            <div class="flex items-center justify-between">
                                <div class="flex items-center gap-2">
                                    <span class="w-2 h-2 rounded-full" style="background: ${chapter.color}"></span>
                                    <span class="font-medium text-sm">${chapter.title}</span>
                                </div>
                                <span class="text-xs text-gray-400">${completedCount}/${totalCount}</span>
                            </div>
                            <div class="mt-2 flex items-center gap-2">
                                <div class="flex-1 h-1 bg-gray-700 rounded-full overflow-hidden">
                                    <div class="h-full rounded-full" style="width: ${percentage}%; background: ${chapter.color}"></div>
                                </div>
                                <span class="text-xs font-mono" style="color: ${chapter.color}">${percentage}%</span>
                            </div>
                        </div>
                    `;
                    sidebarNav.appendChild(chapterDiv);
                });
                
                // Render Control Center chapters (first 3)
                const controlCenter = document.getElementById('control-center-chapters');
                chapters.slice(0, 3).forEach(chapter => {
                    const completedCount = chapter.blocks.filter(b => b.completed).length;
                    const totalCount = chapter.blocks.length;
                    const percentage = Math.round((completedCount / totalCount) * 100);
                    
                    controlCenter.innerHTML += `
                        <div class="p-4 rounded-xl transition-all hover:scale-[1.02] cursor-pointer"
                             style="background: ${chapter.color}15; border: 1px solid ${chapter.color}30;">
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
                                <span>${completedCount} van ${totalCount} blocks</span>
                                <span>${completedCount === totalCount ? '✓ Compleet' : 'In progress'}</span>
                            </div>
                        </div>
                    `;
                });
                
                // Render AI Angels chapters (last 3)
                const aiAngels = document.getElementById('ai-angels-chapters');
                chapters.slice(3).forEach(chapter => {
                    const completedCount = chapter.blocks.filter(b => b.completed).length;
                    const totalCount = chapter.blocks.length;
                    const percentage = Math.round((completedCount / totalCount) * 100);
                    
                    aiAngels.innerHTML += `
                        <div class="p-4 rounded-xl transition-all hover:scale-[1.02] cursor-pointer"
                             style="background: ${chapter.color}15; border: 1px solid ${chapter.color}30;">
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
                                <span>${completedCount} van ${totalCount} blocks</span>
                                <span>${completedCount === totalCount ? '✓ Compleet' : 'In progress'}</span>
                            </div>
                        </div>
                    `;
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
</html>'''

with open('/home/prime/arc_ai_angels/website/index.html', 'w') as f:
    f.write(html_content)

print("✅ index.html geschreven!")
print("Grootte:", len(html_content), "karakters")
print("\nRefresh je browser nu (Ctrl+Shift+R)")
