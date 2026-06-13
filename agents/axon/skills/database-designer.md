---
name: database-designer
description: "Ontwerp database schemas voor ARC AI Agents projecten op basis van features."
metadata: { "openclaw": { "emoji": "🗄️" } }
---
# Database Designer

Gebruik deze skill voor het ontwerpen van database structuren.

## Schema ontwerp process
1. Lees project specs (features lijst)
2. Identificeer entiteiten (wat moet opgeslagen worden)
3. Definieer relaties (één-op-één, één-op-veel, veel-op-veel)
4. Maak schema met SQLite of PostgreSQL syntax

## Veelgebruikte schemas

### Users tabel
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    name TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Products tabel
```sql
CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    price REAL NOT NULL,
    stock INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Orders tabel
```sql
CREATE TABLE orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER REFERENCES users(id),
    total REAL NOT NULL,
    status TEXT DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## SQLite setup script template
```python
import sqlite3

def init_db(db_path):
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON")
    # Schema hier
    conn.commit()
    conn.close()
    print(f"Database aangemaakt: {db_path}")
```

## Output formaat aan Cortexia
DATABASE SCHEMA — [project]
Tabellen: [lijst]
Relaties: [beschrijving]
Bestand: [pad naar .sql file]
