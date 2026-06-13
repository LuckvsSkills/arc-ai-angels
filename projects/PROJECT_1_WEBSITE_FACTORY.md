# PROJECT 5 — WEBSITE FACTORY
## Status: IN ONTWIKKELING
## Eigenaar: Supreme Fea — ARC AI Agents
## Lead Agent: Cortexia (Helix/Tech domein)
## Aangemaakt: 2026-06-12

---

## Wat bouwen wij

Een volledig autonome website fabriek waarbij ARC AI Agents agents op verzoek professionele websites bouwen, deployen en optioneel beheren via een gebonden AI agent. De fabriek werkt vanuit GitHub templates, een intake formulier en een geautomatiseerde agent pipeline.

---

## Waarom

Websites zijn het meest concrete digitale product dat wij kunnen leveren. Met onze agent infrastructuur kunnen wij websites sneller, goedkoper en consistenter bouwen dan een menselijk team. Dit wordt onze eerste externe revenue stream met meetbare output per dag.

---

## Wat levert het op

| Tier | Type | Verkoopprijs | AI kosten | Marge |
|------|------|-------------|-----------|-------|
| 1 — Basic | Landing/Portfolio/Blog | €500–2.000 | ~€0,50 | 99% |
| 2 — Pro | SaaS/Ecommerce/Directory | €3.000–8.000 | ~€5–15 | 98% |
| 3 — AI-powered | Elk type + gebonden agent | €10.000 + €500/mnd | ~€20–50 | 95% |

Doel: 3 websites per dag × gemiddeld €2.000 = €6.000/dag potentieel

---

## De 10 website types (GitHub templates)

| # | Template repo | Type | Stack | Admin | Agent |
|---|--------------|------|-------|-------|-------|
| 1 | template-landing | Landing page | HTML/CSS/JS | Nee | Nee |
| 2 | template-portfolio | Portfolio | HTML/CSS/JS | Nee | Nee |
| 3 | template-blog | Blog/Content | Next.js+Markdown | Basis | Optioneel |
| 4 | template-saas | SaaS platform | React+FastAPI+PG | Volledig | Ja |
| 5 | template-ecommerce | E-commerce | React+FastAPI+Stripe | Volledig | Ja |
| 6 | template-directory | Directory | React+FastAPI+PG | Volledig | Ja |
| 7 | template-marketplace | Marketplace | React+FastAPI+Stripe Connect | Volledig | Ja |
| 8 | template-dashboard | Dashboard/Tool | React+FastAPI+WS | Volledig | Ja |
| 9 | template-community | Community/Forum | React+FastAPI+WS | Volledig | Ja |
| 10 | template-booking | Booking/Reservering | React+FastAPI+Stripe | Volledig | Ja |

---

## Elke template bevat

- `/frontend` — volledige UI code
- `/backend` — FastAPI backend met alle endpoints
- `/admin` — admin panel (orders, analytics, klanten, content, financieel)
- `/database` — schema migrations + seed data
- `/agent` — OpenClaw agent config voor website beheer
- `/deploy` — Vercel config + VPS setup scripts
- `README.md` — installatie + gebruik
- `PRICING.md` — kosten en verkoopprijs

---

## De agent pipeline (intake tot oplevering)
Klant intake formulier
↓
Nova ontvangt verzoek
↓
Flux routeert naar Helix
↓
Cortexia analyseert + selecteert template
↓
Parallel spawn:
Forge    → clone template + personaliseren + code
Axon     → database + pipeline opzetten
Nero     → security audit
Ventura  → deploy naar Vercel/VPS
Clio     → documentatie + oplevering
↓
Cortexia valideert + rapporteert aan Flux
↓
Nova rapporteert aan Supreme Fea via Telegram
↓
Live website opgeleverd

---

## Fasering

### Fase 1 — GitHub Templates (week 1)
- 10 template repos aanmaken op LuckvsSkills GitHub
- Elke template volledig uitgewerkt met frontend+backend+admin+DB+agent config
- Templates gemarkeerd als GitHub Template repo

### Fase 2 — Prijslijst vastleggen (week 1)
- PRICING.md per template
- Kosten berekening per type
- Verkoopprijzen vastgesteld

### Fase 3 — Helix agents configureren (week 1-2)
- Cortexia: WORKFLOW uitbreiden met website fabriek orchestratie
- Forge: 3 nieuwe workers + template-selector skill
- Axon: 3 nieuwe workers + db-provisioner skill
- Nero: 3 nieuwe workers + pre-deploy-audit skill
- Ventura: 3 nieuwe workers + cloud-deployer skill
- Clio: 3 nieuwe workers + client-handoff skill

### Fase 4 — Intake formulier (week 2)
- JSON intake formulier structuur vastleggen
- Nova WORKFLOW uitbreiden voor website verzoeken
- Flux routing naar Helix toevoegen

### Fase 5 — Test run (week 2)
- Eerste website bouwen via live agent pipeline
- Nova ontvangt verzoek via Telegram
- Meten: bouwtijd, kosten, kwaliteit
- Debuggen en optimaliseren

### Fase 6 — Productie (week 3+)
- Fabriek live
- Meten: websites per dag, kosten per site, marge
- Optimaliseren op basis van data

---

## Meten

| Metric | Doel | Hoe meten |
|--------|------|-----------|
| Bouwtijd per site | < 2 uur | TASKS.md timestamps |
| AI kosten per site | < €15 | cost_tracker.py |
| Kwaliteitsscore | > 90/100 | Nero security + Clio audit |
| Sites per dag | 3+ | PROJECT_5 dashboard |
| Marge per site | > 95% | Finoria rapportage |

---

## Technische vereisten per agent

### Cortexia (orchestrator)
- WORKFLOW 5: Website Fabriek Orchestratie
- Skill: project-orchestrator
- Intake formulier verwerken
- Template selectie logica
- Parallel LLM Task spawning
- QA validatie voor oplevering

### Forge (bouwen)
- Worker: clone_template.py
- Worker: personalize_site.py
- Worker: build_admin_panel.py
- Skill: template-selector
- Skill: mcc-component-builder

### Axon (data + pipeline)
- Worker: provision_database.py
- Worker: seed_initial_data.py
- Worker: setup_payment_integration.py
- Skill: db-provisioner
- Skill: stripe-integrator

### Nero (security)
- Worker: scan_template_security.py
- Worker: harden_deployment.sh
- Worker: check_secrets.sh
- Skill: pre-deploy-security-gate

### Ventura (deploy)
- Worker: provision_cloud_service.sh
- Worker: setup_custom_domain.sh
- Worker: monitor_live_site.py
- Skill: cloud-deployer
- Skill: domain-manager

### Clio (oplevering)
- Worker: generate_client_handoff.py
- Worker: generate_sop.py
- Worker: onboard_website_agent.py
- Skill: client-handoff-package

---

## Status per fase

| Fase | Status | Verantwoordelijke |
|------|--------|-----------------|
| Fase 1 — Templates | 🔴 OPEN | Forge |
| Fase 2 — Prijslijst | 🔴 OPEN | Finoria |
| Fase 3 — Agent config | 🟡 BEZIG | Cortexia |
| Fase 4 — Intake formulier | 🔴 OPEN | Nova + Flux |
| Fase 5 — Test run | 🔴 OPEN | Cortexia |
| Fase 6 — Productie | 🔴 OPEN | Alle Helix agents |

---

## Diagrammen

Zie `/home/prime/arc_ai_angels/projects/PROJECT_5_DIAGRAMS/` voor:
- website_types_matrix.svg
- website_fabriek_flow.svg
- helix_domain_overzicht.svg
- agent_pipeline_flow.svg
- pricing_overview.svg

---

## Gerelateerde bestanden

- Agents: `/home/prime/arc_ai_angels/agents/cortexia/WORKFLOW.md`
- Templates: `https://github.com/LuckvsSkills/template-*`
- Kosten DB: `/home/prime/arc_ai_angels/LITELLM/costs.db`
- HARNAS jobs: `/home/prime/arc_ai_angels/HARNAS/`
