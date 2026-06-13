#!/bin/bash
# deploy_website.sh — Forge worker
# Gebruik: ./deploy_website.sh "project-naam" "/pad/naar/code"
# Bouwt en deployt een website naar Vercel

PROJECT_NAME=$1
CODE_PATH=$2
VERCEL_TOKEN=$(grep "^VERCEL_TOKEN" /home/prime/.openclaw/.env | cut -d= -f2)

if [ -z "$PROJECT_NAME" ] || [ -z "$CODE_PATH" ]; then
    echo "Gebruik: ./deploy_website.sh project-naam /pad/naar/code"
    exit 1
fi

echo "🚀 Deploying $PROJECT_NAME naar Vercel..."

# Stap 1 — GitHub repo aanmaken
echo "📁 Stap 1: GitHub repo aanmaken..."
GITHUB_TOKEN=$(grep "^GITHUB_TOKEN" /home/prime/.openclaw/.env | cut -d= -f2)
if [ ! -z "$GITHUB_TOKEN" ]; then
    curl -s -X POST https://api.github.com/user/repos \
        -H "Authorization: token $GITHUB_TOKEN" \
        -H "Content-Type: application/json" \
        -d "{\"name\":\"$PROJECT_NAME\",\"private\":false,\"auto_init\":true}" | python3 -c "
import json,sys; d=json.load(sys.stdin)
print('GitHub repo:', d.get('html_url','FAIL: '+str(d.get('message',''))))"
fi

# Stap 2 — Code naar GitHub pushen
echo "📤 Stap 2: Code pushen naar GitHub..."
cd $CODE_PATH
git init 2>/dev/null || true
git add -A
git commit -m "Initial deploy via ARC AI Agents — Forge" 2>/dev/null || true
git remote add origin "https://github.com/LuckvsSkills/$PROJECT_NAME.git" 2>/dev/null || true
git push -u origin main 2>/dev/null || git push -u origin master 2>/dev/null

# Stap 3 — Vercel deploy
echo "🌐 Stap 3: Vercel deploy..."
cd $CODE_PATH
npx vercel --token $VERCEL_TOKEN --yes --name $PROJECT_NAME 2>/dev/null
if [ $? -eq 0 ]; then
    echo "✅ Deploy succesvol!"
    echo "🌐 URL: https://$PROJECT_NAME.vercel.app"
else
    # Fallback: Vercel API direct
    curl -s -X POST https://api.vercel.com/v13/deployments \
        -H "Authorization: Bearer $VERCEL_TOKEN" \
        -H "Content-Type: application/json" \
        -d "{\"name\":\"$PROJECT_NAME\",\"gitSource\":{\"type\":\"github\",\"repoId\":\"LuckvsSkills/$PROJECT_NAME\",\"ref\":\"main\"}}" | python3 -c "
import json,sys; d=json.load(sys.stdin)
print('Deploy URL:', d.get('url','FAIL'))"
fi

echo "✅ Forge — deploy_website.sh voltooid"
