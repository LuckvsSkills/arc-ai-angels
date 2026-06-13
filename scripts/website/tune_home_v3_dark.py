from pathlib import Path

index = Path.home() / "arc_strategic_control_center" / "index.html"
html = index.read_text(encoding="utf-8")

replacements = [
    ("--bg0:#243041;", "--bg0:#0f1722;"),
    ("--bg1:#2d3a4d;", "--bg1:#151f2d;"),
    ("--panel:#33445a;", "--panel:#1d2938;"),
    ("--panel2:#3a4d66;", "--panel2:#223245;"),
    ("--card:#3a4d66;", "--card:#243548;"),

    ("background:color-mix(in oklab,var(--panel) 88%, transparent);",
     "background:color-mix(in oklab,var(--panel) 94%, black 6%);"),

    ("background:color-mix(in oklab,var(--card) 92%, transparent);",
     "background:color-mix(in oklab,var(--card) 94%, black 6%);"),

    ('background:linear-gradient(90deg, transparent, var(--c), transparent);',
     'background:linear-gradient(90deg, color-mix(in oklab,var(--c) 45%, transparent), var(--c), color-mix(in oklab,var(--c) 45%, transparent));'),

    ('background:radial-gradient(560px 220px at 0% 0%, color-mix(in oklab,var(--c) 18%, transparent), transparent 62%);',
     'background:radial-gradient(560px 220px at 0% 0%, color-mix(in oklab,var(--c) 26%, transparent), transparent 62%);'),

    ('box-shadow:0 12px 28px rgba(0,0,0,.14);',
     'box-shadow:0 14px 34px rgba(0,0,0,.32), 0 0 0 1px color-mix(in oklab,var(--c) 22%, transparent);'),

    ('box-shadow:0 18px 48px rgba(0,0,0,.18);',
     'box-shadow:0 20px 52px rgba(0,0,0,.34), 0 0 0 1px var(--line);'),

    ('color:var(--muted);font-size:16px;line-height:1.65;',
     'color:var(--muted);font-size:16.5px;line-height:1.72;'),

    ('font-size:21px;',
     'font-size:22px;'),

    ('font-size:17px;',
     'font-size:18px;'),

    ('font-size:30px;',
     'font-size:32px;'),

    ('font-size:48px;',
     'font-size:50px;'),
]

for old, new in replacements:
    html = html.replace(old, new)

index.write_text(html, encoding="utf-8")
print("Homepage tuned: darker background + stronger accents")
