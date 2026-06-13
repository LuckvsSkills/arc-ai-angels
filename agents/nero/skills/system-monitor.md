---
name: system-monitor
description: "Bewaakt het ARC AI Agents systeem op verdachte activiteit, config wijzigingen en onverwacht gedrag."
metadata: { "openclaw": { "emoji": "🛡️" } }
---
# System Monitor

Gebruik deze skill voor proactieve systeem bewaking.

## Wat te bewaken

### 1. Config bestanden
Controleer dagelijks op onverwachte wijzigingen:
- `~/.openclaw/openclaw.json` — agent tool toewijzingen
- `~/.openclaw/.env` — API keys en secrets
- `~/.openclaw/cron/jobs.json` — cronjob definities

### 2. Service status
Check dagelijks:
- OpenClaw Gateway poort 50506
- LiteLLM poort 4000
- MCC Backend poort 8000
- Cloudflare tunnel

### 3. Abnormaal gedrag signalen
Let op:
- Agent die tools aanroept buiten zijn allow lijst
- Onverwacht hoog token gebruik
- Cronjobs die plotseling falen
- Nieuwe processen die niet horen te draaien

### 4. API key bewaking
- Check of keys nog geldig zijn
- Log wanneer keys voor het laatst gebruikt zijn
- Alert bij onverwacht gebruik

## Monitoring workflow (dagelijks)
1. Check service status → rapporteer aan Cortexia
2. Vergelijk openclaw.json hash met gisteren → alert bij wijziging
3. Check cron job error rate → alert bij >20% fouten
4. Check disk space → alert bij <10% vrij

## Alert formaten

### Routine check OK
🛡️ NERO SYSTEEM CHECK — [datum]
Alle services: ✅
Config ongewijzigd: ✅
Cron jobs: ✅ ([n]/[n] succesvol)
Disk: ✅ ([n]% vrij)
STATUS: VEILIG

### Alert bij afwijking
⚠️ NERO SYSTEEM ALERT
Wat: [beschrijving]
Wanneer: [tijd]
Impact: [hoog/medium/laag]
Actie: [wat moet er gebeuren]
