# NOVA Direct Access Requirements

## Current Problem
NOVA moet dingen via FLUX doen (3 hops), maar zou direct moeten kunnen:

### Scope: What NOVA needs DIRECT access to

1. **Cronjobs Management**
   - List cronjobs: `openclaw cron list`
   - Create cronjobs: `openclaw cron add`
   - Delete cronjobs: `openclaw cron delete`
   - Status: `openclaw cron status`

2. **System Status** (needs definition)
   - Agent status
   - OpenClaw health
   - Gateway info
   - Resource usage

3. **Agent Management** (needs definition)
   - List agents
   - Agent health
   - Session management
   - ...

4. **Telegram Commands** (needs definition)
   - Direct bot control
   - Message routing
   - ...

5. **Other Direct Needs** (TBD with Supreme Fea)
   - To be discussed & documented

## Architecture Solutions

**Option A:** NOVA_TOKEN + CLI access
**Option B:** Python skills for direct API access
**Option C:** REST API wrapper
**Option D:** Hybrid approach

## Status
⏳ TO BE DISCUSSED WITH SUPREME FEA
