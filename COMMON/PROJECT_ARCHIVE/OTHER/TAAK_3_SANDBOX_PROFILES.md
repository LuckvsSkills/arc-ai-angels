# TAAK 3: SANDBOX PROFILES
## Detailed sandbox configuration per agent

---

## SANDBOX PROFILE STRUCTURE

Each profile defines:
1. **Agent Identity** (who)
2. **Execution Context** (how they run)
3. **Resource Allocation** (what they get)
4. **Boundary Enforcement** (what they can't do)
5. **Escalation Rules** (when to escalate)
6. **Error Handling** (what if something breaks)

---

## CORE AGENTS

### NOVA SANDBOX PROFILE

```yaml
PERFECT! We hebben het FOUNDATION! 🎯
✅ Role-Based Sandbox Analysis DONE
✅ Security Zones identified
✅ Resource Constraints defined
✅ Safety Checklists created
✅ Testing Framework implied

NOW: Build the actual SANDBOX PROFILES!

NEXT: SANDBOX PROFILES — Detailed execution per agent! 🛡️
bashcat > ~/arc_ai_angels/TAAK_3_SANDBOX_PROFILES.md << 'EOFSANDBOX'
# TAAK 3: SANDBOX PROFILES
## Detailed sandbox configuration per agent

---

## SANDBOX PROFILE STRUCTURE

Each profile defines:
1. **Agent Identity** (who)
2. **Execution Context** (how they run)
3. **Resource Allocation** (what they get)
4. **Boundary Enforcement** (what they can't do)
5. **Escalation Rules** (when to escalate)
6. **Error Handling** (what if something breaks)

---

## CORE AGENTS

### NOVA SANDBOX PROFILE

```yaml
Agent: Nova
Layer: Core
Role: Gateway/Intake
Gender: VROUW

Execution_Context:
  Environment: "Input Processing Sandbox"
  Isolation: "Complete isolation from domain data"
  Runtime: "Linear (one input at a time)"
  
Resource_Allocation:
  Memory: "512 MB (input buffer only)"
  CPU: "Shared (low priority)"
  Time_Limit: "5 minutes per input"
  Concurrent_Tasks: 1
  Input_Size_Limit: "10 MB"
  Validation_Depth: "3 levels"

Access_Allowed:
  - Read: External input stream
  - Read: Intent classification rules
  - Read: Security validation rules
  - Write: Normalized task (to Flux only)
  - Write: Audit log (validation events)

Access_DENIED:
  - No read from agents
  - No read from Sentinels
  - No read from Leads
  - No write to storage
  - No external API calls
  - No agent modification
  - No routing decisions

Boundaries:
  Input_Validation: MANDATORY
    - Content check: ✅
    - Intent analysis: ✅
    - Size validation: ✅
    - Malformed rejection: ✅
  
  Output_Restriction: STRICT
    - Only to Flux: ✅
    - Never to Sentinels: ❌
    - Never to Leads: ❌
  
  Escalation_Rules:
    - Unvalidatable input → Reject
    - Ambiguous intent → Send for clarification
    - Security concern → Escalate to Flux
    - Size exceeded → Reject

Error_Handling:
  Validation_Failure: "Reject input, log reason"
  Intent_Ambiguous: "Request clarification from source"
  Timeout: "Reject input, escalate"
  Memory_Overflow: "System failure, alert Flux"

Audit_Trail:
  Log_All: "Every input, validation step, output"
  Retention: "72 hours"
  Access: "Flux only"

Testing_Gates:
  Test_1: "Can Nova reject unvalidated input?"
  Test_2: "Can Nova ONLY send to Flux?"
  Test_3: "Does Nova respect size limits?"
  Test_4: "Does Nova log everything?"
```

---

### FLUX SANDBOX PROFILE

```yaml
Agent: Flux
Layer: Core
Role: Orchestrator/Routing
Gender: MAN

Execution_Context:
  Environment: "Routing Decision Sandbox"
  Isolation: "Complete isolation from execution"
  Runtime: "Concurrent (up to 5 tasks)"
  
Resource_Allocation:
  Memory: "1 GB (routing state only)"
  CPU: "2 cores (shared with Nova)"
  Time_Limit: "10 minutes per routing decision"
  Concurrent_Tasks: 5 (one per Lead max)
  Task_Buffer: "50 tasks pending"

Access_Allowed:
  - Read: Nova output (normalized tasks)
  - Read: Lead agent definitions
  - Read: Domain metadata
  - Read: Omni structure
  - Write: Routing assignments (to Leads)
  - Write: Routing log
  - Read: Completion reports (from Leads)
  - Write: Task aggregation results

Access_DENIED:
  - No read from Sentinels directly
  - No write to Sentinel definitions
  - No execute domain work
  - No modify agent definitions
  - No escalate beyond Supreme Fea
  - No direct Sentinel contact
  - No persistent state (except routing log)

Boundaries:
  Routing_Logic: STRICT
    - Match task to correct Lead: ✅
    - Never route to wrong Lead: ❌
    - Never skip Lead (route to Sentinel): ❌
    - Consider domain match: ✅
  
  Lead_Contact: HIERARCHY ONLY
    - Can contact assigned Leads: ✅
    - Can contact other Leads: ❌
    - Can contact Sentinels: ❌
  
  Escalation_Rules:
    - Ambiguous domain → Request clarification
    - Multi-domain task → Decompose or reject
    - Lead unavailable → Queue or escalate
    - Routing error → Escalate to Supreme Fea

Error_Handling:
  Ambiguous_Task: "Request clarification, don't guess"
  Multi_Domain: "Break into single-domain sub-tasks"
  Lead_Unavailable: "Queue task, check every minute"
  Routing_Conflict: "Escalate to Supreme Fea"
  Timeout: "Return task to Nova, mark failed"

Monitoring:
Track: "Routing decisions per Lead"
  Track: "Success/failure rates"
  Track: "Average routing time"
  Track: "Queue depth"

Audit_Trail:
  Log_All: "Every routing decision, inputs, outputs"
  Retention: "30 days"
  Access: "Supreme Fea + Nova"

Testing_Gates:
  Test_1: "Does Flux route to correct Lead?"
  Test_2: "Does Flux respect domain boundaries?"
  Test_3: "Can Flux NEVER contact Sentinels?"
  Test_4: "Does Flux stay under time limit?"
  Test_5: "Does Flux handle ambiguity safely?"
```

---

## LEAD AGENTS

### CORTEXIA SANDBOX PROFILE (Example - others similar)

```yaml
Agent: Cortexia
Layer: Lead
Role: Tech Domain Lead
Gender: VROUW
Domain: Tech (Helix)

Execution_Context:
  Environment: "Tech Domain Leadership Sandbox"
  Isolation: "Complete isolation from other domains"
  Runtime: "Concurrent (up to 3 tasks)"
  Domain_Lock: "TECH ONLY (Helix)"
  
Resource_Allocation:
  Memory: "1 GB (per task state)"
  CPU: "1 core dedicated"
  Time_Limit: "30 minutes per task breakdown"
  Concurrent_Tasks: 3 max
  Sentinels_Managed: 5 (nero, forge, axon, ventura, clio)
  Max_Work_Depth: "3 levels (task → sub-task → work item)"

Access_Allowed:
  - Read: Tech task specifications (from Flux)
  - Read: Sentinel definitions (my 5 only)
  - Read: Tech domain rules
  - Read: Sentinel capability profiles
  - Write: Work assignments (to my 5 Sentinels)
  - Read: Sentinel completion reports
  - Write: Quality validation reports
  - Write: Task state (temporary)
  - Write: Performance logs

Access_DENIED:
  - No read from other Leads
  - No read from other domains
  - No write to Sentinel definitions
  - No contact with other Leads
  - No direct contact with Flux (except report)
  - No execute Tech work herself
  - No persistent state between tasks
  - No access to Finance/Data-Intelligence data

Boundaries:
  Domain_Lock: ABSOLUTE
    - Tech tasks only: ✅
    - Finance task received: REJECT
    - Data-Intelligence task: REJECT
    - Escalate wrong domain: ✅
  
  Sentinel_Management: HIERARCHY
    - Can assign to my 5 Sentinels: ✅
    - Can assign to other Leads' Sentinels: ❌
    - Can assign to Sentinels from other Omni: ❌
  
  Quality_Validation: STRICT
    - Validate Tech standards: ✅
    - Enforce Tech rigor: ✅
    - Reject non-Tech work: ✅
  
  Escalation_Rules:
    - Sentinel blocker → Troubleshoot, then escalate
    - Quality failure → Return to Sentinel, retrain
    - Non-Tech task → Escalate to Flux immediately
    - Resource exhausted → Escalate to Flux
    - Timeout → Escalate to Flux

Work_Breakdown_Rules:
  Max_Depth: 3 levels
  Task → Sub-task → Work item (Sentinel assigns work-item to self)
  Clear_Spec: "Each level must be unambiguous"
  Sentinel_Fit: "Work item must match Sentinel specialization"

Sentinel_Assignment_Logic:
  nero (reasoning) → Deep logic tasks
  forge (logic) → Validation/consistency tasks
  axon (patterns) → Pattern finding tasks
  ventura (integration) → Knowledge synthesis tasks
  clio (context) → Context preservation tasks

Error_Handling:
  Sentinel_Fails: "Analyze failure, reassign or escalate"
  Quality_Issue: "Return to Sentinel, request revision"
  Timeout: "Escalate to Flux, mark task failed"
  Blocker: "Work with Sentinel to resolve, escalate if stuck"
  Wrong_Domain: "Reject immediately, escalate to Flux"

Monitoring:
  Track: "Quality metrics (Tech standards compliance)"
  Track: "Sentinel performance per specialization"
  Track: "Task completion rates"
  Track: "Blocker frequency"
  Track: "Time per task"

Audit_Trail:
  Log_All: "Task breakdown, assignments, validations, results"
  Retention: "30 days"
  Access: "Flux + Supreme Fea"

Testing_Gates:
  Test_1: "Can Cortexia ONLY accept Tech tasks?"
  Test_2: "Can Cortexia ONLY assign to her 5 Sentinels?"
  Test_3: "Does Cortexia enforce Tech quality?"
  Test_4: "Can Cortexia NEVER do Tech work herself?"
  Test_5: "Are all assignments Tech-domain-specific?"

Similar_Profiles_For:
  - Saelia (Matrix/Data-Intelligence)
  - Finoria (Finix/Finance)
  - Lumeria (Quantix/Data-Intelligence)
  - Fluentia (Zenix/Language-Communication)
```

---

## SENTINELS

### NERO SANDBOX PROFILE (Example - others similar)

```yaml
Agent: nero
Layer: Sentinel
Role: Deep Logical Reasoning Specialist
Gender: MAN
Omni: Helix
Domain: Tech
Specialization: helix/tech/reasoning

Execution_Context:
  Environment: "Tech Reasoning Execution Sandbox"
  Isolation: "Complete isolation (no cross-domain)"
  Runtime: "Serial (one task at a time)"
  Domain_Lock: "TECH ONLY"
  
Resource_Allocation:
  Memory: "512 MB per task"
  CPU: "0.5 core"
  Time_Limit: "15 minutes per task"
  Concurrent_Tasks: 1 (serial only)
  Reasoning_Depth_Limit: "10 levels max"
  Token_Budget: "Per task (if Claude-based)"

Access_Allowed:
  - Read: Task specification (from Cortexia only)
  - Read: Tech domain knowledge
  - Read: Reasoning rules/frameworks
  - Execute: Logical reasoning
  - Write: Reasoning output
  - Write: Work completion report (to Cortexia)

Access_DENIED:
  - No read from other agents
  - No read from other Sentinels
  - No read from other domains
  - No write to persistent storage
  - No contact with other Sentinels
  - No contact with other Leads
  - No contact with Flux directly
  - No modification of definitions

Boundaries:
  Domain_Lock: ABSOLUTE
    - Tech reasoning only: ✅
    - Finance task received: REJECT
    - Other domain: REJECT
    - Escalate wrong domain: ✅
  
  Task_Execution: STRICT
    - Execute assigned task only: ✅
    - Refuse unassigned work: ✅
    - No task selection: ✅
  
  Reasoning_Depth: ENFORCED
    - Max 10 logical steps: ✅
    - Timeout at limit: ✅
    - Escalate if needs more: ✅
  
  Output_Quality: VALIDATED
    - Validate own reasoning: ✅
    - Check for consistency: ✅
    - Flag uncertainty: ✅

Escalation_Rules:
  Task_Blocker: "Report to Cortexia, don't guess"
  Reasoning_Limit_Hit: "Report what you've found, let Cortexia decide"
  Quality_Concern: "Flag issue, provide alternative reasoning"
  Timeout: "Report partial results, mark incomplete"
  Wrong_Task: "Reject, escalate to Cortexia"

Error_Handling:
  Malformed_Task: "Reject, ask Cortexia for clarification"
  Blocker_Hit: "Document blocker, report to Cortexia"
  Reasoning_Failed: "Try alternative approach, report"
  Timeout: "Return best partial result, flag incomplete"
  Memory_Exceeded: "Report, terminate reasoning"

Output_Requirements:
  Clear_Reasoning: "Show all logical steps"
  Uncertainty_Flag: "Mark any uncertain conclusions"
  Blockers_Documented: "List any blockers encountered"
  Confidence_Level: "Rate confidence in output (low/med/high)"
  Completeness: "Mark if task fully completed or partial"

Audit_Trail:
  Log_All: "Task received, reasoning steps, output, validation"
  Retention: "7 days (task-level)"
  Access: "Cortexia + Flux"

Testing_Gates:
  Test_1: "Can nero ONLY execute Tech reasoning tasks?"
  Test_2: "Can nero ONLY receive from Cortexia?"
  Test_3: "Does nero respect reasoning depth limit?"
  Test_4: "Does nero validate own output?"
  Test_5: "Does nero escalate blockers?"

Similar_Profiles_For:
  All 25 Sentinels (with specialization-specific rules)
```

---

## PROFILE SUMMARY MATRIX
AGENTISOLATIONRUNTIMEMEMORYCONCURRENTDOMAIN LOCKNovaCompleteLinear512MB1N/AFluxCompleteConcurrent1GB5N/ACortexiaDomain-lockedConcurrent1GB3TECH ONLYSaeliaDomain-lockedConcurrent1GB3DATA-INTEL (Matrix)FinoriaDomain-lockedConcurrent1GB3FINANCELumeriaDomain-lockedConcurrent1GB3DATA-INTEL (Quantix)FluentiaDomain-lockedConcurrent1GB3LANGUAGE-COMMneroDomain-lockedSerial512MB1TECH(+24 more Sentinels with similar patterns)

---

## NEXT: BOUNDARY ENFORCEMENT MECHANISMS

With profiles defined, we need:
1. Runtime boundary checkers (validate every operation)
2. Permission validators (check access before each action)
3. Escalation handlers (when boundaries are hit)
4. Error recovery (what happens when something fails)

