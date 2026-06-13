from pathlib import Path

index = Path.home() / "arc_strategic_control_center" / "index.html"
html = index.read_text(encoding="utf-8")

html = html.replace(
"""position:sticky;top:0;z-index:1000;""",
"""position:fixed;top:0;left:0;right:0;z-index:1200;"""
)

html = html.replace(
""".sidebar{
position:fixed;
left:0;
top:70px;""",
""".sidebar{
position:fixed;
left:0;
top:78px;"""
)

if ".main{" in html:
    html = html.replace(
        """.main{
margin-left:240px;
}""",
        """.main{
margin-left:240px;
padding-top:88px;
}"""
    )
else:
    html = html.replace(
        "<div class=\"main\">",
        "<div class=\"main\" style=\"margin-left:240px;padding-top:88px;\">"
    )

index.write_text(html, encoding="utf-8")
print("Topbar fixed and sidebar aligned")
