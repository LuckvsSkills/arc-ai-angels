#!/usr/bin/env python3
from pathlib import Path
from datetime import datetime
import json
import shutil

HOME = Path.home()
BASE = HOME / "arc_ai_angels"
REPORTS = BASE / "reports"
BACKUPS = BASE / "backups"

REPORTS.mkdir(parents=True, exist_ok=True)
BACKUPS.mkdir(parents=True, exist_ok=True)

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
report_txt = REPORTS / f"phase_e_cleanup_root_junk_{timestamp}.txt"
report_json = REPORTS / f"phase_e_cleanup_root_junk_{timestamp}.json"
backup_root = BACKUPS / f"phase_e_root_junk_{timestamp}"
backup_home = backup_root / "home"
backup_base = backup_root / "arc_ai_angels_root"

backup_home.mkdir(parents=True, exist_ok=True)
backup_base.mkdir(parents=True, exist_ok=True)

HOME_EXACT = {
    "FINIX_TO_VECTOR_OK",
    "FLUX_TO_FINIX_OK",
    "FLUX_TO_HELIX_OK",
    "FLUX_TO_QUANTIX_OK",
    "HELIX_TO_FLUX_OK",
    "HELIX_TO_NERO_OK",
    "NERO_TO_HELIX_OK",
    "QUANTIX_TO_VONDRA_OK",
    "VONDRA_TO_QUANTIX_OK",
    "Gebruik",
    "Geef",
    "Vraag",
    "[",
    "done",
}

BASE_EXACT = {
    "=====",
    "^C",
    "Omni",
    "Sentinel",
    "Worker",
    "do",
    "done",
    "echo",
    "grep",
    "printf",
    "sed",
}

BASE_KEEP = {
    "AGENTS.md",
    "CANON.md",
    "CANON.md.bak",
    "CANON_DOMAIN_NAMING_PATCH.md",
    "CANON_PROJECT_PATCH.md",
    "DEPLOYMENT.md",
    "ESCALATION.md",
    "HEARTBEAT.md",
    "IDENTITY.md",
    "MEMORY.md",
    "PHASE_STATUS.md",
    "PROTOCOL.md",
    "REPORTING.md",
    "SECURITY.md",
    "SKILLS.md",
    "SOUL.md",
    "TOOLS.md",
    "USER.md",
}

WEIRD_MARKERS = ("OpenClaw", "│", "◇", "🦞")

def safe_iterdir(path: Path):
    try:
        return sorted(path.iterdir(), key=lambda p: p.name.lower())
    except Exception:
        return []

def is_suspicious_home_file(p: Path) -> bool:
    if not p.is_file():
        return False

    name = p.name

    if name in HOME_EXACT:
        return True

    if any(marker in name for marker in WEIRD_MARKERS):
        return True

    if "\n" in name:
        return True

    if len(name) > 80:
        return True

    return False

def is_suspicious_base_file(p: Path) -> bool:
    if not p.is_file():
        return False

    name = p.name

    if name in BASE_EXACT:
        return True

    if name in BASE_KEEP:
        return False

    if "\n" in name:
        return True

    if any(marker in name for marker in WEIRD_MARKERS):
        return True

    return False

def backup_move(src: Path, dst_dir: Path):
    dst = dst_dir / src.name
    counter = 1
    while dst.exists():
        dst = dst_dir / f"{src.name}.dup{counter}"
        counter += 1
    shutil.move(str(src), str(dst))
    return dst

results = {
    "generated_at": datetime.now().isoformat(),
    "backup_root": str(backup_root),
    "home_removed": [],
    "base_removed": [],
    "errors": [],
}

# Home cleanup
for item in safe_iterdir(HOME):
    try:
        if is_suspicious_home_file(item):
            dst = backup_move(item, backup_home)
            results["home_removed"].append({
                "name": item.name,
                "from": str(item),
                "to": str(dst),
            })
    except Exception as e:
        results["errors"].append({
            "path": str(item),
            "error": str(e),
        })

# arc_ai_angels root cleanup
for item in safe_iterdir(BASE):
    try:
        if is_suspicious_base_file(item):
            dst = backup_move(item, backup_base)
            results["base_removed"].append({
                "name": item.name,
                "from": str(item),
                "to": str(dst),
            })
    except Exception as e:
        results["errors"].append({
            "path": str(item),
            "error": str(e),
        })

lines = []
lines.append("=== ARC AI ANGELS — PHASE E CLEANUP ROOT JUNK ===")
lines.append(f"Generated at: {results['generated_at']}")
lines.append(f"Backup root: {results['backup_root']}")
lines.append("")

lines.append("=== SUMMARY ===")
lines.append(f"Home files moved: {len(results['home_removed'])}")
lines.append(f"arc_ai_angels root files moved: {len(results['base_removed'])}")
lines.append(f"Errors: {len(results['errors'])}")
lines.append("")

lines.append("=== HOME MOVED ===")
if results["home_removed"]:
    for item in results["home_removed"]:
        lines.append(f"- {item['name']}")
        lines.append(f"  from: {item['from']}")
        lines.append(f"  to:   {item['to']}")
else:
    lines.append("- none")
lines.append("")

lines.append("=== ARC_AI_ANGELS ROOT MOVED ===")
if results["base_removed"]:
    for item in results["base_removed"]:
        lines.append(f"- {item['name']}")
        lines.append(f"  from: {item['from']}")
        lines.append(f"  to:   {item['to']}")
else:
    lines.append("- none")
lines.append("")

lines.append("=== ERRORS ===")
if results["errors"]:
    for err in results["errors"]:
        lines.append(f"- {err['path']}: {err['error']}")
else:
    lines.append("- none")
lines.append("")

report_txt.write_text("\n".join(lines) + "\n", encoding="utf-8")
report_json.write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

print(f"TXT report:  {report_txt}")
print(f"JSON report: {report_json}")
print(f"Backup dir:  {backup_root}")
print("")
print("Moved from HOME:")
for item in results["home_removed"]:
    print(f"- {item['name']}")
print("")
print("Moved from arc_ai_angels root:")
for item in results["base_removed"]:
    print(f"- {item['name']}")

