# Agent .md File Analysis & Rollout Plan

## AGENT CATEGORIES

### 1. EMPTY AGENTS (NEED COMPLETE SETUP - 7 agents)
- cortexia (Omni Lead - HELIX)
- saelia (Omni Lead - SAELIA)  
- lumeria (Omni Lead - QUANTIX)
- fluentia (Omni Lead - ZENIX)
- finoria (Omni Lead - FINORIA)
- main (System agent)
- workers (Worker layer)

### 2. STANDARD SENTINELS (MOSTLY COMPLETE - 17 agents)
Have: AGENTS.md, HEARTBEAT.md, IDENTITY.md, SOUL.md, TOOLS.md, USER.md

- nero, forge, axon (HELIX)
- kairo, kenzo, odis, vector, zion (SAELIA)
- arix, daxio, enki, sora, tharos (FINORIA)
- elora, kresta, luvia, nura, vondra (QUANTIX)
- draven, orizon, solis, unia, zena (ZENIX)

### 3. ADVANCED AGENTS (MORE COMPLETE)
- flux_core (13 files)
- nova (40 files - with security/rules)
- flux (60 files - with historical logs)
- omni (434 files - with historical logs)

### 4. SPECIAL/TEST
- standalone (10 files - test agent)

## UNIVERSAL TEMPLATE FILES NEEDED

Based on standard agents pattern:

1. **AGENTS_UNIVERSAL_TEMPLATE.md**
   - Agent registry/relationship definition
   - Subagent mappings

2. **IDENTITY_UNIVERSAL_TEMPLATE.md**
   - Agent name, role, specialty
   - Domain assignment
   - Responsibilities

3. **SOUL_UNIVERSAL_TEMPLATE.md**
   - Personality/character
   - Decision-making style
   - Communication approach

4. **TOOLS_UNIVERSAL_TEMPLATE.md**
   - Available tools
   - Capabilities
   - Restrictions

5. **USER_UNIVERSAL_TEMPLATE.md**
   - User interaction rules
   - Preferences
   - Communication norms

6. **HEARTBEAT_UNIVERSAL_TEMPLATE.md**
   - Status monitoring
   - Health checks
   - Operational status

7. **BOOTSTRAP_UNIVERSAL_TEMPLATE.md** (Optional)
   - Initialization procedures
   - Startup configuration

8. **MEMORY_UNIVERSAL_TEMPLATE.md** (Optional)
   - Memory structure
   - Learning approach
   - Persistence rules

## ROLLOUT STRATEGY

### Phase 1: Create Universal Templates
- IDENTITY_UNIVERSAL_TEMPLATE.md
- SOUL_UNIVERSAL_TEMPLATE.md
- TOOLS_UNIVERSAL_TEMPLATE.md
- USER_UNIVERSAL_TEMPLATE.md
- HEARTBEAT_UNIVERSAL_TEMPLATE.md
- AGENTS_UNIVERSAL_TEMPLATE.md

### Phase 2: Populate Empty Omni Leads
- cortexia, saelia, lumeria, fluentia, finoria

### Phase 3: Update Sentinels (if needed)
- Ensure all have standard 6+ files
- Add BOOTSTRAP.md where missing

### Phase 4: Automation
- Create script to generate .md files for new agents
- Template system for consistency

## NEXT STEPS

1. Review what's IN flux, nova, omni files (they might have patterns!)
2. Create universal templates
3. Map which agent needs which file
4. Build rollout system
