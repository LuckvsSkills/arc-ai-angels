#!/usr/bin/env python3
import json
from pathlib import Path
from html import escape

base = Path.home() / "arc_strategic_control_center"
progress = json.loads((base / "data" / "progress.json").read_text(encoding="utf-8"))
meta = json.loads((base / "data" / "chapter_meta.json").read_text(encoding="utf-8"))
chapters_dir = base / "chapters"
chapters_dir.mkdir(exist_ok=True)

chapter_details = {
    "platform_runtime": {
        "subtitle": "Foundation layer for OpenClaw execution",
        "description": "Dit hoofdstuk bevat de fundering van het platform: core installatie, runtime, runner, environment loading, isolation en worker cluster voorbereiding.",
        "goal": "Een stabiele en herhaalbare execution base neerzetten waarop alle volgende hoofdstukken veilig kunnen bouwen."
    },
    "security_hardening": {
        "subtitle": "Prod readiness, default deny and response controls",
        "description": "Dit hoofdstuk maakt de infrastructuur productierijp met secrets hardening, egress control, incident response, kill switch en monitoring/backpressure.",
        "goal": "Een veilige, auditbare en gecontroleerde runtime neerzetten voordat het systeem live gaat."
    },
    "model_runtime": {
        "subtitle": "Local and cloud model execution layer",
        "description": "Dit hoofdstuk gaat over Ollama, externe providers, model switching per agent, fallback logic en een provider abstraction layer.",
        "goal": "Een flexibele model runtime bouwen waarbij agents tussen lokale en externe modellen kunnen wisselen zonder logic te herschrijven."
    },
    "data_memory": {
        "subtitle": "Databases for agents, memory and system state",
        "description": "Dit hoofdstuk definieert de data- en memorylaag van The Arc: agent management database, memory database, retrieval, embeddings en seed knowledge.",
        "goal": "Agents voorzien van consistente state, geheugen en bestuurbare data-architectuur."
    },
    "agent_logic": {
        "subtitle": "Roles, skills, workflows and swarm logic",
        "description": "Dit hoofdstuk beschrijft agentrollen, communicatieprotocollen, skill governance, workflow routing en swarm coordination.",
        "goal": "Agents smal, effectief en veilig laten samenwerken zonder skill overkill."
    },
    "observability": {
        "subtitle": "Usage, tracing, cost and health visibility",
        "description": "Dit hoofdstuk geeft zicht op API usage, kosten, health, tracing, provider calls, latency en operationele signalen.",
        "goal": "Weten wat draait, wat het kost, wat faalt en waarom."
    },
    "control_center": {
        "subtitle": "Roadmap site now, operations dashboard later",
        "description": "Dit hoofdstuk gaat over de UI van The Arc Strategic Control Center: homepage, hoofdstukpagina’s, prompt library, diagrams en later live operations widgets.",
        "goal": "Een centrale bestuurbare interface maken die roadmap-first begint en operations-ready eindigt."
    }
}

prompt_links = {
    "security_hardening": {
        "cluster": {
            "prod_safety_core": "../security_prompts.html#cluster-prompt"
        },
        "blocks": {
            "b07": "../security_prompts.html#b07",
            "b08": "../security_prompts.html#b08",
            "b09": "../security_prompts.html#b09",
            "b10": "../security_prompts.html#b10",
            "b11": "../security_prompts.html#b11"
        }
    }
}

base_css = r"""
:root{
  --bg0:#0b0b0c; --bg1:#0f0f11; --bg2:#121214;
  --panel:#161618; --panel2:#1c1c20; --panel3:#232329;
  --line:rgba(255,255,255,.10); --line2:rgba(255,255,255,.18);
  --text:#eef4fb; --muted:#c3d0e3; --muted2:#95a7c2;
  --accent:#d6b35e; --accent2:#f0d18a; --accentGlow:rgba(240,209,138,.20);
}
[data-theme="light"]{
  --bg0:#eef3f9; --bg1:#f6f9fc; --bg2:#ffffff;
  --panel:#ffffff; --panel2:#f4f7fb; --panel3:#edf2f8;
  --line:rgba(18,24,36,.12); --line2:rgba(18,24,36,.20);
  --text:#122033; --muted:#425874; --muted2:#677d98; --accentGlow:rgba(214,179,94,.14);
}
[data-preset="obsidian_gold"]{--accent:#d6b35e; --accent2:#f0d18a; --accentGlow:rgba(240,209,138,.20);}
[data-preset="graphite_cyan"]{--accent:#36c9ff; --accent2:#92e8ff; --accentGlow:rgba(54,201,255,.16);}
[data-preset="midnight_purple"]{--accent:#9b7cff; --accent2:#c9b8ff; --accentGlow:rgba(155,124,255,.16);}
[data-preset="slate_teal"]{--accent:#2fd3c5; --accent2:#93fff4; --accentGlow:rgba(47,211,197,.14);}
*{box-sizing:border-box}
html,body{height:100%}
body{
  margin:0;
  font-family: Inter, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif;
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
.sidebar a.active{
  background:radial-gradient(180px 70px at 0% 0%, color-mix(in oklab,var(--accent) 18%, transparent), transparent 68%), color-mix(in oklab,var(--panel2) 92%, transparent);
  color:var(--accent2);border-left:3px solid var(--accent);padding-left:9px;
}
.main{margin-left:240px;padding-top:96px;}
.hero{padding:34px 0 12px;}
.panel{
  background:color-mix(in oklab,var(--panel) 94%, black 6%);
  border:1px solid color-mix(in oklab,var(--chapter-color) 26%, var(--line));
  border-radius:24px;padding:24px;position:relative;overflow:hidden;
  box-shadow:0 20px 50px rgba(0,0,0,.34), 0 0 0 1px color-mix(in oklab,var(--chapter-color) 18%, transparent), inset 0 1px 0 rgba(255,255,255,.04);
}
.panel:before{
  content:"";position:absolute;inset:-1px;
  background:radial-gradient(640px 240px at 0% 0%, color-mix(in oklab,var(--chapter-color) 18%, transparent), transparent 58%);
  pointer-events:none;
}
.panel>*{position:relative}
.hero-panel:after{
  content:"";position:absolute;left:0;top:0;right:0;height:4px;
  background:linear-gradient(90deg, transparent, var(--chapter-color), transparent);
}
h1{margin:0;font-size:48px;line-height:1.06}
.subtitle{margin:14px 0 0;color:var(--muted);font-size:18px;line-height:1.75}
.section{padding:14px 0 0}
.section h2{margin:0 0 14px;font-size:32px}
.section h3{margin:0 0 12px;font-size:24px}
.section-intro{margin:0 0 18px;color:var(--muted);font-size:17px;line-height:1.72}
.grid-2{display:grid;grid-template-columns:1fr 1fr;gap:18px}
@media (max-width:980px){.grid-2{grid-template-columns:1fr}}
.kpi-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-top:20px}
@media (max-width:900px){.kpi-grid{grid-template-columns:1fr}}
.kpi{
  border-radius:18px;border:1px solid color-mix(in oklab,var(--chapter-color) 26%, var(--line));
  background:radial-gradient(240px 90px at 10% 10%, color-mix(in oklab,var(--chapter-color) 18%, transparent), transparent 65%), color-mix(in oklab,var(--panel2) 84%, transparent);
  padding:14px;
}
.kpi-label{font-size:13px;color:var(--muted2)}
.kpi-value{font-size:19px;font-weight:900;margin-top:4px}
.cluster-card{
  border-radius:24px;border:1px solid color-mix(in oklab,var(--cluster-color) 34%, var(--line));
  background:color-mix(in oklab,var(--panel3) 92%, black 4%);
  padding:18px;position:relative;overflow:hidden;margin-top:20px;
  box-shadow:0 16px 38px rgba(0,0,0,.34), 0 0 14px color-mix(in oklab,var(--cluster-color) 24%, transparent), 0 0 0 1px color-mix(in oklab,var(--cluster-color) 18%, transparent), inset 0 1px 0 rgba(255,255,255,.04);
}
.cluster-card:before{
  content:"";position:absolute;left:0;top:0;right:0;height:4px;
  background:linear-gradient(90deg, color-mix(in oklab,var(--cluster-color) 55%, transparent), var(--cluster-color), color-mix(in oklab,var(--cluster-color) 55%, transparent));
}
.cluster-card>*{position:relative}
.cluster-top{display:grid;grid-template-columns:1.15fr .85fr;gap:18px}
@media (max-width:980px){.cluster-top{grid-template-columns:1fr}}
.cluster-meta{display:flex;gap:10px;flex-wrap:wrap;color:var(--muted2);font-size:14px;margin-top:10px}
.pbar{margin-top:10px;height:14px;border-radius:999px;border:1px solid color-mix(in oklab,var(--cluster-color) 22%, var(--line));overflow:hidden;background:color-mix(in oklab,var(--panel2) 78%, transparent)}
.pbar>div{height:100%;border-radius:999px;background:linear-gradient(90deg, color-mix(in oklab,var(--cluster-color) 70%, transparent), color-mix(in oklab,var(--cluster-color) 95%, white 10%));box-shadow:0 0 0 4px color-mix(in oklab,var(--cluster-color) 16%, transparent)}
.cluster-side{
  border-radius:18px;border:1px solid color-mix(in oklab,var(--cluster-color) 22%, var(--line));
  background:color-mix(in oklab,var(--panel2) 84%, transparent);padding:14px;
}
.action-row{display:flex;gap:10px;flex-wrap:wrap;margin-top:12px}
.action-btn{
  display:inline-flex;align-items:center;justify-content:center;padding:10px 14px;border-radius:12px;text-decoration:none;font-size:14px;font-weight:800;
  border:1px solid color-mix(in oklab,var(--cluster-color) 26%, var(--line));
  background:radial-gradient(180px 70px at 0% 0%, color-mix(in oklab,var(--cluster-color) 14%, transparent), transparent 70%), color-mix(in oklab,var(--panel2) 88%, transparent);
  color:var(--text);
}
.action-btn.secondary{color:var(--muted)}
.block-grid{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:16px}
@media (max-width:980px){.block-grid{grid-template-columns:1fr}}
.block-card{
  border-radius:18px;border:1px solid color-mix(in oklab,var(--block-color) 28%, var(--line));
  background:color-mix(in oklab,var(--panel2) 86%, transparent);padding:14px;position:relative;overflow:hidden;
}
.block-card:before{
  content:"";position:absolute;left:0;top:0;right:0;height:3px;
  background:linear-gradient(90deg, color-mix(in oklab,var(--block-color) 55%, transparent), var(--block-color), color-mix(in oklab,var(--block-color) 55%, transparent));
}
.block-card>*{position:relative}
.block-top{display:flex;justify-content:space-between;gap:10px;align-items:baseline;flex-wrap:wrap}
.block-num{font-size:13px;color:var(--muted2);font-weight:800;letter-spacing:.04em}
.block-title{font-size:18px;font-weight:900;margin-top:4px}
.block-overview{margin-top:8px;color:var(--muted);font-size:15px;line-height:1.65}
.badge{
  display:inline-flex;align-items:center;gap:8px;padding:5px 10px;border-radius:999px;
  border:1px solid color-mix(in oklab,var(--block-color) 22%, var(--line));
  background:color-mix(in oklab,var(--panel2) 78%, transparent);font-size:13px;color:var(--muted);
}
.badge.finished{color:#9ff6ce}.badge.started{color:#ffe39a}.badge.planned{color:var(--muted)}
.block-progress{margin-top:10px}
.block-progress .smallbar{
  height:10px;border-radius:999px;border:1px solid color-mix(in oklab,var(--block-color) 20%, var(--line));overflow:hidden;background:color-mix(in oklab,var(--panel2) 80%, transparent);
}
.block-progress .smallbar > div{
  height:100%;border-radius:999px;background:linear-gradient(90deg, color-mix(in oklab,var(--block-color) 70%, transparent), color-mix(in oklab,var(--block-color) 95%, white 10%));
}
.block-progress .pct{margin-top:6px;color:var(--muted2);font-size:13px}
.footer-space{height:40px}
"""

theme_script = r"""
<script>
const root = document.documentElement;
const presetSelect = document.getElementById("presetSelect");
const themeBtn = document.getElementById("themeBtn");
const savedTheme = localStorage.getItem("arc_scc_theme");
const savedPreset = localStorage.getItem("arc_scc_preset");
if(savedTheme === "light" || savedTheme === "dark") root.setAttribute("data-theme", savedTheme);
if(savedPreset) root.setAttribute("data-preset", savedPreset);
if(presetSelect) presetSelect.value = root.getAttribute("data-preset") || "obsidian_gold";
if(presetSelect){
  presetSelect.addEventListener("change", ()=>{
    root.setAttribute("data-preset", presetSelect.value);
    localStorage.setItem("arc_scc_preset", presetSelect.value);
  });
}
if(themeBtn){
  themeBtn.addEventListener("click", ()=>{
    const cur = root.getAttribute("data-theme") || "dark";
    const next = cur === "dark" ? "light" : "dark";
    root.setAttribute("data-theme", next);
    localStorage.setItem("arc_scc_theme", next);
  });
}
</script>
"""

for chapter in progress["chapters"]:
    cid = chapter["id"]
    title = chapter["title"]
    details = chapter_details.get(cid, {})
    cmeta = meta.get(cid, {"cluster_order": [], "clusters": {}, "blocks": {}})
    subtitle = details.get("subtitle", "")
    description = details.get("description", "")
    goal = details.get("goal", "")
    total_blocks = chapter["total_blocks"]
    total_clusters = len(chapter["clusters"])

    chapter_color = cmeta.get("clusters", {})
    order = cmeta.get("cluster_order", [c["id"] for c in chapter["clusters"]])
    cluster_map = {c["id"]: c for c in chapter["clusters"]}

    cluster_sections = []
    block_color_palette = ["#8ee3f5", "#9b7cff", "#3fe3b5", "#ffb84d", "#ff4d6d", "#d6b35e", "#60a5fa", "#f472b6"]

    for cluster_id in order:
        if cluster_id not in cluster_map:
            continue
        cluster = cluster_map[cluster_id]
        cm = cmeta.get("clusters", {}).get(cluster_id, {})
        cluster_color = cm.get("color", "#d6b35e")
        cluster_title = cm.get("title", cluster["title"])
        cluster_overview = cm.get("overview", "")
        cluster_duration = cm.get("duration", "TBD")

        cluster_prompt_action = '<span class="action-btn secondary">Cluster prompt volgt later</span>'
        if cid in prompt_links and cluster_id in prompt_links[cid]["cluster"]:
            cluster_prompt_action = f'<a class="action-btn" href="{prompt_links[cid]["cluster"][cluster_id]}">Open Cluster Prompt</a>'

        block_cards = []
        for idx, b in enumerate(cluster["blocks"]):
            bm = cmeta.get("blocks", {}).get(b["id"], {})
            block_num = bm.get("number", b["id"].upper())
            block_overview = bm.get("overview", "Overzicht volgt later.")
            block_color = block_color_palette[idx % len(block_color_palette)]
            block_pct = 100 if b["status"] == "finished" else 50 if b["status"] == "started" else 0

            block_prompt_action = '<span class="action-btn secondary">Block prompt volgt later</span>'
            if cid in prompt_links and b["id"] in prompt_links[cid]["blocks"]:
                block_prompt_action = f'<a class="action-btn" href="{prompt_links[cid]["blocks"][b["id"]]}">Open Block Prompt</a>'

            block_cards.append(f"""
<div class="block-card" style="--block-color:{block_color}">
  <div class="block-top">
    <div>
      <div class="block-num">{escape(block_num)}</div>
      <div class="block-title">{escape(b["title"])}</div>
    </div>
    <div class="badge {escape(b["status"])}">{escape(b["status"])}</div>
  </div>
  <div class="block-overview">{escape(block_overview)}</div>
  <div class="block-progress">
    <div class="smallbar"><div style="width:{block_pct}%"></div></div>
    <div class="pct">{block_pct}% block progress</div>
  </div>
  <div class="action-row">
    {block_prompt_action}
  </div>
</div>
""")

        cluster_sections.append(f"""
<section class="cluster-card" style="--cluster-color:{cluster_color}">
  <div class="cluster-top">
    <div>
      <h3>{escape(cluster_title)}</h3>
      <p class="section-intro">{escape(cluster_overview)}</p>
      <div class="cluster-meta">
        <span>Status: {escape(cluster["status"])}</span>
        <span>{cluster["done_blocks"]}/{cluster["total_blocks"]} blocks done</span>
        <span>Cluster duration: {escape(cluster_duration)}</span>
      </div>
      <div class="pbar"><div style="width:{cluster["progress_percent"]}%"></div></div>
    </div>
    <div class="cluster-side">
      <div><strong>Cluster Prompt</strong></div>
      <p class="section-intro" style="font-size:15px;margin-top:8px">Gebruik eerst de cluster prompt als je het cluster als geheel wilt oppakken. Werk daarna op block-niveau verder.</p>
      <div class="action-row">{cluster_prompt_action}</div>
    </div>
  </div>

  <div class="block-grid">
    {''.join(block_cards)}
  </div>
</section>
""")

    html = f"""<!DOCTYPE html>
<html lang="en" data-theme="dark" data-preset="obsidian_gold" style="--chapter-color:{'#d6b35e'}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)} · The Arc Strategic Control Center</title>
<style>{base_css}</style>
</head>
<body>

<div class="topbar">
  <div class="wrap">
    <div class="topbar-inner">
      <div class="logo-wrap">
        <div class="logo">The Arc Strategic Control Center</div>
        <div class="logo-sub">{escape(title)}</div>
      </div>

      <div class="nav">
        <a href="../index.html">Home</a>
        <a href="../index.html#chapters" class="active">Chapters</a>
        <a href="../index.html#architecture">Architecture</a>
        <a href="../index.html#roadmap">Roadmap</a>
        <a href="../prompts.html">Prompts</a>

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
  <h3>Navigation</h3>
  <a href="../index.html">Home</a>
  <a href="../index.html#chapters" class="active">Chapters</a>
  <a href="../index.html#architecture">Architecture</a>
  <a href="../index.html#roadmap">Roadmap</a>
  <a href="../prompts.html">Prompt Library</a>

  <h3>Chapters</h3>
  <a href="./platform_runtime.html" {"class='active'" if cid=="platform_runtime" else ""}>Platform & Runtime</a>
  <a href="./security_hardening.html" {"class='active'" if cid=="security_hardening" else ""}>Security Hardening</a>
  <a href="./model_runtime.html" {"class='active'" if cid=="model_runtime" else ""}>Model Runtime</a>
  <a href="./data_memory.html" {"class='active'" if cid=="data_memory" else ""}>Data & Memory</a>
  <a href="./agent_logic.html" {"class='active'" if cid=="agent_logic" else ""}>Agent Logic</a>
  <a href="./observability.html" {"class='active'" if cid=="observability" else ""}>Observability</a>
  <a href="./control_center.html" {"class='active'" if cid=="control_center" else ""}>Control Center UI</a>
</div>

<div class="main">
  <section class="hero">
    <div class="wrap">
      <section class="panel hero-panel">
        <h1>{escape(title)}</h1>
        <p class="subtitle">{escape(subtitle)}</p>
        <div class="kpi-grid">
          <div class="kpi">
            <div class="kpi-label">Status</div>
            <div class="kpi-value">{escape(chapter["status"])}</div>
          </div>
          <div class="kpi">
            <div class="kpi-label">Blocks Done</div>
            <div class="kpi-value">{chapter["done_blocks"]}/{chapter["total_blocks"]}</div>
          </div>
          <div class="kpi">
            <div class="kpi-label">Progress</div>
            <div class="kpi-value">{chapter["progress_percent"]}%</div>
          </div>
        </div>
      </section>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <div class="grid-2">
        <section class="panel">
          <h2>Overview</h2>
          <p class="section-intro">{escape(description)}</p>
        </section>
        <section class="panel">
          <h2>Goal</h2>
          <p class="section-intro">{escape(goal)}</p>
        </section>
      </div>

      <section class="section">
        <section class="panel">
          <h2>Chapter Structure</h2>
          <p class="section-intro">
            Dit hoofdstuk bestaat uit <strong>{total_blocks}</strong> blokken en is onderverdeeld in <strong>{total_clusters}</strong> cluster(s).
            Een cluster kan één lang blok zijn of meerdere blokken bevatten die logisch samen horen. Clusters worden getoond van minst naar meest tijdsintensief om te realiseren.
          </p>
        </section>
      </section>

      <section class="section">
        <h2>Clusters</h2>
        <p class="section-intro">Werk eerst op cluster-niveau en daarna op block-niveau. Cluster prompts en block prompts zijn acties die je direct naar de juiste prompt in de promptflow brengen.</p>
        {''.join(cluster_sections)}
      </section>
    </div>
  </section>

  <div class="footer-space"></div>
</div>

{theme_script}
</body>
</html>
"""
    (chapters_dir / f"{cid}.html").write_text(html, encoding="utf-8")

print("Rebuilt chapter pages v5")
