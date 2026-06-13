#!/bin/bash
PROJECT=$1
if [ -z "$PROJECT" ]; then echo "Gebruik: ./deploy.sh project-naam"; exit 1; fi
PROJECT_DIR="/home/prime/arc_ai_angels/agents/forge/projects/$PROJECT"
VERCEL_TOKEN=$(grep "^VERCEL_TOKEN" /home/prime/.openclaw/.env | cut -d= -f2)
if [ ! -d "$PROJECT_DIR" ]; then echo "❌ Project niet gevonden: $PROJECT_DIR"; exit 1; fi
echo "▲ Ventura Deploy: $PROJECT"
cd $PROJECT_DIR
vercel --token $VERCEL_TOKEN --prod --yes 2>&1 | tail -5
