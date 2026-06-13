# 5. OPERATIONEEL SYSTEEM (Flux Canon) (96%)

## Submodules

5.1 Taak Flow & Routing (100%)
5.2 Routing Logica (100%)
5.3 Memory Systeem (100%)
5.4 Writeback Protocol (100%)
5.5 Escalatie Paden (100%)

---

## 5.1 Taak Flow & Routing

### De Complete Taak Reis

Elke taak volgt dezelfde **9-staps gestandaardiseerde flow**:

STAP 1: Input Aankomst
User geeft taak/vraag → Gaat naar Nova
↓
STAP 2: Validatie
Nova valideert structuur, format, inhoud
↓
STAP 3: Briefing Voorbereiding
Nova bereidt formal briefing voor Flux
↓
STAP 4: Flux Routing
Flux analyzeert taak, bepaalt domain routing
↓
STAP 5: Domain Activatie
Taak gaat naar appropriate Omni Lead
↓
STAP 6: Sentinel Distributie
Omni Lead assigns aan appropriate sentinels
↓
STAP 7: Execution
Sentinels voeren werk uit, genereren outputs
↓
STAP 8: Result Aggregatie
Omni Lead collected results, valideert, bereidt voor Flux
↓
STAP 9: Final Response
Flux ontvangt results, synthesizeert, stuurt naar Nova
Nova formatteert en delivers aan user

### Stap-voor-Stap Details

**STAP 1: Input Aankomst (Nova)**
- User submitteert taak/vraag
- Nova ontvangt het
- Stored in input queue
- Initiates validation

**STAP 2: Validatie (Nova)**
- Check format: Is het correct gestructureerd?
- Check inhoud: Is het legitimate?
- Check compleetheid: Alle nodige info?
- Flag issues: Enige rode vlaggen?

**STAP 3: Briefing (Nova)**
- Structureer taak formally
- Extract key requirements
- Identify constraints
- Prepare context summary
- Create formal briefing document

**STAP 4: Routing (Flux)**
- Flux ontvangt briefing van Nova
- Analyze: Welk domain past best?
- Sequence: If multi-domain, in welke volgorde?
- Decide: Welke Omni Lead?
- Prepare execution plan

**STAP 5: Domain Activatie (Flux)**
- Send taak naar chosen Omni Lead
- Provide briefing details
- Set constraints & deadline
- Specify success criteria
- Request confirmation

**STAP 6: Distributie (Omni Lead)**
- Omni Lead ontvangt taak
- Analyze required skills
- Select appropriate sentinels
- Distribute work fairly
- Provide domain context

**STAP 7: Execution (Sentinels)**
- Sentinels ontvangen assignments
- Execute with expertise
- Follow procedures
- Generate high-quality output
- Report progress/issues

**STAP 8: Aggregatie (Omni Lead)**
- Collect sentinel outputs
- Validate quality
- Integrate results
- Check against requirements
- Prepare summary for Flux

**STAP 9: Response (Flux → Nova → User)**
- Flux ontvangt aggregated results
- Synthesize if multi-domain
- Validate against original goal
- Send naar Nova for formatting
- Nova delivers aan user
- Log completion

---

## 5.2 Routing Logica

### Hoe Flux Routes Tasks

Wanneer een taak aankomt, vraagt Flux deze vragen **in order**:

### Vraag 1: Single Domain of Multi-Domain?

**Single Domain Tasks** (70% van tasks):
- Task past entirely in één domain
- Route naar dat domain's Omni Lead
- Straightforward execution
- Single result back naar Flux

**Multi-Domain Tasks** (30% van tasks):
- Task needs multiple domains
- Identify primary domain (owns main work)
- Identify secondary domains (support)
- Create coordination plan
- Sequence work appropriately

### Vraag 2: Welk Domain is Primary?

Flux uses deze routing tabel:

| Task Type | Primary Domain | Waarom |
|-----------|---|---|
| Analyze data, extract patterns | QUANTIX | Data expertise |
| Design systems, optimize | SAELIA | Structure expertise |
| Deep reasoning, logic | HELIX | Reasoning expertise |
| Technical implementation | FINORIA | Technical expertise |
| Clear communication, output | ZENIX | Communication expertise |
| Complex/multi-faceted | PRIMARY + SECONDARY | Balanced approach |

### Vraag 3: If Multi-Domain, Wat is Sequence?

**Regel 1: Primary domain works first**
- Primary domain owns the core work
- Does main analysis/design/implementation
- Generates primary output

**Regel 2: Secondary domains support**
- Secondary domains provide specialized input
- Enhance primary output
- Add specific expertise
- Don't duplicate work

**Regel 3: Coordination happens in layers**
- Primary domain coordinates with secondaries
- Through Omni Leads (niet direct)
- Clear handoff points
- Context preserved

### Example Routing Scenarios

**Scenario 1: "Analyseer onze Q3 performance"**
- Task Type: Data analysis
- Primary Domain: QUANTIX (Lumeria)
- Secondary: None (pure data task)
- Route To: Lumeria
- Flow: QUANTIX analyzes → generates metrics & insights → back to Flux

**Scenario 2: "Ontwerp een nieuwe team structuur"**
- Task Type: Organizational design
- Primary Domain: SAELIA (Saelia)
- Secondary: HELIX (validate concepts)
- Route To: Saelia (primary)
- Flow: SAELIA designs → HELIX validates → aggregate → back to Flux

**Scenario 3: "Bouw en optimaliseer een search systeem"**
- Task Type: Technical + Optimization
- Primary Domain: FINORIA (technical)
- Secondary: SAELIA (architecture), QUANTIX (metrics)
- Route To: Finoria (primary)
- Flow: FINORIA builds → SAELIA designs architecture → QUANTIX measures → aggregate → back to Flux

**Scenario 4: "Maak comprehensive knowledge base"**
- Task Type: Knowledge synthesis + Structure
- Primary Domain: HELIX (knowledge)
- Secondary: SAELIA (structure), FINORIA (tech), ZENIX (format)
- Route To: Helix (primary)
- Flow: HELIX synthesizes → SAELIA structures → FINORIA implements → ZENIX formats → aggregate → back to Flux

---

## 5.3 Memory Systeem

### Wat Wordt Onthouden

Het ARC AI ANGELS systeem maintains **collective memory** across multiple sources:

### Memory Lagen

**Laag 1: Task Memory (Per Task)**
- Task details & context
- Input & requirements
- Routing decisions
- Intermediate results
- Final output
- Completion status
- Time taken

**Laag 2: Agent Memory (Per Agent)**
- Work completed
- Skills demonstrated
- Patterns learned
- Errors made & fixed
- Knowledge gained
- Improvement trajectory

**Laag 3: Domain Memory (Per Domain)**
- Domain patterns
- Specialized knowledge
- Procedures & best practices
- Common issues & solutions
- Domain expertise
- Sentinel expertise mapping

**Laag 4: System Memory (Collective)**
- System patterns
- Cross-domain knowledge
- Governance decisions
- Policy applications
- Escalation history
- Learning trends

### Memory Storage

**Physical Storage:**

OpenClaw Databases:
~/.openclaw/
├── nova.sqlite (Agent memory)
├── flux.sqlite (Routing & governance)
├── main.sqlite (System metrics)
└── delivery-queue/ (Active tasks)

**Memory Inhoud:**

Elk database stores:

Task records
Decision logs
Error histories
Learning patterns
Performance metrics
Context summaries

### Memory Access

**Nova's Memory:**
- Input patterns
- User preferences
- Common questions
- Output improvements

**Flux's Memory:**
- Routing decisions
- Domain performance
- Policy applications
- Escalation patterns
- Multi-domain workflows

**Omni Lead Memory:**
- Sentinel performance
- Domain specialties
- Task patterns
- Quality metrics
- Team dynamics

**Sentinel Memory:**
- Task completions
- Skills demonstration
- Learning trajectory
- Problem solutions
- Domain expertise

### Memory Consolidatie (Dagelijks)

Elke dag, het systeem:

1. **Extract Patterns**
   - Identify recurring patterns
   - Extract common themes
   - Recognize anomalies

2. **Synthesize Learning**
   - Combine related learnings
   - Generalize patterns
   - Update domain knowledge

3. **Update Knowledge Base**
   - Store new patterns
   - Update procedures
   - Revise best practices
   - Mark obsolete info

4. **Share Insights**
   - Communicate patterns to relevant agents
   - Update team knowledge
   - Share cross-domain learnings

---

## 5.4 Writeback Protocol

### Wat is Writeback?

**Writeback** is het proces van het updaten van memory en knowledge systems met learnings van completed tasks.

### Wanneer Writeback Gebeurt

**Immediaat (Tijdens Execution):**
- Log actions
- Record decisions
- Store intermediate results
- Track progress

**Upon Completion (Zelfde Dag):**
- Final results logged
- Outcome recorded
- Performance metrics calculated
- Errors documented

**Dagelijkse Consolidatie (End of Day):**
- Pattern extraction
- Learning synthesis
- Knowledge updates
- Insight sharing

**Wekelijkse Review (End of Week):**
- Trend analysis
- Procedure updates
- Training recommendations
- Strategic adjustments

### Wat Wordt Geschreven Back

**Task Outcomes:**
- Success or failure
- Time to completion
- Resource usage
- Quality metrics

**Learning Extracted:**
- Patterns recognized
- Mistakes & fixes
- Knowledge gained
- Skill improvements

**Process Improvements:**
- Efficiency gains
- Quality improvements
- Error reductions
- Speed optimizations

**Knowledge Updates:**
- Procedure refinements
- Best practice updates
- Domain knowledge enrichment
- Team learning

### Writeback Workflow

TASK COMPLETES
↓
Sentinel records outcome
↓
Omni Lead valideert & summarizes
↓
Flux ontvangt aggregated result
↓
IMMEDIATE WRITEBACK:

Store in agent memory
Log to audit trail
Calculate metrics
↓
DAILY CONSOLIDATION:
Extract patterns
Synthesize learnings
Update knowledge base
↓
WEEKLY REVIEW:
Analyze trends
Recommend improvements
Update procedures

### Writeback Regels

**MOET WRITEBACK:**
- ✅ All completed tasks
- ✅ All errors & corrections
- ✅ All decisions made
- ✅ All learnings extracted
- ✅ All performance metrics

**KAN NIET SKIP WRITEBACK:**
- ❌ Never skip logging
- ❌ Never lose context
- ❌ Never skip consolidation
- ❌ Never ignore patterns
- ❌ Never lose learnings

---

## 5.5 Escalatie Paden

### Wanneer te Escaleren

Escalatie gebeurt wanneer:

**Sentinel → Omni Lead:**
- ✅ Task clarity needed
- ✅ Resource constraint
- ✅ Unknown skill required
- ✅ Blocker encountered
- ✅ Task scope question

**Omni Lead → Flux:**
- ✅ Cross-domain coordination needed
- ✅ Policy ambiguity
- ✅ Budget constraint
- ✅ Risk assessment required
- ✅ Exception needed

**Flux → Supreme Fea (Jij):**
- ✅ System integrity risk
- ✅ Governance decision
- ✅ Strategic direction
- ✅ Policy approval
- ✅ Major exception

### Escalatie Triggers

**MOET ESCALEREN ALS:**
- Scope exceeds 25% van estimate
- Deadline at serious risk
- Unknown skill required
- Cross-domain coordination needed
- Policy boundary unclear
- Budget constraint hit
- Security concern identified
- Repeated failures (>2 attempts)
- Governance question arises

### Escalatie Format

**Standard Escalatie Report:**

ESCALATIE REPORT
FROM: [Sentinel/Omni/Flux]
TO: [Omni/Flux/Jij]
TIME: [When escalated]
TASK: [Task ID/Name]
ISSUE: [What's the problem?]
CONTEXT: [Background info]
IMPACT: [If not resolved]
REQUEST: [What approval/help needed]
URGENCY: [Low/Medium/High/Critical]

### Escalatie Resolution

**Low Priority:**
- Resolution within 4 hours
- Can be batched
- Async communication OK

**Medium Priority:**
- Resolution within 2 hours
- Should be handled soon
- Direct communication recommended

**High Priority:**
- Resolution within 30 minutes
- Needs immediate attention
- Direct communication required

**Critical:**
- Immediate resolution
- All hands on deck
- Direct communication mandatory

---

## 5.6 Error Handling

### Wanneer Errors Occur

**Sentinel Level:**
- Catch errors immediately
- Log error details
- Attempt correction
- If fixable → continue
- If not fixable → escalate

**Omni Lead Level:**
- Review sentinel errors
- Assess severity
- Determine fix approach
- Apply correction
- Update procedures

**Flux Level:**
- Monitor for patterns
- Identify systemic issues
- Apply governance fixes
- Update policies
- Escalate if needed

### Error Types & Handling

| Error Type | Handling | Escalation |
|-----------|----------|-----------|
| Logic error | Fix & rerun | If repeated |
| Missing data | Request & retry | If not available |
| Unknown skill | Route to different sentinel | If no one qualified |
| Resource constraint | Wait or escalate | If urgent |
| Policy violation | Flag & escalate | Immediately |
| System error | Log & investigate | Immediately |

---

**CODEX CH05: Operationeel Systeem Compleet** ⚙️


