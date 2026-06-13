#!/usr/bin/env python3
"""
seed_initial_data.py — Axon worker
Voert basis data in voor een geprovisioneerde database
Gebruik: python3 seed_initial_data.py /pad/naar/PROJECT_BRIEF.json
"""
import os, sys, json, sqlite3, hashlib
from datetime import datetime

def log(msg):
    ts = datetime.now().strftime('%H:%M:%S')
    print(f'[{ts}] {msg}')

def load_brief(path):
    with open(path) as f:
        return json.load(f)

def hash_password(pwd):
    return hashlib.sha256(pwd.encode()).hexdigest()

def seed_database(brief, db_path):
    ptype = brief['type']
    naam = brief['project_naam']
    conn = sqlite3.connect(db_path)
    seeded = []
    try:
        # Admin gebruiker voor alle types
        if ptype not in ['landing', 'portfolio']:
            try:
                conn.execute("INSERT OR IGNORE INTO users (email, password, naam, role) VALUES (?, ?, ?, ?)",
                    ('admin@' + naam.lower().replace(' ', '') + '.nl', hash_password('admin123'), 'Admin', 'admin'))
                seeded.append('admin gebruiker')
            except: pass
            try:
                conn.execute("INSERT OR IGNORE INTO users (email, password, naam, rol) VALUES (?, ?, ?, ?)",
                    ('admin@' + naam.lower().replace(' ', '') + '.nl', hash_password('admin123'), 'Admin', 'admin'))
                seeded.append('admin gebruiker (rol)')
            except: pass

        # Type-specifieke seed data
        if ptype == 'blog':
            conn.execute("INSERT OR IGNORE INTO categories (naam, slug) VALUES (?, ?)", ('Algemeen', 'algemeen'))
            conn.execute("INSERT OR IGNORE INTO categories (naam, slug) VALUES (?, ?)", ('Nieuws', 'nieuws'))
            conn.execute("INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)", ('site_naam', naam))
            seeded.append('blog categorieën + instellingen')

        elif ptype == 'ecommerce':
            conn.execute("INSERT OR IGNORE INTO categories (naam, slug, beschrijving) VALUES (?, ?, ?)", ('Nieuw', 'nieuw', 'Nieuwe producten'))
            conn.execute("INSERT OR IGNORE INTO categories (naam, slug, beschrijving) VALUES (?, ?, ?)", ('Populair', 'populair', 'Populaire producten'))
            conn.execute("INSERT OR IGNORE INTO products (naam, slug, beschrijving, prijs, voorraad, category_id) VALUES (?, ?, ?, ?, ?, ?)",
                ('Demo Product', 'demo-product', 'Dit is een demo product', 29.99, 100, 1))
            seeded.append('demo product + categorieën')

        elif ptype == 'saas':
            conn.execute("INSERT OR IGNORE INTO plans (naam, prijs, interval, features) VALUES (?, ?, ?, ?)",
                ('Starter', 9.99, 'maand', 'Basis features, 1 gebruiker'))
            conn.execute("INSERT OR IGNORE INTO plans (naam, prijs, interval, features) VALUES (?, ?, ?, ?)",
                ('Pro', 29.99, 'maand', 'Alle features, 5 gebruikers'))
            conn.execute("INSERT OR IGNORE INTO plans (naam, prijs, interval, features) VALUES (?, ?, ?, ?)",
                ('Enterprise', 99.99, 'maand', 'Alles ongelimiteerd'))
            seeded.append('3 abonnementen plans')

        elif ptype == 'directory':
            conn.execute("INSERT OR IGNORE INTO categories (naam, slug, icon) VALUES (?, ?, ?)", ('Restaurants', 'restaurants', '🍽️'))
            conn.execute("INSERT OR IGNORE INTO categories (naam, slug, icon) VALUES (?, ?, ?)", ('Winkels', 'winkels', '🛍️'))
            conn.execute("INSERT OR IGNORE INTO categories (naam, slug, icon) VALUES (?, ?, ?)", ('Services', 'services', '🔧'))
            conn.execute("INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)", ('site_naam', naam))
            seeded.append('directory categorieën')

        elif ptype == 'community':
            conn.execute("INSERT OR IGNORE INTO categories (naam, slug, beschrijving) VALUES (?, ?, ?)", ('Algemeen', 'algemeen', 'Algemene discussies'))
            conn.execute("INSERT OR IGNORE INTO categories (naam, slug, beschrijving) VALUES (?, ?, ?)", ('Introductie', 'introductie', 'Stel jezelf voor'))
            seeded.append('community categorieën')

        elif ptype == 'booking':
            conn.execute("INSERT OR IGNORE INTO services (naam, beschrijving, duur_minuten, prijs) VALUES (?, ?, ?, ?)",
                ('Consult', 'Eerste consult', 60, 75.00))
            conn.execute("INSERT OR IGNORE INTO services (naam, beschrijving, duur_minuten, prijs) VALUES (?, ?, ?, ?)",
                ('Follow-up', 'Vervolg afspraak', 30, 45.00))
            seeded.append('demo services')

        elif ptype == 'dashboard':
            conn.execute("INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)", ('dashboard_naam', naam))
            conn.execute("INSERT OR IGNORE INTO data_sources (naam, type, config) VALUES (?, ?, ?)",
                ('Demo Bron', 'json', '{"url": "https://api.example.com/data"}'))
            seeded.append('dashboard instellingen + demo bron')

        conn.commit()
        log(f'✅ Seed data ingevoerd: {", ".join(seeded)}')
    except Exception as e:
        log(f'⚠️  Seed fout: {e}')
    finally:
        conn.close()
    return seeded

def update_brief(brief_path, brief, seeded):
    if 'database' in brief:
        brief['database']['seeded'] = seeded
        brief['database']['seeded_at'] = datetime.now().isoformat()
    brief['sentinels']['axon'] = 'SEED_DONE'
    with open(brief_path, 'w') as f:
        json.dump(brief, f, indent=2, ensure_ascii=False)

def main():
    if len(sys.argv) < 2:
        print('Gebruik: python3 seed_initial_data.py /pad/naar/PROJECT_BRIEF.json')
        sys.exit(1)
    brief_path = sys.argv[1]
    brief = load_brief(brief_path)
    db_info = brief.get('database', {})
    db_path = db_info.get('path')
    if not db_path or not os.path.exists(db_path):
        log('⚠️  Geen database gevonden — voer eerst provision_database.py uit')
        sys.exit(0)
    log(f'🌱 Seed data: {brief["project_naam"]} ({brief["type"]})')
    seeded = seed_database(brief, db_path)
    update_brief(brief_path, brief, seeded)
    print('\n' + '='*50)
    print('✅ AXON SEED KLAAR')
    print(f'   Data: {", ".join(seeded) if seeded else "geen"}')
    print(f'   Volgende: setup_payment_integration.py (indien vereist)')
    print('='*50)

if __name__ == '__main__':
    main()
