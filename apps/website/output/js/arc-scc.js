// ARC Strategic Control Center - Complete JavaScript
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
