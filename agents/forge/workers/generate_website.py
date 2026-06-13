#!/usr/bin/env python3
"""
generate_website.py — Forge worker
Genereert een complete website structuur op basis van requirements
Gebruik: python3 generate_website.py "project-naam" "beschrijving" "features"
"""
import os, sys, json

def generate_website(project_name, description, features):
    base_dir = f'/home/prime/arc_ai_angels/agents/forge/projects/{project_name}'
    os.makedirs(base_dir, exist_ok=True)

    # index.html
    features_html = '\n'.join([f'<li>✅ {f.strip()}</li>' for f in features.split(',')])
    with open(f'{base_dir}/index.html', 'w') as f:
        f.write(f"""<!DOCTYPE html>
<html lang="nl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{project_name}</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header>
        <nav>
            <div class="logo">{project_name}</div>
            <ul>
                <li><a href="#features">Features</a></li>
                <li><a href="#contact">Contact</a></li>
            </ul>
        </nav>
    </header>
    <main>
        <section class="hero">
            <h1>{project_name}</h1>
            <p>{description}</p>
            <a href="#features" class="cta">Ontdek meer</a>
        </section>
        <section id="features">
            <h2>Features</h2>
            <ul class="features-list">
                {features_html}
            </ul>
        </section>
        <section id="contact">
            <h2>Contact</h2>
            <p>Neem contact op voor meer informatie.</p>
        </section>
    </main>
    <footer>
        <p>© 2026 {project_name} — Gebouwd door ARC AI Agents</p>
    </footer>
    <script src="app.js"></script>
</body>
</html>""")

    # style.css
    with open(f'{base_dir}/style.css', 'w') as f:
        f.write("""* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: 'Segoe UI', sans-serif; background: #0a0a0f; color: #e2e8f0; }
nav { display: flex; justify-content: space-between; align-items: center; padding: 20px 40px; background: rgba(255,255,255,0.05); backdrop-filter: blur(10px); position: fixed; width: 100%; top: 0; z-index: 100; }
.logo { font-size: 24px; font-weight: 800; color: #c9a84c; }
nav ul { display: flex; gap: 30px; list-style: none; }
nav ul a { color: #94a3b8; text-decoration: none; transition: color .2s; }
nav ul a:hover { color: #c9a84c; }
.hero { min-height: 100vh; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; padding: 40px; background: linear-gradient(135deg, #0a0a0f 0%, #1a1a2e 100%); }
.hero h1 { font-size: 64px; font-weight: 900; color: #c9a84c; margin-bottom: 20px; }
.hero p { font-size: 20px; color: #94a3b8; max-width: 600px; margin-bottom: 40px; line-height: 1.6; }
.cta { padding: 16px 40px; background: #c9a84c; color: #0a0a0f; border-radius: 50px; text-decoration: none; font-weight: 700; font-size: 16px; transition: all .2s; }
.cta:hover { background: #e2c06a; transform: translateY(-2px); }
#features { padding: 100px 40px; text-align: center; }
#features h2 { font-size: 40px; font-weight: 800; color: #e2e8f0; margin-bottom: 40px; }
.features-list { list-style: none; display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 20px; max-width: 900px; margin: 0 auto; }
.features-list li { background: rgba(255,255,255,0.05); border: 1px solid rgba(201,168,76,0.2); border-radius: 12px; padding: 20px; font-size: 16px; color: #94a3b8; }
#contact { padding: 80px 40px; text-align: center; background: rgba(255,255,255,0.02); }
#contact h2 { font-size: 36px; color: #e2e8f0; margin-bottom: 20px; }
footer { padding: 30px; text-align: center; color: #475569; font-size: 14px; border-top: 1px solid rgba(255,255,255,0.05); }""")

    # app.js
    with open(f'{base_dir}/app.js', 'w') as f:
        f.write("""// Smooth scroll
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({ behavior: 'smooth' });
    });
});
// Fade in on scroll
const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => { if (entry.isIntersecting) entry.target.style.opacity = '1'; });
});
document.querySelectorAll('section').forEach(s => { s.style.opacity = '0'; s.style.transition = 'opacity 0.6s'; observer.observe(s); });
""")

    print(f'✅ Website gegenereerd: {base_dir}')
    print(f'   Files: index.html, style.css, app.js')
    return base_dir

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print('Gebruik: python3 generate_website.py "naam" "beschrijving" "feature1,feature2,feature3"')
        sys.exit(1)
    generate_website(sys.argv[1], sys.argv[2], sys.argv[3])
