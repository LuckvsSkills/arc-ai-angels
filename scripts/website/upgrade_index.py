#!/usr/bin/env python3
from pathlib import Path

base = Path.home() / "arc_strategic_control_center"
index_file = base / "index.html"

html = """<!doctype html>
<html lang="en" data-theme="dark" data-preset="obsidian_gold">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>The Arc Strategic Control Center</title>
  <style>
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
    }
    .panel:before{
      content:""; position:absolute; inset:-1px;
      background: radial-gradient(600px 220px at 0% 0%, var(--accentGlow), transparent 58%);
      pointer-events:none;
    }
    .panel > *{position:relative}

    h1{margin:0;font-size:30px;line-height:1.12}
    h2{margin:0 0 8px}
    h3{margin:0 0 8px}
    .subtitle{margin:10px 0 0;color:var(--muted);font-size:15.5px}
    .divider{height:1px;background:linear-gradient(90deg,transparent,var(--line2),transparent);margin:14px 0}
    .muted{color:var(--muted);font-size:14.5px}
    .muted2{color:var(--muted2);font-size:13.5px}

    .overview-grid{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:14px}
    @media (max-width:980px){.overview-grid{grid-template-columns:1fr}}

    .kvs{display:grid;grid-template-columns:220px 1fr;gap:8px 12px}
    .k{color:var(--muted2);font-size:14px}
    .v{font-size:14.5px}

    .pbar{height:14px;border-radius:999px;border:1px solid var(--line);background:color-mix(in oklab,var(--panel2) 72%,transparent);overflow:hidden}
    .pbar-in{
      height:100%;
      border-radius:999px;
      background:linear-gradient(90deg,var(--accentLine),color-mix(in oklab,var(--accent2) 70%, transparent));
      box-shadow:0 0 0 4px color-mix(in oklab,var(--accentGlow) 65%, transparent);
    }

    .cards{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-top:14px}
    @media (max-width:1100px){.cards{grid-template-columns:repeat(2,1fr)}}
    @media (max-width:720px){.cards{grid-template-columns:1fr}}

    .chapter{
      border-radius: var(--radius);
      border:1px solid var(--line);
      background: var(--card);
      box-shadow: var(--shadow2);
      padding:14px;
      position:relative;
      overflow:hidden;
    }
    .chapter:before{
      content:""; position:absolute; inset:-1px;
      background: radial-gradient(520px 220px at 0% 0%, var(--accentGlow), transparent 62%);
      pointer-events:none;
      opacity:.95;
    }
    .chapter>*{position:relative}

    .chapter-title{font-size:17px;font-weight:900}
    .row{display:flex;justify-content:space-between;gap:12px;align-items:baseline;flex-wrap:wrap}

    .badge{
      display:inline-flex;align-items:center;gap:8px;
      padding:5px 10px;border-radius:999px;border:1px solid var(--line);
      background: color-mix(in oklab,var(--panel2) 72%, transparent);
      font-size:13px;color:var(--muted);
    }

    a.chapter-link{
      display:inline-block;margin-top:12px;
      color: var(--accent2);
      text-decoration:none;
      font-weight:800;
    }

    .info-grid{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:14px}
    @media (max-width:980px){.info-grid{grid-template-columns:1fr}}

    .mini-card{
      border-radius: var(--radius);
      border:1px solid var(--line);
      background: var(--card);
      box-shadow: var(--shadow2);
      padding:14px;
      position:relative;
      overflow:hidden;
    }
    .mini-card:before{
      content:""; position:absolute; inset:-1px;
      background: radial-gradient(520px 220px at 0% 0%, var(--accentGlow), transparent 62%);
      pointer-events:none;
      opacity:.95;
    }
    .mini-card>*{position:relative}

    .path-list{margin:8px 0 0 18px;padding:0}
    .path-list li{margin:6px 0}

    .dep-wrap{
      border-radius: 16px;
      border:1px solid var(--line);
      background: color-mix(in oklab,var(--panel2) 72%, transparent);
      padding:12px;
      margin-top:10px;
    }
    .dep-step{
      padding:10px 12px;
      border-radius: 12px;
      border:1px solid var(--line);
      background: color-mix(in oklab,var(--panel) 70%, transparent);
      margin-top:8px;
      font-weight:800;
    }
    .dep-arrow{
      text-align:center;
      color: var(--accent2);
      font-size:20px;
      line-height:1.2;
      margin-top:4px;
    }
  </style>
</head>
<body>
  <div class="topbar">
    <div class="wrap">
      <div class="topbar-inner">
        <div class="brand-title">
          <div class="h" id="projectTitle">The Arc Strategic Control Center</div>
          <div class="s" id="projectSubtitle">Roadmap-first · operations-ready</div>
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
        <h1>The Arc Strategic Control Center</h1>
        <p class="subtitle" id="heroSubtitle">
          Architecture, Governance & Deployment Hub for the Arc AI Agent Network
        </p>

        <div class="divider"></div>

        <div class="overview-grid">
          <div>
            <h2 style="margin:0 0 8px">Project Overview</h2>
            <div class="kvs">
              <div class="k">Current focus</div>
              <div class="v">Security Hardening → Prod Safety Core</div>
              <div class="k">Current mode</div>
              <div class="v">Local roadmap site, later uitbreidbaar naar live operations dashboard</div>
              <div class="k">Structure</div>
              <div class="v">Hoofdstuk → Cluster → Blok</div>
              <div class="k">Goal</div>
              <div class="v">Fastest path to live met veilige architectuur, memory, skills en cost control</div>
            </div>
          </div>

          <div>
            <h2 style="margin:0 0 8px">Overall Progress</h2>
            <div class="row">
              <div class="muted">Total completion</div>
              <div id="overallPct" class="muted"><b>0%</b></div>
            </div>
            <div class="pbar" style="margin-top:8px">
              <div id="overallBar" class="pbar-in" style="width:0%"></div>
            </div>
            <div class="divider"></div>
            <div class="muted2" id="overallHours">0h / 0h</div>
          </div>
        </div>
      </section>

      <section class="info-grid">
        <article class="mini-card">
          <h2 style="margin:0 0 8px">Estimated Duration</h2>
          <div class="kvs">
            <div class="k">Minimum</div>
            <div class="v" id="minHours">-</div>
            <div class="k">Realistic</div>
            <div class="v" id="realHours">-</div>
            <div class="k">Heavy scenario</div>
            <div class="v" id="heavyHours">-</div>
          </div>
        </article>

        <article class="mini-card">
          <h2 style="margin:0 0 8px">Fastest Path to Live</h2>
          <ol class="path-list" id="fastestPath"></ol>
        </article>
      </section>

      <section class="mini-card" style="margin-top:14px">
        <h2 style="margin:0 0 8px">Dependency Map</h2>
        <div class="muted2">Welke hoofdstukken logisch op elkaar volgen.</div>
        <div class="dep-wrap" id="dependencyMap"></div>
      </section>

      <section class="cards" id="chapterCards"></section>
    </div>
  </header>

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

    Promise.all([
      fetch("./data/roadmap.json").then(r => r.json()),
      fetch("./data/meta.json").then(r => r.json())
    ])
    .then(([roadmap, meta]) => {
      const chapters = roadmap.chapters || [];
      const totalHours = chapters.reduce((a,c)=>a + (c.duration_hours || 0), 0);
      const doneHours = chapters.reduce((a,c)=>{
        const pct = (c.progress || 0)/100;
        return a + ((c.duration_hours || 0) * pct);
      }, 0);

      const overallPct = totalHours > 0 ? Math.round((doneHours/totalHours)*100) : 0;
      document.getElementById("overallPct").innerHTML = `<b>${overallPct}%</b>`;
      document.getElementById("overallBar").style.width = overallPct + "%";
      document.getElementById("overallHours").textContent = `${Math.round(doneHours)}h / ${totalHours}h`;

      document.getElementById("projectTitle").textContent = meta.project_title || roadmap.project || "The Arc Strategic Control Center";
      document.getElementById("projectSubtitle").textContent = "Roadmap-first · operations-ready";
      document.getElementById("heroSubtitle").textContent = meta.subtitle || "Architecture, Governance & Deployment Hub";

      const d = meta.durations || {};
      document.getElementById("minHours").textContent = (d.minimum_hours || 0) + "h";
      document.getElementById("realHours").textContent = (d.realistic_hours || 0) + "h";
      document.getElementById("heavyHours").textContent = (d.heavy_hours || 0) + "h";

      const fp = document.getElementById("fastestPath");
      fp.innerHTML = "";
      (meta.fastest_path_to_live || []).forEach(step => {
        const li = document.createElement("li");
        li.textContent = step;
        fp.appendChild(li);
      });

      const dep = document.getElementById("dependencyMap");
      dep.innerHTML = "";
      (meta.dependencies || []).forEach((x, idx) => {
        const a = document.createElement("div");
        a.className = "dep-step";
        a.textContent = x.from;
        dep.appendChild(a);

        const arrow = document.createElement("div");
        arrow.className = "dep-arrow";
        arrow.textContent = "↓";
        dep.appendChild(arrow);

        const b = document.createElement("div");
        b.className = "dep-step";
        b.textContent = x.to;
        dep.appendChild(b);

        if(idx < (meta.dependencies.length - 1)){
          const spacer = document.createElement("div");
          spacer.style.height = "8px";
          dep.appendChild(spacer);
        }
      });

      const host = document.getElementById("chapterCards");
      host.innerHTML = "";

      chapters.forEach(ch => {
        const card = document.createElement("article");
        card.className = "chapter";

        card.innerHTML = `
          <div class="row">
            <div class="chapter-title">${ch.title}</div>
            <div class="badge">${ch.status}</div>
          </div>
          <div class="muted2" style="margin-top:6px">Estimated duration: ${ch.duration_hours}h</div>
          <div class="divider"></div>
          <div class="row">
            <div class="muted">Progress</div>
            <div class="muted"><b>${ch.progress}%</b></div>
          </div>
          <div class="pbar" style="margin-top:8px">
            <div class="pbar-in" style="width:${ch.progress}%"></div>
          </div>
          <a class="chapter-link" href="./chapters/${ch.id}.html">Open chapter →</a>
        `;

        host.appendChild(card);
      });
    })
    .catch(err => {
      document.getElementById("chapterCards").innerHTML = `
        <section class="panel">
          <h2 style="margin:0 0 8px">Error loading data</h2>
          <div class="muted2">${String(err)}</div>
        </section>
      `;
    });
  </script>
</body>
</html>
"""

index_file.write_text(html, encoding="utf-8")
print(f"Updated {index_file}")
