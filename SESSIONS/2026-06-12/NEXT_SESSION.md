# Next Session Agenda — vervolg 2026-06-12

## Prioriteit 1 — Forge volledig klaarstomen
- WORKFLOW.md uitbreiden met WORKFLOW 5 (template klonen) en WORKFLOW 6 (admin panel)
- Skill: template-selector.md aanmaken
- Middag cronjob (12:00) toevoegen via OpenClaw

## Prioriteit 2 — Axon workers + workflow
- Worker: provision_database.py
- Worker: seed_initial_data.py
- Worker: setup_payment_integration.py
- WORKFLOW 4: Database provisioning
- Skill: db-provisioner.md

## Prioriteit 3 — Nero workers + workflow
- Worker: scan_template_security.py
- Worker: harden_deployment.sh
- Worker: check_secrets.sh
- WORKFLOW 4: Pre-deploy security gate
- Skill: pre-deploy-security-gate.md

## Prioriteit 4 — Ventura workers + workflow
- Worker: provision_cloud_service.sh
- Worker: setup_custom_domain.sh
- Worker: monitor_live_site.py
- WORKFLOW 4: Cloud deploy + domein
- Skill: cloud-deployer.md

## Prioriteit 5 — Clio workers + workflow
- Worker: generate_client_handoff.py
- Worker: generate_sop.py
- Worker: onboard_website_agent.py
- WORKFLOW 4: Client oplevering
- Skill: client-handoff-package.md

## Prioriteit 6 — Nova + Flux routing
- Nova WORKFLOW: website verzoek ontvangen via Telegram
- Flux WORKFLOW: routing naar Helix

## Doel
Alle Helix agents volledig klaar → dan templates bouwen in aparte chat → live test
