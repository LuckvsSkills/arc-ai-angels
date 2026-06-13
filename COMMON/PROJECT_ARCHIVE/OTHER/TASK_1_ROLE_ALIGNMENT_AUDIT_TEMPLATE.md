# TASK 1: ROLE ALIGNMENT AUDIT
## Agent Role Clarity & Self-Improvement Capability Assessment

**Focus:** Niet "hebben ze alle files?" maar "BEGRIJPEN ze hun rol en kunnen ze zichzelf verbeteren?"

---

## PER AGENT AUDIT CHECKLIST

### AGENT: [agent_name]

#### DEEL 1: ROLE ALIGNMENT

Stated Role (van IDENTITY.md in workspace/):
  [Wat zegt de agent over zichzelf?]

Expected Role (van CODEX):
  [Wat zegt CODEX dat ze hoort te zijn?]

ALIGNMENT:
  OK ALIGNED / PARTIAL / MISALIGNED
  
Gaps (als er zijn):
  - [Gap 1]
  - [Gap 2]

#### DEEL 2: WORKFLOW CLARITY

INPUT: Wie/wat roept deze agent aan?
  [Beschrijf input source + protocol]

OUTPUT: Wie/wat roept deze agent aan?
  [Beschrijf output destination + protocol]

DECISION AUTHORITY:
  Can decide:
    - [Decision 1]
    - [Decision 2]
  Cannot decide:
    - [Boundary 1]
    - [Boundary 2]

CLARITY SCORE: 0-100%

#### DEEL 3: SELF-IMPROVEMENT CAPABILITY

BOOTSTRAP.md (in workspace/):
  Exists: YES/NO
  Actionable: YES/NO (kan agent eigen files updaten?)
  Quality: HIGH/MEDIUM/LOW

Can update own files:
  HANDOFF.md: YES/NO (trigger framework?)
  MEMORY.md: YES/NO (trigger framework?)
  TASKS.md: YES/NO (trigger framework?)

Self-improvement score: 0-100%

#### DEEL 4: CODEX ALIGNMENT

CODEX says:
  Template type: [Blue Core / Blue Lead / Blue Sentinel]
  Layer: [number + name]
  Status: [Operational / Partial / Missing]

Files in workspace/ match CODEX spec:
  YES / NO
  
Issues found:
  - [Issue 1]
  - [Issue 2]

#### DEEL 5: TECHNICAL ISSUES

Errors in BOOTSTRAP.md: YES/NO
  [Describe if yes]

Missing critical files: YES/NO
  [Which ones if yes]

File format issues: YES/NO
  [Describe if yes]

#### SUMMARY

Overall Role Clarity: ___% (0-100)
Workflow Understanding: ___% (0-100)
Self-improvement Capability: ___% (0-100)
CODEX Alignment: ___% (0-100)
Technical Readiness: ___% (0-100)

OVERALL STRENGTH: ___% (0-100)

Status:
  READY FOR OPERATIONS
  NEEDS CLARIFICATION
  BLOCKED - NEEDS FIXES

Next Actions:
  1. [Action 1]
  2. [Action 2]
  3. [Action 3]

---

## EXECUTION STEPS

Step 1: Start with NOVA (reference agent)

cd ~/arc_ai_angels/agents/nova
ls -la workspace/
cat workspace/IDENTITY.md
cat workspace/BOOTSTRAP.md
cat workspace/HANDOFF.md
cat workspace/MEMORY.md

Step 2: Compare with CODEX

cat ~/arc_ai_angels/CODEX/CH10_AGENT_CONFIG_1/CODEX_CH10.md | grep -A 40 "NOVA"

Step 3: Fill audit checklist

Use template above for Nova, document findings

Step 4: Move to next agent

Repeat for: Flux, Cortexia, Finoria, Fluentia, then Sentinels

---

## PATTERN TO FIND

Good alignment means:
- Agent weet haar rol
- Agent weet wie haar aanroept
- Agent weet wie zij aanroept
- Agent kan zichzelf verbeteren (Bootstrap + triggers)
- Agent leest CODEX correct

Bad alignment means:
- Agent weet haar rol niet (IDENTITY unclear)
- Agent weet workflow niet (HANDOFF onduidelijk)
- Agent kan niet zichzelf updaten (no triggers)
- Agent past niet in CODEX spec
- Files zijn inconsistent

---

## DELIVERABLE

Final document: AGENTS_ROLE_ALIGNMENT_AUDIT.yaml

audit_results:
  nova:
    role_alignment: 85%
    workflow_clarity: 90%
    self_improvement: 60%
    codex_alignment: 95%
    overall: 82.5%
    status: "READY (need self-improvement triggers)"
    
  flux:
    role_alignment: 90%
    workflow_clarity: 95%
    self_improvement: 70%
    codex_alignment: 95%
    overall: 87.5%
    status: "READY (need self-improvement triggers)"
    
  [etc for all agents]

