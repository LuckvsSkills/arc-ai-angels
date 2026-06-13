---
name: git-workflow
description: "Git workflow voor ARC AI Agents projecten — commit conventies, branches en GitHub management."
metadata: { "openclaw": { "emoji": "🌿" } }
---
# Git Workflow

Gebruik deze skill voor alle git operaties in ARC AI Agents projecten.

## Repository setup
```bash
cd /project-dir
git init
git remote add origin https://github.com/LuckvsSkills/[project-naam].git
echo "node_modules/" > .gitignore
echo ".env" >> .gitignore
echo "__pycache__/" >> .gitignore
git add -A
git commit -m "initial: project setup"
git branch -M main
git push -u origin main
```

## Commit conventies
feat:     nieuwe feature
fix:      bug fix
style:    CSS/design wijzigingen
refactor: code herstructurering
docs:     documentatie update
deploy:   deployment gerelateerd
security: security fix

Voorbeelden:
- `feat: voeg winkelwagen toe`
- `fix: herstel mobiele navigatie`
- `deploy: vercel productie deploy`

## Branch strategie
- `main` — productie code
- `dev` — development
- `feature/[naam]` — nieuwe features

## ARC AI Agents deploy flow
1. Code klaar → commit naar main
2. Push naar GitHub
3. Vercel pikt automatisch op
4. Ventura monitort deploy status

## GitHub token
Token staat in `/home/prime/.openclaw/.env` als `GITHUB_TOKEN`
Gebruik: `git remote set-url origin https://$GITHUB_TOKEN@github.com/LuckvsSkills/[repo].git`
