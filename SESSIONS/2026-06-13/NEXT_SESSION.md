# Next Session Agenda — 2026-06-13

## Prioriteit 1 — GitHub templates aanmaken
10 template repos op LuckvsSkills GitHub:
template-landing, portfolio, blog, saas, ecommerce,
directory, marketplace, dashboard, community, booking

Begin met template-landing als eerste test.

## Prioriteit 2 — Nova + Flux routing voor website verzoeken
- Nova WORKFLOW: website verzoek ontvangen via Telegram
- Flux WORKFLOW: routing naar Helix

## Prioriteit 3 — Live test
Verzoek via Nova → Flux → Cortexia → sentinels parallel → oplevering
Meten: bouwtijd, kosten, kwaliteit

## Prioriteit 4 — Wrapup timeout fixen
Alle wrapup cronjobs geven "Request was aborted" (390s timeout)
Fix: --timeout-seconds 60 op alle wrapup jobs
