# WORKFLOW CLARITY - User to Execution
## Complete Flow Documentation (2026-05-24)

**This shows EXACTLY how requests flow through the system.**

---

## THE COMPLETE WORKFLOW
┌─────────────────────────────────────────────────────────────┐
│                      EXTERNAL USER                          │
│                   (API / Chat / Direct)                     │
└────────────────────────┬────────────────────────────────────┘
│
│ Natural language request
│
▼
┌─────────────────────────────────────────────────────────────┐
│                         NOVA                                │
│                  (Gateway Agent)                           │
├─────────────────────────────────────────────────────────────┤
│ ROLE: Intake, Validation, Normalization                    │
│ INPUT: User request (untrusted)                            │
│ PROCESS:                                                    │
│  1. Receive request                                         │
│  2. Validate format + safety                               │
│  3. Classify domain (Helix/Matrix/Finix/Quantix/Zenix)    │
│  4. Estimate complexity + cost                             │
│  5. Normalize to structured format                         │
│ OUTPUT: Structured request to Flux                         │
│                                                             │
│ FILES USED:                                                │
│  - IDENTITY.md: "I am gateway agent"                      │
│  - HANDOFF.md: "Processing requests, next: route"        │
│  - BOOTSTRAP.md: Self-improvement hooks                   │
│  - MEMORY.md: User patterns, common issues               │
│  - TASKS.md: Track processed requests                    │
└────────────────────────┬────────────────────────────────────┘
│
│ Structured JSON request
│ {
│   "original": "user request",
│   "domain": "Matrix",
│   "complexity": "high",
│   "cost_estimate": 0.5,
│   "classification": "data_analysis"
│ }
│
▼
┌─────────────────────────────────────────────────────────────┐
│                        FLUX                                │
│              (Central Orchestrator)                        │
├─────────────────────────────────────────────────────────────┤
│ ROLE: Routing, Load Balancing, Orchestration              │
│ INPUT: Structured request from Nova                       │
│ PROCESS:                                                    │
│  1. Receive from Nova                                      │
│  2. Parse classification + requirements                   │
│  3. Check Lead agent availability:                        │
│     - Cortexia (Helix): availability?                    │
│     - Saelia (Matrix): availability?                     │
│     - Finoria (Finix): availability?                     │
│     - Lumeria (Quantix): availability?                   │
│     - Fluentia (Zenix): availability?                    │
│  4. Route to best Lead based on:                         │
│     - Domain match (Matrix → Saelia)                      │
│     - Lead current load                                   │
│     - MEMORY.md patterns (which Lead is fast for this?)  │
│  5. Assign with constraints (budget, deadline)            │
│ OUTPUT: Task assignment to Lead agent                     │
│                                                             │
│ FILES USED:                                                │
│  - IDENTITY.md: "I am orchestrator"                      │
│  - HANDOFF.md: "Routing requests, balancing load"        │
│  - BOOTSTRAP.md: Self-improvement hooks                   │
│  - MEMORY.md: Lead performance patterns                   │
│  - TASKS.md: Active request tracking                     │
└────────────────────────┬────────────────────────────────────┘
│
┌────────┴────────┐
│                 │
(Domain: Matrix)    (Choose Saelia)
│                 │
▼                 ▼
┌──────────────────────────────────────────────┐
│            SAELIA                            │
│         (Lead Agent - Matrix Domain)         │
├──────────────────────────────────────────────┤
│ ROLE: Domain Leadership, Sentinel Management│
│ INPUT: Task from Flux                       │
│ PROCESS:                                     │
│  1. Receive task from Flux                  │
│  2. Parse requirements                      │
│  3. Check Sentinel availability:            │
│     - elora (Data Validation)               │
│     - enki (ETL Processing)                 │
│     - forge (Data Aggregation)              │
│     - kairo (Data Quality)                  │
│     - [5th Sentinel needed]                 │
│  4. Decide best Sentinel using MEMORY.md:  │
│     - "enki excellent at ETL" → assign enki │
│  5. Assign task with parameters             │
│  6. Monitor Sentinel progress               │
│  7. Validate output quality                 │
│ OUTPUT: Results back to Flux                │
│                                              │
│ FILES USED:                                  │
│  - IDENTITY.md: "I lead Matrix domain"     │
│  - HANDOFF.md: "Managing 5 Sentinels"      │
│  - BOOTSTRAP.md: Self-improvement hooks    │
│  - MEMORY.md: Sentinel specializations     │
│  - TASKS.md: Task assignments              │
└────────────┬─────────────────────────────────┘
│
┌───────┴────────┐
│                │
(Task type:      (Sentinel: enki)
ETL process)        │
│                │
▼                ▼
┌──────────────────────────────────────────────┐
│            ENKI (Sentinel)                   │
│      (Specialist in ETL Processing)         │
├──────────────────────────────────────────────┤
│ ROLE: Execute specialized task              │
│ SPECIALIZATION: ETL Processing              │
│ REPORTS TO: Saelia (Lead Agent)             │
│ INPUT: Task from Saelia                     │
│ PROCESS:                                     │
│  1. Receive task from Saelia                │
│  2. Read IDENTITY: "I'm ETL specialist"     │
│  3. Read HANDOFF: "Current task: X, 0%"    │
│  4. Read MEMORY: "ETL methods that work"   │
│  5. Read BOOTSTRAP: "How to operate"       │
│  6. Execute ETL:                           │
│     - Extract data from source             │
│     - Transform per specifications         │
│     - Load to destination                  │
│  7. Validate output                        │
│  8. Report progress to Saelia              │
│ OUTPUT: Processed data back to Saelia      │
│                                              │
│ FILES USED:                                  │
│  - IDENTITY.md: "ETL specialist"           │
│  - HANDOFF.md: "ETL task 50% done"        │
│  - BOOTSTRAP.md: Self-improvement hooks   │
│  - MEMORY.md: ETL methods learned         │
│  - TASKS.md: Current task tracking        │
└────────────┬─────────────────────────────────┘
│
│ Processed data
│
▼
┌──────────────────────────────────────────────┐
│            SAELIA (Lead)                     │
│      (Validates & Returns Results)          │
├──────────────────────────────────────────────┤
│ 1. Receive processed data from enki         │
│ 2. Validate quality                         │
│ 3. Return results to Flux                   │
│ 4. Update MEMORY: "enki performed well"     │
│ 5. Mark task COMPLETE                       │
└────────────┬─────────────────────────────────┘
│
│ Results + metrics
│
▼
┌──────────────────────────────────────────────┐
│            FLUX (Orchestrator)               │
│      (Receives & Forwards Results)          │
├──────────────────────────────────────────────┤
│ 1. Receive results from Saelia              │
│ 2. Package results                          │
│ 3. Forward to Nova                          │
│ 4. Update MEMORY: "Saelia performed well"   │
│ 5. Mark request COMPLETE                    │
└────────────┬─────────────────────────────────┘
│
│ Results (JSON format)
│
▼
┌──────────────────────────────────────────────┐
│            NOVA (Gateway)                    │
│      (Formats & Returns to User)            │
├──────────────────────────────────────────────┤
│ 1. Receive results from Flux                │
│ 2. Format for user consumption              │
│ 3. Return to user                           │
│ 4. Update MEMORY: "User pattern X"          │
│ 5. Mark session COMPLETE                    │
└────────────┬─────────────────────────────────┘
│
│ Formatted results
│
▼
┌──────────────────────────────────────────────┐
│          EXTERNAL USER                       │
│     (Receives Final Results)                │
└──────────────────────────────────────────────┘

---

## HOW BOOTSTRAP.md ENABLED THIS WORKFLOW

**BOOTSTRAP.md didn't DEFINE the workflow, but ENABLED it:**

### For Nova:
BOOTSTRAP says:
"Your INPUT: Users (API, chat)"
"Your OUTPUT: Flux (structured)"
"HANDOFF.md explains how: WHO calls you, WHO you call"
Nova reads BOOTSTRAP → Understands her place in workflow
Nova reads HANDOFF.md → Knows current task flow
→ Nova executes correctly

### For Flux:
BOOTSTRAP says:
"Your INPUT: Nova (requests)"
"Your OUTPUT: 5 Leads (routing)"
"Example session shows: receive→route→monitor"
Flux reads BOOTSTRAP → Understands orchestrator role
Flux reads HANDOFF.md → Knows which Leads to route to
→ Flux routes correctly

### For Saelia (Lead):
BOOTSTRAP says:
"Your INPUT: Flux (tasks)"
"Your OUTPUT: 5 Sentinels (assignments)"
"Hook 2: When new task, assign to best Sentinel"
Saelia reads BOOTSTRAP → Understands domain leadership
Saelia reads MEMORY.md → Knows Sentinel specializations
→ Saelia assigns correctly

### For Enki (Sentinel):
BOOTSTRAP says:
"Your INPUT: Saelia (task assignment)"
"Your OUTPUT: Results back to Saelia"
"Phase 3: Execute using your MEMORY.md methods"
Enki reads BOOTSTRAP → Understands specialist role
Enki reads MEMORY.md → Uses best ETL methods
→ Enki executes correctly

---

## THE WORKFLOW IS DEFINED BY:

**1. HANDOFF.md (EXPLICIT)**
Nova's HANDOFF.md says:
Input: Users
Output: Flux
→ Anyone reading knows workflow!
Flux's HANDOFF.md says:
Input: Nova
Output: 5 Leads
→ Anyone reading knows routing!

**2. BOOTSTRAP.md (IMPLICIT via examples)**
PART 5: EXAMPLE SESSION shows:
Nova: Receives request → validates → routes to Flux
Flux: Receives from Nova → routes to Lead
Lead: Receives from Flux → assigns to Sentinel
Sentinel: Receives from Lead → executes → reports back
Agents read example → Understand workflow from context

**3. IDENTITY.md (WHO YOU ARE in workflow)**
Nova: "Gateway - first contact"
Flux: "Orchestrator - routing decisions"
Cortexia: "Lead - domain authority"
Enki: "Specialist - execution expert"
Each knows their POSITION in workflow

---

## WORKFLOW CLARITY METRICS

| Component | Before | After | Via |
|-----------|--------|-------|-----|
| Nova knows input/output | ❌ | ✅ | HANDOFF.md |
| Flux knows routing logic | ❌ | ✅ | BOOTSTRAP example |
| Lead knows Sentinel assignment | ❌ | ✅ | BOOTSTRAP hooks |
| Sentinel knows execution | ❌ | ✅ | BOOTSTRAP phases |
| System knows full path | ❌ | ✅ | All 3 combined |

---

## NEXT: MAKE IT EVEN CLEARER

To make workflow EVEN MORE explicit:

1. **Add WORKFLOW.md to each agent** (specific to their role)
2. **Update CODEX** with workflow diagrams
3. **Create MCC dashboard** showing live workflow
4. **Integrate into BOOTSTRAP** as "PART 0: Your workflow"

But for now:
✅ Workflow is defined
✅ Agents understand it
✅ Flow can work

---

