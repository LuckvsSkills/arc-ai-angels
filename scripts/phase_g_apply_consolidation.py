#!/usr/bin/env python3
from pathlib import Path
from datetime import datetime
import shutil
import json

HOME = Path.home()
BASE = HOME / "arc_ai_angels"
AGENTS = BASE / "agents"
BACKUPS = BASE / "backups"
REPORTS = BASE / "reports"

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

BACKUP_DIR = BACKUPS / f"phase_g_consolidation_{timestamp}"
REPORT_TXT = REPORTS / f"phase_g_consolidation_{timestamp}.txt"

BACKUP_DIR.mkdir(parents=True, exist_ok=True)

CONSOLIDATION_MAP = {
    "helix": AGENTS / "omni" / "helix" / "lead agent cortexia",
    "matrix": AGENTS / "omni" / "matrix" / "lead agent saelia",
    "quantix": AGENTS / "omni" / "quantix" / "lead agent lumeria",
    "zenix": AGENTS / "omni" / "zenix" / "lead agent fluentia",
    "finix": AGENTS / "omni" / "finix" / "lead agent finoria",
    "nero": AGENTS / "omni" / "helix" / "sentinels" / "nero",
    "solis": AGENTS / "omni" / "zenix" / "sentinels" / "solis",
    "sora": AGENTS / "omni" / "matrix" / "sentinels" / "sora",
    "vector": AGENTS / "omni" / "finix" / "sentinels" / "vector",
    "vondra": AGENTS / "omni" / "quantix" / "sentinels" / "vondra",
}

log = []
log.append("=== PHASE G CONSOLIDATION APPLY ===")
log.append(f"Time: {timestamp}\n")

for name, target in CONSOLIDATION_MAP.items():
    wrapper = AGENTS / name
    log.append(f"[{name}]")

    if not wrapper.exists():
        log.append("  - wrapper missing, skipped")
        continue

    # Backup wrapper
    backup_target = BACKUP_DIR / name
    shutil.copytree(wrapper, backup_target)
    log.append(f"  - backup created: {backup_target}")

    # Ensure target dirs
    (target / "sessions").mkdir(parents=True, exist_ok=True)
    (target / "agent").mkdir(parents=True, exist_ok=True)

    # Merge sessions
    wrapper_sessions = wrapper / "sessions"
    target_sessions = target / "sessions"

    if wrapper_sessions.exists():
        for f in wrapper_sessions.glob("*"):
            dest = target_sessions / f.name
            if not dest.exists():
                shutil.move(str(f), str(dest))
                log.append(f"  - moved session: {f.name}")
            else:
                log.append(f"  - skipped (exists): {f.name}")

    # Move models.json
    wrapper_models = wrapper / "agent" / "models.json"
    target_models = target / "agent" / "models.json"

    if wrapper_models.exists() and not target_models.exists():
        shutil.copy2(wrapper_models, target_models)
        log.append("  - models.json copied")

    # Archive wrapper
    archive_path = BACKUP_DIR / f"{name}_archived"
    shutil.move(str(wrapper), str(archive_path))
    log.append(f"  - wrapper archived → {archive_path}\n")

# Write report
REPORT_TXT.write_text("\n".join(log))
print(f"Report: {REPORT_TXT}")
print(f"Backup: {BACKUP_DIR}")
