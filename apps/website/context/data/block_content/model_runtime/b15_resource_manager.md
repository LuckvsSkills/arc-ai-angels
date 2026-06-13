# Block 15: Resource Manager

## Purpose

Het Resource Manager block beheert alle compute resources (GPU, CPU, memory) voor model inference. Het zorgt voor eerlijke verdeling van resources tussen verschillende modellen en tenants, en voorkomt resource starvation.

Kernfuncties:
- **Resource allocation**: GPU/CPU/memory toewijzing aan modellen
- **Quota enforcement**: Limieten per tenant/model
- **Load balancing**: Verdeling over multiple GPUs/nodes
- **Resource reclamation**: Cleanup van idle resources


## System Context

Block 14 (Cache) <- Block 15 (Resource Manager) -> Block 16 (Router)
Ook verbonden met: Block 11 (Health Monitor), Block 17 (Scaling)


## Concrete Structure

### Components

1. **Resource Allocator**: Toewijzing van GPU/CPU/memory aan requests
2. **Quota Manager**: Handhaaft limieten per tenant en model
3. **Load Balancer**: Verdeelt load over beschikbare resources
4. **Reclaimer**: Ruimt idle resources op na timeout


## Flows

1. **Allocation**: Request -> Quota check -> Resource assign -> Grant
2. **Reclamation**: Idle detect -> Warning -> Cleanup -> Release
3. **Rebalancing**: Load monitor -> Imbalance detect -> Migrate
4. **Failure**: Resource unavailable -> Queue -> Retry/Redirect


## Rules & Constraints

- Max 1 model per GPU (optimal voor grote modellen)
- Multi-tenant isolatie verplicht
- Resource request timeout: 30 seconden
- Idle reclamation na 10 minuten geen requests
- Emergency reserve: 10% GPU memory voor critical requests


## Dependencies

- Block 11 (Health Monitor): Resource health status
- Block 14 (Cache): Memory usage coordination
- Block 17 (Scaling): Signalering voor scale-up/down
- Kubernetes/Docker: Container orchestratie


## Decisions Made

1. **1-GPU-1-Model**: Simpele scheduling, optimale performance
2. **Tenant quotas**: Fair sharing tussen teams
3. **Async reclamation**: Niet blokkeren voor running inference
4. **Priority classes**: Critical > Normal > Background


## Decision Locked

| Aspect | Keuze | Datum |
|--------|-------|-------|
| GPU Sharing | 1 model per GPU | 2024-03-20 |
| Quota System | Per tenant + per model | 2024-03-20 |
| Reclaim Timeout | 10 minuten | 2024-03-20 |
| Emergency Reserve | 10% | 2024-03-20 |
