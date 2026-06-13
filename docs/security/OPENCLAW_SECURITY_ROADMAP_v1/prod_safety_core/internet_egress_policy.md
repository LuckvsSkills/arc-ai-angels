# B11 — Internet / Egress Policy

## Scope
Deze block definieert het outbound internetbeleid voor OpenClaw / Arc AI Angels.

Doel:
- default deny als uitgangspunt
- alleen noodzakelijke outbound toestaan
- per agenttype duidelijke egress scope bepalen
- risico op data exfiltration beperken

## 1. Security Principle

Uitgangspunt:
- outbound internet is niet standaard toegestaan
- elke uitzondering moet expliciet gemotiveerd zijn
- policies moeten per component beoordeeld worden

## 2. Component-based policy

### Nova
Nova heeft alleen outbound nodig voor:
- Telegram API
- model/provider APIs indien Nova die direct gebruikt

### Flux
Flux mag alleen gecontroleerd outbound hebben voor:
- expliciet goedgekeurde provider APIs
- strikt noodzakelijke documentatie / package / repo endpoints indien operationeel nodig

### Worker agents
Worker agents:
- deny by default
- alleen uitzonderen indien een specifieke taak dit vereist

### Gateway / lokale services
Gateway:
- bij voorkeur lokaal / loopback-only
- geen onnodig publiek outbound gedrag

## 3. Bekende relevante outbound dependencies

Op basis van huidige config / omgeving:

- Telegram
- OpenAI
- Gemini
- Moonshot
- Ollama lokaal op `127.0.0.1:11434`

## 4. Policy model

### Default policy
- deny by default

### Explicit allows
Alleen toestaan wat nodig is voor:
- messaging
- model inference
- strikt noodzakelijke operations

### Explicit deny
Verbieden:
- willekeurige browsing
- onbekende third-party APIs
- niet-goedgekeurde file exfiltration routes

## 5. Operational intent

Doel van deze block:
- eerst policy en verificatie scherp krijgen
- daarna pas technische enforcement doen
- productiebeleid baseren op minimale noodzakelijke egress

## 6. Verification goals

We willen kunnen verifiëren:
- welke dependencies echt nodig zijn
- welke processen outbound gebruiken
- welke services lokaal blijven
- welke hosts expliciet op allowlist moeten

## 7. Output van deze block

Deze block levert:
- egress beleid
- allow/deny denkrichting
- basis voor latere firewall / nftables / ufw enforcement

## 8. Runtime validation (Magneto)

Tijdens runtime inspectie zijn volgende eigenschappen bevestigd.

### Listening services

- openclaw-gateway
  - 127.0.0.1:50506
  - 127.0.0.1:50509

Gateway is correct beperkt tot localhost.

- development HTTP server
  - 0.0.0.0:8080
  - gebruikt voor documentatie / UI

### Active outbound connection

Gedetecteerde verbinding:

- Telegram servers
- TCP 443

Dit komt overeen met Nova messaging.

### Model providers configured

Configuratie bevat:

- Moonshot API
- Gemini API
- OpenAI API

### Local model endpoint

Configuratie ondersteunt:

- Ollama
- localhost:11434

Deze service draaide niet tijdens inspectie.

### Agent isolation

Agent instances:

- agent-01 t/m agent-50
- eigen env + allow files

Dit ondersteunt fine-grained runtime policies.

## 9. Security conclusion

B11 egress policy is consistent met runtime gedrag.

Outbound afhankelijkheden zijn beperkt tot:

- messaging
- model inference

Geen onverwachte externe endpoints gedetecteerd.

Block B11 kan als **validated** worden beschouwd.
