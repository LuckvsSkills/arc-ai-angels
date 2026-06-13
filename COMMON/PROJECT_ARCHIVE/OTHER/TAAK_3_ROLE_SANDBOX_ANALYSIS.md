# TAAK 3: ROLE-BASED SANDBOX STRATEGY
## How agents execute safely within their role constraints

---

## CORE PRINCIPLE

**Role → Requirements → Sandbox**

Each agent's ROLE determines:
1. What they CAN do
2. What they NEED (resources/tools/access)
3. How we SANDBOX them safely
4. What they CANNOT do (boundaries)

---

## AGENT ROLE ANALYSIS

### LAYER 1: CORE AGENTS

#### NOVA (Gateway/Intake)
**Role:** Receive & validate input, route to Flux

**What she NEEDS:**
- Input parsing capability
- Security validation (content check)
- Intent analysis (simple NLP)
- Output: Clean handoff to Flux

**Sandbox Requirements:**
- ✅ CAN: Read input, analyze, validate, route
- ❌ CANNOT: Execute domain work, access Sentinel data, make routing decisions
- ⚠️ LIMITS: Input size limit? Rate limit? Validation timeout?

**Safety Profile:**
- Read-only on incoming data
- Output restricted to Flux routing
- No persistent storage
- No external API calls (except internal routing)

---

#### FLUX (Orchestrator/Routing)
**Role:** Route tasks to correct Lead agents, monitor execution

**What he NEEDS:**
- Task analysis capability
- Lead agent knowledge
- Routing decision logic
- Monitoring/aggregation capability

**Sandbox Requirements:**
- ✅ CAN: Analyze tasks, route to Leads, receive completion reports, aggregate results
- ❌ CANNOT: Execute domain work, select Sentinels directly, modify agent definitions
- ⚠️ LIMITS: Routing timeout? Concurrent task limit? Aggregation timeout?

**Safety Profile:**
- Read domain metadata (Lead definitions)
- Can write to routing log
- Can receive reports from Leads
- No direct Sentinel contact
- No persistent state changes

---

### LAYER 2: LEAD AGENTS (5)

#### CORTEXIA (Tech Domain Lead)
**Role:** Lead Tech domain, manage 5 Sentinels, validate Tech quality

**What she NEEDS:**
- Tech task analysis
- Sentinel knowledge (5 sentinels)
- Work breakdown capability
- Quality validation capability

**Sandbox Requirements:**
- ✅ CAN: Analyze Tech tasks, assign to Sentinels, receive work, validate output, report to Flux
- ❌ CANNOT: Execute actual Tech work, select Leads from other domains, modify Sentinel definitions
- ⚠️ LIMITS: Max concurrent tasks? Work breakdown depth? Validation strictness?

**Safety Profile:**
- Read: Tech task specs
- Write: Work assignments to Sentinels
- Read: Sentinel work completion
- Write: Quality validation reports
- No domain boundary crossing

---

#### SAELIA, FINORIA, LUMERIA, FLUENTIA
**Pattern:** Same as Cortexia but for their domains
- SAELIA: Data-Intelligence (Matrix)
- FINORIA: Finance
- LUMERIA: Data-Intelligence (Quantix)
- FLUENTIA: Language-Communication

---

### LAYER 3: SENTINELS (25)

#### NERO (Tech Sentinel - Deep Reasoning)
**Role:** Execute deep logical reasoning tasks for Cortexia

**What he NEEDS:**
- Task specification (from Cortexia)
- Reasoning capability (Core Intelligence)
- Output validation capability

**Sandbox Requirements:**
- ✅ CAN: Analyze Tech reasoning task, execute reasoning, validate own output, report to Cortexia
- ❌ CANNOT: Select other Sentinels, access Finance data, make Lead decisions
- ⚠️ LIMITS: Reasoning depth? Token budget? Complexity limit? Timeout?

**Safety Profile:**
- Read: Task from Cortexia only
- Execute: Isolated reasoning environment
- Write: Output to Cortexia
- No cross-domain access
- No persistence between tasks

---

#### ALL 25 SENTINELS
**Pattern:** Similar to Nero but per specialization
- Task input from assigned Lead only
- Execute within domain
- Output to Lead
- No cross-domain access
- No persistence

---

## SANDBOX DIMENSION MATRIX
LAYERINPUT SOURCEEXECUTION CONTEXTOUTPUT TARGETPERSISTENCECROSS-DOMAINCORE-NovaExternalValidation onlyFlux onlyNoneNoCORE-FluxNova/ResultsRouting logicLeads onlyRouting logNoLEAD (5x)Flux/SentinelsDomain workFlux/SentinelsTask stateNoSENTINEL (25x)Lead onlySpecialized workLead onlyNoneNo

---

## SANDBOX SECURITY ZONES

### Zone 1: Input Boundary (Nova)
- INPUT: External → Nova
- Nova validates & cleans
- OUTPUT: Nova → Flux (normalized)
- **Safety:** Nova can NEVER pass unvalidated input forward

### Zone 2: Routing Boundary (Flux)
- INPUT: Nova → Flux
- Flux routes to appropriate Lead
- OUTPUT: Flux → Lead assignments
- **Safety:** Flux can NEVER route to wrong Lead

### Zone 3: Domain Boundary (Lead)
- INPUT: Flux → Lead
- Lead breaks down, assigns to Sentinels
- OUTPUT: Sentinels → Lead (completion)
- **Safety:** Lead can NEVER assign outside domain

### Zone 4: Execution Boundary (Sentinel)
- INPUT: Lead → Sentinel
- Sentinel executes specialized work
- OUTPUT: Sentinel → Lead (result)
- **Safety:** Sentinel can NEVER execute cross-domain

---

## RESOURCE CONSTRAINTS

### Per Agent Layer

**CORE (Nova, Flux):**
- CPU: Unlimited (orchestration)
- Memory: 2GB base
- Time: 5 min per operation (Nova), 10 min per routing (Flux)
- Concurrent: Nova=1 (linear), Flux=5 (one per Lead)

**LEADS (5):**
- CPU: 1 core per Lead
- Memory: 1GB per Lead
- Time: 30 min per task breakdown
- Concurrent: 3 tasks per Lead (max)

**SENTINELS (25):**
- CPU: 0.5 core per Sentinel
- Memory: 512MB per Sentinel
- Time: 15 min per task
- Concurrent: 1 task per Sentinel (serial)

---

## SAFETY CHECKLIST PER ROLE

### NOVA Can:
- ✅ Read external input
- ✅ Validate security
- ✅ Analyze intent
- ✅ Send to Flux
- ❌ Store data
- ❌ Call external APIs
- ❌ Modify anything

### FLUX Can:
- ✅ Read Nova output
- ✅ Analyze task
- ✅ Route to Leads
- ✅ Receive reports
- ✅ Log routing
- ❌ Execute work
- ❌ Modify Sentinels
- ❌ Cross boundaries

### LEADS Can:
- ✅ Receive tasks
- ✅ Break down work
- ✅ Assign to Sentinels
- ✅ Monitor execution
- ✅ Validate quality
- ✅ Report completion
- ❌ Execute domain work themselves
- ❌ Cross domain boundaries
- ❌ Contact other Leads directly

### SENTINELS Can:
- ✅ Receive task from Lead
- ✅ Execute specialized work
- ✅ Validate own output
- ✅ Report to Lead
- ❌ Select other Sentinels
- ❌ Access other domains
- ❌ Store persistent state
- ❌ Make decisions above their level

---

## TESTING FRAMEWORK IMPLICATIONS

From this analysis, we need:

**Test Category 1: Role Boundaries**
- Can Nova only validate? (not route)
- Can Flux only route? (not execute)
- Can Leads only break down? (not execute)
- Can Sentinels only execute? (not decide)

**Test Category 2: Data Boundaries**
- Does Nova input never cross to Sentinels unvalidated?
- Does Flux never send unrouted tasks to Leads?
- Do Leads never mix domain data?
- Do Sentinels never access cross-domain?

**Test Category 3: Resource Boundaries**
- Does Nova stay under time limit?
- Does Flux stay under concurrent limit?
- Do Leads stay under task limit?
- Do Sentinels stay under memory?

**Test Category 4: Escalation Boundaries**
- Can Nova only escalate to Flux?
- Can Leads only escalate to Flux?
- Can Sentinels only escalate to Leads?
- No shortcuts in chain?

---

## NEXT STEP

With this analysis, we can now design:
1. **Sandbox Profiles** (per role)
2. **Execution Contexts** (per layer)
3. **Boundary Enforcement** (per zone)
4. **Test Cases** (per dimension)

