#!/usr/bin/env python3
from pathlib import Path

index = Path.home() / "arc_strategic_control_center" / "index.html"
html = index.read_text(encoding="utf-8")

cta_css = """
.hero-actions{
  display:flex;
  gap:12px;
  flex-wrap:wrap;
  margin-top:20px;
}
.hero-cta{
  display:inline-flex;
  align-items:center;
  justify-content:center;
  padding:12px 16px;
  border-radius:14px;
  text-decoration:none;
  font-size:15px;
  font-weight:900;
  border:1px solid color-mix(in oklab,var(--accent) 24%, var(--line));
  background:
    radial-gradient(220px 90px at 0% 0%, color-mix(in oklab,var(--accent) 16%, transparent), transparent 68%),
    color-mix(in oklab,var(--panel2) 88%, transparent);
  color:var(--text);
  box-shadow:0 8px 22px rgba(0,0,0,.18);
}
.hero-cta.secondary{
  border-color:color-mix(in oklab,var(--accent) 14%, var(--line));
  background:color-mix(in oklab,var(--panel2) 78%, transparent);
  color:var(--muted);
}
.hero-cta:hover{
  transform:translateY(-1px);
}
"""
if ".hero-actions" not in html:
    html = html.replace("</style>", cta_css + "\n</style>")

needle = """        <div class="kpi-grid">
          <div class="kpi">
            <div class="kpi-label">Current Focus</div>
            <div class="kpi-value" id="kpiCurrentFocus">Security Hardening</div>
          </div>
          <div class="kpi">
            <div class="kpi-label">Active Cluster</div>
            <div class="kpi-value" id="kpiActiveCluster">Prod Safety Core</div>
          </div>
          <div class="kpi">
            <div class="kpi-label">Overall Progress</div>
            <div class="kpi-value" id="kpiOverallProgress">31%</div>
          </div>
          <div class="kpi">
            <div class="kpi-label">Realistic Duration</div>
            <div class="kpi-value" id="kpiRealisticDuration">190h</div>
          </div>
        </div>"""

replacement = needle + """

        <div class="hero-actions">
          <a class="hero-cta" href="./prompts.html">Open Prompt Library</a>
          <a class="hero-cta secondary" href="./chapters/security_hardening.html">Open Current Chapter</a>
        </div>"""

if 'href="./prompts.html"' not in html or 'Open Prompt Library' not in html:
    html = html.replace(needle, replacement)

index.write_text(html, encoding="utf-8")
print("Homepage prompt CTA added")
