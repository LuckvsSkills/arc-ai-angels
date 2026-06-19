# Website Agent Config — TestWebshop
**Website:** https://testwebshop.vercel.app
**Type:** ecommerce
**Aangemaakt:** 2026-06-13
**Door:** Clio — ARC AI Agents

---

## Agent identiteit

**Naam:** testwebshop-agent
**Rol:** Website beheer agent voor TestWebshop
**Platform:** OpenClaw (eigen instantie of ARC systeem)

---

## Taken van deze agent

- Nieuwe bestellingen verwerken en bevestigingsmail sturen
- Leveranciers informeren bij lage voorraad
- Klantenvragen beantwoorden via email
- Wekelijks omzetrapport sturen aan eigenaar
- Verlaten winkelwagens opvolgen met reminder email

---

## Configuratie

### OpenClaw setup
```bash
# Installeer OpenClaw op de doelserver
curl -fsSL https://openclaw.ai/install.sh | bash

# Configureer agent
openclaw agent create testwebshop-agent \
  --role "Website beheer agent voor TestWebshop" \
  --model "gpt-4o-mini"
```

### Environment variables
WEBSITE_URL=https://testwebshop.vercel.app

ADMIN_URL=https://testwebshop.vercel.app/admin

WEBSITE_TYPE=ecommerce

OWNER_EMAIL=eigenaar@testwebshop.nl

TELEGRAM_CHAT_ID=VUL_IN

### Cronjobs
Dagelijkse check
0 9 * * * openclaw task testwebshop-agent "Voer dagelijkse website check uit"
Wekelijks rapport
0 10 * * 1 openclaw task testwebshop-agent "Maak wekelijks rapport voor eigenaar"

---

## Kosten schatting

| Gebruik | Model | Kosten/maand |
|---------|-------|-------------|
| Lichte taken | gemini-flash | ~€5-15 |
| Normale taken | gpt-4o-mini | ~€15-30 |
| Intensieve taken | gpt-4o | ~€30-80 |

**Aanbeveling:** gpt-4o-mini (~€15-30/maand)

---

*Gegenereerd door Clio — ARC AI Agents*
