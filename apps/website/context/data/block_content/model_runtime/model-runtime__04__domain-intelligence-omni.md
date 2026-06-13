# Model Runtime & Providers
## Block 04 — Domain Intelligence Layer (Omni)

---

### Purpose

Omni is de **domeinexpertise laag**. Waar Flux beslist *wat* er moet gebeuren, bepaalt Omni *hoe* het binnen een specifiek vakgebied wordt uitgevoerd.

| Aspect | Functie |
|--------|---------|
| **Domain Translation** | Vertaal intentie naar domein-specifieke taak |
| **Knowledge Retrieval** | Haal relevante domein-kennis op |
| **Specialist Routing** | Bepaal welk Sentinel-team en welke Workers |
| **Quality Calibration** | Domein-specifieke kwaliteitscriteria |

---

### System Context

Flux → Omni → Sentinel

---

### Concrete Structure

#### 4.1 Domain Parser
Analyseert RDO, extract domein-entiteiten.

#### 4.2 Knowledge Retriever
Query vector DB + graph voor context.

#### 4.3 Task Decomposer
Splits complexe taken in Sentinel-taken.

---

### Rules

- R1: Omni communiceert nooit direct naar Fea
- R2: Knowledge retrieval max 500ms
- R3: Task specs immutable na dispatch
- R4: Minimaal 2 Sentinel teams per Omni

---

### Decision Locked

Owner: Fea  
Status: Active  
Version: 2.0.0

### Concrete Structure

Omni bestaat uit 5 kerncomponenten:

#### 4.1 Domain Instanties

| Omni ID | Domein | Specialisatie | Sentinel Teams |
|---------|--------|---------------|----------------|
| omni_technical_01 | Software Engineering | Code, architecture, DevOps | code_team, infra_team, security_team |
| omni_creative_01 | Content & Design | Copy, visuals, UX, branding | copy_team, design_team, ux_team |
| omni_data_01 | Data & Analytics | SQL, ML, BI, pipelines | analytics_team, ml_team, viz_team |
| omni_security_01 | Security & Compliance | Audits, policies, threats | audit_team, threat_team, policy_team |
| omni_general_01 | Algemene kennis | Geen diepe specialisatie | general_team |

#### 4.2 Domain Parser
Analyseer RDO, extract domein-specifieke entiteiten.

#### 4.3 Knowledge Retriever
Multi-stage retrieval uit Vector Store, Graph DB, Live APIs.

#### 4.4 Task Decomposer
Splits complexe taken in Sentinel-taken met dependencies.

#### 4.5 Specification Builder
Output: Sentinel Task Specs (STS) met domein-specifieke criteria.

### Flows

#### 4.1 Standard Domain Processing

#### 4.2 Cross-Domain Request

### Relaties met andere ARC-lagen

| Laag | Relatie | Mechanisme |
|------|---------|------------|
| **Flux** | Parent/Consumer | Ontvangt RDO, returnt Result+Quality |
| **Sentinel** | Child/Dispatcher | Stuurt Task Specs, ontvangt uitvoering |
| **Andere Omni** | Peer/Coordinator | Via Flux voor cross-domain |
| **Knowledge Stores** | Data dependency | Vector DB, Graph DB, API clients |

---

### Decision Logic

| Beslissing | Input | Output |
|------------|-------|--------|
| **Welke Sentinel teams?** | Task type + complexity + beschikbaarheid | Team ID lijst met prioriteit |
| **Welke knowledge bronnen?** | Entity types + urgency | Geprioriteerde retrieval strategie |
| **Hoe decomponeren?** | Complexity score + dependencies | Task graph (parallel/sequential) |
| **Quality threshold?** | Domein + user tier + request type | Minimale acceptatie scores |

---

### Rules & Constraints

| Regel | Rationale |
|-------|-----------|
| **R1:** Omni mag nooit direct naar Fea communiceren | Altijd via Flux voor context-integriteit |
| **R2:** Knowledge retrieval max 500ms | Voorkomt timeout cascade |
| **R3:** Task specs zijn immutable na dispatch | Consistentie in uitvoering |
| **R4:** Elke Omni heeft minimaal 2 Sentinel teams | Redundantie voor load balancing |
| **R5:** Cross-domain requests expliciet markeren | Flux weet dat aggregatie nodig is |

---

### Dependencies

| Component | Type | Fallback |
|-----------|------|----------|
| Vector Store | Hard | Generieke prompts zonder context |
| Graph DB | Soft | Alleen vector search |
| Sentinel queues | Hard | Queue in backlog, alert operators |
| Live APIs | Soft | Cached versies (max 24u oud) |

---

### Decisions Made

| Beslissing | Argumentatie |
|------------|--------------|
| **Multi-stage retrieval** | Balans tussen snelheid (vector) en diepgang (graph) |
| **Domein-specifieke instanties** | Expertise concentratie vs generalisatie |
| **Immutable task specs** | Voorkomt wijzigingen tijdens uitvoering |

---

### Decision Locked

**Owner:** Fea  
**Status:** Active  
**Version:** 2.0.0  
**Last Updated:** 2026-03-22

---

**Einde Block 04**

## Domain Knowledge Flow

+----------------+      +----------------+      +----------------+
|   Flux Task    |----->|  Omni Engine   |----->|  Domain DB     |
|   (Intent)     |      |   (M04)        |      |  (Knowledge)   |
+----------------+      +----------------+      +----------------+
                               |
                               v
                        +----------------+
                        |  Context       |
                        |  Enrichment    |
                        +----------------+
                               |
                               v
                        +----------------+
                        |  Enriched Task |
                        |  to Sentinel   |
                        +----------------+
