# Supreme Flux - Communicatie Protocol

## Bericht Formaat (JSON)
{
  "timestamp": "2026-03-03T12:00:00Z",
  "source": "nova|gatekeeper|flux",
  "type": "command|response|status",
  "payload": {},
  "signature": "optional"
}

## Command Flow
1. Nova schrijft command naar nova_to_flux/
2. Gatekeeper valideert en voorziet van goedkeuring
3. Flux leest, voert uit, schrijft resultaat naar flux_to_nova/
4. Nova leest resultaat

## Fout Afhandeling
- Timeout na 300 seconden
- Onbekende commands = weigeren + loggen
- Crash = herstart met state recovery
