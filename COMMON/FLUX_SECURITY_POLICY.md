# Supreme Flux - Security Policy

## Toegestane Operaties
- File operaties in /home/prime/arc_ai_angels/supreme_flux/
- Git operaties (status, log, diff, pull)
- Systeem info (ps, df, du, free)
- Netwerk info (ping, netstat)

## Verboden Operaties
- Alle commands in NOVA_BLOCKED_COMMANDS
- Schrijven buiten toegestane paden
- Executie zonder Gatekeeper goedkeuring

## Communicatie
- Input: /home/prime/arc_ai_angels/shared/nova_to_flux/
- Output: /home/prime/arc_ai_angels/shared/flux_to_nova/
- Formaat: JSON met timestamp, command, status
