# ARC AI Angels — Project SOP
# Standaard Operationeel Proces (versie 1.0 — 15 juni 2026)

---

## KERNPRINCIPES

1. **Eén bron van waarheid**: PROJECT_STATUS.json per project — agents lezen EN schrijven hier
2. **Parallel waar mogelijk**: Agents wachten niet op elkaar tenzij er een echte dependency is
3. **Status-gedreven overdracht**: Niet "ik stuur jou een bericht", maar "ik zet mijn status op DONE, jij pikt het op bij je volgende HARNAS-run"
4. **Geen chat-afhankelijkheid**: Alles staat in bestanden — agents werken door ook als een andere agent niet beschikbaar is
5. **Lock-ready**: Elk project kan verborgen worden voor demo/presentatie-modus

---

## PROJECT TYPES

### TYPE A — KLANT-PROJECT (website build)
Pad: /home/prime/arc_ai_angels/projects/website_builds/[klant-slug]/
Trigger: Nova ontvangt klantverzoek

### TYPE B — INTERN PROJECT (systeem/development)
Pad: /home/prime/arc_ai_angels/projects/intern/[project-slug]/
Trigger: Fea of Flux initieert

---

## VERPLICHTE MAPSTRUCTUUR (beide types)
[project-pad]/

├── PROJECT_BRIEF.json      # Intake-output, NOOIT wijzigen na aanmaken

├── PROJECT_STATUS.json     # Machine-leesbare voortgang — agents schrijven hiernaar

├── tasks/

│   ├── [agent]_task.md    # Per betrokken agent 1 task-file

│   └── ...

├── code/                   # Gegenereerde code (klant-projecten)

├── docs/                   # Documentatie, handoff, QA-rapport

└── database/              # Database-config (indien van toepassing)

---

## PROJECT_STATUS.json — STRUCTUUR (bron van waarheid)

```json
{
  "project_id": "testwebshop",
  "naam": "TestWebshop",
  "type": "klant",
  "template_type": "ecommerce",
  "locked": false,
  "lock_hint": "",
  "status": "in_uitvoering",
  "fase": 2,
  "fase_naam": "Uitvoering",
  "aangemaakt": "2026-06-15T00:00:00",
  "laatste_update": "2026-06-15T08:00:00",
  "sla_deadline": "2026-06-16T00:00:00",
  "lead_agent": "cortexia",
  "agents": ["cortexia", "forge", "axon", "nero", "ventura", "clio"],
  "tasks": {
    "cortexia": {
      "status": "done",
      "gestart": "2026-06-15T01:00:00",
      "voltooid": "2026-06-15T01:30:00",
      "notitie": "Tasks aangemaakt, Forge als eerste geactiveerd"
    },
    "forge": {
      "status": "in_progress",
      "gestart": "2026-06-15T01:30:00",
      "voltooid": null,
      "notitie": "Template gekloond, personalisatie bezig"
    },
    "axon": {
      "status": "wacht_op",
      "wacht_op": ["forge"],
      "gestart": null,
      "voltooid": null,
      "notitie": ""
    },
    "nero": {
      "status": "parallel_met",
      "parallel_met": ["forge"],
      "gestart": "2026-06-15T01:30:00",
      "voltooid": null,
      "notitie": "Security-scan loopt parallel met Forge"
    },
    "ventura": {
      "status": "wacht_op",
      "wacht_op": ["forge", "axon"],
      "gestart": null,
      "voltooid": null,
      "notitie": ""
    },
    "clio": {
      "status": "wacht_op",
      "wacht_op": ["ventura"],
      "gestart": null,
      "voltooid": null,
      "notitie": ""
    }
  },
  "live_url": null,
  "notion_page_url": null,
  "notities": [],
  "fases_voltooid": [0, 1]
}
```

### Task statussen
- `open` — nog niet gestart, geen blokkade
- `in_progress` — agent is bezig
- `wacht_op` — wacht op andere agent(s) (lijst in `wacht_op`)
- `parallel_met` — loopt gelijktijdig met andere agent(s)
- `done` — voltooid
- `geblokkeerd` — onverwachte blokkade, escaleer naar Cortexia/Flux
- `overgeslagen` — niet van toepassing voor dit project

---

## PARALLELLE WERKWIJZE — HOE AGENTS SAMENWERKEN

### Principe: HARNAS-run als synchronisatie-moment

Bij elke HARNAS-run (06:00, 15:00, 00:00) doet elke agent:
1. Lees PROJECT_STATUS.json van alle actieve projecten
2. Check: zijn mijn `wacht_op` agents klaar (status: done)?
3. Zo ja → start mijn eigen task, zet status op `in_progress`
4. Voer task uit
5. Zet eigen status op `done`, schrijf `voltooid` timestamp
6. Schrijf notitie in task-entry

### Voorbeeld parallelle flow (website-build)
T+0 (Intake)     Nova     → PROJECT_STATUS.json aangemaakt (fase 0)

T+0              Flux     → Routeert naar Cortexia

T+1u             Cortexia → Tasks aangemaakt, status fase 1 → fase 2

→ Forge: open

→ Nero: parallel_met [forge]  ← start direct

→ Axon: wacht_op [forge]

→ Ventura: wacht_op [forge, axon]

→ Clio: wacht_op [ventura]
T+1u (HARNAS 06:00 run):

Forge  → ziet status: open → start → in_progress

Nero   → ziet parallel_met forge → start → in_progress (TEGELIJK met Forge)
T+5u (volgende check):

Forge  → klaar → done ✅

Nero   → klaar → done ✅

Axon   → wacht_op [forge] → forge is done → START → in_progress
T+7u:

Axon   → klaar → done ✅

Ventura→ wacht_op [forge ✅, axon ✅] → beide done → START → in_progress
T+9u:

Ventura → klaar → done ✅ (site live)

Clio    → wacht_op [ventura ✅] → START → docs schrijven → done ✅
T+10u: Nova informeert klant → fase 5 (live)

### Overdracht-mechaniek (geen chat nodig)

Een agent "overdraagt" niet actief — hij zet zijn status op `done`.
De volgende agent pikt dit op bij zijn eigen HARNAS-run.
Geen Telegram-berichten nodig voor interne overdracht.
Alleen escalaties en klant-communicatie gaan via Telegram/Nova.

---

## FASES (6 fases, beide project-types)

| Fase | Naam | Wie | SLA | Trigger |
|---|---|---|---|---|
| 0 | Intake | Nova | Direct | Klantverzoek |
| 1 | Setup | Flux → Cortexia | < 1u | PROJECT_BRIEF.json aangemaakt |
| 2 | Uitvoering | Forge/Axon/Nero parallel | < 8u | Tasks aangemaakt |
| 3 | QA | Nero/Forge/Clio | < 4u | Alle uitvoering-tasks done |
| 4 | Deploy + Overdracht | Ventura/Nova | < 2u | QA groen |
| 5 | Nazorg | Cortexia/Forge | Doorlopend | Site live |

---

## LOCK/PRIVATE SYSTEEM

Elk project heeft in PROJECT_STATUS.json:
```json
"locked": false,
"lock_hint": "Vraag Fea om de PIN"
```

- `locked: true` → project zichtbaar als grijs blok met 🔒 in MCC
- Inhoud niet zichtbaar zonder PIN
- PIN wordt per sessie ingevoerd (niet opgeslagen)
- Fea kan elk project locken/unlocken via MCC toggle
- Gebruik: demo-modus, privé klantprojecten, gevoelige interne projecten

---

## NOTION-INTEGRATIE (optioneel, per klant)

Notion wordt NIET gebruikt als interne backbone.
Intern draait alles op PROJECT_STATUS.json + TASKS.md.

Notion wordt WEL gebruikt als optionele klant-facing module:
- Na fase 4 (oplevering) maakt Clio optioneel een Notion-pagina aan
- Inhoud: projectdocumentatie, handleiding, edit-request instructies
- Klant ontvangt Notion-link via Nova (Telegram)
- Vereist: NOTION_TOKEN in .openclaw/.env

Worker: agents/clio/workers/create_notion_handoff.py (aan te maken)

---

## AGENT VERANTWOORDELIJKHEDEN PER FASE

### Nova
- Fase 0: Intake-wizard, PROJECT_BRIEF.json aanmaken, PROJECT_STATUS.json initialiseren
- Fase 4: Klant informeren (live URL, documentatie)
- Fase 5: Edit-requests ontvangen, routeren

### Flux
- Fase 1: Beoordelen PROJECT_BRIEF, routeren naar Cortexia

### Cortexia
- Fase 1: Tasks aanmaken per agent, PROJECT_STATUS.json updaten naar fase 2
- Fase 3: Eindvalidatie QA, PROJECT_STATUS.json updaten naar fase 4
- Fase 5: Edit-requests routeren naar juiste agent

### Forge
- Fase 2: Template klonen, personaliseren (clone_template.py)
- Fase 3: Responsive QA (375/768/1280px)

### Axon
- Fase 2: Backend/database koppelen (wacht op Forge)

### Nero
- Fase 2: Security-scan (parallel met Forge)
- Fase 3: Security-validatie

### Ventura
- Fase 4: Deploy naar Vercel, domein koppelen (wacht op Forge + Axon)

### Clio
- Fase 4: HANDOFF.md schrijven, optioneel Notion-pagina aanmaken
- Fase 5: Documentatie bijhouden bij wijzigingen

---

## PROJECT AANMAKEN — SCRIPT

Cortexia gebruikt workers/coordinate_project.py om een nieuw project te initialiseren:
1. Maak project-map aan
2. Kopieer PROJECT_BRIEF.json
3. Genereer PROJECT_STATUS.json (fase 0, alle tasks: open)
4. Genereer task-files per agent in tasks/
5. Update PROJECT_STATUS.json naar fase 1

---

## MCC MONITORING

De MCC ProjectsView leest dynamisch alle PROJECT_STATUS.json bestanden via:
GET /api/projects

Toont:
- Kolomweergave per fase (Kanban-stijl)
- Per kaart: naam, type, fase, SLA-status (groen/oranje/rood), lead agent
- Locked projecten: grijs blok met 🔒, inhoud verborgen
- Filter: Klant / Intern / Alle
- Klik op project → detailpagina met agent-tasks, documenten, tijdlijn


---

## PROJECT IDENTITEIT — WAT MAAKT IETS EEN PROJECT?

Een project bestaat officieel zodra het een PROJECT_STATUS.json heeft.
Zonder dat bestand is het geen project maar een losse map/notitie.

### Project-identiteit bestaat uit 4 lagen:

**Laag 1 — Identiteit (WAT is het?)**
Vastgelegd in PROJECT_BRIEF.json (onveranderlijk na aanmaken):
- project_id: unieke slug (bv. "testwebshop")
- naam: leesbare naam (bv. "TestWebshop")
- type: klant of intern
- template_type: welk type website (ecommerce, landing, etc.)
- beschrijving: 1-2 zinnen wat het project is
- klant: naam/contactinfo (klant-projecten)
- aangemaakt_door: Nova (klant) of Fea (intern)

**Laag 2 — Voortgang (WAAR staat het?)**
Vastgelegd in PROJECT_STATUS.json (dynamisch, agents schrijven hiernaar):
- fase: 0-5 (Intake/Setup/Uitvoering/QA/Deploy/Nazorg)
- status: open/in_uitvoering/geblokkeerd/live/afgesloten
- tasks: per agent open/in_progress/wacht_op/done
- sla_deadline: wanneer moet het klaar zijn
- laatste_update: wanneer is er voor het laatst iets veranderd
- live_url: eindresultaat

**Laag 3 — Documentatie (WAT is er gedaan?)**
Vastgelegd in docs/ map:
- HANDOFF.md: overdracht aan klant (fase 4)
- QA_RAPPORT.md: kwaliteitscheck (fase 3)
- SECURITY_RAPPORT.md: veiligheidscheck (fase 2/3)
- DEPLOYMENT.md: deploy-instructies (fase 4)
- NOTITIES.md: lopende aantekeningen agents

**Laag 4 — Code & Data (WAT is er gebouwd?)**
- code/: website-code
- database/: database-configuratie
- tasks/: per-agent taakbestanden

---

## VERVOLGSTAPPEN PER FASE — BESLISBOOM

### Hoe weet een agent wat hij moet doen?
START HARNAS-run

│

├── Lees alle PROJECT_STATUS.json bestanden

│

├── Voor elk project:

│   ├── Ben ik betrokken agent? (zit ik in "agents" lijst?)

│   │   └── Nee → skip dit project

│   │

│   ├── Wat is mijn task-status?

│   │   ├── "done" → skip, niets meer te doen

│   │   ├── "overgeslagen" → skip

│   │   ├── "geblokkeerd" → escaleer naar Cortexia/Flux

│   │   ├── "in_progress" → hervat taak, check of klaar

│   │   ├── "wacht_op" → check of alle wacht_op agents "done" zijn

│   │   │   ├── Niet allemaal done → skip, wacht op volgende run

│   │   │   └── Allemaal done → zet status "in_progress", start taak

│   │   └── "open" of "parallel_met" → start direct

│   │

│   └── Na voltooiing:

│       ├── Zet eigen status op "done"

│       ├── Schrijf timestamp + notitie in task-entry

│       ├── Update PROJECT_STATUS.json "laatste_update"

│       └── Check: zijn ALLE agents done? → update fase + status

│

└── Einde HARNAS-run

### Fase-overgang: wanneer gaat een project naar de volgende fase?
Fase 0 → 1: PROJECT_BRIEF.json aangemaakt + Nova heeft gerouteerd naar Flux

Fase 1 → 2: Cortexia heeft tasks aangemaakt (cortexia_task status: done)

Fase 2 → 3: Forge + Axon + Nero allemaal done

Fase 3 → 4: QA_RAPPORT.md aangemaakt + Forge/Nero/Clio QA-tasks done

Fase 4 → 5: live_url ingevuld in PROJECT_STATUS.json + klant geïnformeerd

Fase 5:     Doorlopend, project blijft "live" tot afgesloten

---

## PROJECT DOCUMENTATIE — WAT HOORT ALTIJD BIJ EEN PROJECT?

### Verplichte documenten (altijd aanwezig)
| Bestand | Aangemaakt door | Wanneer | Inhoud |
|---|---|---|---|
| PROJECT_BRIEF.json | Nova | Fase 0 | Intake-output, onveranderlijk |
| PROJECT_STATUS.json | Cortexia | Fase 1 | Machine-leesbare voortgang |
| tasks/[agent]_task.md | Cortexia | Fase 1 | Per-agent taakomschrijving |

### Optionele documenten (per project-type)
| Bestand | Aangemaakt door | Wanneer | Inhoud |
|---|---|---|---|
| docs/SECURITY_RAPPORT.md | Nero | Fase 2/3 | Security-bevindingen |
| docs/QA_RAPPORT.md | Forge/Nero | Fase 3 | Responsive + security QA |
| docs/HANDOFF.md | Clio | Fase 4 | Overdracht aan klant |
| docs/DEPLOYMENT.md | Ventura | Fase 4 | Deploy-instructies + URL |
| docs/NOTITIES.md | Alle agents | Doorlopend | Aantekeningen + beslissingen |

### Hoe navigeer je door een project? (voor Fea in MCC)
MCC Projects-tab

│

├── Zijbalk: lijst alle projecten (kaarten)

│   ├── Filter: Klant / Intern / Alle

│   ├── Sortering: fase / SLA-deadline / laatste update

│   └── Locked projecten: grijs blok met 🔒

│

└── Detailpagina (klik op project)

├── Header: naam, type, fase, SLA-status, lead agent

├── Voortgangsbalk: fase X/6

├── Agent-tasks: per agent status + tijdstip

├── Documenten: klikbare links naar docs/

├── Tijdlijn: wanneer is elke fase gestart/voltooid

└── Acties: Lock/Unlock, Notitie toevoegen, Fase forceren

---

## PROJECT AFSLUITEN

Een project wordt afgesloten wanneer:
- Fase 5 actief is (live)
- Klant heeft bevestigd (of 30 dagen na oplevering zonder klacht)
- Alle tasks done

Afsluiting:
1. Cortexia zet PROJECT_STATUS.json status op "afgesloten"
2. Map blijft bewaard in projects/website_builds/ (nooit verwijderen)
3. MCC toont project als "Afgesloten" (apart filter)
4. Project kan op elk moment heropend worden (nazorg/updates)
