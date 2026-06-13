from pathlib import Path

index = Path.home() / "arc_strategic_control_center" / "index.html"
html = index.read_text(encoding="utf-8")

html = html.replace(
""".topbar{
  position:sticky;top:0;z-index:60;
  background:color-mix(in oklab,var(--panel) 84%, transparent);
  backdrop-filter:blur(12px);
  border-bottom:1px solid var(--line);
}""",
""".topbar{
  position:sticky;top:0;z-index:60;
  background:color-mix(in oklab,var(--panel) 88%, black 4%);
  backdrop-filter:blur(14px);
  border-bottom:1px solid color-mix(in oklab,var(--accent) 24%, var(--line));
  box-shadow:0 10px 24px rgba(0,0,0,.22);
}"""
)

html = html.replace(
""".logo{
  font-size:22px;
  font-weight:900;
  letter-spacing:.2px;
}
.logo-sub{
  margin-top:4px;
  font-size:13px;
  color:var(--muted2);
}""",
""".logo-wrap{
  display:inline-flex;
  flex-direction:column;
  gap:4px;
  padding:8px 12px;
  border-radius:16px;
  border:1px solid color-mix(in oklab,var(--accent) 24%, var(--line));
  background:
    radial-gradient(220px 80px at 0% 0%, color-mix(in oklab,var(--accent) 14%, transparent), transparent 68%),
    color-mix(in oklab,var(--panel2) 82%, transparent);
  box-shadow:0 0 0 1px rgba(255,255,255,.02) inset;
}
.logo{
  font-size:24px;
  font-weight:950;
  letter-spacing:.2px;
  color:color-mix(in oklab,var(--accent2) 82%, var(--text));
  line-height:1.1;
}
.logo-sub{
  margin-top:0;
  font-size:13px;
  color:var(--muted2);
  line-height:1.3;
}"""
)

html = html.replace(
"""      <div>
        <div class="logo">The Arc Strategic Control Center</div>
        <div class="logo-sub">Architecture, Governance & Deployment Hub</div>
      </div>""",
"""      <div class="logo-wrap">
        <div class="logo">The Arc Strategic Control Center</div>
        <div class="logo-sub">Architecture, Governance & Deployment Hub</div>
      </div>"""
)

html = html.replace(
""".nav a,.btn,select{
  text-decoration:none;
  color:var(--muted);
  font-size:14px;
  padding:9px 13px;
  border-radius:999px;
  border:1px solid var(--line);
  background:color-mix(in oklab,var(--panel2) 76%, transparent);
  cursor:pointer;
}""",
""".nav a,.btn,select{
  text-decoration:none;
  color:var(--muted);
  font-size:14px;
  padding:9px 13px;
  border-radius:999px;
  border:1px solid color-mix(in oklab,var(--accent) 16%, var(--line));
  background:color-mix(in oklab,var(--panel2) 78%, transparent);
  cursor:pointer;
  transition:transform .14s ease, border-color .14s ease, color .14s ease, background .14s ease;
}
.nav a:hover,.btn:hover,select:hover{
  transform:translateY(-1px);
  border-color:color-mix(in oklab,var(--accent) 38%, var(--line));
  color:var(--text);
  background:color-mix(in oklab,var(--panel2) 90%, transparent);
}"""
)

index.write_text(html, encoding="utf-8")
print("Topbar polished")
