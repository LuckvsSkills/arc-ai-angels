---
name: project-orchestrator
description: "Orkestreer een volledig website bouwproject van intake tot oplevering. Verwerkt intake JSON, selecteert template, spawnt sentinels parallel en bewaakt voortgang."
metadata: { "openclaw": { "emoji": "🎯" } }
---
# Project Orchestrator

Gebruik deze skill wanneer Cortexia een website project moet opstarten en coördineren.

## Intake formaat
```json
{
  "naam": "ProjectNaam",
  "type": "landing|portfolio|blog|saas|ecommerce|directory|marketplace|dashboard|community|booking",
  "beschrijving": "Wat doet de website",
  "features": ["feature1", "feature2"],
  "kleurenschema": "optioneel",
  "domein": "optioneel"
}
```

## Template selectie logica
- 1 pagina, conversie → landing
- Werk tonen → portfolio
- Artikelen, SEO → blog
- Abonnement model → saas
- Producten verkopen → ecommerce
- Listings, zoeken → directory
- Buyers + sellers → marketplace
- Data visualisatie, intern → dashboard
- Forum, netwerk → community
- Reserveringen, kalender → booking

## Uitvoering
```bash
python3 /home/prime/arc_ai_angels/agents/cortexia/workers/orchestrate_website_project.py /pad/naar/intake.json
```

## Sentinel volgorde
1. PARALLEL: Forge (code) + Axon (database)
2. SEQUENTIEEL: Nero (security) → Ventura (deploy) → Clio (docs)

## Rapportage aan Flux
Na oplevering altijd rapporteren:
- Live URL
- Admin URL
- Bouwtijd
- AI kosten
- Security status
