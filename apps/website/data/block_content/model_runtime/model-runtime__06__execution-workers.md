# Model Runtime & Providers
## Block 06 — Execution Workers

---

### Purpose

Workers zijn de **concrete uitvoeringsinstanties**. Stateless, ephemeral, gespecialiseerd.

| Aspect | Functie |
|--------|---------|
| **Task Execution** | Voer atomic taken uit |
| **Tool Usage** | Bedien externe tools, API's |
| **Model Interaction** | Communcatie met LLMs |
| **Output Generation** | Produceer tastbare resultaten |

---

### System Context

Sentinel → Workers

---

### Concrete Structure

#### 6.1 Worker Types
LLM, Tool, Code, Data, File, API Workers.

#### 6.2 Lifecycle
IDLE → ASSIGNED → RUNNING → COMPLETE → IDLE.

#### 6.3 Execution Command/Result
Gestandaardiseerde formats voor input/output.

---

### Rules

- R1: Workers zijn stateless
- R2: Max execution time enforced
- R3: Geen directe externe communicatie zonder proxy
- R4: Alle tool calls gelogd

---

### Decision Locked

Owner: Fea  
Status: Active  
Version: 2.0.0

#### 6.4 Execution Result (ER) Formaat

Status, output, metadata, quality_signals.


### Flows

#### 6.1 LLM Worker Execution

Sentinel EC binnen → Context ophalen → Prompt samenstellen → Model API call → Output ontvangen → Basis validatie → Metadata verzamelen → ER bouwen → Terug naar Sentinel → Cleanup

#### 6.2 Code Worker Execution (Sandboxed)

Sentinel EC binnen → Sandbox initialiseren (gVisor) → Code schrijven → Dependencies installeren → Code uitvoeren met resource limits → Output capture → Test suite draaien → Resultaat terugsturen → Sandbox vernietigen

---

### Relaties met andere ARC-lagen

| Laag | Richting | Data |
|------|----------|------|
| **Sentinel** | Ontvangt EC / Stuurt ER | Commands / Results |
| **OpenClaw** | Runtime dependency | Model API's, sandboxing |
| **External** | Tool/API calls | Gecontroleerde egress |

**Critical:** Workers communiceren **nooit direct** met Flux, Omni, Nova, of Fea. Altijd via Sentinel.

---

### Decision Logic

| Beslissing | Input | Output |
|------------|-------|--------|
| **Welk model?** | Task type, complexity, cost constraints | Model ID + parameters |
| **Sandbox level?** | Code vs data vs tool | gVisor / Kata / Namespace |
| **Retry in Worker?** | Failure type | Boolean (meestal nee, Sentinel handelt retry) |
| **Early termination?** | Streaming output quality | Stop criteria check |

---

### Rules & Constraints

| Regel | Rationale |
|-------|-----------|
| **R1:** Workers zijn stateless | Schaalbaarheid, debugbaarheid |
| **R2:** Max execution time enforced (hard kill) | Resource bescherming |
| **R3:** Geen directe externe communicatie zonder proxy | Security, auditability |
| **R4:** Alle tool calls gelogd | Reproduceerbaarheid |
| **R5:** Output size limits (max 10MB) | Memory bescherming |
| **R6:** Worker pool altijd warm (pre-initialized) | Latency reductie |

---

### Dependencies

| Component | Type | Fallback |
|-----------|------|----------|
| OpenClaw Runtime | Hard | Geen uitvoering |
| Model API's | Hard | Fallback model (lokaal) |
| Sandbox runtime | Hard | Geen code execution |
| Tool registries | Soft | Cached tool definitions |
| Sentinel command queue | Hard | Worker idle |

---

### Decisions Made

| Beslissing | Argumentatie |
|------------|--------------|
| **Stateless design** | Schaalbaarheid > state complexiteit |
| **Ephemeral sandboxes** | Security > herbruikbaarheid |
| **Pre-warmed pool** | Latency > resource efficiëntie |

---

### Decision Locked

**Owner:** Fea  
**Status:** Active  
**Version:** 2.0.0  
**Last Updated:** 2026-03-22

---

**Einde Block 06**

## Worker Execution Flow

+----------------+      +----------------+      +----------------+
|  Sentinel Task |----->|  Worker Pool   |----->|  Agent Exec    |
|  (Assigned)    |      |  (M06)         |      |  (Sandbox)     |
+----------------+      +----------------+      +----------------+
                               |                       |
                               v                       v
                        +----------------+      +----------------+
                        |  Monitoring    |      |  Result        |
                        |  (Health)      |      |  (Output)      |
                        +----------------+      +----------------+
                                                        |
                                                        v
                                                 +----------------+
                                                 |  Back to       |
                                                 |  Flux          |
                                                 +----------------+
