# Model Runtime & Providers
## Block 03 — Master Orchestrator (Flux)

---

### Purpose

Flux is het **centrale brein** van ARC AI Agents. Het ontvangt geverifieerde intenties van Nova, bepaalt *wat* er moet gebeuren, *wie* het doet, en *hoe* het resultaat terugstroomt.

| Aspect | Functie |
|--------|---------|
| **Routing Decision** | Welke Omni-domein en Sentinel-team krijgt de taak? |
| **Context Management** | Sessiestatus, historie, dependencies tussen sub-taken |
| **Resource Allocation** | Welke Workers, welke prioriteit, welke deadline? |
| **Quality Assurance** | Controleer output voordat het naar Fea retourneert |

Flux is **stateful per sessie** en houdt de volledige conversation graph bij.

---

### System Context

**Positionering:**
- **Parent:** Nova (enkel GIO input)
- **Children:** Omni (domeinselectie), Sentinel (teamselectie), Workers (uitvoering)
- **Peers:** Geen — Flux is de enige orchestrator

---

### Concrete Structure

Flux bestaat uit 4 kerncomponenten:

#### 3.1 Router Engine
**Input:** GIO van Nova  
**Output:** Routing Decision Object (RDO)

| Component | Verantwoordelijkheid |
|-----------|---------------------|
| Intent Analyzer | Parse classified_intent, bepaal domein category |
| Domain Mapper | Match intent naar Omni-domein (tech, creative, data, etc.) |
| Complexity Scorer | Schat benodigde processing depth (1-5) |
| Dependency Resolver | Check of eerdere sessie-context nodig is |

**RDO Structuur:**
- target_omni, target_sentinel_team
- complexity_level, estimated_tokens
- required_capabilities, context_dependencies
- execution_plan (parallel/sequential steps)
- constraints (max_latency, max_cost, quality_threshold)

#### 3.2 Context Manager
**State opslag per sessie:**

| Data type | Storage | TTL |
|-----------|---------|-----|
| Active conversation graph | Redis | 24 uur |
| Historical message references | PostgreSQL | 90 dagen |
| User preference cache | Redis | 1 uur |
| Cross-session patterns | Graph DB (Neo4j) | permanent |

**Context merging:** Combineer nieuwe GIO met bestaande sessie-graph, relevante historie (laatste 5 turns OF keywords), user preferences.

#### 3.3 Dispatch Engine
**Taak distributie:**

| Priority | Lane | Gebruik |
|----------|------|---------|
| 5 (Critical) | Instant | Security incidents, system alerts |
| 4 (High) | Fast | Admin requests, urgent user queries |
| 3 (Normal) | Standard | Regular requests |
| 2 (Low) | Batch | Background tasks |
| 1 (Background) | Deferred | Analytics, non-urgent jobs |

**Dispatch protocol:** Enriched context + execution plan + callback endpoint + timeout deadline naar Omni.

#### 3.4 Result Aggregator
**Verzamel en combineer:**
- Sub-results van multi-domain requests
- Parallelle taak outputs
- Quality checks tegen threshold
- Response formatting naar Fea-compatibel formaat

### Flows

#### 4.1 Standard Request Flow

#### 4.2 Multi-Step Planning Flow (Complex Requests)

#### 4.3 Failure Recovery Flow

### Relaties met andere ARC-lagen

| Laag | Interface | Data formaat |
|------|-----------|--------------|
| **Nova** | Input queue | GIO (JSON) |
| **Omni** | RPC / Message Queue | Dispatch Object + Context Ref |
| **Sentinel** | Via Omni (indirect) | Task specifications |
| **Workers** | Via Sentinel (indirect) | Execution commands |
| **Nova (terug)** | Output queue | Response Object (RO) |

**Critical:** Flux kent Workers **niet direct**. Alleen via Omni → Sentinel → Workers.

---

### Decision Logic

| Beslissing | Input | Logica |
|------------|-------|--------|
| **Omni selectie** | Intent classification + entities | Lookup table: intent_pattern → omni_id |
| **Complexity score** | Token estimate + domain + historie | Formula: base(1-5) * domain_factor * history_modifier |
| **Parallel vs Sequential** | Dependency graph analyse | IF shared_deps → sequential; IF independent → parallel |
| **Retry vs Fail** | Failure type + retry_count + user tier | Hard fail bij security errors; retry bij timeouts (max 2x) |

---

### Rules & Constraints

| Regel | Rationale |
|-------|-----------|
| **R1:** Flux mag nooit direct met Workers communiceren | Architectuur-integriteit: altijd via Omni→Sentinel |
| **R2:** Alle routing beslissingen moeten gelogd zijn | Auditability, debugging, optimalisatie |
| **R3:** Max 3 retry pogingen per request | Resource bescherming, gebruiker experience |
| **R4:** Context graph max 100 nodes per sessie | Memory bescherming, performance |
| **R5:** Timeout deadlines zijn hard | Voorkomt cascade failures |
| **R6:** Quality gate kan output rejecten | Fea krijgt nooit ongeverifieerde content |

---

### Dependencies

| Component | Type | Impact bij uitval |
|-----------|------|-------------------|
| Conversation State Store (Redis) | Hard | Geen context tracking, stateless fallback |
| Persistent Store (PostgreSQL) | Soft | Historie niet beschikbaar, maar current sessie werkt |
| Omni message queues | Hard | Geen taak distributie mogelijk |
| Graph DB (Neo4j) | Soft | Cross-session insights niet beschikbaar |

---

### Decisions Made

| Beslissing | Alternatief | Argumentatie |
|------------|-------------|--------------|
| **Stateful design** | Stateless met externe state | Complexiteit in Flux is acceptabel voor betere context management |
| **RDO als expliciet object** | Impliciete routing | Transparantie, debugging, replay mogelijkheid |
| **Quality gate in Flux** | Quality gate in Sentinel | Sentinel is gespecialiseerd, Flux heeft overzicht over volledige output |
| **Graph-based conversation model** | Lineaire lijst | Branching (multi-task) en merging (aggregatie) natuurlijk ondersteund |

---

### Decision Locked

**Owner:** Fea  
**Status:** Active  
**Version:** 2.0.0  
**Last Updated:** 2026-03-22

---

**Einde Block 03**

## Orchestration Flow Diagram

### Task Distribution Flow

+----------------+      +----------------+      +----------------+
|   Nova Queue   |----->|  Flux Master   |----->|   Dispatcher   |
|   (GIO Input)  |      |   (M03)        |      |   (Routing)    |
+----------------+      +----------------+      +----------------+
                               |                       |
                               v                       v
                        +----------------+      +----------------+
                        |  State Store   |      |  Sentinel Team |
                        |  (Workflow)    |      |  Assignment    |
                        +----------------+      +----------------+
                               ^                       |
                               |                       v
                        +----------------+      +----------------+
                        |  Result        |<-----|  Worker        |
                        |  Aggregation   |      |  Execution     |
                        +----------------+      +----------------+
