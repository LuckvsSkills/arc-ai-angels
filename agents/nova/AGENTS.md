# NOVA - Agent Manifest
## Complete Agent Inventory

### System Overview
**Total Agents:** 32
**Operational:** 32/32 ✅
**Orchestrator Tier:** 2 (NOVA, FLUX with FLUX_CORE as heavyweight mode)
**Omni Leads:** 5 (Cortexia, Saelia, Finoria, Lumeria, Fluentia)
**Sentinels:** 25

---

## Orchestrator Tier
1. **NOVA** (Self) - Gateway, Intake, Consigliere
2. **FLUX** - Orchestrator, Underboss (FLUX_CORE = heavyweight auto-escalation mode)

## Omni Leads (Domain Leadership)
3. **CORTEXIA** - Tech/Systems Lead (HELIX workers: nero, forge, axon, ventura, clio)
4. **SAELIA** - Data & Intelligence Lead (MATRIX workers: kairo, kenzo, odis, vector, zion)
5. **FINORIA** - Finance & Operations Lead (FINIX workers: arix, daxio, enki, sora, tharos)
6. **LUMERIA** - Creative & Innovation Lead (QUANTIX workers: elora, kresta, luvia, nura, vondra)
7. **FLUENTIA** - Communication & Collaboration Lead (ZENIX workers: draven, orizon, solis, unia, zena)

## Sentinel Tier (Executors - 25 total)
### HELIX (Cortexia's team) - 5 Sentinels
8. **NERO** - Error Handling & Recovery
9. **FORGE** - GitHub & Repository Management
10. **AXON** - Network Operations
11. **VENTURA** - Venture & Growth
12. **CLIO** - Documentation & Knowledge

### MATRIX (Saelia's team) - 5 Sentinels
13. **KAIRO** - API Integration
14. **KENZO** - Performance Monitoring
15. **ODIS** - Optimization
16. **VECTOR** - Vectorization & ML
17. **ZION** - Zenith Goals & Vision

### FINIX (Finoria's team) - 5 Sentinels
18. **ARIX** - Data Processing
19. **DAXIO** - Analytics
20. **ENKI** - Research & Discovery
21. **SORA** - Speech & Audio
22. **THAROS** - Threat Detection

### QUANTIX (Lumeria's team) - 5 Sentinels
23. **ELORA** - Planning & Scheduling
24. **KRESTA** - Task Execution
25. **LUVIA** - Memory Management
26. **NURA** - User Interface
27. **VONDRA** - Vanguard Operations

### ZENIX (Fluentia's team) - 5 Sentinels
28. **DRAVEN** - Security & Compliance
29. **ORIZON** - Horizons & Strategy
30. **SOLIS** - Solar/Energy Systems
31. **UNIA** - Unified Systems
32. **ZENA** - Automation Framework

---

## Communication Hierarchy
SUPREME FEA → NOVA (Gateway) → FLUX → Omni Leads → 25 Sentinels

**Note:** FLUX_CORE is not a separate agent - it is FLUX operating in heavyweight mode for complex orchestration decisions.

**Status:** All 32 agents operational with HARNAS cronjob orchestration (128 cronjobs: 4x daily per agent)

**Last Updated:** 2026-06-03
