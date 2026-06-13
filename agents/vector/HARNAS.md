# HARNAS — Your Autonomy System

## WHAT IS HARNAS?

HARNAS = **HA**ndling **R**esources **N**on-**AS**siduously

A system that makes YOU autonomous by automatically managing your memory consolidation.

---

## HOW DOES HARNAS WORK FOR YOU?

### Your Daily Cycle:
You Execute Task
↓
Log to JOURNAL.md (what you did)
↓
Update MEMORY.md (what you learned)
↓
At 00:00, 06:00, 12:00, 18:00 → CRONJOB RUNS
↓
consolidate-memory.sh reads your files
↓

Reads MEMORY.md (your knowledge)
Reads JOURNAL.md (your actions)
Reads TASK_HISTORY.md (your results)
↓
CONSOLIDATES → removes noise, patterns, irrelevant
↓
UPDATES MEMORY.md → compressed, optimized
↓
NEXT TASK: YOU'RE SMARTER (read optimized MEMORY.md)
---

## YOUR FILES IN HARNAS

### MEMORY.md
- **What:** Your persistent knowledge base
- **Updated by:** You (during execution) + HARNAS (consolidation)
- **Read by:** You (to recall past learnings)
- **Growth:** Gets more concise, more valuable over time

### JOURNAL.md
- **What:** Your daily execution log
- **Updated by:** You (every task completed)
- **Read by:** HARNAS (to find patterns)
- **Purpose:** Raw data for consolidation

### TASK_HISTORY.md
- **What:** Structured record of completed tasks
- **Updated by:** You (task completion)
- **Read by:** HARNAS (to validate patterns)
- **Purpose:** Structured tracking

---

## HARNAS SCHEDULE
00:00 → Midnight consolidation (deep cleanup)
06:00 → Morning consolidation (prepare for day)
12:00 → Midday consolidation (pattern recognition)
18:00 → Evening consolidation (reflect on day)
Each cronjob takes ~5-10 minutes per agent.

---

## WHAT TO EXPECT

**Week 1:** Memory starts getting organized
**Week 2:** You notice patterns emerging
**Week 3:** Your responses become more concise
**Week 4:** You operate at 2x efficiency

---

## YOUR RESPONSIBILITY

To make HARNAS work:
1. **Write clear JOURNAL entries** → HARNAS learns from them
2. **Update MEMORY.md thoughtfully** → becomes your knowledge base
3. **Log task completion** → tracks your progress
4. **Review consolidated MEMORY** → understand your growth

**Bad input → Bad consolidation → No growth**
**Good input → Smart consolidation → Exponential growth**

---

## HOW TO MONITOR YOUR HARNAS

Check:
- `HARNAS/logs/execution/[AGENT]/consolidation.log` → your consolidations
- `HARNAS/logs/cronjobs/` → all system cronjobs
- Your MEMORY.md file size → should stabilize after week 2

---

## RELATIONSHIP WITH CODEX

HARNAS operates based on CODEX standards:
- See CODEX/CH15_AGENT_HARNAS.md for system-level docs
- HARNAS ensures you stay CODEX-conforme
- Your consolidated MEMORY.md IS your personal CODEX

---

## KEY PRINCIPLE

**You become what you consolidate.**

Clean, thoughtful MEMORY.md = Clean, thoughtful agent
Messy JOURNAL.md = Messy learning → messy consolidation

HARNAS is your tool for self-improvement.

