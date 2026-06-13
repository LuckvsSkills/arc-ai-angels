---
name: doc-writer
description: "Schrijf duidelijke technische documentatie voor ARC AI Agents projecten."
metadata: { "openclaw": { "emoji": "✍️" } }
---
# Doc Writer

Gebruik deze skill voor het schrijven van technische documentatie.

## Documentatie types

### README.md
Altijd aanmaken bij elk project:
```markdown
Clio heeft al diagram-maker — perfect voor documentatie.
CLIO ANALYSE:
HEEFT AL:
✅ diagram-maker   — diagrammen maken (SVG/Excalidraw)
✅ wiki-maintainer — kennisbase bijhouden
✅ healthcheck     — basis
✅ generate_readme.py — README generator (werkt!)

ONTBREEKT:
❌ doc-writer       — technische documentatie schrijven
❌ api-documenter   — API endpoints documenteren
❌ audit-checker    — domein audit uitvoeren
❌ knowledge-curator — kennisbase beheren en structureren
bash# Skill 1 — doc-writer
cat > /home/prime/arc_ai_angels/agents/clio/skills/doc-writer.md << 'EOF'
---
name: doc-writer
description: "Schrijf duidelijke technische documentatie voor ARC AI Agents projecten."
metadata: { "openclaw": { "emoji": "✍️" } }
---
# Doc Writer

Gebruik deze skill voor het schrijven van technische documentatie.

## Documentatie types

### README.md
Altijd aanmaken bij elk project:
````markdown
# Project Naam

Korte beschrijving wat het doet.

## 🌐 Live
[https://project.vercel.app](https://project.vercel.app)

## 🛠️ Tech Stack
- Frontend: React / HTML
- Backend: FastAPI / geen
- Database: SQLite / geen
- Hosting: Vercel

## 🚀 Lokaal starten
```bash
git clone [repo-url]
cd [project]
# installatie stappen
```

## 📁 Structuur
Beschrijving van de mapstructuur

## 🤖 Gebouwd door ARC AI Agents
````

### DEPLOYMENT.md
Bij elk project dat deployt:
- Deploy commando's
- Environment variables
- Rollback procedure

### API.md
Bij elk project met een backend:
- Alle endpoints
- Request/response voorbeelden
- Authenticatie uitleg

## Schrijfstijl regels
- Kort en helder — geen overbodige tekst
- Code voorbeelden voor technische zaken
- Nederlandse tekst voor ARC AI Agents docs
- Emoji voor visuele structuur
- Altijd een "Gebouwd door ARC AI Agents" sectie

## Output locatie
Altijd opslaan in:
`/home/prime/arc_ai_angels/agents/forge/projects/[project]/`
