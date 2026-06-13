from pathlib import Path

index = Path.home() / "arc_strategic_control_center" / "index.html"
html = index.read_text(encoding="utf-8")

replacements = [
    (
        "border:1px solid var(--line);",
        "border:1px solid color-mix(in oklab,var(--accent) 26%, var(--line));"
    ),
    (
        "border:1px solid color-mix(in oklab,var(--accent) 28%, var(--line));",
        "border:1px solid color-mix(in oklab,var(--accent) 42%, var(--line));"
    ),
    (
        "box-shadow:0 20px 50px rgba(0,0,0,.34);",
        "box-shadow:0 20px 50px rgba(0,0,0,.34), 0 0 0 1px color-mix(in oklab,var(--accent) 18%, transparent);"
    ),
    (
        "box-shadow:0 16px 38px rgba(0,0,0,.34), 0 0 12px color-mix(in oklab,var(--c) 22%, transparent);",
        "box-shadow:0 16px 38px rgba(0,0,0,.34), 0 0 14px color-mix(in oklab,var(--c) 28%, transparent), 0 0 0 1px color-mix(in oklab,var(--c) 20%, transparent);"
    ),
    (
        "border:1px solid var(--line);",
        "border:1px solid color-mix(in oklab,var(--c, var(--accent)) 26%, var(--line));"
    ),
]

# first do selective replacements more safely
html = html.replace(
    "background:color-mix(in oklab,var(--panel) 94%, black 6%);\n  border:1px solid var(--line);",
    "background:color-mix(in oklab,var(--panel) 94%, black 6%);\n  border:1px solid color-mix(in oklab,var(--accent) 26%, var(--line));"
)

html = html.replace(
    "background:color-mix(in oklab,var(--panel3) 92%, black 4%);\n  padding:18px;",
    "background:color-mix(in oklab,var(--panel3) 92%, black 4%);\n  padding:18px;"
)

html = html.replace(
    "border:1px solid var(--line);\n  background:color-mix(in oklab,var(--panel3) 92%, black 4%);",
    "border:1px solid color-mix(in oklab,var(--c) 30%, var(--line));\n  background:color-mix(in oklab,var(--panel3) 92%, black 4%);"
)

html = html.replace(
    "border:1px solid var(--line);\n  background:color-mix(in oklab,var(--panel2) 84%, transparent);",
    "border:1px solid color-mix(in oklab,var(--accent) 22%, var(--line));\n  background:color-mix(in oklab,var(--panel2) 84%, transparent);"
)

html = html.replace(
    "border:1px solid var(--line);\n  background:color-mix(in oklab,var(--panel2) 78%, transparent);",
    "border:1px solid color-mix(in oklab,var(--c, var(--accent)) 24%, var(--line));\n  background:color-mix(in oklab,var(--panel2) 78%, transparent);"
)

html = html.replace(
    "border:1px solid var(--line);\n  background:color-mix(in oklab,var(--panel) 84%, transparent);",
    "border:1px solid color-mix(in oklab,var(--accent) 24%, var(--line));\n  background:color-mix(in oklab,var(--panel) 84%, transparent);"
)

html = html.replace(
    "box-shadow:0 20px 50px rgba(0,0,0,.34);",
    "box-shadow:0 20px 50px rgba(0,0,0,.34), 0 0 0 1px color-mix(in oklab,var(--accent) 18%, transparent);"
)

html = html.replace(
    "box-shadow:0 16px 38px rgba(0,0,0,.34), 0 0 12px color-mix(in oklab,var(--c) 22%, transparent);",
    "box-shadow:0 16px 38px rgba(0,0,0,.34), 0 0 14px color-mix(in oklab,var(--c) 28%, transparent), 0 0 0 1px color-mix(in oklab,var(--c) 20%, transparent);"
)

html = html.replace(
    "border:1px solid var(--line);\n  background:color-mix(in oklab,var(--panel) 94%, black 6%);",
    "border:1px solid color-mix(in oklab,var(--accent) 26%, var(--line));\n  background:color-mix(in oklab,var(--panel) 94%, black 6%);"
)

index.write_text(html, encoding="utf-8")
print("Borders strengthened with theme-color accents")
