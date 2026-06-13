# Cronjob Orchestration Architecture

## The Real Flow
Supreme Fea (Human)
↓ (Natural language request)
NOVA (Orchestrator)
↓ (Interprets, routes)
FLUX (Orchestration Layer)
↓ (Manages flow)
LEAD AGENTS (per domain)
↓ (Execute, monitor)
TARGET AGENT (forge, nova, etc)
↓ (Does work)
OpenClaw (Cronjob System)
↓ (Schedules execution)
FORGE Worker (executes)
↓ (Reports back)
NOVA (Aggregates status)
↓ (Reports to Fea)

## What We Need to Define

### 1. NOVA's Role (Orchestrator)
- ❓ How does Fea communicate with NOVA? (Telegram? Direct?)
- ❓ What language/format?
- ❓ NOVA interprets → routes to FLUX?
- ❓ NOVA tracks ALL cronjobs globally?

### 2. FLUX's Role (Orchestration)
- ❓ FLUX creates cronjob in OpenClaw?
- ❓ FLUX delegates to Lead Agents?
- ❓ FLUX monitors execution?
- ❓ FLUX reports back to NOVA?

### 3. LEAD AGENTS Role (Domain Managers)
- ❓ Do Lead Agents own their domain cronjobs?
- ❓ Do they validate before creation?
- ❓ Do they monitor their own jobs?
- ❓ How do they report to FLUX?

### 4. TARGET AGENT Role (Executor)
- ❓ Does FORGE create its own cronjobs?
- ❓ Or only execute what FLUX tells it?
- ❓ Self-reporting status?

### 5. Monitoring & Reporting
- ❓ Real-time dashboard monitoring?
- ❓ Telegram status updates?
- ❓ Error handling & retry?
- ❓ Audit trail?

## Questions to Answer

1. **Natural Language**: How should you talk to NOVA?
   - Telegram message format?
   - Specific keywords/syntax?
   - Example: "@Nova create cronjob FORGE GitHub Searcher schedule 0 7 * * 1,3,5"?

2. **Hierarchy**:
   - NOVA → FLUX → Lead Agent → Agent?
   - Or NOVA → Agent directly for simple tasks?

3. **Monitoring**:
   - Who watches the dashboard?
   - Who reports errors?
   - Who retries failed jobs?

4. **Permissions**:
   - Can any agent create cronjobs?
   - Only Lead Agents?
   - Only FLUX?
   - Only NOVA?

5. **Status Updates**:
   - Real-time WebSocket to dashboard?
   - Polling every N seconds?
   - Post-execution report only?

## Current Status
⏳ NEEDS DESIGN DECISION
⏳ WAITING FOR SUPREME FEA INPUT

