# Model Runtime & Providers
## Block 07 — Model Runtime Integration (OpenClaw)

---

### Purpose

OpenClaw is de **execution runtime** waarop ARC AI Agents draait. Het beheert de fysieke resources, model inference, en infrastructuur waar alle ARC-lagen op voortbouwen.

| Aspect | Functie |
|--------|---------|
| **Resource Management** | GPU/CPU allocatie, scaling, scheduling |
| **Model Serving** | LLM inference, embeddings, fine-tuning |
| **Sandboxing** | Veilige code-uitvoering voor Workers |
| **Observability** | Metrics, logging, tracing voor hele stack |

OpenClaw is de **fundering** — zonder OpenClaw draait ARC niet.

---

### System Context

**Positionering:**
- **Parent:** Geen — fundering voor alle ARC-lagen
- **Children:** Alle ARC-lagen (indirect via API's)
- **Peers:** Externe infrastructure (cloud providers, on-prem clusters)

---

### Concrete Structure

#### 7.1 Model Engine

| Component | Functie | Technologie |
|-----------|---------|-------------|
| Inference Server | LLM inference serving | vLLM, TGI, TensorRT-LLM |
| Embedding Engine | Text/vector embeddings | SentenceTransformers, OpenAI API |
| Batch Processor | Async batch jobs | Ray, Celery |
| Model Cache | Hot model loading | GPU memory management |

**Model Configuratie:**
- gpt4_arc: OpenAI API, max 100 concurrent, 30s timeout
- llama3_local: 70B Q4_K_M, 4x A100, 48GB VRAM, batch 16
- embedding_default: all-MiniLM-L6-v2, CUDA, batch 32

#### 7.2 Sandbox Runtime

| Type | Use Case | Isolatie Level |
|------|----------|----------------|
| gvisor_container | Code execution | Syscall filtering + user namespace |
| firecracker_microvm | Untrusted code | KVM virtualisatie |
| namespace_sandbox | Trusted tools | Linux namespaces only |

**Sandbox Resource Limits:**
- CPU: 1 core
- Memory: 512MB
- Disk: 1024MB
- Network: egress_only / none / full
- Timeout: 30s max
- Max processes: 10

#### 7.3 Resource Manager

| Functie | Implementatie | Metrics |
|---------|-------------|---------|
| GPU scheduling | Kubernetes + GPU operator | Utilization %, queue depth |
| Autoscaling | KEDA + Prometheus | Latency p95, request rate |
| Load balancing | Envoy + consistent hashing | Per-model distribution |
| Cost optimization | Spot instance fallback | Cost per 1k tokens |

#### 7.4 Storage Layer

| Component | Type | Data |
|-----------|------|------|
| Model Registry | Object storage | gguf, safetensors, ONNX |
| Vector Store | Vector DB | Pinecone, Weaviate, Milvus |
| Object Store | S3/MinIO | Files, logs, temp data |

### Flows

#### 7.1 Model Inference Request (van Worker)

Worker request → API Gateway → Model Router → Queue → Batch Manager → Inference Engine → GPU execution → Response streaming → Metrics logging

**Timing breakdown:**
- Gateway + Router: < 10ms
- Queue wait: 0-50ms
- Inference: 50-500ms
- Logging: async

#### 7.2 Sandbox Creation (voor Code Worker)

Sentinel request → Resource check → MicroVM creatie (Firecracker < 100ms) → Filesystem overlay → Network setup → Code + dependencies injecteren → Execution start → Cleanup trigger → MicroVM destroy + log capture

---

### Relaties met ARC-lagen

| ARC Laag | OpenClaw Service | Interface |
|----------|------------------|-----------|
| **Nova** | API Gateway | HTTP/gRPC |
| **Flux** | Context Store | Redis protocol |
| **Omni** | Vector Store | Native client |
| **Sentinel** | Task Queue | Message queue |
| **Workers** | Model API + Sandbox | Interne SDK |

**Critical:** ARC-lagen communiceren met OpenClaw via **abstracte interfaces**, niet direct met infrastructuur.

---

### Decision Logic

| Beslissing | Input | Output |
|------------|-------|--------|
| **Welk model?** | Requested model, load, cost | Geselecteerde model instantie |
| **GPU of CPU?** | Model size, latency, queue | Hardware target |
| **Sandbox type?** | Code source, trust, network | Isolatie level |
| **Scale up/down?** | Utilization, queue, budget | Replica count |

---

### Rules & Constraints

| Regel | Rationale |
|-------|-----------|
| **R1:** Model API's altijd via OpenClaw proxy | Centralized rate limiting, caching, failover |
| **R2:** GPU resources exclusief per model | Voorkomt interference, consistente latency |
| **R3:** Sandboxen max 30s levensduur | Resource rotatie, security |
| **R4:** Alle model calls gelogd | Audit trail, geen data leakage |
| **R5:** Fallback model bij primary failure | Availability garantie |
| **R6:** Cost attribution per ARC-laag | Budget management, optimalisatie |

---

### Dependencies

| Component | Type | Impact bij uitval |
|-----------|------|-------------------|
| GPU cluster | Hard | Geen LLM inference |
| Model weights storage | Hard | Geen model loading |
| Container runtime | Hard | Geen sandboxing |
| Network (intern) | Hard | Geen communicatie tussen lagen |
| Externe model API's | Soft | Fallback naar lokale modellen |

---

### Decisions Made

| Beslissing | Argumentatie |
|------------|--------------|
| **vLLM/TGI voor inference** | Throughput > latency voor batch |
| **gVisor/Firecracker voor sandbox** | Veiligheid > performance |
| **Kubernetes voor orchestratie** | Ecosysteem vs custom solution |
| **Spot instances voor cost** | Besparing > availability risk |

---

### Decision Locked

**Owner:** Fea  
**Status:** Active  
**Version:** 2.0.0  
**Last Updated:** 2026-03-22

---

**Einde Block 07**

## OpenClaw Integration Flow

+----------------+      +----------------+      +----------------+
|  Worker Result |----->|  OpenClaw      |----->|  Platform      |
|  (Output)      |      |  (M07)         |      |  Runtime       |
+----------------+      +----------------+      +----------------+
                               |
                               v
                        +----------------+
                        |  Systemd       |
                        |  Services      |
                        +----------------+
                               |
                               v
                        +----------------+
                        |  Hardened      |
                        |  Runner        |
                        +----------------+
