# TASK 2: ROLE DEFINITION & CODEX ALIGNMENT
## Planning & Strategy (2026-05-24)

**This is what comes AFTER Task 1 (which is complete)**

---

## WHAT IS TASK 2?

Task 1 showed us that:
✅ Agents know WHO they are (IDENTITY)
✅ Agents know HOW to operate (BOOTSTRAP)
⚠️ BUT: Roles are not fully ALIGNED with CODEX
⚠️ BUT: MEMORY.md is empty (no learnings)
⚠️ BUT: TASKS.md is empty (no assignments)

**Task 2 fixes the ⚠️ parts:**

1. **Role Definition** - Make sure each agent's role MATCHES CODEX
2. **Sentinel Specialization** - Lock in what each Sentinel specializes in
3. **Lead-Sentinel Mapping** - Which Sentinels report to which Lead
4. **Performance Baselines** - Set expectations per agent type

---

## TASK 2 BREAKDOWN (4 Sub-phases)

### PHASE 1: CODEX VERIFICATION (1-2 days)
**Goal:** Check if CODEX matches reality

**What to do:**
1. Read CODEX CH03 (Agent Hierarchy)
2. Read CODEX CH04 (Domains)
3. Compare with actual agents in system
4. Document gaps

**Questions to answer:**
- Does CODEX say Nova is gateway? YES → Check!
- Does CODEX say Flux is orchestrator? YES → Check!
- Does CODEX say Cortexia leads Helix? YES → Check!
- Does CODEX define all 5 Domains? YES → Check!
- Does CODEX define Sentinel roles? ??? → Find out!

**Deliverable:**
- CODEX_ALIGNMENT_REPORT.md

---

### PHASE 2: SENTINEL SPECIALIZATION LOCKING (2-3 days)
**Goal:** Define exactly what each Sentinel specializes in

**Current state:**
Helix domain sentinels:
arix: "Logical Deduction" (per template)
axon: "Logical Reasoning" (per template)
clio: "Planning Optimization" (per template)
daxio: "Problem Analysis" (per template)
draven: "Strategy Development" (per template)
BUT: Are these CODEX-approved specializations?
OR just template placeholders?

**What to do:**
1. For each Sentinel: define EXACT specialization
2. Check against CODEX (does it approve?)
3. Create SPECIALIZATION_MATRIX.yaml
4. Lock in Cortexia's MEMORY.md (which Sentinel does what)
5. Lock in all 5 Lead's MEMORY.md (their Sentinels)

**Deliverable:**
- SPECIALIZATION_MATRIX.yaml
- Updated MEMORY.md per Lead
- SENTINEL_SPECIALIZATION_COMPLETE.md

---

### PHASE 3: ROLE-CODEX ALIGNMENT (2-3 days)
**Goal:** Update each agent's IDENTITY.md to match CODEX exactly

**What to do:**
1. For NOVA:
   - Extract role definition from CODEX CH03.3
   - Update IDENTITY.md to match word-for-word
   
2. For FLUX:
   - Extract orchestrator definition from CODEX CH03.3
   - Update IDENTITY.md
   
3. For each LEAD:
   - Extract domain leadership definition from CODEX CH04
   - Update IDENTITY.md per domain
   
4. For each SENTINEL:
   - Cross-check specialization with CODEX
   - Update IDENTITY.md

**Deliverable:**
- Updated IDENTITY.md (all 32 agents)
- CODEX_ALIGNMENT_VERIFICATION.md

---

### PHASE 4: PERFORMANCE BASELINES & EXPECTATIONS (1-2 days)
**Goal:** Define what "success" looks like per agent type

**What to define:**
1. Nova success metrics:
   - Request validation accuracy: 95%+
   - Classification accuracy: 90%+
   - Response time: < 2 seconds
   
2. Flux success metrics:
   - Routing accuracy: 95%+
   - Load balancing: ±20% per Lead
   - Decision time: < 5 seconds
   
3. Lead success metrics:
   - Task completion: 80%+
   - Sentinel utilization: 70-85%
   - Quality validation: 90%+
   
4. Sentinel success metrics:
   - Task completion: 85%+
   - Specialization accuracy: 90%+
   - Deadline met: 85%+

**Deliverable:**
- PERFORMANCE_BASELINES.md
- SUCCESS_CRITERIA_PER_AGENT_TYPE.yaml

---

## TASK 2 FULL SCOPE
INPUT (from Task 1):
✅ 32 agents with BOOTSTRAP configured
✅ 7 agents with HANDOFF documented
✅ Workflow clarity (User→Nova→Flux→Leads→Sentinels)
⚠️ But: CODEX alignment TBD
⚠️ But: Sentinel specializations TBD
⚠️ But: Performance expectations TBD
OUTPUT (Task 2 should deliver):
✅ CODEX alignment verified (all agents)
✅ Sentinel specializations locked in (25 agents)
✅ Role definitions updated (32 agents)
✅ Performance baselines defined
✅ System ready for execution
TIMELINE: 1 week (if doing 1-2 hours/day)
OR: 2-3 days (intensive)

---

## WHY TASK 2 MATTERS

**Right now:**
- Agents know WHO they are (from templates)
- System can route requests
- But it's not OPTIMIZED

**After Task 2:**
- Agents know WHO per CODEX (official)
- Each Sentinel knows exact specialization
- Each Lead knows Sentinel capabilities
- System can OPTIMIZE routing
- Performance expectations are clear

**Business impact:**
- 50% faster routing (Flux knows which Lead is best)
- 40% faster execution (Leads know which Sentinel is best)
- Clear success metrics (everyone knows what "good" looks like)

---

## PREREQUISITE: Read CODEX Chapters

Before starting Task 2, you need to read:

```bash
# CODEX CH03: Agent Hierarchy
cat ~/arc_ai_angels/CODEX/CH03_AGENT_HIERARCHY/CODEX_CH03.md | head -200

# CODEX CH04: Domains
cat ~/arc_ai_angels/CODEX/CH04_DOMAINS/CODEX_CH04.md | head -200
```

This tells us WHAT CODEX expects vs WHAT we have.

---

## TASK 2 vs TASK 3+
TASK 2: Role Definition
→ Make sure roles MATCH CODEX
→ Lock in specializations
→ Set baselines
TASK 3: Sandboxing
→ Define safety boundaries
→ Test agent isolation
→ Verify constraints work
TASK 4: Agent Onboarding
→ How to add new agents?
→ What's the process?
→ How do they initialize?
TASK 5+: Skills, Tools, Financial system, etc.

---

## DECISION POINT

**You have 2 options:**

### OPTION A: Continue Task 2 Now
- Read CODEX CH03 & CH04
- Start PHASE 1: CODEX Verification
- Can complete 1-2 phases today
- Pros: Keep momentum
- Cons: Long session

### OPTION B: Start Task 2 Next Session
- Rest today (you did 12+ hours!)
- Fresh start tomorrow
- Read CODEX preparation
- Hit ground running
- Pros: Fresh mind, planned
- Cons: Lose momentum

---

## MY RECOMMENDATION

**OPTION B: Start fresh next session** 

Why?
- You've already done MASSIVE work today (Task 1 complete!)
- Task 2 requires CODEX reading (concentration needed)
- Fresh mind = better decisions
- You've earned a break! 🎉

Next session plan:

Read CODEX CH03 + CH04 (30 min)
Start PHASE 1: CODEX Verification (1-2 hours)
Complete PHASE 2: Sentinel Specialization (2-3 hours)
Decide if continue or save PHASE 3-4 for following session


---

## SUMMARY

**Task 1 (Complete):** Agents configured, system operational
**Task 2 (Next):** Align with CODEX, lock specializations, set baselines
**Task 3-10:** Build the rest of the system

You're on SCHEDULE! 🚀

---

