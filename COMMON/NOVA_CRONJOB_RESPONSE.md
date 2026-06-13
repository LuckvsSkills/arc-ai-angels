# NOVA Cronjob Status Response Format

## Problem
NOVA gave incomplete response - didn't answer the actual question about cronjobs

## Solution: Proper Response Structure

### What Fea Asked
"Status cronjobs" OR "What cronjobs are active?"

### What NOVA Should Answer

#### Format 1: Full Cronjob List
✅ CRONJOB STATUS REPORT
Current Cronjobs: 2 active, 0 disabled
Active Cronjobs:

Flux Memory Pipeline

Agent: flux
Schedule: every 1d
Next: [time]
Status: OK


OpenClaw Automatic Update

Agent: flux
Schedule: every 21d
Next: [time]
Status: OK



Disabled/Error Cronjobs:

None

Missing Expected Cronjobs:

CORTEXIA System Startup (@reboot) - NOT FOUND
CORTEXIA Health Monitor - NOT FOUND
FORGE GitHub Searcher - NOT FOUND
(9 other FORGE jobs missing)

Action Required:

Register CORTEXIA cronjobs
Register FORGE cronjobs
See: /home/prime/arc_ai_angels/COMMON/cronjob_add.sh

Ref: [timestamp]

#### Format 2: Agent-Specific
✅ CORTEXIA CRONJOB STATUS
Agent: cortexia
Role: TECH Lead Agent
Domain: Infrastructure/Technical
Current Cronjobs: 0
Expected: 4

System Startup (@reboot)
Health Monitor (*/5 * * * *)
Daily Report (0 6 * * *)
Config Validation (0 * * * *)

Status: NOT REGISTERED YET
Action: Register cronjobs with openclaw cron add
Ref: [timestamp]

#### Format 3: Problem Report
❌ CRONJOB SYSTEM STATUS - ISSUES FOUND
Issue 1: CORTEXIA Cronjobs Not Registered

Expected: 4 cronjobs
Found: 0 cronjobs
Impact: System won't auto-start on reboot
Fix: Use cronjob_add.sh or openclaw cron add

Issue 2: FORGE Cronjobs Missing

Expected: 9 cronjobs (GitHub searcher, analyzer, etc)
Found: 0 cronjobs
Impact: FORGE automation not running
Fix: Recreate via cronjob framework

Issue 3: Cronjob_add.sh Not Working

Tried: 1 time
Result: Silent failure
Status: Script needs debugging
Fix: Use openclaw cron add directly

Current System Cronjobs: 2 (flux only)
Recommendation:

Register CORTEXIA cronjobs first (system ops)
Then register FORGE cronjobs (projects)
Test each with eenmalige (one-time) execution
Monitor via health_check.sh

Ref: [timestamp]

## Implementation: Make NOVA Answer Properly

### What NOVA Should Do When Asked "Status cronjobs"

```bash
# Step 1: Get current cronjobs
openclaw cron list > /tmp/cronjobs.txt

# Step 2: Parse results
- Count active cronjobs
- List each with agent, schedule, status
- Identify missing expected cronjobs
- Flag errors/issues

# Step 3: Generate proper response
- Format as above
- Include actionable info
- Suggest next steps
- Provide references
```

### Example NOVA Telegram Response
User: @Nova_Lens_bot Status cronjobs
NOVA Response:
✅ CRONJOB STATUS
Active: 2

Flux Memory Pipeline (flux, every 1d, OK)
OpenClaw Update (flux, every 21d, OK)

Not Registered: 13

CORTEXIA System Startup (@reboot)
CORTEXIA Health Monitor (every 5 min)
CORTEXIA Daily Report (daily 6:00)
CORTEXIA Config Check (hourly)
FORGE GitHub Searcher (Mon/Wed/Fri 7:00)
[8 more FORGE jobs]

Ref: 2026-05-28 01:05 UTC
Next: Register CORTEXIA first → FORGE second

## Critical Issue

**cronjob_add.sh is NOT working!**

Symptoms:
- Script runs without errors
- No cronjob appears in list
- Silent failure

Solution:
- Use `openclaw cron add` directly
- OR debug cronjob_add.sh script
- OR create new cronjob_registration.sh

## Action Items

1. ✅ Identify the actual problem (CORTEXIA/FORGE cronjobs not registered)
2. ✅ NOVA must report complete status
3. ✅ NOVA must flag missing cronjobs
4. ✅ NOVA must suggest actions
5. ⏳ Register cronjobs properly
6. ⏳ Test cronjob execution
7. ⏳ Create cronjob testing framework

