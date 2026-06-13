# Security Guide

## File Rechten
.env: chmod 600 (alleen jij)
.openclaw: chmod 700 (alleen jij)
Gatekeeper: chmod 700 (alleen jij)

## Wat wordt geblokkeerd
- Sudo commands
- /etc, /root, /bin toegang
- Command injection (; && ||)
- Wildcards (rm *)

## Test
Goed: ~/arc_ai_angels/gatekeeper/gatekeeper.sh 'ls -la'
Slecht: ~/arc_ai_angels/gatekeeper/gatekeeper.sh 'sudo cat /etc/passwd'
