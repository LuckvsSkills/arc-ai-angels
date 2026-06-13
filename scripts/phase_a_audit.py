#!/usr/bin/env python3
from pathlib import Path
from datetime import datetime
import json

HOME = Path.home()
BASE = HOME / "arc_ai_angels"
AGENTS = BASE / "agents"
REPORTS = BASE / "reports"

REPORTS.mkdir(parents=True, exist_ok=True)

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
report_txt = REPORTS / f"phase_a_audit_{timestamp}.txt"
report_json = REPORTS / f"phase_a_audit_{timestamp}.json"

SPECIAL_CANON = {"flux", "nova", "flux_core", "main", "omni", "workers", "standalone"}

JUNK_NAMES = {
    "=====",
    "^C",
    "echo",
    "grep",
    "sed",
    "do",
    "done",
    "Omni",
    "Sentinel",
    "Worker",
    "[",
    "Gebruik",
    "Geef",
    "Vraag",
    "tart",
}

JUNK_PREFIXES = (
    "FLUX_TO_",
    "HELIX_TO_",
    "NERO_TO_",
    "FINIX_TO_",
    "QUANTIX_TO_",
    "VONDRA_TO_",
)

def has_dir(p: Path, name: str) -> bool:
    return (p / name).exists()

def is_nonempty_dir(p: Path, name: str) -> bool:
    d = p / name
    if not d.is_dir():
        return False
    try:
        next(d.iterdir())
        return True
    except StopIteration:
        return False

def safe_listdir(p: Path):
    try:
        return sorted(p.iterdir(), key=lambda x: x.name.lower())
    except Exception:
        return []

def classify_agent_dir(p: Path):
    name = p.name

    if name in SPECIAL_CANON:
        return "CANON_SPECIAL"

    agent_dir = p / "agent"
    workspace_dir = p / "workspace"
    sessions_dir = p / "sessions"
    runtime_dir = p / "runtime"
    logs_dir = p / "logs"

    has_agent = agent_dir.is_dir()
    has_workspace = workspace_dir.is_dir()
    has_sessions = sessions_dir.is_dir()
    has_runtime = runtime_dir.is_dir()
    has_logs = logs_dir.is_dir()

    active_runtime = False
    if has_workspace and is_nonempty_dir(p, "workspace"):
        active_runtime = True
    if has_sessions and is_nonempty_dir(p, "sessions"):
        active_runtime = True
    if has_runtime and is_nonempty_dir(p, "runtime"):
        active_runtime = True
    if has_logs and is_nonempty_dir(p, "logs"):
        active_runtime = True

    symlink_count = 0
    real_file_count = 0
    if has_agent:
        for item in safe_listdir(agent_dir):
            if item.is_symlink():
                symlink_count += 1
            elif item.is_file():
                real_file_count += 1

    if name == "omni":
        return "OMNI_ROOT"

    if has_agent and active_runtime:
        return "RUNTIME_ACTIVE"

    if has_agent and symlink_count > 0 and not active_runtime:
        return "RUNTIME_STUB"

    if has_agent and real_file_count > 0 and not active_runtime:
        return "RUNTIME_STUB"

    return "UNKNOWN"

def scan_agent_dir(p: Path):
    info = {
        "name": p.name,
        "path": str(p),
        "classification": classify_agent_dir(p),
        "has_agent_dir": (p / "agent").is_dir(),
        "has_workspace": (p / "workspace").is_dir(),
        "has_sessions": (p / "sessions").is_dir(),
        "has_runtime": (p / "runtime").is_dir(),
        "has_logs": (p / "logs").is_dir(),
        "top_level_extras": [],
        "agent_symlinks": [],
        "agent_real_files": [],
        "agent_real_dirs": [],
    }

    allowed = {"agent", "workspace", "sessions", "runtime", "logs"}

    for item in safe_listdir(p):
        if item.name not in allowed:
            info["top_level_extras"].append({
                "name": item.name,
                "path": str(item),
                "type": "dir" if item.is_dir() else "file" if item.is_file() else "other"
            })

    agent_dir = p / "agent"
    if agent_dir.is_dir():
        for item in safe_listdir(agent_dir):
            entry = {
                "name": item.name,
                "path": str(item),
            }
            if item.is_symlink():
                try:
                    entry["target"] = str(item.resolve())
                except Exception:
                    entry["target"] = "UNRESOLVED"
                info["agent_symlinks"].append(entry)
            elif item.is_file():
                info["agent_real_files"].append(entry)
            elif item.is_dir():
                info["agent_real_dirs"].append(entry)

    return info

def scan_junk_files(root: Path):
    found = []
    for item in safe_listdir(root):
        if item.is_file():
            name = item.name
            if name in JUNK_NAMES or any(name.startswith(prefix) for prefix in JUNK_PREFIXES):
                found.append(str(item))
    return found

def scan_zero_byte_weird_files(root: Path):
    found = []
    for item in safe_listdir(root):
        if not item.is_file():
            continue
        try:
            size = item.stat().st_size
        except Exception:
            continue
        if size != 0:
            continue

        name = item.name
        suspicious = False

        if name in JUNK_NAMES:
            suspicious = True
        elif any(name.startswith(prefix) for prefix in JUNK_PREFIXES):
            suspicious = True
        elif "\n" in name:
            suspicious = True
        elif name.strip() != name:
            suspicious = True
        elif len(name) > 40:
            suspicious = True
        elif any(ch in name for ch in ["│", "◇", "🦞"]):
            suspicious = True

        if suspicious:
            found.append(str(item))
    return found

results = {
    "generated_at": datetime.now().isoformat(),
    "base": str(BASE),
    "agents_root": str(AGENTS),
    "agents": [],
    "summary": {},
    "junk": {
        "home_suspect_files": scan_junk_files(HOME),
        "home_zero_byte_weird_files": scan_zero_byte_weird_files(HOME),
        "base_suspect_files": scan_junk_files(BASE),
        "base_zero_byte_weird_files": scan_zero_byte_weird_files(BASE),
    }
}

if AGENTS.is_dir():
    for item in sorted(AGENTS.iterdir(), key=lambda x: x.name.lower()):
        if item.is_dir():
            results["agents"].append(scan_agent_dir(item))

summary_counts = {}
for a in results["agents"]:
    summary_counts[a["classification"]] = summary_counts.get(a["classification"], 0) + 1

results["summary"] = {
    "total_agent_dirs": len(results["agents"]),
    "by_classification": summary_counts,
}

lines = []
lines.append("=== ARC AI ANGELS — PHASE A AUDIT ===")
lines.append(f"Generated at: {results['generated_at']}")
lines.append(f"Base: {BASE}")
lines.append(f"Agents root: {AGENTS}")
lines.append("")

lines.append("=== SUMMARY ===")
lines.append(f"Total agent dirs: {results['summary']['total_agent_dirs']}")
for k, v in sorted(results["summary"]["by_classification"].items()):
    lines.append(f"- {k}: {v}")
lines.append("")

lines.append("=== AGENT CLASSIFICATION ===")
for a in results["agents"]:
    lines.append(f"- {a['name']}: {a['classification']}")
lines.append("")

lines.append("=== DETAILS ===")
for a in results["agents"]:
    lines.append(f"[{a['name']}]")
    lines.append(f"  path: {a['path']}")
    lines.append(f"  classification: {a['classification']}")
    lines.append(f"  has_agent_dir: {a['has_agent_dir']}")
    lines.append(f"  has_workspace: {a['has_workspace']}")
    lines.append(f"  has_sessions: {a['has_sessions']}")
    lines.append(f"  has_runtime: {a['has_runtime']}")
    lines.append(f"  has_logs: {a['has_logs']}")

    if a["top_level_extras"]:
        lines.append("  top_level_extras:")
        for x in a["top_level_extras"]:
            lines.append(f"    - {x['type']}: {x['name']}")

    if a["agent_real_files"]:
        lines.append("  agent_real_files:")
        for x in a["agent_real_files"]:
            lines.append(f"    - {x['name']}")

    if a["agent_real_dirs"]:
        lines.append("  agent_real_dirs:")
        for x in a["agent_real_dirs"]:
            lines.append(f"    - {x['name']}")

    if a["agent_symlinks"]:
        lines.append("  agent_symlinks:")
        for x in a["agent_symlinks"]:
            lines.append(f"    - {x['name']} -> {x['target']}")

    lines.append("")

lines.append("=== SUSPECT JUNK FILES IN HOME ===")
if results["junk"]["home_suspect_files"] or results["junk"]["home_zero_byte_weird_files"]:
    for p in results["junk"]["home_suspect_files"]:
        lines.append(f"- {p}")
    for p in results["junk"]["home_zero_byte_weird_files"]:
        if p not in results["junk"]["home_suspect_files"]:
            lines.append(f"- {p}")
else:
    lines.append("- none")
lines.append("")

lines.append("=== SUSPECT JUNK FILES IN arc_ai_angels ===")
if results["junk"]["base_suspect_files"] or results["junk"]["base_zero_byte_weird_files"]:
    for p in results["junk"]["base_suspect_files"]:
        lines.append(f"- {p}")
    for p in results["junk"]["base_zero_byte_weird_files"]:
        if p not in results["junk"]["base_suspect_files"]:
            lines.append(f"- {p}")
else:
    lines.append("- none")
lines.append("")

report_txt.write_text("\n".join(lines) + "\n", encoding="utf-8")
report_json.write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

print(f"TXT report:  {report_txt}")
print(f"JSON report: {report_json}")
