---
name: pipeline-builder
description: "Ontwerp en bouw CI/CD pipelines voor ARC AI Agents projecten."
metadata: { "openclaw": { "emoji": "🚀" } }
---
# Pipeline Builder

Gebruik deze skill voor het bouwen van deployment pipelines.

## ARC AI Agents standaard pipeline
STAP 1 — Code gereed (Forge)
↓
STAP 2 — Security audit (Nero)
↓ groen licht
STAP 3 — Build check
→ npm install / pip install
→ syntax check
↓
STAP 4 — Deploy naar Vercel (Ventura)
→ vercel --prod
↓
STAP 5 — Health check
→ curl live URL
→ response code 200?
↓
STAP 6 — Notify Cortexia
→ live URL rapporteren

## Pipeline types

### Statische website pipeline
```bash
# 1. Valideer HTML
# 2. Optimaliseer CSS/JS
# 3. Deploy naar Vercel
# 4. Check live URL
```

### React app pipeline
```bash
# 1. npm install
# 2. npm run build
# 3. Check build output
# 4. Deploy naar Vercel
# 5. Check live URL
```

### FastAPI backend pipeline
```bash
# 1. pip install -r requirements.txt
# 2. Python syntax check
# 3. Deploy naar Vercel of server
# 4. Health endpoint check
```

## Pipeline status tracking
Gebruik TASKS.md voor pipeline voortgang:
PIPELINE: [project-naam]
Stap 1 — Code: ✅
Stap 2 — Security: ✅
Stap 3 — Build: ✅
Stap 4 — Deploy: ⏳
Stap 5 — Health: ⏳
Status: IN PROGRESS
