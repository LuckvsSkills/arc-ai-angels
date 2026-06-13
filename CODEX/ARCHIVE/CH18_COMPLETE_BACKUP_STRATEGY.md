# CH18 - Complete Backup Strategy & Recovery

## Overview: 4-Level Backup Strategie
LEVEL 1: GitHub (Online - Fase 2)
↓ IF GitHub fails
LEVEL 2: Local Daily Backups (System)
↓ IF Local fails
LEVEL 3: Windows Download (Manual)
↓ IF Windows fails
LEVEL 4: Email Archive (Emergency)

---

## LEVEL 1: GitHub Backup (LATER - Fase 2)

### Setup
- Repository: `https://github.com/LuckvsSkills/arc-ai-angels-clean.git`
- Account: LuckvsSkills
- Access: Overal, online, altijd beschikbaar
- Auto-sync: Elke 4 uur (cronjob)

### Push Strategy
```bash
# Alleen core files
git add agents/ CODEX/ HARNAS_OPENCLAW/ CANON.md
git commit -m "Auto-backup: $(date)"
git push origin master
```

### Recovery via GitHub
```bash
# Clone complete repo
git clone https://github.com/LuckvsSkills/arc-ai-angels-clean.git
cd arc-ai-angels-clean

# Restore naar /home/prime/
cp -r agents/ /home/prime/arc_ai_angels/
cp -r CODEX/ /home/prime/arc_ai_angels/
cp -r HARNAS_OPENCLAW/ /home/prime/arc_ai_angels/
cp CANON.md /home/prime/arc_ai_angels/
```

---

## LEVEL 2: Local Daily Backups (System) - ACTIEF ✅

### Location
/home/prime/backups/ARC_COMPLETE_SYSTEM_YYYYMMDD-HHMMSS.zip (69M)

### Schedule
- **Timing:** Elke dag om 02:00 UTC
- **Script:** `/home/prime/backup-daily.sh`
- **Retention:** Laatste 7 backups (auto-cleanup)
- **Size:** ~69M per backup

### Inhoud
ARC_COMPLETE_SYSTEM_*.zip bevat:
✅ agents/ (32 agents, alle files)
✅ CODEX/ (16 chapters)
✅ HARNAS_OPENCLAW/ (deployment scripts)
✅ config/ (system config)
✅ COMMON/ (shared libraries)
✅ SESSIONS/ (history)
✅ CANON.md (system bible)
✅ README.md (restore guide)

### Backup aanmaken (handmatig)
```bash
cd /home/prime
backup-daily.sh

# Controleren
ls -lh /home/prime/backups/ARC_COMPLETE_SYSTEM_*.zip
```

### Backup downloaden naar Windows (2 opties)

#### OPTIE 1: Browser (Eenvoudig)

Open: http://172.24.162.255:8888
Kies: ARC_COMPLETE_SYSTEM_[DATE].zip
Download automatisch


#### OPTIE 2: PowerShell (Commando)
```powershell
# In PowerShell (als admin)
$url = "http://172.24.162.255:8888/ARC_COMPLETE_SYSTEM_20260603-151209.zip"
$output = "$env:USERPROFILE\Downloads\ARC_BACKUP.zip"
Invoke-WebRequest -Uri $url -OutFile $output

# Verifiëren
ls $env:USERPROFILE\Downloads\ARC_BACKUP.zip
```

#### OPTIE 3: Port Forward (Als WSL niet direct bereikbaar)
```powershell
# CMD (als admin)
netsh interface portproxy add v4tov4 listenport=8888 listenaddress=127.0.0.1 connectport=8888 connectaddress=172.24.162.255

# Dan: http://localhost:8888/
```

### Recovery van Local Backup (WSL2)
```bash
# Restore from backup
cd /home/prime/backups
unzip ARC_COMPLETE_SYSTEM_YYYYMMDD-HHMMSS.zip

# Copy naar production
cp -r ARC_COMPLETE_SYSTEM_*/agents /home/prime/arc_ai_angels/
cp -r ARC_COMPLETE_SYSTEM_*/CODEX /home/prime/arc_ai_angels/
cp -r ARC_COMPLETE_SYSTEM_*/HARNAS_OPENCLAW /home/prime/arc_ai_angels/

# Verify
ls -la /home/prime/arc_ai_angels/agents | head -5
```

---

## LEVEL 3: Windows Download Backup (Manual)

### Stap-voor-stap Download

**1. Backup aanmaken (WSL2)**
```bash
# SSH in WSL2
ssh prime@172.24.162.255

# Run backup
backup-daily.sh

# Get latest file
ls -lh /home/prime/backups/ | head -2
```

**2. Download naar Windows**
```powershell
# Kies OPTIE 1, 2 of 3 (zie hierboven)

# Voorbeeld: Browser
# 1. Open http://172.24.162.255:8888 in Chrome/Edge
# 2. Klik op ARC_COMPLETE_SYSTEM_*.zip
# 3. Save to Downloads
```

**3. Extract op Windows**
```powershell
# In PowerShell
cd $env:USERPROFILE\Downloads
Expand-Archive ARC_BACKUP.zip -DestinationPath "C:\arc-ai-angels-backup"

# Check
dir "C:\arc-ai-angels-backup"
```

**4. Verify inhoud**
```powershell
# Check folders
dir "C:\arc-ai-angels-backup\agents" | head
dir "C:\arc-ai-angels-backup\CODEX" | head
```

### Windows Backup Opslag
Recommended:
C:\Users[YourUser]\Documents\ARC-Backups\
Structuur:
ARC-Backups/
├── 2026-06-03-backup-1/
├── 2026-06-03-backup-2/
└── 2026-06-04-backup-1/

---

## LEVEL 4: Email Archive (Emergency Only)

### Monthly Email Backup
- **Frequency:** 1x per maand (1ste van de maand)
- **Recipient:** Fea's email
- **Size:** 69M (compleet system)
- **Timing:** 03:00 UTC
- **Note:** Outdated OK - alleen voor extreme emergency

### Script Setup (Fase 2)
```bash
# /home/prime/backup-email.sh
# Cron: 0 3 1 * * (first day of month, 03:00 UTC)

LATEST=$(ls -t /home/prime/backups/ARC_COMPLETE_SYSTEM_*.zip | head -1)
FILENAME=$(basename $LATEST)

echo "ARC AI AGENTS backup attached" | \
  mail -s "Monthly Backup: $FILENAME" \
  -a "$LATEST" \
  fea@example.com
```

---

## Recovery Decision Tree
Need to restore?
├─ GitHub beschikbaar?
│  YES → git clone van GitHub (snelst, online)
│  NO  ↓
│
├─ WSL2 local backups beschikbaar?
│  YES → unzip /home/prime/backups/ARC_COMPLETE_SYSTEM_*.zip
│  NO  ↓
│
├─ Windows backup beschikbaar?
│  YES → Extract + copy terug naar WSL2
│  NO  ↓
│
└─ Email backup beschikbaar?
YES → Download + extract (outdated, maar beter dan niks!)
NO  → CRITICAL: Contact backup support

---

## Best Practices

✅ **DO:**
- Check backups elke week: `ls /home/prime/backups/`
- Download copy naar Windows maandelijks
- Test restore procedure (1x per kwartaal)
- Monitor GitHub (Fase 2)
- Check email backups ontvangen

❌ **DON'T:**
- Vertrouw op ONLY GitHub (nog niet implementeerd)
- Let log files (flux.err, nova_router.err) groeien >100MB
- Push grote binaries naar git
- Vergeet cronjobs in- en uit te schakelen

---

## Verification Commands

```bash
# Check all backups
ls -lh /home/prime/backups/ARC_COMPLETE_SYSTEM_*.zip

# Count backups (should be ≤7)
ls /home/prime/backups/ARC_COMPLETE_SYSTEM_*.zip | wc -l

# Verify latest backup integrity
unzip -t $(ls -t /home/prime/backups/ARC_COMPLETE_SYSTEM_*.zip | head -1) | tail -3

# Check HTTP server running
curl -I http://172.24.162.255:8888 | head -3

# Check backup cron job
crontab -l | grep backup-daily
```

---

## Timeline
NOW (Fase 1):
✅ Local daily backups (02:00 UTC)
✅ Windows download ready
✅ HTTP server (8888)
✅ 7-day retention
FASE 2:
⏳ GitHub setup (fresh repo)
⏳ Auto-push cronjob (every 4h)
⏳ Email archive (monthly)
⏳ Recovery testing
FASE 3:
⏳ Monitoring dashboard
⏳ Backup alerts (if failed)
⏳ Disaster recovery plan

---

## Contact & Support

For backup issues:
- WSL2 storage: Check `/home/prime/backups/` size
- HTTP access: Test `http://172.24.162.255:8888`
- Windows download: Use PowerShell method if browser fails
- Git setup: See CH17_GITHUB_BACKUP_STRATEGY.md
