#!/usr/bin/env python3
from pathlib import Path

index = Path.home() / "arc_strategic_control_center" / "index.html"
html = index.read_text(encoding="utf-8")

# 1) voeg ids toe aan KPI values als ze nog niet bestaan
html = html.replace(
    '<div class="kpi-value">Security Hardening</div>',
    '<div class="kpi-value" id="kpiCurrentFocus">Security Hardening</div>'
)
html = html.replace(
    '<div class="kpi-value">Prod Safety Core</div>',
    '<div class="kpi-value" id="kpiActiveCluster">Prod Safety Core</div>'
)
html = html.replace(
    '<div class="kpi-value">31%</div>',
    '<div class="kpi-value" id="kpiOverallProgress">31%</div>'
)
html = html.replace(
    '<div class="kpi-value">190h</div>',
    '<div class="kpi-value" id="kpiRealisticDuration">190h</div>'
)

# 2) voeg ids toe aan chapter cards zodat progress bars later dynamisch zijn
repls = [
    ('href="./chapters/platform_runtime.html" style="--c:var(--runtime)">',
     'href="./chapters/platform_runtime.html" style="--c:var(--runtime)" data-chapter="platform_runtime">'),
    ('href="./chapters/security_hardening.html" style="--c:var(--security)">',
     'href="./chapters/security_hardening.html" style="--c:var(--security)" data-chapter="security_hardening">'),
    ('href="./chapters/model_runtime.html" style="--c:var(--models)">',
     'href="./chapters/model_runtime.html" style="--c:var(--models)" data-chapter="model_runtime">'),
    ('href="./chapters/data_memory.html" style="--c:var(--memory)">',
     'href="./chapters/data_memory.html" style="--c:var(--memory)" data-chapter="data_memory">'),
    ('href="./chapters/agent_logic.html" style="--c:var(--swarm)">',
     'href="./chapters/agent_logic.html" style="--c:var(--swarm)" data-chapter="agent_logic">'),
    ('href="./chapters/observability.html" style="--c:var(--observe)">',
     'href="./chapters/observability.html" style="--c:var(--observe)" data-chapter="observability">'),
    ('href="./chapters/control_center.html" style="--c:var(--ui)">',
     'href="./chapters/control_center.html" style="--c:var(--ui)" data-chapter="control_center">'),
]
for old, new in repls:
    html = html.replace(old, new)

# 3) voeg ids toe aan meta/progress tekst op cards
html = html.replace('<div class="meta"><span>23h</span><span>100%</span></div>', '<div class="meta"><span>23h</span><span class="chapter-pct">100%</span></div>', 1)
html = html.replace('<div class="meta"><span>28h</span><span>0%</span></div>', '<div class="meta"><span>28h</span><span class="chapter-pct">0%</span></div>', 1)
html = html.replace('<div class="meta"><span>22h</span><span>0%</span></div>', '<div class="meta"><span>22h</span><span class="chapter-pct">0%</span></div>', 1)
html = html.replace('<div class="meta"><span>32h</span><span>0%</span></div>', '<div class="meta"><span>32h</span><span class="chapter-pct">0%</span></div>', 1)
html = html.replace('<div class="meta"><span>54h</span><span>0%</span></div>', '<div class="meta"><span>54h</span><span class="chapter-pct">0%</span></div>', 1)
html = html.replace('<div class="meta"><span>24h</span><span>0%</span></div>', '<div class="meta"><span>24h</span><span class="chapter-pct">0%</span></div>', 1)
html = html.replace('<div class="meta"><span>30h</span><span>20%</span></div>', '<div class="meta"><span>30h</span><span class="chapter-pct">20%</span></div>', 1)

# 4) injecteer JS om progress.json te lezen
progress_js = """
fetch('./data/progress.json')
  .then(r => r.json())
  .then(progress => {
    const overall = progress.overall || {};
    const chapters = progress.chapters || [];

    const overallPct = (overall.progress_percent ?? 0) + '%';
    const overallEl = document.getElementById('kpiOverallProgress');
    if (overallEl) overallEl.textContent = overallPct;

    const firstStarted = chapters.find(c => c.status === 'started');
    const firstPlanned = chapters.find(c => c.status === 'planned');
    const currentFocus = firstStarted ? firstStarted.title : (firstPlanned ? firstPlanned.title : 'Completed');
    const currentFocusEl = document.getElementById('kpiCurrentFocus');
    if (currentFocusEl) currentFocusEl.textContent = currentFocus;

    let activeCluster = '—';
    if (firstStarted && firstStarted.clusters && firstStarted.clusters.length) {
      const startedCluster = firstStarted.clusters.find(cl => cl.status === 'started') || firstStarted.clusters[0];
      activeCluster = startedCluster.title;
    } else if (firstPlanned && firstPlanned.clusters && firstPlanned.clusters.length) {
      activeCluster = firstPlanned.clusters[0].title;
    }
    const activeClusterEl = document.getElementById('kpiActiveCluster');
    if (activeClusterEl) activeClusterEl.textContent = activeCluster;

    document.querySelectorAll('.chapter-card[data-chapter]').forEach(card => {
      const id = card.getAttribute('data-chapter');
      const item = chapters.find(c => c.id === id);
      if (!item) return;

      const pctEl = card.querySelector('.chapter-pct');
      if (pctEl) pctEl.textContent = item.progress_percent + '%';

      const barEl = card.querySelector('.pbar > div');
      if (barEl) barEl.style.width = item.progress_percent + '%';
    });
  })
  .catch(err => console.error('Failed to load progress.json', err));
"""

if "fetch('./data/progress.json')" not in html:
    html = html.replace("</script>", progress_js + "\n</script>")

index.write_text(html, encoding="utf-8")
print("Homepage linked to progress.json")
