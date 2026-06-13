# PHASE 2: AGENT CRONJOB API
## Implementation of Cronjob Operations for Agent Independence

Date: 2026-06-01
Status: IMPLEMENTATION IN PROGRESS
Goal: Agents can schedule and manage their own cronjobs

---

## 🎯 WHAT WE'RE BUILDING

A set of **cronjob operations** that agents can call to:
1. Schedule cronjobs (e.g., daily consolidation at 06:00)
2. Trigger cronjobs manually (run now)
3. Check cronjob status (is it running?)
4. Read cronjob logs (what happened?)
5. Delete/modify cronjobs (remove or reschedule)

---

## 📝 REQUIRED CRONJOB OPERATIONS

### 1. SCHEDULE CRONJOB
```bash
schedule_cronjob(agent, time, command)
├─ Input: Agent name, time (HH:MM), command to run
├─ Returns: cronjob_id
└─ Example: schedule_cronjob("arix", "06:00", "consolidate-memory")
```

### 2. TRIGGER CRONJOB
```bash
trigger_cronjob(agent, cronjob_id)
├─ Input: Agent name, cronjob_id
├─ Returns: job_execution_id
└─ Example: trigger_cronjob("arix", "cron-001")
```

### 3. CHECK STATUS
```bash
check_cronjob_status(agent, cronjob_id)
├─ Input: Agent name, cronjob_id
├─ Returns: "active|inactive|running|failed"
└─ Example: check_cronjob_status("arix", "cron-001")
```

### 4. READ LOGS
```bash
read_cronjob_logs(agent, cronjob_id)
├─ Input: Agent name, cronjob_id
├─ Returns: Log contents
└─ Example: read_cronjob_logs("arix", "cron-001")
```

### 5. DELETE CRONJOB
```bash
delete_cronjob(agent, cronjob_id)
├─ Input: Agent name, cronjob_id
├─ Returns: Success/failure
└─ Example: delete_cronjob("arix", "cron-001")
```

---

## 🔧 IMPLEMENTATION APPROACH

### Option A: Crontab-based
Use system crontab to manage agent cronjobs:
- Store cronjob definitions in `/etc/cron.d/`
- Agents can add/remove via wrapper
- Native system integration

### Option B: Task Scheduler Script
Custom script-based scheduler:
- Store cronjob definitions in HARNAS
- Custom scheduler daemon checks and runs
- More control, less dependency on system cron

### Option C: OpenClaw Native
Use OpenClaw's built-in scheduling:
- Check if OpenClaw supports cronjobs
- Agents schedule via OpenClaw API
- Clean integration with existing system

---

## 📊 CRONJOB STRUCTURE

Each cronjob needs:
cronjob_id:      unique identifier (cron-001, cron-002, etc)
agent:           which agent owns it
schedule:        time to run (06:00, 12:00, etc)
command:         what to execute
status:          active/inactive/running
created:         timestamp
last_run:        timestamp
next_run:        timestamp
logs:            execution logs
---

## 🎯 USE CASE: DAILY CONSOLIDATION

Agent ARIX wants to consolidate memory daily at 06:00:

```bash
# Agent schedules consolidation
schedule_cronjob("arix", "06:00", "consolidate-memory")
← Returns: cron-001

# System stores this
cron-001: arix, 06:00, "consolidate-memory", active

# Every day at 06:00, system:
trigger_cronjob("arix", "cron-001")
← Agent runs consolidation routine

# Agent can check status
check_cronjob_status("arix", "cron-001")
← Returns: "active, last_run: 2026-06-01 06:05, next_run: 2026-06-02 06:00"

# Agent can read logs
read_cronjob_logs("arix", "cron-001")
← Returns: "✓ Consolidation complete, 15 learnings extracted"
```

---

## 📋 TESTING PLAN

### Test with ARIX
1. ARIX schedules daily consolidation (06:00)
2. ARIX checks if cronjob was created
3. ARIX can manually trigger cronjob
4. ARIX can read execution logs
5. ARIX can modify or delete cronjob

### Success Criteria
- ✅ Cronjob scheduling works
- ✅ Manual triggering works
- ✅ Status checking works
- ✅ Log reading works
- ✅ Deletion/modification works

---

## 🚀 NEXT STEPS

Determine implementation approach:
1. Check what cron infrastructure is available
2. Check OpenClaw capabilities
3. Build wrapper based on best approach
4. Test with ARIX
5. Rollout to all 32 agents

Ready to begin implementation?

