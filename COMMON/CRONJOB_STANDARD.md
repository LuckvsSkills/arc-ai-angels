# OpenClaw Cronjob Standard

## Delivery Configuration

**ALLE cronjobs moeten deze delivery config gebruiken:**

```json
"delivery": {
  "to": "openclaw-control-ui",
  "channel": "webchat",
  "mode": "announce"
}
```

**NOOIT:**
- `"channel": "last"` ❌ (no route)
- `"channel": "telegram"` ❌ (for Telegram input only)
- Custom channels zonder routing ❌

## Cronjob Template (Alle Agents)

```json
{
  "agentId": "AGENT_NAME",
  "name": "Job Name",
  "enabled": true,
  "schedule": {
    "kind": "cron",
    "expr": "0 7 * * 1",
    "tz": "Europe/Amsterdam"
  },
  "sessionTarget": "isolated",
  "wakeMode": "now",
  "payload": {
    "kind": "agentTurn",
    "message": "Your message here",
    "model": "google/gemini-2.5-flash"
  },
  "delivery": {
    "to": "openclaw-control-ui",
    "channel": "webchat",
    "mode": "announce"
  }
}
```

## Toekomstige Cronjobs

**Wanneer je NEW cronjobs toevoegt (via Telegram of CLI):**

1. Gebruik dit template
2. Check delivery config VOOR je opslaat
3. Test in OpenClaw dashboard

## Agents Cronjob Rules

- **NOVA**: Memory pipeline, heartbeats
- **FLUX**: Orchestration, automation, updates
- **FORGE**: GitHub search/analysis workflows
- **Others**: Custom workflows per agent

**ALL must use**: `"delivery": {"to": "openclaw-control-ui", "channel": "webchat", "mode": "announce"}`
