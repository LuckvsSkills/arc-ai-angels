from pathlib import Path

base = Path.home() / "arc_strategic_control_center"
index = base / "index.html"

html = """
<!DOCTYPE html>
<html lang="en" data-theme="dark">

<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">

<title>The Arc Strategic Control Center</title>

<style>

body{
margin:0;
font-family: system-ui,Segoe UI,Roboto;
background:#1c2634;
color:#e8eef7;
}

/* TOP BAR */

.topbar{
background:#243041;
padding:16px 30px;
display:flex;
justify-content:space-between;
align-items:center;
}

.logo{
font-size:22px;
font-weight:700;
}

.nav a{
color:#c7d2e5;
margin-left:20px;
text-decoration:none;
font-size:15px;
}

/* HERO */

.hero{
padding:60px 40px;
max-width:1200px;
margin:auto;
}

.hero h1{
font-size:46px;
margin-bottom:10px;
}

.hero p{
font-size:18px;
color:#aab7cc;
}

/* GRID */

.section{
max-width:1200px;
margin:40px auto;
padding:0 40px;
}

.section h2{
font-size:28px;
margin-bottom:20px;
}

/* CHAPTER GRID */

.grid{
display:grid;
grid-template-columns:repeat(3,1fr);
gap:20px;
}

.card{
background:#2c3a4e;
padding:20px;
border-radius:12px;
transition:0.2s;
}

.card:hover{
transform:translateY(-3px);
background:#34455d;
}

.card h3{
margin:0;
font-size:20px;
}

.card p{
color:#b6c2d6;
font-size:15px;
margin-top:10px;
}

/* FLOW */

.flow{
background:#243041;
padding:30px;
border-radius:12px;
}

.flow-step{
padding:14px;
background:#2c3a4e;
margin-bottom:10px;
border-radius:8px;
}

</style>
</head>

<body>

<div class="topbar">
<div class="logo">Arc Strategic Control Center</div>
<div class="nav">
<a href="#">Home</a>
<a href="#">Architecture</a>
<a href="#">Roadmap</a>
<a href="#">Chapters</a>
<a href="#">Prompts</a>
</div>
</div>

<div class="hero">
<h1>The Arc Strategic Control Center</h1>
<p>Architecture, Governance & Deployment Hub for the Arc AI Agent Network</p>
</div>

<div class="section">
<h2>Chapters</h2>

<div class="grid">

<div class="card">
<h3>Platform & Runtime</h3>
<p>Core OpenClaw runtime infrastructure.</p>
</div>

<div class="card">
<h3>Security Hardening</h3>
<p>Secrets, monitoring and kill-switch systems.</p>
</div>

<div class="card">
<h3>Model Runtime</h3>
<p>Ollama integration and provider routing.</p>
</div>

<div class="card">
<h3>Data & Memory</h3>
<p>Agent memory architecture and vector storage.</p>
</div>

<div class="card">
<h3>Agent Logic & Swarm</h3>
<p>Roles, skills and multi-agent orchestration.</p>
</div>

<div class="card">
<h3>Observability</h3>
<p>API cost tracking, telemetry and tracing.</p>
</div>

</div>
</div>

<div class="section">

<h2>Arc Architecture</h2>

<div class="flow">

<div class="flow-step">FEA → Vision Source</div>

<div class="flow-step">Nova → Gateway Interface</div>

<div class="flow-step">Flux → Strategic Brain</div>

<div class="flow-step">Sentinel Layer → Pillar Leaders</div>

<div class="flow-step">Worker Swarm → Task Execution</div>

</div>

</div>

<div class="section">

<h2>Fastest Path to Live</h2>

<div class="flow">

<div class="flow-step">Platform Runtime</div>
<div class="flow-step">Security Hardening</div>
<div class="flow-step">Model Runtime</div>
<div class="flow-step">Data & Memory</div>
<div class="flow-step">Agent Logic</div>
<div class="flow-step">Observability</div>
<div class="flow-step">Control Center UI</div>

</div>

</div>

</body>
</html>
"""

index.write_text(html)

print("Arc Control Center V2 homepage built.")
