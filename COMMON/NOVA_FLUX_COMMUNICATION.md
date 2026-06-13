# NOVA ↔ FLUX Communication Protocol

## Current Problem
- NOVA sends requests to FLUX
- FLUX processes & might delay
- Response is slow
- No structured request/response pattern
- FLUX might loop back to NOVA unnecessarily

## Required Pattern

### Fast Communication Requirements

**1. REQUEST/RESPONSE (Synchronous)**
NOVA: "What's current system status?"
↓ (instant question)
FLUX: ✓ Status returned (< 500ms)
↓ (direct answer)
NOVA: Processes & acts
**2. DIRECT ANSWER (no loops)**
❌ NOVA → FLUX → NOVA → FLUX (back and forth)
✅ NOVA → FLUX → Answer (one round trip)
**3. ACTION + NEXT STEP (atomic)**
NOVA: "Add cronjob X, then Y"
FLUX: ✓ Job added + Y initiated (one action)
(Not: "added, now what?")
## Protocol Design Needed

### Message Format
```json
{
  "id": "req-12345",
  "from": "nova",
  "to": "flux",
  "type": "request|command|query",
  "action": "cronjob_add|status_check|agent_list",
  "priority": "urgent|normal|background",
  "payload": {...},
  "expect_response": true,
  "timeout_ms": 5000,
  "next_action_if_success": "...",
  "next_action_if_fail": "..."
}
```

### Response Format
```json
{
  "id": "req-12345",
  "status": "success|error",
  "result": {...},
  "action_taken": "...",
  "next_action": "..."
}
```

## Implementation

### Option 1: WebSocket Direct (Fastest)
- NOVA ↔ FLUX direct WebSocket
- Request/response protocol
- Latency: <100ms

### Option 2: Redis Queue
- NOVA pushes request
- FLUX processes immediately
- Returns via response queue
- Latency: 100-300ms

### Option 3: REST API
- FLUX exposes endpoints
- NOVA calls directly
- Latency: 200-500ms

### Option 4: OpenClaw Native
- Use OpenClaw message passing
- Built-in pub/sub
- Latency: 50-200ms

## Status
⏳ DISCUSS: Which protocol? WebSocket? Redis? REST?
⏳ Define: Timeout behavior, retry logic, error handling
