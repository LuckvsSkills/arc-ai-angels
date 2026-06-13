# Block 17: Auto Scaling

## Purpose

Het Auto Scaling block beheert dynamische schaling van model instances op basis van vraag. Het scalet horizontaal (meer instances) en verticaal (grotere/smaller resources) om kosten te optimaliseren en performance te garanderen.

Kernfuncties:
- **Horizontal scaling**: Meer/fewer instances obv load
- **Vertical scaling**: GPU/CPU/memory aanpassingen
- **Predictive scaling**: Anticiperen op load patterns
- **Cost optimization**: Balans tussen performance en kosten


## System Context

Block 11 (Health Monitor) -> Block 17 (Auto Scaling) -> Block 15 (Resource Manager)
Input metrics van: Block 14 (Cache), Block 16 (Router)


## Flows

1. **Scale Up**: High load -> Metric trigger -> Decision -> Provision -> Ready
2. **Scale Down**: Low load -> Cooldown check -> Drain -> Terminate
3. **Predictive**: Pattern detect -> Forecast -> Pre-scale -> Verify
4. **Emergency**: Sudden spike -> Bypass cooldown -> Fast scale


## Flows

1. **Scale Up**: High load -> Metric trigger -> Decision -> Provision -> Ready
2. **Scale Down**: Low load -> Cooldown check -> Drain -> Terminate
3. **Predictive**: Pattern detect -> Forecast -> Pre-scale -> Verify
4. **Emergency**: Sudden spike -> Bypass cooldown -> Fast scale


## Rules & Constraints

- Scale up: Max 1 instance per 30 seconden
- Scale down cooldown: 5 minuten na scale up
- Min instances: 1 (voor productie modellen)
- Max instances: 100 per model
- Target utilization: 70% (CPU) / 80% (GPU)


## Dependencies

- Block 11 (Health Monitor): Instance health voor scaling decisions
- Block 15 (Resource Manager): Resource availability checks
- Block 14 (Cache): Hit rates als scaling metric
- Kubernetes/AWS/GCP: Orchestration API voor provisioning


## Decisions Made

1. **Horizontal first**: Liever meer kleine instances dan grotere
2. **Cooldown periods**: Voorkomt flapping (snel op/neer)
3. **Predictive scaling**: Voor bekende patterns (dagelijks verkeer)
4. **Cost-aware**: Geen scaling als kosten > opbrengst


## Decision Locked

| Aspect | Keuze | Datum |
|--------|-------|-------|
| Scaling Type | Horizontal priority | 2024-03-20 |
| Scale Up Rate | 1 per 30s | 2024-03-20 |
| Cooldown | 5 minuten | 2024-03-20 |
| Target Util | 70% CPU / 80% GPU | 2024-03-20 |
