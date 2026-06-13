# MCC HARNAS MONITORING PROMPT
## Nederlandse Chat Instructie voor Real-time Monitoring

Datum: 2026-06-01
Doel: Monitor HARNAS Agent Autonomy System in MCC chat interface

---

## 🎯 PROMPT VOOR MCC CHAT

Kopieer deze prompt in je MCC chat om HARNAS te monitoren:
Perfect! 🎯 Laat me een NEDERLANDSE MCC CHAT PROMPT maken:
bashcat > /home/prime/arc_ai_angels/HARNAS/MCC_CHAT_PROMPT_NL.md << 'EOF'
# MCC HARNAS MONITORING PROMPT
## Nederlandse Chat Instructie voor Real-time Monitoring

Datum: 2026-06-01
Doel: Monitor HARNAS Agent Autonomy System in MCC chat interface

---

## 🎯 PROMPT VOOR MCC CHAT

Kopieer deze prompt in je MCC chat om HARNAS te monitoren:
HARNAS STATUS & MONITORING
Ik wil het HARNAS Agent Autonomy System monitoren dat we zojuist hebben gebouwd.
Dit systeem bestaat uit:

4 Phases (File API, Cronjob API, Auto-Consolidation, Intelligent HARNAS)
32 autonome AI agents
128 dagelijkse cronjobs (4 per agent)
Automatische consolidatie om 00:00, 06:00, 12:00, 18:00

File locaties:

Dashboard: /home/prime/arc_ai_angels/HARNAS/monitoring-dashboard.sh
Agents data: /home/prime/arc_ai_angels/agents/[agent]/
MEMORY groei: /home/prime/arc_ai_angels/agents/[agent]/MEMORY.md
Consolidatie logs: /home/prime/arc_ai_angels/agents/[agent]/consolidation.log
JOURNAL taken: /home/prime/arc_ai_angels/agents/[agent]/JOURNAL/closed/

Ik wil weten:

Zijn alle 32 agents gezond? (MEMORY, JOURNAL, logs aanwezig?)
Zijn alle 128 cronjobs actief? (4 per agent × 32 agents)
Runnen de consolidaties succesvol? (Phase 3 & 4)
Groeit MEMORY dagelijks in alle agents?
Wat zijn de laatste consolidatie resultaten?
Zijn er errors of warnings?

Geef me een duidelijk status overzicht met aanbevelingen.

---

## 📋 ALTERNATIVE PROMPTS (per use case)

### Prompt 1: DAGELIJKSE STATUS CHECK
HARNAS Dagelijkse Status Check
Voer uit en rapporteer:

HEALTH CHECK
Command: /home/prime/arc_ai_angels/HARNAS/monitoring-dashboard.sh
Controleer:

Aantal actieve cronjobs (doel: 128)
Agent status (gezond/waarschuwing)
MEMORY groei
Consolidatie activiteit


CRONJOB VERIFICATIE
Command: crontab -l | grep consolidate-memory
Tel: hoeveel regels? (moet 128 zijn)
SAMPLE AGENTS CHECK
Controleer voor NOVA, ARIX, CORTEXIA:

File: /home/prime/arc_ai_angels/agents/[agent]/consolidation.log
Wat is de laatste entry?
Zijn er errors?



Geef me samenvatting: GROEN (alles OK) / GEEL (waarschuwing) / ROOD (kritiek)

### Prompt 2: MEMORY GROEI ANALYSE
HARNAS Memory Groei Tracking
Analyse 7-dagse groei van agent MEMORY files:
Locatie: /home/prime/arc_ai_angels/agents/*/MEMORY.md
Voor elk van de 32 agents:

Controleer file size
Controleer laatste update timestamp
Toon aantal "Consolidation" entries
Toon aantal "Pattern" entries
Toon aantal "Suggestion" entries

Rapporteer:

Top 5 agents by MEMORY size
Agents met stale MEMORY (>24h geen update)
Totale MEMORY groei
Trend: groeit of plateaut?


### Prompt 3: CONSOLIDATION PERFORMANCE
HARNAS Consolidatie Performance Report
Analyseer consolidation.log files van alle 32 agents:
Locatie: /home/prime/arc_ai_angels/agents/*/consolidation.log
Voor afgelopen 24 uur:

Hoeveel consolidaties succesvol? (target: 128)
Gemiddelde consolidatie duur?
Welke agents hebben errors?
Success rate per agent?
Welke agents missen consolidaties?

Geef:

Success rate % (128/128 = 100%)
Failed consolidations (indien van toepassing)
Agents die aandacht nodig hebben
Aanbevelingen


### Prompt 4: INTELLIGENT PHASE 4 CHECK
HARNAS Phase 4 Intelligent Analysis
Controleer intelligent-consolidation output:
Locatie: /home/prime/arc_ai_angels/agents/*/intelligent-consolidation.log
Voor sample agents (NOVA, ARIX, CORTEXIA, SAELIA, CORTEXIA):

Zijn Phase 4 logs aanwezig?
Welke patterns zijn gedetecteerd?
Welke bottlenecks zijn gevonden?
Welke optimization suggestions zijn gegenereerd?
Worden deze suggestions in MEMORY opgeslagen?

Rapporteer:

Phase 4 operationele status
Intelligentie niveau per agent
Top 3 patterns gedetecteerd
Top 3 bottlenecks


### Prompt 5: CRONJOB SCHEDULE VERIFICATIE
HARNAS Cronjob Schedule Check
Controleer crontab scheduling:
Command: crontab -l | grep consolidate-memory
Toon:

Totaal aantal cronjob entries (moet 128 zijn)
Verdeling over timing:

00:00 (night mode) - moet 32 zijn
06:00 (morning) - moet 32 zijn
12:00 (midday) - moet 32 zijn
18:00 (evening) - moet 32 zijn


Sample van 3 cronjob entries
Zijn er duplicates?
Zijn er broken entries?

Status: ✅ OK / ⚠️ WAARSCHUWING / ❌ KRITIEK

### Prompt 6: AGENT-BY-AGENT DEEP DIVE
HARNAS Agent Analysis [AGENT_NAME]
Diepte analyse van specifieke agent:
(Vervang [AGENT_NAME] met: arix, nova, cortexia, saelia, etc)
Controleer:

MEMORY.md

File size
Aantal learnings
Aantal consolidation entries
Laatst geupdate


consolidation.log

Laatste 5 entries
Success rate
Execution time
Errors/warnings


intelligent-consolidation.log

Patterns gedetecteerd
Bottlenecks gevonden
Suggestions gegenereerd


JOURNAL/closed/

Aantal entries vandaag
Succes rate tasks
Gemiddelde execution time



Rapporteer: Hoe gaat het met deze agent? Wat kan beter?

---

## 🎯 ESSENTIËLE BESTANDSLOCATIES
Dashboard:
/home/prime/arc_ai_angels/HARNAS/monitoring-dashboard.sh
Scripts (Phase 1-4):
/home/prime/arc_ai_angels/HARNAS/Phase1_FileAPI/agent-file-ops.sh
/home/prime/arc_ai_angels/HARNAS/Phase2_CronjobAPI/agent-cronjob-ops.sh
/home/prime/arc_ai_angels/HARNAS/Phase3_AutoConsolidation/consolidate-memory.sh
/home/prime/arc_ai_angels/HARNAS/Phase4_Intelligent/intelligent-consolidation.sh
Agent Data (voor alle 32 agents):
/home/prime/arc_ai_angels/agents/[agent]/MEMORY.md
/home/prime/arc_ai_angels/agents/[agent]/consolidation.log
/home/prime/arc_ai_angels/agents/[agent]/intelligent-consolidation.log
/home/prime/arc_ai_angels/agents/[agent]/JOURNAL/closed/
/home/prime/arc_ai_angels/agents/[agent]/workspace/BOOTSTRAP.md
Cronjob Schedule:
crontab -l | grep consolidate-memory
Documentatie:
/home/prime/arc_ai_angels/CODEX/CH14_MEMORY_JOURNAL_TASK_WORKFLOW.md
/home/prime/arc_ai_angels/CODEX/CH15_AGENT_HARNAS.md
/home/prime/arc_ai_angels/HARNAS/HARNAS_COMPLETE_FINAL_SUMMARY.md

---

## 📊 AGENT LIJST (32 agents)
ORCHESTRATORS (2):
nova, flux
OMNI LEADS (5):
cortexia, saelia, finoria, lumeria, fluentia
SENTINELS (25):
arix, axon, clio, daxio, draven, elora, enki, forge,
kairo, kenzo, kresta, luvia, nero, nura, odis, orizon,
solis, sora, tharos, unia, vector, ventura, vondra, zena, zion

---

## ✅ MONITORING CHECKLIST

- [ ] Dashboard uitvoeren: `/home/prime/arc_ai_angels/HARNAS/monitoring-dashboard.sh`
- [ ] Cronjobs tellen: `crontab -l | grep consolidate-memory` (moet 128 zijn)
- [ ] 32 agents hebben MEMORY.md
- [ ] Consolidatie logs groeiend (afgelopen 24h)
- [ ] Geen errors in Phase 3 & 4 logs
- [ ] Phase 4 patterns gedetecteerd
- [ ] MEMORY files groeiend
- [ ] Geen stale logs (>6 uur oud)

---

**Klaar? Kopieer een prompt hieroven in je MCC chat! 🚀**

