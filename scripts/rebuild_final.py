#!/usr/bin/env python3
import json
import os

# Create directories
os.makedirs('~/arc_ai_angels/website/data', exist_ok=True)
os.makedirs('~/arc_ai_angels/website/chapters', exist_ok=True)

# Complete chapters data
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

# INDEX.HTML - Complete nieuwe versie
index_html = '''<!DOCTYPE html>
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
        
        /* Chapter hover - 30% lighter full row */
        .chapter-header {
            transition: all 0.3s ease;
            border-left: 3px solid transparent;
        }
        
        .chapter-header:hover {
            filter: brightness(1.3);
            transform: translateX(4px);
        }
        
        /* Block hover */
        .block-item {
            transition: all 0.2s ease;
        }
        
        .block-item:hover {
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
        
        /* Theme dropdown */
        .theme-dropdown {
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 1000;
        }
        
        .theme-select {
            background: rgba(30, 41, 59, 0.9);
            border: 1px solid rgba(255, 255, 255, 0.2);
            color: white;
            padding: 8px 12px;
            border-radius: 8px;
            font-size: 14px;
            cursor: pointer;
            backdrop-filter: blur(10px);
        }
        
        .theme-select option {
            background: #1e293b;
            color: white;
            padding: 8px;
        }
        
        .arc-ai-angels-compact {
            background: linear-gradient(135deg, rgba(59, 130, 246, 0.2) 0%, rgba(139, 92, 246, 0.2) 100%);
            border: 1px solid rgba(59, 130, 246, 0.3);
        }
        
        .grid-bg {
            background-image: 
                linear-gradient(rgba(59, 130, 246, 0.05) 1px, transparent 1px),
                linear-gradient(90deg, rgba(59, 130, 246, 0.05) 1px, transparent 1px);
            background-size: 50px 50px;
        }
        
        /* Diagram container styling */
        .diagram-container {
            background: rgba(15, 23, 42, 0.6);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 16px;
            padding: 24px;
        }
        
        /* Chapter cards smaller */
        .chapter-card-compact {
            padding: 16px;
            margin-bottom: 12px;
        }
        
        /* Intro section */
        .intro-section {
            background: linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, rgba(139, 92, 246, 0.1) 100%);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
    </style>
</head>
<body class="min-h-screen grid-bg">
    <!-- Theme Dropdown -->
    <div class="theme-dropdown">
        <select class="theme-select" id="themeSelect" onchange="setTheme(this.value)">
            <option value="dark">🌙 Dark</option>
            <option value="light">☀️ Light</option>
            <option value="midnight">🌌 Midnight</option>
            <option value="forest">🌲 Forest</option>
        </select>
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
            <section class="relative py-12 px-8 border-b border-white/10">
                <div class="max-w-6xl mx-auto">
                    <div class="flex items-center gap-4 mb-4">
                        <div class="w-14 h-14 rounded-2xl bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center glow">
                            <svg class="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                                      d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"/>
                            </svg>
                        </div>
                        <div>
                            <h1 class="text-4xl font-bold font-mono glow-text">Arc AI Angels</h1>
                            <p class="text-lg text-gray-400 mt-1">Strategisch Architectuur Platform voor AI Agent Orchestration</p>
                        </div>
                    </div>
                </div>
            </section>

            <!-- Intro Section -->
            <section class="p-8">
                <div class="max-w-6xl mx-auto">
                    <div class="intro-section rounded-2xl p-6 mb-8">
                        <h2 class="text-xl font-bold mb-4 flex items-center gap-2">
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
                                    <span class="text-blue-400">Navigatie:</span> Gebruik de sidebar links om door hoofdstukken en blocks te navigeren. Klik op een hoofdstuk om deze uit te klappen en toegang te krijgen tot individuele blocks.
                                </p>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            <!-- Chapters Overview (Compact) + Total Progress -->
            <section class="px-8 pb-8">
                <div class="max-w-6xl mx-auto">
                    <h2 class="text-2xl font-bold mb-6 font-mono">Chapters & Voortgang</h2>
                    
                    <!-- Total Progress Bar -->
                    <div class="glass rounded-xl p-4 mb-6">
                        <div class="flex justify-between items-center mb-2">
                            <span class="text-sm font-medium">Totale Voortgang</span>
                            <span class="text-sm font-mono text-blue-400" id="main-total-percentage">0%</span>
                        </div>
                        <div class="h-3 bg-gray-700 rounded-full overflow-hidden">
                            <div class="h-full bg-gradient-to-r from-blue-500 via-purple-500 to-pink-500 transition-all duration-500" 
                                 id="main-total-progress" style="width: 0%"></div>
                        </div>
                        <div class="flex justify-between text-xs text-gray-500 mt-2">
                            <span id="main-completed-chapters">0/6 chapters</span>
                            <span id="main-completed-blocks">0/24 blocks</span>
                        </div>
                    </div>

                    <!-- Chapter Cards Grid -->
                    <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-4" id="chapters-grid">
                        <!-- Chapters loaded via JS -->
                    </div>
                </div>
            </section>

            <!-- Diagrams Section -->
            <section class="p-8 border-t border-white/10">
                <div class="max-w-6xl mx-auto">
                    <h2 class="text-2xl font-bold mb-6 font-mono">Architectuur & Flow Diagrammen</h2>
                    
                    <div class="grid md:grid-cols-2 gap-6">
                        <!-- Agent Flow Diagram -->
                        <div class="diagram-container">
                            <h3 class="text-lg font-semibold mb-4 text-blue-400 flex items-center gap-2">
                                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/>
                                </svg>
                                Agent Flow
                            </h3>
                            <div class="mermaid">
%%{init: {'theme': 'dark', 'themeVariables': { 'primaryColor': '#3b82f6', 'primaryTextColor': '#fff', 'primaryBorderColor': '#3b82f6', 'lineColor': '#64748b', 'secondaryColor': '#8b5cf6', 'tertiaryColor': '#10b981'}}}%%
flowchart TB
    subgraph Input["User Input"]
        A[Query/Command] --> B{Intent Classifier}
    end
    
    subgraph Orchestration["Arc Orchestrator"]
        B -->|Code| C[Code Agent]
        B -->|Research| D[Research Agent]
        B -->|Creative| E[Creative Agent]
        B -->|Analysis| F[Analysis Agent]
    end
    
    subgraph Processing["Agent Processing"]
        C --> G[LLM Engine]
        D --> G
        E --> G
        F --> G
    end
    
    subgraph Output["Result Aggregation"]
        G --> H[Response Formatter]
        H --> I[User Response]
    end
    
    style A fill:#3b82f6,stroke:#60a5fa,stroke-width:2px,color:#fff
    style B fill:#8b5cf6,stroke:#a78bfa,stroke-width:2px,color:#fff
    style C fill:#10b981,stroke:#34d399,stroke-width:2px,color:#fff
    style D fill:#10b981,stroke:#34d399,stroke-width:2px,color:#fff
    style E fill:#10b981,stroke:#34d399,stroke-width:2px,color:#fff
    style F fill:#10b981,stroke:#34d399,stroke-width:2px,color:#fff
    style G fill:#f59e0b,stroke:#fbbf24,stroke-width:2px,color:#fff
    style H fill:#ec4899,stroke:#f472b6,stroke-width:2px,color:#fff
    style I fill:#3b82f6,stroke:#60a5fa,stroke-width:2px,color:#fff
                            </div>
                        </div>

                        <!-- System Architecture - Nova, Flux, Omni, Sentinels -->
                        <div class="diagram-container">
                            <h3 class="text-lg font-semibold mb-4 text-purple-400 flex items-center gap-2">
                                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"/>
                                </svg>
                                System Architecture - Omni & Sentinels
                            </h3>
                            <div class="mermaid">
%%{init: {'theme': 'dark', 'themeVariables': { 'primaryColor': '#8b5cf6', 'primaryTextColor': '#fff', 'primaryBorderColor': '#8b5cf6', 'lineColor': '#64748b'}}}%%
graph TB
    subgraph UserLayer["User Layer"]
        UI[Web Interface]
        CLI[CLI Tool]
    end
    
    subgraph OmniCore["OMNI Core"]
        OC[Orchestrator]
        KM[Knowledge Manager]
        SM[Session Manager]
    end
    
    subgraph Sentinels["AI Sentinels"]
        NOVA[Nova<br/>Code/Analysis]
        FLUX[Flux<br/>Creative]
        NERO[Nero<br/>Security]
        CLIO[Clio<br/>Research]
        SORA[Sora<br/>Vision]
    end
    
    subgraph Runtime["OpenClaw Runtime"]
        DOCKER[Docker Containers]
        MODELS[Local LLMs]
        VECTOR[Vector Store]
    end
    
    UI --> OmniCore
    CLI --> OmniCore
    OC --> NOVA
    OC --> FLUX
    OC --> NERO
    OC --> CLIO
    OC --> SORA
    KM --> VECTOR
    SM --> DOCKER
    Sentinels --> MODELS
    
    style UI fill:#3b82f6,stroke:#60a5fa,stroke-width:2px,color:#fff
    style CLI fill:#3b82f6,stroke:#60a5fa,stroke-width:2px,color:#fff
    style OC fill:#8b5cf6,stroke:#a78bfa,stroke-width:3px,color:#fff
    style NOVA fill:#10b981,stroke:#34d399,stroke-width:2px,color:#fff
    style FLUX fill:#f59e0b,stroke:#fbbf24,stroke-width:2px,color:#fff
    style NERO fill:#ef4444,stroke:#f87171,stroke-width:2px,color:#fff
    style CLIO fill:#06b6d4,stroke:#22d3ee,stroke-width:2px,color:#fff
    style SORA fill:#ec4899,stroke:#f472b6,stroke-width:2px,color:#fff
                            </div>
                        </div>

                        <!-- Data Flow Diagram -->
                        <div class="diagram-container">
                            <h3 class="text-lg font-semibold mb-4 text-green-400 flex items-center gap-2">
                                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4m0 5c0 2.21-3.582 4-8 4s-8-1.79-8-4"/>
                                </svg>
                                Data Flow
                            </h3>
                            <div class="mermaid">
%%{init: {'theme': 'dark', 'themeVariables': { 'primaryColor': '#10b981', 'primaryTextColor': '#fff', 'primaryBorderColor': '#10b981', 'lineColor': '#64748b'}}}%%
flowchart LR
    subgraph Input["Input Layer"]
        A[User Query] --> B[Input Parser]
        C[File Upload] --> D[Document Processor]
    end
    
    subgraph Processing["Processing Layer"]
        B --> E[Context Enricher]
        D --> E
        E --> F[LLM Processor]
    end
    
    subgraph Storage["Storage Layer"]
        G[(Vector DB<br/>Chroma)]
        H[(Cache<br/>Redis)]
        I[(File Store)]
    end
    
    subgraph Output["Output Layer"]
        F --> J[Response Generator]
        J --> K[User Output]
        F --> L[Action Executor]
    end
    
    E <--> G
    F <--> H
    D --> I
    
    style A fill:#3b82f6,stroke:#60a5fa,stroke-width:2px,color:#fff
    style B fill:#8b5cf6,stroke:#a78bfa,stroke-width:2px,color:#fff
    style C fill:#3b82f6,stroke:#60a5fa,stroke-width:2px,color:#fff
    style D fill:#8b5cf6,stroke:#a78bfa,stroke-width:2px,color:#fff
    style E fill:#10b981,stroke:#34d399,stroke-width:2px,color:#fff
    style F fill:#f59e0b,stroke:#fbbf24,stroke-width:2px,color:#fff
    style G fill:#ec4899,stroke:#f472b6,stroke-width:2px,color:#fff
    style H fill:#06b6d4,stroke:#22d3ee,stroke-width:2px,color:#fff
    style I fill:#6b7280,stroke:#9ca3af,stroke-width:2px,color:#fff
    style J fill:#8b5cf6,stroke:#a78bfa,stroke-width:2px,color:#fff
    style K fill:#3b82f6,stroke:#60a5fa,stroke-width:2px,color:#fff
    style L fill:#ef4444,stroke:#f87171,stroke-width:2px,color:#fff
                            </div>
                        </div>

                        <!-- Build Sequence -->
                        <div class="diagram-container">
                            <h3 class="text-lg font-semibold mb-4 text-amber-400 flex items-center gap-2">
                                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01"/>
                                </svg>
                                Deployment Sequence
                            </h3>
                            <div class="mermaid">
%%{init: {'theme': 'dark', 'themeVariables': { 'primaryColor': '#f59e0b', 'primaryTextColor': '#fff', 'primaryBorderColor': '#f59e0b', 'lineColor': '#64748b'}}}%%
graph TD
    A[1. Setup<br/>Clone Repository] --> B[2. Configure<br/>Environment Vars]
    B --> C[3. Install<br/>Dependencies]
    C --> D[4. Build<br/>Docker Images]
    D --> E[5. Deploy<br/>Start Services]
    E --> F[6. Configure<br/>AI Models]
    F --> G[7. Test<br/>Verify Setup]
    G --> H{Success?}
    H -->|Yes| I[8. Monitor<br/>Production]
    H -->|No| J[Debug & Fix]
    J --> B
    
    style A fill:#3b82f6,stroke:#60a5fa,stroke-width:2px,color:#fff
    style B fill:#8b5cf6,stroke:#a78bfa,stroke-width:2px,color:#fff
    style C fill:#8b5cf6,stroke:#a78bfa,stroke-width:2px,color:#fff
    style D fill:#10b981,stroke:#34d399,stroke-width:2px,color:#fff
    style E fill:#10b981,stroke:#34d399,stroke-width:2px,color:#fff
    style F fill:#f59e0b,stroke:#fbbf24,stroke-width:2px,color:#fff
    style G fill:#06b6d4,stroke:#22d3ee,stroke-width:2px,color:#fff
    style H fill:#ec4899,stroke:#f472b6,stroke-width:2px,color:#fff
    style I fill:#10b981,stroke:#34d399,stroke-width:3px,color:#fff
    style J fill:#ef4444,stroke:#f87171,stroke-width:2px,color:#fff
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
            dark: { bg: '#0f172a', secondary: '#1e293b', tertiary: '#334155', text: '#f8fafc', accent: '#3b82f6' },
            light: { bg: '#f8fafc', secondary: '#e2e8f0', tertiary: '#cbd5e1', text: '#0f172a', accent: '#3b82f6' },
            midnight: { bg: '#020617', secondary: '#0f172a', tertiary: '#1e293b', text: '#e2e8f0', accent: '#6366f1' },
            forest: { bg: '#022c22', secondary: '#064e3b', tertiary: '#065f46', text: '#ecfdf5', accent: '#10b981' }
        };

        function setTheme(themeName) {
            const theme = themes[themeName];
            document.documentElement.style.setProperty('--bg-primary', theme.bg);
            document.documentElement.style.setProperty('--bg-secondary', theme.secondary);
            document.documentElement.style.setProperty('--bg-tertiary', theme.tertiary);
            document.documentElement.style.setProperty('--text-primary', theme.text);
            document.documentElement.style.setProperty('--accent', theme.accent);
            
            // Re-render mermaid with new theme
            mermaid.initialize({ 
                theme: themeName === 'light' ? 'default' : 'dark',
                startOnLoad: true,
                securityLevel: 'loose'
            });
            
            // Close dropdown (browser handles this automatically for select)
        }

        // Load and render chapters
        async function loadChapters() {
            try {
                const response = await fetch('data/progress.json');
                const data = await response.json();
                const chapters = data.chapters;
                
                // Render sidebar navigation with EXPANDABLE blocks
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
                        <div id="blocks-${chapter.id}" class="ml-4 space-y-1 hidden chapter-blocks">
                            <a href="chapters/${chapter.id}.html" class="block-item block p-2 text-xs text-gray-400 hover:text-white rounded flex items-center gap-2 font-medium" style="background: ${chapter.color}10;">
                                <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h7"/>
                                </svg>
                                Chapter Overview
                            </a>
                            ${chapter.blocks.map(block => `
                                <a href="chapters/${chapter.id}.html#${block.id}" 
                                   class="block-item block p-2 text-xs rounded flex items-center gap-2 ${block.completed ? 'opacity-60 line-through text-gray-500' : 'text-gray-300 hover:text-white'}"
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
                
                // Render compact chapter cards in main content
                const chaptersGrid = document.getElementById('chapters-grid');
                chapters.forEach((chapter, idx) => {
                    const completedCount = chapter.blocks.filter(b => b.completed).length;
                    const totalCount = chapter.blocks.length;
                    const percentage = Math.round((completedCount / totalCount) * 100);
                    
                    chaptersGrid.innerHTML += `
                        <div class="chapter-card-compact glass rounded-xl cursor-pointer transition-all hover:scale-[1.02]"
                             style="background: ${chapter.color}10; border: 1px solid ${chapter.color}30;"
                             onclick="location.href='chapters/${chapter.id}.html'">
                            <div class="flex items-center justify-between mb-2">
                                <div class="flex items-center gap-2">
                                    <span class="w-8 h-8 rounded-lg flex items-center justify-center text-sm font-bold"
                                          style="background: ${chapter.color}30; color: ${chapter.color};">${idx + 1}</span>
                                    <span class="font-semibold text-sm">${chapter.title}</span>
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
                
                // Update totals
                const totalBlocks = chapters.reduce((sum, c) => sum + c.blocks.length, 0);
                const completedBlocks = chapters.reduce((sum, c) => sum + c.blocks.filter(b => b.completed).length, 0);
                const completedChapters = chapters.filter(c => c.completed).length;
                const totalPercentage = Math.round((completedBlocks / totalBlocks) * 100);
                
                // Sidebar totals
                document.getElementById('total-percentage').textContent = totalPercentage + '%';
                document.getElementById('total-progress').style.width = totalPercentage + '%';
                document.getElementById('completed-chapters').textContent = completedChapters + ' chapters';
                document.getElementById('completed-blocks').textContent = completedBlocks + '/' + totalBlocks + ' blocks';
                
                // Main content totals
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
        
        // Initialize
        document.addEventListener('DOMContentLoaded', () => {
            mermaid.initialize({ 
                theme: 'dark',
                startOnLoad: true,
                securityLevel: 'loose',
                flowchart: { useMaxWidth: true, htmlLabels: true, curve: 'basis' }
            });
            loadChapters();
        });
    </script>
</body>
</html>'''

# Write index.html
with open(os.path.expanduser('~/arc_ai_angels/website/index.html'), 'w') as f:
    f.write(index_html)

print("✅ index.html gebouwd!")
print("📝 Features:")
print("   - Theme dropdown (sluit automatisch na keuze)")
print("   - Intro sectie met uitleg over OpenClaw & Arc AI Angels")
print("   - Compacte chapter cards met totale progress bar erboven")
print("   - 4 Levendige Mermaid diagrammen (Agent Flow, Omni/Sentinels, Data Flow, Deployment)")
print("   - Hoofdstuk hover: 30% lichter, hele rij")
print("   - Block hover in uitgeklapte hoofdstukken")
print("   - Sidebar met uitklapbare blocks")
print("")
print("Draai: python3 ~/arc_ai_angels/rebuild_final.py")
print("Refresh: http://172.24.162.255:9000/index.html")
