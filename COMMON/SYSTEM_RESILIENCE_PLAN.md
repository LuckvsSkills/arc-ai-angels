# System Resilience & Observability Plan

## Problem Analysis: Today's Issues

### What Went Wrong
1. OpenClaw Gateway binding issue (WSL2 loopback vs LAN)
2. MCC Frontend couldn't reach backend
3. OAuth redirect URI misconfiguration
4. No early warning system

### Root Causes
- No health check automation
- No status dashboard visibility
- No startup validation script
- Network configuration not monitored

---

## Solution 1: SYSTEM HEALTH MONITORING

### Health Check Script
```bash
/home/prime/arc_ai_angels/COMMON/health_check.sh
```

Checks:
- OpenClaw Gateway reachable
- MCC Frontend responding
- MCC Backend responding
- All 32 agents bootstrapped
- Cronjobs valid
- Network bindings correct
- OAuth config correct

### MCC Tab: System Status

Add to MCC:
OpenClaw Dashboard
├─ Gateway Status: ✅/❌
├─ Latest Check: [timestamp]
├─ Network: 127.0.0.1:50506
├─ Agents: 32/32 active
├─ Cronjobs: 3 valid
└─ Quick Actions
├─ Restart Gateway
├─ Check Health
└─ View Logs

---

## Solution 2: STARTUP ORCHESTRATION SCRIPT

### Master Startup Script
```bash
/home/prime/arc_ai_angels/COMMON/startup_all.sh
```

**Steps:**
1. Check prerequisites (Node, Python, etc)
2. Start OpenClaw Gateway
3. Start MCC Backend
4. Start MCC Frontend
5. Start Cloudflare Tunnel
6. Verify all services running
7. Run health check
8. Report status

**Output:**
- Success: All green
- Failure: Which service failed + logs
- Suggestions: How to fix

---

## Solution 3: MCC SYSTEM CONTROL TAB

### New Tab in MCC: "System Control"

**Features:**

#### Health Status
- OpenClaw: ✅/❌ (reachable, agents, cronjobs)
- MCC Backend: ✅/❌ (responding, database)
- MCC Frontend: ✅/❌ (loaded, API connected)
- Cloudflare Tunnel: ✅/❌ (active, DNS)
- Network: ✅/❌ (bindings, ports)

#### Quick Actions
- [🔄 Check Health] - Run health check now
- [🚀 Startup All] - Start all services
- [🛑 Shutdown All] - Stop all services
- [📊 View Logs] - Show recent logs
- [🔧 Config Check] - Validate all configs

#### Problem Resolution
If OpenClaw failing:
├─ Binding: loopback/lan/custom
├─ Port: 50506
├─ Try: Restart Gateway
└─ See Logs

#### Auto-Recovery
- Service down? Auto-restart with retries
- Failed health check? Alert + suggest fix
- Port conflict? Suggest next available port
- Network unreachable? Offer Tailscale fallback

---

## Solution 4: EARLY WARNING SYSTEM

### Automated Monitoring (runs every 5 min)

```bash
/home/prime/arc_ai_angels/COMMON/monitor_continuous.sh
```

Watches:
- Port availability
- Service responsiveness
- Network connectivity
- Config integrity
- Cronjob validity

**On Problem:**
1. Alert in MCC System Status
2. Log event with timestamp
3. Suggest auto-recovery
4. Telegram notification to Fea

---

## Solution 5: CONFIGURATION VALIDATION

### Pre-Startup Checks
```bash
/home/prime/arc_ai_angels/COMMON/validate_system_config.sh
```

Verifies:
- ~/.openclaw/openclaw.json: valid JSON
- ~/.openclaw/openclaw.json: binding correct
- /mcc-backend/.env: OAuth config correct
- Cloudflare config: valid tunnel token
- Cronjobs: valid delivery configs
- Network: ports not in use

---

## Solution 6: PREVENTION CHECKLIST

### Configuration Lock
- Store "known good" configs
- Warn if config changed unexpectedly
- Suggest rollback if needed

### Network Resilience
- Monitor WSL2 network binding
- Fallback: Tailscale if loopback fails
- Fallback: SSH tunnel if needed

### Port Management
- Track which services use which ports
- Auto-detect conflicts
- Suggest alternatives

---

## Implementation Checklist

- [ ] health_check.sh: Create
- [ ] startup_all.sh: Create
- [ ] monitor_continuous.sh: Create
- [ ] validate_system_config.sh: Create
- [ ] MCC System Status Tab: Design
- [ ] MCC System Control Tab: Design
- [ ] Auto-recovery logic: Implement
- [ ] Telegram alerts: Setup
- [ ] Documentation: Complete

---

## Files to Create

1. **health_check.sh** - Check all services
2. **startup_all.sh** - Start all services in correct order
3. **monitor_continuous.sh** - Background monitoring
4. **validate_system_config.sh** - Pre-startup validation
5. **auto_recovery.sh** - Auto-restart failed services
6. **MCC System Status Component** - React component
7. **MCC System Control Component** - React component

---

## Status
⏳ NEEDS IMPLEMENTATION
🎯 Priority: HIGH (prevents today's issues)

