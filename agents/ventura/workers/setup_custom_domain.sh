#!/bin/bash
# setup_custom_domain.sh — Ventura worker
# Koppelt custom domein aan Vercel deployment
# Gebruik: bash setup_custom_domain.sh /pad/naar/PROJECT_BRIEF.json

BRIEF_PATH=$1
if [ -z "$BRIEF_PATH" ]; then
    echo "Gebruik: bash setup_custom_domain.sh /pad/naar/PROJECT_BRIEF.json"
    exit 1
fi

NAAM=$(python3 -c "import json; d=json.load(open('$BRIEF_PATH')); print(d['project_naam'].lower().replace(' ','-'))")
DOMEIN=$(python3 -c "import json; d=json.load(open('$BRIEF_PATH')); print(d.get('domein',''))")
VERCEL_TOKEN=$(grep "^VERCEL_TOKEN" /home/prime/.openclaw/.env | cut -d= -f2)

echo "🌐 Ventura domein setup: $DOMEIN"

if [ -z "$DOMEIN" ] || [[ "$DOMEIN" == *"vercel.app"* ]]; then
    echo "ℹ️  Geen custom domein opgegeven — Vercel subdomain wordt gebruikt"
    exit 0
fi

if [ -z "$VERCEL_TOKEN" ]; then
    echo "⚠️  Geen VERCEL_TOKEN — domein koppeling overgeslagen"
    exit 0
fi

# Vercel project ID ophalen
PROJECT_ID=$(curl -s "https://api.vercel.com/v9/projects/$NAAM" \
    -H "Authorization: Bearer $VERCEL_TOKEN" | \
    python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('id',''))" 2>/dev/null)

if [ -z "$PROJECT_ID" ]; then
    echo "⚠️  Project niet gevonden op Vercel: $NAAM"
    exit 1
fi

# Domein toevoegen
RESULT=$(curl -s -X POST "https://api.vercel.com/v10/projects/$PROJECT_ID/domains" \
    -H "Authorization: Bearer $VERCEL_TOKEN" \
    -H "Content-Type: application/json" \
    -d "{\"name\":\"$DOMEIN\"}" 2>/dev/null)

echo "✅ Domein gekoppeld: $DOMEIN"
echo "ℹ️  DNS instelling vereist: CNAME $DOMEIN → cname.vercel-dns.com"

python3 << PYEOF
import json
with open('$BRIEF_PATH') as f:
    brief = json.load(f)
if 'deploy' in brief:
    brief['deploy']['custom_domain'] = '$DOMEIN'
    brief['deploy']['dns_required'] = 'CNAME $DOMEIN cname.vercel-dns.com'
with open('$BRIEF_PATH', 'w') as f:
    json.dump(brief, f, indent=2, ensure_ascii=False)
print('✅ PROJECT_BRIEF bijgewerkt met domein info')
PYEOF

echo "=================================================="
echo "✅ VENTURA DOMEIN KLAAR"
echo "   Domein: $DOMEIN"
echo "   DNS: CNAME → cname.vercel-dns.com"
echo "=================================================="
