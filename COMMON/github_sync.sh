#!/bin/bash
# github_sync.sh — ARC AI Agents GitHub auto-sync
cd /home/prime/arc_ai_angels
git add .
CHANGES=$(git status --short | wc -l)
if [ "$CHANGES" -gt 0 ]; then
    git commit -m "Auto-sync $(date +%Y-%m-%d_%H:%M) — $CHANGES bestanden"
    git push origin master
    echo "[$(date)] GitHub sync: $CHANGES bestanden gepusht"
else
    echo "[$(date)] GitHub sync: geen wijzigingen"
fi
