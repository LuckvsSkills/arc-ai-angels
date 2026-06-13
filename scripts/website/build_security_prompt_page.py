#!/usr/bin/env python3
import json
from pathlib import Path
from html import escape

base = Path.home() / "arc_strategic_control_center"
src = base / "data" / "security_prompts.json"
out = base / "security_prompts.html"

data = json.loads(src.read_text(encoding="utf-8"))

chapter = data["chapter"]
cluster = data["cluster"]
blocks = data["blocks"]

def block_html(b):
    return f"""
<article class="prompt-card">
<h3>{escape(b["title"])}</h3>
<div class="prompt-meta">{escape(b["id"])} · Block prompt</div>
<pre class="prompt-body">{escape(b["prompt"])}</pre>
<button class="copy-btn">Copy Prompt</button>
</article>
"""

blocks_html = "\n".join([block_html(b) for b in blocks])

html = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Security Hardening Prompts</title>

<style>
body{
font-family:Arial;
background:#0f0f12;
color:white;
margin:40px;
}

.prompt-card{
background:#1a1a1f;
padding:20px;
margin-bottom:20px;
border-radius:10px;
border:1px solid #2c2c35;
}

.prompt-body{
white-space:pre-wrap;
background:#121217;
padding:15px;
border-radius:8px;
border:1px solid #333;
}

.copy-btn{
margin-top:10px;
padding:8px 14px;
background:#d6b35e;
border:none;
border-radius:6px;
font-weight:bold;
cursor:pointer;
}
</style>

</head>
<body>

<h1>Security Hardening Prompts</h1>

<h2>Chapter Prompt</h2>

<div class="prompt-card">
<h3>""" + escape(chapter["title"]) + """</h3>
<pre class="prompt-body">""" + escape(chapter["prompt"]) + """</pre>
<button class="copy-btn">Copy Prompt</button>
</div>

<h2>Cluster Prompt</h2>

<div class="prompt-card">
<h3>""" + escape(cluster["title"]) + """</h3>
<pre class="prompt-body">""" + escape(cluster["prompt"]) + """</pre>
<button class="copy-btn">Copy Prompt</button>
</div>

<h2>Block Prompts</h2>

""" + blocks_html + """

<script>
document.querySelectorAll(".copy-btn").forEach(btn=>{
btn.onclick=()=>{
const text=btn.parentElement.querySelector(".prompt-body").innerText
navigator.clipboard.writeText(text)
btn.innerText="Copied!"
setTimeout(()=>btn.innerText="Copy Prompt",1200)
}
})
</script>

</body>
</html>
"""

out.write_text(html,encoding="utf-8")

print("Built:", out)
