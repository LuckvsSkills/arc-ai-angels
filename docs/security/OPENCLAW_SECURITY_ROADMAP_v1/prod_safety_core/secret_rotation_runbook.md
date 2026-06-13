# B10.4 — Secret Rotation Runbook

## Scope
Dit document beschrijft hoe alle kritieke secrets in de OpenClaw / Arc AI Angels omgeving veilig geroteerd kunnen worden zonder de runtime te breken.

Secrets worden als mogelijk gecompromitteerd behandeld omdat ze zichtbaar zijn geweest tijdens beheer in terminaloutput of logs.

---

# 1. Secrets die moeten worden geroteerd

## Prioriteit 1
Deze secrets geven directe toegang tot services.

- OPENAI_API_KEY
- TELEGRAM_BOT_TOKEN
- OPENCLAW_GATEWAY_TOKEN
- MOONSHOT_API_KEY
- GEMINI_API_KEY

## Prioriteit 2

- telegram pairing credentials
- device-auth credentials

---

# 2. Pre-rotation checks

Controleer eerst dat de runtime stabiel is.

Check services:

systemctl status openclaw-flux
systemctl status openclaw-nova

Controleer gateway:

ss -tulpn | grep openclaw

---

# 3. Rotation procedure

## Step 1 — Generate new secrets
Nieuwe keys genereren via:

OpenAI dashboard  
Telegram BotFather  
Moonshot console  
Google Gemini console  

Nieuwe tokens nog niet activeren in runtime.

---

## Step 2 — Update environment

Secrets staan in:

~/.openclaw/.env
~/.openclaw/.env.systemd

Procedure:

1. oude value vervangen
2. file permissions behouden (600)
3. geen secrets loggen

---

## Step 3 — Restart services

Na env update:

sudo systemctl restart openclaw-nova
sudo systemctl restart openclaw-flux

Controleer daarna:

systemctl status openclaw-nova
systemctl status openclaw-flux

---

# 4. Telegram bot rotation

Indien bot token wordt vervangen:

1. nieuw token genereren via BotFather
2. token vervangen in .env
3. service restart
4. test message sturen

---

# 5. Gateway token rotation

Gateway token wordt gebruikt voor agent authentication.

Procedure:

1. nieuw token genereren
2. vervangen in .env
3. services restart
4. gateway health check

---

# 6. Device / pairing credentials

Indien compromise vermoed wordt:

Remove:

~/.openclaw/credentials/telegram-pairing.json
~/.openclaw/identity/device-auth.json

Daarna opnieuw pairen.

---

# 7. Post-rotation validation

Controleer:

openclaw health
telegram messaging
agent execution
memory persistence

---

# 8. Security best practice

Secrets moeten:

- alleen in env files staan
- nooit in logs verschijnen
- niet in git repositories staan
- niet in backups zichtbaar zijn

---

# Output van deze block

Deze block levert:

- veilige secret rotation procedure
- incident response voor secret leaks
- basis voor automated rotation later
