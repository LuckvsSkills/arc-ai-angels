# MCC MEMORY TAB - Monitoring Plan

## TAB: MEMORY

### SECTION 1: System Status (Top)
- Overall Memory Health: gauge (85%)
- Agent Memory: 21KB / 100KB
- Shared Memory: X KB
- Last Consolidation: timestamp + status
- Sync Status: 27/32 agents
- Status indicators: green/yellow/red

### SECTION 2: Agent Memory Table
Columns: Agent | Layer | Domain | HANDOFF | MEMORY | JOURNAL | Last Update | Status

Features:
- All 32 agents listed
- Filter by layer (core/lead/sentinel)
- Filter by domain (finix/helix/matrix/quantix/zenix)
- Sort by size, date, status
- Color codes: green < 1KB, yellow 1-2KB, red > 2KB
- Click agent → detail view

### SECTION 3: Domain Breakdown
Per domain (Finix/Helix/Matrix/Quantix/Zenix):
- Lead agent name
- Total sentinels: 5
- Total memory: X KB
- Total learnings: X
- Last sync: timestamp
- Status: OPTIMAL/CAUTION/ALERT

### SECTION 4: Learning Analytics (Charts)
Chart 1: Learning Growth Over Time
- Days on X-axis, cumulative learnings on Y-axis
- Per domain color coded

Chart 2: Memory Usage Trend
- Days on X-axis, KB on Y-axis
- Agent memory vs shared memory

Chart 3: Consolidation Frequency
- Days on X-axis, consolidations per day
- Per agent or per domain

Chart 4: Domain Learning Distribution
- Pie chart: % learnings per domain

### SECTION 5: Recent Learnings Log
Latest 20 learning entries:
[timestamp] agent (domain/layer)
- learning text

Features:
- Search by text
- Filter by agent/domain
- Filter by time range
- Click to view full entry

### SECTION 6: Cronjob Status
All 34 cronjobs:
- Agent name
- Schedule: 24 hours
- Next run: time remaining
- Last run: timestamp + duration
- Status: ACTIVE/IDLE/ERROR
- Buttons: [View Logs] [Run Now]

### SECTION 7: Memory Quality Metrics
Checks:
- Duplicate learnings: 0 ✅
- Empty MEMORY files: 0 ✅
- Missing JOURNAL: 0 ✅
- Memory size OK: 32/32 ✅
- Consolidation frequency: 24h ✅
- Last full sync: 27/32 agents ✅

Performance:
- Avg consolidation time: 34ms
- Largest memory: 1.1KB
- Smallest memory: 245B
- Average per agent: 673B
- Efficiency: 21% of limit ✅

### SECTION 8: Manual Controls
Consolidation:
- [Consolidate All Agents Now]
- [Consolidate Selected Agent] (dropdown)
- [Preview Consolidation] (dry-run)

Sync:
- [Sync Learnings to Shared]
- [Run Flux Orchestration]
- [Update Shared Memory]

View:
- [View SYSTEM_STATE.md]
- [View CROSS_LEARNING.md]
- [View Sync Reports]
- [View Orchestration Reports]

Config:
- [Edit Consolidation Schedule]
- [Edit Memory Limits]
- [Edit Alert Thresholds]

### SECTION 9: Alerts & Issues
Current:
- No critical alerts
- No warnings
- Next maintenance: in 22h

If problems occur:
- Show agent name + error
- Show action buttons to fix
- Show historical issues (7 days)

### SECTION 10: Export & Reports
- [Export Agent Memory as CSV]
- [Export Learning Analytics as PDF]
- [Export Consolidation Logs]
- [Export Full Memory Snapshot]
- [Export Domain Reports]

Report generation:
- Memory Health Report
- Learning Trends Report
- Domain Comparison Report
- Consolidation Statistics

## DATA SOURCES (waar we data uit halen)

Agent files:
- ~/arc_ai_angels/agents/[agent]/HANDOFF.md
- ~/arc_ai_angels/agents/[agent]/MEMORY.md
- ~/arc_ai_angels/agents/[agent]/JOURNAL/open/
- ~/arc_ai_angels/agents/[agent]/JOURNAL/closed/

Shared memory:
- ~/arc_ai_angels/shared/memory/SYSTEM_STATE.md
- ~/arc_ai_angels/shared/memory/CROSS_LEARNING.md
- ~/arc_ai_angels/shared/memory/sync-*.json
- ~/arc_ai_angels/shared/memory/orchestration-*.json

Cronjobs:
- ~/.openclaw/cron/jobs.json
- ~/.openclaw/cron/runs/*.jsonl

System:
- ~/arc_ai_angels/CANON.md

## REAL-TIME FEATURES

- Auto-refresh every 5 minutes
- Manual refresh button
- Live countdown for next cronjob
- Last updated timestamp
- Green/yellow/red status indicators
- Click-through for detail views
- Search and filter options

## SUMMARY

10 sections + rich data visualization + manual controls + alerts + exports

Everything needed to monitor and control the memory system from one place.

