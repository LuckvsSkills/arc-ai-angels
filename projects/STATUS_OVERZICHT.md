# ARC AI Angels — Status Overzicht (bijgewerkt 15 juni 2026)

## ✅ KLAAR / AFGEVINKT

### Systeem & Infrastructuur
- [x] 33 agents gecertificeerd (20-22 .md bestanden elk, 33/33 PASS audit)
- [x] OpenClaw gateway actief (port 50506)
- [x] MCC frontend actief (Vite, port 3002, arc-vortex.nl)
- [x] MCC backend actief (FastAPI, port 8000)
- [x] Google OAuth login werkend
- [x] Cloudflare tunnel actief
- [x] GitHub backup (LuckvsSkills/arc-ai-angels, auto-push 4u)
- [x] SOUL.md + WORKFLOW.md herschreven voor alle 33 agents
- [x] CODEX 12 hoofdstukken + 17 Mermaid diagrammen
- [x] 16 OpenClaw plugins actief
- [x] ElevenLabs stemmen toegewezen aan alle 32 agents
- [x] PING/PONG health check systeem (30/31 agents OK)
- [x] MODEL_ROUTER.sh + PROJECT_COST_TRACKER.sh (budget <€150/maand)

### HARNAS Governance
- [x] Cronjobs geconsolideerd van 127 naar 71
- [x] Morning PREP 06:00 Amsterdam
- [x] Intelligent FLOW 15:00 Amsterdam (leads only)
- [x] Day WRAP-UP 00:00 Amsterdam
- [x] skill-workshop auto-approval geconfigureerd (approvalPolicy: auto)
- [x] OpenClaw node-service fix (vision/foto werkt)
- [x] Firecrawl/Exa/Perplexity beperkt (cost governance)

### MCC Tabs
- [x] Agents tab (Three.js 3D rendering, lazy loading, touch support)
- [x] Memory tab (7 endpoints, alle 32 agents)
- [x] Skills tab (approval flow, 50 pending skills, actieve skills per agent)
- [x] Tasks tab (TASKS.md per agent, filter op status/domain)
- [x] Services tab (start/stop/restart per service)
- [x] Domein tab (domain overview, agent detail panels, Command Flow)
- [x] Kosten tab (tool usage, budget monitoring)
- [x] OpenClaw tab (Overzicht, Agents, Cronjobs, Memory, Logs, Telegram)
- [x] ProjectsView bijgewerkt (P1: Template Library, 13/52, voortgangsbalk, documenten-links)

### Helix Domain
- [x] Cortexia — skills + workers (coordinate_project.py)
- [x] Nero — skills + workers (code_audit.py, cve_scan.sh, system_monitor.sh)
- [x] Forge — skills + workers (generate_website.py, build_api.py, deploy_website.sh)
- [x] Axon — skills + workers (build_pipeline.py, setup_database.py, run_pipeline.sh)
- [x] Ventura — skills + workers (deploy.sh, health_check.sh, infra_status.py)
- [x] Clio — skills + workers (generate_readme.py, generate_api_docs.py, domain_audit.py)
- [x] Nova + Flux WORKFLOW.md bijgewerkt (domain-routing alle 5 Omni Leads)

### Website Factory / Template Library
- [x] 13/13 basis-templates gebouwd en getest (GitHub repos: LuckvsSkills/template-[type])
- [x] clone_template.py gebouwd + timing-bug gefixed (retry-logica)
- [x] STIJL_VARS systeem (6 stijlen, theme.css injectie)
- [x] Responsive QA: dashboard (hamburger-toggle), bakkerij/marketplace/community/directory (scroll-fix)
- [x] WEBSITE_DELIVERY_PIPELINE.md (A-Z flow, 9 fases, clone-first strategie)
- [x] MASTERPLAN_52_TEMPLATES.md (52 referenties, backend-architectuur, flowcharts, 4-maanden planning)
- [x] TEMPLATE_LIBRARY_DRAAIBOEK.md (bouwvolgorde per maand, Forge als hoofduitvoerder)
- [x] FUNCTIONALITEIT_MODULES.md (12 modules)
- [x] EDIT_REQUEST_SYSTEM.md (element-ID systeem, bewerk-modus)
- [x] Nova INTAKE_WIZARD.md (stijl-mapping gefixed)
- [x] Forge workspace STATUS.json aangemaakt
- [x] 52-template library strategie bepaald (12 clone-types × 4 + hybride-retail × 4)
- [x] Benchmark-sites bepaald (39 links, 4 per type)

---


### Matrix Domain ✅
- [x] Saelia — coordinate_intelligence.py
- [x] Arix — run_research.py
- [x] Daxio — detect_signals.py
- [x] Enki — structure_knowledge.py
- [x] Sora — run_synthesis.py
- [x] Tharos — strategic_analysis.py

### Quantix Domain ✅
- [x] Lumeria — coordinate_data.py
- [x] Elora — run_data_research.py
- [x] Kresta — run_analytics.py
- [x] Luvia — run_forecast.py
- [x] Nura — manage_knowledge.py
- [x] Vondra — detect_data_signals.py

### Zenix Domain ✅
- [x] Fluentia — coordinate_language.py
- [x] Draven — write_copy.py
- [x] Orizon — run_strategy.py
- [x] Solis — write_story.py
- [x] Unia — run_editorial.py
- [x] Zena — run_localization.py

### Finix aanvulling ✅
- [x] Vector — run_finance_strategy.py (gemist in eerste pass)

### Alle 5 domains COMPLEET ✅
- [x] Helix (Cortexia + 5 sentinels) — skills + workers
- [x] Finix (Finoria + 5 sentinels incl. Vector) — skills + workers
- [x] Matrix (Saelia + 5 sentinels) — workers
- [x] Quantix (Lumeria + 5 sentinels) — workers
- [x] Zenix (Fluentia + 5 sentinels) — workers


### Project Management Systeem ✅
- [x] PROJECT_SOP.md (462 regels) — parallelle werkwijze, project-identiteit, beslisboom, lock-systeem, Notion-advies
- [x] init_project.py (Cortexia worker) — automatische project-initialisatie met dependency/parallel-logica
- [x] projects_routes.py (backend API) — GET/PATCH/lock/unlock/notities endpoints
- [x] ProjectsView.jsx — dynamisch, PIN-beveiligd lock/unlock, filter klant/intern, agent-tasks, SLA, voortgang
- [x] Template Library als officieel intern project in MCC (5/52 klaar, Forge in_progress)
- [x] Test-projecten gearchiveerd naar _archief/
- [x] mcc-backend crash-loop opgelost (stabiel draaiend via systemd)
- [x] PIN gewijzigd naar 5076 via systemd Environment variabele

## 🔴 OPEN / VOLGENDE CHAT

### Website Factory (volgende chat: Template Library bouwen)
- [ ] Maand 1: landing-V1 (notion) — eerste van 52 herbouwen
- [ ] Maand 1: overige 12 V1-templates herbouwen
- [ ] Backend-stack keuze (Supabase vs Pocketbase)
- [ ] Hybride-retail kalender-component (Kwik-Fit techniek)
- [ ] Maand 2-4: V2, V3, V4 templates

### Domains (volgende chat: domain-by-domain)
- [ ] Finix domain (Finoria + Kairo, Kenzo, Zion, Odis, Daxio) — nog niet aangeraakt
- [ ] Matrix domain (Saelia + sentinels) — nog niet aangeraakt
- [ ] Quantix domain (Lumeria + Elora, Kresta, Luvia, Nura, Vondra) — nog niet aangeraakt
- [ ] Zenix domain (Fluentia + Draven, Orizon, Solis, Unia, Zena) — nog niet aangeraakt

### Technische openstaande punten
- [ ] Sora's ping/pong status (nooit opgelost, mei 2026)
- [ ] OpenClaw update 2026.5.28
- [ ] 235 OpenClaw issues onderzoeken
- [ ] Heartbeat activering 31 agents
- [ ] mcc-backend.service crash-loop (port 8000 conflict, 58140 restarts) — niet urgent
- [ ] Sportsite Fea (oddsportal.com structuur) — apart project

### Roadmap (toekomst, niet nu)
- [ ] MCC Project-tab uitbreiden (Kanban, klant vs intern filter)
- [ ] 24-uur klant-MVP flow (na 52-template library klaar)
- [ ] Admin/CMS laag voor klanten
- [ ] Media/foto pipeline (Unsplash/Pexels API)
- [ ] Animatie-laag (AOS/GSAP)
