#!/usr/bin/env python3
from pathlib import Path
from datetime import datetime
import hashlib
import json

HOME = Path.home()
BASE = HOME / "arc_ai_angels"
AGENTS = BASE / "agents"
REPORTS = BASE / "reports"

REPORTS.mkdir(parents=True, exist_ok=True)

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
report_txt = REPORTS / f"phase_f_consolidation_audit_{timestamp}.txt"
report_json = REPORTS / f"phase_f_consolidation_audit_{timestamp}.json"

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

STANDARD_WORKSPACE_FILES = {
    "AGENTS.md",
    "BOOTSTRAP.md",
    "HEARTBEAT.md",
    "IDENTITY.md",
    "SOUL.md",
    "TOOLS.md",
    "USER.md",
}

STANDARD_WORKSPACE_DIRS = {
    ".git",
    ".openclaw",
}

REQUIRED_AGENT_LINKS = {
    "AGENTS.md",
    "HANDOFF.md",
    "IDENTITY.md",
    "JOURNAL",
    "MEMORY.md",
    "MODEL.md",
    "SKILLS.md",
    "SOUL.md",
    "TASKS.md",
    "TOOLS.md",
}

OPTIONAL_AGENT_LINKS = {
    "TASK_HISTORY.md",
}

def safe_iterdir(path: Path):
    try:
        return sorted(path.iterdir(), key=lambda p: p.name.lower())
    except Exception:
        return []

def sha256_file(path: Path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def rel_str(path: Path, root: Path):
    try:
        return str(path.relative_to(root))
    except Exception:
        return str(path)

def list_real_files_recursive(root: Path):
    results = []
    if not root.exists():
        return results
    for p in sorted(root.rglob("*")):
        try:
            if p.is_file() and not p.is_symlink():
                results.append(p)
        except Exception:
            continue
    return results

def list_all_entries_recursive(root: Path):
    results = []
    if not root.exists():
        return results
    for p in sorted(root.rglob("*")):
        results.append(p)
    return results

def file_map_by_relative(root: Path):
    out = {}
    for f in list_real_files_recursive(root):
        out[rel_str(f, root)] = f
    return out

def scan_wrapper_agent_dir(wrapper_agent_dir: Path):
    info = {
        "exists": wrapper_agent_dir.is_dir(),
        "real_files": [],
        "real_dirs": [],
        "symlinks": [],
        "broken_symlinks": [],
        "missing_required_links": [],
    }

    if not wrapper_agent_dir.is_dir():
        return info

    seen_names = set()

    for item in safe_iterdir(wrapper_agent_dir):
        seen_names.add(item.name)
        entry = {"name": item.name, "path": str(item)}

        try:
            is_symlink = item.is_symlink()
        except Exception:
            is_symlink = False

        if is_symlink:
            try:
                target = item.resolve(strict=False)
                entry["target"] = str(target)
            except Exception:
                entry["target"] = "UNRESOLVED"
            info["symlinks"].append(entry)

            try:
                item.resolve(strict=True)
            except Exception:
                info["broken_symlinks"].append(item.name)
        else:
            try:
                if item.is_file():
                    info["real_files"].append(entry)
                elif item.is_dir():
                    info["real_dirs"].append(entry)
            except Exception:
                pass

    for name in sorted(REQUIRED_AGENT_LINKS):
        if name not in seen_names:
            info["missing_required_links"].append(name)

    return info

def scan_workspace(wrapper_workspace: Path, target_dir: Path):
    target_workspace = target_dir / "workspace"

    info = {
        "wrapper_exists": wrapper_workspace.is_dir(),
        "target_exists": target_workspace.is_dir(),
        "wrapper_nonstandard_files": [],
        "wrapper_nonstandard_dirs": [],
        "wrapper_nonstandard_recursive_files": [],
        "target_workspace_files": [],
        "target_workspace_dirs": [],
    }

    if wrapper_workspace.is_dir():
        for item in safe_iterdir(wrapper_workspace):
            if item.name in STANDARD_WORKSPACE_FILES or item.name in STANDARD_WORKSPACE_DIRS:
                continue
            if item.is_file():
                info["wrapper_nonstandard_files"].append(item.name)
            elif item.is_dir():
                info["wrapper_nonstandard_dirs"].append(item.name)

        for f in list_real_files_recursive(wrapper_workspace):
            rel = rel_str(f, wrapper_workspace)
            top = rel.split("/", 1)[0]
            if top in STANDARD_WORKSPACE_FILES or top in STANDARD_WORKSPACE_DIRS:
                continue
            info["wrapper_nonstandard_recursive_files"].append(rel)

    if target_workspace.is_dir():
        for item in safe_iterdir(target_workspace):
            if item.is_file() and not item.is_symlink():
                info["target_workspace_files"].append(item.name)
            elif item.is_dir() and not item.is_symlink():
                info["target_workspace_dirs"].append(item.name)

    return info

def scan_sessions(wrapper_sessions: Path, target_dir: Path):
    target_sessions = target_dir / "sessions"

    wrapper_map = file_map_by_relative(wrapper_sessions)
    target_map = file_map_by_relative(target_sessions)

    wrapper_only = sorted(set(wrapper_map) - set(target_map))
    target_only = sorted(set(target_map) - set(wrapper_map))
    shared = sorted(set(wrapper_map) & set(target_map))

    same_content = []
    different_content = []

    for rel in shared:
        try:
            if sha256_file(wrapper_map[rel]) == sha256_file(target_map[rel]):
                same_content.append(rel)
            else:
                different_content.append(rel)
        except Exception:
            different_content.append(rel)

    return {
        "wrapper_exists": wrapper_sessions.is_dir(),
        "target_exists": target_sessions.is_dir(),
        "wrapper_file_count": len(wrapper_map),
        "target_file_count": len(target_map),
        "wrapper_only_files": wrapper_only,
        "target_only_files": target_only,
        "same_content_files": same_content,
        "different_content_files": different_content,
    }

def scan_models(wrapper_agent_dir: Path, target_dir: Path):
    wrapper_models = wrapper_agent_dir / "models.json"
    target_models = target_dir / "models.json"

    out = {
        "wrapper_models_exists": wrapper_models.is_file(),
        "target_models_exists": target_models.is_file(),
        "same_content": None,
    }

    if wrapper_models.is_file() and target_models.is_file():
        try:
            out["same_content"] = sha256_file(wrapper_models) == sha256_file(target_models)
        except Exception:
            out["same_content"] = False

    return out

def determine_decision(agent_name: str, agent_scan: dict, workspace_scan: dict, sessions_scan: dict, models_scan: dict):
    reasons = []
    flags = []

    if not (AGENTS / agent_name).is_dir():
        return "SOURCE_MISSING", ["source wrapper directory missing"]

    if not Path(CONSOLIDATION_MAP[agent_name]).is_dir():
        return "BLOCKED", ["target canonical directory missing"]

    if agent_scan["broken_symlinks"]:
        flags.append("broken_agent_symlinks")
        reasons.append("wrapper agent dir has broken symlinks")

    if agent_scan["real_dirs"]:
        flags.append("agent_real_dirs")
        reasons.append("wrapper agent dir contains real directories")

    extra_real_files = sorted(
        x["name"] for x in agent_scan["real_files"]
        if x["name"] != "models.json"
    )
    if extra_real_files:
        flags.append("agent_extra_real_files")
        reasons.append("wrapper agent dir contains extra real files")

    if workspace_scan["wrapper_nonstandard_recursive_files"]:
        flags.append("workspace_nonstandard_files")
        reasons.append("wrapper workspace has nonstandard files/dirs")

    if sessions_scan["different_content_files"]:
        flags.append("session_conflicts")
        reasons.append("target sessions already contain same relative names with different content")

    if models_scan["wrapper_models_exists"] and models_scan["target_models_exists"] and models_scan["same_content"] is False:
        flags.append("models_conflict")
        reasons.append("models.json differs between wrapper and target")

    if flags:
        return "MERGE_WITH_REVIEW", reasons

    if (
        sessions_scan["wrapper_exists"]
        and sessions_scan["wrapper_file_count"] > 0
        and not sessions_scan["different_content_files"]
    ):
        reasons.append("sessions can be merged safely by filename")
        if models_scan["wrapper_models_exists"] and not models_scan["target_models_exists"]:
            reasons.append("target missing models.json; wrapper copy can supply it")
        elif models_scan["wrapper_models_exists"] and models_scan["same_content"] is True:
            reasons.append("models.json already matches")
        elif not models_scan["wrapper_models_exists"]:
            reasons.append("wrapper has no models.json to migrate")
        return "SAFE_MERGE", reasons

    if (
        not sessions_scan["wrapper_exists"]
        and not workspace_scan["wrapper_nonstandard_recursive_files"]
        and not extra_real_files
        and not agent_scan["real_dirs"]
    ):
        return "SAFE_ARCHIVE_WRAPPER", ["no unique runtime payload found in wrapper"]

    return "SAFE_MERGE", ["no blocking differences detected"]

results = {
    "generated_at": datetime.now().isoformat(),
    "base": str(BASE),
    "agents_root": str(AGENTS),
    "targets": {},
    "summary": {},
    "agents": [],
}

for name, target in CONSOLIDATION_MAP.items():
    wrapper_root = AGENTS / name
    wrapper_agent_dir = wrapper_root / "agent"
    wrapper_workspace = wrapper_root / "workspace"
    wrapper_sessions = wrapper_root / "sessions"

    agent_scan = scan_wrapper_agent_dir(wrapper_agent_dir)
    workspace_scan = scan_workspace(wrapper_workspace, target)
    sessions_scan = scan_sessions(wrapper_sessions, target)
    models_scan = scan_models(wrapper_agent_dir, target)

    decision, reasons = determine_decision(
        name=name,
        agent_scan=agent_scan,
        workspace_scan=workspace_scan,
        sessions_scan=sessions_scan,
        models_scan=models_scan,
    ) if False else determine_decision(
        agent_name=name,
        agent_scan=agent_scan,
        workspace_scan=workspace_scan,
        sessions_scan=sessions_scan,
        models_scan=models_scan,
    )

    entry = {
        "name": name,
        "wrapper_root": str(wrapper_root),
        "target_root": str(target),
        "target_exists": target.is_dir(),
        "agent_scan": agent_scan,
        "workspace_scan": workspace_scan,
        "sessions_scan": sessions_scan,
        "models_scan": models_scan,
        "decision": decision,
        "reasons": reasons,
    }
    results["agents"].append(entry)
    results["targets"][name] = str(target)

summary_by_decision = {}
for entry in results["agents"]:
    summary_by_decision[entry["decision"]] = summary_by_decision.get(entry["decision"], 0) + 1

results["summary"] = {
    "total_agents_checked": len(results["agents"]),
    "by_decision": summary_by_decision,
}

lines = []
lines.append("=== ARC AI ANGELS — PHASE F CONSOLIDATION AUDIT ===")
lines.append(f"Generated at: {results['generated_at']}")
lines.append(f"Base: {BASE}")
lines.append(f"Agents root: {AGENTS}")
lines.append("")

lines.append("=== SUMMARY ===")
lines.append(f"Total checked: {results['summary']['total_agents_checked']}")
for k, v in sorted(results["summary"]["by_decision"].items()):
    lines.append(f"- {k}: {v}")
lines.append("")

lines.append("=== TARGET MAP ===")
for name, target in CONSOLIDATION_MAP.items():
    lines.append(f"- {name} -> {target}")
lines.append("")

for entry in results["agents"]:
    lines.append(f"[{entry['name']}]")
    lines.append(f"  wrapper_root: {entry['wrapper_root']}")
    lines.append(f"  target_root: {entry['target_root']}")
    lines.append(f"  target_exists: {entry['target_exists']}")
    lines.append(f"  decision: {entry['decision']}")
    lines.append("  reasons:")
    for reason in entry["reasons"]:
        lines.append(f"    - {reason}")

    agent_scan = entry["agent_scan"]
    lines.append("  agent_dir:")
    lines.append(f"    exists: {agent_scan['exists']}")
    lines.append(f"    real_files: {len(agent_scan['real_files'])}")
    for x in agent_scan["real_files"]:
        lines.append(f"      - {x['name']}")
    lines.append(f"    real_dirs: {len(agent_scan['real_dirs'])}")
    for x in agent_scan["real_dirs"]:
        lines.append(f"      - {x['name']}")
    lines.append(f"    symlinks: {len(agent_scan['symlinks'])}")
    lines.append(f"    broken_symlinks: {len(agent_scan['broken_symlinks'])}")
    for x in agent_scan["broken_symlinks"]:
        lines.append(f"      - {x}")
    if agent_scan["missing_required_links"]:
        lines.append("    missing_required_links:")
        for x in agent_scan["missing_required_links"]:
            lines.append(f"      - {x}")

    workspace_scan = entry["workspace_scan"]
    lines.append("  workspace:")
    lines.append(f"    wrapper_exists: {workspace_scan['wrapper_exists']}")
    lines.append(f"    target_exists: {workspace_scan['target_exists']}")
    lines.append(f"    wrapper_nonstandard_files: {len(workspace_scan['wrapper_nonstandard_files'])}")
    for x in workspace_scan["wrapper_nonstandard_files"]:
        lines.append(f"      - {x}")
    lines.append(f"    wrapper_nonstandard_dirs: {len(workspace_scan['wrapper_nonstandard_dirs'])}")
    for x in workspace_scan["wrapper_nonstandard_dirs"]:
        lines.append(f"      - {x}")
    lines.append(f"    wrapper_nonstandard_recursive_files: {len(workspace_scan['wrapper_nonstandard_recursive_files'])}")
    for x in workspace_scan["wrapper_nonstandard_recursive_files"][:50]:
        lines.append(f"      - {x}")

    sessions_scan = entry["sessions_scan"]
    lines.append("  sessions:")
    lines.append(f"    wrapper_exists: {sessions_scan['wrapper_exists']}")
    lines.append(f"    target_exists: {sessions_scan['target_exists']}")
    lines.append(f"    wrapper_file_count: {sessions_scan['wrapper_file_count']}")
    lines.append(f"    target_file_count: {sessions_scan['target_file_count']}")
    lines.append(f"    wrapper_only_files: {len(sessions_scan['wrapper_only_files'])}")
    for x in sessions_scan["wrapper_only_files"][:50]:
        lines.append(f"      - {x}")
    lines.append(f"    target_only_files: {len(sessions_scan['target_only_files'])}")
    for x in sessions_scan["target_only_files"][:25]:
        lines.append(f"      - {x}")
    lines.append(f"    same_content_files: {len(sessions_scan['same_content_files'])}")
    lines.append(f"    different_content_files: {len(sessions_scan['different_content_files'])}")
    for x in sessions_scan["different_content_files"][:50]:
        lines.append(f"      - {x}")

    models_scan = entry["models_scan"]
    lines.append("  models:")
    lines.append(f"    wrapper_models_exists: {models_scan['wrapper_models_exists']}")
    lines.append(f"    target_models_exists: {models_scan['target_models_exists']}")
    lines.append(f"    same_content: {models_scan['same_content']}")
    lines.append("")

report_txt.write_text("\n".join(lines) + "\n", encoding="utf-8")
report_json.write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

print(f"TXT report:  {report_txt}")
print(f"JSON report: {report_json}")
