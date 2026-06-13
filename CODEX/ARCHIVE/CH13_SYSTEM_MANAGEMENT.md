# ARC SYSTEM MANAGEMENT GUIDE

## Quick Start

/home/prime/arc_ai_angels/arc_system

## Overview

Complete system management tool voor ARC AI ANGELS met:
- System status monitoring
- Service management
- Agent status checking
- Process monitoring
- Diagnostics & troubleshooting

## Main Menu

### 1. SERVICES
Manage OpenClaw Gateway service
- View Status
- Start/Stop/Restart

### 2. AGENTS
Check and test individual agents or all agents
- Check Individual Agent (10 sec per agent)
- Test Agent Connection
- View All Agents (5-10 minutes)

### 3. PROCESSES
View all running services

### 4. TROUBLESHOOT
- Gateway Logs
- Listening Ports
- System Health
- Debug Agent

## Agent Status

✅ = Online and responding
⏳ = Not responding (may be loading)

## Command Reference

Check agent:
openclaw agent --agent nova --message "ping" --json

View gateway status:
PAGER=cat systemctl status openclaw-gateway.service

View logs:
PAGER=cat journalctl -u openclaw-gateway.service -n 30

## File Locations

/home/prime/arc_ai_angels/arc_system (This tool)
/home/prime/arc_ai_angels/CODEX/ (Documentation)
/home/prime/arc_ai_angels/SESSIONS/ (History)

