#!/usr/bin/env python3
import json
from pathlib import Path
from html import escape

BASE = Path(__file__).resolve().parent
roadmap_path = BASE / "data" / "roadmap.json"
chapters_dir = BASE / "chapters"
chapters_dir.mkdir(parents=True, exist_ok=True)

roadmap = json.loads(roadmap_path.read_text(encoding="utf-8"))
project = roadmap.get("project", "The Arc Strategic Control Center")
chapters = roadmap.get("chapters", [])

chapter_details = {
    "platform_runtime": {
        "subtitle": "Foundation layer for OpenClaw execution",
        "description": "Dit hoofdstuk bevat de fundering van het platform: core installatie, runtime, runner, environment loading, isolation en worker cluster voorbereiding.",
        "goal": "Een stabiele en herhaalbare execution base neerzetten waarop alle volgende hoofdstukken veilig kunnen bouwen.",
        "clusters": [
            {
                "name": "Core Runtime Foundation",
                "status": "finished",
                "progress": 100,
                "blocks": [
                    "OpenClaw core installatie",
                    "Systemd runtime services",
                    "Hardened agent runner",
                    "Central env + allowlists",
                    "Linux user isolation",
                    "Worker skeleton cluster"
                ],
                "prompt": "Werk verder aan Hoofdstuk Platform & Runtime. Verifieer of alle runtime-onderdelen stabiel, idempotent en goed gedocumenteerd zijn. Controleer systemd services, runner, env model, isolation en worker skeletons. Lever ontbrekende docs/tests op."
            }
        ],
        "done": [
            "OpenClaw core installatie gereed",
            "Nova en Flux runtime operationeel",
            "Hardened runner aanwezig",
            "Central env model staat",
            "Worker cluster voorbereid"
        ],
        "remaining": [
            "Alleen onderhoud / verificatie",
            "Later koppeling met observability"
        ]
    },
    "security_hardening": {
        "subtitle": "Prod readiness, default deny and response controls",
        "description": "Dit hoofdstuk maakt de infrastructuur productierijp met secrets hardening, egress control, incident response, kill switch en monitoring/backpressure.",
        "goal": "Een veilige, auditbare en gecontroleerde runtime neerzetten voordat het systeem live gaat.",
        "clusters": [
            {
                "name": "Prod Safety Core",
                "status": "planned",
                "progress": 0,
                "blocks": [
                    "Baseline inventory",
                    "Monitoring / runtime safety",
                    "Incident response / kill switch",
                    "Secrets hardening",
                    "Internet / egress policy"
                ],
                "prompt": "JE BENT OPENCLAW PROD SAFETY CORE ENGINEER. Werk binnen Hoofdstuk Security Hardening aan de cluster Prod Safety Core. Lever baseline inventory, secrets hardening, egress control, incident response, kill switch, monitoring en queue/backpressure op in docs/scripts/tests. Werk stap voor stap, met concrete terminalacties voor de gebruiker."
            }
        ],
        "done": [],
        "remaining": [
            "Baseline inventory uitvoeren",
            "Secrets hardening implementeren",
            "Default deny egress policy invoeren",
            "Kill switch en incident runbooks bouwen",
            "Monitoring + queue/backpressure opleveren"
        ]
    },
    "model_runtime": {
        "subtitle": "Local and cloud model execution layer",
        "description": "Dit hoofdstuk gaat over Ollama, externe providers, model switching per agent, fallback logic en een provider abstraction layer.",
        "goal": "Een flexibele model runtime bouwen waarbij agents tussen lokale en externe modellen kunnen wisselen zonder logic te herschrijven.",
        "clusters": [
            {
                "name": "Ollama & Provider Layer",
                "status": "planned",
                "progress": 0,
                "blocks": [
                    "Ollama installatie & service setup",
                    "Model registry",
                    "Provider abstraction",
                    "Fallback logic local/cloud",
                    "Per-agent model assignment"
                ],
                "prompt": "JE BENT OPENCLAW MODEL RUNTIME ENGINEER. Werk binnen Hoofdstuk Model Runtime & Providers aan Ollama, provider abstraction, model switching en fallback logic. Ontwerp een lokale + externe providerlaag die per agent flexibel instelbaar is."
            }
        ],
        "done": [],
        "remaining": [
            "Ollama integratie ontwerpen",
            "Provider registry bouwen",
            "Model switching per agent uitwerken",
            "Fallback strategy documenteren"
        ]
    },
    "data_memory": {
        "subtitle": "Databases for agents, memory and system state",
        "description": "Dit hoofdstuk definieert de data- en memorylaag van The Arc: agent management database, memory database, retrieval, embeddings en seed knowledge.",
        "goal": "Agents voorzien van consistente state, geheugen en bestuurbare data-architectuur.",
        "clusters": [
            {
                "name": "Agent DB + Memory Layer",
                "status": "planned",
                "progress": 0,
                "blocks": [
                    "Agent management schema",
                    "Memory architecture",
                    "Embedding/vector strategy",
                    "Shared world memory",
                    "Per-agent memory links"
                ],
                "prompt": "JE BENT OPENCLAW DATA & MEMORY ARCHITECT. Werk binnen Hoofdstuk Data & Memory Architecture aan agent management database, memory model, retrieval, vector storage en per-agent memory linking. Maak een praktisch ontwerp voor een schaalbare eerste versie."
            }
        ],
        "done": [],
        "remaining": [
            "Databasekeuze vastleggen",
            "Agent schema ontwerpen",
            "Memory types definiëren",
            "Retrieval + population strategy uitwerken"
        ]
    },
    "agent_logic": {
        "subtitle": "Roles, skills, workflows and swarm logic",
        "description": "Dit hoofdstuk beschrijft agentrollen, communicatieprotocollen, skill governance, workflow routing en swarm coordination.",
        "goal": "Agents smal, effectief en veilig laten samenwerken zonder skill overkill.",
        "clusters": [
            {
                "name": "Roles, Skills & Swarm Core",
                "status": "planned",
                "progress": 0,
                "blocks": [
                    "Agent roles framework",
                    "Communication protocol",
                    "Workflow dispatcher",
                    "Skill registry",
                    "Swarm coordination"
                ],
                "prompt": "JE BENT OPENCLAW AGENT LOGIC ENGINEER. Werk binnen Hoofdstuk Agent Logic, Skills & Swarm aan agent roles, communication protocol, workflow dispatching, skill registry en swarm coordination. Focus op veilige en effectieve agent-specialisatie."
            }
        ],
        "done": [],
        "remaining": [
            "Rollenmodel definiëren",
            "Skill registry ontwerpen",
            "Maximale skillset per agent bepalen",
            "Workflow routing en swarm patterns uitwerken"
        ]
    },
    "observability": {
        "subtitle": "Usage, tracing, cost and health visibility",
        "description": "Dit hoofdstuk geeft zicht op API usage, kosten, health, tracing, provider calls, latency en operationele signalen.",
        "goal": "Weten wat draait, wat het kost, wat faalt en waarom.",
        "clusters": [
            {
                "name": "Observability & Cost Ledger",
                "status": "planned",
                "progress": 0,
                "blocks": [
                    "API inventory",
                    "Usage ledger",
                    "Cost calculations",
                    "Latency/error tracing",
                    "Per agent / per workflow reporting"
                ],
                "prompt": "JE BENT OPENCLAW OBSERVABILITY & COST ENGINEER. Werk binnen Hoofdstuk Observability & API Cost Control aan API inventory, usage logging, cost ledger, latency/error tracing en reporting per agent, provider en workflow."
            }
        ],
        "done": [],
        "remaining": [
            "API ledger model ontwerpen",
            "Cost per provider zichtbaar maken",
            "Dag/week/maand reporting bouwen",
            "Tracing model uitwerken"
        ]
    },
    "control_center": {
        "subtitle": "Roadmap site now, operations dashboard later",
        "description": "Dit hoofdstuk gaat over de UI van The Arc Strategic Control Center: homepage, hoofdstukpagina’s, prompt library, diagrams en later live operations widgets.",
        "goal": "Een centrale bestuurbare interface maken die roadmap-first begint en operations-ready eindigt.",
        "clusters": [
            {
                "name": "Strategic Control Center UI",
                "status": "started",
                "progress": 20,
                "blocks": [
                    "Homepage dashboard",
                    "Chapter pages",
                    "Prompt library",
                    "Progress visualization",
                    "Operations-ready layout"
                ],
                "prompt": "JE BENT THE ARC STRATEGIC CONTROL CENTER UI ARCHITECT. Werk binnen Hoofdstuk Strategic Control Center UI aan de lokale site-architectuur, hoofdstukpagina’s, progress visualisaties, prompt library en voorbereidingen voor een later operations dashboard."
            }
        ],
        "done": [
            "Homepage basis opgezet",
            "Roadmap datafile aanwezig"
        ],
        "remaining": [
            "Hoofdstukpagina’s genereren",
            "Prompt library toevoegen",
            "Charts uitbreiden",
            "Operations-ready modules voorbereiden"
        ]
    }
}

base_css = """
:root{
  --sans: ui-sans-serif, system-ui, -apple-system, Segoe UI, Inter, Roboto, Helvetica, Arial;
  --radius: 20px;
  --line: rgba(255,255,255,.10);
  --line2: rgba(255,255,255,.18);
  --text: #eef2f7;
  --muted: #b9c4d8;
  --muted2: #93a3bf;
  --bg0: #121a24;
  --bg1: #162231;
  --panel: rgba(18,24,36,.78);
  --panel2: rgba(18,24,36,.62);
  --card: rgba(22,30,44,.78);
  --shadow: 0 18px 48px rgba(0,0,0,.35);
  --shadow2: 0 10px 28px rgba(0,0,0,.25);
  --accent:#d6b35e;
  --accent2:#f0d18a;
  --accentGlow: rgba(240,209,138,.16);
  --accentLine: rgba(214,179,94,.48);
}
[data-theme="light"]{
  --bg0:#e7edf5;
  --bg1:#f2f6fb;
  --panel: rgba(255,255,255,.88);
  --panel2: rgba(255,255,255,.78);
  --card: rgba(255,255,255,.92);
  --line: rgba(18,24,36,.14);
  --line2: rgba(18,24,36,.22);
  --text:#0f172a;
  --muted:#2c3c55;
  --muted2:#4e6283;
  --shadow: 0 18px 46px rgba(18,24,36,.14);
  --shadow2: 0 10px 28px rgba(18,24,36,.10);
}
[data-preset="obsidian_gold"]{
  --accent:#d6b35e; --accent2:#f0d18a; --accentGlow: rgba(240,209,138,.16); --accentLine: rgba(214,179,94,.48);
}
[data-preset="graphite_cyan"]{
  --accent:#36c9ff; --accent2:#92e8ff; --accentGlow: rgba(54,201,255,.14); --accentLine: rgba(54,201,255,.42);
}
[data-preset="midnight_purple"]{
  --accent:#9b7cff; --accent2:#c9b8ff; --accentGlow: rgba(155,124,255,.14); --accentLine: rgba(155,124,255,.40);
}
[data-preset="slate_teal"]{
  --accent:#2fd3c5; --accent2:#93fff4; --accentGlow: rgba(47,211,197,.12); --accentLine: rgba(47,211,197,.38);
}
*{box-sizing:border-box}
html,body{height:100%}
body{
  margin:0;
  font-family: var(--sans);
  color: var(--text);
  background:
    radial-gradient(1200px 700px at 85% -10%, var(--accentGlow), transparent 60%),
    linear-gradient(180deg, var(--bg0), var(--bg1));
}
.wrap{max-width:1200px;margin:0 auto;padding:0 18px}
.topbar{
  position: sticky; top:0; z-index:50;
  background: color-mix(in oklab,var(--panel) 72%, transparent);
  backdrop-filter: blur(12px);
  border-bottom:1px solid var(--line);
}
.topbar-inner{
  display:flex;align-items:center;justify-content:space-between;gap:14px;padding:14px 0;
}
.brand-title .h{font-size:18px;font-weight:850}
.brand-title .s{font-size:13px;color:var(--muted2)}
.controls{display:flex;gap:10px;flex-wrap:wrap}
.btn, select{
  font-size:14px;padding:8px 12px;border-radius:999px;border:1px solid var(--line);
  background: color-mix(in oklab,var(--panel2) 72%, transparent);
  color: var(--muted);
  cursor:pointer;
}
.hero{padding:24px 0 12px}
.panel{
  border-radius: var(--radius);
  border:1px solid var(--line);
  background: var(--panel);
  box-shadow: var(--shadow);
  padding:18px;
  overflow:hidden;
  position:relative;
  margin-top:14px;
}
.panel:before{
  content:""; position:absolute; inset:-1px;
  background: radial-gradient(600px 220px at 0% 0%, var(--accentGlow), transparent 58%);
  pointer-events:none;
}
.panel > *{position:relative}
h1{margin:0;font-size:30px;line-height:1.12}
h2{margin:0 0 8px;font-size:22px}
h3{margin:0 0 8px;font-size:17px}
.subtitle{margin:10px 0 0;color:var(--muted);font-size:15.5px}
.divider{height:1px;background:linear-gradient(90deg,transparent,var(--line2),transparent);margin:14px 0}
.muted{color:var(--muted);font-size:14.5px}
.muted2{color:var(--muted2);font-size:13.5px}
.row{display:flex;justify-content:space-between;gap:12px;align-items:baseline;flex-wrap:wrap}
.badge{
  display:inline-flex;align-items:center;gap:8px;
  padding:5px 10px;border-radius:999px;border:1px solid var(--line);
  background: color-mix(in oklab,var(--panel2) 72%, transparent);
  font-size:13px;color:var(--muted);
}
.pbar{height:14px;border-radius:999px;border:1px solid var(--line);background:color-mix(in oklab,var(--panel2) 72%,transparent);overflow:hidden}
.pbar-in{
  height:100%;
  border-radius:999px;
  background:linear-gradient(90deg,var(--accentLine),color-mix(in oklab,var(--accent2) 70%, transparent));
  box-shadow:0 0 0 4px color-mix(in oklab,var(--accentGlow) 65%, transparent);
}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:14px}
@media (max-width:980px){.grid{grid-template-columns:1fr}}
ul{margin:8px 0 0 18px;padding:0}
li{margin:6px 0}
.prompt{
  white-space:pre-wrap;
  border-radius:16px;
  border:1px solid var(--line);
  background: color-mix(in oklab,var(--panel2) 72%, transparent);
  padding:14px;
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
  font-size:13.5px;
  line-height:1.55;
}
a.back{
  display:inline-block;
  margin-top:12px;
  color: var(--accent2);
  text-decoration:none;
  font-weight:800;
}
"""

script_block = """
<script>
const root = document.documentElement;
const presetSelect = document.getElementById('presetSelect');
const themeBtn = document.getElementById('themeBtn');

const savedTheme = localStorage.getItem('arc_scc_theme');
const savedPreset = localStorage.getItem('arc_scc_preset');
if (savedTheme === 'light' || savedTheme === 'dark') root.setAttribute('data-theme', savedTheme);
if (savedPreset) root.setAttribute('data-preset', savedPreset);
presetSelect.value = root.getAttribute('data-preset') || 'obsidian_gold';

presetSelect.addEventListener('change', function(){
  root.setAttribute('data-preset', presetSelect.value);
  localStorage.setItem('arc_scc_preset', presetSelect.value);
});

themeBtn.addEventListener('click', function(){
  const cur = root.getAttribute('data-theme') || 'dark';
  const next = cur === 'dark' ? 'light' : 'dark';
  root.setAttribute('data-theme', next);
  localStorage.setItem('arc_scc_theme', next);
});
</script>
"""

for ch in chapters:
    cid = ch["id"]
    title = ch["title"]
    details = chapter_details.get(cid, {
        "subtitle": "Chapter details",
        "description": "Nog uit te werken.",
        "goal": "Nog uit te werken.",
        "clusters": [],
        "done": [],
        "remaining": []
    })

    progress = int(ch.get("progress", 0))
    duration = ch.get("duration_hours", 0)
    status = ch.get("status", "planned")

    cluster_html = []
    for cluster in details["clusters"]:
        blocks_html = "".join(f"<li>{escape(b)}</li>" for b in cluster["blocks"])
        cluster_html.append(f"""
<section class="panel">
  <div class="row">
    <h3>{escape(cluster["name"])}</h3>
    <div class="badge">{escape(cluster["status"])} · {escape(str(cluster["progress"]))}%</div>
  </div>
  <div class="divider"></div>
  <div class="muted"><b>Blocks</b></div>
  <ul>{blocks_html}</ul>
  <div class="divider"></div>
  <div class="muted"><b>Prompt for new chat</b></div>
  <div class="prompt">{escape(cluster["prompt"])}</div>
</section>
""")

    done_html = "".join(f"<li>{escape(x)}</li>" for x in details["done"])
    remaining_html = "".join(f"<li>{escape(x)}</li>" for x in details["remaining"])

    html = f"""<!doctype html>
<html lang="en" data-theme="dark" data-preset="obsidian_gold">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>{escape(title)} · {escape(project)}</title>
  <style>{base_css}</style>
</head>
<body>
  <div class="topbar">
    <div class="wrap">
      <div class="topbar-inner">
        <div class="brand-title">
          <div class="h">{escape(project)}</div>
          <div class="s">{escape(title)}</div>
        </div>
        <div class="controls">
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

  <header class="hero">
    <div class="wrap">
      <section class="panel">
        <h1>{escape(title)}</h1>
        <p class="subtitle">{escape(details["subtitle"])}</p>
        <div class="divider"></div>

        <div class="grid">
          <div>
            <h2>Chapter Overview</h2>
            <div class="muted">{escape(details["description"])}</div>
            <div class="divider"></div>
            <div class="muted"><b>Goal</b></div>
            <div class="muted">{escape(details["goal"])}</div>
          </div>
          <div>
            <h2>Status & Progress</h2>
            <div class="row">
              <div class="muted">Status</div>
              <div class="badge">{escape(status)}</div>
            </div>
            <div class="divider"></div>
            <div class="row">
              <div class="muted">Progress</div>
              <div class="muted"><b>{progress}%</b></div>
            </div>
            <div class="pbar" style="margin-top:8px"><div class="pbar-in" style="width:{progress}%"></div></div>
            <div class="divider"></div>
            <div class="muted2">Estimated duration: {duration}h</div>
          </div>
        </div>

        <a class="back" href="../index.html">← Back to homepage</a>
      </section>

      <section class="grid">
        <section class="panel">
          <h2>Done</h2>
          <ul>{done_html}</ul>
        </section>
        <section class="panel">
          <h2>Remaining</h2>
          <ul>{remaining_html}</ul>
        </section>
      </section>

      {''.join(cluster_html)}
    </div>
  </header>

  {script_block}
</body>
</html>
"""
    out = chapters_dir / f"{cid}.html"
    out.write_text(html, encoding="utf-8")

print(f"Generated {len(chapters)} chapter pages in {chapters_dir}")
