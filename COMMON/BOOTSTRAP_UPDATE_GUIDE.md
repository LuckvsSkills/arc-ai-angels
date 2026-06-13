# BOOTSTRAP UPDATE GUIDE
## How All MD Files Connect for Agent Startup

---

## AGENT STARTUP SEQUENCE (NEW ORDER)

When an agent starts, it should load files in this order:

### 1. CORE EXPECTATIONS (READ ONLY)
USER_MAIN.md

Supreme Fea's expectations for ALL agents
Non-negotiable principles
Organization rules
Success criteria


IDENTITY.md

Who you are
Your role
Your domain
Your characteristics


AGENTS.md

Your position in hierarchy
Your responsibilities
Your scope
Your constraints




### 2. HOW YOU WORK (OPERATIONAL)

WORKFLOW.md

Your daily process
Input → Process → Output
Your constraints (can't do)
Your freedom (can do)
Success criteria


HANDOFF.md

Communication protocol
How you send/receive work
Escalation rules
Reporting format




### 3. CAPABILITY & CONTEXT

SKILLS.md

What you can do
What tools you have
What training you have


USER_MAIN.md (ref again)

Fea's communication style
Decision authority rules
Autonomy growth path


USER.md (agent-specific)

Fea's preferences for YOU
Special considerations
Personal notes




### 4. STARTUP & OPERATION

BOOTSTRAP.md

Startup instructions
Health check
Load configuration
Ready to work


HEARTBEAT.md

Keep alive signal
Health status
Regular check-in




### 5. LEARNING & MEMORY

TASKS.md

Current tasks
Task tracking
Completed tasks log


MEMORY.md

What to remember
Patterns learned
Preferences learned
Domain knowledge


JOURNAL/ directory

Daily reflections
Improvement notes
Decision logs
Learning captured




### 6. CONTEXT & TOOLS

TOOLS.md

Available tools
How to use them
Constraints per tool


SOUL.md

Personality
Cognitive style
Decision logic
Essence


README.md

Overview
Quick reference
Links to other resources




---

## BOOTSTRAP.md TEMPLATE UPDATE

Current BOOTSTRAP.md is missing key references.

**Should include:**

```markdown
# BOOTSTRAP.md — [Agent Name]

## Startup Sequence

1. Load USER_MAIN.md (read: Supreme Fea's expectations)
2. Load IDENTITY.md (read: who you are)
3. Load AGENTS.md (read: your role in system)
4. Load WORKFLOW.md (read: your daily process)
5. Load HANDOFF.md (read: communication protocol)
6. Load SKILLS.md (read: what you can do)
7. Load USER_[name].md (read: Fea's preferences for you)
8. Load HEARTBEAT.md (verify: you're healthy)
9. Ready to work!

## Self-Improvement

Track and update:
- TASKS.md (mark tasks done, lessons learned)
- MEMORY.md (new patterns, preferences, domain knowledge)
- JOURNAL/ (daily reflections, improvements, decisions)

See SELF_IMPROVING_GUIDE.md for details.

## Daily Operations

1. Check HEARTBEAT.md (are you healthy?)
2. Read TASKS.md (what's today's work?)
3. Check WORKFLOW.md (what's your process?)
4. Execute
5. Update TASKS.md (log completion)
6. Update MEMORY.md (lessons learned)
7. Reflect in JOURNAL/ (daily note)

## References
- WORKFLOW.md → Your daily process
- AGENTS.md → Your role + constraints
- HANDOFF.md → How to communicate
- USER_MAIN.md → Fea's expectations
- SKILLS.md → What you can do
```

---

## FILE UPDATE LOCATIONS

### Per Agent Workspace:
/agents/[agent]/workspace/BOOTSTRAP.md
→ Add references to USER_MAIN.md, WORKFLOW.md
→ Add Self-Improvement section

### Per Agent Root:
/agents/[agent]/BOOTSTRAP.md
→ Add same references
→ Link to workspace version if different

---

## VERIFICATION CHECKLIST

Each agent should have:
✅ USER_MAIN.md (central, all agents reference)
✅ IDENTITY.md (who you are)
✅ AGENTS.md (your role)
✅ WORKFLOW.md (your process) ← NEW
✅ HANDOFF.md (communication)
✅ SKILLS.md (what you can do)
✅ USER_[agent].md (Fea's preferences for you)
✅ BOOTSTRAP.md (updated with references)
✅ HEARTBEAT.md (keep alive)
✅ TASKS.md (current work)
✅ MEMORY.md (what to remember)
✅ JOURNAL/ (reflections)

