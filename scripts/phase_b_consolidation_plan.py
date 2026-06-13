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
report_txt = REPORTS / f"phase_b_consolidation_plan_{timestamp}.txt"
report_json = REPORTS / f"phase_b_consolidation_plan_{timestamp}.json"

SPECIAL_CANON = {"flux", "nova", "flux_core", "main", "omni", "workers", "standalone"}

STANDARD_WORKSPACE_FILES = {
    "AGENTS.md",
    "BOOTSTRAP.md",
    "HEARTBEAT.md",
    "IDENTITY.md",
    "SOUL.md",
    "TOOLS.md",
    "USER.md",
}

STANDARD_AGENT_REAL_FILES = {
    "models.json",
    "auth.json",
    "auth-profiles.json",
}

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

def list_files_recursive(p: Path):
    results = []
    if not p.exists():
        return results
    for item in p.rglob("*"):
        try:
            if item.is_file() and not item.is_symlink():
                results.append(item)
        except Exception:
            pass
    return sorted(results)

def relpaths(paths, base):
    out = []
    for p in paths:
        try:
            out.append(str(p.relative_to(base)))
        except Exception:
            out.append(str(p))
    return sorted(out)

def classify_agent_dir(p: Path):
    name = p.name

    if name in SPECIAL_CANON:
        return "KEEP_SPECIAL"

    has_sessions = has_nonempty_dir(p / "sessions")
    has_runtime = has_nonempty_dir(p / "runtime")
    has_logs = has_nonempty_dir(p / "logs")
    has_workspace = has_nonempty_dir(p / "workspace")

    active_runtime = has_sessions or has_runtime or has_logs

    if active_runtime:
        return "KEEP_ACTIVE"

    return "STUB_CANDIDATE"

def analyze_workspace(p: Path):
    ws = p / "workspace"
    result = {
        "exists": ws.is_dir(),
        "real_files": [],
        "nonstandard_files": [],
        "has_git": (ws / ".git").exists(),
        "has_openclaw": (ws / ".openclaw").exists(),
    }

    if not ws.is_dir():
        return result

    real_files = []
    for item in ws.rglob("*"):
        try:
            if item.is_file() and not item.is_symlink():
                real_files.append(item)
        except Exception:
            pass

    result["real_files"] = relpaths(real_files, ws)

    nonstandard = []
    for rel in result["real_files"]:
        top = rel.split("/")[0]
        if top in STANDARD_WORKSPACE_FILES:
            continue
        if top == ".git":
            continue
        if top == ".openclaw":
            continue
        nonstandard.append(rel)

    result["nonstandard_files"] = sorted(nonstandard)
    return result

def analyze_agent_subdir(p: Path):
    agent = p / "agent"
    result = {
        "exists": agent.is_dir(),
        "real_files": [],
        "real_dirs": [],
        "symlinks": [],
        "unexpected_real_files": [],
        "unexpected_real_dirs": [],
    }

    if not agent.is_dir():
        return result

    for item in safe_listdir(agent):
        entry = {"name": item.name, "path": str(item)}
        try:
            if item.is_symlink():
                try:
                    entry["target"] = str(item.resolve())
                except Exception:
                    entry["target"] = "UNRESOLVED"
                result["symlinks"].append(entry)
            elif item.is_file():
                result["real_files"].append(entry)
            elif item.is_dir():
                result["real_dirs"].append(entry)
        except Exception:
            pass

    result["unexpected_real_files"] = [
        x for x in result["real_files"] if x["name"] not in STANDARD_AGENT_REAL_FILES
    ]
    result["unexpected_real_dirs"] = list(result["real_dirs"])
    return result

def analyze_top_level_extras(p: Path):
    allowed = {"agent", "workspace", "sessions", "runtime", "logs"}
    extras = []

    for item in safe_listdir(p):
        if item.name in allowed:
            continue
        kind = "dir" if item.is_dir() else "file" if item.is_file() else "other"
        extras.append({
            "name": item.name,
            "path": str(item),
            "type": kind,
        })

    return extras

def analyze_sessions_runtime_logs(p: Path):
    out = {}
    for name in ["sessions", "runtime", "logs"]:
        d = p / name
        files = list_files_recursive(d)
        out[name] = {
            "exists": d.exists(),
            "real_file_count": len(files),
            "sample": relpaths(files[:20], p) if files else [],
        }
    return out

def decide_status(agent_name, classification, top_extras, agent_info, workspace_info, runtime_info):
    reasons = []

    if classification == "KEEP_SPECIAL":
        reasons.append("canon/special directory")
        return "KEEP_SPECIAL", reasons

    if classification == "KEEP_ACTIVE":
        reasons.append("runtime data present in sessions/runtime/logs")
        return "KEEP_ACTIVE", reasons

    if top_extras:
        reasons.append("top-level extras present")
        return "MANUAL_REVIEW", reasons

    if agent_info["unexpected_real_files"]:
        reasons.append("unexpected real files inside agent/")
        return "MANUAL_REVIEW", reasons

    if agent_info["unexpected_real_dirs"]:
        reasons.append("unexpected real directories inside agent/")
        return "MANUAL_REVIEW", reasons

    if workspace_info["nonstandard_files"]:
        reasons.append("nonstandard workspace files present")
        return "MANUAL_REVIEW", reasons

    if runtime_info["sessions"]["real_file_count"] > 0:
        reasons.append("sessions data present")
        return "KEEP_ACTIVE", reasons

    if runtime_info["runtime"]["real_file_count"] > 0:
        reasons.append("runtime data present")
        return "KEEP_ACTIVE", reasons

    if runtime_info["logs"]["real_file_count"] > 0:
        reasons.append("logs data present")
        return "KEEP_ACTIVE", reasons

    reasons.append("stub only: symlinked agent content + standard workspace skeleton")
    return "SAFE_TO_REMOVE_STUB", reasons

results = {
    "generated_at": datetime.now().isoformat(),
    "base": str(BASE),
    "agents_root": str(AGENTS),
    "agents": [],
    "summary": {},
}

if AGENTS.is_dir():
    for item in sorted(AGENTS.iterdir(), key=lambda x: x.name.lower()):
        if not item.is_dir():
            continue

        classification = classify_agent_dir(item)
        top_extras = analyze_top_level_extras(item)
        agent_info = analyze_agent_subdir(item)
        workspace_info = analyze_workspace(item)
        runtime_info = analyze_sessions_runtime_logs(item)
        decision, reasons = decide_status(
            item.name,
            classification,
            top_extras,
            agent_info,
            workspace_info,
            runtime_info,
        )

        results["agents"].append({
            "name": item.name,
            "path": str(item),
            "classification": classification,
            "decision": decision,
            "decision_reasons": reasons,
            "top_level_extras": top_extras,
            "agent": agent_info,
            "workspace": workspace_info,
            "runtime": runtime_info,
        })

summary = {
    "total_agent_dirs": len(results["agents"]),
    "by_classification": {},
    "by_decision": {},
}

for item in results["agents"]:
    c = item["classification"]
    d = item["decision"]
    summary["by_classification"][c] = summary["by_classification"].get(c, 0) + 1
    summary["by_decision"][d] = summary["by_decision"].get(d, 0) + 1

results["summary"] = summary

lines = []
lines.append("=== ARC AI ANGELS — PHASE B CONSOLIDATION PLAN ===")
lines.append(f"Generated at: {results['generated_at']}")
lines.append(f"Base: {BASE}")
lines.append(f"Agents root: {AGENTS}")
lines.append("")

lines.append("=== SUMMARY ===")
lines.append(f"Total agent dirs: {summary['total_agent_dirs']}")
lines.append("By classification:")
for k, v in sorted(summary["by_classification"].items()):
    lines.append(f"- {k}: {v}")
lines.append("By decision:")
for k, v in sorted(summary["by_decision"].items()):
    lines.append(f"- {k}: {v}")
lines.append("")

for section in ["KEEP_SPECIAL", "KEEP_ACTIVE", "SAFE_TO_REMOVE_STUB", "MANUAL_REVIEW"]:
    lines.append(f"=== {section} ===")
    found = [a for a in results["agents"] if a["decision"] == section]
    if not found:
        lines.append("- none")
    else:
        for a in found:
            lines.append(f"- {a['name']}")
    lines.append("")

lines.append("=== DETAILS ===")
for a in results["agents"]:
    lines.append(f"[{a['name']}]")
    lines.append(f"  classification: {a['classification']}")
    lines.append(f"  decision: {a['decision']}")
    for r in a["decision_reasons"]:
        lines.append(f"  reason: {r}")

    if a["top_level_extras"]:
        lines.append("  top_level_extras:")
        for x in a["top_level_extras"]:
            lines.append(f"    - {x['type']}: {x['name']}")

    if a["agent"]["unexpected_real_files"]:
        lines.append("  unexpected_agent_real_files:")
        for x in a["agent"]["unexpected_real_files"]:
            lines.append(f"    - {x['name']}")

    if a["agent"]["unexpected_real_dirs"]:
        lines.append("  unexpected_agent_real_dirs:")
        for x in a["agent"]["unexpected_real_dirs"]:
            lines.append(f"    - {x['name']}")

    if a["workspace"]["nonstandard_files"]:
        lines.append("  workspace_nonstandard_files:")
        for x in a["workspace"]["nonstandard_files"]:
            lines.append(f"    - {x}")

    for bucket in ["sessions", "runtime", "logs"]:
        info = a["runtime"][bucket]
        if info["real_file_count"] > 0:
            lines.append(f"  {bucket}_real_file_count: {info['real_file_count']}")
            for x in info["sample"]:
                lines.append(f"    - {x}")

    lines.append("")

report_txt.write_text("\n".join(lines) + "\n", encoding="utf-8")
report_json.write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

print(f"TXT report:  {report_txt}")
print(f"JSON report: {report_json}")
