#!/usr/bin/env python3
import json
from pathlib import Path
from html import escape

base = Path.home() / "arc_strategic_control_center"

progress = json.loads((base / "data" / "progress.json").read_text())

security_prompts = json.loads((base / "data" / "security_prompts.json").read_text())

html_sections = []

for chapter in progress["chapters"]:

    cid = chapter["id"]
    title = chapter["title"]

    chapter_prompt = ""
    cluster_prompts = ""
    block_prompts = ""

    if cid == "security_hardening":

        chapter_prompt = f"""
        <div class="prompt-card" id="chapter-security">
        <h3>Chapter Prompt</h3>
        <pre>{escape(security_prompts["chapter"]["prompt"])}</pre>
        <button onclick="copyPrompt(this)">Copy Prompt</button>
        </div>
        """

        cluster = security_prompts["cluster"]

        cluster_prompts = f"""
        <div class="prompt-card" id="cluster-prod_safety_core">
        <h3>Cluster Prompt — {cluster["title"]}</h3>
        <pre>{escape(cluster["prompt"])}</pre>
        <button onclick="copyPrompt(this)">Copy Prompt</button>
        </div>
        """

        for block in security_prompts["blocks"]:

            block_prompts += f"""
            <div class="prompt-card" id="{block["id"]}">
            <h3>{block["title"]}</h3>
            <pre>{escape(block["prompt"])}</pre>
            <button onclick="copyPrompt(this)">Copy Prompt</button>
            </div>
            """

    section = f"""
    <section class="chapter-prompts" id="prompts-{cid}">
    <h2>{title}</h2>
    {chapter_prompt}
    {cluster_prompts}
    {block_prompts}
    </section>
    """

    html_sections.append(section)

html = f"""
<html>
<head>

<title>The Arc Prompt Library</title>

<style>

body{{
font-family:Inter;
background:#0b0b0d;
color:white;
padding:40px;
}}

.chapter-prompts{{
margin-bottom:60px;
}}

.prompt-card{{
background:#16161a;
border-radius:16px;
padding:20px;
margin-bottom:20px;
border:1px solid #2c2c33;
}}

pre{{
white-space:pre-wrap;
font-family:monospace;
font-size:14px;
}}

button{{
margin-top:10px;
padding:8px 12px;
background:#d6b35e;
border:none;
border-radius:6px;
font-weight:600;
cursor:pointer;
}}

</style>

<script>

function copyPrompt(btn){{
let text = btn.parentElement.querySelector("pre").innerText
navigator.clipboard.writeText(text)
btn.innerText="Copied"
setTimeout(()=>btn.innerText="Copy Prompt",1200)
}}

</script>

</head>

<body>

<h1>The Arc Prompt Library</h1>

{''.join(html_sections)}

</body>
</html>
"""

(base / "prompts.html").write_text(html)

print("Prompt hub rebuilt")

