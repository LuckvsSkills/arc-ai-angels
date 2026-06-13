#!/usr/bin/env python3
import json
from pathlib import Path
from html import escape

base = Path.home() / "arc_strategic_control_center"
progress = json.loads((base / "data" / "progress.json").read_text(encoding="utf-8"))
security = json.loads((base / "data" / "security_prompts.json").read_text(encoding="utf-8"))
out = base / "prompts.html"

chapter_prompt_map = {
    "platform_runtime": """JE BENT OPENCLAW PLATFORM & RUNTIME ENGINEER.

Werk binnen het hoofdstuk Platform & Runtime. Focus op:
- OpenClaw core installatie
- systemd runtime
- hardened runner
- env allowlists
- linux user isolation
- worker skeleton cluster

Doel:
verifiëren, documenteren en waar nodig stabiliseren van de bestaande runtime foundation.

Werk stap voor stap en lever concrete verificatiecommando’s op.""",
    "security_hardening": security["chapter"]["prompt"],
    "model_runtime": """JE BENT OPENCLAW MODEL RUNTIME ENGINEER.

Werk binnen het hoofdstuk Model Runtime & Providers aan:
- Ollama
- lokale modellen
- provider abstraction
- fallback logic
- model switching per agent

Doel:
één flexibele model-laag maken die lokaal en extern kan schakelen zonder agent logic te herschrijven.""",
    "data_memory": """JE BENT OPENCLAW DATA & MEMORY ARCHITECT.

Werk binnen het hoofdstuk Data & Memory Architecture aan:
- agent management database
- memory architecture
- embeddings / vector strategy
- shared world memory
- per-agent memory links

Doel:
een schaalbare eerste data- en geheugenlaag ontwerpen voor de Arc agents.""",
    "agent_logic": """JE BENT OPENCLAW AGENT LOGIC ENGINEER.

Werk binnen het hoofdstuk Agent Logic, Skills & Swarm aan:
- agent roles
- communication protocol
- workflow dispatcher
- skill registry
- swarm coordination

Doel:
agents effectief, veilig en zonder skill overkill laten samenwerken.""",
    "observability": """JE BENT OPENCLAW OBSERVABILITY & COST ENGINEER.

Werk binnen het hoofdstuk Observability & API Cost Control aan:
- API inventory
- usage ledger
- cost calculations
- latency/error tracing
- per-agent / per-workflow reporting

Doel:
zicht krijgen op gebruik, kosten, failures en performance van het volledige Arc systeem.""",
    "control_center": """JE BENT THE ARC STRATEGIC CONTROL CENTER UI ARCHITECT.

Werk binnen het hoofdstuk Strategic Control Center UI aan:
- homepage dashboard
- chapter pages
- prompt library
- progress visualisatie
- operations-ready layout

Doel:
een lokale control center site bouwen die roadmap-first begint en later uitgroeit tot operations dashboard."""
}

chapter_colors = {
    "platform_runtime": "#36c9ff",
    "security_hardening": "#3fe3b5",
    "model_runtime": "#9b7cff",
    "data_memory": "#4ea8de",
    "agent_logic": "#ff4d6d",
    "observability": "#ffb84d",
    "control_center": "#d6b35e",
}

section_html = []

for chapter in progress["chapters"]:
    cid = chapter["id"]
    title = chapter["title"]
    color = chapter_colors.get(cid, "#d6b35e")
    chapter_prompt = chapter_prompt_map.get(cid, "Prompt volgt later.")

    cards = []

    # Chapter prompt
    anchor_id = f"chapter-{cid}"
    cards.append(f"""
    <article class="prompt-card" id="{escape(anchor_id)}" style="--c:{color}">
      <h3 class="prompt-title">{escape(title)} — Chapter Prompt</h3>
      <div class="prompt-meta">Hoofdstukprompt</div>
      <pre class="prompt-body">{escape(chapter_prompt)}</pre>
      <div class="copy-row"><button class="copy-btn" type="button">Copy Prompt</button></div>
    </article>
    """)

    # Real security cluster/block prompts
    if cid == "security_hardening":
        cards.append(f"""
        <article class="prompt-card" id="cluster-prod_safety_core" style="--c:{color}">
          <h3 class="prompt-title">{escape(security["cluster"]["title"])} — Cluster Prompt</h3>
          <div class="prompt-meta">Clusterprompt</div>
          <pre class="prompt-body">{escape(security["cluster"]["prompt"])}</pre>
          <div class="copy-row"><button class="copy-btn" type="button">Copy Prompt</button></div>
        </article>
        """)
        for block in security["blocks"]:
            cards.append(f"""
            <article class="prompt-card" id="{escape(block['id'])}" style="--c:{color}">
              <h3 class="prompt-title">{escape(block['title'])}</h3>
              <div class="prompt-meta">{escape(block['id'])} · Block prompt</div>
              <pre class="prompt-body">{escape(block['prompt'])}</pre>
              <div class="copy-row"><button class="copy-btn" type="button">Copy Prompt</button></div>
            </article>
            """)

    section_html.append(f"""
    <section class="chapter-section" id="prompts-{escape(cid)}">
      <div class="chapter-head" style="--c:{color}">
        <h2>{escape(title)}</h2>
        <div class="chapter-sub">{chapter['done_blocks']}/{chapter['total_blocks']} blocks done · {chapter['progress_percent']}%</div>
      </div>
      <div class="prompt-grid">
        {''.join(cards)}
      </div>
    </section>
    """)

html = """<!DOCTYPE html>
<html lang="en" data-theme="dark" data-preset="obsidian_gold">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Prompt Library · The Arc Strategic Control Center</title>
<style>
:root{
  --bg0:#0b0b0c; --bg1:#0f0f11; --bg2:#121214;
  --panel:#161618; --panel2:#1c1c20; --panel3:#232329;
  --line:rgba(255,255,255,.10); --text:#eef4fb; --muted:#c3d0e3; --muted2:#95a7c2;
  --accent:#d6b35e; --accent2:#f0d18a; --accentGlow:rgba(240,209,138,.20);
}
[data-theme="light"]{
  --bg0:#eef3f9; --bg1:#f6f9fc; --bg2:#ffffff;
  --panel:#ffffff; --panel2:#f4f7fb; --panel3:#edf2f8;
  --line:rgba(18,24,36,.12); --text:#122033; --muted:#425874; --muted2:#677d98;
  --accentGlow:rgba(214,179,94,.14);
}
[data-preset="obsidian_gold"]{--accent:#d6b35e; --accent2:#f0d18a; --accentGlow:rgba(240,209,138,.20);}
[data-preset="graphite_cyan"]{--accent:#36c9ff; --accent2:#92e8ff; --accentGlow:rgba(54,201,255,.16);}
[data-preset="midnight_purple"]{--accent:#9b7cff; --accent2:#c9b8ff; --accentGlow:rgba(155,124,255,.16);}
[data-preset="slate_teal"]{--accent:#2fd3c5; --accent2:#93fff4; --accentGlow:rgba(47,211,197,.14);}
*{box-sizing:border-box}
html,body{height:100%}
body{
  margin:0;
  font-family:Inter, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif;
  color:var(--text);
  background:
    radial-gradient(1100px 700px at 85% -10%, var(--accentGlow), transparent 60%),
    linear-gradient(180deg, var(--bg0), var(--bg1) 42%, var(--bg2));
}
.wrap{max-width:1320px;margin:0 auto;padding:0 28px}
.topbar{
  position:fixed;top:0;left:0;right:0;z-index:1200;
  background:color-mix(in oklab,var(--panel) 88%, black 4%);
  backdrop-filter:blur(14px);
  border-bottom:1px solid color-mix(in oklab,var(--accent) 24%, var(--line));
  box-shadow:0 10px 24px rgba(0,0,0,.22);
}
.topbar-inner{display:flex;justify-content:space-between;align-items:center;gap:18px;padding:16px 0;}
.logo-wrap{
  display:inline-flex;flex-direction:column;gap:4px;padding:8px 12px;border-radius:16px;
  border:1px solid color-mix(in oklab,var(--accent) 24%, var(--line));
  background:radial-gradient(220px 80px at 0% 0%, color-mix(in oklab,var(--accent) 14%, transparent), transparent 68%), color-mix(in oklab,var(--panel2) 82%, transparent);
}
.logo{font-size:24px;font-weight:950;color:color-mix(in oklab,var(--accent2) 82%, var(--text));line-height:1.1;}
.logo-sub{font-size:13px;color:var(--muted2);}
.nav{display:flex;gap:10px;flex-wrap:wrap;align-items:center;}
.nav a,.btn,select{
  text-decoration:none;color:var(--muted);font-size:14px;padding:9px 13px;border-radius:999px;
  border:1px solid color-mix(in oklab,var(--accent) 16%, var(--line));
  background:color-mix(in oklab,var(--panel2) 78%, transparent);cursor:pointer;
}
.nav a.active{
  color:var(--text);
  border-color:color-mix(in oklab,var(--accent) 44%, var(--line));
  background:radial-gradient(180px 70px at 0% 0%, color-mix(in oklab,var(--accent) 18%, transparent), transparent 68%), color-mix(in oklab,var(--panel2) 92%, transparent);
}
.sidebar{
  position:fixed;left:0;top:78px;width:220px;bottom:0;padding:20px 16px;background:var(--bg1);
  border-right:1px solid color-mix(in oklab,var(--accent) 12%, var(--line));overflow-y:auto;z-index:900;
}
.sidebar h3{font-size:13px;text-transform:uppercase;letter-spacing:.08em;color:var(--muted2);margin:18px 0 8px;}
.sidebar a{
  display:block;padding:10px 12px;margin:4px 0;border-radius:8px;text-decoration:none;font-size:14px;color:var(--muted);
}
.sidebar a:hover{background:color-mix(in oklab,var(--panel2) 78%, transparent);color:var(--text);}
.main{margin-left:240px;padding-top:96px;}
.hero{padding:34px 0 12px}
.panel{
  background:color-mix(in oklab,var(--panel) 94%, black 6%);
  border:1px solid color-mix(in oklab,var(--accent) 26%, var(--line));
  border-radius:24px;padding:24px;position:relative;overflow:hidden;
  box-shadow:0 20px 50px rgba(0,0,0,.34), 0 0 0 1px color-mix(in oklab,var(--accent) 18%, transparent), inset 0 1px 0 rgba(255,255,255,.04);
}
.panel:before{
  content:"";position:absolute;inset:-1px;
  background:radial-gradient(640px 240px at 0% 0%, var(--accentGlow), transparent 58%);
  pointer-events:none;
}
.panel>*{position:relative}
h1{margin:0;font-size:46px;line-height:1.06}
.subtitle{margin:14px 0 0;color:var(--muted);font-size:18px;line-height:1.75}
.section{padding:14px 0 0}
.chapter-section{padding:14px 0 0}
.chapter-head{
  border-radius:18px;
  border:1px solid color-mix(in oklab,var(--c) 26%, var(--line));
  background:radial-gradient(240px 90px at 0% 0%, color-mix(in oklab,var(--c) 14%, transparent), transparent 70%), color-mix(in oklab,var(--panel2) 84%, transparent);
  padding:16px 18px;
}
.chapter-head h2{margin:0;font-size:28px}
.chapter-sub{margin-top:6px;color:var(--muted2);font-size:14px}
.prompt-grid{display:grid;grid-template-columns:1fr 1fr;gap:18px;margin-top:16px}
@media (max-width:980px){.prompt-grid{grid-template-columns:1fr}}
.prompt-card{
  border-radius:24px;
  border:1px solid color-mix(in oklab,var(--c) 30%, var(--line));
  background:color-mix(in oklab,var(--panel3) 92%, black 4%);
  padding:18px;position:relative;overflow:hidden;
  box-shadow:0 16px 38px rgba(0,0,0,.34), 0 0 14px color-mix(in oklab,var(--c) 28%, transparent), 0 0 0 1px color-mix(in oklab,var(--c) 20%, transparent), inset 0 1px 0 rgba(255,255,255,.04);
}
.prompt-card:before{
  content:"";position:absolute;left:0;top:0;right:0;height:4px;
  background:linear-gradient(90deg, color-mix(in oklab,var(--c) 55%, transparent), var(--c), color-mix(in oklab,var(--c) 55%, transparent));
}
.prompt-card>*{position:relative}
.prompt-title{margin:0;font-size:22px;font-weight:900}
.prompt-meta{margin-top:8px;color:var(--muted2);font-size:14px}
.prompt-body{
  margin-top:14px;border-radius:18px;border:1px solid color-mix(in oklab,var(--c) 24%, var(--line));
  background:color-mix(in oklab,var(--panel2) 84%, transparent);
  padding:16px;white-space:pre-wrap;font-family:ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
  font-size:14px;line-height:1.7;color:var(--text);
}
.copy-row{display:flex;justify-content:flex-end;margin-top:12px}
.copy-btn{
  appearance:none;border:1px solid color-mix(in oklab,var(--c) 26%, var(--line));
  background:radial-gradient(160px 70px at 0% 0%, color-mix(in oklab,var(--c) 14%, transparent), transparent 70%), color-mix(in oklab,var(--panel2) 88%, transparent);
  color:var(--text);padding:10px 14px;border-radius:12px;font-size:14px;font-weight:800;cursor:pointer;
}
.copy-btn.copied{color:var(--accent2)}
.footer-space{height:40px}
</style>
</head>
<body>

<div class="topbar">
  <div class="wrap">
    <div class="topbar-inner">
      <div class="logo-wrap">
        <div class="logo">The Arc Strategic Control Center</div>
        <div class="logo-sub">Prompt Library</div>
      </div>

      <div class="nav">
        <a href="./index.html">Home</a>
        <a href="./index.html#chapters">Chapters</a>
        <a href="./index.html#architecture">Architecture</a>
        <a href="./index.html#roadmap">Roadmap</a>
        <a href="./prompts.html" class="active">Prompts</a>

        <select id="presetSelect">
          <option value="obsidian_gold">Obsidian Gold</option>
          <option value="graphite_cyan">Graphite Cyan</option>
          <option value="midnight_purple">Midnight Purple</option>
          <option value="slate_teal">Slate Teal</option>
        </select>
        <button class="btn" id="themeBtn">Theme</button>
      </div>
    </div>
  </div>
</div>

<div class="sidebar">
  <h3>Prompt Hub</h3>
  <a href="#prompts-platform_runtime">Platform & Runtime</a>
  <a href="#prompts-security_hardening">Security Hardening</a>
  <a href="#prompts-model_runtime">Model Runtime</a>
  <a href="#prompts-data_memory">Data & Memory</a>
  <a href="#prompts-agent_logic">Agent Logic</a>
  <a href="#prompts-observability">Observability</a>
  <a href="#prompts-control_center">Control Center UI</a>
</div>

<div class="main">
  <section class="hero">
    <div class="wrap">
      <section class="panel">
        <h1>Prompt Library</h1>
        <p class="subtitle">
          Hoofdstukgerichte prompt hub. Vanuit hoofdstukpagina’s link je naar deze centrale bron.
          Security Hardening bevat hier de echte chapter-, cluster- en block prompts. Andere hoofdstukken hebben nu hun chapter prompt klaar en kunnen later verder worden ingevuld.
        </p>
      </section>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      __SECTIONS__
    </div>
  </section>

  <div class="footer-space"></div>
</div>

<script>
const root = document.documentElement;
const presetSelect = document.getElementById("presetSelect");
const themeBtn = document.getElementById("themeBtn");
const savedTheme = localStorage.getItem("arc_scc_theme");
const savedPreset = localStorage.getItem("arc_scc_preset");
if(savedTheme === "light" || savedTheme === "dark") root.setAttribute("data-theme", savedTheme);
if(savedPreset) root.setAttribute("data-preset", savedPreset);
presetSelect.value = root.getAttribute("data-preset") || "obsidian_gold";

presetSelect.addEventListener("change", ()=>{
  root.setAttribute("data-preset", presetSelect.value);
  localStorage.setItem("arc_scc_preset", presetSelect.value);
});

themeBtn.addEventListener("click", ()=>{
  const cur = root.getAttribute("data-theme") || "dark";
  const next = cur === "dark" ? "light" : "dark";
  root.setAttribute("data-theme", next);
  localStorage.setItem("arc_scc_theme", next);
});

document.querySelectorAll('.copy-btn').forEach(btn => {
  btn.addEventListener('click', async () => {
    const body = btn.closest('.prompt-card').querySelector('.prompt-body');
    if(!body) return;
    try{
      await navigator.clipboard.writeText(body.innerText.trim());
      const old = btn.textContent;
      btn.textContent = 'Copied';
      btn.classList.add('copied');
      setTimeout(() => {
        btn.textContent = old;
        btn.classList.remove('copied');
      }, 1400);
    }catch(err){
      btn.textContent = 'Copy failed';
      setTimeout(() => btn.textContent = 'Copy Prompt', 1400);
    }
  });
});
</script>

</body>
</html>
"""

html = html.replace("__SECTIONS__", "".join(section_html))
out.write_text(html, encoding="utf-8")
print(f"Built {out}")
