# Block 14: Model Cache & Preloading

## Purpose

Het Model Cache & Preloading block optimaliseert model loading performance door intelligente caching en voorspellende preloading. Het reduceert latency voor inference requests door modellen in GPU/CPU memory te houden en anticipeert op welke modellen nodig zullen zijn.

Kernfuncties:
- **LRU caching** van hot models in GPU memory
- **Predictive preloading** gebaseerd op usage patterns
- **Tiered storage** (GPU -> CPU RAM -> Disk -> Remote)
- **Cache eviction** met graceful degradation


## System Context

Block 13 (Registry) -> Block 14 (Cache) -> Block 16 (Router)
Verbonden met: Block 15 (Resource Manager voor GPU/CPU quotas)


## Concrete Structure

### Components

1. **Cache Manager**: Beheert cache entries, TTL, eviction policies
2. **Preloader**: Anticipeert op model requests obv traffic patterns
3. **Tiered Storage**: GPU VRAM -> CPU RAM -> Local Disk -> Remote
4. **Memory Monitor**: Trackt gebruik en triggers cleanup bij druk


## Flows

1. **Cache Hit**: Request -> Cache check -> Direct return (< 10ms)
2. **Cache Miss**: Request -> Registry -> Load -> Cache -> Return
3. **Preloading**: Usage pattern analyse -> Predict next models -> Load
4. **Eviction**: Memory pressure -> LRU eviction -> Lower tier/Disk


## Rules & Constraints

- Max GPU cache: 80% van beschikbare VRAM
- Max CPU cache: 50% van beschikbare RAM
- Cache hit rate target: > 85%
- Preloading alleen tijdens low-traffic periods
- Eviction timeout: 5 minuten grace period voor hot models


## Dependencies

- Block 13 (Registry): Voor model metadata en artifact locaties
- Block 15 (Resource Manager): Voor GPU/CPU quota toewijzing
- Block 11 (Health Monitor): Voor memory pressure alerts
- Redis: Voor distributed cache state


## Decisions Made

1. **LRU eviction**: Eenvoudig en effectief voor ML workloads
2. **Tiered storage**: Balans tussen snelheid en capaciteit
3. **Async preloading**: Niet blokkeren voor running inference
4. **Redis voor state**: Shared cache state across instances


## Decision Locked

| Aspect | Keuze | Datum |
|--------|-------|-------|
| Eviction Policy | LRU | 2024-03-20 |
| Cache Tiers | 4-tier (GPU/CPU/Disk/Remote) | 2024-03-20 |
| State Backend | Redis | 2024-03-20 |
| Hit Rate Target | 85% | 2024-03-20 |
