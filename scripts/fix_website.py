#!/usr/bin/env python3

# Dit is de backup die we gebruiken als basis
backup_content = open('/home/prime/arc_ai_angels/website/index.html.backup.20260324_225350').read()

# We schrijven een compleet nieuw bestand met de JUISTE structuur
# gebaseerd op jouw wensen, maar wel werkend

new_html = '''<!DOCTYPE html>
<html lang="nl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Arc AI Angels - Strategisch Architectuur Platform</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    <style>
        :root { --bg-primary: #0f172a; --bg-secondary: #1e293b; --text-primary: #f8fafc; }
        body { font-family: 'Inter', sans-serif; background: var(--bg-primary); color: var(--text-primary); }
        .font-mono { font-family: 'JetBrains Mono', monospace; }
        .glass { background: rgba(30, 41, 59, 0.7); backdrop-filter: blur(12px); border: 1px solid rgba(255, 255, 255, 0.1); }
        .glass-strong { background: rgba(15, 23, 42, 0.9); backdrop-filter: blur(16px); border: 1px solid rgba(255, 255, 255, 0.1); }
        .glow { box-shadow: 0 0 20px rgba(59, 130, 246, 0.3); }
        .glow-text { text-shadow: 0 0 30px rgba(59, 130, 246, 0.5); }
        
        /* THEME DROPDOWN FIX - witte tekst op donkere achtergrond */
        .theme-dropdown { position: fixed; top: 20px; right: 20px; z-index: 1000; }
        .theme-select { 
            background: rgba(30, 41, 59, 0.95) !important; 
            color: #ffffff !important; 
            border: 1px solid rgba(255, 255, 255, 0.3) !important; 
            padding: 8px 12px; 
            border-radius: 8px; 
            font-size: 14px; 
            cursor: pointer;
        }
        .theme-select option { 
            background: #1e293b !important; 
            color: #ffffff !important; 
        }
        
        /* CHAPTER HOVER - 30% lichter, hele rij */
        .chapter-header { 
            transition: all 0.3s ease; 
            border-left: 3px solid transparent;
        }
        .chapter-header:hover { 
            filter: brightness(1.3) !important; 
            transform: translateX(4px); 
        }
        
        /* BLOCK HOVER in uitgeklapte hoofdstukken */
        .block-link { transition: all 0.2s ease; }
        .block-link:hover { 
            filter: brightness(1.3) !important; 
            transform: translateX(8px); 
            background: rgba(255, 255, 255, 0.1) !important;
        }
        
        .arc-ai-angels-compact {
            background: linear-gradient(135deg, rgba(59, 130, 246, 0.2) 0%, rgba(139, 92, 246, 0.2) 100%);
            border: 1px solid rgba(59, 130, 246, 0.3);
        }
        
        .grid-bg {
            background-image: linear-gradient(rgba(59, 130, 246, 0.05) 1px, transparent 1px),
                linear-gradient(90deg, rgba(59, 130, 246, 0.05) 1px, transparent 1px);
            background-size: 50px 50px;
        }
        
        /* Intro sectie */
        .intro-section {
            background: linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, rgba(139, 92, 246, 0.1) 100%);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 16px;
        }
        
        /* Diagrammen */
        .diagram-container {
            background: rgba(15, 23, 42, 0.6);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 16px;
            padding: 24px;
        }
        
        .mermaid svg { max-width: 100%; height: auto; }
        
        /* Chapter cards compact */
        .chapter-card-compact {
            transition: all 0.3s ease;
        }
        .chapter-card-compact:hover {
            transform: scale(1.02);
        }
    </style>
</head>
<body class="min-h-screen grid-bg">
    <!-- THEME DROPDOWN -->
    <div class="theme-dropdown">
        <select class="theme-select" id="themeSelect" onchange="setTheme(this.value)">
            <option value="dark">🌙 Dark</option>
            <option value="light">☀️ Light</option>
            <option value="midnight">🌌 Midnight</option>
            <option value="forest">🌲 Forest</option>
        </select>
    </div>

    <div class="flex h-screen overflow-hidden">
        <!-- SIDEBAR -->
        <aside class="w-80 glass-strong flex flex-col overflow-hidden">
            <div class="p-6 border-b border-white/10">
                <h1 class="text-2xl font-bold font-mono glow-text bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
                    Arc AI Angels
                </h1>
                <p class="text-xs text-gray-400 mt-1">Strategisch Architectuur Platform</p>
            </div>
            
            <!-- ARC AI ANGELS COMPACT BLOCK -->
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
            </div>
            
            <!-- NAVIGATION -->
            <nav class="flex-1 overflow-y-auto p-4 space-y-2" id="sidebar-nav"></nav>
            
            <!-- TOTAL PROGRESS -->
            <div class="p-4 border-t border-white/10">
                <div class="flex justify-between text-sm mb-2">
                    <span class="text-gray-400">Totale Voortgang</span>
                    <span class="font-mono text-blue-400" id="total-percentage">0%</span>
                </div>
                <div class="h-2 bg-gray-700 rounded-full overflow-hidden">
                    <div class="h-full bg-gradient-to-r from-blue-500 to-purple-500 transition-all duration-500" id="total-progress" style="width: 0%"></div>
                </div>
                <div class="flex justify-between text-xs text-gray-500 mt-2">
                    <span id="completed-chapters">0 chapters</span>
                    <span id="completed-blocks">0 blocks</span>
                </div>
            </div>
        </aside>

        <!-- MAIN CONTENT -->
        <main class="flex-1 overflow-y-auto">
            <!-- HERO -->
            <section class="relative py-12 px-8 border-b border-white/10">
                <div class="max-w-6xl mx-auto">
                    <div class="flex items-center gap-4 mb-4">
                        <div class="w-14 h-14 rounded-2xl bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center glow">
                            <svg class="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"/>
                            </svg>
                        </div>
                        <div>
                            <h1 class="text-4xl font-bold font-mono glow-text">Arc AI Angels</h1>
                            <p class="text-lg text-gray-400 mt-1">Strategisch Architectuur Platform voor AI Agent Orchestration</p>
                        </div>
                    </div>
                </div>
            </section>

            <!-- INTRO SECTION -->
            <section class="p-8">
                <div class="max-w-6xl mx-auto">
                    <div class="intro-section p-6 mb-8">
                        <h2 class="text-xl font-bold mb-4 flex items-center gap-2 text-white">
                            <svg class="w-5 h-5 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                            </svg>
                            Welkom bij Arc AI Angels
                        </h2>
                        <div class="grid md:grid-cols-2 gap-6 text-sm text-gray-300 leading-relaxed">
                            <div>
                                <p class="mb-3">
                                    <strong class="text-white">Arc AI Angels</strong> is een compleet framework voor het opzetten, beheren en orchestreren van AI agents op je eigen infrastructuur. Gebouwd op <strong class="text-blue-400">OpenClaw</strong> - een open-source platform voor lokale AI deployment.
                                </p>
                                <p>
                                    Het platform draait op je eigen PC of server, wat volledige controle geeft over je data en privacy. Geen cloud-afhankelijkheid, geen vendor lock-in.
                                </p>
                            </div>
                            <div>
                                <p class="mb-3">
                                    <strong class="text-white">Arc Control Center (ACC)</strong> is de documentatiehub die aangeeft <em>hoe</em>, <em>waar</em>, <em>wie</em> en <em>waarmee</em> je aan de slag gaat.
                                </p>
                                <p class="text-xs text-gray-400">
                                    <span class="text-blue-400">Navigatie:</span> Gebruik de sidebar links om door hoofdstukken en blocks te navigeren. Klik op een hoofdstuk om deze uit te klappen.
                                </p>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            <!-- CHAPTERS + TOTAL PROGRESS (BOVEN) -->
            <section class="px-8 pb-8">
                <div class="max-w-6xl mx-auto">
                    <h2 class="text-2xl font-bold mb-6 font-mono text-white">Chapters & Voortgang</h2>
                    
                    <!-- TOTAL PROGRESS BAR -->
                    <div class="glass rounded-xl p-4 mb-6">
                        <div class="flex justify-between items-center mb-2">
                            <span class="text-sm font-medium text-white">Totale Voortgang</span>
                            <span class="text-sm font-mono text-blue-400" id="main-total-percentage">0%</span>
                        </div>
                        <div class="h-3 bg-gray-700 rounded-full overflow-hidden">
                            <div class="h-full bg-gradient-to-r from-blue-500 via-purple-500 to-pink-500 transition-all duration-500" id="main-total-progress" style="width: 0%"></div>
                        </div>
                        <div class="flex justify-between text-xs text-gray-500 mt-2">
                            <span id="main-completed-chapters">0/6 chapters</span>
                            <span id="main-completed-blocks">0/24 blocks</span>
                        </div>
                    </div>

                    <!-- CHAPTER CARDS (COMPACT) -->
                    <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-4" id="chapters-grid"></div>
                </div>
            </section>

            <!-- DIAGRAMMEN (ONDERAAN) -->
            <section class="p-8 border-t border-white/10">
                <div class="max-w-6xl mx-auto">
                    <h2 class="text-2xl font-bold mb-6 font-mono text-white">Architectuur & Flow Diagrammen</h2>
                    
                    <div class="grid md:grid-cols-2 gap-6">
                        <!-- Agent Flow -->
                        <div class="diagram-container">
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
                        <div class="diagram-container">
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
                        <div class="diagram-container">
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
                        <div class="diagram-container">
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
            document.body.style.background = theme.bg;
            document.body.style.color = theme.text;
            mermaid.initialize({ theme: themeName === 'light' ? 'default' : 'dark', startOnLoad: true, securityLevel: 'loose' });
        }

        async function loadChapters() {
            try {
                const response = await fetch('data/progress.json');
                const data = await response.json();
                const chapters = data.chapters;
                
                const sidebarNav = document.getElementById('sidebar-nav');
                sidebarNav.innerHTML = '';
                
                chapters.forEach(chapter => {
                    const completedCount = chapter.blocks.filter(b => b.completed).length;
                    const totalCount = chapter.blocks.length;
                    const percentage = Math.round((completedCount / totalCount) * 100);
                    
                    const chapterDiv = document.createElement('div');
                    chapterDiv.className = 'mb-2';
                    chapterDiv.innerHTML = `
                        <div class="chapter-header cursor-pointer p-3 rounded-lg mb-1"
                             style="background: ${chapter.color}20; border-left: 3px solid ${chapter.color};"
                             onclick="toggleChapter('${chapter.id}')">
                            <div class="flex items-center justify-between">
                                <div class="flex items-center gap-2">
                                    <span class="w-2 h-2 rounded-full" style="background: ${chapter.color}"></span>
                                    <span class="font-medium text-sm text-white">${chapter.title}</span>
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
                        <div id="blocks-${chapter.id}" class="ml-4 space-y-1 hidden chapter-blocks">
                            <a href="chapters/${chapter.id}.html" class="block-link block p-2 text-xs text-gray-400 hover:text-white rounded flex items-center gap-2 font-medium" style="background: ${chapter.color}10;">
                                <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h7"/>
                                </svg>
                                Chapter Overview
                            </a>
                            ${chapter.blocks.map(block => `
                                <a href="chapters/${chapter.id}.html#${block.id}" 
                                   class="block-link block p-2 text-xs rounded flex items-center gap-2 ${block.completed ? 'opacity-60 line-through text-gray-500' : 'text-gray-300 hover:text-white'}"
                                   style="background: ${chapter.color}08; border-left: 2px solid ${block.completed ? '#10b981' : chapter.color}40;"
                                   onclick="event.stopPropagation()">
                                    <span class="w-1.5 h-1.5 rounded-full" style="background: ${block.completed ? '#10b981' : chapter.color}"></span>
                                    ${block.title}
                                </a>
                            `).join('')}
                        </div>
                    `;
                    sidebarNav.appendChild(chapterDiv);
                });
                
                const chaptersGrid = document.getElementById('chapters-grid');
                chapters.forEach((chapter, idx) => {
                    const completedCount = chapter.blocks.filter(b => b.completed).length;
                    const totalCount = chapter.blocks.length;
                    const percentage = Math.round((completedCount / totalCount) * 100);
                    
                    chaptersGrid.innerHTML += `
                        <div class="chapter-card-compact glass rounded-xl cursor-pointer p-4"
                             style="background: ${chapter.color}15; border: 1px solid ${chapter.color}30;"
                             onclick="location.href='chapters/${chapter.id}.html'">
                            <div class="flex items-center justify-between mb-2">
                                <div class="flex items-center gap-2">
                                    <span class="w-8 h-8 rounded-lg flex items-center justify-center text-sm font-bold"
                                          style="background: ${chapter.color}30; color: ${chapter.color};">${idx + 1}</span>
                                    <span class="font-semibold text-sm text-white">${chapter.title}</span>
                                </div>
                                <span class="text-xs font-mono" style="color: ${chapter.color}">${percentage}%</span>
                            </div>
                            <div class="h-2 bg-gray-700 rounded-full overflow-hidden mb-2">
                                <div class="h-full rounded-full transition-all duration-500" 
                                     style="width: ${percentage}%; background: ${chapter.color}"></div>
                            </div>
                            <div class="flex justify-between text-xs text-gray-400">
                                <span>${completedCount}/${totalCount} blocks</span>
                                <span>${completedCount === totalCount ? '✓' : '○'}</span>
                            </div>
                        </div>
                    `;
                });
                
                const totalBlocks = chapters.reduce((sum, c) => sum + c.blocks.length, 0);
                const completedBlocks = chapters.reduce((sum, c) => sum + c.blocks.filter(b => b.completed).length, 0);
                const completedChapters = chapters.filter(c => c.completed).length;
                const totalPercentage = Math.round((completedBlocks / totalBlocks) * 100);
                
                document.getElementById('total-percentage').textContent = totalPercentage + '%';
                document.getElementById('total-progress').style.width = totalPercentage + '%';
                document.getElementById('completed-chapters').textContent = completedChapters + ' chapters';
                document.getElementById('completed-blocks').textContent = completedBlocks + '/' + totalBlocks + ' blocks';
                
                document.getElementById('main-total-percentage').textContent = totalPercentage + '%';
                document.getElementById('main-total-progress').style.width = totalPercentage + '%';
                document.getElementById('main-completed-chapters').textContent = completedChapters + '/6 chapters';
                document.getElementById('main-completed-blocks').textContent = completedBlocks + '/' + totalBlocks + ' blocks';
                
            } catch (error) {
                console.error('Error loading chapters:', error);
            }
        }
        
        function toggleChapter(chapterId) {
            const blocks = document.getElementById(`blocks-${chapterId}`);
            const chevron = document.getElementById(`chevron-${chapterId}`);
            if (blocks.classList.contains('hidden')) {
                blocks.classList.remove('hidden');
                chevron.style.transform = 'rotate(180deg)';
            } else {
                blocks.classList.add('hidden');
                chevron.style.transform = 'rotate(0deg)';
            }
        }
        
        document.addEventListener('DOMContentLoaded', () => {
            mermaid.initialize({ theme: 'dark', startOnLoad: true, securityLevel: 'loose' });
            loadChapters();
        });
    </script>
</body>
</html>'''

# Schrijf het bestand
with open('/home/prime/arc_ai_angels/website/index.html', 'w') as f:
    f.write(new_html)

print("✅ NIEUWE index.html geschreven!")
print(f"Grootte: {len(new_html)} bytes")
print("")
print("Wat erin zit:")
print("- Theme dropdown met witte tekst op donkere achtergrond")
print("- Chapter hover: 30% lichter, hele rij")
print("- Block hover: 30% lichter + transform")
print("- Intro sectie met uitleg")
print("- Compacte chapter cards")
print("- Totale progress bar BOVEN de chapters")
print("- 4 Mermaid diagrammen ONDERAAN")
