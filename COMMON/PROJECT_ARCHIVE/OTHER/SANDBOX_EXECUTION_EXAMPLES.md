# SANDBOX EXECUTION — CONCRETE EXAMPLES
## Hoe sandboxing in praktijk werkt per agent

---

## VOORBEELD 1: NOVA (STRICT SANDBOX)

### Scenario: Externa input arriveert
STAP 1: INPUT ARRIVES
├─ Source: External user
├─ Message: "Analyze this financial report"
├─ Size: 2 MB
└─ Content: Contains potentially malicious code
STAP 2: PERMISSION CHECK (Layer 1)
├─ Check: Is Nova allowed to READ external input?
├─ Profile: NOVA_SANDBOX_PROFILE
├─ Access_Allowed: YES (Read external input stream)
└─ Decision: ALLOW → Continue
STAP 3: RESOURCE CHECK (Layer 2)
├─ Check: Does Nova have resources?
├─ Memory limit: 512 MB
├─ Memory available: 450 MB
├─ Time limit: 5 minutes
├─ Time available: 4:50 remaining
└─ Decision: ALLOW → Continue
STAP 4: BOUNDARY CHECK (Layer 3)
├─ Check 1: Is input size < 10 MB limit?
│  └─ 2 MB < 10 MB? YES ✅
├─ Check 2: Can Nova validate this?
│  └─ Validation depth 3 levels? YES ✅
├─ Check 3: Security scanning possible?
│  └─ Malware check? YES ✅
└─ Decision: ALLOW → Continue
STAP 5: EXECUTION
├─ Nova starts input parsing
├─ Security validation: RUNS
├─ Content check: RUNS
├─ Intent analysis: RUNS
├─ All checks pass ✅
└─ Output: Normalized task object
STAP 6: OUTPUT CHECK (Layer 1 again)
├─ Check: Can Nova WRITE to Flux?
├─ Access_Allowed: YES (Write to Flux only)
├─ Target is Flux? YES ✅
├─ Is output validated? YES ✅
└─ Decision: ALLOW → Send to Flux
STAP 7: AUDIT & LOG
├─ Log: "Nova received external input"
├─ Log: "Security validation PASSED"
├─ Log: "Task routed to Flux: [task_id]"
├─ Timestamp: 2026-05-25 10:15:42
└─ Retention: 72 hours
RESULT: ✅ INPUT SAFE & PROCESSED

---

## VOORBEELD 2: NOVA (VIOLATION ATTEMPT)

### Scenario: Nova tries to bypass security
STAP 1: NOVA WANTS TO
├─ Operation: "Write directly to Cortexia (skip Flux)"
├─ Reason: "Task is clearly Tech, let's shortcut"
└─ Intent: Bypass Flux routing
STAP 2: PERMISSION CHECK (Layer 1)
├─ Check: Is Nova allowed to WRITE to Cortexia?
├─ Profile: NOVA_SANDBOX_PROFILE
├─ Access_Allowed:
│  ├─ Write to Flux? YES
│  ├─ Write to Cortexia? NO ❌
│  └─ Write to any Lead? NO ❌
└─ Decision: BLOCK ❌
STAP 3: ESCALATION (Layer 4)
├─ Nova tried: Unauthorized write
├─ Nova is blocked: YES
├─ Escalate to: Flux
├─ Message: "Nova attempted write to unauthorized target"
└─ Action: Alert + Log + Prevent
STAP 4: AUDIT & SECURITY LOG
├─ Log: "SECURITY EVENT: Nova attempted unauthorized write"
├─ Target: Cortexia (unauthorized)
├─ Timestamp: 2026-05-25 10:16:15
├─ Severity: MEDIUM
└─ Retention: 90 days (extended)
RESULT: ❌ VIOLATION BLOCKED & ESCALATED

---

## VOORBEELD 3: FLUX (STRICT SANDBOX)

### Scenario: Flux routing a task
STAP 1: FLUX RECEIVES TASK FROM NOVA
├─ Input: Normalized task object
├─ Domain: Tech
├─ Lead needed: ?
└─ Action: Route to correct Lead
STAP 2: PERMISSION CHECK (Layer 1)
├─ Check: Is Flux allowed to READ task?
├─ Source: Nova? YES ✅
├─ Can Flux ROUTE? YES ✅
└─ Decision: ALLOW → Continue
STAP 3: ROUTING LOGIC
├─ Step 1: Analyze domain
│  └─ Domain detected: TECH
├─ Step 2: Match to Lead
│  ├─ Tech domain → Cortexia? YES ✅
│  └─ Cortexia available? YES ✅
├─ Step 3: Verify Lead can accept
│  ├─ Cortexia's concurrent tasks: 1/3
│  └─ Can accept more? YES ✅
└─ Decision: Route to Cortexia
STAP 4: PERMISSION CHECK (Layer 1 again)
├─ Check: Is Flux allowed to WRITE to Cortexia?
├─ Target: Cortexia (Lead)? YES ✅
├─ Domain match verified? YES ✅
└─ Decision: ALLOW → Send
STAP 5: RESOURCE CHECK (Layer 2)
├─ Check: Does Flux have resources?
├─ Memory: 800 MB / 1 GB? YES ✅
├─ Time: 8 min / 10 min limit? YES ✅
├─ Concurrent tasks: 2/5? YES ✅
└─ Decision: ALLOW → Continue
STAP 6: EXECUTION
├─ Flux sends task to Cortexia
├─ Task ID assigned: [task_12345]
├─ Routing record created
└─ Status: SENT
STAP 7: AUDIT & LOG
├─ Log: "Flux routed task to Cortexia"
├─ Domain: TECH ✅
├─ Lead: Cortexia ✅
├─ Task ID: task_12345
└─ Timestamp: 2026-05-25 10:17:00
RESULT: ✅ TASK ROUTED CORRECTLY

---

## VOORBEELD 4: CORTEXIA (MODERATE-STRICT SANDBOX)

### Scenario: Cortexia assigns to Sentinels
STAP 1: CORTEXIA RECEIVES TASK FROM FLUX
├─ Task: "Analyze Tech reasoning chain"
├─ Domain: TECH ✅
├─ Status: Ready for assignment
└─ Action: Break down & assign to Sentinels
STAP 2: DOMAIN CHECK (Layer 3)
├─ Check: Is this a TECH task?
├─ Task domain: TECH
├─ Cortexia's domain: TECH
├─ Match? YES ✅
└─ Decision: ALLOW → Process
STAP 3: TASK BREAKDOWN
├─ Analyze: "reasoning chain" → nero specialization
├─ nero: Deep logical reasoning ✅
├─ Task type matches specialization? YES ✅
└─ Decision: Assign to nero
STAP 4: PERMISSION CHECK (Layer 1)
├─ Check: Can Cortexia WRITE to nero?
├─ nero in Cortexia's team? YES ✅
├─ Is nero a Sentinel? YES ✅
├─ Domain Tech? YES ✅
└─ Decision: ALLOW → Send
STAP 5: RESOURCE CHECK (Layer 2)
├─ Cortexia's resources:
│  ├─ Memory: 850 MB / 1 GB? YES ✅
│  ├─ Concurrent tasks: 2/3? YES ✅
│  └─ Time: 15 min / 30 min? YES ✅
└─ Decision: ALLOW → Continue
STAP 6: BOUNDARY CHECK (Layer 3)
├─ Check 1: Is nero in Tech domain?
│  └─ nero/helix/tech? YES ✅
├─ Check 2: Does task match domain?
│  └─ Tech reasoning in Tech? YES ✅
├─ Check 3: Can nero execute alone?
│  └─ Reasoning task = nero specialization? YES ✅
└─ Decision: ALLOW → Execute
STAP 7: EXECUTION
├─ Task sent to nero
├─ Assignment record created
├─ nero status: EXECUTING
└─ Cortexia status: MONITORING
STAP 8: AUDIT & LOG
├─ Log: "Cortexia assigned Tech task to nero"
├─ Task ID: task_12345_nero
├─ Specialist: nero (reasoning)
├─ Domain: TECH ✅
└─ Timestamp: 2026-05-25 10:17:45
RESULT: ✅ TASK ASSIGNED TO CORRECT SENTINEL

---

## VOORBEELD 5: nero (MODERATE SANDBOX)

### Scenario: nero executes reasoning task
STAP 1: nero RECEIVES TASK FROM CORTEXIA
├─ Task: "Analyze this logic chain (5 steps)"
├─ Domain: TECH (Deep Logical Reasoning)
├─ Expected depth: 5 steps
├─ Limit: 10 steps max
└─ Action: Execute reasoning
STAP 2: TASK VALIDATION
├─ Check: Is this from Cortexia (my Lead)?
├─ Sender: Cortexia? YES ✅
├─ Domain: TECH? YES ✅
├─ Type: Reasoning? YES ✅
└─ Decision: ALLOW → Execute
STAP 3: RESOURCE CHECK (Layer 2)
├─ Check: Do I have resources?
├─ Memory limit: 512 MB
├─ Memory available: 480 MB
├─ Time limit: 15 minutes
├─ Time available: 14:50
├─ Concurrent tasks: 1/1 (serial)
└─ Decision: ALLOW → Execute
STAP 4: BOUNDARY CHECK (Layer 3)
├─ Check 1: Is this TECH reasoning?
│  └─ nero/helix/tech/reasoning? YES ✅
├─ Check 2: Is it within my domain?
│  └─ No Finance/Data-Intelligence? YES ✅
├─ Check 3: Reasoning depth limit?
│  └─ Max 10 steps, I'll do 5? YES ✅
└─ Decision: ALLOW → Execute
STAP 5: EXECUTION
├─ nero starts logical reasoning
├─ Step 1: [analyzing...] ✓
├─ Step 2: [analyzing...] ✓
├─ Step 3: [analyzing...] ✓
├─ Step 4: [analyzing...] ✓
├─ Step 5: [analyzing...] ✓
└─ Depth: 5/10 steps (within limit) ✅
STAP 6: OUTPUT VALIDATION
├─ nero validates own output:
│  ├─ Logical consistency? YES ✅
│  ├─ All steps documented? YES ✅
│  ├─ No external data accessed? YES ✅
│  └─ Confidence level: HIGH
└─ Decision: Output is GOOD
STAP 7: AUDIT & LOG
├─ Log: "nero executed Tech reasoning task"
├─ Task ID: task_12345_nero
├─ Steps executed: 5/10 limit
├─ Time used: 4:23 / 15:00 limit
├─ Memory used: 280 MB / 512 MB
├─ Errors: NONE
└─ Timestamp: 2026-05-25 10:22:10
STAP 8: RETURN TO CORTEXIA
├─ nero sends result to Cortexia
├─ Result validation: PASSED ✅
├─ Cortexia status: MONITORING (complete)
└─ Result: Ready for aggregation
RESULT: ✅ TASK EXECUTED SUCCESSFULLY

---

## VOORBEELD 6: nero (VIOLATION ATTEMPT)

### Scenario: nero tries to access Finance data
STAP 1: nero WANTS TO
├─ Operation: "Read Finance data"
├─ Reason: "Might be useful for reasoning"
└─ Intent: Cross-domain data access (VIOLATION)
STAP 2: BOUNDARY CHECK (Layer 3)
├─ Check: Domain lock verification
├─ nero's domain: TECH
├─ Data source: Finance
├─ Domain match? NO ❌
└─ Decision: BLOCK ❌
STAP 3: SECURITY RESPONSE
├─ Operation: BLOCKED
├─ Reason: Domain lock violation
├─ Type: SECURITY VIOLATION
└─ Action: LOG + ESCALATE
STAP 4: ESCALATION (Layer 4)
├─ Escalate to: Cortexia (nero's Lead)
├─ Alert: "nero attempted cross-domain access"
├─ Evidence: Tried to access Finance domain
├─ Timestamp: 2026-05-25 10:25:33
└─ Severity: HIGH
STAP 5: AUDIT & SECURITY LOG
├─ Log: "SECURITY VIOLATION: nero attempted Finance data access"
├─ Violation type: Cross-domain data access
├─ Attempted access: Finance domain
├─ Result: BLOCKED
├─ Agent's domain: TECH
├─ Timestamp: 2026-05-25 10:25:33
├─ Duration in log: 90 days (security event)
└─ Investigator: Cortexia
RESULT: ❌ VIOLATION BLOCKED & ESCALATED

---

## VOORBEELD 7: nero (RESOURCE LIMIT HIT)

### Scenario: nero runs out of time
STAP 1: nero EXECUTING
├─ Task depth: Expected 5 steps
├─ Actual depth so far: 8 steps
├─ Time remaining: 1 minute
├─ Reasoning complexity: HIGH
└─ Decision: Continue or stop?
STAP 2: RESOURCE CHECK (Layer 2)
├─ Monitor: Time limit
├─ Started: 10:17:00
├─ Limit: 15 minutes (10:32:00)
├─ Current: 10:31:45
├─ Time remaining: 15 seconds! ⚠️
└─ Check: Approaching timeout
STAP 3: TIMEOUT TRIGGERS
├─ Time remaining: 5 seconds
├─ Decision: STOP reasoning
├─ Action: Save current state
├─ Status: PARTIAL RESULTS
└─ Next step: Escalate
STAP 4: PARTIAL RESULT SAVING
├─ Save: Steps 1-8 (complete)
├─ Save: Current analysis
├─ Save: Findings so far
├─ Quality: PARTIAL (not complete)
├─ Confidence: MEDIUM (incomplete)
└─ Status: SAVED
STAP 5: ESCALATION (Layer 4)
├─ Escalate to: Cortexia
├─ Message: "nero ran out of time"
├─ Partial results: AVAILABLE
├─ Depth reached: 8/10 steps
├─ Time used: 15:00 (TIMEOUT)
├─ Options: Retry with more time? Escalate further?
└─ Cortexia decides
STAP 6: AUDIT & LOG
├─ Log: "nero timed out on task"
├─ Task ID: task_12345_nero
├─ Time limit: 15 minutes
├─ Time used: 15:00
├─ Steps completed: 8/10
├─ Status: PARTIAL
├─ Escalated: YES (to Cortexia)
└─ Timestamp: 2026-05-25 10:32:00
RESULT: ⚠️ TIMEOUT - ESCALATED TO LEAD

---

## SANDBOX FLOW OVERVIEW
ANY AGENT DOING ANYTHING:

PERMISSION CHECK (Can I do this?)
├─ Allowed by profile? YES → Continue
└─ NOT allowed? → BLOCK + LOG + ESCALATE
RESOURCE CHECK (Do I have resources?)
├─ Resources available? YES → Continue
└─ Out of resources? → PAUSE + SAVE + ESCALATE
BOUNDARY CHECK (Am I in my domain/authority?)
├─ Within boundaries? YES → Continue
└─ Boundary violation? → BLOCK + LOG + ESCALATE
EXECUTION (Do the work)
├─ During: Monitor resources
├─ During: Validate partial outputs
└─ On error: Save state + escalate
OUTPUT CHECK (Can I send output?)
├─ Allowed target? YES → Send
└─ Disallowed? → BLOCK + ESCALATE
AUDIT (Log everything)
├─ Log: All checks
├─ Log: Decision results
├─ Log: Execution details
└─ Log: Any violations

RESULT: ✅ SAFE EXECUTION
OR
RESULT: ❌ VIOLATION BLOCKED + ESCALATED

---

## KEY PRINCIPLES

✅ **Every operation is checked**
- Before execution
- During execution (monitoring)
- After execution (validation)

✅ **Violations are immediate**
- Not allowed = BLOCKED
- Not boundaried = BLOCKED
- Out of resources = SAVED + ESCALATED

✅ **Everything is logged**
- All checks recorded
- All decisions recorded
- All violations recorded
- 90-day retention for security events

✅ **Escalation is automatic**
- Blocker found → Escalate immediately
- No guessing → Escalate
- Boundary crossed → Escalate
- Resources exceeded → Escalate

✅ **No bypasses**
- Agents cannot disable sandbox
- Agents cannot escalate up (only to assigned Lead)
- Agents cannot access other domains
- System enforces boundaries

