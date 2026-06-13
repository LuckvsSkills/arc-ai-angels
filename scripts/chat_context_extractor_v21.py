#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any


HOME = Path.home()
BASE = HOME / "arc_ai_angels"
REPORTS = BASE / "reports"
CHAT_ANALYSIS_DIR = REPORTS / "chat_analysis"


KNOWN_AGENTS = [
    "nova",
    "flux",
    "flux-core",
    "flux_core",
    "main",
    "workers",
    "standalone",
    "omni",
    "helix",
    "matrix",
    "quantix",
    "zenix",
    "finix",
    "nero",
    "forge",
    "ventura",
    "axon",
    "clio",
    "sora",
    "daxio",
    "enki",
    "tharos",
    "arix",
    "vondra",
    "nura",
    "elora",
    "luvia",
    "kresta",
    "solis",
    "orizon",
    "zena",
    "unia",
    "draven",
    "vector",
    "zion",
    "odis",
    "kenzo",
    "kairo",
]

OMNI_DOMAINS = {
    "helix": {
        "lead_label": "cortexia",
        "sentinels": ["nero", "forge", "ventura", "axon", "clio"],
    },
    "matrix": {
        "lead_label": "saelia",
        "sentinels": ["sora", "daxio", "enki", "tharos", "arix"],
    },
    "quantix": {
        "lead_label": "lumeria",
        "sentinels": ["vondra", "nura", "elora", "luvia", "kresta"],
    },
    "zenix": {
        "lead_label": "fluentia",
        "sentinels": ["solis", "orizon", "zena", "unia", "draven"],
    },
    "finix": {
        "lead_label": "finoria",
        "sentinels": ["vector", "zion", "odis", "kenzo", "kairo"],
    },
}

TOPIC_PATTERNS = {
    "canon": [
        r"\bcanon\b",
        r"\bcanonical\b",
        r"\bdomain map\b",
        r"\bowner_agent\b",
        r"\bassigned_to\b",
        r"\bassigned_by\b",
    ],
    "tasks": [
        r"\bTASKS\.md\b",
        r"\btask\b",
        r"\btasks\b",
        r"\bopenstaand\b",
        r"\bafgerond\b",
        r"\bvolgende stap\b",
    ],
    "memory": [
        r"\bMEMORY\.md\b",
        r"\bmemory\b",
        r"\bcontinuation\b",
        r"\bcontext\b",
        r"\brecap\b",
        r"\bsamenvatting\b",
    ],
    "structure": [
        r"\bcleanup\b",
        r"\bconsolidation\b",
        r"\bverify structure\b",
        r"\bstub cleanup\b",
        r"\barchive\b",
        r"\bbackup\b",
        r"\bsymlink\b",
        r"\bworkspace\b",
        r"\bsessions\b",
        r"\bagent dir\b",
    ],
    "openclaw": [
        r"\bopenclaw\b",
        r"\bagents list\b",
        r"\bchannels status\b",
        r"\bbindings\b",
        r"\bgateway\b",
        r"\btelegram\b",
    ],
    "agents": [
        r"\blead agent\b",
        r"\bsentinel\b",
        r"\bomni\b",
        r"\bdomain\b",
        r"\bwrapper\b",
        r"\bruntime wrapper\b",
    ],
    "scripts": [
        r"\bphase_[a-z]\b",
        r"\.py\b",
        r"\baudit\b",
        r"\bverify\b",
        r"\bscript\b",
        r"\bextractor\b",
    ],
}

PHASE_RE = re.compile(r"\bphase_[a-z]\b", re.IGNORECASE)
FILE_RE = re.compile(
    r"\b(?:[A-Z0-9_\-]+\.md|[A-Z0-9_\-]+\.json|[A-Z0-9_\-]+\.jsonl|[A-Z0-9_\-]+\.py|[A-Z0-9_\-]+\.txt)\b",
    re.IGNORECASE,
)
SCRIPT_PATH_RE = re.compile(
    r"(?:~|/home/\w+)?/?(?:[\w\-.]+/)*[\w\-.]+\.py",
    re.IGNORECASE,
)
TITLE_HINT_RE = re.compile(
    r"^\s*(?:#\s*)?(?:chat\s*title|titel|title)\s*[:=-]\s*(.+?)\s*$",
    re.IGNORECASE,
)

COMPLETED_HINTS = [
    "afgerond",
    "uitgevoerd",
    "voltooid",
    "overall_ok true",
    "overall_ok: true",
    "succesvol",
    "klaar",
    "done",
    "fixed",
    "verified",
    "merged",
    "moved",
    "removed",
]
OPEN_HINTS = [
    "volgende stap",
    "openstaand",
    "nog doen",
    "nog nalopen",
    "moet nog",
    "later",
    "todo",
    "to do",
    "back on track",
]
DECISION_HINTS = [
    "we hebben besloten",
    "besluit",
    "gekozen",
    "we gaan",
    "het moet",
    "is de bedoeling",
    "kan weg",
    "archiveren",
    "safe_merge",
    "safe_to_remove_stub",
]
CLEANUP_HINTS = [
    "cleanup",
    "removed",
    "moved",
    "backup",
    "archive",
    "safe_to_remove_stub",
    "stub cleanup",
]
CONSOLIDATION_HINTS = [
    "consolidation",
    "merge",
    "safe_merge",
    "lead agent",
    "sentinel",
    "omni",
    "wrapper",
]
CANON_HINTS = [
    "canon",
    "domain label",
    "owner_agent",
    "assigned_to",
    "assigned_by",
    "canonical",
]
TASK_HINTS = [
    "tasks.md",
    "task",
    "phase_",
    "openstaand",
    "afgerond",
    "volgende stap",
]
MEMORY_HINTS = [
    "memory",
    "continuation",
    "samenvatting",
    "recap",
    "context",
]


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "_", value)
    value = re.sub(r"_+", "_", value).strip("_")
    return value or "untitled_chat"


def dedupe_keep_order(items: list[str]) -> list[str]:
    seen = set()
    out = []
    for item in items:
        key = item.strip()
        if not key:
            continue
        if key not in seen:
            seen.add(key)
            out.append(key)
    return out


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def detect_title(text: str, fallback: str) -> str:
    lines = text.splitlines()
    for line in lines[:50]:
        m = TITLE_HINT_RE.match(line)
        if m:
            title = m.group(1).strip()
            if title:
                return title
    nonempty = [ln.strip() for ln in lines if ln.strip()]
    if nonempty:
        first = nonempty[0]
        if len(first) <= 140 and not first.startswith(">"):
            return first
    return fallback


def normalize_agent_name(name: str) -> str:
    name = name.strip().lower()
    if name == "flux core":
        return "flux_core"
    if name == "flux-core":
        return "flux_core"
    return name


def score_topics(lines: list[str]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for topic, patterns in TOPIC_PATTERNS.items():
        c = 0
        for line in lines:
            for pat in patterns:
                if re.search(pat, line, re.IGNORECASE):
                    c += 1
        if c:
            counts[topic] = c
    return counts


def collect_matching_lines(lines: list[str], hints: list[str]) -> list[str]:
    out = []
    for line in lines:
        low = line.lower()
        if any(h in low for h in hints):
            out.append(line.strip())
    return dedupe_keep_order(out)


def collect_files(lines: list[str]) -> list[str]:
    out = []
    for line in lines:
        for m in FILE_RE.findall(line):
            out.append(m)
        for m in SCRIPT_PATH_RE.findall(line):
            out.append(m)
    return dedupe_keep_order(out)


def collect_phases(lines: list[str]) -> list[str]:
    out = []
    for line in lines:
        for m in PHASE_RE.findall(line):
            out.append(m.lower())
    return dedupe_keep_order(out)


def collect_agents(lines: list[str]) -> list[str]:
    found = []
    for line in lines:
        low = line.lower().replace("flux core", "flux_core")
        for agent in KNOWN_AGENTS:
            if re.search(rf"\b{re.escape(agent)}\b", low):
                found.append(normalize_agent_name(agent))
    return dedupe_keep_order(found)


def extract_openclaw_registered_agents(lines: list[str]) -> list[str]:
    agents = []
    capture = False

    for line in lines:
        stripped = line.strip()

        if "openclaw agents list --json" in stripped.lower():
            capture = True
            continue

        if capture:
            if not stripped:
                continue
            if stripped.startswith("prime@") or stripped.endswith("$"):
                continue
            if stripped.startswith("Routing rules map"):
                break
            if stripped.startswith("[" ) or stripped.startswith("{"):
                continue

            if re.fullmatch(r"[a-z0-9_\-]+", stripped.lower()):
                name = normalize_agent_name(stripped)
                if name in [normalize_agent_name(a) for a in KNOWN_AGENTS]:
                    agents.append(name)

    if not agents:
        for line in lines:
            m = re.search(r'"id"\s*:\s*"([^"]+)"', line)
            if m:
                name = normalize_agent_name(m.group(1))
                agents.append(name)

    return dedupe_keep_order(agents)


def extract_count_from_text(lines: list[str], label: str) -> int | None:
    label_low = label.lower()
    for idx, line in enumerate(lines):
        if label_low in line.lower():
            for nxt in lines[idx:idx + 4]:
                m = re.search(r"\b(\d+)\b", nxt)
                if m:
                    return int(m.group(1))
    return None


def extract_numeric_facts(lines: list[str]) -> dict[str, int | None]:
    return {
        "openclaw_registered_count": extract_count_from_text(lines, "OpenClaw registered"),
        "top_level_agents_dir_count": extract_count_from_text(lines, "Top-level agents dir"),
        "consolidated_omni_agent_dir_count": extract_count_from_text(lines, "Consolidated omni agents with agent dir"),
        "active_arc_runtime_wrappers_count": extract_count_from_text(lines, "Active ARC runtime wrappers"),
        "canonical_omni_leads_count": extract_count_from_text(lines, "Canonical omni leads"),
        "canonical_sentinels_count": extract_count_from_text(lines, "Canonical sentinels"),
    }


def build_expected_omni_map() -> dict[str, Any]:
    domains = {}
    all_agents = []

    for domain, data in OMNI_DOMAINS.items():
        lead = data["lead_label"]
        sentinels = data["sentinels"]
        domains[domain] = {
            "lead": lead,
            "sentinels": sentinels,
            "count": 1 + len(sentinels),
        }
        all_agents.append(domain)
        all_agents.extend(sentinels)

    return {
        "domains": domains,
        "domain_count": len(domains),
        "total_omni_agents": len(all_agents),
        "all_omni_agents": all_agents,
    }


def build_summary(
    title: str,
    topics: dict[str, int],
    phases: list[str],
    completed: list[str],
    open_points: list[str],
    detected_agents: list[str],
    registered_agents: list[str],
    numeric_facts: dict[str, int | None],
    omni_map: dict[str, Any],
) -> str:
    topic_text = ", ".join(
        f"{k} ({v})" for k, v in sorted(topics.items(), key=lambda x: (-x[1], x[0]))
    ) or "geen"
    phase_text = ", ".join(phases) or "geen"
    agent_text = ", ".join(detected_agents[:20]) if detected_agents else "geen"

    reg_count = numeric_facts.get("openclaw_registered_count")
    top_level = numeric_facts.get("top_level_agents_dir_count")
    omni_agent_dirs = numeric_facts.get("consolidated_omni_agent_dir_count")
    omni_total = omni_map["total_omni_agents"]

    return (
        f"Chat '{title}' draaide vooral om: {topic_text}. "
        f"Fases/scripts: {phase_text}. "
        f"Gedetecteerde agentnamen: {agent_text}. "
        f"OpenClaw registered agents: {reg_count if reg_count is not None else len(registered_agents)}. "
        f"Top-level agents map: {top_level if top_level is not None else 'onbekend'}. "
        f"Omni canon model: {omni_total} agents binnen 5 domeinen. "
        f"Omni geconsolideerde agent-dirs gevonden: {omni_agent_dirs if omni_agent_dirs is not None else 'onbekend'}. "
        f"Afgeronde punten: {len(completed)}. Openstaande punten: {len(open_points)}."
    )


def make_continuation_prompt(
    title: str,
    summary: str,
    topics: dict[str, int],
    phases: list[str],
    completed: list[str],
    open_points: list[str],
    cleanup_points: list[str],
    consolidation_points: list[str],
    canon_candidates: list[str],
    task_candidates: list[str],
    memory_candidates: list[str],
    registered_agents: list[str],
    omni_map: dict[str, Any],
    files: list[str],
) -> str:
    lines = []
    lines.append(f"# CONTEXT CONTINUATION — {title}")
    lines.append("")
    lines.append("## Samenvatting")
    lines.append(summary)
    lines.append("")

    lines.append("## Canonieke Omni agent-structuur")
    lines.append(f"- Domeinen: {omni_map['domain_count']}")
    lines.append(f"- Totaal Omni agents: {omni_map['total_omni_agents']}")
    for domain, data in omni_map["domains"].items():
        lines.append(f"- {domain}: lead={data['lead']}, sentinels={', '.join(data['sentinels'])}")
    lines.append("")

    if registered_agents:
        lines.append("## OpenClaw geregistreerde agents")
        for agent in registered_agents:
            lines.append(f"- {agent}")
        lines.append("")

    if topics:
        lines.append("## Hoofdthema's")
        for k, v in sorted(topics.items(), key=lambda x: (-x[1], x[0])):
            lines.append(f"- {k}: {v}")
        lines.append("")

    if phases:
        lines.append("## Fases / scripts")
        for p in phases:
            lines.append(f"- {p}")
        lines.append("")

    if completed:
        lines.append("## Afgeronde punten")
        for item in completed[:25]:
            lines.append(f"- {item}")
        lines.append("")

    if open_points:
        lines.append("## Openstaande punten")
        for item in open_points[:25]:
            lines.append(f"- {item}")
        lines.append("")

    if cleanup_points:
        lines.append("## Cleanup / archief relevante punten")
        for item in cleanup_points[:20]:
            lines.append(f"- {item}")
        lines.append("")

    if consolidation_points:
        lines.append("## Consolidatie relevante punten")
        for item in consolidation_points[:20]:
            lines.append(f"- {item}")
        lines.append("")

    if canon_candidates:
        lines.append("## Mogelijke canon-data")
        for item in canon_candidates[:20]:
            lines.append(f"- {item}")
        lines.append("")

    if task_candidates:
        lines.append("## Mogelijke TASKS.md-data")
        for item in task_candidates[:20]:
            lines.append(f"- {item}")
        lines.append("")

    if memory_candidates:
        lines.append("## Mogelijke MEMORY.md-data")
        for item in memory_candidates[:20]:
            lines.append(f"- {item}")
        lines.append("")

    if files:
        lines.append("## Relevante bestanden / scripts")
        for item in files[:30]:
            lines.append(f"- {item}")
        lines.append("")

    lines.append("## Werkinstructie")
    lines.append(
        "Ga verder waar de vorige chat stopte. "
        "Gebruik canon als waarheid voor agent- en domeinstructuur. "
        "Splits output in: canon-data, task-data, memory-data en tijdelijke cleanup-notities."
    )

    return "\n".join(lines).strip() + "\n"


def write_outputs(result: dict[str, Any], source_file: Path) -> dict[str, str]:
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    slug = result["chat_slug"]
    out_dir = CHAT_ANALYSIS_DIR / slug
    out_dir.mkdir(parents=True, exist_ok=True)

    txt_path = out_dir / f"chat_context_extract_v21_{ts}.txt"
    json_path = out_dir / f"chat_context_extract_v21_{ts}.json"
    prompt_path = out_dir / f"continuation_prompt_v21_{ts}.md"

    lines = []
    lines.append("=== ARC AI ANGELS — CHAT CONTEXT EXTRACTOR V2.1 ===")
    lines.append(f"Generated at: {result['generated_at']}")
    lines.append(f"Source file: {source_file}")
    lines.append(f"Chat title: {result['chat_title']}")
    lines.append(f"Chat slug: {result['chat_slug']}")
    lines.append(f"Line count: {result['line_count']}")
    lines.append("")

    lines.append("=== DETECTED TOPICS ===")
    if result["topics"]:
        for k, v in sorted(result["topics"].items(), key=lambda x: (-x[1], x[0])):
            lines.append(f"- {k}: {v}")
    else:
        lines.append("- none")
    lines.append("")

    lines.append("=== DETECTED PHASES ===")
    if result["likely_phases"]:
        for item in result["likely_phases"]:
            lines.append(f"- {item}")
    else:
        lines.append("- none")
    lines.append("")

    lines.append("=== DETECTED AGENTS IN TEXT ===")
    if result["detected_agents"]:
        for item in result["detected_agents"]:
            lines.append(f"- {item}")
    else:
        lines.append("- none")
    lines.append("")

    lines.append("=== OPENCLAW REGISTERED AGENTS ===")
    if result["openclaw_registered_agents"]:
        for item in result["openclaw_registered_agents"]:
            lines.append(f"- {item}")
    else:
        lines.append("- none")
    lines.append("")

    lines.append("=== NUMERIC FACTS ===")
    for k, v in result["numeric_facts"].items():
        lines.append(f"- {k}: {v}")
    lines.append("")

    lines.append("=== EXPECTED OMNI MAP ===")
    lines.append(f"- domain_count: {result['expected_omni_map']['domain_count']}")
    lines.append(f"- total_omni_agents: {result['expected_omni_map']['total_omni_agents']}")
    for domain, data in result["expected_omni_map"]["domains"].items():
        lines.append(
            f"- {domain}: lead={data['lead']}, sentinels={', '.join(data['sentinels'])}, count={data['count']}"
        )
    lines.append("")

    lines.append("=== COMPLETED POINTS ===")
    if result["completed_points"]:
        for item in result["completed_points"][:25]:
            lines.append(f"- {item}")
    else:
        lines.append("- none")
    lines.append("")

    lines.append("=== OPEN POINTS ===")
    if result["open_points"]:
        for item in result["open_points"][:25]:
            lines.append(f"- {item}")
    else:
        lines.append("- none")
    lines.append("")

    lines.append("=== CLEANUP POINTS ===")
    if result["cleanup_points"]:
        for item in result["cleanup_points"][:25]:
            lines.append(f"- {item}")
    else:
        lines.append("- none")
    lines.append("")

    lines.append("=== CONSOLIDATION POINTS ===")
    if result["consolidation_points"]:
        for item in result["consolidation_points"][:25]:
            lines.append(f"- {item}")
    else:
        lines.append("- none")
    lines.append("")

    lines.append("=== CANON CANDIDATES ===")
    if result["canon_candidates"]:
        for item in result["canon_candidates"][:25]:
            lines.append(f"- {item}")
    else:
        lines.append("- none")
    lines.append("")

    lines.append("=== TASK CANDIDATES ===")
    if result["task_candidates"]:
        for item in result["task_candidates"][:25]:
            lines.append(f"- {item}")
    else:
        lines.append("- none")
    lines.append("")

    lines.append("=== MEMORY CANDIDATES ===")
    if result["memory_candidates"]:
        for item in result["memory_candidates"][:25]:
            lines.append(f"- {item}")
    else:
        lines.append("- none")
    lines.append("")

    lines.append("=== LIKELY FILES / SCRIPTS ===")
    if result["likely_files"]:
        for item in result["likely_files"]:
            lines.append(f"- {item}")
    else:
        lines.append("- none")
    lines.append("")

    lines.append("=== SUMMARY ===")
    lines.append(result["summary"])
    lines.append("")

    lines.append("=== CONTINUATION PROMPT ===")
    lines.append(result["continuation_prompt"])

    txt_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    json_path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    prompt_path.write_text(result["continuation_prompt"], encoding="utf-8")

    return {
        "txt": str(txt_path),
        "json": str(json_path),
        "prompt": str(prompt_path),
        "dir": str(out_dir),
    }


def analyze_chat_dump(source_file: Path, chat_title: str | None = None) -> dict[str, Any]:
    text = read_text(source_file)
    lines = [ln.rstrip() for ln in text.splitlines()]
    nonempty_lines = [ln for ln in lines if ln.strip()]

    title = chat_title.strip() if chat_title else detect_title(text, source_file.stem)
    slug = slugify(title)

    topics = score_topics(nonempty_lines)
    likely_files = collect_files(nonempty_lines)
    likely_phases = collect_phases(nonempty_lines)
    detected_agents = collect_agents(nonempty_lines)
    openclaw_registered_agents = extract_openclaw_registered_agents(nonempty_lines)
    numeric_facts = extract_numeric_facts(nonempty_lines)

    completed_points = collect_matching_lines(nonempty_lines, COMPLETED_HINTS)
    open_points = collect_matching_lines(nonempty_lines, OPEN_HINTS)
    decisions = collect_matching_lines(nonempty_lines, DECISION_HINTS)
    cleanup_points = collect_matching_lines(nonempty_lines, CLEANUP_HINTS)
    consolidation_points = collect_matching_lines(nonempty_lines, CONSOLIDATION_HINTS)
    canon_candidates = collect_matching_lines(nonempty_lines, CANON_HINTS)
    task_candidates = collect_matching_lines(nonempty_lines, TASK_HINTS)
    memory_candidates = collect_matching_lines(nonempty_lines, MEMORY_HINTS)

    expected_omni_map = build_expected_omni_map()

    summary = build_summary(
        title=title,
        topics=topics,
        phases=likely_phases,
        completed=completed_points,
        open_points=open_points,
        detected_agents=detected_agents,
        registered_agents=openclaw_registered_agents,
        numeric_facts=numeric_facts,
        omni_map=expected_omni_map,
    )

    continuation_prompt = make_continuation_prompt(
        title=title,
        summary=summary,
        topics=topics,
        phases=likely_phases,
        completed=completed_points,
        open_points=open_points,
        cleanup_points=cleanup_points,
        consolidation_points=consolidation_points,
        canon_candidates=canon_candidates,
        task_candidates=task_candidates,
        memory_candidates=memory_candidates,
        registered_agents=openclaw_registered_agents,
        omni_map=expected_omni_map,
        files=likely_files,
    )

    return {
        "generated_at": datetime.now().isoformat(),
        "source_file": str(source_file),
        "chat_title": title,
        "chat_slug": slug,
        "line_count": len(lines),
        "nonempty_line_count": len(nonempty_lines),
        "topics": topics,
        "likely_files": likely_files,
        "likely_phases": likely_phases,
        "detected_agents": detected_agents,
        "openclaw_registered_agents": openclaw_registered_agents,
        "numeric_facts": numeric_facts,
        "expected_omni_map": expected_omni_map,
        "completed_points": completed_points,
        "open_points": open_points,
        "decisions": decisions,
        "cleanup_points": cleanup_points,
        "consolidation_points": consolidation_points,
        "canon_candidates": canon_candidates,
        "task_candidates": task_candidates,
        "memory_candidates": memory_candidates,
        "summary": summary,
        "continuation_prompt": continuation_prompt,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Analyze copied chat dump with ARC/OpenClaw aware extractor v2.1")
    parser.add_argument("input_file", help="Path to chat dump txt file")
    parser.add_argument("--title", default=None, help="Optional explicit chat title")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    source_file = Path(args.input_file).expanduser()

    if not source_file.exists():
        print(f"Input file does not exist: {source_file}", file=sys.stderr)
        return 1
    if not source_file.is_file():
        print(f"Input path is not a file: {source_file}", file=sys.stderr)
        return 1

    REPORTS.mkdir(parents=True, exist_ok=True)
    CHAT_ANALYSIS_DIR.mkdir(parents=True, exist_ok=True)

    result = analyze_chat_dump(source_file, chat_title=args.title)
    outputs = write_outputs(result, source_file)

    print(f"TXT report:  {outputs['txt']}")
    print(f"JSON report: {outputs['json']}")
    print(f"PROMPT md:   {outputs['prompt']}")
    print(f"Output dir:  {outputs['dir']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
