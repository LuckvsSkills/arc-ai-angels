---
name: knowledge-curator
description: "Beheer en structureer de ARC AI Agents kennisbase via Memory Wiki."
metadata: { "openclaw": { "emoji": "🗂️" } }
---
# Knowledge Curator

Gebruik deze skill voor het beheren van de domein kennisbase.

## Kennisbase structuur

### Helix domain wiki paginas
helix/
├── overzicht.md          — domein beschrijving
├── agents/
│   ├── cortexia.md       — rol en capabilities
│   ├── forge.md
│   └── ...
├── workflows/
│   ├── website-fabriek.md
│   └── code-review.md
├── projecten/
│   └── [project-naam].md — per project docs
└── learnings.md          — domain learnings

## Wanneer wiki updaten
- Na elk voltooid project
- Na domein audit
- Na nieuwe workflow ontdekking
- Na tool of skill update

## Wiki pagina formaat
````markdown
# [Titel]

**Laatste update:** [datum]
**Eigenaar:** [agent]

## Samenvatting
Korte beschrijving

## Details
Uitgebreide informatie

## Gerelateerde paginas
- [link]
````

## Memory Wiki commando's
Gebruik de Memory Wiki plugin:
- Pagina aanmaken
- Pagina updaten
- Pagina zoeken
- Pagina verwijderen
