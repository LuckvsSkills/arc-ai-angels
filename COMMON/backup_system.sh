#!/bin/bash
# backup_system.sh — ARC AI Agents dagelijkse backup
# Draait dagelijks 03:00 via crontab

BACKUP_DIR="/home/prime/backups"
SYSTEM_DIR="/home/prime/arc_ai_angels"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/arc_ai_agents_$DATE.tar.gz"
KEEP_DAYS=7

mkdir -p $BACKUP_DIR

echo "[$(date)] Backup starten..."

tar -czf $BACKUP_FILE \
  --exclude="$SYSTEM_DIR/.git" \
  --exclude="$SYSTEM_DIR/logs" \
  --exclude="$SYSTEM_DIR/mcc-frontend" \
  --exclude="$SYSTEM_DIR/mission_control/frontend-mcc/node_modules" \
  --exclude="$SYSTEM_DIR/mcc-backend/node_modules" \
  --exclude="$SYSTEM_DIR/agents/*/sessions" \
  --exclude="$SYSTEM_DIR/agents/*/runtime" \
  --exclude="$SYSTEM_DIR/agents/*/workspace" \
  --exclude="$SYSTEM_DIR/ROOT_ARCHIVE" \
  --exclude="$SYSTEM_DIR/ping_pong_logs" \
  $SYSTEM_DIR/

SIZE=$(du -sh $BACKUP_FILE | cut -f1)
echo "[$(date)] Backup klaar: $BACKUP_FILE ($SIZE)"

# Oude backups verwijderen (ouder dan 7 dagen)
find $BACKUP_DIR -name "arc_ai_agents_*.tar.gz" -mtime +$KEEP_DAYS -delete
echo "[$(date)] Oude backups opgeruimd"

# Lijst huidige backups
echo "[$(date)] Beschikbare backups:"
ls -lh $BACKUP_DIR/arc_ai_agents_*.tar.gz 2>/dev/null
