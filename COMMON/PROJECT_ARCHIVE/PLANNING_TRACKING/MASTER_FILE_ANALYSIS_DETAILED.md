# Master File Analysis - Per File Assessment

## TIER 1: FILES THAT SHOULD BE MASTER (Universal content)

### ✅ USER.md 
**NOVA: 65 lines | FLUX: 146 lines | NERO: 21 lines**

**Assessment: YES - MASTER CANDIDATE**
- Content: About YOU (the user/owner)
- Universal: Same content for ALL agents
- Why: You don't change per agent
- Recommendation: Create USER_MASTER.md, all agents REFERENCE it
- Customization needed: None (except agent's perspective on YOU)

---

### ✅ HEARTBEAT.md
**NOVA: 2 lines | FLUX: 106 lines | NERO: 9 lines**

**Assessment: PARTIALLY - Hybrid Master**
- NOVA version: Too minimal (2 lines)
- FLUX version: 106 lines - much more complete
- NERO version: 9 lines - minimal
- Universal parts: Monitoring structure, status checks
- Agent-specific: Their specific responsibilities to monitor
- Recommendation: Create HEARTBEAT_MASTER.md with structure + customizable sections
- Customization needed: Per-agent responsibilities

---

### ✅ PROTOCOL.md
**NOVA: 71 lines | FLUX: 21 lines | Not in NERO**

**Assessment: PARTIALLY - Hybrid Master**
- Universal parts: Communication standards, format rules
- Agent-specific: Their role in communication chain
- NOVA version longer = more detail needed?
- FLUX version shorter = simplified?
- Recommendation: Create PROTOCOL_MASTER.md (universal comms rules) + agent customizations
- Customization needed: Their specific protocol role

---

### ✅ SECURITY.md
**NOVA: 55 lines | FLUX: 17 lines | Not in NERO**

**Assessment: PARTIALLY - Hybrid Master**
- Universal parts: Security policies, restrictions, forbidden actions
- Agent-specific: Their access levels, allowed tools
- Both have similar structure
- Recommendation: Create SECURITY_MASTER.md (policies) + agent-specific access/restrictions
- Customization needed: Per-agent security level

---

### ✅ REPORTING.md
**NOVA: 80 lines | FLUX: 38 lines | Not in NERO**

**Assessment: PARTIALLY - Hybrid Master**
- Universal parts: Reporting format, structure, required fields
- Agent-specific: What they report on, their metrics
- Similar structure in both
- Recommendation: Create REPORTING_MASTER.md (format) + agent-specific metrics
- Customization needed: Per-agent reporting focus

---

## TIER 2: FILES THAT ARE HYBRID (Mix of universal + specific)

### 🟡 IDENTITY.md
**NOVA: 51 lines | FLUX: 50 lines | NERO: 27 lines**

**Assessment: NO - Keep agent-specific**
- Universal structure: Layer, Domain, Parent, Role, Mission, Core Identity, Cognitive Style
- Agent-specific content: Every field is unique per agent
- Example: 
  - NOVA role = "First-Line Operator / Gateway"
  - FLUX role = "Central Orchestration & Routing Engine"
  - NERO role = "Reasoning Specialist"
- Recommendation: NO MASTER - Each agent needs unique identity
- Template: Use structure as template, not master

---

### 🟡 SOUL.md
**NOVA: 25 lines | FLUX: 20 lines | NERO: 42 lines**

**Assessment: NO - Keep agent-specific + TONE template**
- Structure is universal: Principles, Behavior, Responsibility
- Content is ENTIRELY unique per agent
- Example principles:
  - NOVA: "elke externe input verdient eerst helderheid"
  - FLUX: "routing zonder samenhang is fout"
  - NERO: (would be unique)
- Recommendation: NO MASTER - Each agent has unique personality
- Note: But use TONE templates (Female/Male vibe) to guide writing

---

### 🟡 TOOLS.md
**NOVA: 23 lines | FLUX: 36 lines | NERO: 44 lines**

**Assessment: PARTIALLY - Hybrid Master**
- Universal parts: Default policies (deny-by-default), general rules
- Agent-specific: Their allowed tools, restrictions, special permissions
- Structure: Similar in both
- Recommendation: Create TOOLS_MASTER.md (policies) + agent-specific allowed/forbidden sections
- Customization needed: Per-agent tool access

---

### 🟡 SKILLS.md
**NOVA: 74 lines | FLUX: 37 lines | Not in NERO**

**Assessment: NO - Keep agent-specific**
- Content: Lists THEIR specific skills and expertise
- NOVA skills: Different from FLUX skills
- NERO skills: Would be unique
- Recommendation: NO MASTER - Each agent has different skills
- Template: Use structure as template for consistency

---

### 🟡 AGENTS.md
**NOVA: 410 lines | FLUX: 154 lines | NERO: 218 lines**

**Assessment: NO - Keep agent-specific**
- Content: Their relationships to OTHER agents
- NOVA's agents list: Different from FLUX's list
- NERO would list their relationships
- Dynamic: Changes as system evolves
- Recommendation: NO MASTER - Each agent manages their own relationships
- Template: Use structure as template

---

## TIER 3: FILES THAT ARE SPECIALIZED (Usually NO master)

### ❌ MEMORY.md
**NOVA: 20 lines | FLUX: 21 lines | Not in NERO (yet)**

**Assessment: NO - Keep agent-specific**
- Content: Their specific memory structure and approach
- Recommendation: NO MASTER - Each agent may have different memory needs
- Note: Could have MEMORY guidelines/structure as template, not master

---

### ❌ MEMORY_RULES.md
**NOVA: 173 lines | FLUX: 202 lines | Not in NERO**

**Assessment: PARTIALLY - Shared rules**
- Universal: Some memory governance rules apply to all
- Agent-specific: Their memory constraints and rules
- Recommendation: Create MEMORY_RULES_MASTER.md (shared governance) + agent overrides
- Customization: Per-agent memory limits/rules

---

### ❌ MODEL.md
**NOVA: 18 lines | FLUX: 19 lines | Not in NERO**

**Assessment: NO - Keep agent-specific**
- Content: Their model preferences (which LLM, parameters)
- Different per agent
- Recommendation: NO MASTER - Each agent chooses their model

---

### ❌ TASKS.md
**NOVA: 33 lines | FLUX: 33 lines | Not in NERO**

**Assessment: NO - Keep agent-specific**
- Content: Their assigned tasks and responsibilities
- Different per agent
- NOVA tasks ≠ FLUX tasks
- Recommendation: NO MASTER - Each agent has unique tasks

---

### ❌ ESCALATION.md
**NOVA: 68 lines | FLUX: 41 lines | Not in NERO**

**Assessment: PARTIALLY - Shared structure**
- Universal: Escalation paths exist for all
- Agent-specific: When/how they escalate
- Recommendation: Create ESCALATION_MASTER.md (paths/process) + agent-specific triggers
- Customization: Per-agent escalation triggers

---

### ❌ BOOTSTRAP.md
**NOVA: 55 lines | Not in FLUX | Not in NERO**

**Assessment: NO - Keep agent-specific**
- Content: Their initialization procedures
- Only NOVA has it (so far)
- Would be unique per agent
- Recommendation: NO MASTER - Each agent may have different init

---

### ❌ ALLOWLIST.md
**NOVA: 22 lines | Not in FLUX | Not in NERO**

**Assessment: NO - NOVA-specific**
- Content: NOVA's specific internet access allowlist
- Gateway-specific
- Recommendation: NO MASTER - This is NOVA only (for now)

---

### ❌ ENVIRONMENT.md
**NOVA: 21 lines | Not in FLUX | Not in NERO**

**Assessment: NO - NOVA-specific**
- Content: NOVA's environment variables
- Not needed for other agents
- Recommendation: NO MASTER - NOVA only

---

### ❌ INTERNET_USAGE.md
**NOVA: 47 lines | Not in FLUX | Not in NERO**

**Assessment: NO - NOVA-specific**
- Content: NOVA's internet usage policies
- Gateway-specific
- Recommendation: NO MASTER - NOVA only

---

### ❌ NETWORK_POLICY.md
**NOVA: 19 lines | Not in FLUX | Not in NERO**

**Assessment: NO - NOVA-specific**
- Content: NOVA's network restrictions
- Gateway-specific
- Recommendation: NO MASTER - NOVA only

---

### ❌ OPERATING_RULES.md
**NOVA: 118 lines | Not in FLUX | Not in NERO**

**Assessment: NO - NOVA-specific**
- Content: NOVA's operating constraints
- Gateway-specific
- Recommendation: NO MASTER - NOVA only

---

### ❌ DEPLOYMENT.md
**Not in NOVA | FLUX: 170 lines | Not in NERO**

**Assessment: NO - FLUX-specific**
- Content: FLUX's deployment procedures
- Orchestration-specific
- Recommendation: NO MASTER - FLUX only

---

### ❌ FILE_GOVERNANCE.md
**Not in NOVA | FLUX: 61 lines | Not in NERO**

**Assessment: NO - FLUX-specific**
- Content: FLUX's file management governance
- System-specific
- Recommendation: NO MASTER - FLUX only

---

### ❌ MEMORY_PROCESS_LOG.md
**Not in NOVA | FLUX: 141 lines | Not in NERO**

**Assessment: NO - FLUX-specific**
- Content: FLUX's memory processing logs
- Dynamic/operational
- Recommendation: NO MASTER - FLUX only

---

### ❌ OMNI_LEAD_TEMPLATE.md
**Not in NOVA | FLUX: 36 lines | Not in NERO**

**Assessment: NO - But IMPORTANT**
- Content: Template for Omni Leads
- Should be referenced by Omni Leads when created
- Recommendation: Keep in FLUX, reference from Omni Leads

---

### ❌ PROJECT_BRIEF.md
**Not in NOVA | FLUX: 99 lines | Not in NERO**

**Assessment: NO - FLUX-specific**
- Content: Current project briefing
- Dynamic/operational
- Recommendation: NO MASTER - FLUX only

---

### ❌ CANON.md
**Not in NOVA | FLUX: 2812 lines | Not in NERO**

**Assessment: NO - FLUX-specific**
- Content: System canon/documentation (HUGE!)
- This is system documentation, not agent-specific
- Recommendation: NO MASTER - FLUX only (but important reference)

---

### ❌ BUILD_BACKLOG.md
**Not in NOVA | FLUX: 0 lines | Not in NERO**

**Assessment: NO - Empty file**
- Recommendation: NO MASTER - Skip for now

---

### ❌ WEBSITE_REBUILD_STATUS.md
**Not in NOVA | FLUX: 30 lines | Not in NERO**

**Assessment: NO - FLUX-specific project status**
- Recommendation: NO MASTER - FLUX only

---

## SUMMARY: WHICH FILES SHOULD BECOME MASTER

### ✅ YES - CREATE MASTER FILES (5 files):
1. **USER_MASTER.md** - About YOU (all agents reference)
2. **HEARTBEAT_MASTER.md** - Monitoring structure (hybrid)
3. **PROTOCOL_MASTER.md** - Communication rules (hybrid)
4. **SECURITY_MASTER.md** - Security policies (hybrid)
5. **REPORTING_MASTER.md** - Reporting format (hybrid)

### 🟡 MAYBE - SHARED RULES (2 files):
6. **MEMORY_RULES_MASTER.md** - Memory governance (shared + overrides)
7. **ESCALATION_MASTER.md** - Escalation paths (shared + agent triggers)
8. **TOOLS_MASTER.md** - Tool policies (shared + agent access)

### ❌ NO - KEEP AGENT-SPECIFIC (Many files):
- IDENTITY.md (unique per agent)
- SOUL.md (unique personality per agent)
- SKILLS.md (unique per agent)
- AGENTS.md (unique relationships per agent)
- MODEL.md (unique per agent)
- TASKS.md (unique per agent)
- MEMORY.md (unique per agent)
- BOOTSTRAP.md (unique per agent)
- All NOVA-only files (ALLOWLIST, ENVIRONMENT, etc.)
- All FLUX-only files (DEPLOYMENT, CANON, etc.)

### RECOMMENDATION ORDER:
1. Start with **USER_MASTER.md** (easiest - universal content)
2. Then **HEARTBEAT_MASTER.md** (structure-based)
3. Then **PROTOCOL_MASTER.md**
4. Then **SECURITY_MASTER.md**
5. Then **REPORTING_MASTER.md**

