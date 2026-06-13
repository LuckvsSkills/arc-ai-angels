---
name: template-selector
description: "Selecteer het juiste GitHub template op basis van website type en requirements. Gebruik bij elk website build verzoek om de juiste template te kiezen voor clone_template.py."
metadata: { "openclaw": { "emoji": "🎯" } }
---
# Template Selector

Gebruik deze skill om het juiste template te kiezen bij een website build opdracht.

## Template keuze matrix

| Type | Template | Stack | Wanneer kiezen |
|------|----------|-------|----------------|
| landing | template-landing | HTML/CSS/JS | 1 pagina, conversie, product lancering |
| portfolio | template-portfolio | HTML/CSS/JS | Werk tonen, personal brand, freelancer |
| blog | template-blog | Next.js+Markdown | Artikelen, SEO, thought leadership |
| saas | template-saas | React+FastAPI+PG | Abonnement model, recurring revenue |
| ecommerce | template-ecommerce | React+FastAPI+Stripe | Producten verkopen, webshop |
| directory | template-directory | React+FastAPI+PG | Listings, zoeken, vermeldingen |
| marketplace | template-marketplace | React+FastAPI+Stripe | Buyers + sellers, commissie model |
| dashboard | template-dashboard | React+FastAPI+WS | Data visualisatie, analytics, intern |
| community | template-community | React+FastAPI+WS | Forum, netwerk, membership |
| booking | template-booking | React+FastAPI+Stripe | Reserveringen, kalender, afspraken |

## Beslisregels

1. Heeft de site betalingen nodig? → ecommerce / marketplace / booking / saas
2. Is het primair informeren? → landing / portfolio / blog
3. Zijn er gebruikersaccounts? → saas / community / marketplace
4. Is het data-gedreven? → dashboard / directory
5. Is het een community? → community
6. Is het 1 pagina? → landing

## Uitvoering na keuze

```bash
python3 /home/prime/arc_ai_angels/agents/forge/workers/clone_template.py /pad/naar/PROJECT_BRIEF.json
python3 /home/prime/arc_ai_angels/agents/forge/workers/personalize_site.py /pad/naar/PROJECT_BRIEF.json
python3 /home/prime/arc_ai_angels/agents/forge/workers/build_admin_panel.py /pad/naar/PROJECT_BRIEF.json
```

## GitHub template repos
Alle templates staan op: https://github.com/LuckvsSkills/template-{type}
