---
name: webhook-handler
description: "Ontvang en verwerk webhooks van GitHub, Vercel en andere services voor automation triggers."
metadata: { "openclaw": { "emoji": "🔗" } }
---
# Webhook Handler

Gebruik deze skill bij het ontvangen en verwerken van externe webhook triggers.

## Ondersteunde webhook bronnen

### GitHub webhooks
Events die Axon verwerkt:
- `push` — nieuwe code gepusht → trigger deploy pipeline
- `pull_request` — PR geopend → trigger code review bij Forge
- `issues` — nieuwe issue → toevoegen aan TASKS.md

### Vercel webhooks
- `deployment.succeeded` → Ventura notificeren
- `deployment.failed` → Cortexia alerteren

### Handmatige webhooks
Via MCC of externe systemen:
- `start-project` — nieuw project starten
- `run-pipeline` — specifieke pipeline uitvoeren

## Webhook verwerking workflow
1. Webhook ontvangen via Webhooks plugin
2. Parse payload — bepaal event type
3. Routeer naar juiste actie:
   - GitHub push → run_pipeline.sh deploy
   - GitHub issue → update TASKS.md
   - Vercel failure → alert Cortexia
4. Log in JOURNAL/

## Webhook payload formaten

### GitHub push event
```json

Axon heeft al taskflow en taskflow-inbox-triage — perfect voor automation.
AXON ANALYSE:
HEEFT AL:
✅ taskflow              — multi-step jobs orkestreren
✅ taskflow-inbox-triage — inbox verwerking en routing
✅ wiki-maintainer       — kennisbase
✅ healthcheck + tmux    — basis
✅ run_pipeline.sh       — basis pipeline runner

ONTBREEKT:
❌ webhook-handler    — webhooks ontvangen en verwerken
❌ pipeline-builder   — deployment pipelines bouwen
❌ database-designer  — database schemas ontwerpen
❌ scheduler-manager  — taken plannen en monitoren
bash# Skill 1 — webhook-handler
cat > /home/prime/arc_ai_angels/agents/axon/skills/webhook-handler.md << 'EOF'
---
name: webhook-handler
description: "Ontvang en verwerk webhooks van GitHub, Vercel en andere services voor automation triggers."
metadata: { "openclaw": { "emoji": "🔗" } }
---
# Webhook Handler

Gebruik deze skill bij het ontvangen en verwerken van externe webhook triggers.

## Ondersteunde webhook bronnen

### GitHub webhooks
Events die Axon verwerkt:
- `push` — nieuwe code gepusht → trigger deploy pipeline
- `pull_request` — PR geopend → trigger code review bij Forge
- `issues` — nieuwe issue → toevoegen aan TASKS.md

### Vercel webhooks
- `deployment.succeeded` → Ventura notificeren
- `deployment.failed` → Cortexia alerteren

### Handmatige webhooks
Via MCC of externe systemen:
- `start-project` — nieuw project starten
- `run-pipeline` — specifieke pipeline uitvoeren

## Webhook verwerking workflow
1. Webhook ontvangen via Webhooks plugin
2. Parse payload — bepaal event type
3. Routeer naar juiste actie:
   - GitHub push → run_pipeline.sh deploy
   - GitHub issue → update TASKS.md
   - Vercel failure → alert Cortexia
4. Log in JOURNAL/

## Webhook payload formaten

### GitHub push event
```json
{
  "event": "push",
  "repository": "repo-naam",
  "branch": "main",
  "commit": "abc123",
  "pusher": "LuckvsSkills"
}
```

### Vercel deployment
```json
{
  "event": "deployment.succeeded",
  "project": "project-naam",
  "url": "https://project.vercel.app",
  "environment": "production"
}
```

## Response formaat aan Cortexia
WEBHOOK VERWERKT
Event: [type]
Bron: [github/vercel/handmatig]
Actie: [wat gedaan]
Status: [OK/FOUT]
