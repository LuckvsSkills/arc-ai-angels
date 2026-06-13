from pathlib import Path

index = Path.home() / "arc_strategic_control_center/index.html"
html = index.read_text()

replacements = [

("var(--accentGlow), transparent 60%",
"color-mix(in oklab,var(--accentGlow) 140%, transparent), transparent 60%"),

("color-mix(in oklab,var(--c) 45%, transparent), var(--c), color-mix(in oklab,var(--c) 45%, transparent)",
"color-mix(in oklab,var(--c) 60%, transparent), var(--c), color-mix(in oklab,var(--c) 60%, transparent)"),

("color-mix(in oklab,var(--c) 26%, transparent)",
"color-mix(in oklab,var(--c) 38%, transparent)"),

("0 14px 34px rgba(0,0,0,.32)",
"0 16px 38px rgba(0,0,0,.36), 0 0 12px color-mix(in oklab,var(--c) 30%, transparent)"),

("stroke=\"var(--accent)\"",
"stroke=\"color-mix(in oklab,var(--accent) 130%, white 10%)\""),

]

for old,new in replacements:
    html = html.replace(old,new)

index.write_text(html)

print("Accent colors boosted")
