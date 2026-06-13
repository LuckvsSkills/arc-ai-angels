from pathlib import Path

index = Path.home() / "arc_strategic_control_center" / "index.html"
html = index.read_text(encoding="utf-8")

# 1) Dark theme closer to the nice white-theme separation
html = html.replace("--bg0:#0c1420;", "--bg0:#111827;")
html = html.replace("--bg1:#101a28;", "--bg1:#172131;")
html = html.replace("--bg2:#162233;", "--bg2:#1d2a3d;")

html = html.replace("--panel:#182433;", "--panel:#223146;")
html = html.replace("--panel2:#1d2b3d;", "--panel2:#29384d;")
html = html.replace("--panel3:#223246;", "--panel3:#31435a;")

html = html.replace(
    "background:color-mix(in oklab,var(--panel) 94%, black 6%);",
    "background:color-mix(in oklab,var(--panel) 92%, black 8%);"
)
html = html.replace(
    "background:color-mix(in oklab,var(--panel3) 92%, black 4%);",
    "background:color-mix(in oklab,var(--panel3) 90%, black 6%);"
)

# Add a subtle inner highlight to panels/cards
html = html.replace(
    "box-shadow:0 20px 50px rgba(0,0,0,.34), 0 0 0 1px color-mix(in oklab,var(--accent) 18%, transparent);",
    "box-shadow:0 20px 50px rgba(0,0,0,.34), 0 0 0 1px color-mix(in oklab,var(--accent) 18%, transparent), inset 0 1px 0 rgba(255,255,255,.04);"
)
html = html.replace(
    "box-shadow:0 16px 38px rgba(0,0,0,.34), 0 0 14px color-mix(in oklab,var(--c) 28%, transparent), 0 0 0 1px color-mix(in oklab,var(--c) 20%, transparent);",
    "box-shadow:0 16px 38px rgba(0,0,0,.34), 0 0 14px color-mix(in oklab,var(--c) 28%, transparent), 0 0 0 1px color-mix(in oklab,var(--c) 20%, transparent), inset 0 1px 0 rgba(255,255,255,.04);"
)

# 2) Add active nav styling
insert_css = """
.nav a.active{
  color:var(--text);
  border-color:color-mix(in oklab,var(--accent) 44%, var(--line));
  background:
    radial-gradient(180px 70px at 0% 0%, color-mix(in oklab,var(--accent) 18%, transparent), transparent 68%),
    color-mix(in oklab,var(--panel2) 92%, transparent);
  box-shadow:0 0 0 1px color-mix(in oklab,var(--accent) 18%, transparent), inset 0 1px 0 rgba(255,255,255,.05);
}
"""

if ".nav a.active" not in html:
    html = html.replace("</style>", insert_css + "\n</style>")

# 3) Add nav ids and active-nav script
html = html.replace('<a href="#home">Home</a>', '<a href="#home" data-nav="home">Home</a>')
html = html.replace('<a href="#chapters">Chapters</a>', '<a href="#chapters" data-nav="chapters">Chapters</a>')
html = html.replace('<a href="#architecture">Architecture</a>', '<a href="#architecture" data-nav="architecture">Architecture</a>')
html = html.replace('<a href="#roadmap">Roadmap</a>', '<a href="#roadmap" data-nav="roadmap">Roadmap</a>')

active_script = """
function updateActiveNav(){
  const sections = [
    { id: 'home', el: document.getElementById('home') },
    { id: 'chapters', el: document.getElementById('chapters') },
    { id: 'architecture', el: document.getElementById('architecture') },
    { id: 'roadmap', el: document.getElementById('roadmap') }
  ];

  let current = 'home';
  const offset = 120;

  sections.forEach(s => {
    if(!s.el) return;
    const rect = s.el.getBoundingClientRect();
    if(rect.top <= offset && rect.bottom > offset){
      current = s.id;
    }
  });

  document.querySelectorAll('.nav a[data-nav]').forEach(a => {
    a.classList.toggle('active', a.dataset.nav === current);
  });
}

window.addEventListener('scroll', updateActiveNav, { passive: true });
window.addEventListener('load', updateActiveNav);
"""

if "function updateActiveNav()" not in html:
    html = html.replace("</script>", active_script + "\n</script>")

index.write_text(html, encoding="utf-8")
print("Dark theme refined and active nav added")
