#!/usr/bin/env python3
from pathlib import Path

page = Path.home() / "arc_strategic_control_center" / "chapters" / "security_hardening.html"
html = page.read_text(encoding="utf-8")

# 1. Extra CSS
extra_css = """
.chapter-overview-grid{
  display:grid;
  grid-template-columns:repeat(3,1fr);
  gap:12px;
  margin-top:18px;
}
@media (max-width:980px){
  .chapter-overview-grid{grid-template-columns:1fr}
}
.chapter-overview-card{
  border-radius:18px;
  border:1px solid color-mix(in oklab,var(--chapter-color) 24%, var(--line));
  background:
    radial-gradient(220px 90px at 0% 0%, color-mix(in oklab,var(--chapter-color) 14%, transparent), transparent 70%),
    color-mix(in oklab,var(--panel2) 84%, transparent);
  padding:14px;
}
.chapter-overview-label{
  font-size:13px;
  color:var(--muted2);
}
.chapter-overview-value{
  font-size:20px;
  font-weight:900;
  margin-top:4px;
}
.chapter-overview-note{
  margin-top:10px;
  color:var(--muted);
  font-size:15px;
  line-height:1.65;
}
.cluster-meta-strong{
  font-weight:800;
  color:var(--text);
}
"""
if ".chapter-overview-grid" not in html:
    html = html.replace("</style>", extra_css + "\n</style>")

# 2. Voeg hoofdstuk-overzicht toe na Goal-sectie
goal_block = """      <section class="section">
        <section class="panel">
          <h2>Chapter Structure</h2>"""

overview_insert = """
      <section class="section">
        <section class="panel">
          <h2>Security Hardening Overview</h2>
          <p class="section-intro">
            Security Hardening bestaat uit <strong>5 totale blokken</strong>, verdeeld over <strong>1 cluster</strong>.
            De bloknummers zijn hoofdstukbreed genummerd. Daarom zie je hier B07 t/m B11 als onderdelen van dit hoofdstuk en van de cluster Prod Safety Core.
          </p>

          <div class="chapter-overview-grid">
            <div class="chapter-overview-card">
              <div class="chapter-overview-label">Total Blocks</div>
              <div class="chapter-overview-value">5</div>
            </div>
            <div class="chapter-overview-card">
              <div class="chapter-overview-label">Total Clusters</div>
              <div class="chapter-overview-value">1</div>
            </div>
            <div class="chapter-overview-card">
              <div class="chapter-overview-label">Blocks Completed</div>
              <div class="chapter-overview-value">0</div>
            </div>
            <div class="chapter-overview-card">
              <div class="chapter-overview-label">Clusters Completed</div>
              <div class="chapter-overview-value">0</div>
            </div>
            <div class="chapter-overview-card">
              <div class="chapter-overview-label">Blocks Remaining</div>
              <div class="chapter-overview-value">5</div>
            </div>
            <div class="chapter-overview-card">
              <div class="chapter-overview-label">Clusters Remaining</div>
              <div class="chapter-overview-value">1</div>
            </div>
          </div>

          <div class="chapter-overview-note">
            Werkvolgorde: eerst cluster-overzicht en clusterprompt, daarna de block prompts binnen dezelfde cluster.
            De promptbron staat centraal in de Prompt Hub, en deze hoofdstukpagina linkt daar direct naartoe.
          </div>
        </section>
      </section>

""" + goal_block

if "Security Hardening Overview" not in html:
    html = html.replace(goal_block, overview_insert)

# 3. Vervang cluster prompt link naar Prompt Hub
html = html.replace(
    'href="../security_prompts.html#cluster-prompt"',
    'href="../prompts.html#cluster-prod_safety_core"'
)

# 4. Vervang block prompt links naar Prompt Hub
replacements = {
    'href="../security_prompts.html#b07"': 'href="../prompts.html#b07"',
    'href="../security_prompts.html#b08"': 'href="../prompts.html#b08"',
    'href="../security_prompts.html#b09"': 'href="../prompts.html#b09"',
    'href="../security_prompts.html#b10"': 'href="../prompts.html#b10"',
    'href="../security_prompts.html#b11"': 'href="../prompts.html#b11"',
}
for old, new in replacements.items():
    html = html.replace(old, new)

# 5. Verduidelijk clustermeta
html = html.replace(
    '<span>Cluster duration: Kort → middel</span>',
    '<span class="cluster-meta-strong">Cluster duration: Kort → middel</span>'
)

page.write_text(html, encoding="utf-8")
print("Security chapter integrated with Prompt Hub")
