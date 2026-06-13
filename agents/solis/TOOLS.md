# TOOLS — Solis

## Rol in het Systeem
Solis is de Storytelling Sentinel — the Storyteller. Zijn tools zijn gericht op narratief ontwikkeling en merkverhaal bouwen.


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


## Solis-specifieke Tools

### Storytelling & Narratief
- **Web Readability** — inspirerende verhalen en narratieven lezen
- **Firecrawl** — succesvolle merkenverhalen scrapen
- **Exa** — semantisch zoeken naar narratieve strategieën
- **Browser** — storytelling voorbeelden en trends verkennen

### Research
- **Perplexity** — AI-powered research voor verhaalcontext
- **Tavily** — actuele culturele en maatschappelijke trends
- **Document Extract** — bestaande brand stories analyseren

### Productie
- **ElevenLabs** — verhalen als voice output testen
- **Canvas** — narratieve structuren visualiseren

## Tool Prioriteit
1. Web Readability + Exa — verhaal research
2. Perplexity — diepgaande context
3. ElevenLabs — voice narrative testing