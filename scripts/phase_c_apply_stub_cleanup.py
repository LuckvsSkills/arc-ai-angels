#!/usr/bin/env python3
from pathlib import Path
from datetime import datetime
import shutil
import json
import sys

HOME = Path.home()
BASE = HOME / "arc_ai_angels"
AGENTS = BASE / "agents"
REPORTS = BASE / "reports"
BACKUPS = BASE / "backups"

REPORTS.mkdir(parents=True, exist_ok=True)
BACKUPS.mkdir(parents=True, exist_ok=True)

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

SAFE_TO_REMOVE = [
    "arix",
    "axon",
    "clio",
    "daxio",
    "draven",
    "elora",
    "enki",
    "forge",
    "kairo",
    "kenzo",
    "kresta",
    "luvia",
    "nura",
    "odis",
    "orizon",
    "tharos",
    "unia",
    "ventura",
    "zena",
    "zion",
]

KEEP_ACTIVE = {
    "finix",
    "helix",
    "matrix",
    "nero",
    "quantix",
    "solis",
    "sora",
    "vector",
    "vondra",
    "zenix",
}

KEEP_SPECIAL = {
    "flux",
    "flux_core",
    "main",
    "nova",
    "omni",
    "standalone",
    "workers",
}

report_txt = REPORTS / f"phase_c_apply_stub_cleanup_{timestamp}.txt"
report_json = REPORTS / f"phase_c_apply_stub_cleanup_{timestamp}.json"

backup_root = BACKUPS / f"phase_c_stub_cleanup_{timestamp}"
backup_root.mkdir(parents=True, exist_ok=True)

def safe_listdir(p: Path):
    try:
        return sorted(p.iterdir(), key=lambda x: x.name.lower())
    except Exception:
        return []

def has_nonempty_dir(p: Path) -> bool:
    if not p.is_dir():
        return False
    try:
        next(p.iterdir())
        return True
    except StopIteration:
        return False
    except Exception:
        return False

def detect_runtime_activity(agent_dir: Path):
    return {
        "workspace_nonempty": has_nonempty_dir(agent_dir / "workspace"),
        "sessions_nonempty": has_nonempty_dir(agent_dir / "sessions"),
        "runtime_nonempty": has_nonempty_dir(agent_dir / "runtime"),
        "logs_nonempty": has_nonempty_dir(agent_dir / "logs"),
    }

def validate_stub(agent_dir: Path):
    problems = []

    if not agent_dir.exists():
        problems.append("missing_directory")
        return problems

    if not (agent_dir / "agent").is_dir():
        problems.append("missing_agent_dir")

    runtime = detect_runtime_activity(agent_dir)

    if runtime["sessions_nonempty"]:
        problems.append("sessions_not_empty")
    if runtime["runtime_nonempty"]:
        problems.append("runtime_not_empty")
    if runtime["logs_nonempty"]:
        problems.append("logs_not_empty")

    agent_subdir = agent_dir / "agent"
    if agent_subdir.is_dir():
        for item in safe_listdir(agent_subdir):
            try:
                if item.is_dir() and not item.is_symlink():
                    problems.append(f"unexpected_real_dir_in_agent:{item.name}")
                elif item.is_file() and not item.is_symlink():
                    if item.name not in {"models.json", "auth.json", "auth-profiles.json"}:
                        problems.append(f"unexpected_real_file_in_agent:{item.name}")
            except Exception:
                problems.append(f"unreadable_agent_item:{item.name}")

    allowed_top = {"agent", "workspace", "sessions", "runtime", "logs"}
    for item in safe_listdir(agent_dir):
        if item.name not in allowed_top:
            problems.append(f"unexpected_top_level:{item.name}")

    return problems

def copy_dir(src: Path, dst: Path):
    shutil.copytree(src, dst, symlinks=True)

results = {
    "generated_at": datetime.now().isoformat(),
    "base": str(BASE),
    "agents_root": str(AGENTS),
    "backup_root": str(backup_root),
    "removed": [],
    "skipped": [],
    "errors": [],
}

for name in SAFE_TO_REMOVE:
    agent_dir = AGENTS / name

    if name in KEEP_ACTIVE or name in KEEP_SPECIAL:
        results["errors"].append({
            "agent": name,
            "reason": "listed_for_removal_but_marked_keep",
        })
        continue

    problems = validate_stub(agent_dir)
    if problems:
        results["skipped"].append({
            "agent": name,
            "path": str(agent_dir),
            "reason": "validation_failed",
            "details": problems,
        })
        continue

    backup_target = backup_root / name

    try:
        copy_dir(agent_dir, backup_target)
        shutil.rmtree(agent_dir)
        results["removed"].append({
            "agent": name,
            "path": str(agent_dir),
            "backup": str(backup_target),
        })
    except Exception as e:
        results["errors"].append({
            "agent": name,
            "path": str(agent_dir),
            "error": str(e),
        })

summary = {
    "planned_removals": len(SAFE_TO_REMOVE),
    "removed_count": len(results["removed"]),
    "skipped_count": len(results["skipped"]),
    "error_count": len(results["errors"]),
}

results["summary"] = summary

lines = []
lines.append("=== ARC AI ANGELS — PHASE C APPLY STUB CLEANUP ===")
lines.append(f"Generated at: {results['generated_at']}")
lines.append(f"Agents root: {AGENTS}")
lines.append(f"Backup root: {backup_root}")
lines.append("")

lines.append("=== SUMMARY ===")
lines.append(f"Planned removals: {summary['planned_removals']}")
lines.append(f"Removed: {summary['removed_count']}")
lines.append(f"Skipped: {summary['skipped_count']}")
lines.append(f"Errors: {summary['error_count']}")
lines.append("")

lines.append("=== REMOVED ===")
if results["removed"]:
    for item in results["removed"]:
        lines.append(f"- {item['agent']}")
        lines.append(f"  path: {item['path']}")
        lines.append(f"  backup: {item['backup']}")
else:
    lines.append("- none")
lines.append("")

lines.append("=== SKIPPED ===")
if results["skipped"]:
    for item in results["skipped"]:
        lines.append(f"- {item['agent']}")
        lines.append(f"  path: {item['path']}")
        lines.append(f"  reason: {item['reason']}")
        for d in item["details"]:
            lines.append(f"    - {d}")
else:
    lines.append("- none")
lines.append("")

lines.append("=== ERRORS ===")
if results["errors"]:
    for item in results["errors"]:
        lines.append(f"- {item['agent']}")
        for k, v in item.items():
            if k != "agent":
                lines.append(f"  {k}: {v}")
else:
    lines.append("- none")
lines.append("")

report_txt.write_text("\n".join(lines) + "\n", encoding="utf-8")
report_json.write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

print(f"TXT report:  {report_txt}")
print(f"JSON report: {report_json}")
print(f"Backup dir:  {backup_root}")
print("")
print("Removed agents:")
for item in results["removed"]:
    print(f"- {item['agent']}")

if results["skipped"]:
    print("")
    print("Skipped agents:")
    for item in results["skipped"]:
        print(f"- {item['agent']} :: {', '.join(item['details'])}")

if results["errors"]:
    print("")
    print("Errors:")
    for item in results["errors"]:
        print(f"- {item['agent']} :: {item}")
