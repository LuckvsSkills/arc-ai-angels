# Upgrade Plan — TestKlantWebshop
**Scope:** REBUILD — Volledige herbouw met nieuwe stack + admin + AI agents
**Doorlooptijd:** 3-6 weken
**Kostenraming:** €5.000 – €15.000 + €500/mnd
**Aangemaakt:** 2026-06-12

---

## Gewenste verbeteringen
- AI chatbot
- order automatisering
- betere SEO
- leverancier emails

---

## Sentinel taakverdeling

### FORGE
**Taak:** Volledige herbouw frontend + backend
**Acties:** nieuwe React frontend, FastAPI backend, admin panel, content migratie
**Worker:** clone_template.py
**Status:** PENDING

### AXON
**Taak:** Nieuwe database + pipelines
**Acties:** database ontwerp, migratie bestaande data, payment integratie, webhooks
**Worker:** provision_database.py
**Status:** PENDING

### NERO
**Taak:** Volledige security audit
**Acties:** OWASP scan, penetration test, secrets check, hardening
**Worker:** scan_template_security.py
**Status:** PENDING

### VENTURA
**Taak:** Cloud deploy + domein migratie
**Acties:** VPS of Vercel setup, domein migratie, SSL, monitoring
**Worker:** provision_cloud_service.sh
**Status:** PENDING

### CLIO
**Taak:** Volledige documentatie + client handoff
**Acties:** README, API docs, deployment guide, gebruikershandleiding, AI agent docs
**Worker:** generate_client_handoff.py
**Status:** PENDING

---

## AI Agent integratie
Website agent wordt toegevoegd voor:
- order automatisering

Agent draait op OpenClaw, volledig autonoom.
Maandelijkse kosten: €300 – €500/mnd
