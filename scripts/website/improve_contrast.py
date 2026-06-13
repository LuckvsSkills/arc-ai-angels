from pathlib import Path

index = Path.home() / "arc_strategic_control_center/index.html"
html = index.read_text()

html = html.replace(
"--bg0: #121a24;",
"--bg0: #1a2432;"
)

html = html.replace(
"--bg1: #162231;",
"--bg1: #202c3d;"
)

html = html.replace(
"background: var(--panel);",
"background: color-mix(in oklab,var(--panel) 85%, white 5%);"
)

html = html.replace(
"background: var(--card);",
"background: color-mix(in oklab,var(--card) 85%, white 6%);"
)

html = html.replace(
"box-shadow: var(--shadow2);",
"box-shadow: 0 12px 32px rgba(0,0,0,.35), 0 0 0 1px var(--accentGlow);"
)

index.write_text(html)

print("Contrast update applied")
