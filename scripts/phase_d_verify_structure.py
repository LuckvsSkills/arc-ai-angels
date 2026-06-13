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
report_txt = REPORTS / f"phase_d_verify_structure_{timestamp}.txt"
report_json = REPORTS / f"phase_d_verify_structure_{timestamp}.json"

EXPECTED_TOP_LEVEL = {
    "finix",
    "flux",
    "flux_core",
    "helix",
    "main",
    "matrix",
    "nero",
    "nova",
    "omni",
    "quantix",
    "solis",
    "sora",
    "standalone",
    "vector",
    "vondra",
    "workers",
    "zenix",
}

EXPECTED_OMNI = {
    "helix": {
        "lead": "lead agent cortexia",
        "sentinels": {"nero", "forge", "ventura", "axon", "clio"},
    },
    "matrix": {
        "lead": "lead agent saelia",
        "sentinels": {"sora", "daxio", "enki", "tharos", "arix"},
    },
    "quantix": {
        "lead": "lead agent lumeria",
        "sentinels": {"vondra", "nura", "elora", "luvia", "kresta"},
    },
    "zenix": {
        "lead": "lead agent fluentia",
        "sentinels": {"solis", "orizon", "zena", "unia", "draven"},
    },
    "finix": {
        "lead": "lead agent finoria",
        "sentinels": {"vector", "zion", "odis", "kenzo", "kairo"},
    },
}

ACTIVE_RUNTIME = {
    "finix": "/home/prime/arc_ai_angels/agents/omni/finix/lead agent finoria",
    "helix": "/home/prime/arc_ai_angels/agents/omni/helix/lead agent cortexia",
    "matrix": "/home/prime/arc_ai_angels/agents/omni/matrix/lead agent saelia",
    "nero": "/home/prime/arc_ai_angels/agents/omni/helix/sentinels/nero",
    "quantix": "/home/prime/arc_ai_angels/agents/omni/quantix/lead agent lumeria",
    "solis": "/home/prime/arc_ai_angels/agents/omni/zenix/sentinels/solis",
    "sora": "/home/prime/arc_ai_angels/agents/omni/matrix/sentinels/sora",
    "vector": "/home/prime/arc_ai_angels/agents/omni/finix/sentinels/vector",
    "vondra": "/home/prime/arc_ai_angels/agents/omni/quantix/sentinels/vondra",
    "zenix": "/home/prime/arc_ai_angels/agents/omni/zenix/lead agent fluentia",
}

def safe_iterdir(path: Path):
    try:
        return sorted(path.iterdir(), key=lambda p: p.name.lower())
    except Exception:
        return []

def rel(path: Path):
    try:
        return str(path.relative_to(BASE))
    except Exception:
        return str(path)

results = {
    "generated_at": datetime.now().isoformat(),
    "base": str(BASE),
    "agents_root": str(AGENTS),
    "checks": {
        "top_level": {},
        "omni_structure": {},
        "runtime_links": {},
        "broken_symlinks": [],
        "unexpected_top_level": [],
        "missing_top_level": [],
        "summary": {},
    }
}

# 1. Top level check
actual_top = {p.name for p in safe_iterdir(AGENTS) if p.is_dir()}
missing_top = sorted(EXPECTED_TOP_LEVEL - actual_top)
unexpected_top = sorted(actual_top - EXPECTED_TOP_LEVEL)

results["checks"]["missing_top_level"] = missing_top
results["checks"]["unexpected_top_level"] = unexpected_top

for name in sorted(EXPECTED_TOP_LEVEL):
    results["checks"]["top_level"][name] = {
        "exists": (AGENTS / name).is_dir()
    }

# 2. Omni structure check
omni_root = AGENTS / "omni"
for omni_name, spec in EXPECTED_OMNI.items():
    omni_path = omni_root / omni_name
    lead_path = omni_path / spec["lead"]
    sentinels_path = omni_path / "sentinels"

    actual_sentinels = set()
    if sentinels_path.is_dir():
        actual_sentinels = {p.name for p in safe_iterdir(sentinels_path) if p.is_dir()}

    results["checks"]["omni_structure"][omni_name] = {
        "omni_dir_exists": omni_path.is_dir(),
        "lead_exists": lead_path.is_dir(),
        "lead_journal_exists": (lead_path / "JOURNAL").is_dir(),
        "sentinels_dir_exists": sentinels_path.is_dir(),
        "missing_sentinels": sorted(spec["sentinels"] - actual_sentinels),
        "unexpected_sentinels": sorted(actual_sentinels - spec["sentinels"]),
    }

# 3. Active runtime symlink check
required_link_names = {
    "AGENTS.md",
    "HANDOFF.md",
    "IDENTITY.md",
    "MEMORY.md",
    "MODEL.md",
    "SKILLS.md",
    "SOUL.md",
    "TASKS.md",
    "TOOLS.md",
}

for runtime_name, expected_target in ACTIVE_RUNTIME.items():
    agent_dir = AGENTS / runtime_name / "agent"
    status = {
        "agent_dir_exists": agent_dir.is_dir(),
        "models_json_exists": (agent_dir / "models.json").is_file(),
        "missing_required_links": [],
        "broken_links": [],
        "wrong_target_links": [],
    }

    if agent_dir.is_dir():
        for link_name in sorted(required_link_names):
            link_path = agent_dir / link_name
            if not link_path.exists() and not link_path.is_symlink():
                status["missing_required_links"].append(link_name)
                continue
            if not link_path.is_symlink():
                status["wrong_target_links"].append({
                    "name": link_name,
                    "reason": "not_a_symlink",
                })
                continue
            try:
                resolved = str(link_path.resolve())
                if not resolved.startswith(expected_target):
                    status["wrong_target_links"].append({
                        "name": link_name,
                        "resolved": resolved,
                        "expected_prefix": expected_target,
                    })
            except Exception:
                status["broken_links"].append(link_name)

        journal_link = agent_dir / "JOURNAL"
        if not journal_link.exists() and not journal_link.is_symlink():
            status["missing_required_links"].append("JOURNAL")
        elif not journal_link.is_symlink():
            status["wrong_target_links"].append({
                "name": "JOURNAL",
                "reason": "not_a_symlink",
            })
        else:
            try:
                resolved = str(journal_link.resolve())
                if not resolved.startswith(expected_target):
                    status["wrong_target_links"].append({
                        "name": "JOURNAL",
                        "resolved": resolved,
                        "expected_prefix": expected_target,
                    })
            except Exception:
                status["broken_links"].append("JOURNAL")

    results["checks"]["runtime_links"][runtime_name] = status

# 4. Global broken symlink scan under agents
for p in AGENTS.rglob("*"):
    try:
        if p.is_symlink() and not p.exists():
            results["checks"]["broken_symlinks"].append(rel(p))
    except Exception:
        results["checks"]["broken_symlinks"].append(rel(p))

# Summary
omni_ok = True
for _, data in results["checks"]["omni_structure"].items():
    if (
        not data["omni_dir_exists"]
        or not data["lead_exists"]
        or not data["sentinels_dir_exists"]
        or data["missing_sentinels"]
        or data["unexpected_sentinels"]
    ):
        omni_ok = False

runtime_ok = True
for _, data in results["checks"]["runtime_links"].items():
    if (
        not data["agent_dir_exists"]
        or not data["models_json_exists"]
        or data["missing_required_links"]
        or data["broken_links"]
        or data["wrong_target_links"]
    ):
        runtime_ok = False

top_level_ok = not missing_top and not unexpected_top
broken_symlinks_ok = len(results["checks"]["broken_symlinks"]) == 0

results["checks"]["summary"] = {
    "top_level_ok": top_level_ok,
    "omni_structure_ok": omni_ok,
    "runtime_links_ok": runtime_ok,
    "broken_symlinks_ok": broken_symlinks_ok,
    "overall_ok": top_level_ok and omni_ok and runtime_ok and broken_symlinks_ok,
}

lines = []
lines.append("=== ARC AI ANGELS — PHASE D VERIFY STRUCTURE ===")
lines.append(f"Generated at: {results['generated_at']}")
lines.append(f"Base: {BASE}")
lines.append(f"Agents root: {AGENTS}")
lines.append("")

summary = results["checks"]["summary"]
lines.append("=== SUMMARY ===")
for k, v in summary.items():
    lines.append(f"- {k}: {v}")
lines.append("")

lines.append("=== TOP LEVEL ===")
if missing_top:
    lines.append("Missing:")
    for x in missing_top:
        lines.append(f"- {x}")
else:
    lines.append("Missing: none")

if unexpected_top:
    lines.append("Unexpected:")
    for x in unexpected_top:
        lines.append(f"- {x}")
else:
    lines.append("Unexpected: none")
lines.append("")

lines.append("=== OMNI STRUCTURE ===")
for omni_name, data in results["checks"]["omni_structure"].items():
    lines.append(f"[{omni_name}]")
    lines.append(f"  omni_dir_exists: {data['omni_dir_exists']}")
    lines.append(f"  lead_exists: {data['lead_exists']}")
    lines.append(f"  lead_journal_exists: {data['lead_journal_exists']}")
    lines.append(f"  sentinels_dir_exists: {data['sentinels_dir_exists']}")
    lines.append(f"  missing_sentinels: {data['missing_sentinels'] or 'none'}")
    lines.append(f"  unexpected_sentinels: {data['unexpected_sentinels'] or 'none'}")
    lines.append("")

lines.append("=== ACTIVE RUNTIME LINK CHECK ===")
for name, data in results["checks"]["runtime_links"].items():
    lines.append(f"[{name}]")
    lines.append(f"  agent_dir_exists: {data['agent_dir_exists']}")
    lines.append(f"  models_json_exists: {data['models_json_exists']}")
    lines.append(f"  missing_required_links: {data['missing_required_links'] or 'none'}")
    lines.append(f"  broken_links: {data['broken_links'] or 'none'}")
    lines.append(f"  wrong_target_links: {data['wrong_target_links'] or 'none'}")
    lines.append("")

lines.append("=== GLOBAL BROKEN SYMLINKS ===")
if results["checks"]["broken_symlinks"]:
    for x in results["checks"]["broken_symlinks"]:
        lines.append(f"- {x}")
else:
    lines.append("- none")
lines.append("")

report_txt.write_text("\n".join(lines) + "\n", encoding="utf-8")
report_json.write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

print(f"TXT report:  {report_txt}")
print(f"JSON report: {report_json}")
print("")
print("SUMMARY:")
for k, v in summary.items():
    print(f"- {k}: {v}")
