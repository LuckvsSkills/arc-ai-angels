# Model Runtime & Providers
## Block 05 — Specialist Teams (Sentinel)

---

### Purpose

Sentinel is de **specialistische uitvoeringslaag** binnen ARC AI Agents. Waar Omni domein-kennis beheert, bevat Sentinel de **operationele expertise** voor specifieke taken.

| Aspect | Functie |
|--------|---------|
| **Expert Coordination** | Beheer teams van gespecialiseerde Workers |
| **Skill Matching** | Match taak-specificaties met Worker capabilities |
| **Quality Control** | Eerste validatie van Worker output |
| **Error Handling** | Lokaal herstel voordat escalatie naar Flux |

Sentinel-teams zijn **verticaal gespecialiseerd** (bijv. code, design, data) en **horizontaal gestructureerd** (lead + specialists + juniors).

---

### System Context

**Positionering:**
- **Parent:** Omni (ontvangt Task Specs)
- **Children:** Workers (concrete uitvoering)
- **Peers:** Andere Sentinel teams (load balancing, failover)

---

### Concrete Structure

Sentinel bestaat uit 4 kerncomponenten:

#### 5.1 Team Organisatie

| Rol | Verantwoordelijkheid | Worker Type |
|-----|---------------------|-------------|
| **Lead** | Review, architectuur beslissingen, escalatie | Senior Worker |
| **Senior** | Complexe taken, mentoring, kwaliteit | Specialized Worker |
| **Junior** | Standaard taken, ondersteuning, learning | General Worker |

#### 5.2 Sentinel Teams Registry

| Team ID | Domein | Specialisaties | Workers |
|---------|--------|--------------|---------|
| sentinel_code_team | Software | Python, JS, Go, Rust, SQL | 3 senior, 5 junior |
| sentinel_design_team | Visual | UI/UX, branding, illustration | 2 senior, 3 junior |
| sentinel_data_team | Analytics | SQL, Python, visualization | 2 senior, 4 junior |
| sentinel_security_team | Security | Audits, pentest, compliance | 2 senior, 2 junior |
| sentinel_copy_team | Content | SEO, technical writing, tone | 2 senior, 3 junior |

#### 5.3 Task Distribution Engine
Wijs taak toe op basis van:
- Vereiste skills (filter)
- Huidige load (50% weight)
- Expertise match (40% weight)
- Recency factor (10% weight)
- Backup Worker selectie

#### 5.4 Quality Gate
Eerste controle voor terugkeer naar Omni:
- Automated checks (syntax, tests, linting)
- Lead review voor complexiteit > 3
- Security scan voor gevoelige code
- Performance benchmarks

### Flows

#### 5.1 Standard Task Execution

#### 5.2 Multi-Worker Parallel Task

### Flows

#### 5.1 Standard Task Execution

#### 5.2 Multi-Worker Parallel Task

### Relaties met andere ARC-lagen

| Laag | Interface | Data |
|------|-----------|------|
| **Omni** | Input/Output | Task Specs / Results |
| **Workers** | Command/Response | Execution commands / Output |
| **Flux** | Escalatie only | Bij failures na retry |
| **Andere Sentinel** | Failover | Task overname bij overload |

---

### Decision Logic

| Beslissing | Input | Output |
|------------|-------|--------|
| **Welke Worker?** | Skills nodig, huidige load, expertise | Worker ID + backup ID |
| **Review nodig?** | Complexity, security flag, historie | Boolean + reviewer assignment |
| **Retry of escalatie?** | Failure type, retry count, impact | "retry" / "escalate_to_flux" / "fail_fast" |
| **Parallel of sequentieel?** | Sub-task dependencies | Execution graph |

---

### Rules & Constraints

| Regel | Rationale |
|-------|-----------|
| **R1:** Elke taak heeft minimaal 1 backup Worker | Voorkomt single point of failure |
| **R2:** Lead review verplicht voor complexity > 3 | Kwaliteitshandhaving |
| **R3:** Worker timeout strikt gehandhaafd | Voorkomt resource starvation |
| **R4:** Sentinel mag nooit direct naar Fea | Altijd via Omni→Flux |
| **R5:** Worker attribution altijd gelogd | Accountability, debugging, learning |

---

### Dependencies

| Component | Type | Impact |
|-----------|------|--------|
| Worker pool | Hard | Geen uitvoering mogelijk |
| Task queue | Hard | Backlog opbouwen |
| Omni specificaties | Hard | Geen richting zonder STS |
| Lead Worker availability | Soft | Review queue opbouwen |

---

### Decisions Made

| Beslissing | Argumentatie |
|------------|--------------|
| **Team hierarchie** | Lead/Senior/Junior voor kwaliteit en schaalbaarheid |
| **Skill-based routing** | Precieze matching taak-capability |
| **Automated + human review** | Balans tussen snelheid en kwaliteit |

---

### Decision Locked

**Owner:** Fea  
**Status:** Active  
**Version:** 2.0.0  
**Last Updated:** 2026-03-22

---

**Einde Block 05**

## Team Dispatch Flow

+----------------+      +----------------+      +----------------+
|  Omni Task     |----->|  Sentinel      |----->|  Team Router   |
|  (Enriched)    |      |  (M05)         |      |  (Classifier)  |
+----------------+      +----------------+      +----------------+
                               |
                    +----------+----------+
                    |                     |
                    v                     v
             +------------+        +------------+
             |  Domain A  |        |  Domain B  |
             |  Team      |        |  Team      |
             +------------+        +------------+
                    |                     |
                    v                     v
             +------------+        +------------+
             |  Workers   |        |  Workers   |
             +------------+        +------------+
