from pathlib import Path

index = Path.home() / "arc_strategic_control_center" / "index.html"

html = r"""<!DOCTYPE html>
<html lang="en" data-theme="dark" data-preset="obsidian_gold">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>The Arc Strategic Control Center</title>

<style>
:root{
  --bg0:#0c1420;
  --bg1:#101a28;
  --bg2:#162233;

  --panel:#182433;
  --panel2:#1d2b3d;
  --panel3:#223246;

  --line:rgba(255,255,255,.10);
  --line2:rgba(255,255,255,.18);

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
  --observe:#ffb84d;
  --ui:#d6b35e;
}

[data-theme="light"]{
  --bg0:#eef3f9;
  --bg1:#f6f9fc;
  --bg2:#ffffff;
  --panel:#ffffff;
  --panel2:#f4f7fb;
  --panel3:#edf2f8;
  --line:rgba(18,24,36,.12);
  --line2:rgba(18,24,36,.20);
  --text:#122033;
  --muted:#425874;
  --muted2:#677d98;
  --accentGlow:rgba(214,179,94,.14);
}

[data-preset="obsidian_gold"]{
  --accent:#d6b35e; --accent2:#f0d18a; --accentGlow:rgba(240,209,138,.20);
}
[data-preset="graphite_cyan"]{
  --accent:#36c9ff; --accent2:#92e8ff; --accentGlow:rgba(54,201,255,.16);
}
[data-preset="midnight_purple"]{
  --accent:#9b7cff; --accent2:#c9b8ff; --accentGlow:rgba(155,124,255,.16);
}
[data-preset="slate_teal"]{
  --accent:#2fd3c5; --accent2:#93fff4; --accentGlow:rgba(47,211,197,.14);
}

*{box-sizing:border-box}
html,body{height:100%}
body{
  margin:0;
  font-family: Inter, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif;
  color:var(--text);
  background:
    radial-gradient(1100px 700px at 85% -10%, var(--accentGlow), transparent 55%),
    radial-gradient(800px 400px at 10% 10%, rgba(255,255,255,.03), transparent 50%),
    linear-gradient(180deg, var(--bg0), var(--bg1) 42%, var(--bg2));
}

.wrap{max-width:1360px;margin:0 auto;padding:0 28px}
.topbar{
  position:sticky;top:0;z-index:60;
  background:color-mix(in oklab,var(--panel) 84%, transparent);
  backdrop-filter:blur(12px);
  border-bottom:1px solid var(--line);
}
.topbar-inner{
  display:flex;justify-content:space-between;align-items:center;gap:18px;padding:16px 0;
}
.logo{
  font-size:22px;
  font-weight:900;
  letter-spacing:.2px;
}
.logo-sub{
  margin-top:4px;
  font-size:13px;
  color:var(--muted2);
}
.nav{
  display:flex;gap:10px;flex-wrap:wrap;align-items:center;
}
.nav a,.btn,select{
  text-decoration:none;
  color:var(--muted);
  font-size:14px;
  padding:9px 13px;
  border-radius:999px;
  border:1px solid var(--line);
  background:color-mix(in oklab,var(--panel2) 76%, transparent);
  cursor:pointer;
}

.hero{padding:52px 0 18px}
.hero-grid{
  display:grid;
  grid-template-columns:1.18fr .82fr;
  gap:20px;
}
@media (max-width: 980px){.hero-grid{grid-template-columns:1fr}}

.panel{
  background:color-mix(in oklab,var(--panel) 94%, black 6%);
  border:1px solid var(--line);
  border-radius:24px;
  padding:24px;
  position:relative;
  overflow:hidden;
  box-shadow:0 20px 50px rgba(0,0,0,.34);
}
.panel:before{
  content:"";
  position:absolute;inset:-1px;
  background:radial-gradient(640px 240px at 0% 0%, var(--accentGlow), transparent 58%);
  opacity:.95;
  pointer-events:none;
}
.panel>*{position:relative}

.hero-panel{
  border-color:color-mix(in oklab,var(--accent) 28%, var(--line));
}
.hero-panel:after{
  content:"";
  position:absolute;left:0;top:0;right:0;height:4px;
  background:linear-gradient(90deg, transparent, var(--accent), transparent);
}
.hero-panel h1{
  margin:0;
  font-size:52px;
  line-height:1.04;
  letter-spacing:.2px;
}
.hero-panel p{
  margin:16px 0 0;
  font-size:18px;
  line-height:1.78;
  color:var(--muted);
}

.kpi-grid{
  display:grid;
  grid-template-columns:repeat(2,1fr);
  gap:12px;
  margin-top:20px;
}
.kpi{
  border-radius:18px;
  border:1px solid color-mix(in oklab,var(--accent) 26%, var(--line));
  background:
    radial-gradient(240px 90px at 10% 10%, color-mix(in oklab,var(--accent) 18%, transparent), transparent 65%),
    color-mix(in oklab,var(--panel2) 84%, transparent);
  padding:14px;
  box-shadow:0 0 0 1px rgba(255,255,255,.02) inset;
}
.kpi-label{font-size:13px;color:var(--muted2)}
.kpi-value{font-size:19px;font-weight:900;margin-top:4px}

.quick-panel{
  border-color:rgba(255,255,255,.14);
}
.quick-panel .callout{
  border-radius:18px;
  padding:14px 16px;
  margin-top:12px;
  border:1px solid var(--line);
  background:color-mix(in oklab,var(--panel2) 84%, transparent);
  font-size:17px;
  line-height:1.6;
  font-weight:800;
}
.quick-panel .callout.security{
  border-color:color-mix(in oklab,var(--security) 35%, var(--line));
  background:
    radial-gradient(240px 100px at 0% 0%, color-mix(in oklab,var(--security) 16%, transparent), transparent 70%),
    color-mix(in oklab,var(--panel2) 88%, transparent);
}
.quick-panel .callout.models{
  border-color:color-mix(in oklab,var(--models) 35%, var(--line));
  background:
    radial-gradient(240px 100px at 0% 0%, color-mix(in oklab,var(--models) 16%, transparent), transparent 70%),
    color-mix(in oklab,var(--panel2) 88%, transparent);
}
.quick-panel .callout.data{
  border-color:color-mix(in oklab,var(--memory) 35%, var(--line));
  background:
    radial-gradient(240px 100px at 0% 0%, color-mix(in oklab,var(--memory) 16%, transparent), transparent 70%),
    color-mix(in oklab,var(--panel2) 88%, transparent);
}
.quick-panel .callout.ops{
  border-color:color-mix(in oklab,var(--observe) 35%, var(--line));
  background:
    radial-gradient(240px 100px at 0% 0%, color-mix(in oklab,var(--observe) 16%, transparent), transparent 70%),
    color-mix(in oklab,var(--panel2) 88%, transparent);
}

.section{padding:10px 0 0}
.section h2{
  font-size:32px;
  margin:0 0 14px;
}
.section-intro{
  margin:0 0 16px;
  color:var(--muted);
  font-size:17px;
  line-height:1.75;
}

.chapter-grid{
  display:grid;
  grid-template-columns:repeat(3,1fr);
  gap:18px;
}
@media (max-width:1100px){.chapter-grid{grid-template-columns:repeat(2,1fr)}}
@media (max-width:760px){.chapter-grid{grid-template-columns:1fr}}

.chapter-card{
  border-radius:24px;
  border:1px solid var(--line);
  background:color-mix(in oklab,var(--panel3) 92%, black 4%);
  padding:18px;
  position:relative;
  overflow:hidden;
  text-decoration:none;
  color:inherit;
  box-shadow:0 16px 38px rgba(0,0,0,.34), 0 0 12px color-mix(in oklab,var(--c) 22%, transparent);
  transition:transform .16s ease, border-color .16s ease, box-shadow .16s ease;
}
.chapter-card:hover{
  transform:translateY(-3px);
  border-color:color-mix(in oklab,var(--c) 45%, var(--line));
  box-shadow:0 18px 42px rgba(0,0,0,.38), 0 0 16px color-mix(in oklab,var(--c) 28%, transparent);
}
.chapter-card:before{
  content:"";
  position:absolute;left:0;top:0;right:0;height:4px;
  background:linear-gradient(90deg,
    color-mix(in oklab,var(--c) 55%, transparent),
    var(--c),
    color-mix(in oklab,var(--c) 55%, transparent)
  );
}
.chapter-card:after{
  content:"";
  position:absolute;inset:-1px;
  background:radial-gradient(560px 220px at 0% 0%, color-mix(in oklab,var(--c) 34%, transparent), transparent 64%);
  pointer-events:none;
}
.chapter-card>*{position:relative}
.chapter-title{
  margin:0;
  font-size:23px;
  font-weight:900;
}
.chapter-desc{
  margin:10px 0 0;
  color:var(--muted);
  font-size:16.5px;
  line-height:1.72;
}
.meta{
  display:flex;justify-content:space-between;gap:12px;align-items:baseline;
  margin-top:14px;color:var(--muted2);font-size:14px;
}
.pbar{
  margin-top:10px;
  height:14px;
  border-radius:999px;
  border:1px solid var(--line);
  overflow:hidden;
  background:color-mix(in oklab,var(--panel2) 78%, transparent);
}
.pbar > div{
  height:100%;
  border-radius:999px;
  background:linear-gradient(90deg, color-mix(in oklab,var(--c) 70%, transparent), color-mix(in oklab,var(--c) 95%, white 10%));
  box-shadow:0 0 0 4px color-mix(in oklab,var(--c) 16%, transparent);
}

.layout-grid{
  display:grid;
  grid-template-columns:1fr 1fr;
  gap:18px;
}
@media (max-width:980px){.layout-grid{grid-template-columns:1fr}}

.svg-card{
  border-radius:24px;
  border:1px solid var(--line);
  background:color-mix(in oklab,var(--panel) 94%, black 6%);
  padding:20px;
  box-shadow:0 16px 38px rgba(0,0,0,.30);
  position:relative;
  overflow:hidden;
}
.svg-card:before{
  content:"";
  position:absolute;inset:-1px;
  background:radial-gradient(520px 220px at 0% 0%, var(--accentGlow), transparent 62%);
  pointer-events:none;
}
.svg-card>*{position:relative}
.svg-card h3{
  margin:0 0 8px;
  font-size:24px;
}
.svg-card p{
  margin:0 0 14px;
  color:var(--muted);
  font-size:16.5px;
  line-height:1.72;
}
.svg-card svg{
  width:100%;
  height:auto;
  display:block;
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
      <div class="panel hero-panel">
        <h1>The Arc Strategic<br>Control Center</h1>
        <p>
          Dit is het centrale overzichtspunt voor het volledige Arc project:
          platform, security, models, data, memory, swarm skills, observability en UI.
          Doel is om snel te kunnen scannen waar we staan, wat nog moet gebeuren en
          welke route het snelst naar live leidt.
        </p>

        <div class="kpi-grid">
          <div class="kpi">
            <div class="kpi-label">Current Focus</div>
            <div class="kpi-value">Security Hardening</div>
          </div>
          <div class="kpi">
            <div class="kpi-label">Active Cluster</div>
            <div class="kpi-value">Prod Safety Core</div>
          </div>
          <div class="kpi">
            <div class="kpi-label">Overall Progress</div>
            <div class="kpi-value">31%</div>
          </div>
          <div class="kpi">
            <div class="kpi-label">Realistic Duration</div>
            <div class="kpi-value">190h</div>
          </div>
        </div>
      </div>

      <div class="panel quick-panel">
        <h2 style="font-size:32px;margin:0 0 10px">Quick Read</h2>
        <p class="section-intro">In één oogopslag waar het project nu staat.</p>

        <div class="callout security">Security Hardening is de eerstvolgende kritieke fase richting live.</div>
        <div class="callout models">Model Runtime voegt Ollama, routing en provider abstraction toe.</div>
        <div class="callout data">Data & Memory zorgt dat agents consistente state en kennis krijgen.</div>
        <div class="callout ops">Observability en UI maken het platform bestuurbaar en live-ready.</div>
      </div>
    </div>
  </div>
</section>

<section class="section" id="chapters">
  <div class="wrap">
    <h2>Chapter Navigation</h2>
    <p class="section-intro">
      Gebruik deze hoofdstukken als hoofdroute door het project. Elk hoofdstuk heeft een eigen pagina,
      status, prompts en uitwerking.
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
    </div>
  </div>
</section>

<section class="section" id="architecture">
  <div class="wrap">
    <h2>Architecture Preview</h2>
    <p class="section-intro">
      Hier zie je het Arc model in één beeld: van intent en gateway tot orchestration, sentinels en worker execution.
    </p>

    <div class="layout-grid">
      <div class="svg-card">
        <h3>Arc Command Flow</h3>
        <p>De strategische stroom van FEA naar Nova, Flux, Sentinels en Workers.</p>

        <svg viewBox="0 0 760 520" role="img" aria-label="Arc Command Flow">
          <defs>
            <marker id="arr1" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
              <path d="M0,0 L10,3 L0,6 Z" fill="var(--accent2)"></path>
            </marker>
          </defs>

          <rect x="250" y="20" width="260" height="70" rx="18" fill="rgba(214,179,94,.20)" stroke="var(--accent)" />
          <text x="380" y="50" text-anchor="middle" font-size="22" font-weight="900" fill="var(--text)">FEA</text>
          <text x="380" y="72" text-anchor="middle" font-size="14" fill="var(--muted)">Vision Source</text>

          <rect x="250" y="130" width="260" height="70" rx="18" fill="rgba(54,201,255,.18)" stroke="var(--runtime)" />
          <text x="380" y="160" text-anchor="middle" font-size="22" font-weight="900" fill="var(--text)">NOVA</text>
          <text x="380" y="182" text-anchor="middle" font-size="14" fill="var(--muted)">Gateway Interface</text>

          <rect x="250" y="240" width="260" height="70" rx="18" fill="rgba(155,124,255,.18)" stroke="var(--models)" />
          <text x="380" y="270" text-anchor="middle" font-size="22" font-weight="900" fill="var(--text)">FLUX</text>
          <text x="380" y="292" text-anchor="middle" font-size="14" fill="var(--muted)">Strategic Brain</text>

          <rect x="90" y="370" width="190" height="72" rx="18" fill="rgba(63,227,181,.18)" stroke="var(--security)" />
          <text x="185" y="400" text-anchor="middle" font-size="18" font-weight="900" fill="var(--text)">Sentinel Layer</text>
          <text x="185" y="422" text-anchor="middle" font-size="13" fill="var(--muted)">Pillar Leaders</text>

          <rect x="490" y="370" width="190" height="72" rx="18" fill="rgba(255,77,109,.18)" stroke="var(--swarm)" />
          <text x="585" y="400" text-anchor="middle" font-size="18" font-weight="900" fill="var(--text)">Worker Swarm</text>
          <text x="585" y="422" text-anchor="middle" font-size="13" fill="var(--muted)">Task Execution</text>

          <line x1="380" y1="90" x2="380" y2="130" stroke="var(--accent2)" stroke-width="3" marker-end="url(#arr1)" />
          <line x1="380" y1="200" x2="380" y2="240" stroke="var(--accent2)" stroke-width="3" marker-end="url(#arr1)" />
          <line x1="340" y1="310" x2="220" y2="370" stroke="var(--accent2)" stroke-width="3" marker-end="url(#arr1)" />
          <line x1="420" y1="310" x2="540" y2="370" stroke="var(--accent2)" stroke-width="3" marker-end="url(#arr1)" />
        </svg>
      </div>

      <div class="svg-card" id="roadmap">
        <h3>Fastest Path to Live</h3>
        <p>De logische volgorde om het systeem zo snel mogelijk live-ready te krijgen.</p>

        <svg viewBox="0 0 760 520" role="img" aria-label="Fastest Path to Live">
          <defs>
            <marker id="arr2" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
              <path d="M0,0 L10,3 L0,6 Z" fill="var(--accent2)"></path>
            </marker>
          </defs>

          <g font-family="Inter, system-ui, sans-serif">
            <rect x="160" y="20" width="430" height="56" rx="16" fill="rgba(54,201,255,.16)" stroke="var(--runtime)" />
            <text x="375" y="54" text-anchor="middle" font-size="20" font-weight="900" fill="var(--text)">Platform & Runtime</text>

            <rect x="160" y="96" width="430" height="56" rx="16" fill="rgba(63,227,181,.16)" stroke="var(--security)" />
            <text x="375" y="130" text-anchor="middle" font-size="20" font-weight="900" fill="var(--text)">Security Hardening</text>

            <rect x="160" y="172" width="430" height="56" rx="16" fill="rgba(155,124,255,.16)" stroke="var(--models)" />
            <text x="375" y="206" text-anchor="middle" font-size="20" font-weight="900" fill="var(--text)">Model Runtime & Providers</text>

            <rect x="160" y="248" width="430" height="56" rx="16" fill="rgba(78,168,222,.16)" stroke="var(--memory)" />
            <text x="375" y="282" text-anchor="middle" font-size="20" font-weight="900" fill="var(--text)">Data & Memory Architecture</text>

            <rect x="160" y="324" width="430" height="56" rx="16" fill="rgba(255,77,109,.16)" stroke="var(--swarm)" />
            <text x="375" y="358" text-anchor="middle" font-size="20" font-weight="900" fill="var(--text)">Agent Logic, Skills & Swarm</text>

            <rect x="160" y="400" width="430" height="56" rx="16" fill="rgba(255,184,77,.16)" stroke="var(--observe)" />
            <text x="375" y="434" text-anchor="middle" font-size="20" font-weight="900" fill="var(--text)">Observability & API Cost Control</text>

            <line x1="375" y1="76" x2="375" y2="96" stroke="var(--accent2)" stroke-width="3" marker-end="url(#arr2)" />
            <line x1="375" y1="152" x2="375" y2="172" stroke="var(--accent2)" stroke-width="3" marker-end="url(#arr2)" />
            <line x1="375" y1="228" x2="375" y2="248" stroke="var(--accent2)" stroke-width="3" marker-end="url(#arr2)" />
            <line x1="375" y1="304" x2="375" y2="324" stroke="var(--accent2)" stroke-width="3" marker-end="url(#arr2)" />
            <line x1="375" y1="380" x2="375" y2="400" stroke="var(--accent2)" stroke-width="3" marker-end="url(#arr2)" />
          </g>
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

</body>
</html>
"""
index.write_text(html, encoding="utf-8")
print("Rebuilt homepage V4 with restored dark background and stronger card accents")
