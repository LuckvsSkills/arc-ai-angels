# Block 13: Model Registry & Versioning

## Purpose

Het Model Registry & Versioning block vormt het centrale beheersysteem voor alle AI-modellen binnen de ARC runtime.
- **Centrale catalogus** voor alle geregistreerde modellen
- **Audit trail** voor wijzigingen en deployments
- **Governance hub** voor goedkeuringsworkflows
- **Artifact repository** voor model binaries
- **Version control system** voor ML workflows


## System Context

Block 12 (Provider Factory) -> Block 13 (Registry) -> Block 14 (Cache)
Ook verbonden met: Artifact Storage, Metadata DB, Version Control


## Concrete Structure

### Components

1. **Registry Core**: Model registratie, metadata opslag
2. **Version Controller**: Semantische versioning (MAJOR.MINOR.PATCH)
3. **Artifact Manager**: Opslag en retrieval van model binaries
4. **Governance Engine**: Compliance checks en approval workflows


## Flows

1. **Registration**: CI/CD -> Registry -> Artifact Store -> Metadata DB
2. **Retrieval**: Client -> Registry -> Cache Check -> Artifact Download
3. **Promotion**: Dev -> Staging -> Production (met governance checks)


## Rules & Constraints

- Artifacts zijn IMMUTABLE na registratie
- Versie format: MAJOR.MINOR.PATCH[-EXPERIMENT]
- Retentie: Production 7 jaar, Dev 90 dagen
- Metadata queries < 50ms (p95)
- Artifact retrieval < 5s voor modellen < 10GB


## Dependencies

- PostgreSQL 14+ (metadata)
- S3-compatible storage (artifacts)
- Redis/RabbitMQ (async jobs)
- Block 11 (Health Monitor), Block 15 (Resource Manager)


## Decisions Made

1. **PostgreSQL + Object Storage apart**: query performance vs kosten
2. **SemVer voor ML**: duidelijke breaking change indicatie
3. **Stages los van versies**: versie kan door dev/staging/prod heen
4. **Async governance**: security scans duren minuten


## Decision Locked

| Aspect | Keuze | Datum |
|--------|-------|-------|
| Database | PostgreSQL | 2024-03-15 |
| Storage | S3-API | 2024-03-15 |
| Versioning | SemVer-ML | 2024-03-15 |
| Encryptie | At-rest verplicht | 2024-03-20 |

## Architecture Overview

### Data Flow Patterns

**1. Request Flow:**

**2. Model Loading Flow:**

**3. Scaling Flow:**

### Integration Points

| Source | Target | Protocol | Purpose |
|--------|--------|----------|---------|
| M02 | M03 | Internal API | Intent routing |
| M03 | M10 | gRPC | Orchestration |
| M05 | M14 | REST | Model fetch |
| M13 | M15 | SQL | Resource alloc |
| M16 | M17 | Events | Routing updates |

## Architecture Overview

Complete system architecture showing all 17 blocks and their relationships:

+-----------------------------------------------------------------------------+
|                     ARC AI ANGELS - MODEL RUNTIME                             |
|                Complete Architecture (All 17 Blocks)                          |
+-----------------------------------------------------------------------------+
|                                                                             |
|  [M01 Runtime] -> [M02 Nova] -> [M03 Flux] -> [M04 Omni]                     |
|       |              |              |              |                        |
|       v              v              v              v                         |
|  [M05 Sentinel] -> [M06 Workers] -> [M07 OpenClaw] -> [M08 Direct]            |
|       |              |              |              |                        |
|       v              v              v              v                         |
|  [M09 Team] -> [M10 Orch] -> [M11 Governance] -> [M12 Build]              |
|       |              |              |              |                        |
|       v              v              v              v                         |
|  [M13 Comm] -> [M14 Flux-Sent] -> [M15 Protocol] -> [M16 Queue]             |
|       |              |              |              |                        |
|       +--------------+--------------+--------------+                        |
|                      |                                                       |
|                      v                                                       |
|           [M17 Routing Blueprint]                                            |
|                                                                             |
|  DATA LAYERS: [B13 Registry] [B14 Cache] [B15 Resources] [B17 Scaling]      |
|                                                                             |
+-----------------------------------------------------------------------------+
