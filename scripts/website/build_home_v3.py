from pathlib import Path

base = Path.home() / "arc_strategic_control_center"
index = base / "index.html"

html = r"""<!DOCTYPE html>
<html lang="en" data-theme="dark" data-preset="obsidian_gold">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>The Arc Strategic Control Center</title>

<style>
:root{
  --bg0:#0b0b0c;
  --bg1:#0f0f11;
  --panel:#161618;
  --panel2:#1c1c20;
  --card:#232329;
  --line:rgba(255,255,255,.10);
  --text:#eef4fb;
  --muted:#c3d0e3;
  --muted2:#95a7c2;

  --accent:#d6b35e;
  --accent2:#f0d18a;
  --accentGlow:rgba(240,209,138,.20);

  --runtime:#36c9ff;
  --security:#3fe3b5;
  --models:#9b7cff;
  --memory:#4ea8de;
  --swarm:#ff4d6d;
  --observe:#ff9f43;
  --ui:#d6b35e;
  --command:#7fb8ff;
}

[data-theme="light"]{
  --bg0:#f8fbff;
  --bg1:#f2f7fd;
  --panel:#ffffff;
  --panel2:#edf4fb;
  --card:#ffffff;
  --line:rgba(16,24,40,.10);
  --text:#132033;
  --muted:#51627b;
  --muted2:#6d7f99;
  --accentGlow:rgba(214,179,94,.10);
}

[data-preset="obsidian_gold"]{
  --accent:#d6b35e; --accent2:#f0d18a; --accentGlow:rgba(240,209,138,.20);
}
[data-preset="graphite_cyan"]{
  --accent:#36c9ff; --accent2:#92e8ff; --accentGlow:rgba(54,201,255,.14);
}
[data-preset="midnight_purple"]{
  --accent:#9b7cff; --accent2:#c9b8ff; --accentGlow:rgba(155,124,255,.14);
}
[data-preset="slate_teal"]{
  --accent:#2fd3c5; --accent2:#93fff4; --accentGlow:rgba(47,211,197,.12);
}

*{box-sizing:border-box}
html,body{height:100%}
body{
  margin:0;
  font-family: Inter, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif;
  color:var(--text);
  background:
    radial-gradient(1200px 700px at 85% -10%, var(--accentGlow), transparent 60%),
    linear-gradient(180deg, var(--bg0), var(--bg1));
}

.wrap{max-width:1320px;margin:0 auto;padding:0 28px}
.topbar{
  position:sticky;top:0;z-index:50;
  background:color-mix(in oklab,var(--panel) 82%, transparent);
  backdrop-filter:blur(12px);
  border-bottom:1px solid var(--line);
}
.topbar-inner{
  display:flex;justify-content:space-between;align-items:center;gap:16px;padding:16px 0;
}
.logo{
  font-size:22px;
  font-weight:900;
  letter-spacing:.2px;
}
.logo-sub{
  font-size:13px;
  color:var(--muted2);
  margin-top:4px;
}
.nav{
  display:flex;
  gap:10px;
  flex-wrap:wrap;
  align-items:center;
}
.nav a,.btn,select{
  text-decoration:none;
  color:var(--muted);
  font-size:14px;
  padding:9px 13px;
  border-radius:999px;
  border:1px solid var(--line);
  background:color-mix(in oklab,var(--panel2) 74%, transparent);
  cursor:pointer;
}

.hero{
  padding:54px 0 20px;
}
.hero-grid{
  display:grid;
  grid-template-columns:1.2fr .8fr;
  gap:18px;
}
@media (max-width: 980px){
  .hero-grid{grid-template-columns:1fr}
}

.panel{
  background:color-mix(in oklab,var(--panel) 88%, transparent);
  border:1px solid var(--line);
  border-radius:22px;
  padding:24px;
  position:relative;
  overflow:hidden;
  box-shadow:0 18px 48px rgba(0,0,0,.18);
}
.panel:before{
  content:"";
  position:absolute;inset:-1px;
  background:
    radial-gradient(640px 220px at 0% 0%, var(--accentGlow), transparent 60%);
  opacity:.95;
  pointer-events:none;
}
.panel>*{position:relative}

h1{
  margin:0;
  font-size:48px;
  line-height:1.05;
  letter-spacing:.2px;
}
.hero p{
  margin:14px 0 0;
  font-size:18px;
  color:var(--muted);
  line-height:1.7;
}
.kpi{
  display:grid;
  grid-template-columns:repeat(2,1fr);
  gap:12px;
  margin-top:18px;
}
.kpi-box{
  border-radius:18px;
  border:1px solid var(--line);
  background:color-mix(in oklab,var(--panel2) 78%, transparent);
  padding:14px;
}
.kpi-label{font-size:13px;color:var(--muted2)}
.kpi-value{font-size:18px;font-weight:900;margin-top:4px}

.section{
  padding:8px 0 0;
}
.section h2{
  font-size:30px;
  margin:0 0 16px;
}
.section-intro{
  color:var(--muted);
  font-size:17px;
  margin:0 0 14px;
  line-height:1.7;
}

.chapter-grid{
  display:grid;
  grid-template-columns:repeat(3,1fr);
  gap:18px;
}
@media (max-width:1100px){.chapter-grid{grid-template-columns:repeat(2,1fr)}}
@media (max-width:760px){.chapter-grid{grid-template-columns:1fr}}

.chapter-card{
  border-radius:22px;
  border:1px solid var(--line);
  background:color-mix(in oklab,var(--card) 92%, transparent);
  padding:18px;
  position:relative;
  overflow:hidden;
  text-decoration:none;
  color:inherit;
  box-shadow:0 12px 28px rgba(0,0,0,.14);
  transition:transform .15s ease, border-color .15s ease;
}
.chapter-card:hover{
  transform:translateY(-3px);
  border-color:color-mix(in oklab,var(--c) 45%, var(--line));
}
.chapter-card:before{
  content:"";
  position:absolute;left:0;top:0;right:0;height:4px;
  background:linear-gradient(90deg, transparent, var(--c), transparent);
  opacity:.95;
}
.chapter-card:after{
  content:"";
  position:absolute;inset:-1px;
  background:radial-gradient(560px 220px at 0% 0%, color-mix(in oklab,var(--c) 18%, transparent), transparent 62%);
  pointer-events:none;
}
.chapter-card>*{position:relative}
.chapter-title{
  font-size:21px;
  font-weight:900;
  margin:0;
}
.chapter-desc{
  margin:10px 0 0;
  color:var(--muted);
  font-size:16px;
  line-height:1.65;
}
.meta{
  display:flex;
  justify-content:space-between;
  align-items:baseline;
  gap:12px;
  margin-top:14px;
  color:var(--muted2);
  font-size:14px;
}
.pbar{
  margin-top:10px;
  height:14px;
  border-radius:999px;
  border:1px solid var(--line);
  overflow:hidden;
  background:color-mix(in oklab,var(--panel2) 76%, transparent);
}
.pbar > div{
  height:100%;
  border-radius:999px;
  background:linear-gradient(90deg, color-mix(in oklab,var(--c) 68%, transparent), color-mix(in oklab,var(--c) 95%, white 8%));
  box-shadow:0 0 0 4px color-mix(in oklab,var(--c) 14%, transparent);
}

.layout-grid{
  display:grid;
  grid-template-columns:1fr 1fr;
  gap:18px;
}
@media (max-width:980px){.layout-grid{grid-template-columns:1fr}}

.svg-card{
  background:color-mix(in oklab,var(--panel) 92%, transparent);
  border:1px solid var(--line);
  border-radius:24px;
  padding:24px;
  box-shadow:0 18px 48px rgba(0,0,0,.18);
}
.svg-card h3{
  margin:0 0 10px;
  font-size:26px;
  line-height:1.2;
}
.svg-card p{
  margin:0 0 16px;
  color:var(--muted);
  font-size:17px;
  line-height:1.65;
}
.svg-card svg{
  width:100%;
  height:auto;
  display:block;
  overflow:visible;
}

.step-list{
  display:grid;
  gap:12px;
}
.step{
  border-radius:18px;
  border:1px solid var(--line);
  background:color-mix(in oklab,var(--panel2) 76%, transparent);
  padding:14px 16px;
  font-size:17px;
  font-weight:800;
}
.footer-space{height:36px}
</style>
</head>
<body>

<div class="topbar">
  <div class="wrap">
    <div class="topbar-inner">
      <div>
        <div class="logo">The Arc Strategic Control Center</div>
        <div class="logo-sub">Architecture, Governance & Deployment Hub</div>
      </div>

      <div class="nav">
        <a href="#home">Home</a>
        <a href="#chapters">Chapters</a>
        <a href="#architecture">Architecture</a>
        <a href="#roadmap">Roadmap</a>
        <a href="./chapters/control_center.html">UI Chapter</a>

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

<section class="hero" id="home">
  <div class="wrap">
    <div class="hero-grid">
      <div class="panel">
        <h1>The Arc Strategic<br>Control Center</h1>
        <p>
          Dit is het centrale overzichtspunt voor het volledige Arc project:
          platform, security, models, data, memory, swarm skills, observability en UI.
          Doel is om snel te kunnen scannen waar we staan, wat nog moet gebeuren en
          welke route het snelst naar live leidt.
        </p>

        <div class="kpi">
          <div class="kpi-box">
            <div class="kpi-label">Current Focus</div>
            <div class="kpi-value">Security Hardening</div>
          </div>
          <div class="kpi-box">
            <div class="kpi-label">Active Block</div>
            <div class="kpi-value">Prod Safety Core</div>
          </div>
          <div class="kpi-box">
            <div class="kpi-label">Overall Progress</div>
            <div class="kpi-value">60%</div>
          </div>
          <div class="kpi-box">
            <div class="kpi-label">Realistic Duration</div>
            <div class="kpi-value">190h</div>
          </div>
        </div>
      </div>

      <div class="panel">
        <h2 style="font-size:30px;margin:0 0 10px">Quick Read</h2>
        <p class="section-intro">
          In één oogopslag:
        </p>
        <div class="step-list">
          <div class="step">1. Platform & Runtime is grotendeels gereed</div>
          <div class="step">2. Security Hardening is de volgende kritieke fase</div>
          <div class="step">3. Daarna volgen Models, Data/Memory en Agent Logic</div>
          <div class="step">4. Observability en UI maken het live-ready</div>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section" id="chapters">
  <div class="wrap">
    <h2>Chapter Navigation</h2>
    <p class="section-intro">
      Gebruik deze hoofdstukken als hoofdroute door het project. Elk hoofdstuk heeft zijn eigen pagina,
      progressie, prompts en uitwerking.
    </p>

    <div class="chapter-grid">
      <a class="chapter-card" href="./chapters/platform_runtime.html" style="--c:var(--runtime)">
        <h3 class="chapter-title">Platform & Runtime</h3>
        <p class="chapter-desc">OpenClaw core, systemd runtime, hardened runner, isolation en worker skeletons.</p>
        <div class="meta"><span>23h</span><span>100%</span></div>
        <div class="pbar"><div style="width:100%"></div></div>
      </a>

      <a class="chapter-card" href="./chapters/security_hardening.html" style="--c:var(--security)">
        <h3 class="chapter-title">Security Hardening</h3>
        <p class="chapter-desc">Secrets, egress control, monitoring, incident response, kill switch en runtime safety.</p>
        <div class="meta"><span>28h</span><span>0%</span></div>
        <div class="pbar"><div style="width:0%"></div></div>
      </a>

      <a class="chapter-card" href="./chapters/model_runtime.html" style="--c:var(--models)">
        <h3 class="chapter-title">Model Runtime & Providers</h3>
        <p class="chapter-desc">Ollama, lokale modellen, provider abstraction, fallback en model switching per agent.</p>
        <div class="meta"><span>22h</span><span>0%</span></div>
        <div class="pbar"><div style="width:0%"></div></div>
      </a>

      <a class="chapter-card" href="./chapters/data_memory.html" style="--c:var(--memory)">
        <h3 class="chapter-title">Data & Memory Architecture</h3>
        <p class="chapter-desc">Agent DB, memory layer, embeddings, retrieval en system state.</p>
        <div class="meta"><span>32h</span><span>0%</span></div>
        <div class="pbar"><div style="width:0%"></div></div>
      </a>

      <a class="chapter-card" href="./chapters/agent_logic.html" style="--c:var(--swarm)">
        <h3 class="chapter-title">Agent Logic, Skills & Swarm</h3>
        <p class="chapter-desc">Rollen, protocol, workflows, skill governance en swarm coordination.</p>
        <div class="meta"><span>54h</span><span>0%</span></div>
        <div class="pbar"><div style="width:0%"></div></div>
      </a>

      <a class="chapter-card" href="./chapters/observability.html" style="--c:var(--observe)">
        <h3 class="chapter-title">Observability & API Cost Control</h3>
        <p class="chapter-desc">Usage, tracing, cost ledger, provider inzicht en operationele signalen.</p>
        <div class="meta"><span>24h</span><span>0%</span></div>
        <div class="pbar"><div style="width:0%"></div></div>
      </a>

      <a class="chapter-card" href="./chapters/control_center.html" style="--c:var(--ui)">
        <h3 class="chapter-title">Strategic Control Center UI</h3>
        <p class="chapter-desc">Homepage, chapter pages, prompt library, visuals en operations-ready dashboard structuur.</p>
        <div class="meta"><span>30h</span><span>20%</span></div>
        <div class="pbar"><div style="width:20%"></div></div>
      </a>

      <a class="chapter-card" href="./chapters/mission_control_ops.html" style="--c:var(--command)">
        <h3 class="chapter-title">Mission Control &amp; Operations Orchestration</h3>
        <p class="chapter-desc">Live besturing van Flux, sentinels, queues, overrides, escalaties en runtime-operaties.</p>
        <div class="meta"><span>0h</span><span>0%</span></div>
        <div class="pbar"><div style="width:0%"></div></div>
      </a>
    </div>
  </div>
</section>

<section class="section" id="architecture">
  <div class="wrap">
    <h2>Architecture Preview</h2>
    <p class="section-intro">
      Hier zie je het ARC-model in één beeld: van operator en interface-agents tot Flux, sentinels, leads en worker-uitvoering.
    </p>

    <div class="layout-grid">

      <div class="svg-card">
        <h3>Fastest Path to Live</h3>
        <p>De snelste live route loopt van Model Runtime naar Agent Logic, daarna Data &amp; Memory en vervolgens Mission Control.</p>
        <svg viewBox="0 0 1200 280" role="img" aria-label="Fastest Path to Live">
          <defs>
            <marker id="arrowFast2" markerWidth="12" markerHeight="12" refX="10" refY="4" orient="auto">
              <path d="M0,0 L12,4 L0,8 z" fill="var(--accent)"/>
            </marker>
          </defs>

          <rect x="40" y="92" width="240" height="84" rx="20" fill="rgba(155,124,255,.14)" stroke="var(--models)" stroke-width="2.5"/>
          <text x="160" y="126" text-anchor="middle" font-size="24" font-weight="900" fill="var(--text)">Model Runtime</text>
          <text x="160" y="154" text-anchor="middle" font-size="16" fill="var(--muted)">providers · governance</text>

          <line x1="280" y1="134" x2="350" y2="134" stroke="var(--accent)" stroke-width="4" marker-end="url(#arrowFast2)"/>

          <rect x="370" y="92" width="240" height="84" rx="20" fill="rgba(255,77,109,.14)" stroke="var(--swarm)" stroke-width="2.5"/>
          <text x="490" y="126" text-anchor="middle" font-size="24" font-weight="900" fill="var(--text)">Agent Logic</text>
          <text x="490" y="154" text-anchor="middle" font-size="16" fill="var(--muted)">roles · skills · swarm</text>

          <line x1="610" y1="134" x2="680" y2="134" stroke="var(--accent)" stroke-width="4" marker-end="url(#arrowFast2)"/>

          <rect x="700" y="92" width="240" height="84" rx="20" fill="rgba(78,168,222,.14)" stroke="var(--memory)" stroke-width="2.5"/>
          <text x="820" y="126" text-anchor="middle" font-size="24" font-weight="900" fill="var(--text)">Data &amp; Memory</text>
          <text x="820" y="154" text-anchor="middle" font-size="16" fill="var(--muted)">shared state · memory</text>

          <line x1="940" y1="134" x2="1010" y2="134" stroke="var(--accent)" stroke-width="4" marker-end="url(#arrowFast2)"/>

          <rect x="1030" y="92" width="140" height="84" rx="20" fill="rgba(127,184,255,.14)" stroke="var(--command)" stroke-width="2.5"/>
          <text x="1100" y="126" text-anchor="middle" font-size="22" font-weight="900" fill="var(--text)">Mission</text>
          <text x="1100" y="154" text-anchor="middle" font-size="16" fill="var(--muted)">Control</text>
        </svg>
      </div>

      <div class="svg-card" id="roadmap">
        <h3>ARC Command Flow</h3>
        <p>De operationele stroom loopt van Fea via Nova naar Flux. Vanuit Flux wordt het werk verdeeld naar sentinels met per domein een lead, skill-set, workers en uitvoering.</p>
        <svg viewBox="0 0 1280 980" role="img" aria-label="ARC Command Flow">
          <defs>
            <marker id="arrowFlow2" markerWidth="14" markerHeight="14" refX="11" refY="5" orient="auto">
              <path d="M0,0 L14,5 L0,10 z" fill="var(--accent)"/>
            </marker>
          </defs>

          <rect x="505" y="18" width="270" height="96" rx="24" fill="rgba(214,179,94,.16)" stroke="var(--accent)" stroke-width="2.5"/>
          <text x="640" y="56" text-anchor="middle" font-size="30" font-weight="900" fill="var(--text)">Operator</text>
          <text x="640" y="88" text-anchor="middle" font-size="22" font-weight="700" fill="var(--muted)">Fea</text>

          <line x1="640" y1="114" x2="640" y2="150" stroke="var(--accent)" stroke-width="4.5" marker-end="url(#arrowFlow2)"/>

          <rect x="110" y="180" width="210" height="92" rx="22" fill="rgba(127,184,255,.12)" stroke="var(--command)" stroke-width="2"/>
          <text x="215" y="216" text-anchor="middle" font-size="28" font-weight="900" fill="var(--text)">James</text>
          <text x="215" y="246" text-anchor="middle" font-size="18" fill="var(--muted)">Direct Interface Agent</text>

          <rect x="535" y="166" width="210" height="120" rx="24" fill="rgba(127,184,255,.18)" stroke="var(--command)" stroke-width="2.5"/>
          <text x="640" y="208" text-anchor="middle" font-size="34" font-weight="900" fill="var(--text)">Nova</text>
          <text x="640" y="240" text-anchor="middle" font-size="18" fill="var(--muted)">Link · Envoy · Catalyst</text>

          <rect x="960" y="180" width="210" height="92" rx="22" fill="rgba(127,184,255,.12)" stroke="var(--command)" stroke-width="2"/>
          <text x="1065" y="216" text-anchor="middle" font-size="28" font-weight="900" fill="var(--text)">Jim</text>
          <text x="1065" y="246" text-anchor="middle" font-size="18" fill="var(--muted)">Direct Interface Agent</text>

          <line x1="640" y1="286" x2="640" y2="346" stroke="var(--accent)" stroke-width="5" marker-end="url(#arrowFlow2)"/>

          <ellipse cx="640" cy="432" rx="170" ry="92" fill="rgba(155,124,255,.16)" stroke="var(--models)" stroke-width="3"/>
          <text x="640" y="428" text-anchor="middle" font-size="38" font-weight="900" fill="var(--text)">Flux</text>
          <text x="640" y="462" text-anchor="middle" font-size="20" fill="var(--muted)">Brein</text>

          <line x1="640" y1="524" x2="640" y2="580" stroke="var(--accent)" stroke-width="4.5"/>
          <line x1="200" y1="610" x2="1080" y2="610" stroke="var(--accent)" stroke-width="4.5"/>

          <line x1="320" y1="610" x2="320" y2="648" stroke="var(--accent)" stroke-width="4.5" marker-end="url(#arrowFlow2)"/>
          <line x1="640" y1="580" x2="640" y2="648" stroke="var(--accent)" stroke-width="4.5" marker-end="url(#arrowFlow2)"/>
          <line x1="960" y1="610" x2="960" y2="648" stroke="var(--accent)" stroke-width="4.5" marker-end="url(#arrowFlow2)"/>

          <rect x="40" y="648" width="360" height="262" rx="24" fill="rgba(63,227,181,.12)" stroke="var(--security)" stroke-width="2.5"/>
          <text x="220" y="690" text-anchor="middle" font-size="28" font-weight="900" fill="var(--text)">Sentinel</text>
          <text x="220" y="724" text-anchor="middle" font-size="30" font-weight="900" fill="var(--text)">Security</text>
          <text x="78" y="770" font-size="18" font-weight="800" fill="var(--muted)">Lead</text>
          <text x="170" y="770" font-size="18" fill="var(--text)">Nero</text>
          <text x="78" y="806" font-size="18" font-weight="800" fill="var(--muted)">Layers</text>
          <text x="170" y="806" font-size="15" fill="var(--muted2)">Prompt Defense · Runtime Security</text>
          <text x="78" y="842" font-size="18" font-weight="800" fill="var(--muted)">Skills</text>
          <text x="170" y="842" font-size="15" fill="var(--muted2)">Audit · Secrets · Incident Response</text>
          <text x="78" y="878" font-size="18" font-weight="800" fill="var(--muted)">Workers</text>
          <text x="170" y="878" font-size="15" fill="var(--muted2)">Prompt Defense · Runtime Audit</text>

          <rect x="460" y="648" width="360" height="262" rx="24" fill="rgba(54,201,255,.12)" stroke="var(--runtime)" stroke-width="2.5"/>
          <text x="640" y="690" text-anchor="middle" font-size="28" font-weight="900" fill="var(--text)">Sentinel</text>
          <text x="640" y="724" text-anchor="middle" font-size="30" font-weight="900" fill="var(--text)">Research</text>
          <text x="498" y="770" font-size="18" font-weight="800" fill="var(--muted)">Lead</text>
          <text x="590" y="770" font-size="18" fill="var(--text)">Sora</text>
          <text x="498" y="806" font-size="18" font-weight="800" fill="var(--muted)">Layers</text>
          <text x="590" y="806" font-size="15" fill="var(--muted2)">Web Research · Competitor Analysis</text>
          <text x="498" y="842" font-size="18" font-weight="800" fill="var(--muted)">Skills</text>
          <text x="590" y="842" font-size="15" fill="var(--muted2)">Validation · Dataset Collection</text>
          <text x="498" y="878" font-size="18" font-weight="800" fill="var(--muted)">Workers</text>
          <text x="590" y="878" font-size="15" fill="var(--muted2)">Web Research · Source Validation</text>

          <rect x="880" y="648" width="360" height="262" rx="24" fill="rgba(255,77,109,.12)" stroke="var(--swarm)" stroke-width="2.5"/>
          <text x="1060" y="690" text-anchor="middle" font-size="28" font-weight="900" fill="var(--text)">Sentinel</text>
          <text x="1060" y="724" text-anchor="middle" font-size="30" font-weight="900" fill="var(--text)">Engineering</text>
          <text x="918" y="770" font-size="18" font-weight="800" fill="var(--muted)">Lead</text>
          <text x="1010" y="770" font-size="18" fill="var(--text)">Forge</text>
          <text x="918" y="806" font-size="18" font-weight="800" fill="var(--muted)">Layers</text>
          <text x="1010" y="806" font-size="15" fill="var(--muted2)">Code Generation · Architecture Validation</text>
          <text x="918" y="842" font-size="18" font-weight="800" fill="var(--muted)">Skills</text>
          <text x="1010" y="842" font-size="15" fill="var(--muted2)">Review · Automation · Build Execution</text>
          <text x="918" y="878" font-size="18" font-weight="800" fill="var(--muted)">Workers</text>
          <text x="1010" y="878" font-size="15" fill="var(--muted2)">Code Review · Automation Build</text>
        </svg>
      </div>

      <div class="svg-card">
        <h3>Chapter Status Snapshot</h3>
        <p>Verdeling van het totaalprogramma over finished, started en planned hoofdstukken.</p>
        <svg viewBox="0 0 1200 320" role="img" aria-label="Chapter Status Snapshot">
          <rect x="80" y="54" width="260" height="36" rx="14" fill="rgba(63,227,181,.18)" stroke="var(--security)" stroke-width="2"/>
          <text x="210" y="78" text-anchor="middle" font-size="18" font-weight="800" fill="var(--text)">Finished</text>

          <rect x="470" y="54" width="260" height="36" rx="14" fill="rgba(214,179,94,.18)" stroke="var(--accent)" stroke-width="2"/>
          <text x="600" y="78" text-anchor="middle" font-size="18" font-weight="800" fill="var(--text)">Started</text>

          <rect x="860" y="54" width="260" height="36" rx="14" fill="rgba(155,124,255,.18)" stroke="var(--models)" stroke-width="2"/>
          <text x="990" y="78" text-anchor="middle" font-size="18" font-weight="800" fill="var(--text)">Planned</text>

          <rect x="115" y="122" width="190" height="88" rx="18" fill="rgba(63,227,181,.12)" stroke="var(--security)" stroke-width="2.5"/>
          <text x="210" y="176" text-anchor="middle" font-size="38" font-weight="900" fill="var(--text)">4</text>

          <rect x="505" y="122" width="190" height="88" rx="18" fill="rgba(214,179,94,.12)" stroke="var(--accent)" stroke-width="2.5"/>
          <text x="600" y="176" text-anchor="middle" font-size="38" font-weight="900" fill="var(--text)">1</text>

          <rect x="895" y="122" width="190" height="88" rx="18" fill="rgba(155,124,255,.12)" stroke="var(--models)" stroke-width="2.5"/>
          <text x="990" y="176" text-anchor="middle" font-size="38" font-weight="900" fill="var(--text)">4</text>

          <text x="210" y="250" text-anchor="middle" font-size="17" fill="var(--muted)">Platform · Security · Model Runtime · UI</text>
          <text x="600" y="250" text-anchor="middle" font-size="17" fill="var(--muted)">Agent Logic</text>
          <text x="990" y="250" text-anchor="middle" font-size="17" fill="var(--muted)">Memory · Observability · Mission Control · Launch</text>
        </svg>
      </div>

      <div class="svg-card">
        <h3>Sentinel Deployment Snapshot</h3>
        <p>De eerste sentinel-wave toont domein, lead en fase-status voor de eerste concrete build-baseline.</p>
        <svg viewBox="0 0 1200 320" role="img" aria-label="Sentinel Deployment Snapshot">
          <rect x="40" y="40" width="250" height="110" rx="20" fill="rgba(63,227,181,.14)" stroke="var(--security)" stroke-width="2.5"/>
          <text x="165" y="78" text-anchor="middle" font-size="26" font-weight="900" fill="var(--text)">Security</text>
          <text x="165" y="108" text-anchor="middle" font-size="18" fill="var(--muted)">Lead: Nero</text>
          <text x="165" y="132" text-anchor="middle" font-size="16" fill="var(--muted2)">built phase 1</text>

          <rect x="330" y="40" width="250" height="110" rx="20" fill="rgba(54,201,255,.14)" stroke="var(--runtime)" stroke-width="2.5"/>
          <text x="455" y="78" text-anchor="middle" font-size="26" font-weight="900" fill="var(--text)">Research</text>
          <text x="455" y="108" text-anchor="middle" font-size="18" fill="var(--muted)">Lead: Sora</text>
          <text x="455" y="132" text-anchor="middle" font-size="16" fill="var(--muted2)">built phase 1</text>

          <rect x="620" y="40" width="250" height="110" rx="20" fill="rgba(255,77,109,.14)" stroke="var(--swarm)" stroke-width="2.5"/>
          <text x="745" y="78" text-anchor="middle" font-size="26" font-weight="900" fill="var(--text)">Engineering</text>
          <text x="745" y="108" text-anchor="middle" font-size="18" fill="var(--muted)">Lead: Forge</text>
          <text x="745" y="132" text-anchor="middle" font-size="16" fill="var(--muted2)">built phase 1</text>

          <rect x="910" y="40" width="250" height="110" rx="20" fill="rgba(78,168,222,.14)" stroke="var(--memory)" stroke-width="2.5"/>
          <text x="1035" y="78" text-anchor="middle" font-size="24" font-weight="900" fill="var(--text)">Documentation</text>
          <text x="1035" y="108" text-anchor="middle" font-size="18" fill="var(--muted)">Lead: Clio</text>
          <text x="1035" y="132" text-anchor="middle" font-size="16" fill="var(--muted2)">built phase 1</text>

          <line x1="165" y1="170" x2="165" y2="220" stroke="var(--accent)" stroke-width="4"/>
          <line x1="455" y1="170" x2="455" y2="220" stroke="var(--accent)" stroke-width="4"/>
          <line x1="745" y1="170" x2="745" y2="220" stroke="var(--accent)" stroke-width="4"/>
          <line x1="1035" y1="170" x2="1035" y2="220" stroke="var(--accent)" stroke-width="4"/>

          <text x="165" y="252" text-anchor="middle" font-size="16" fill="var(--muted)">lead + workers</text>
          <text x="455" y="252" text-anchor="middle" font-size="16" fill="var(--muted)">lead + workers</text>
          <text x="745" y="252" text-anchor="middle" font-size="16" fill="var(--muted)">lead + workers</text>
          <text x="1035" y="252" text-anchor="middle" font-size="16" fill="var(--muted)">lead + workers</text>
        </svg>
      </div>

    </div>
  </div>
</section>

<div class="footer-space"></div>

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
</script>

  <script src="./assets/homepage_progress_sync.js"></script>
</body>
</html>
"""
index.write_text(html, encoding="utf-8")
print(f"Built {index}")
