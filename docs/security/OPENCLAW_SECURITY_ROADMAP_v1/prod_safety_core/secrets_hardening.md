# B10 — Secrets Hardening

## Scope
Deze stap brengt de secret surface in kaart, hardent permissies op gevoelige paden en definieert een rotatieprioriteit voor credentials en API keys.

## 1. Bevestigde Secret Locations

### Primaire secret-bestanden
- `~/.openclaw/.env`
- `~/.openclaw/.env.systemd`
- `~/.openclaw/credentials/telegram-pairing.json`
- `~/.openclaw/identity/device-auth.json`

### Config met env-references
- `~/.openclaw/openclaw.json`

### Config/backups met secret-referenties
- `~/.openclaw/openclaw.json.bak`
- `~/.openclaw/openclaw.json.bak.3`
- `~/.openclaw/openclaw.json.bak.20260302-124650`
- `~/.openclaw/openclaw.json.backup.fix`

## 2. Confirmed Secret Types
De omgeving gebruikt of refereert aan:
- `OPENAI_API_KEY`
- `TELEGRAM_BOT_TOKEN`
- `OPENCLAW_GATEWAY_TOKEN`
- `MOONSHOT_API_KEY`
- `GEMINI_API_KEY`

Daarnaast bestaan:
- Telegram pairing credentials
- Device auth credentials

## 3. Permission Hardening Applied

### Aangepast
- `~/.openclaw/identity` → `700`
- `~/.openclaw/memory` → `700`
- `~/.openclaw/memory/*.sqlite` → `600`
- `~/arc_ai_angels/gatekeeper/logs` → `700`
- `~/arc_ai_angels/gatekeeper/policies` → `700`

### Effect
- memory data is niet meer leesbaar voor andere lokale users
- identity / device-auth surface is afgeschermd
- gatekeeper logs/policies zijn niet meer breed leesbaar

## 4. Risk Assessment

### Belangrijkste risico’s
1. Secrets staan in plaintext env-bestanden
2. Gevoelige waarden zijn tijdens beheer zichtbaar geweest in terminal/chat
3. Pairing/device-auth bestanden bestaan lokaal
4. Config-backups vergroten secret-retentie
5. Historische logs/sessions/backups kunnen oude auth-context bevatten

### Security posture
Secrets moeten worden behandeld als:
- lokaal aanwezig
- bruikbaar voor runtime
- deels mogelijk blootgesteld tijdens beheer

## 5. Rotation Priority

### Hoogste prioriteit
1. `OPENAI_API_KEY`
2. `TELEGRAM_BOT_TOKEN`
3. `OPENCLAW_GATEWAY_TOKEN`
4. `MOONSHOT_API_KEY`
5. `GEMINI_API_KEY`

### Tweede prioriteit
6. Telegram pairing opnieuw beoordelen
7. Device auth opnieuw beoordelen / herpairing indien nodig

## 6. Aanbevolen vervolgstappen

### Direct
- roteer alle actieve provider/API secrets
- vervang gateway token
- vervang Telegram bot token als compromise-impact niet acceptabel is
- beoordeel of pairing/device-auth opnieuw moet

### Daarna
- redaction checks bouwen voor logs
- backups beoordelen op secretretentie
- env hygiene verbeteren
- secrets injectie centraliseren waar mogelijk

## 7. Output van deze block
Deze block levert:
- permission hardening
- secret inventory
- rotation priority
- basis voor latere redaction / rotation runbook
