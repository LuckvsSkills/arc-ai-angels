# B07 — Baseline Inventory

## Scope
Deze baseline inventariseert de huidige OpenClaw / Arc AI Angels runtime op het systeem van gebruiker `prime`.

Relevante paden:
- `~/arc_ai_angels`
- `~/.openclaw`
- `~/.openclaw-agent-07`

## 1. Runtime / Services

### Aanwezige unit files
- `openclaw-agent@.service`
- `openclaw-flux.service`
- `openclaw-nova.service`

### Actieve services
- `openclaw-flux.service` → active/running
- `openclaw-nova.service` → active/running

### Inactieve agent templates
- `openclaw-agent@agent-02` t/m `openclaw-agent@agent-50` → loaded, inactive/dead

### Process model
- `openclaw-gateway` draait als user `prime`
- agent runners starten via root-runner scripts
- executie wordt gedelegeerd met `sudo -u agent-nova` en `sudo -u agent-flux`
- stdout redaction draait via `python3 /usr/local/lib/openclaw/redact_stdout.py`

## 2. Accounts / Isolation

### Service-accounts aanwezig
- `agent-nova`
- `agent-flux`
- `agent-01` t/m `agent-50`

### Observatie
- accounts gebruiken `/usr/sbin/nologin`
- dit bevestigt basis user isolation per agent

## 3. Filesystem Surface

### Projectstructuur
`~/arc_ai_angels` bevat onder meer:
- agent workspaces
- backups
- docs
- gatekeeper
- shared communicatiepaden
- roadmap-gerelateerde bestanden

### OpenClaw home
`~/.openclaw` bevat onder meer:
- `.env`
- `.env.systemd`
- `openclaw.json`
- `exec-approvals.json`
- credentials / identity
- memory sqlite databases
- cron runs
- media inbound
- canvas files
- workspace-main git repo

### Extra agent path
`~/.openclaw-agent-07` bestaat, maar lijkt beperkt gevuld.

## 4. Sensitive Files / Secret Surface

### Gevoelige bestanden aanwezig
- `~/.openclaw/.env`
- `~/.openclaw/.env.systemd`
- `~/.openclaw/openclaw.json`
- `~/.openclaw/exec-approvals.json`
- `~/.openclaw/credentials/telegram-pairing.json`
- `~/.openclaw/identity/device-auth.json`
- `~/.openclaw/identity/device.json`

### Config-referenties tonen gebruik van:
- OpenAI
- Telegram
- Gateway
- Ollama
- sandbox / allowlist execution model

## 5. Permissions Review

### Goed
- `~/.openclaw` = `700`
- `~/.openclaw/secrets` = `700`
- `~/.openclaw/credentials` = `700`
- `.env`, `.env.systemd`, `openclaw.json`, `exec-approvals.json` = `600`
- pairing/device-auth/device files = `600`

### Aandachtspunten
- `~/.openclaw/identity` = `755`
- `~/.openclaw/memory` = `775`
- memory sqlite files = `644`
- `~/arc_ai_angels/gatekeeper/logs` = `755`
- `~/arc_ai_angels/gatekeeper/policies` = `755`
- `start_flux.sh` = `755`

## 6. Network / Exposure Surface

### Listening services
- `python3` luistert op `0.0.0.0:8080`
- `openclaw-gateway` luistert op `127.0.0.1:50506`
- `openclaw-gateway` luistert op `127.0.0.1:50509`

### Observatie
- OpenClaw gateway lijkt lokaal gebonden
- lokale webserver op `0.0.0.0:8080` is breder blootgesteld dan alleen loopback

## 7. Historical / Backup Surface

### Backups aanwezig
- tar.gz backups
- pre-merge backupstructuren
- oude agent/session data
- historische logs / session transcripts

### Observatie
Backups en sessielogs vergroten risico op:
- secret persistence
- oude configuraties met gevoelige waarden
- bredere forensic surface bij compromise

## 8. Key Findings

### Sterke punten
- basis agent-isolatie aanwezig
- actieve Nova/Flux gescheiden via dedicated users
- gateway lokaal gebonden
- kernconfigfiles grotendeels correct afgeschermd

### Belangrijkste risico’s
1. Secrets zijn aanwezig in plaintext env-bestanden
2. Memory databases zijn te ruim leesbaar
3. Identity directory is te ruim leesbaar
4. Logs / policy directories zijn breder leesbaar dan nodig
5. HTTP server op `0.0.0.0:8080` vergroot exposure
6. Backups en transcripts vergroten secret-retentie
7. Git workspace + backups vragen extra secret hygiene

## 9. Priority Recommendations

### Direct
- roteer exposed secrets die als gecompromitteerd moeten worden behandeld
- beperk rechten op memory / identity / logs
- controleer of `0.0.0.0:8080` echt nodig is

### Volgende security blocks
- B08 Monitoring / runtime safety
- B09 Incident response / kill switch
- B10 Secrets hardening
- B11 Internet / egress policy

## 10. Risk Summary
Huidige posture: **matig risico**
- geen directe aanwijzing dat gateway publiek internet-blootgesteld is
- wel duidelijke secret- en permission-risico’s
- hardening van storage, logs en exposure is nodig voor production readiness
