#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from dataclasses import dataclass, asdict
from pathlib import Path
from datetime import datetime
from typing import Any

BASE = Path.home() / "arc_ai_angels"
REPORTS = BASE / "reports"
REPORTS.mkdir(parents=True, exist_ok=True)

KEY_TOPICS = {
    "canon": [
        "canon", "omni", "nova", "flux", "flux core", "main",
        "helix", "matrix", "quantix", "zenix", "finix",
        "cortexia", "saelia", "lumeria", "fluentia", "finoria",
        "nero", "forge", "ventura", "axon", "clio",
        "sora", "daxio", "enki", "tharos", "arix",
        "vondra", "nura", "elora", "luvia", "kresta",
        "solis", "orizon", "zena", "unia", "draven",
        "vector", "zion", "odis", "kenzo", "kairo",
    ],
    "tasks": [
        "task", "tasks.md", "task_history", "task registry",
        "task_registry", "task_events", "phase", "audit",
        "cleanup", "consolidation", "verify structure",
    ],
    "memory": [
        "memory", "memory.md", "memory_rules", "memory_process_log",
        "sqlite", "flux.sqlite", "main.sqlite", "nova.sqlite",
    ],
    "structure": [
        "directory", "directories", "agents/", "agent dir",
        "workspace", "sessions", "runtime", "symlink",
        "stub", "wrapper", "consolidation", "cleanup",
    ],
    "openclaw": [
        "openclaw", "gateway", "telegram", "agents list",
        "channels status", "routing rules", "bindings",
    ],
    "scripts": [
        "phase_a", "phase_b", "phase_c", "phase_d", "phase_e",
        "phase_f", "phase_g", "python3", "nano", "script",
    ],
}

ACTION_PATTERNS = [
    r"maak .*?script",
    r"build .*?script",
    r"cleanup",
    r"consolidation",
    r"verify structure",
    r"audit",
    r"samenvatting",
    r"summary",
    r"prompt",
    r"memory",
    r"tasks\.md",
]

PROMPT_TEMPLATE = """# CONTEXT CONTINUATION — ARC AI ANGELS

## Korte samenvatting
{summary}

## Hoofdthema's uit vorige chat
{topics}

## Belangrijke afgeronde punten
{completed}

## Openstaande punten
{open_items}

## Relevante bestanden / scripts
{files}

## Werkinstructie
Ga verder waar de vorige chat stopte. Bewaak canon-consistentie, wees exact met bestandsnamen en wijzig niets zonder duidelijk doel.
"""

@dataclass
class ExtractionResult:
    source_file: str
    generated_at: str
    line_count: int
    detected_topics: dict[str, int]
    likely_files: list[str]
    likely_phases: list[str]
    likely_actions: list[str]
    completed_points: list[str]
    open_points: list[str]
    summary: str
    continuation_prompt: str


def read_text(path: Path) -> str:
    suffix = path.suffix.lower()

    if suffix in {".txt", ".md", ".log", ".jsonl"}:
        return path.read_text(encoding="utf-8", errors="ignore")

    if suffix == ".json":
        raw = path.read_text(encoding="utf-8", errors="ignore")
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            return raw
        return json_to_text(data)

    return path.read_text(encoding="utf-8", errors="ignore")


def json_to_text(data: Any) -> str:
    chunks: list[str] = []

    def walk(obj: Any) -> None:
        if isinstance(obj, dict):
            for k, v in obj.items():
                if k in {"text", "content", "message", "prompt", "response"} and isinstance(v, str):
                    chunks.append(v)
                else:
                    walk(v)
        elif isinstance(obj, list):
            for item in obj:
                walk(item)
        elif isinstance(obj, str):
            if len(obj.strip()) > 0:
                chunks.append(obj)

    walk(data)
    return "\n".join(chunks)


def normalize_whitespace(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def extract_likely_files(text: str) -> list[str]:
    patterns = [
        r"~/arc_ai_angels/[^\s\"']+",
        r"/home/prime/arc_ai_angels/[^\s\"']+",
        r"[A-Za-z0-9_\-./]+\.md",
        r"[A-Za-z0-9_\-./]+\.py",
        r"[A-Za-z0-9_\-./]+\.json",
        r"[A-Za-z0-9_\-./]+\.sqlite",
    ]
    found: set[str] = set()
    for pat in patterns:
        for match in re.findall(pat, text):
            cleaned = match.strip(".,:;)}]>\"'")
            if "jsonl" in cleaned or cleaned.endswith((".md", ".py", ".json", ".sqlite")) or "arc_ai_angels" in cleaned:
                found.add(cleaned)
    return sorted(found)[:50]


def extract_phases(text: str) -> list[str]:
    found = set(re.findall(r"phase[_\s-]?[a-z]\b", text, flags=re.IGNORECASE))
    found.update(re.findall(r"phase_[a-z]_[A-Za-z0-9_]+", text, flags=re.IGNORECASE))
    found.update(re.findall(r"phase [a-z]\b", text, flags=re.IGNORECASE))
    cleaned = sorted({x.lower().replace(" ", "_").replace("-", "_") for x in found})
    return cleaned[:50]


def detect_topics(text: str) -> dict[str, int]:
    lower = text.lower()
    counts: dict[str, int] = {}
    for topic, words in KEY_TOPICS.items():
        score = 0
        for word in words:
            score += len(re.findall(re.escape(word.lower()), lower))
        if score > 0:
            counts[topic] = score
    return dict(sorted(counts.items(), key=lambda kv: kv[1], reverse=True))


def extract_actions(text: str) -> list[str]:
    lower = text.lower()
    found: list[str] = []

    for pat in ACTION_PATTERNS:
        for match in re.findall(pat, lower):
            found.append(match.strip())

    for line in text.splitlines():
        line_clean = line.strip()
        if not line_clean:
            continue
        if any(keyword in line_clean.lower() for keyword in [
            "maak ", "script", "cleanup", "audit", "consolidation",
            "verify", "memory", "tasks", "prompt", "samenvatting"
        ]):
            found.append(line_clean)

    deduped: list[str] = []
    seen: set[str] = set()
    for item in found:
        short = item[:200]
        if short not in seen:
            seen.add(short)
            deduped.append(short)

    return deduped[:40]


def extract_completed_points(text: str) -> list[str]:
    candidates: list[str] = []
    lines = [x.strip() for x in text.splitlines() if x.strip()]

    keywords = [
        "succesvol", "afgerond", "completed", "overall_ok: True",
        "Removed:", "Moved from", "SAFE_MERGE", "structure_ok",
        "runtime_links_ok", "broken_symlinks_ok", "cleanup",
        "consolidation", "verify structure",
    ]

    for line in lines:
        low = line.lower()
        if any(k.lower() in low for k in keywords):
            candidates.append(line)

    return dedupe_preserve_order(candidates)[:30]


def extract_open_points(text: str) -> list[str]:
    candidates: list[str] = []
    lines = [x.strip() for x in text.splitlines() if x.strip()]

    hints = [
        "we moeten", "volgende stap", "to do", "openstaand",
        "nog", "later", "verder gaan", "back on track",
        "task", "memory", "md files", "prompt nodig",
    ]

    for line in lines:
        low = line.lower()
        if any(h in low for h in hints):
            candidates.append(line)

    return dedupe_preserve_order(candidates)[:30]


def dedupe_preserve_order(items: list[str]) -> list[str]:
    out: list[str] = []
    seen: set[str] = set()
    for item in items:
        key = item.strip()
        if not key or key in seen:
            continue
        seen.add(key)
        out.append(key)
    return out


def build_summary(
    topics: dict[str, int],
    files: list[str],
    phases: list[str],
    completed: list[str],
    open_points: list[str],
) -> str:
    topic_text = ", ".join(topics.keys()) if topics else "geen duidelijke topics gedetecteerd"
    phase_text = ", ".join(phases[:10]) if phases else "geen fases gedetecteerd"

    parts = [
        f"De chat draaide vooral om: {topic_text}.",
        f"Gedetecteerde fase-/scriptverwijzingen: {phase_text}.",
    ]

    if completed:
        parts.append(f"Belangrijke afgeronde punten: {len(completed)} items gedetecteerd.")
    if open_points:
        parts.append(f"Openstaande of vervolgpunten: {len(open_points)} items gedetecteerd.")
    if files:
        parts.append(f"Relevante bestanden/scripts gevonden: {min(len(files), 10)}+.")

    return " ".join(parts)


def format_list(items: list[str], fallback: str = "- none", limit: int = 12) -> str:
    if not items:
        return fallback
    return "\n".join(f"- {x}" for x in items[:limit])


def build_prompt(summary: str, topics: dict[str, int], completed: list[str], open_points: list[str], files: list[str]) -> str:
    topics_text = format_list([f"{k} ({v})" for k, v in topics.items()], fallback="- none")
    completed_text = format_list(completed)
    open_text = format_list(open_points)
    files_text = format_list(files)
    return PROMPT_TEMPLATE.format(
        summary=summary,
        topics=topics_text,
        completed=completed_text,
        open_items=open_text,
        files=files_text,
    ).strip() + "\n"


def write_reports(result: ExtractionResult) -> tuple[Path, Path]:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    txt_path = REPORTS / f"chat_context_extract_{timestamp}.txt"
    json_path = REPORTS / f"chat_context_extract_{timestamp}.json"

    lines: list[str] = [
        "=== ARC AI ANGELS — CHAT CONTEXT EXTRACTOR ===",
        f"Generated at: {result.generated_at}",
        f"Source file: {result.source_file}",
        f"Line count: {result.line_count}",
        "",
        "=== DETECTED TOPICS ===",
    ]

    if result.detected_topics:
        for k, v in result.detected_topics.items():
            lines.append(f"- {k}: {v}")
    else:
        lines.append("- none")

    lines += [
        "",
        "=== LIKELY FILES ===",
        format_list(result.likely_files, fallback="- none", limit=50),
        "",
        "=== LIKELY PHASES ===",
        format_list(result.likely_phases),
        "",
        "=== LIKELY ACTIONS ===",
        format_list(result.likely_actions, limit=30),
        "",
        "=== COMPLETED POINTS ===",
        format_list(result.completed_points, limit=30),
        "",
        "=== OPEN POINTS ===",
        format_list(result.open_points, limit=30),
        "",
        "=== SUMMARY ===",
        result.summary,
        "",
        "=== CONTINUATION PROMPT ===",
        result.continuation_prompt,
        "",
    ]

    txt_path.write_text("\n".join(lines), encoding="utf-8")
    json_path.write_text(json.dumps(asdict(result), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return txt_path, json_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract summary + continuation prompt from a saved chat/export.")
    parser.add_argument("input_file", help="Path to chat export (.txt, .md, .json, .jsonl)")
    args = parser.parse_args()

    input_path = Path(args.input_file).expanduser().resolve()
    if not input_path.exists():
        raise SystemExit(f"Input file does not exist: {input_path}")

    raw = read_text(input_path)
    text = normalize_whitespace(raw)

    lines = text.splitlines()
    topics = detect_topics(text)
    files = extract_likely_files(text)
    phases = extract_phases(text)
    actions = extract_actions(text)
    completed = extract_completed_points(text)
    open_points = extract_open_points(text)
    summary = build_summary(topics, files, phases, completed, open_points)
    prompt = build_prompt(summary, topics, completed, open_points, files)

    result = ExtractionResult(
        source_file=str(input_path),
        generated_at=datetime.now().isoformat(),
        line_count=len(lines),
        detected_topics=topics,
        likely_files=files,
        likely_phases=phases,
        likely_actions=actions,
        completed_points=completed,
        open_points=open_points,
        summary=summary,
        continuation_prompt=prompt,
    )

    txt_path, json_path = write_reports(result)

    print(f"TXT report:  {txt_path}")
    print(f"JSON report: {json_path}")


if __name__ == "__main__":
    main()

