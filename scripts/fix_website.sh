#!/bin/bash
echo "🔧 Website repareren..."

cd ~/arc_strategic_control_center/output

# Download nieuwe CSS
curl -s "https://raw.githubusercontent.com/prime0x2c/arc-scc/main/css/arc-scc.css" -o css/arc-scc.css 2>/dev/null || echo "⚠️  CSS download mislukt, handmatige fix nodig"

# Maak een simpele index.html met werkende sidebar
cat > index.html << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <title>ARC Strategic Control Center</title>
    <style>
        body { font-family: Arial, sans-serif; background: #0f0f1a; color: #e0e0e0; margin: 0; }
        .topbar { background: #1a1a2e; padding: 1rem; border-bottom: 1px solid #333; }
        .logo { color: #FFD700; font-size: 1.5rem; text-decoration: none; font-weight: bold; }
        .container { display: flex; }
        .sidebar { width: 300px; background: #1a1a2e; padding: 1rem; height: calc(100vh - 60px); overflow-y: auto; }
        .main { flex: 1; padding: 2rem; }
        .nav-chapter { margin-bottom: 1rem; }
        .chapter-title { color: #FFD700; font-weight: bold; margin-bottom: 0.5rem; }
        .block-link { display: block; color: #888; text-decoration: none; padding: 0.25rem 0; font-size: 0.9rem; }
        .block-link:hover { color: #FFD700; }
        .block-id { color: #FFD700; font-weight: bold; margin-right: 0.5rem; }
        h1 { color: #FFD700; }
    </style>
</head>
<body>
    <div class="topbar">
        <a href="index.html" class="logo">ARC Strategic Control Center</a>
    </div>
    <div class="container">
        <div class="sidebar">
            <div class="nav-chapter">
                <div class="chapter-title">Foundation</div>
                <a href="block_b01.html" class="block-link"><span class="block-id">b01</span>System Architecture Overview</a>
                <a href="block_b02.html" class="block-link"><span class="block-id">b02</span>Hardware Requirements</a>
                <a href="block_b03.html" class="block-link"><span class="block-id">b03</span>Network Topology</a>
                <a href="block_b04.html" class="block-link"><span class="block-id">b04</span>Base Configuration</a>
                <a href="block_b05.html" class="block-link"><span class="block-id">b05</span>Installation Procedures</a>
                <a href="block_b06.html" class="block-link"><span class="block-id">b06</span>Initial Setup</a>
                <a href="block_b07.html" class="block-link"><span class="block-id">b07</span>Core Services</a>
            </div>
            <div class="nav-chapter">
                <div class="chapter-title">Platform & Runtime</div>
                <a href="block_b08.html" class="block-link"><span class="block-id">b08</span>Runtime Environment</a>
                <a href="block_b09.html" class="block-link"><span class="block-id">b09</span>Container Orchestration</a>
                <a href="block_b10.html" class="block-link"><span class="block-id">b10</span>Service Mesh</a>
            </div>
        </div>
        <div class="main">
            <h1>Dashboard</h1>
            <p>Welkom bij ARC Strategic Control Center</p>
            <p><a href="chapters.html" style="color: #FFD700;">Bekijk alle hoofdstukken →</a></p>
        </div>
    </div>
</body>
</html>
EOF

echo "✅ Website gerepareerd!"
echo "🚀 Start de server opnieuw:"
echo "   cd ~/arc_strategic_control_center/output && python3 -m http.server 8888"
