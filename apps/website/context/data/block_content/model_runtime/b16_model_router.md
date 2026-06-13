# Block 16: Model Router

## Purpose

Het Model Router block bepaalt welk model instance een request afhandelt. Het routeert requests op basis van model versie, tenant, load balancing rules, en beschikbaarheid. Het is de traffic cop van het inference systeem.

Kernfuncties:
- **Request routing**: Kiest optimale model instance
- **Version routing**: A/B testing en canary deployments
- **Tenant isolation**: Dedicated vs shared instances
- **Failover**: Redirect bij instance failure


## System Context

Block 15 (Resource Manager) -> Block 16 (Router) -> Block 18 (Inference Engine)
Input van: API Gateway, Load Balancer


## Concrete Structure

### Components

1. **Route Resolver**: Bepaalt target model obv request metadata
2. **Load Balancer**: Verdeelt over healthy instances
3. **Version Manager**: Handhaaft routing rules per versie
4. **Failover Handler**: Detecteert failures en redirect


## Flows

1. **Standard**: Request -> Parse -> Route -> Instance -> Forward
2. **Canary**: 90% v1, 10% v2 routing met metrics tracking
3. **Failover**: Primary down -> Health check fail -> Backup route
4. **Tenant**: Identify tenant -> Dedicated pool -> Route


## Rules & Constraints

- Routing decision < 5ms
- Health checks elke 10 seconden
- Max 3 retry attempts per request
- Sticky sessions voor stateful modellen
- Circuit breaker na 5 consecutive failures


## Dependencies

- Block 11 (Health Monitor): Instance health status
- Block 13 (Registry): Model versie metadata
- Block 15 (Resource Manager): Resource availability
- Block 18 (Inference Engine): Instance endpoints


## Decisions Made

1. **Layer 7 routing**: HTTP header based vs IP based
2. **Client-side discovery**: Router kent alle instances
3. **Weighted routing**: Eenvoudige canary implementatie
4. **Stateless router**: Geen session state in router


## Decision Locked

| Aspect | Keuze | Datum |
|--------|-------|-------|
| Routing Level | Layer 7 (HTTP) | 2024-03-20 |
| Discovery | Client-side | 2024-03-20 |
| Canary Support | Weighted routing | 2024-03-20 |
| Health Check | 10s interval | 2024-03-20 |
