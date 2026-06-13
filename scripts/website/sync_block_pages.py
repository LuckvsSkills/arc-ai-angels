from pathlib import Path
import json
import re
import html
from typing import Optional

ROOT = Path("/home/prime/arc_strategic_control_center")
PROGRESS = ROOT / "data" / "progress.json"
BLOCK_ROOT = ROOT / "data" / "block_content"
CHAPTERS_DIR = ROOT / "chapters"
BLOCK_PAGES_DIR = CHAPTERS_DIR / "blocks"

if not PROGRESS.exists():
    raise SystemExit(f"Missing {PROGRESS}")

data = json.loads(PROGRESS.read_text(encoding="utf-8"))
chapters = data.get("chapters", data if isinstance(data, list) else [])
if not isinstance(chapters, list):
    raise SystemExit("progress.json chapters format not recognized")

CHAPTER_COLORS = {
    "platform_runtime": "#3fe3b5",
    "security_hardening": "#36c9ff",
    "model_runtime": "#9b7cff",
    "data_memory": "#4ea8de",
    "agent_logic": "#ff4d6d",
    "observability": "#ff9f43",
    "control_center": "#d6b35e",
    "mission_control_ops": "#7fb8ff",
}

def find_block_file(chapter_id: str, block_id: str) -> Optional[Path]:
    chapter_dir = BLOCK_ROOT / chapter_id
    if not chapter_dir.exists():
        return None
    matches = sorted(chapter_dir.glob(f"*__{block_id[-2:]}__*.md"))
    if matches:
        return matches[0]
    legacy = chapter_dir / f"{block_id}.md"
    if legacy.exists():
        return legacy
    return None

def md_to_html(text: str) -> str:
    lines = text.splitlines()

    while lines and not lines[0].strip():
        lines.pop(0)
    if lines and lines[0].startswith("# "):
        lines.pop(0)
    while lines and not lines[0].strip():
        lines.pop(0)
    if lines and lines[0].startswith("## "):
        lines.pop(0)

    out = []
    in_ul = False
    in_ol = False
    in_code = False
    code_lines = []
    code_lang = None
    code_lang = None

    def close_lists():
        nonlocal in_ul, in_ol
        if in_ul:
            out.append("</ul>")
            in_ul = False
        if in_ol:
            out.append("</ol>")
            in_ol = False

    def close_code():
        nonlocal in_code, code_lines, code_lang
        if in_code:
            code_content = "\n".join(code_lines)
            if code_lang == "mermaid":
                # Mermaid diagram - geen escaping, speciale div
                out.append(f'<div class="mermaid">{code_content}</div>')
            else:
                # Normale code - wel escapen
                escaped = html.escape(code_content)
                out.append(f"<pre><code>{escaped}</code></pre>")
            in_code = False
            code_lines = []
            code_lang = None

    for raw in lines:
        line = raw.rstrip("\n")

        if line.strip().startswith("```"):
            close_lists()
            if in_code:
                close_code()
            else:
                in_code = True
                code_lines = []
                # Detecteer taal (bijv. ```mermaid)
                lang_match = re.match(r"```(\w+)", line.strip())
                code_lang = lang_match.group(1) if lang_match else None
            continue

        if in_code:
            code_lines.append(line)
            continue

        if not line.strip():
            close_lists()
            continue

        if line.startswith("### "):
            close_lists()
            out.append(f"<h3>{html.escape(line[4:])}</h3>")
            continue
        if line.startswith("## "):
            close_lists()
            out.append(f"<h2>{html.escape(line[3:])}</h2>")
            continue
        if line.startswith("# "):
            close_lists()
            out.append(f"<h1>{html.escape(line[2:])}</h1>")
            continue

        if re.match(r"^\d+\.\s+", line):
            if not in_ol:
                close_lists()
                out.append("<ol>")
                in_ol = True
            item = re.sub(r"^\d+\.\s+", "", line)
            out.append(f"<li>{html.escape(item)}</li>")
            continue

        if line.startswith("- "):
            if not in_ul:
                close_lists()
                out.append("<ul>")
                in_ul = True
            out.append(f"<li>{html.escape(line[2:])}</li>")
            continue

        close_lists()
        out.append(f"<p>{html.escape(line)}</p>")

    close_lists()
    close_code()
    return "\n".join(out)

def ensure_block_page(chapter, block):
    chapter_id = chapter["id"]
    chapter_title = chapter["title"]
    block_id = block["id"]
    block_title = block["title"]
    color = CHAPTER_COLORS.get(chapter_id, "#7fb8ff")
    source = find_block_file(chapter_id, block_id)

    if source and source.exists():
        md = source.read_text(encoding="utf-8")
    else:
        md = f"# {chapter_title}\n## Block {block_id[-2:]} — {block_title}\n\n### Purpose\nTBD\n"

    rendered = md_to_html(md)
    out_dir = BLOCK_PAGES_DIR / chapter_id
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / f"{block_id}.html"

    page = f"""<!DOCTYPE html>
<html lang="nl">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width,initial-scale=1.0">
  <title>{html.escape(chapter_title)} — {html.escape(block_title)}</title>
  <style>
    :root {{
      --bg: #0b1020;
      --panel: #121a2b;
      --line: rgba(255,255,255,.10);
      --text: #eef4ff;
      --muted: #a8b7d1;
      --accent: {color};
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      background:
        radial-gradient(circle at top left, color-mix(in srgb, var(--accent) 18%, transparent), transparent 35%),
        linear-gradient(180deg, #0a0f1d 0%, #0d1324 100%);
      color: var(--text);
      font-family: Inter, Arial, sans-serif;
    }}
    .wrap {{
      width: min(1080px, 92vw);
      margin: 0 auto;
      padding: 32px 0 72px;
    }}
    .topbar {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 18px;
      margin-bottom: 24px;
      flex-wrap: wrap;
    }}
    .backlink {{
      color: var(--accent);
      text-decoration: none;
      font-weight: 800;
      font-size: 16px;
    }}
    .meta {{
      color: var(--muted);
      font-size: 15px;
      font-weight: 700;
    }}
    .hero {{
      background: linear-gradient(180deg, color-mix(in srgb, var(--accent) 12%, var(--panel)) 0%, var(--panel) 100%);
      border: 1px solid var(--line);
      border-radius: 28px;
      padding: 28px 28px 22px;
      box-shadow: 0 20px 60px rgba(0,0,0,.25);
      margin-bottom: 22px;
    }}
    .content {{
      background: color-mix(in srgb, var(--panel) 94%, transparent);
      border: 1px solid var(--line);
      border-radius: 28px;
      padding: 34px;
      box-shadow: 0 20px 60px rgba(0,0,0,.22);
    }}
    h1 {{
      margin: 0 0 8px;
      font-size: clamp(34px, 4vw, 46px);
      line-height: 1.1;
      color: var(--text);
    }}
    h2 {{
      margin: 0;
      font-size: clamp(24px, 2.6vw, 30px);
      line-height: 1.2;
      color: var(--accent);
    }}
    h3 {{
      margin: 30px 0 12px;
      font-size: 24px;
      line-height: 1.2;
      color: var(--text);
      padding-bottom: 8px;
      border-bottom: 1px solid color-mix(in srgb, var(--accent) 40%, var(--line));
    }}
    p, li {{
      font-size: 18px;
      line-height: 1.8;
      color: var(--text);
    }}
    ul, ol {{
      margin: 0 0 18px 24px;
      padding: 0;
    }}
    pre {{
      margin: 16px 0 22px;
      padding: 18px 20px;
      background: #0a0f1a;
      border: 1px solid color-mix(in srgb, var(--accent) 30%, var(--line));
      border-radius: 18px;
      overflow: auto;
      color: #eaf1ff;
      font-size: 16px;
      line-height: 1.7;
    }}
    code {{
      font-family: "SFMono-Regular", Consolas, monospace;
    }}
    @media (max-width: 720px) {{
      .content, .hero {{ padding: 22px; }}
      p, li {{ font-size: 17px; }}
      h3 {{ font-size: 21px; }}
    }}
  </style>
</head>
<body>
  <div class="wrap">
    <div class="topbar">
      <a class="backlink" href="../../{chapter_id}.html">← Terug naar hoofdstuk</a>
      <div class="meta">{html.escape(chapter_title)} · {html.escape(block_id.upper())}</div>
    </div>

    <div class="hero">
      <h1>{html.escape(chapter_title)}</h1>
      <h2>Block {html.escape(block_id[-2:])} — {html.escape(block_title)}</h2>
    </div>

    <div class="content">
      {rendered}
    </div>
  </div>
</body>
</html>
"""
    out_file.write_text(page, encoding="utf-8")

def patch_chapter_page(chapter):
    chapter_id = chapter["id"]
    chapter_file = CHAPTERS_DIR / f"{chapter_id}.html"
    if not chapter_file.exists():
        return

    text = chapter_file.read_text(encoding="utf-8")

    if ".block-link{" not in text:
        text = text.replace(
            "</style>",
            """
.block-link{
  color:inherit;
  text-decoration:none;
  font-weight:800;
}
.block-link:hover{
  text-decoration:underline;
}
""" + "\n</style>",
            1
        )

    for cluster in chapter.get("clusters", []):
        for block in cluster.get("blocks", []):
            title = block["title"]
            href = f"./blocks/{chapter_id}/{block['id']}.html"
            if href in text:
                continue
            pattern = rf"(<div class=\"block-title\">)\s*({re.escape(title)})\s*(</div>)"
            replacement = rf'\1<a class="block-link" href="{href}">\2</a>\3'
            text = re.sub(pattern, replacement, text, count=1)

    chapter_file.write_text(text, encoding="utf-8")

count = 0
for chapter in chapters:
    for cluster in chapter.get("clusters", []):
        for block in cluster.get("blocks", []):
            ensure_block_page(chapter, block)
            count += 1
    patch_chapter_page(chapter)

print(f"Built/updated {count} block pages")
print("Patched chapter pages with block links")
