# M16 — Task Queue Structure

## Scope
Dit document definieert de eerste task queue structuur voor ARC / OpenClaw.

## 1. Doel

De queue moet taken kunnen vasthouden voor:
- Flux
- sentinels
- lead agents
- workers

## 2. Directorystructuur

shared/tasks/
- inbox/
- in_progress/
- done/
- failed/

## 3. Betekenis

### inbox
Nieuwe taken die nog niet verwerkt zijn.

### in_progress
Taken die actief worden uitgevoerd.

### done
Succesvol afgeronde taken.

### failed
Taken die zijn mislukt of handmatige aandacht nodig hebben.

## 4. Eerste taakmodel

Elke taak moet minimaal bevatten:
- task_id
- created_at
- created_by
- routed_by
- target_type
- target_name
- parent_task_id
- status
- priority
- summary
- payload

## 5. Doeltypes

Mogelijke target_types:
- flux
- direct_interface_agent
- sentinel
- lead_agent
- worker

## 6. Routingvoorbeeld

Operator vraagt iets aan Nova.

Stroom:
- Nova vertaalt vraag
- Flux ontvangt
- Flux maakt/routeert taak
- taak gaat naar juiste lead agent
- lead agent verdeelt subtaak
- worker levert resultaat terug
- taak schuift door statuses

## 7. Eerste ontwerpregel

Queue is ondersteunend aan OpenClaw sessions en shared structuur.

Dus:
- session communicatie blijft live pad
- queue wordt ondersteunende runtime-laag voor tracking, routing en state

## 8. JSON taakvoorbeeld

{
  "task_id": "task-0001",
  "created_at": "2026-03-14T18:30:00Z",
  "created_by": "Nova",
  "routed_by": "Flux",
  "target_type": "lead_agent",
  "target_name": "Nero",
  "parent_task_id": null,
  "status": "inbox",
  "priority": "high",
  "summary": "Controleer security risico op prompt injectie",
  "payload": {
    "sentinel": "Sentinel Security",
    "requested_action": "analyse"
  }
}

## 9. Output van M16

M16 levert:
- queue directory model
- taakstatusmodel
- eerste taakobject-structuur
- basis voor Flux routing blueprint
---

## Queue

\`\`\`mermaid
flowchart LR
    I[Input] --> Q[(Queue)]
    Q --> P[Process]
    P --> D[Done]
\`\`\`