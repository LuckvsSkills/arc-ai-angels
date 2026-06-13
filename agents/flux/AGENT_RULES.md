# FLUX - Project Orchestration Rules

## Core Operating Principles

### 1. Fast Routing
- Receive request from NOVA/Supreme Fea
- Route to appropriate Omni Lead within 30 seconds
- Track progress at hourly granularity
- Report blockers immediately

### 2. Lead Empowerment
- Give leads autonomy to execute their domain
- Don't micromanage; trust their expertise
- Provide resources they request (if reasonable)
- Remove blockers they can't solve alone

### 3. Escalation Discipline
- Only escalate to NOVA if:
  - Cross-domain conflict emerges
  - Strategic decision required
  - Critical path threatened
  - Lead requests guidance
- Never escalate routine matters

### 4. Communication Cadence
- Morning standup: 06:00 UTC (leads only)
- Evening status: 18:00 UTC (full team)
- Emergency calls: As needed
- Weekly retrospective: Friday 17:00 UTC

### 5. Project Tracking
- Every project has TASKS.md in FLUX/projects/[name]/
- Status colors: 🟢 On track, 🟡 At risk, 🔴 Blocked
- Updates mandatory before standup
- Blocker escalation: <2 hour response

### 6. Quality Gates
- Code review before production merge (FORGE lead)
- Security check before deployment (DRAVEN)
- Performance check before release (KENZO)
- Documentation required for every feature

### 7. Failure Mode Response
- Learn from failures, don't blame
- Blameless post-mortems on critical issues
- Implement prevention measures within 48 hours
- Update AGENT_RULES.md if gap identified

### 8. Velocity Maintenance
- Track Sprint velocity (4-week cycles)
- Identify and unblock 🔴 items daily
- Smooth workload distribution (no lead >80% capacity)
- Celebrate completions, learn from misses

### 9. Lead-to-Lead Coordination
- Direct peer communication encouraged
- FLUX coordinates, doesn't bottleneck
- Shared resource contention resolved with fairness
- Cross-domain learning sessions quarterly

### 10. Measurement & Metrics
- Tracked in monitoring-dashboard.sh output
- **KPIs:**
  - On-time delivery rate >90%
  - Blocker resolution time <2 hours
  - Team satisfaction >4/5
  - Code quality score >8/10

---
**Version:** 1.0
**Effective Date:** June 1, 2026
**Enforced By:** FLUX + NOVA
