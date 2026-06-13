# Session Index

## Organization
Sessions are organized by date in YYYY-MM-DD format.
Each session has:
- SUMMARY.md (what was done)
- NOTES.md (thoughts & observations)
- ARTIFACTS/ (files created)
- DECISIONS.md (choices made)

## Quick Navigation

### 2026-05-27 - OpenClaw & Cronjob System
- Status: COMPLETE
- Focus: Infrastructure fix, cronjob errors, NOVA architecture
- Key files: CRONJOB_STANDARD.md, NOVA_DIRECT_ACCESS.md
- Next: NOVA direct access implementation

### 2026-05-28 - NOVA Direct Access (Planning)
- Status: PENDING
- Focus: Token system, direct CLI access

---
Last updated: 2026-05-27

### 2026-06-05 - Model Routing, HARNAS & Agentic Levels
- Status: COMPLETE
- Focus: CH19 model tiers, CH20 agentic levels, HARNAS afronden, Active Memory plugin
- Key files: CH19_MODEL_ROUTING_STRATEGY.md, CH20_AGENTIC_LEVEL_FRAMEWORK.md
- Next: Telegram berichten verifiëren, Active Memory testen, flux_core vervangen

### 2026-06-05 (avond) — SOUL.md, WORKFLOW.md & Backups
- Status: COMPLETE
- Focus: Alle 33 agents SOUL.md en WORKFLOW.md volledig herschreven met karakter, persoonlijkheid, beslislogica en HARNAS integratie
- Key: Nova=Consigliere/Silver Surfer, Flux=Underboss, 4 agent types uitgewerkt
- Next: Git backup, Replit frontend integratie, Telegram wrap-up berichten verifiëren

### 2026-06-05 (nacht) — CODEX v2.0
- Status: COMPLETE
- Focus: Volledige herschrijving CODEX van 20 naar 12 hoofdstukken — verhalend, volledig Nederlands, met 17 Mermaid diagrammen
- Key: CH01-CH12 nieuw, logische verhaallijn, oude versies gearchiveerd
- Next: Diagrammen in MCC Diagrams tab tonen, CODEX Canon tab updaten

### 2026-06-06 (nacht) — Telegram wrap-up fix
- Status: COMPLETE
- Focus: 32 wrap-up cronjobs sturen geen Telegram meer, Nova master-status cronjob aangemaakt op 22:15 UTC
- Key: Één gecombineerd nachtrapport via Nova, alleen falende agents bij naam
- Next: Monitoren of nachtrapport consistent binnenkomt

### 2026-06-06 — Plugins, Voice Stack & Search
- Status: COMPLETE
- Focus: 16 plugins ingeschakeld, ElevenLabs/Deepgram/Exa/Perplexity API keys geconfigureerd, 32 agents elk eigen stem toegewezen
- Key: Voice stack klaar voor MCC integratie, Search stack volledig operationeel
- Next: Voice UI in MCC frontend (Replit), Research Pipeline workflow, Agent stemmen testen

### 2026-06-06 (later) — Tools per agent & CH10
- Status: COMPLETE
- Focus: Alle 32 agents TOOLS.md herschreven, tools_api.json aangemaakt met 28 tools, CH10 herschreven, MCC Tools tab live met nieuwe data
- Key: 28 tools verdeeld over 8 categorieën, alle agents specifieke toolset
- Next: Voice UI in MCC, Research Pipeline workflow, CH09 Skills herschrijven

### 2026-06-06 (avond) — Skills systeem
- Status: COMPLETE
- Focus: SKILLS.md alle 33 agents herschreven, 18 OpenClaw skills per agent geconfigureerd, Skills API backend, SkillsTab in Kernel, CH09 herschreven
- Key: Twee vormen van skills — identiteit (SKILLS.md) en uitvoerbaar (OpenClaw skills)
- Next: Frontend bouwen in Replit, Research Pipeline workflow, Skill bibliotheek GitHub

### 2026-06-06 (nacht) — CODEX, Diagrams, Skills & Tools in MCC
- Status: COMPLETE
- Focus: Canon→Codex hernoemd, DiagramsTab met 17 Mermaid diagrammen, SkillsTab in Kernel, CODEX v2.0 live in MCC
- Key: Alle 12 nieuwe hoofdstukken zichtbaar, alle 17 diagrammen rendeerbaar, Skills tab volledig
- Next: Replit frontend integratie, Voice UI, Research Pipeline workflow

## 2026-06-11
- Helix domain volledig (6 agents, skills, workers)
- Nova/Flux workflows + HARNAS bijgewerkt
- MCC: Services, Domein, Kosten, Tasks tabs
- 32 agents WORKFLOW.md + TASKS.md governance update
- Kosten monitoring + tool budget bewaking

## 2026-06-12
- HARNAS herstructureerd: 127→71 jobs, nieuwe tijden Amsterdam
- Helix audit: cron failures, llm-task misbruik, skill workshop approval
- MCC Skills Tab: pending approvals + actieve skills + bibliotheek
- Tool governance: dure tools beperkt tot Cortexia
