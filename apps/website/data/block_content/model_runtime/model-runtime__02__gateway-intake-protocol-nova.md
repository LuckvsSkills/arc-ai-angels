# Model Runtime & Providers
## Block 02 — Gateway & Intake Protocol (Nova)

---

### Purpose

Nova is de **enige toegangspoort** tussen externe actors (Fea) en het ARC AI Agents ecosysteem. Nova's purpose is driedubbel:

| Aspect | Functie |
|--------|---------|
| **Boundary Control** | Fysieke en logische scheiding tussen onvertrouwde input en interne systemen |
| **Intent Extraction** | Ruwe input transformeren naar gestructureerde, geverifieerde intentie-objecten |
| **Load & Threat Shaping** | Traffic management, rate limiting, en eerste afwijzing van malafide of overbelastende requests |

Nova is **stateless per request** maar **state-aware over sessies**. Het maakt geen beslissingen over *wat* er moet gebeuren (dat is Flux), maar bepaalt *of* en *hoe* een intentie het systeem binnenkomt.

---

### System Context

**Positionering in ARC-hiërarchie:**
- Directe parent: Fea (alle mogelijke bronnen)
- Directe child: Flux (enkel geverifieerde intenties)
- Parallelle lagen: Geen — Nova is de enige gateway

---

### Concrete Structure

Nova bestaat uit 3 subcomponenten met strikte verantwoordelijkheden:

#### 3.1 Intake Handler
**Verantwoordelijkheid:** Ruwe data ontvangen en normaliseren

| Input Type | Handler Module | Normalisatie Output |
|------------|---------------|---------------------|
| Text (chat, prompt) | text_intake.py | UTF-8 string, max 100k chars |
| Voice (audio) | voice_intake.py | Transcript + audio metadata |
| File (pdf, code, image) | file_intake.py | Extracted text + file hash |
| API (structured JSON) | api_intake.py | Gevalideerd JSON object |
| Stream (real-time data) | stream_intake.py | Gebufferde chunks met sequentie ID |

**Critical Rule:** Alle handlers produceren een Unified Input Envelope (UIE) met versie, source, payload, context en metadata.

#### 3.2 Validation Engine
**Verantwoordelijkheid:** UIE controleren op toegestaanheid en integriteit

**Validatielagen (strikte volgorde):**
1. Schema Check → Fout = 400 Bad Request
2. Auth Check → Fout = 401 Unauthorized
3. Rate Check → Fout = 429 Too Many Requests
4. Content Scan → Fout = 403 Forbidden
5. Size Check → Fout = 413 Payload Too Large

**Rate Limiting Regels:**
- anonymous: 10 req/min, burst 3, max 50/uur
- user: 60 req/min, burst 10, max 500/uur
- admin: 300 req/min, burst 50, max 2000/uur
- system: 1000 req/min, burst 100, onbeperkt

#### 3.3 Transform Pipeline
**Verantwoordelijkheid:** Geverifieerde UIE omzetten naar Intentie-Object voor Flux

**Transformatiestappen:**
1. Language Detection → ISO code + confidence
2. Entity Extraction → gestructureerde entities
3. Intent Classification → primaire intent + confidence
4. Context Enrichment → + historie + preferences
5. Priority Tagging → score 1-5

**Output:** Geverifieerd Intentie-Object (GIO) met routing, enriched_payload, security_context.

### Flows

#### 4.1 Happy Path: Standaard Request

Fea input → Intake Handler → UIE creatie → Validation Engine → Alle checks pass → Transform Pipeline → GIO creatie → Queue naar Flux → Flux acknowledge → Fea bevestiging

Timing: < 250ms (p95)

#### 4.2 Failure Path: Afwijzing

Fea input → Intake Handler → UIE creatie → Validation Engine → CHECK FAIL → Error Handler → Logging naar Sentinel → Fea foutcode (zonder interne details)

#### 4.3 Async Path: Grote Bestanden

Fea upload → Intake Handler → UIE met async_required → Size check fail → Async Router → Temp bucket + job → Worker Queue → Progress updates → Completion → GIO naar Flux

### Relaties met andere ARC-lagen

| Laag | Relatie type | Concreet mechanisme |
|------|-------------|---------------------|
| **Flux** | Parent/Consumer | Nova pusht GIO naar Flux input queue (Redis/RabbitMQ). Flux returnt acknowledge. Geen directe state sharing. |
| **Omni** | Configuratie bron | Omni levert domein-specifieke validatieregels (bijv. "code requests max 10k regels"). Nova cached deze regels, refreshed elke 60s. |
| **Sentinel** | Security reporting | Bij afwijzingen (401, 403, 429) → directe log naar Sentinel Security. Bij verdachte patronen → real-time alert. |
| **Workers** | Async delegatie | Grote files worden door Nova doorgeschoven naar FileProcessor Workers, niet door Nova zelf verwerkt. |

---

### Decision Logic

Nova neemt 3 typen beslissingen:

| Beslissing | Input | Logica | Output |
|------------|-------|--------|--------|
| **Accept/Reject** | UIE + validatiechecks | AND-gate: alle checks moeten pass | Doorgaan naar Transform of Afwijzen |
| **Priority** | Intent classificatie + actor level + historie | Score = (intent_urgency * 0.4) + (actor_priority * 0.3) + (historie_context * 0.3) | Priority 1-5 naar Flux |
| **Routing** | Payload type + size + classified intent | IF size > threshold → Async Worker route; ELSE IF intent in domein_X → Flux queue voor domein_X | Target queue selectie |

---

### Rules & Constraints

| Regel | Rationale | Sanctie bij overtreding |
|-------|-----------|------------------------|
| **R1:** Nova mag **nooit** business logic uitvoeren | Nova is gateway, geen processor | Code review blocker |
| **R2:** Alle afwijzingen **moeten** gelogd worden naar Sentinel | Security audit trail vereist | Compliance failure |
| **R3:** Max processing time 250ms (p99) | Flux mag niet wachten | Auto-escalatie naar Flux met "degraded" flag |
| **R4:** Geen state in Nova nodes | Horizontal scaling vereist | Architectuur afwijking |
| **R5:** UIE/GIO schema's zijn **immutable** backwards compat | Data integriteit | Major version bump nodig |
| **R6:** Async routes **moeten** progress reporting hebben | Fea experience | UX failure |
| **R7:** Rate limits **moeten** per-actor-type configureerbaar zijn | Flexibele governance | Hardcoded = bug |

---

### Dependencies

| Afhankelijkheid | Type | Impact bij uitval |
|-----------------|------|-------------------|
| OpenClaw Runtime | Hard | Nova kan niet starten |
| Redis/RabbitMQ (queue) | Hard | GIO kan niet naar Flux, backlog ontstaat |
| Sentinel Security endpoint | Soft | Afwijzingen niet gelogd, maar requests blijven werken |
| Omni Config Service | Soft | Nova gebruikt cached regels (max 60s stale) |
| File Storage (S3/MinIO) | Hard (voor async routes) | Grote uploads falen |
| Language Detection Model | Soft | Fallback naar "unknown" + doorsturen |

---

### Decisions Made

| Beslissing | Alternatief | Argumentatie |
|------------|-------------|--------------|
| **Stateless design** | Stateful sessions in Nova | Schaalbaarheid > complexiteit. State zit in GIO + externe storage |
| **UIE/GIO scheiding** | Één enkel formaat | Scheiding van concerns: UIE = ruwe input, GIO = verrijkt voor Flux |
| **Push naar Flux (vs pull)** | Flux polled Nova | Lagere latency, maar hoger risico op queue overflow. Gecompenseerd door backpressure. |
| **Synchrone validatie** | Async validatie voor alles | 95% van requests is klein; async zou onnodige complexiteit toevoegen |
| **Hardcoded rate limits in config** | Dynamic ML-based limits | Voorspelbaarheid > optimalisatie. ML kan in Sentinel voor analyse, niet voor blocking. |
| **Geen content generation in Nova** | Nova doet eerste interpretatie | Nova mag geen antwoorden genereren — dat is Flux/Omni domein. Risico op verkeerde verwachtingen. |

---

### Decision Locked

**Owner:** Fea  
**Status:** Active  
**Version:** 2.1.0  
**Last Updated:** 2026-03-22

---

**Einde Block 02**

## Sequence Diagrams

### 1. Happy Path Flow

+--------+      +----------------+      +---------------+      +------------+
|  Fea   |----->| Intake Handler |----->|  Validation   |----->| Transform  |
| (User) |      |   (M02)        |      |   Engine      |      | Pipeline   |
+--------+      +----------------+      +---------------+      +------------+
                      |                       |                      |
                      v                       v                      v
               [UIE Created]          [All Checks Pass]      [GIO Created]
                      |                       |                      |
                      +-----------------------+----------------------+
                                              |
                                              v
                                       +------------+
                                       |    Flux    |
                                       |   Queue    |
                                       +------------+

### 2. Failure Path Flow

+--------+      +----------------+      +---------------+      +------------+
|  Fea   |----->| Intake Handler |----->|  Validation   |----->|   CHECK    |
| (User) |      |   (M02)        |      |   Engine      |      |   FAIL     |
+--------+      +----------------+      +---------------+      +------------+
                                              |                      |
                                              v                      v
                                       +------------+      +------------+
                                       |   Error    |      |  Sentinel  |
                                       |  Handler   |      |   Logging  |
                                       +------------+      +------------+
                                              |
                                              v
                                       +------------+
                                       |    Fea     |
                                       | Error Code |
                                       +------------+
