---
name: cloudflare-manager
description: "Beheer Cloudflare tunnel en DNS voor arc-vortex.nl."
metadata: { "openclaw": { "emoji": "☁️" } }
---
# Cloudflare Manager

Gebruik deze skill voor Cloudflare operaties.

## Cloudflare tunnel beheer

### Status checken
```bash
# Check tunnel status
curl -s http://localhost:8000/api/system/services | python3 -c "
import json,sys; d=json.load(sys.stdin)
for s in d['services']:
    if s['id'] == 'cloudflare':
        print(s['status'])
"
```

### Tunnel herstarten
```bash
# Via systemd indien geconfigureerd
systemctl --user restart cloudflared
```

## DNS configuratie arc-vortex.nl
Huidige setup:
- `arc-vortex.nl` → Cloudflare tunnel → poort 3002 (Vite)
- Tunnel naam: arc-vortex

## Custom domein koppelen aan Vercel project
1. Voeg domein toe in Vercel dashboard
2. Voeg CNAME record toe in Cloudflare:
   - Name: `[subdomain]`
   - Target: `cname.vercel-dns.com`
3. Wacht op SSL certificaat (automatisch)
4. Verifieer via browser

## Subdomein voor nieuw project
klant-naam.arc-vortex.nl → Vercel project
Stappen:
1. Vercel: voeg custom domein toe
2. Cloudflare: maak CNAME aan
3. Wacht 5-10 minuten
4. Check HTTPS werkt
