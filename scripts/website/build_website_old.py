#!/usr/bin/env python3
import os
import json

# Paths
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_PATH, "data")
OUTPUT_PATH = os.path.join(BASE_PATH, "output")

print("🚀 Starting Arc SCC Website Generation...")

# Ensure output directory exists
os.makedirs(OUTPUT_PATH, exist_ok=True)

# Create sample progress.json if it doesn't exist
progress_file = os.path.join(DATA_PATH, "progress.json")
if not os.path.exists(progress_file):
    print("⚠️  progress.json niet gevonden, maak sample data...")
    os.makedirs(DATA_PATH, exist_ok=True)
    
    sample_data = {
        "project": "Arc Strategic Control Center",
        "version": "1.0",
        "last_updated": "2024-01-01",
        "blocks": [
            {"id": 1, "name": "Block A - Foundation", "status": "completed", "progress": 100},
            {"id": 2, "name": "Block B - Core Systems", "status": "in_progress", "progress": 75},
            {"id": 3, "name": "Block C - Integration", "status": "pending", "progress": 0},
            {"id": 4, "name": "Block D - Testing", "status": "pending", "progress": 0}
        ]
    }
    
    with open(progress_file, 'w') as f:
        json.dump(sample_data, f, indent=2)
    print("✅ Sample progress.json gemaakt")

# Load data
with open(progress_file, 'r') as f:
    data = json.load(f)

# Generate CSS
css_content = """
:root {
    --primary: #00d4ff;
    --secondary: #0099cc;
    --dark: #0a0e17;
    --darker: #050810;
    --text: #e0f7ff;
    --success: #00ff88;
    --warning: #ffaa00;
    --danger: #ff3366;
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background: var(--darker);
    color: var(--text);
    line-height: 1.6;
    overflow-x: hidden;
}

.container {
    max-width: 1400px;
    margin: 0 auto;
    padding: 2rem;
}

header {
    text-align: center;
    padding: 3rem 0;
    background: linear-gradient(135deg, var(--dark) 0%, var(--darker) 100%);
    border-bottom: 2px solid var(--primary);
    margin-bottom: 2rem;
}

h1 {
    font-size: 3rem;
    color: var(--primary);
    text-shadow: 0 0 20px rgba(0, 212, 255, 0.5);
    margin-bottom: 0.5rem;
}

.subtitle {
    color: var(--secondary);
    font-size: 1.2rem;
}

.grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 1.5rem;
    margin-top: 2rem;
}

.card {
    background: var(--dark);
    border: 1px solid rgba(0, 212, 255, 0.2);
    border-radius: 12px;
    padding: 1.5rem;
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}

.card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 2px;
    background: linear-gradient(90deg, var(--primary), transparent);
}

.card:hover {
    transform: translateY(-5px);
    border-color: var(--primary);
    box-shadow: 0 10px 30px rgba(0, 212, 255, 0.2);
}

.card h3 {
    color: var(--primary);
    margin-bottom: 1rem;
    font-size: 1.3rem;
}

.status {
    display: inline-block;
    padding: 0.3rem 0.8rem;
    border-radius: 20px;
    font-size: 0.85rem;
    font-weight: bold;
    text-transform: uppercase;
}

.status.completed {
    background: rgba(0, 255, 136, 0.2);
    color: var(--success);
    border: 1px solid var(--success);
}

.status.in_progress {
    background: rgba(255, 170, 0, 0.2);
    color: var(--warning);
    border: 1px solid var(--warning);
}

.status.pending {
    background: rgba(255, 51, 102, 0.2);
    color: var(--danger);
    border: 1px solid var(--danger);
}

.progress-bar {
    width: 100%;
    height: 8px;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 4px;
    margin-top: 1rem;
    overflow: hidden;
}

.progress-fill {
    height: 100%;
    background: linear-gradient(90deg, var(--primary), var(--secondary));
    border-radius: 4px;
    transition: width 0.5s ease;
}

nav {
    background: var(--dark);
    padding: 1rem;
    position: sticky;
    top: 0;
    z-index: 100;
    border-bottom: 1px solid rgba(0, 212, 255, 0.2);
}

nav ul {
    list-style: none;
    display: flex;
    justify-content: center;
    gap: 2rem;
    flex-wrap: wrap;
}

nav a {
    color: var(--text);
    text-decoration: none;
    padding: 0.5rem 1rem;
    border-radius: 6px;
    transition: all 0.3s;
}

nav a:hover, nav a.active {
    color: var(--primary);
    background: rgba(0, 212, 255, 0.1);
}

footer {
    text-align: center;
    padding: 2rem;
    margin-top: 3rem;
    border-top: 1px solid rgba(0, 212, 255, 0.2);
    color: var(--secondary);
    font-size: 0.9rem;
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
}

.pulse {
    animation: pulse 2s infinite;
}
"""

with open(os.path.join(OUTPUT_PATH, "style.css"), 'w') as f:
    f.write(css_content)
print("✅ CSS template gemaakt")

# Generate main index.html
blocks_html = ""
for block in data.get("blocks", []):
    status_class = block.get("status", "pending")
    progress = block.get("progress", 0)
    blocks_html += f"""
        <div class="card">
            <h3>{block.get('name', 'Unnamed Block')}</h3>
            <span class="status {status_class}">{status_class.replace('_', ' ')}</span>
            <div class="progress-bar">
                <div class="progress-fill" style="width: {progress}%"></div>
            </div>
            <p style="margin-top: 0.5rem; font-size: 0.9rem; color: var(--secondary);">{progress}% Complete</p>
        </div>
    """

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{data.get('project', 'Arc SCC')} - Dashboard</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <nav>
        <ul>
            <li><a href="index.html" class="active">Dashboard</a></li>
            <li><a href="chapters.html">Chapters</a></li>
            <li><a href="timeline.html">Timeline</a></li>
            <li><a href="about.html">About</a></li>
        </ul>
    </nav>
    
    <header>
        <div class="container">
            <h1>🎯 {data.get('project', 'Arc SCC')}</h1>
            <p class="subtitle">Strategic Control Center Dashboard v{data.get('version', '1.0')}</p>
            <p style="margin-top: 1rem; color: var(--secondary);">Last Updated: {data.get('last_updated', 'Unknown')}</p>
        </div>
    </header>

    <main class="container">
        <h2 style="color: var(--primary); margin-bottom: 1rem;">📊 Project Blocks</h2>
        <div class="grid">
            {blocks_html}
        </div>
        
        <div style="margin-top: 3rem; text-align: center;">
            <h2 style="color: var(--primary); margin-bottom: 1rem;">⚡ Quick Stats</h2>
            <div class="grid" style="max-width: 800px; margin: 0 auto;">
                <div class="card">
                    <h3>Total Blocks</h3>
                    <p style="font-size: 2.5rem; color: var(--primary);">{len(data.get('blocks', []))}</p>
                </div>
                <div class="card">
                    <h3>Completed</h3>
                    <p style="font-size: 2.5rem; color: var(--success);">
                        {sum(1 for b in data.get('blocks', []) if b.get('status') == 'completed')}
                    </p>
                </div>
                <div class="card">
                    <h3>In Progress</h3>
                    <p style="font-size: 2.5rem; color: var(--warning);">
                        {sum(1 for b in data.get('blocks', []) if b.get('status') == 'in_progress')}
                    </p>
                </div>
            </div>
        </div>
    </main>

    <footer>
        <p>&copy; 2024 Arc Strategic Control Center. All systems operational.</p>
    </footer>
</body>
</html>
"""

with open(os.path.join(OUTPUT_PATH, "index.html"), 'w') as f:
    f.write(html_content)
print("✅ Dashboard gegenereerd")

# Generate chapters.html
chapters_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chapters - Arc SCC</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <nav>
        <ul>
            <li><a href="index.html">Dashboard</a></li>
            <li><a href="chapters.html" class="active">Chapters</a></li>
            <li><a href="timeline.html">Timeline</a></li>
            <li><a href="about.html">About</a></li>
        </ul>
    </nav>
    
    <header>
        <div class="container">
            <h1>📚 Chapters</h1>
            <p class="subtitle">Documentation and Guidelines</p>
        </div>
    </header>

    <main class="container">
        <div class="grid">
            <div class="card">
                <h3>Chapter 1: Introduction</h3>
                <p>Overview of the Arc Strategic Control Center methodology and core principles.</p>
                <a href="#" style="color: var(--primary);">Read more →</a>
            </div>
            <div class="card">
                <h3>Chapter 2: Architecture</h3>
                <p>System architecture, components, and integration patterns.</p>
                <a href="#" style="color: var(--primary);">Read more →</a>
            </div>
            <div class="card">
                <h3>Chapter 3: Implementation</h3>
                <p>Step-by-step implementation guide and best practices.</p>
                <a href="#" style="color: var(--primary);">Read more →</a>
            </div>
            <div class="card">
                <h3>Chapter 4: Operations</h3>
                <p>Daily operations, monitoring, and maintenance procedures.</p>
                <a href="#" style="color: var(--primary);">Read more →</a>
            </div>
        </div>
    </main>

    <footer>
        <p>&copy; 2024 Arc Strategic Control Center. All systems operational.</p>
    </footer>
</body>
</html>"""

with open(os.path.join(OUTPUT_PATH, "chapters.html"), 'w') as f:
    f.write(chapters_html)
print("✅ Chapters pagina gegenereerd")

# Generate timeline.html
timeline_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Timeline - Arc SCC</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <nav>
        <ul>
            <li><a href="index.html">Dashboard</a></li>
            <li><a href="chapters.html">Chapters</a></li>
            <li><a href="timeline.html" class="active">Timeline</a></li>
            <li><a href="about.html">About</a></li>
        </ul>
    </nav>
    
    <header>
        <div class="container">
            <h1>📅 Timeline</h1>
            <p class="subtitle">Project Milestones and Roadmap</p>
        </div>
    </header>

    <main class="container">
        <div class="card" style="max-width: 800px; margin: 0 auto;">
            <div style="border-left: 2px solid var(--primary); padding-left: 2rem; position: relative;">
                <div style="position: absolute; left: -6px; top: 0; width: 10px; height: 10px; background: var(--success); border-radius: 50%;"></div>
                <h3 style="color: var(--success);">Q1 2024 - Foundation</h3>
                <p>Project initialization and core architecture design. ✓ Completed</p>
            </div>
            <div style="border-left: 2px solid var(--primary); padding-left: 2rem; position: relative; margin-top: 2rem;">
                <div style="position: absolute; left: -6px; top: 0; width: 10px; height: 10px; background: var(--warning); border-radius: 50%;" class="pulse"></div>
                <h3 style="color: var(--warning);">Q2 2024 - Development</h3>
                <p>Core systems implementation and integration. 🔄 In Progress</p>
            </div>
            <div style="border-left: 2px solid var(--primary); padding-left: 2rem; position: relative; margin-top: 2rem;">
                <div style="position: absolute; left: -6px; top: 0; width: 10px; height: 10px; background: var(--secondary); border-radius: 50%;"></div>
                <h3 style="color: var(--secondary);">Q3 2024 - Testing</h3>
                <p>System testing, validation, and optimization. ⏳ Pending</p>
            </div>
            <div style="border-left: 2px solid var(--primary); padding-left: 2rem; position: relative; margin-top: 2rem;">
                <div style="position: absolute; left: -6px; top: 0; width: 10px; height: 10px; background: var(--secondary); border-radius: 50%;"></div>
                <h3 style="color: var(--secondary);">Q4 2024 - Deployment</h3>
                <p>Production deployment and go-live. ⏳ Pending</p>
            </div>
        </div>
    </main>

    <footer>
        <p>&copy; 2024 Arc Strategic Control Center. All systems operational.</p>
    </footer>
</body>
</html>"""

with open(os.path.join(OUTPUT_PATH, "timeline.html"), 'w') as f:
    f.write(timeline_html)
print("✅ Timeline pagina gegenereerd")

# Generate about.html
about_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>About - Arc SCC</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <nav>
        <ul>
            <li><a href="index.html">Dashboard</a></li>
            <li><a href="chapters.html">Chapters</a></li>
            <li><a href="timeline.html">Timeline</a></li>
            <li><a href="about.html" class="active">About</a></li>
        </ul>
    </nav>
    
    <header>
        <div class="container">
            <h1>ℹ️ About</h1>
            <p class="subtitle">Arc Strategic Control Center</p>
        </div>
    </header>

    <main class="container">
        <div class="card" style="max-width: 800px; margin: 0 auto;">
            <h2>Project Overview</h2>
            <p style="margin-top: 1rem; line-height: 1.8;">
                The Arc Strategic Control Center (SCC) is a comprehensive management and monitoring system 
                designed to streamline project execution and resource allocation. Built with modern web 
                technologies, it provides real-time insights into project progress and status.
            </p>
            
            <h3 style="margin-top: 2rem; color: var(--primary);">Features</h3>
            <ul style="margin-top: 1rem; line-height: 2; list-style: none;">
                <li>✨ Real-time progress tracking</li>
                <li>📊 Visual dashboard with status indicators</li>
                <li>📅 Timeline and milestone management</li>
                <li>📚 Comprehensive documentation</li>
                <li>🎨 Modern, responsive design</li>
            </ul>
            
            <h3 style="margin-top: 2rem; color: var(--primary);">Technology Stack</h3>
            <ul style="margin-top: 1rem; line-height: 2; list-style: none;">
                <li>🐍 Python 3 - Backend generation</li>
                <li>🌐 HTML5 - Structure</li>
                <li>🎨 CSS3 - Styling with CSS variables</li>
                <li>📱 Responsive Design - Mobile friendly</li>
            </ul>
        </div>
    </main>

    <footer>
        <p>&copy; 2024 Arc Strategic Control Center. All systems operational.</p>
    </footer>
</body>
</html>"""

with open(os.path.join(OUTPUT_PATH, "about.html"), 'w') as f:
    f.write(about_html)
print("✅ About pagina gegenereerd")

# Generate individual block pages
for i, block in enumerate(data.get("blocks", []), 1):
    block_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{block.get('name', f'Block {i}')} - Arc SCC</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <nav>
        <ul>
            <li><a href="index.html">Dashboard</a></li>
            <li><a href="chapters.html">Chapters</a></li>
            <li><a href="timeline.html">Timeline</a></li>
            <li><a href="about.html">About</a></li>
        </ul>
    </nav>
    
    <header>
        <div class="container">
            <h1>🔷 {block.get('name', f'Block {i}')}</h1>
            <p class="subtitle">Block Details and Status</p>
        </div>
    </header>

    <main class="container">
        <div class="card" style="max-width: 600px; margin: 0 auto;">
            <h2>Status Information</h2>
            <p style="margin-top: 1rem;"><strong>Status:</strong> <span class="status {block.get('status', 'pending')}">{block.get('status', 'pending').replace('_', ' ')}</span></p>
            <p style="margin-top: 1rem;"><strong>Progress:</strong> {block.get('progress', 0)}%</p>
            <div class="progress-bar" style="margin-top: 1rem;">
                <div class="progress-fill" style="width: {block.get('progress', 0)}%"></div>
            </div>
            <p style="margin-top: 2rem; color: var(--secondary);">
                Block ID: {block.get('id', i)}<br>
                Last updated: {data.get('last_updated', 'Unknown')}
            </p>
        </div>
        
        <div style="text-align: center; margin-top: 2rem;">
            <a href="index.html" style="color: var(--primary); text-decoration: none; padding: 0.5rem 1rem; border: 1px solid var(--primary); border-radius: 6px;">← Back to Dashboard</a>
        </div>
    </main>

    <footer>
        <p>&copy; 2024 Arc Strategic Control Center. All systems operational.</p>
    </footer>
</body>
</html>"""
    
    with open(os.path.join(OUTPUT_PATH, f"block_{i}.html"), 'w') as f:
        f.write(block_html)

print(f"✅ {len(data.get('blocks', []))} blok pagina's gegenereerd")

print(f"""
{'='*50}
✅ Website generated successfully!
📂 Location: {OUTPUT_PATH}
📊 Pages: {4 + len(data.get('blocks', []))} (4 main + {len(data.get('blocks', []))} blocks)

🎉 Website generatie voltooid!
📂 Open output/index.html in je browser
{'='*50}
""")
