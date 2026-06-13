#!/usr/bin/env python3
from pathlib import Path

page = Path.home() / "arc_strategic_control_center" / "chapters" / "security_hardening.html"
html = page.read_text(encoding="utf-8")

new_block = """
<section class="panel">
<h2>Security Hardening Overview</h2>

<p class="section-intro">
Security Hardening bestaat uit <strong>5 blokken</strong> verdeeld over <strong>1 cluster</strong>.
De bloknummers (B07–B11) zijn hoofdstukbreed genummerd en vormen samen de cluster <strong>Prod Safety Core</strong>.
</p>

<div class="kpi-grid">

<div class="kpi">
<div class="kpi-label">Total Blocks</div>
<div class="kpi-value">5</div>
</div>

<div class="kpi">
<div class="kpi-label">Total Clusters</div>
<div class="kpi-value">1</div>
</div>

<div class="kpi">
<div class="kpi-label">Blocks Done</div>
<div class="kpi-value">0 / 5</div>
</div>

</div>

</section>
"""

start = html.find("<h2>Security Hardening Overview</h2>")

if start != -1:

    # verwijder oude overview
    end = html.find("</section>", start) + len("</section>")
    html = html[:start] + html[end:]

# voeg nieuwe versie toe net boven clusters
insert_point = html.find("<h2>Clusters</h2>")

html = html[:insert_point] + new_block + html[insert_point:]

page.write_text(html)

print("Security overview simplified")
