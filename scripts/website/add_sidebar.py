from pathlib import Path

index = Path.home() / "arc_strategic_control_center" / "index.html"
html = index.read_text()

sidebar_css = """

/* SIDEBAR */

.sidebar{
position:fixed;
left:0;
top:70px;
width:220px;
bottom:0;
padding:20px 16px;
background:#0f0f11;
border-right:1px solid rgba(255,255,255,.05);
overflow-y:auto;
z-index:900;
}

.sidebar h3{
font-size:13px;
text-transform:uppercase;
letter-spacing:.08em;
color:var(--muted2);
margin:18px 0 8px;
}

.sidebar a{
display:block;
padding:10px 12px;
margin:4px 0;
border-radius:8px;
text-decoration:none;
font-size:14px;
color:var(--muted);
transition:all .15s ease;
}

.sidebar a:hover{
background:rgba(255,255,255,.04);
color:var(--text);
}

.sidebar a.active{
background:rgba(214,179,94,.14);
color:var(--accent2);
border-left:3px solid var(--accent);
padding-left:9px;
}

.main{
margin-left:240px;
}

"""

html = html.replace("</style>", sidebar_css + "\n</style>")

sidebar_html = """

<div class="sidebar">

<h3>Navigation</h3>
<a href="#home">Home</a>
<a href="#chapters">Chapters</a>
<a href="#architecture">Architecture</a>
<a href="#roadmap">Roadmap</a>

<h3>Chapters</h3>
<a href="./chapters/platform_runtime.html">Platform & Runtime</a>
<a href="./chapters/security_hardening.html">Security Hardening</a>
<a href="./chapters/model_runtime.html">Model Runtime</a>
<a href="./chapters/data_memory.html">Data & Memory</a>
<a href="./chapters/agent_logic.html">Agent Logic</a>
<a href="./chapters/observability.html">Observability</a>
<a href="./chapters/control_center.html">Control Center UI</a>

</div>

"""

html = html.replace("<body>", "<body>\n" + sidebar_html)

html = html.replace(
'<section class="hero" id="home">',
'<div class="main">\n<section class="hero" id="home">'
)

html = html.replace(
'<div class="footer-space"></div>',
'</div>\n<div class="footer-space"></div>'
)

index.write_text(html)

print("Sidebar added")
