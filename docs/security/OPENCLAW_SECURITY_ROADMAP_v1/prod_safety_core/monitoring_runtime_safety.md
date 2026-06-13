# B08 — Monitoring / Runtime Safety

## Scope
Deze block definieert de minimale monitoring- en runtime safety-laag voor de huidige OpenClaw / Arc AI Angels omgeving.

## 1. Te monitoren componenten

### Core services
- openclaw-nova.service
- openclaw-flux.service
- openclaw-gateway process

### Network bindings
- 127.0.0.1:50506
- 127.0.0.1:50509

### Filesystem / state
- ~/.openclaw/.env
- ~/.openclaw/openclaw.json
- ~/.openclaw/memory/*.sqlite
- ~/arc_ai_angels/gatekeeper/logs
- ~/arc_ai_angels/gatekeeper/policies

### Capacity
- disk usage
- memory usage
- process availability

## 2. Monitoring goals

Doelen:
- snel zien of Nova / Flux draaien
- snel zien of gateway leeft
- zien of kritieke bestanden nog bestaan
- basis signalen geven bij runtime failure
- voorbereiding op latere alerts / queue safety

## 3. Minimal health checks

### Service checks
- systemctl is-active openclaw-nova
- systemctl is-active openclaw-flux

### Process checks
- pgrep -af openclaw-gateway

### Port checks
- ss -ltnp | grep 50506
- ss -ltnp | grep 50509

### File checks
- test -f ~/.openclaw/.env
- test -f ~/.openclaw/openclaw.json
- ls ~/.openclaw/memory/*.sqlite

### Capacity checks
- df -h
- free -h

## 4. Output van deze block
Deze block levert:
- monitoring scope
- minimale health checks
- basis voor een runtime health script

## 5. Runtime Failure Found During Validation

Tijdens healthcheck validatie bleken beide services niet healthy te zijn.

### Symptoom
- `openclaw-nova` bleef op `activating`
- `openclaw-flux` bleef op `activating`

### Root cause
Beide services faalden met:
- `status=226/NAMESPACE`
- `Failed to set up mount namespacing`
- ontbrekend pad: `/run/openclaw/env`

De systemd units gebruiken:
- `EnvironmentFile=-/run/openclaw/env/*.env`
- `ReadWritePaths=/run/openclaw`

Wanneer `/run/openclaw` niet bestaat, faalt de service al vóór startup.

## 6. Fix Applied

### Tijdelijke fix
Aangemaakt:
- `/run/openclaw`
- `/run/openclaw/env`

Daarna startten beide services correct:
- `openclaw-nova` → active (running)
- `openclaw-flux` → active (running)

### Permanente fix
Bestand toegevoegd:
- `/etc/tmpfiles.d/openclaw.conf`

Met:
- `d /run/openclaw 0755 root root -`
- `d /run/openclaw/env 0755 root root -`

Hiermee worden de runtime directories automatisch aangemaakt bij boot.

## 7. Conclusie

Deze block leverde niet alleen monitoring op, maar detecteerde ook een concrete runtime failure en herstelde deze structureel.

Status:
- monitoring basis aanwezig
- healthcheck script aanwezig
- runtime failure gedetecteerd
- root cause bevestigd
- permanente fix toegepast
