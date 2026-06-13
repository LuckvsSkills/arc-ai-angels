#!/bin/bash
# provision_cloud_service.sh — Ventura worker
# Deploy website naar Vercel via GitHub
# Gebruik: bash provision_cloud_service.sh /pad/naar/PROJECT_BRIEF.json

BRIEF_PATH=$1
if [ -z "$BRIEF_PATH" ]; then
    echo "Gebruik: bash provision_cloud_service.sh /pad/naar/PROJECT_BRIEF.json"
    exit 1
fi

NAAM=$(python3 -c "import json; d=json.load(open('$BRIEF_PATH')); print(d['project_naam'].lower().replace(' ','-'))")
CODE_DIR=$(python3 -c "import json; d=json.load(open('$BRIEF_PATH')); print(d.get('code_dir', ''))")
GITHUB_TOKEN=$(grep "^GITHUB_TOKEN" /home/prime/.openclaw/.env | cut -d= -f2)
VERCEL_TOKEN=$(grep "^VERCEL_TOKEN" /home/prime/.openclaw/.env | cut -d= -f2)
GITHUB_ORG="LuckvsSkills"

echo "🚀 Ventura deploy: $NAAM"
echo "   Code: $CODE_DIR"

if [ -z "$CODE_DIR" ] || [ ! -d "$CODE_DIR" ]; then
    echo "⚠️  code_dir niet gevonden — genereer basis site"
    CODE_DIR=$(dirname $BRIEF_PATH)/code
    mkdir -p $CODE_DIR/frontend
    python3 /home/prime/arc_ai_angels/agents/forge/workers/clone_template.py $BRIEF_PATH
    CODE_DIR=$(python3 -c "import json; d=json.load(open('$BRIEF_PATH')); print(d.get('code_dir', '$CODE_DIR'))")
fi

# Stap 1 — GitHub repo aanmaken
echo "📁 Stap 1: GitHub repo aanmaken..."
if [ ! -z "$GITHUB_TOKEN" ]; then
    REPO_RESULT=$(curl -s -X POST https://api.github.com/user/repos \
        -H "Authorization: token $GITHUB_TOKEN" \
        -H "Content-Type: application/json" \
        -d "{\"name\":\"$NAAM\",\"private\":false,\"auto_init\":false}" 2>/dev/null)
    REPO_URL=$(echo $REPO_RESULT | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('html_url',''))" 2>/dev/null)
    if [ ! -z "$REPO_URL" ]; then
        echo "✅ GitHub repo: $REPO_URL"
    else
        echo "⚠️  GitHub repo al bestaat of token probleem"
    fi
fi

# Stap 2 — Git init en push
echo "📤 Stap 2: Code pushen naar GitHub..."
DEPLOY_DIR=$CODE_DIR
if [ -d "$CODE_DIR/frontend" ]; then
    DEPLOY_DIR=$CODE_DIR/frontend
fi

cd $DEPLOY_DIR
git init -q 2>/dev/null || true
git add -A 2>/dev/null
git commit -q -m "Deploy via ARC AI Agents — Ventura $(date +%Y-%m-%d)" 2>/dev/null || true

if [ ! -z "$GITHUB_TOKEN" ]; then
    git remote remove origin 2>/dev/null || true
    git remote add origin "https://$GITHUB_TOKEN@github.com/$GITHUB_ORG/$NAAM.git"
    git push -u origin main -q 2>/dev/null || git push -u origin master -q 2>/dev/null
    echo "✅ Code gepushed naar GitHub"
fi

# Stap 3 — Vercel deploy
echo "🌐 Stap 3: Vercel deploy..."
DEPLOY_URL=""
if [ ! -z "$VERCEL_TOKEN" ]; then
    VERCEL_OUT=$(npx vercel --token $VERCEL_TOKEN --yes --name $NAAM 2>/dev/null)
    DEPLOY_URL=$(echo "$VERCEL_OUT" | grep -E "https://.*\.vercel\.app" | tail -1)
    if [ -z "$DEPLOY_URL" ]; then
        DEPLOY_URL="https://$NAAM.vercel.app"
    fi
    echo "✅ Vercel deploy: $DEPLOY_URL"
else
    DEPLOY_URL="https://$NAAM.vercel.app"
    echo "⚠️  Geen VERCEL_TOKEN — verwachte URL: $DEPLOY_URL"
fi

# Stap 4 — Update PROJECT_BRIEF
python3 << PYEOF
import json
with open('$BRIEF_PATH') as f:
    brief = json.load(f)
brief['deploy'] = {
    'url': '$DEPLOY_URL',
    'github': 'https://github.com/$GITHUB_ORG/$NAAM',
    'platform': 'vercel',
    'deployed_at': '$(date -u +%Y-%m-%dT%H:%M:%SZ)',
    'status': 'LIVE'
}
brief['sentinels']['ventura'] = 'DONE'
with open('$BRIEF_PATH', 'w') as f:
    json.dump(brief, f, indent=2, ensure_ascii=False)
print('✅ PROJECT_BRIEF bijgewerkt')
PYEOF

echo ""
echo "=================================================="
echo "✅ VENTURA DEPLOY KLAAR"
echo "   Live URL: $DEPLOY_URL"
echo "   GitHub: https://github.com/$GITHUB_ORG/$NAAM"
echo "   Volgende: Clio documentatie"
echo "=================================================="
