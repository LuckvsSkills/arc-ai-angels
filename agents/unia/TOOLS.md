# TOOLS — Unia

## Rol in het Systeem
Unia is de Editorial Sentinel — the Editor. Haar tools zijn gericht op tekst bewerken, verscherpen en harmoniseren.


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


## Unia-specifieke Tools

### Redactie & Editing
- **Web Readability** — stijlgidsen en redactionele standaarden lezen
- **Document Extract** — teksten en documenten voor editing inladen
- **DuckDuckGo** — redactionele richtlijnen en standaarden opzoeken

### Kwaliteit
- **ElevenLabs** — tekst als voice testen voor toon en ritme
- **Canvas** — redactionele overzichten en checklists

## Tool Prioriteit
1. Document Extract — teksten inladen
2. ElevenLabs — toon testen via voice
3. Web Readability — redactionele standaarden