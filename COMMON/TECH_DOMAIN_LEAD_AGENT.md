# TECH Domain Lead Agent
## System Operations & Infrastructure Management

### Purpose
TECH Lead Agent owns all technical/infrastructure operations:
- System startup & shutdown
- Health monitoring
- Port management
- Service orchestration
- System recovery
- Infrastructure automation

### Responsibilities

#### 1. System Startup Operations
- Orchestrate service startup after reboot
- Validate prerequisites
- Health verification
- Error recovery
- Telegram reporting

#### 2. Continuous Monitoring
- Monitor system health every N minutes
- Alert on service failures
- Detect port conflicts
- Track service uptime
- Report metrics

#### 3. Infrastructure Management
- Manage ports allocation
- Handle service dependencies
- Manage process lifecycle
- Handle configuration validation
- Coordinate with network (Tailscale, Cloudflare)

#### 4. Incident Response
- Auto-restart failed services
- Escalate critical issues
- Generate incident reports
- Coordinate recovery

---

## Architecture
Supreme Fea
↓ "Status system" / "Start system"
NOVA (Orchestrator - routes to TECH)
↓
TECH Lead Agent (System Operations)
├─ startup_all.sh
├─ health_check.sh
├─ monitor_continuous.sh
├─ validate_system_config.sh
└─ auto_recovery.sh
↓
Workers:
├─ system_startup.py
├─ system_health.py
├─ system_monitor.py
├─ system_recovery.py
└─ system_config.py

### Command Flow
Fea: "NOVA, start the system"
↓
NOVA: "This is tech ops, routing to TECH"
↓
TECH: "Starting system via startup_all.sh"
↓
TECH: Reports "System online, all services running"
↓
NOVA: Reports to Fea "System ready"

---

## Workers in TECH Agent
/home/prime/arc_ai_angels/agents/tech/workspace/workers/
├── system_startup.py
│   ├── Run startup_all.sh
│   ├── Verify services
│   ├── Report status
│   └── Escalate errors
│
├── system_health.py
│   ├── Run health_check.sh
│   ├── Parse output
│   ├── Report metrics
│   └── Alert on issues
│
├── system_monitor.py
│   ├── Continuous monitoring loop
│   ├── Check every 5 minutes
│   ├── Log metrics
│   └── Detect anomalies
│
├── system_recovery.py
│   ├── Detect failed service
│   ├── Auto-restart with retry
│   ├── Log recovery action
│   └── Escalate if needed
│
└── system_config.py
├── Validate all configs
├── Check JSON integrity
├── Check port availability
└── Report issues

---

## TECH Cronjobs

### 1. System Startup (On Reboot)
Name: TECH System Startup
Schedule: @reboot
Agent: tech
Command: python3 workspace/workers/system_startup.py
Delivery: announce -> webchat + telegram

### 2. Continuous Health Monitoring
Name: TECH System Health Monitor
Schedule: every 5 minutes (*/5 * * * *)
Agent: tech
Command: python3 workspace/workers/system_health.py
Delivery: announce -> webchat (only on issues)

### 3. Daily System Report
Name: TECH System Daily Report
Schedule: 0 6 * * * (6:00 AM daily)
Agent: tech
Command: python3 workspace/workers/system_monitor.py --report
Delivery: announce -> telegram

### 4. Configuration Validation
Name: TECH System Config Validation
Schedule: 0 * * * * (hourly)
Agent: tech
Command: python3 workspace/workers/system_config.py
Delivery: announce -> webchat (only on errors)

---

## Implementation Steps

### Step 1: Create TECH Agent
```bash
# Create TECH agent in OpenClaw
openclaw agent create \
  --id tech \
  --name "TECH Domain Lead Agent" \
  --role "lead" \
  --domain "tech"
```

### Step 2: Create workspace directory
```bash
mkdir -p /home/prime/arc_ai_angels/agents/tech/workspace/workers
```

### Step 3: Create system_startup.py
```python
#!/usr/bin/env python3
"""TECH Agent - System Startup Worker"""

import subprocess
import json
from datetime import datetime

def startup():
    result = subprocess.run(
        ["/home/prime/arc_ai_angels/COMMON/startup_all.sh"],
        capture_output=True,
        text=True,
        timeout=120
    )
    
    return {
        "timestamp": datetime.now().isoformat(),
        "agent": "tech",
        "task": "system_startup",
        "success": result.returncode == 0,
        "message": "System startup orchestrated"
    }

if __name__ == "__main__":
    result = startup()
    print(json.dumps(result))
```

### Step 4: Add cronjobs
```bash
/home/prime/arc_ai_angels/COMMON/cronjob_add.sh tech \
  "TECH System Startup" \
  "@reboot" \
  "python3 workspace/workers/system_startup.py"
```

---

## TECH Agent Characteristics

**Domain**: Technical Infrastructure
**Lead Role**: System Operations
**Responsibilities**:
- System startup
- Health monitoring
- Infrastructure management
- Service orchestration
- Incident response

**Reports To**: NOVA (for aggregation)

**Cronjobs**: 4-5 critical system jobs

**Workers**: 5 Python scripts

---

## Integration with Architecture
NOVA (Supreme Orchestrator)
├─ Routes "system start" → TECH
├─ Aggregates TECH status
└─ Reports to Fea
TECH Lead Agent (Tech/Infrastructure)
├─ Owns system startup
├─ Owns continuous monitoring
├─ Owns infrastructure ops
└─ Reports to NOVA
CORTEXIA Lead Agent (Tools Domain)
├─ Owns tool management
└─ Reports to NOVA
CLIO Lead Agent (Data Domain)
├─ Owns data operations
└─ Reports to NOVA
TARGET AGENTS (Execution)
└─ Execute domain work

---

## Timeline

**TODAY (2026-05-28):**
- [ ] Create TECH agent structure
- [ ] Create system_startup.py
- [ ] Create system_health.py
- [ ] Test manual execution

**NEXT SESSION:**
- [ ] Create TECH cronjobs
- [ ] Test @reboot trigger
- [ ] Create monitoring workers
- [ ] Test full automation

