#!/usr/bin/env python3
"""
build_admin_panel.py — Forge worker
Bouwt een volledig admin panel voor de website op basis van PROJECT_BRIEF.json
Gebruik: python3 build_admin_panel.py /pad/naar/PROJECT_BRIEF.json
"""
import os, sys, json
from datetime import datetime

def log(msg):
    ts = datetime.now().strftime('%H:%M:%S')
    print(f'[{ts}] {msg}')

def load_brief(path):
    with open(path) as f:
        return json.load(f)

ADMIN_MODULES = {
    'ecommerce':   ['orders', 'products', 'customers', 'analytics', 'settings'],
    'saas':        ['users', 'subscriptions', 'analytics', 'settings', 'billing'],
    'directory':   ['listings', 'categories', 'users', 'analytics', 'settings'],
    'marketplace': ['orders', 'sellers', 'buyers', 'analytics', 'settings', 'payouts'],
    'dashboard':   ['data', 'reports', 'users', 'settings'],
    'community':   ['posts', 'users', 'moderation', 'analytics', 'settings'],
    'booking':     ['reservations', 'calendar', 'customers', 'analytics', 'settings'],
    'blog':        ['posts', 'categories', 'users', 'analytics', 'settings'],
}

def build_admin(brief, code_dir):
    ptype = brief['type']
    naam = brief['project_naam']
    modules = ADMIN_MODULES.get(ptype, ['dashboard', 'users', 'settings'])

    admin_dir = f'{code_dir}/admin'
    os.makedirs(admin_dir, exist_ok=True)

    # Admin index.html
    nav_items = '\n'.join([f'<li><a href="#{m}" onclick="showModule(\'{m}\')">{m.title()}</a></li>' for m in modules])
    modules_html = '\n'.join([f'''
    <div id="module-{m}" class="module" style="display:none">
        <h2>{m.title()}</h2>
        <div class="module-content">
            <div class="stats-grid">
                <div class="stat-card"><div class="stat-value">0</div><div class="stat-label">Totaal</div></div>
                <div class="stat-card"><div class="stat-value">0</div><div class="stat-label">Vandaag</div></div>
                <div class="stat-card"><div class="stat-value">€0</div><div class="stat-label">Omzet</div></div>
            </div>
            <table class="data-table">
                <thead><tr><th>ID</th><th>Naam</th><th>Status</th><th>Datum</th><th>Actie</th></tr></thead>
                <tbody><tr><td colspan="5" style="text-align:center;color:#666">Geen data beschikbaar</td></tr></tbody>
            </table>
        </div>
    </div>''' for m in modules])

    with open(f'{admin_dir}/index.html', 'w') as f:
        f.write(f"""<!DOCTYPE html>
<html lang="nl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{naam} — Admin Panel</title>
    <link rel="stylesheet" href="admin.css">
</head>
<body>
    <div class="admin-layout">
        <aside class="sidebar">
            <div class="sidebar-logo">{naam}<span>Admin</span></div>
            <nav><ul>{nav_items}</ul></nav>
        </aside>
        <main class="admin-main">
            <header class="admin-header">
                <h1 id="current-module">Dashboard</h1>
                <div class="header-actions">
                    <span class="badge">Admin</span>
                    <button onclick="logout()">Uitloggen</button>
                </div>
            </header>
            <div class="admin-content">
                <div id="module-dashboard" class="module">
                    <h2>Dashboard</h2>
                    <div class="stats-grid">
                        <div class="stat-card"><div class="stat-value">0</div><div class="stat-label">Totaal orders</div></div>
                        <div class="stat-card"><div class="stat-value">0</div><div class="stat-label">Actieve gebruikers</div></div>
                        <div class="stat-card"><div class="stat-value">€0</div><div class="stat-label">Omzet vandaag</div></div>
                        <div class="stat-card"><div class="stat-value">0%</div><div class="stat-label">Conversie</div></div>
                    </div>
                </div>
                {modules_html}
            </div>
        </main>
    </div>
    <script src="admin.js"></script>
</body>
</html>""")

    with open(f'{admin_dir}/admin.css', 'w') as f:
        f.write("""* { margin:0; padding:0; box-sizing:border-box; }
body { font-family:'Segoe UI',sans-serif; background:#0f0f17; color:#e2e8f0; }
.admin-layout { display:flex; height:100vh; }
.sidebar { width:220px; background:#0a0a0f; border-right:1px solid rgba(255,255,255,0.08); padding:20px 0; }
.sidebar-logo { padding:0 20px 24px; font-size:18px; font-weight:800; color:#c9a84c; }
.sidebar-logo span { display:block; font-size:11px; font-weight:400; color:#475569; }
nav ul { list-style:none; }
nav ul li a { display:block; padding:10px 20px; color:#94a3b8; text-decoration:none; font-size:14px; transition:all .15s; }
nav ul li a:hover { background:rgba(201,168,76,0.1); color:#c9a84c; }
.admin-main { flex:1; display:flex; flex-direction:column; overflow:hidden; }
.admin-header { padding:16px 24px; border-bottom:1px solid rgba(255,255,255,0.08); display:flex; justify-content:space-between; align-items:center; }
.admin-header h1 { font-size:18px; font-weight:600; }
.header-actions { display:flex; gap:12px; align-items:center; }
.badge { padding:4px 10px; background:rgba(201,168,76,0.15); color:#c9a84c; border-radius:4px; font-size:12px; }
.header-actions button { padding:6px 14px; background:transparent; border:1px solid rgba(255,255,255,0.1); color:#94a3b8; border-radius:6px; cursor:pointer; font-size:13px; }
.admin-content { flex:1; overflow:auto; padding:24px; }
.stats-grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(160px,1fr)); gap:16px; margin-bottom:24px; }
.stat-card { background:#111118; border:1px solid rgba(255,255,255,0.06); border-radius:8px; padding:16px; }
.stat-value { font-size:28px; font-weight:700; color:#c9a84c; }
.stat-label { font-size:12px; color:#475569; margin-top:4px; }
.data-table { width:100%; border-collapse:collapse; background:#111118; border-radius:8px; overflow:hidden; }
.data-table th { padding:12px 16px; text-align:left; font-size:12px; font-weight:600; color:#475569; border-bottom:1px solid rgba(255,255,255,0.06); }
.data-table td { padding:12px 16px; font-size:14px; border-bottom:1px solid rgba(255,255,255,0.04); }
.module { display:block; }""")

    with open(f'{admin_dir}/admin.js', 'w') as f:
        f.write("""function showModule(name) {
    document.querySelectorAll('.module').forEach(m => m.style.display = 'none');
    const el = document.getElementById('module-' + name);
    if (el) { el.style.display = 'block'; }
    document.getElementById('current-module').textContent = name.charAt(0).toUpperCase() + name.slice(1);
}
function logout() { if(confirm('Uitloggen?')) window.location.href = '/login'; }
showModule('dashboard');""")

    log(f'✅ Admin panel gebouwd: {len(modules)} modules — {admin_dir}')
    return admin_dir, modules

def update_brief(brief_path, brief, admin_dir, modules):
    brief['admin_dir'] = admin_dir
    brief['admin_modules'] = modules
    brief['admin_built_at'] = datetime.now().isoformat()
    with open(brief_path, 'w') as f:
        json.dump(brief, f, indent=2, ensure_ascii=False)

def main():
    if len(sys.argv) < 2:
        print('Gebruik: python3 build_admin_panel.py /pad/naar/PROJECT_BRIEF.json')
        sys.exit(1)

    brief_path = sys.argv[1]
    brief = load_brief(brief_path)

    if not brief.get('admin_panel'):
        log(f'ℹ️  Admin panel niet vereist voor type: {brief["type"]}')
        sys.exit(0)

    code_dir = brief.get('code_dir')
    if not code_dir:
        print('❌ code_dir niet gevonden — voer eerst clone_template.py uit')
        sys.exit(1)

    log(f'🔧 Admin panel bouwen: {brief["project_naam"]} ({brief["type"]})')
    admin_dir, modules = build_admin(brief, code_dir)
    update_brief(brief_path, brief, admin_dir, modules)

    print('\n' + '='*50)
    print('✅ FORGE ADMIN PANEL KLAAR')
    print(f'   Modules: {", ".join(modules)}')
    print(f'   Map: {admin_dir}')
    print(f'   Volgende: Nero security scan')
    print('='*50)

if __name__ == '__main__':
    main()
