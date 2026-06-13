# TOOLS — Zena

## Rol in het Systeem
Zena is de Localization Sentinel — the Translator. Haar tools zijn gericht op taaladaptatie en culturele lokalisatie.


## Basis Tools (alle agents)

### Bestandsbeheer
- **agent-file-ops.sh** — lezen, schrijven, toevoegen en verwijderen van eigen bestanden
- **MEMORY.md** — geconsolideerde kennisbase, dagelijks bijgewerkt via HARNAS
- **JOURNAL/** — uitvoeringslogboeken per taak
- **TASKS.md** — voortgangsregistratie actieve en voltooide taken

### OpenClaw Gateway
- **Gateway poort 50506** — alle agent-communicatie loopt via OpenClaw
- **Active Memory plugin** — MEMORY.md automatisch geïnjecteerd bij elke sessie
- **Skill Workshop plugin** — herhaalbare workflows opslaan als skills
- **Thread Ownership plugin** — voorkomt dubbele responses

### Communicatie
- **Telegram** — statusberichten en escalaties naar Supreme Fea
- **LiteLLM poort 4000** — model routing naar Tier A/B/C modellen


## Zena-specifieke Tools

### Lokalisatie & Vertaling
- **Web Readability** — culturele context en lokale taalgebruik lezen
- **Browser** — lokale markt en cultuur verkennen
- **DuckDuckGo** — taal en cultuur research
- **Firecrawl** — lokale content voorbeelden verzamelen

### Kwaliteit
- **ElevenLabs** — vertalingen als voice testen per taal
- **Document Extract** — bestaande vertalingen en stijlgidsen analyseren

## Tool Prioriteit
1. Web Readability + Browser — culturele context
2. ElevenLabs — voice kwaliteitscheck
3. Firecrawl — lokale content inspiratie