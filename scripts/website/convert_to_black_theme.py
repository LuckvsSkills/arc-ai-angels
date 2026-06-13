from pathlib import Path

index = Path.home() / "arc_strategic_control_center" / "index.html"
html = index.read_text()

replacements = {

"#111827":"#0b0b0c",
"#172131":"#0f0f11",
"#1d2a3d":"#121214",

"#223146":"#161618",
"#29384d":"#1c1c20",
"#31435a":"#232329",

"radial-gradient(1100px 700px at 85% -10%, var(--accentGlow), transparent 55%),":"radial-gradient(1100px 700px at 85% -10%, var(--accentGlow), transparent 60%),",

}

for old,new in replacements.items():
    html = html.replace(old,new)

index.write_text(html)

print("Converted theme to neutral black")
