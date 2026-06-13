# AGENT CODEX - Complete File Blueprint

**Version:** 1.0  
**Last Updated:** 2026-06-03  
**Applies to:** All 32 agents (NOVA, FLUX, LEADS, SENTINELS)

---

## 📋 FILE COMPLETENESS STANDARD

Every agent MUST have exactly 18 files. This is the complete, verified file set.

### TIER 1: CORE IDENTITY FILES (5 files)
These define WHO the agent is.

| File | Purpose | Key Content | Size |
|------|---------|-------------|------|
| **IDENTITY.md** | Agent's foundational identity | Layer, Domain, Role, Mission, Boundaries | ~1200 bytes |
| **SOUL.md** | Agent's inner philosophy | Purpose, Values, Strengths, Weaknesses | ~1000 bytes |
| **TOOLS.md** | What agent can DO | File Operations (READ, LIST, WRITE) | ~1500 bytes |
| **AGENT_RULES.md** | Rules & Protocols | Agent rules, escalation rules, protocols | ~2000 bytes |
| **BOOTSTRAP.md** | 🔑 ENTRY POINT - Points to all others | STARTUP MODE, QUICK START, CRISIS MODE | ~1900 bytes |

### TIER 2: OPERATIONAL FILES (6 files)
These define HOW the agent works.

| File | Purpose | Key Content | Size |
|------|---------|-------------|------|
| **WORKFLOW.md** | Work process | INPUT, PROCESS, OUTPUT flow | ~1100 bytes |
| **USER.md** | Fea's expectations | Communication style, role expectations | ~3500 bytes |
| **MEMORY.md** | Learning system | Core learnings, performance baseline | ~2000 bytes |
| **HEARTBEAT.md** | Operational metrics | Health checks, activity metrics | ~500 bytes |
| **HANDOFF.md** | Escalation protocol | How to hand off to other agents | ~900 bytes |
| **MODEL.md** | AI model configuration | Model selection, complexity detection | ~1200 bytes |

### TIER 3: KNOWLEDGE FILES (4 files)
These maintain institutional knowledge.

| File | Purpose | Key Content | Size |
|------|---------|-------------|------|
| **JOURNAL.md** | Session log template | Entry structure for logging sessions | ~900 bytes |
| **TASKS.md** | Active task list | Current tasks, status, priority | ~2000 bytes |
| **TASK_HISTORY.md** | Historical performance | Completed tasks, lessons learned | ~1300 bytes |
| **SKILLS.md** | Domain expertise | Skills, expertise areas, growth areas | ~2400 bytes |

### TIER 4: SYSTEM FILES (3 files)
These manage agent as system component.

| File | Purpose | Key Content | Size |
|------|---------|-------------|------|
| **AGENTS.md** | Agent ecosystem | Total agents, hierarchy, relationships | ~1400 bytes |
| **HARNAS.md** | Autonomy system | Auto-consolidation, HARNAS phases | ~2900 bytes |
| **README.md** | Agent overview | Role, responsibilities, status | ~600 bytes |

---

## 🔗 FILE RELATIONSHIPS & DEPENDENCIES
BOOTSTRAP.md (ENTRY POINT)
├─→ Pointer to: IDENTITY.md
│   └─ "Who am I?"
│   └─ References: SOUL.md (why), USER.md (what Fea expects)
│
├─→ Pointer to: TOOLS.md
│   └─ "What can I do?"
│   └─ References: AGENT_RULES.md (rules for using tools)
│
├─→ Pointer to: WORKFLOW.md
│   └─ "How do I work?"
│   └─ References: HEARTBEAT.md (how healthy?), MEMORY.md (what learned?)
│
├─→ Pointer to: TASKS.md
│   └─ "What am I doing now?"
│   └─ References: TASK_HISTORY.md (what did I do?), SKILLS.md (what can I do?)
│
├─→ Pointer to: HANDOFF.md
│   └─ "How do I escalate?"
│   └─ References: AGENTS.md (who else?), MODEL.md (when escalate?)
│
└─→ Pointer to: HARNAS.md
└─ "How do I grow?"
└─ References: MEMORY.md (consolidate), JOURNAL.md (logs to consolidate)
---

## 📖 FILE READING ORDER (For New Agents)

When deploying a new agent, read in this order:

1. **BOOTSTRAP.md** - Understand the structure
2. **IDENTITY.md** - Understand the agent
3. **TOOLS.md** - Understand capabilities
4. **WORKFLOW.md** - Understand process
5. **USER.md** - Understand Fea's expectations
6. **AGENT_RULES.md** - Understand constraints
7. **MEMORY.md** - Understand past learnings
8. **[OTHERS]** - Reference as needed

---

## 📊 FILE SIZE VERIFICATION

Each file must be:
- **Minimum:** Content must be >500 bytes (typically)
- **Maximum:** No hard limit (but >10KB = reconsider structure)
- **Target:** 1000-3000 bytes (sweet spot for maintenance)

**Verification Command:**
```bash
for file in IDENTITY.md SOUL.md TOOLS.md AGENT_RULES.md BOOTSTRAP.md \
            WORKFLOW.md USER.md MEMORY.md JOURNAL.md TASKS.md TASK_HISTORY.md \
            HEARTBEAT.md AGENTS.md MODEL.md HANDOFF.md HARNAS.md SKILLS.md README.md; do
    size=$(wc -c < "$AGENT_DIR/$file" 2>/dev/null || echo "0")
    if [ $size -gt 0 ]; then
        echo "✅ $file ($size bytes)"
    else
        echo "❌ $file - MISSING"
    fi
done
```

---

## 🎯 BOOTSTRAP.md TEMPLATE

Bootstrap is the **entry point file**. It should point to all other files:

```markdown
# BOOTSTRAP.md — Agent Initialization

## STARTUP MODE
When agent starts:
1. Load IDENTITY.md (understand who you are)
2. Load TOOLS.md (understand what you can do)
3. Load BOOTSTRAP.md (this file - understand the structure)
4. Load WORKFLOW.md (understand how to work)
5. Check HEARTBEAT.md (verify you're healthy)

## QUICK START
For rapid deployment:
→ See IDENTITY.md for role
→ See USER.md for Fea expectations
→ See WORKFLOW.md for process
→ See HANDOFF.md for escalation

## CRISIS MODE
If something breaks:
→ Check HEARTBEAT.md (health status)
→ Review MEMORY.md (what you learned)
→ Check AGENT_RULES.md (what you're breaking)
→ Escalate via HANDOFF.md (get help)

## COMPLETE FILE MANIFEST
[List all 18 files with brief purpose]

## HARNAS CONSOLIDATION
→ See HARNAS.md (autonomy system)
→ See MEMORY.md (learning system)
→ See JOURNAL.md (logging system)
```

---

## 🚀 CODEX FOR DIFFERENT AGENT TYPES

### CORE AGENTS (NOVA, FLUX)
All 18 files + CODEX = **Full operational knowledge**
- Include: CODEX.md
- Purpose: Complex routing, heavyweight decisions
- Access: NOVA ✅, FLUX ✅

### LEAD AGENTS (CORTEXIA, SAELIA, FINORIA, LUMERIA, FLUENTIA)
All 18 files + CODEX = **Recommended** ✅
- Include: CODEX.md
- Purpose: Coordinate their domain + sentinels
- Benefit: Leads need to understand architecture, delegate to sentinels
- Recommendation: **YES - Include CODEX for LEADS**

### SENTINEL AGENTS (25 agents)
All 18 files, CODEX = **Optional**
- Include: CODEX.md (reference only)
- Purpose: Execute tasks, report status
- Benefit: Sentinels can understand file structure if needed
- Recommendation: **Include but lower priority** (they follow lead orders, not independent architects)

---

## ✅ DEPLOYMENT CHECKLIST

For new agent deployment:

```bash
□ Create /agents/[agent]/ directory
□ Add all 18 files (use templates from CODEX)
□ Add CODEX.md (reference copy)
□ Verify file sizes (check_file function)
□ Run audit script (audit-[agent]-complete.sh)
□ Verify: 18/18 files COMPLETE
□ Register in OpenClaw (~/.openclaw/openclaw.json)
□ Set workspace (if NOVA/FLUX)
□ Sync files (if NOVA/FLUX)
□ Test connection (curl test)
□ Deploy!
```

---

## 📝 STANDARDIZED VERIFICATION

**Audit Script Template:**
```bash
#!/bin/bash
AGENT_DIR="/home/prime/arc_ai_angels/agents/$AGENT/[workspace]"

check_file() {
    local filename=$1
    local min_size=$2
    local search_term=$3
    
    if [ -f "$AGENT_DIR/$filename" ]; then
        size=$(wc -c < "$AGENT_DIR/$filename")
        if [ $size -gt $min_size ] && grep -q "$search_term" "$AGENT_DIR/$filename"; then
            echo "✅ $filename - COMPLETE ($size bytes)"
        else
            echo "⚠️ $filename - INCOMPLETE"
        fi
    else
        echo "❌ $filename - MISSING"
    fi
}

# Check all 18 files
```

---

## 🎓 REFERENCE: FLUX VERIFICATION

**FLUX Complete Status (2026-06-03):**
✅ IDENTITY.md - COMPLETE (1255 bytes)
✅ SOUL.md - COMPLETE (1073 bytes)
✅ TOOLS.md - COMPLETE (1542 bytes)
✅ AGENT_RULES.md - COMPLETE (2170 bytes)
✅ BOOTSTRAP.md - COMPLETE (1901 bytes)
✅ WORKFLOW.md - COMPLETE (1175 bytes)
✅ USER.md - COMPLETE (3978 bytes)
✅ MEMORY.md - COMPLETE (2176 bytes)
✅ JOURNAL.md - COMPLETE (916 bytes)
✅ TASKS.md - COMPLETE (2178 bytes)
✅ TASK_HISTORY.md - COMPLETE (1340 bytes)
✅ HEARTBEAT.md - COMPLETE (511 bytes)
✅ AGENTS.md - COMPLETE (1481 bytes)
✅ MODEL.md - COMPLETE (1224 bytes)
✅ HANDOFF.md - COMPLETE (963 bytes)
✅ HARNAS.md - COMPLETE (2900 bytes)
✅ SKILLS.md - COMPLETE (2414 bytes)
✅ README.md - COMPLETE (573 bytes)

**Total:** 18/18 COMPLETE ✅  
**Total Size:** 36,359 bytes  
**Last Verified:** 2026-06-03 02:45 UTC

---

## 📌 USAGE

**For NOVA & FLUX:**
```bash
Include in: /agents/nova/CODEX.md
Include in: /agents/flux/CODEX.md
Access: Via agent's BOOTSTRAP.md reference
```

**For LEAD AGENTS:**
```bash
Include in: /agents/[lead]/CODEX.md
Purpose: Reference + training
```

**For SENTINELS:**
```bash
Include in: /agents/[sentinel]/CODEX.md (optional)
Purpose: Optional reference
```

