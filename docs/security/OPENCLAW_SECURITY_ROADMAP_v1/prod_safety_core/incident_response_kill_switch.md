# B09 — Incident Response / Kill Switch

## Scope
Deze block definieert hoe OpenClaw veilig gestopt, onderzocht en hersteld kan worden bij incidenten of ongewenst gedrag.

## 1. Doelstellingen

Doelen:
- agents snel veilig kunnen stoppen
- gateway / runtime kunnen isoleren
- bewijsmateriaal bewaren
- rollback / containment mogelijk maken
- snelle operator-acties definiëren

## 2. Te stoppen componenten

### Core runtime
- openclaw-nova.service
- openclaw-flux.service
- openclaw-gateway process

### Mogelijke aanvullende componenten
- web UI op 8080
- cron / jobs indien die verstorend werken

## 3. Kill switch principe

Een kill switch moet:
- snel uitvoerbaar zijn
- minimale kans op fouten hebben
- geen complexe afhankelijkheden hebben
- veilig zijn voor data en logs
- door operator handmatig uitvoerbaar zijn

## 4. Incident types

### Type A — Agent malfunction
Voorbeelden:
- runaway loop
- onbedoelde tool calls
- foutieve output
- ongewenste actieherhaling

### Type B — Runtime failure
Voorbeelden:
- service restart loop
- gateway down
- ontbrekende runtime directories
- config corruption

### Type C — Security incident
Voorbeelden:
- secret exposure
- unauthorized access
- verdachte log entries
- policy bypass

## 5. Eerste operatoracties

Bij incident:

1. bepaal of directe stop nodig is
2. stop Nova en Flux
3. verifieer gateway status
4. verzamel status en recente logs
5. noteer tijdstip / context
6. beslis over containment / restart

## 6. Bewijsmateriaal / evidence

Te bewaren:
- systemctl status outputs
- journalctl outputs
- runtime health check output
- relevante config state
- gatekeeper logs
- timestamps van operatoracties

## 7. Output van deze block

Deze block levert:
- incident structuur
- kill switch richting
- basis voor stop/recover scripts
- basis voor runbook en evidence handling

## 8. Operator Command Reference

### Service status

systemctl status openclaw-nova
systemctl status openclaw-flux

### Service start

sudo systemctl start openclaw-nova
sudo systemctl start openclaw-flux

### Service stop (kill switch)

sudo systemctl stop openclaw-nova
sudo systemctl stop openclaw-flux

### Service restart

sudo systemctl restart openclaw-nova
sudo systemctl restart openclaw-flux

### Logs

journalctl -u openclaw-nova -n 100
journalctl -u openclaw-flux -n 100

### Gateway process

pgrep -af openclaw-gateway

### Gateway ports

ss -ltnp | grep openclaw

### Runtime health check

~/arc_ai_angels/OPENCLAW_SECURITY_ROADMAP_v1/prod_safety_core/runtime_health_check.sh

### Full kill switch

sudo systemctl stop openclaw-nova openclaw-flux
pkill -f openclaw-gateway


## 9. Kill Switch Validation Results

Tijdens validatie bleek:

### Wat correct stopte
- `openclaw-nova.service`
- `openclaw-flux.service`
- alle `openclaw-agent@agent-*` services

### Gateway bevinding
De `openclaw-gateway` draaide niet onder een systemd service, maar als user-process onder de user systemd sessie van `prime`.

Validatie liet zien:
- gateway bleef initially draaien na kill switch script
- directe `kill -TERM <pid>` werkte wel
- gateway werd niet automatisch gerespawned

### Conclusie
De kill switch moet gateway-containment doen via expliciete PID-resolutie in plaats van alleen `pkill` patroonmatching.

B09 levert daarmee:
- werkende stop van Nova / Flux / agents
- evidence capture
- gevalideerde containment flow
- duidelijke operator procedure voor gateway stop
