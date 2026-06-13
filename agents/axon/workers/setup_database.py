#!/usr/bin/env python3
"""
setup_database.py — Axon worker
Maakt een SQLite database aan op basis van project specs
Gebruik: python3 setup_database.py "project-naam"
"""
import os, sys, json, sqlite3

def setup_database(project_name):
    project_dir = f'/home/prime/arc_ai_angels/agents/forge/projects/{project_name}'
    specs_file = f'{project_dir}/specs.json'
    
    if not os.path.exists(specs_file):
        print(f'❌ Geen specs.json gevonden voor {project_name}')
        sys.exit(1)
    
    with open(specs_file) as f:
        specs = json.load(f)
    
    if specs.get('database') == 'none':
        print(f'ℹ️  Geen database nodig voor {project_name}')
        return
    
    db_dir = f'{project_dir}/backend'
    os.makedirs(db_dir, exist_ok=True)
    db_path = f'{db_dir}/database.db'
    
    conn = sqlite3.connect(db_path)
    
    # Basis tabellen op basis van features
    features = specs.get('features', [])
    features_str = ' '.join(features).lower()
    
    tables_created = []
    
    # Users tabel — altijd aanmaken bij auth
    if specs.get('auth') != 'none' or 'login' in features_str or 'gebruiker' in features_str:
        conn.execute('''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            name TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        tables_created.append('users')
    
    # Products — bij webshop
    if 'product' in features_str or 'winkel' in features_str or 'shop' in features_str:
        conn.execute('''CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            price REAL NOT NULL,
            stock INTEGER DEFAULT 0,
            image_url TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        tables_created.append('products')
    
    # Orders
    if 'order' in features_str or 'bestelling' in features_str or 'checkout' in features_str:
        conn.execute('''CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            total REAL NOT NULL,
            status TEXT DEFAULT "pending",
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        tables_created.append('orders')
    
    # Content/posts
    if 'blog' in features_str or 'artikel' in features_str or 'post' in features_str:
        conn.execute('''CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT,
            author_id INTEGER,
            published BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        tables_created.append('posts')
    
    conn.commit()
    conn.close()
    
    print(f'✅ Database aangemaakt: {db_path}')
    print(f'Tabellen: {", ".join(tables_created)}')
    return db_path

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Gebruik: python3 setup_database.py "project-naam"')
        sys.exit(1)
    setup_database(sys.argv[1])
