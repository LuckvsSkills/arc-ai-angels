# CH17 - GitHub Backup Strategy (Fase 2)

## Doel
- Primary backup: GitHub (online, altijd bereikbaar)
- Secondary: Local daily backups
- Tertiary: Windows download
- Emergency: Email backup (maandelijks)

## Waarom GitHub?
✅ Online storage (niet afhankelijk van hardware)
✅ Version history (alle versies beschikbaar)
✅ Worldwide access (LuckvsSkills account)
✅ Automatisch (cronjob bij changes)
✅ Snel (delta sync, niet full zip)

## Probleem: Grote Files
❌ GitHub max 100MB per file
❌ logs/flux.err (271MB) = NIET pushen
❌ logs/nova_router.err (186MB) = NIET pushen
❌ Session files = NIET pushen

## Oplossing: Clean Setup
✅ Fresh repo aanmaken (arc-ai-angels-clean)
✅ Perfect .gitignore EERST
✅ ONLY push: /agents/, /CODEX/, /HARNAS_OPENCLAW/, CANON.md
✅ Cronjob: `git add . && git commit && git push` (bij changes)

## Implementatie (LATER - Fase 2)
1. Create fresh GitHub repo
2. Clone locally
3. Copy ONLY core files
4. Initial commit + push
5. Setup cronjob for auto-sync
6. Test recovery process

## Recovery Strategy
IF GitHub works:
→ Clone van https://github.com/LuckvsSkills/arc-ai-angels-clean.git
ELSE IF GitHub down:
→ Use /home/prime/backups/ARC_COMPLETE_SYSTEM_*.zip
ELSE IF Local down:
→ Download from Windows backup
EMERGENCY:
→ Email backup (monthly, outdated OK)

## Auto-Sync Script (Fase 2)
```bash
#!/bin/bash
# Run: git-auto-sync.sh
# Cron: 0 */4 * * * (every 4 hours)

cd /home/prime/arc_ai_angels
git add agents/ CODEX/ HARNAS_OPENCLAW/ CANON.md .gitignore
git commit -m "Auto-backup: $(date)"
git push origin master 2>/dev/null || echo "Push failed - local backup OK"
```

## Status
- ✅ Strategy documented
- ⏳ Implementation: LATER (Fase 2)
- ✅ Local backups: NOW (running)
