# Agent .md File Structure & Requirements

## FILE CATEGORIES

### TIER 1: UNIVERSAL FILES (All agents must have)
Every agent MUST have these 6 files:
- ✅ IDENTITY.md (Role, Mission, Cognitive Style)
- ✅ SOUL.md (Principles, Behavior, Responsibility)
- ✅ TOOLS.md (Policy, Allowed, Forbidden)
- ✅ USER.md (User interaction rules)
- ✅ HEARTBEAT.md (Status monitoring)
- ✅ AGENTS.md (Agent relationships)

### TIER 2: ADVANCED FILES (Core agents + specialists)
Add these if needed:
- MEMORY.md (Memory structure)
- MEMORY_RULES.md (Memory governance)
- BOOTSTRAP.md (Initialization)
- PROTOCOL.md (Communication protocol)
- SKILLS.md (Agent capabilities)
- MODEL.md (Model preferences)
- TASKS.md (Task definitions)
- SECURITY.md (Security rules)
- REPORTING.md (Reporting format)
- ESCALATION.md (Escalation rules)

### TIER 3: SPECIALIZED (Only for specific agents)
- NOVA: ALLOWLIST.md, ENVIRONMENT.md, INTERNET_USAGE.md, NETWORK_POLICY.md, OPERATING_RULES.md
- FLUX: BUILD_BACKLOG.md, CANON.md, DEPLOYMENT.md, FILE_GOVERNANCE.md, MEMORY_PROCESS_LOG.md, OMNI_LEAD_TEMPLATE.md, PROJECT_BRIEF.md

## AGENT TYPES & REQUIRED FILES

### TYPE 1: SENTINELS (25 agents)
**Baseline: 6 files**
- IDENTITY.md
- SOUL.md
- TOOLS.md
- USER.md
- HEARTBEAT.md
- AGENTS.md

**Optional additions:**
- MEMORY.md (if learning required)
- BOOTSTRAP.md (if special init needed)
- SKILLS.md (if specialized skills)

### TYPE 2: OMNI LEADS (5 agents)
**Baseline: 6 files + OMNI specific**
- IDENTITY.md (Role = Domain Lead)
- SOUL.md (Leadership principles)
- TOOLS.md (Domain coordination tools)
- USER.md (Team interaction)
- HEARTBEAT.md (Team health)
- AGENTS.md (Sentinel team roster)

**Required additions:**
- PROTOCOL.md (Team coordination)
- SKILLS.md (Domain expertise)
- TASKS.md (Team task distribution)

### TYPE 3: CORE AGENTS (Nova, Flux)
**Baseline: 6 files + Core specific**
- All universal files
- Plus 10+ specialized files per agent

## TONE/VIBE PATTERNS

### NOVA VIBE (Female/Assertive)
From NOVA/SOUL.md:
- scherp (sharp)
- compact (concise)
- filterend (filtering)
- oplossingsgericht (solution-focused)
- assertief (assertive)

### FLUX VIBE (Male/Systematic)
From FLUX/SOUL.md:
- systemisch (systematic)
- analytisch (analytical)
- besluitgericht (decisive)
- governance-aware
- hiërarchisch disciplinair (hierarchically disciplined)

## GENDER DISTRIBUTION

**FEMALE AGENTS (Nova vibe):**
- clio (Context preservation)
- luvia (Flow/Insight)
- kresta (Pattern extraction)
- elora (Data synthesis)
- vondra (Metrics tracking)
- zena (Output formatting)
- unia (Interface specialist)
- solis (Translation specialist)

**MALE AGENTS (Flux vibe):**
- nero (Reasoning)
- forge (Logic)
- axon (Pattern recognition)
- ventura (Knowledge integration)
- kairo (Structure analysis)
- kenzo (Planning)
- odis (Sequence management)
- vector (Flow analysis)
- zion (Integration)
- arix (Technical execution)
- daxio (Optimization)
- enki (System design)
- sora (Implementation)
- tharos (Quality assurance)
- draven (Communication)
- orizon (Adaptation)
- nura (Analytics)

**OMNI LEADS (Leaders):**
- cortexia (HELIX - Female vibes)
- saelia (SAELIA - Female vibes)
- finoria (FINORIA - Female vibes)
- lumeria (QUANTIX - Female vibes)
- fluentia (ZENIX - Female vibes)

## NEXT STEPS

1. Create TONE_FEMALE_TEMPLATE.md (based on NOVA)
2. Create TONE_MALE_TEMPLATE.md (based on FLUX)
3. Create IDENTITY_UNIVERSAL_TEMPLATE.md
4. Create SOUL_UNIVERSAL_TEMPLATE.md
5. Create TOOLS_UNIVERSAL_TEMPLATE.md
6. Fill empty Omni Leads
7. Verify all Sentinels have 6+ files
8. Build rollout automation script

