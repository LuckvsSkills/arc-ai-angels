---
name: code-architect
description: "Neem architectuur beslissingen voor websites en applicaties op basis van requirements."
metadata: { "openclaw": { "emoji": "🏗️" } }
---
# Code Architect

Gebruik deze skill bij het ontwerpen van de technische architectuur voor een project.

## Beslissingsframework

### Frontend keuze
| Situatie | Keuze |
|----------|-------|
| Statische site, <5 paginas | HTML/CSS/JS |
| Dynamische data, interactie | React + Tailwind |
| Blog/marketing | HTML/CSS/JS |
| Web app met state | React + Tailwind |

### Backend keuze
| Situatie | Keuze |
|----------|-------|
| Geen data opslag nodig | Geen backend |
| REST API nodig | FastAPI (Python) |
| Real-time features | Node.js + WebSocket |
| Eenvoudige CRUD | FastAPI |

### Database keuze
| Situatie | Keuze |
|----------|-------|
| Geen persistentie nodig | Geen |
| Eenvoudige data | SQLite |
| Meerdere gebruikers | PostgreSQL |
| Documenten/flexibel | JSON files |

## Project structuur templates

### Statische website
Forge heeft al goede basis skills — browser-automation, node-debugger, python-debugpy zijn perfect voor een engineer.
FORGE ANALYSE:
HEEFT AL:
✅ browser-automation  — web automatisering
✅ node-inspect-debugger — Node.js debugging
✅ python-debugpy      — Python debugging  
✅ wiki-maintainer     — kennisbase
✅ healthcheck + tmux  — basis
✅ generate_website.py — website generator (werkt!)
✅ deploy_website.sh   — Vercel deploy (werkt!)

ONTBREEKT:
❌ code-architect      — architectuur beslissingen nemen
❌ git-workflow        — GitHub workflow voor ARC AI Agents
❌ api-builder         — REST API bouwen met FastAPI
❌ frontend-builder    — React/HTML component bouwen
bash# Skill 1 — code-architect
cat > /home/prime/arc_ai_angels/agents/forge/skills/code-architect.md << 'EOF'
---
name: code-architect
description: "Neem architectuur beslissingen voor websites en applicaties op basis van requirements."
metadata: { "openclaw": { "emoji": "🏗️" } }
---
# Code Architect

Gebruik deze skill bij het ontwerpen van de technische architectuur voor een project.

## Beslissingsframework

### Frontend keuze
| Situatie | Keuze |
|----------|-------|
| Statische site, <5 paginas | HTML/CSS/JS |
| Dynamische data, interactie | React + Tailwind |
| Blog/marketing | HTML/CSS/JS |
| Web app met state | React + Tailwind |

### Backend keuze
| Situatie | Keuze |
|----------|-------|
| Geen data opslag nodig | Geen backend |
| REST API nodig | FastAPI (Python) |
| Real-time features | Node.js + WebSocket |
| Eenvoudige CRUD | FastAPI |

### Database keuze
| Situatie | Keuze |
|----------|-------|
| Geen persistentie nodig | Geen |
| Eenvoudige data | SQLite |
| Meerdere gebruikers | PostgreSQL |
| Documenten/flexibel | JSON files |

## Project structuur templates

### Statische website
project/
├── index.html
├── style.css
├── app.js
└── README.md

### React + FastAPI
project/
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── components/
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
├── backend/
│   ├── main.py
│   ├── routes/
│   └── requirements.txt
└── README.md

## Code kwaliteit standaarden
- Functions max 20 regels
- Comments op complexe logica
- Environment variables voor alle secrets
- Error handling op alle API calls
- Responsive design verplicht
