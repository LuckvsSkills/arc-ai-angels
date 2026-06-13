#!/usr/bin/env python3
"""
provision_database.py — Axon worker
Provisioneert een database op basis van PROJECT_BRIEF.json
Gebruik: python3 provision_database.py /pad/naar/PROJECT_BRIEF.json
"""
import os, sys, json, sqlite3, subprocess
from datetime import datetime

DB_SCHEMAS = {
    'landing':   None,
    'portfolio': None,
    'blog': {
        'tables': ['posts', 'categories', 'users', 'settings'],
        'sql': """
CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, email TEXT UNIQUE, password TEXT, role TEXT DEFAULT 'admin', created_at DATETIME DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE IF NOT EXISTS categories (id INTEGER PRIMARY KEY, naam TEXT, slug TEXT UNIQUE);
CREATE TABLE IF NOT EXISTS posts (id INTEGER PRIMARY KEY, title TEXT, slug TEXT UNIQUE, content TEXT, category_id INTEGER, author_id INTEGER, status TEXT DEFAULT 'draft', created_at DATETIME DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY(category_id) REFERENCES categories(id), FOREIGN KEY(author_id) REFERENCES users(id));
CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT);
"""
    },
    'saas': {
        'tables': ['users', 'subscriptions', 'plans', 'invoices', 'settings'],
        'sql': """
CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, email TEXT UNIQUE, password TEXT, name TEXT, role TEXT DEFAULT 'user', stripe_customer_id TEXT, created_at DATETIME DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE IF NOT EXISTS plans (id INTEGER PRIMARY KEY, naam TEXT, prijs REAL, interval TEXT, stripe_price_id TEXT, features TEXT);
CREATE TABLE IF NOT EXISTS subscriptions (id INTEGER PRIMARY KEY, user_id INTEGER, plan_id INTEGER, status TEXT, stripe_sub_id TEXT, start_date DATETIME, end_date DATETIME, FOREIGN KEY(user_id) REFERENCES users(id), FOREIGN KEY(plan_id) REFERENCES plans(id));
CREATE TABLE IF NOT EXISTS invoices (id INTEGER PRIMARY KEY, user_id INTEGER, bedrag REAL, status TEXT, stripe_invoice_id TEXT, created_at DATETIME DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY(user_id) REFERENCES users(id));
CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT);
"""
    },
    'ecommerce': {
        'tables': ['users', 'products', 'categories', 'orders', 'order_items', 'cart'],
        'sql': """
CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, email TEXT UNIQUE, password TEXT, naam TEXT, adres TEXT, created_at DATETIME DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE IF NOT EXISTS categories (id INTEGER PRIMARY KEY, naam TEXT, slug TEXT UNIQUE, beschrijving TEXT);
CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY, naam TEXT, slug TEXT UNIQUE, beschrijving TEXT, prijs REAL, voorraad INTEGER DEFAULT 0, category_id INTEGER, afbeelding TEXT, actief INTEGER DEFAULT 1, created_at DATETIME DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY(category_id) REFERENCES categories(id));
CREATE TABLE IF NOT EXISTS orders (id INTEGER PRIMARY KEY, user_id INTEGER, status TEXT DEFAULT 'pending', totaal REAL, stripe_payment_id TEXT, created_at DATETIME DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY(user_id) REFERENCES users(id));
CREATE TABLE IF NOT EXISTS order_items (id INTEGER PRIMARY KEY, order_id INTEGER, product_id INTEGER, aantal INTEGER, prijs REAL, FOREIGN KEY(order_id) REFERENCES orders(id), FOREIGN KEY(product_id) REFERENCES products(id));
CREATE TABLE IF NOT EXISTS cart (id INTEGER PRIMARY KEY, user_id INTEGER, product_id INTEGER, aantal INTEGER, FOREIGN KEY(user_id) REFERENCES users(id), FOREIGN KEY(product_id) REFERENCES products(id));
"""
    },
    'directory': {
        'tables': ['users', 'listings', 'categories', 'reviews', 'settings'],
        'sql': """
CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, email TEXT UNIQUE, password TEXT, naam TEXT, rol TEXT DEFAULT 'user', created_at DATETIME DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE IF NOT EXISTS categories (id INTEGER PRIMARY KEY, naam TEXT, slug TEXT UNIQUE, icon TEXT);
CREATE TABLE IF NOT EXISTS listings (id INTEGER PRIMARY KEY, naam TEXT, slug TEXT UNIQUE, beschrijving TEXT, category_id INTEGER, user_id INTEGER, adres TEXT, telefoon TEXT, website TEXT, email TEXT, status TEXT DEFAULT 'pending', featured INTEGER DEFAULT 0, created_at DATETIME DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY(category_id) REFERENCES categories(id), FOREIGN KEY(user_id) REFERENCES users(id));
CREATE TABLE IF NOT EXISTS reviews (id INTEGER PRIMARY KEY, listing_id INTEGER, user_id INTEGER, rating INTEGER, tekst TEXT, created_at DATETIME DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY(listing_id) REFERENCES listings(id), FOREIGN KEY(user_id) REFERENCES users(id));
CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT);
"""
    },
    'marketplace': {
        'tables': ['users', 'products', 'orders', 'order_items', 'reviews', 'payouts'],
        'sql': """
CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, email TEXT UNIQUE, password TEXT, naam TEXT, rol TEXT DEFAULT 'buyer', stripe_account_id TEXT, created_at DATETIME DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY, naam TEXT, beschrijving TEXT, prijs REAL, seller_id INTEGER, voorraad INTEGER DEFAULT 0, status TEXT DEFAULT 'active', created_at DATETIME DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY(seller_id) REFERENCES users(id));
CREATE TABLE IF NOT EXISTS orders (id INTEGER PRIMARY KEY, buyer_id INTEGER, seller_id INTEGER, status TEXT DEFAULT 'pending', totaal REAL, commissie REAL, stripe_payment_id TEXT, created_at DATETIME DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE IF NOT EXISTS order_items (id INTEGER PRIMARY KEY, order_id INTEGER, product_id INTEGER, aantal INTEGER, prijs REAL);
CREATE TABLE IF NOT EXISTS reviews (id INTEGER PRIMARY KEY, product_id INTEGER, user_id INTEGER, rating INTEGER, tekst TEXT, created_at DATETIME DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE IF NOT EXISTS payouts (id INTEGER PRIMARY KEY, seller_id INTEGER, bedrag REAL, status TEXT, stripe_payout_id TEXT, created_at DATETIME DEFAULT CURRENT_TIMESTAMP);
"""
    },
    'dashboard': {
        'tables': ['users', 'data_sources', 'metrics', 'reports', 'settings'],
        'sql': """
CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, email TEXT UNIQUE, password TEXT, naam TEXT, rol TEXT DEFAULT 'viewer', created_at DATETIME DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE IF NOT EXISTS data_sources (id INTEGER PRIMARY KEY, naam TEXT, type TEXT, config TEXT, actief INTEGER DEFAULT 1);
CREATE TABLE IF NOT EXISTS metrics (id INTEGER PRIMARY KEY, source_id INTEGER, naam TEXT, waarde REAL, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY(source_id) REFERENCES data_sources(id));
CREATE TABLE IF NOT EXISTS reports (id INTEGER PRIMARY KEY, naam TEXT, query TEXT, schedule TEXT, created_at DATETIME DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT);
"""
    },
    'community': {
        'tables': ['users', 'categories', 'posts', 'comments', 'likes', 'members'],
        'sql': """
CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, email TEXT UNIQUE, password TEXT, naam TEXT, bio TEXT, avatar TEXT, rol TEXT DEFAULT 'member', created_at DATETIME DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE IF NOT EXISTS categories (id INTEGER PRIMARY KEY, naam TEXT, slug TEXT UNIQUE, beschrijving TEXT);
CREATE TABLE IF NOT EXISTS posts (id INTEGER PRIMARY KEY, title TEXT, content TEXT, category_id INTEGER, user_id INTEGER, views INTEGER DEFAULT 0, created_at DATETIME DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY(category_id) REFERENCES categories(id), FOREIGN KEY(user_id) REFERENCES users(id));
CREATE TABLE IF NOT EXISTS comments (id INTEGER PRIMARY KEY, post_id INTEGER, user_id INTEGER, content TEXT, created_at DATETIME DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY(post_id) REFERENCES posts(id), FOREIGN KEY(user_id) REFERENCES users(id));
CREATE TABLE IF NOT EXISTS likes (id INTEGER PRIMARY KEY, post_id INTEGER, user_id INTEGER, FOREIGN KEY(post_id) REFERENCES posts(id), FOREIGN KEY(user_id) REFERENCES users(id));
CREATE TABLE IF NOT EXISTS members (id INTEGER PRIMARY KEY, user_id INTEGER, plan TEXT DEFAULT 'free', stripe_sub_id TEXT, created_at DATETIME DEFAULT CURRENT_TIMESTAMP);
"""
    },
    'booking': {
        'tables': ['users', 'services', 'availability', 'bookings', 'payments'],
        'sql': """
CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, email TEXT UNIQUE, password TEXT, naam TEXT, rol TEXT DEFAULT 'client', created_at DATETIME DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE IF NOT EXISTS services (id INTEGER PRIMARY KEY, naam TEXT, beschrijving TEXT, duur_minuten INTEGER, prijs REAL, actief INTEGER DEFAULT 1);
CREATE TABLE IF NOT EXISTS availability (id INTEGER PRIMARY KEY, service_id INTEGER, dag TEXT, start_tijd TEXT, eind_tijd TEXT, FOREIGN KEY(service_id) REFERENCES services(id));
CREATE TABLE IF NOT EXISTS bookings (id INTEGER PRIMARY KEY, user_id INTEGER, service_id INTEGER, datum DATE, tijd TIME, status TEXT DEFAULT 'pending', notities TEXT, stripe_payment_id TEXT, created_at DATETIME DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY(user_id) REFERENCES users(id), FOREIGN KEY(service_id) REFERENCES services(id));
CREATE TABLE IF NOT EXISTS payments (id INTEGER PRIMARY KEY, booking_id INTEGER, bedrag REAL, status TEXT, stripe_payment_id TEXT, created_at DATETIME DEFAULT CURRENT_TIMESTAMP);
"""
    },
}

def log(msg):
    ts = datetime.now().strftime('%H:%M:%S')
    print(f'[{ts}] {msg}')

def load_brief(path):
    with open(path) as f:
        return json.load(f)

def provision_sqlite(brief, project_dir):
    ptype = brief['type']
    naam = brief['project_naam'].lower().replace(' ', '_')
    db_dir = f'{project_dir}/database'
    os.makedirs(db_dir, exist_ok=True)
    db_path = f'{db_dir}/{naam}.db'
    schema = DB_SCHEMAS.get(ptype)
    if not schema:
        log(f'ℹ️  Type {ptype} heeft geen database nodig')
        return None, []
    conn = sqlite3.connect(db_path)
    conn.executescript(schema['sql'])
    conn.commit()
    conn.close()
    log(f'✅ SQLite database aangemaakt: {db_path}')
    log(f'   Tabellen: {", ".join(schema["tables"])}')
    return db_path, schema['tables']

def save_db_config(brief, project_dir, db_path, tables):
    config = {
        'type': 'sqlite',
        'path': db_path,
        'tables': tables,
        'aangemaakt': datetime.now().isoformat()
    }
    config_path = f'{project_dir}/database/db_config.json'
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)
    return config_path

def update_brief(brief_path, brief, db_path, tables):
    brief['database'] = {
        'type': 'sqlite',
        'path': db_path,
        'tables': tables,
        'provisioned_at': datetime.now().isoformat()
    }
    brief['sentinels']['axon'] = 'DB_DONE'
    with open(brief_path, 'w') as f:
        json.dump(brief, f, indent=2, ensure_ascii=False)

def main():
    if len(sys.argv) < 2:
        print('Gebruik: python3 provision_database.py /pad/naar/PROJECT_BRIEF.json')
        sys.exit(1)
    brief_path = sys.argv[1]
    brief = load_brief(brief_path)
    project_dir = os.path.dirname(brief_path)
    log(f'🗄️  Database provisioning: {brief["project_naam"]} ({brief["type"]})')
    db_path, tables = provision_sqlite(brief, project_dir)
    if db_path:
        save_db_config(brief, project_dir, db_path, tables)
        update_brief(brief_path, brief, db_path, tables)
        print('\n' + '='*50)
        print('✅ AXON DATABASE KLAAR')
        print(f'   DB: {db_path}')
        print(f'   Tabellen: {", ".join(tables)}')
        print(f'   Volgende: seed_initial_data.py')
        print('='*50)
    else:
        print('ℹ️  Geen database vereist voor dit type')

if __name__ == '__main__':
    main()
