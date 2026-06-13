# Deployment Guide — TestWebshop

## Tech stack
React+FastAPI+Stripe

## GitHub repository
https://github.com/LuckvsSkills/testwebshop

## Vercel deployment

### Eerste keer deployen
```bash
npm install -g vercel
vercel --token $VERCEL_TOKEN --yes --name testwebshop
```

### Updates deployen
```bash
git add -A
git commit -m "Update: beschrijving van wijziging"
git push origin main
```
Vercel deployt automatisch na elke push naar main.

## Environment variables
Kopieer `.env.example` naar `.env` en vul in:
STRIPE_SECRET_KEY=sk_live_...

STRIPE_PUBLISHABLE_KEY=pk_live_...

DATABASE_URL=postgresql://...

SECRET_KEY=willekeurige-lange-string

## Lokaal draaien
```bash
# Backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8001

# Frontend
npm install
npm run dev
```

## Backup
Database backup dagelijks automatisch via Vercel.
Handmatige backup: exporteer via admin panel → Instellingen → Backup.
