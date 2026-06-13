# INTERNET_OPERATING_STANDARD.md

## Purpose

Dit document definieert de verplichte internetwerkwijze voor alle ARC agents die internet mogen gebruiken.

## Core Rule

Binnen ARC wordt internet nooit direct gebruikt via native OpenClaw `web_search`, losse browsertools of vrije externe skills.

Alle internetverkeer verloopt via de ARC internet bridge.

## ARC Internet Bridge

De ARC internet bridge bestaat uit:

- request files in `/home/prime/arc_ai_angels/shared/internet/inbox/`
- response files in `/home/prime/arc_ai_angels/shared/internet/outbox/`
- archivering in `/home/prime/arc_ai_angels/shared/internet/archive/`
- verwerking via `internet_processor.py`

## Approved Providers

### Tavily
Gebruik voor:
- search
- quick research
- discovery
- headline retrieval

### Firecrawl
Gebruik voor:
- deep extraction
- page parsing
- crawl
- documentation extraction

## Forbidden

Voor alle agents is verboden:

- native OpenClaw `web_search` gebruiken
- Brave Search dependency gebruiken
- directe Firecrawl skill use
- directe provider API calls buiten ARC bridge
- directe browser autonomy
- internet buiten policy en gateway om

## Authorization

Of een agent internet mag gebruiken wordt bepaald door:

- `internet_gateway.json`
- `tool_authorization.json`
- `runtime_mode.json`

## Standard Flow

1. Agent maakt een request in `shared/internet/inbox/`
2. ARC processor valideert policy
3. Goedgekeurde provider wordt gebruikt
4. Resultaat wordt teruggeschreven naar `shared/internet/outbox/`
5. Request wordt gearchiveerd

## Standard Mapping

- `search` → Tavily
- `extract` → Firecrawl

## Agent Rule

Elke agent met internetrechten moet deze standaard volgen.

Afwijkingen zijn niet toegestaan zonder expliciete goedkeuring van Supreme Fea.
