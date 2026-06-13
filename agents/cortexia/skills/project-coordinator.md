---
name: project-coordinator
description: "Vertaal klant requirements naar technische specs en coördineer het Helix domein voor projectuitvoering."
metadata: { "openclaw": { "emoji": "🎯" } }
---
# Project Coordinator

Gebruik deze skill wanneer je een verzoek van Flux ontvangt en dit moet omzetten naar een uitvoerbaar project voor het Helix domein.

## Stap 1 — Requirements analyseren
Stel jezelf deze vragen:
- Wat wil de klant precies bereiken?
- Welke features zijn must-have vs nice-to-have?
- Wat is de deadline/urgentie?
- Zijn er technische constraints?

## Stap 2 — Tech Stack bepalen
Kies op basis van requirements:

| Type | Simpel | Complex |
|------|--------|---------|
| Frontend | HTML/CSS/JS | React + Tailwind |
| Backend | Geen / Static | FastAPI / Node.js |
| Database | Geen / JSON | SQLite / PostgreSQL |
| Auth | Geen | JWT / OAuth |
| Hosting | Vercel static | Vercel + backend |

## Stap 3 — Specs JSON opstellen
```json
{
  "project_name": "naam-zonder-spaties",
  "description": "wat het doet",
  "frontend": "html|react",
  "backend": "none|fastapi|nodejs",
  "database": "none|sqlite|postgresql",
  "auth": "none|jwt",
  "features": ["feature1", "feature2"],
  "hosting": "vercel",
  "assigned_to": {
    "forge": "frontend + backend code",
    "axon": "database + pipeline",
    "ventura": "deploy",
    "nero": "security audit",
    "clio": "documentatie"
  }
}
```

## Stap 4 — Taakverdeling
- Spawn Forge + Axon parallel via LLM Task
- Nero wordt ingeschakeld NA code gereed
- Ventura deployt NA Nero groen licht
- Clio documenteert NA succesvolle deploy

## Stap 5 — Voortgang bewaken
- Houd TASKS.md bij met status per sentinel
- Escaleer blokkades direct
- Rapporteer voltooiing aan Flux met live URL
