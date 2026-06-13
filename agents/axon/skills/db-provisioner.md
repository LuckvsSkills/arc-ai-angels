---
name: db-provisioner
description: "Provisioneer een database op basis van website type. Kiest automatisch het juiste schema (SQLite/PostgreSQL), maakt tabellen aan en voert seed data in. Gebruik bij elke website build die een database vereist."
metadata: { "openclaw": { "emoji": "🗄️" } }
---
# DB Provisioner

Gebruik deze skill voor database setup bij website builds.

## Database per website type

| Type | DB | Tabellen |
|------|----|---------|
| landing | Geen | - |
| portfolio | Geen | - |
| blog | SQLite | users, posts, categories, settings |
| saas | SQLite/PG | users, plans, subscriptions, invoices |
| ecommerce | SQLite/PG | users, products, categories, orders, cart |
| directory | SQLite/PG | users, listings, categories, reviews |
| marketplace | SQLite/PG | users, products, orders, payouts |
| dashboard | SQLite | users, data_sources, metrics, reports |
| community | SQLite/PG | users, posts, comments, likes, members |
| booking | SQLite | users, services, availability, bookings |

## Uitvoering

```bash
python3 /home/prime/arc_ai_angels/agents/axon/workers/provision_database.py /pad/PROJECT_BRIEF.json
python3 /home/prime/arc_ai_angels/agents/axon/workers/seed_initial_data.py /pad/PROJECT_BRIEF.json
python3 /home/prime/arc_ai_angels/agents/axon/workers/setup_payment_integration.py /pad/PROJECT_BRIEF.json
```

## Volgorde
1. provision_database.py — schema aanmaken
2. seed_initial_data.py — basis data invoeren
3. setup_payment_integration.py — Stripe koppelen (indien vereist)
