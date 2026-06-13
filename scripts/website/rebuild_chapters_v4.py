#!/usr/bin/env python3

import json
from pathlib import Path
from html import escape

base = Path.home() / "arc_strategic_control_center"

progress = json.loads((base / "data" / "progress.json").read_text())

structure = json.loads((base / "data" / "project_structure.json").read_text())

chapters_dir = base / "chapters"
chapters_dir.mkdir(exist_ok=True)

prompt_links = {
    "security_hardening":{
        "cluster":{
            "prod_safety_core":"../security_prompts.html#cluster-prompt"
        },
        "blocks":{
            "b07":"../security_prompts.html#b07",
            "b08":"../security_prompts.html#b08",
            "b09":"../security_prompts.html#b09",
            "b10":"../security_prompts.html#b10",
            "b11":"../security_prompts.html#b11"
        }
    }
}

for chapter in progress["chapters"]:

    cid = chapter["id"]
    title = chapter["title"]

    clusters_html = ""

    for cluster in chapter["clusters"]:

        cluster_id = cluster["id"]

        if cid in prompt_links and cluster_id in prompt_links[cid]["cluster"]:
            cluster_prompt = f'<a class="action-btn" href="{prompt_links[cid]["cluster"][cluster_id]}">Open Cluster Prompt</a>'
        else:
            cluster_prompt = '<span class="action-btn secondary">Prompt later</span>'

        blocks_html = ""

        for block in cluster["blocks"]:

            block_id = block["id"]
            block_title = block["title"]
            status = block["status"]

            if cid in prompt_links and block_id in prompt_links[cid]["blocks"]:
                prompt_btn = f'<a class="action-btn" href="{prompt_links[cid]["blocks"][block_id]}">Open Block Prompt</a>'
            else:
                prompt_btn = '<span class="action-btn secondary">Prompt later</span>'

            blocks_html += f"""
<div class="block-card {status}">
<div class="block-title">{escape(block_title)}</div>
<div class="block-status">{status}</div>
<div class="block-actions">{prompt_btn}</div>
</div>
"""

        clusters_html += f"""
<section class="cluster-card">

<h2>{escape(cluster["title"])}</h2>

<div class="cluster-meta">
{cluster["done_blocks"]}/{cluster["total_blocks"]} blocks done
</div>

<div class="cluster-actions">
{cluster_prompt}
</div>

<div class="block-grid">
{blocks_html}
</div>

</section>
"""

    html = f"""
<html>
<head>

<title>{title}</title>

<style>

body{{
font-family:Inter;
background:#0b0b0d;
color:white;
padding:40px;
}}

.cluster-card{{
background:#16161a;
border-radius:16px;
padding:24px;
margin-bottom:24px;
border:1px solid #2c2c33;
}}

.block-grid{{
display:grid;
grid-template-columns:repeat(auto-fill,minmax(260px,1fr));
gap:12px;
margin-top:14px;
}}

.block-card{{
background:#1e1e24;
padding:14px;
border-radius:12px;
border:1px solid #333;
}}

.block-card.finished{{border-color:#35d399}}
.block-card.started{{border-color:#fbbf24}}
.block-card.planned{{border-color:#6b7280}}

.block-title{{font-weight:700}}

.block-status{{font-size:13px;color:#aaa}}

.action-btn{{
display:inline-block;
margin-top:8px;
padding:6px 10px;
background:#d6b35e;
border-radius:6px;
text-decoration:none;
color:black;
font-weight:600;
}}

.secondary{{background:#444;color:#ddd}}

</style>

</head>

<body>

<h1>{title}</h1>

{clusters_html}

</body>
</html>
"""

    (chapters_dir / f"{cid}.html").write_text(html)

print("Chapters rebuilt successfully")
