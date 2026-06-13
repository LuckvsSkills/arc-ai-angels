#!/usr/bin/env python3
from pathlib import Path
from datetime import datetime
import json
import re
import sys
import hashlib

BASE = Path.home() / "arc_ai_angels"
REPORTS = BASE / "reports"
CHAT_ANALYSIS = REPORTS / "chat_analysis"

CHAT_ANALYSIS.mkdir(parents=True, exist_ok=True)

TOPIC_PATTERNS = {
    "canon": [
        r"\bcanon\b",
        r"\bcanonical\b",
        r"\bdomain\b",
        r"\bdomains\b",
        r"\bsentinel\b",
        r"\bsentinels\b",
        r"\blead agent\b",
        r"\bomni\b",
    ],
    "tasks": [
        r"\btasks\.md\b",
        r"\btask\b",
        r"\btasks\b",
        r"\btask list\b",
        r"\bopenstaand\b",
        r"\bvolgende stap\b",
        r"\bnext step\b",
        r"\bto do\b",
        r"\btodo\b",
    ],
    "memory": [
        r"\bmemory\.md\b",
        r"\bmemory\b",
        r"\bremember\b",
        r"\bopslaan\b",
        r"\bgeheugen\b",
        r"\bcontext\b",
    ],
    "structure": [
        r"\bdirectory\b",
        r"\bcleanup\b",
        r"\bconsolidation\b",
        r"\bconsolidatie\b",
        r"\bstructure\b",
        r"\bstructuur\b",
        r"\bagents\b",
        r"\bomni\b",
        r"\bstub\b",
        r"\bverify\b",
    ],
    "reports": [
        r"\breport\b",
        r"\breports\b",
        r"\baudit\b",
        r"\bphase [a-z]\b",
        r"\bphase_[a-z]\b",
    ],
}

ACTION_PATTERNS = [
    ("cleanup", r"\bcleanup\b|\bopruimen\b"),
    ("consolidation", r"\bconsolidation\b|\bconsolidatie\b"),
    ("verify structure", r"\bverify structure\b|\bstructuur check\b"),
    ("audit", r"\baudit\b"),
    ("canon", r"\bcanon\b"),
    ("memory", r"\bmemory\b"),
    ("tasks", r"\btasks\.md\b|\btasks\b"),
]

FILE_PATTERNS = [
    r"\b[A-Z0-9_./-]+\.md\b",
    r"\b[A-Z0-9_./-]+\.py\b",
    r"\b[A-Z0-9_./-]+\.json\b",
    r"\b[A-Z0-9_./-]+\.txt\b",
]

PHASE_PATTERNS = [
    r"\bphase[_ ]a\b",
    r"\bphase[_ ]b\b",
    r"\bphase[_ ]c\b",
    r"\bphase[_ ]d\b",
    r"\bphase[_ ]e\b",
    r"\bphase[_ ]f\b",
    r"\bphase[_ ]g\b",
    r"\bphase[_ ]h\b",
    r"\bphase[_ ]i\b",
]

COMPLETED_PATTERNS = [
    r"\bafgerond\b",
    r"\buitgevoerd\b",
    r"\bvoltooid\b",
    r"\bsuccesvol\b",
    r"\boverall_ok\b",
    r"\bgereed\b",
    r"\bdone\b",
    r"\bcompleted\b",
]

OPEN_PATTERNS = [
    r"\bvolgende stap\b",
    r"\bopenstaand\b",
    r"\bnog doen\b",
    r"\bmoeten nog\b",
    r"\bto do\b",
    r"\btodo\b",
    r"\bnext step\b",
    r"\bstaat nog open\b",
]

CANON_PATTERNS = [
    r"\bcanon\b",
    r"\bcanonical\b",
    r"\bdomain label\b",
    r"\blead agent\b",
    r"\bsentinel\b",
    r"\bowner_agent\b",
    r"\bassigned_to\b",
    r"\bassigned_by\b",
    r"\bfinix\b",
    r"\bhelix\b",
    r"\bmatrix\b",
    r"\bquantix\b",
    r"\bzenix\b",
    r"\bfinoria\b",
    r"\bcortexia\b",
    r"\bsaelia\b",
    r"\blumeria\b",
    r"\bfluentia\b",
]

TASK_PATTERNS = [
    r"\btask\b",
    r"\btasks\b",
    r"\bvolgende stap\b",
    r"\bopenstaand\b",
    r"\bactiepunt\b",
    r"\bactiepunten\b",
    r"\bnext step\b",
    r"\btodo\b",
]

MEMORY_PATTERNS = [
    r"\bmemory\b",
    r"\bonthouden\b",
    r"\bremember\b",
    r"\bcontext\b",
    r"\bbelangrijk\b",
    r"\bvoorkeur\b",
    r"\bwerkwijze\b",
]

def slugify(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = re.sub(r"-+", "-", text).strip("-")
    return text or "chat"

def sha1_text(text: str) -> str:
    return hashlib.sha1(text.encode("utf-8", errors="ignore")).hexdigest()

def unique_preserve(seq):
    seen = set()
    out = []
    for item in seq:
        if item not in seen:
            seen.add(item)
            out.append(item)
    return out

def score_topics(lines):
    scores = {k: 0 for k in TOPIC_PATTERNS}
    for line in lines:
        low = line.lower()
        for topic, patterns in TOPIC_PATTERNS.items():
            for pat in patterns:
                if re.search(pat, low):
                    scores[topic] += 1
    return scores

def detect_files(lines):
    found = []
    for line in lines:
        for pat in FILE_PATTERNS:
            found.extend(re.findall(pat, line, flags=re.IGNORECASE))
    return unique_preserve(found)

def detect_phases(text):
    found = []
    low = text.lower()
    for pat in PHASE_PATTERNS:
        for m in re.findall(pat, low):
            found.append(m.replace(" ", "_"))
    return unique_preserve(found)

def detect_actions(lines):
    found = []
    for line in lines:
        low = line.lower()
        for label, pat in ACTION_PATTERNS:
            if re.search(pat, low):
                found.append(label)
    return unique_preserve(found)

def detect_completed(lines):
    out = []
    for line in lines:
        low = line.lower()
        if any(re.search(p, low) for p in COMPLETED_PATTERNS):
            out.append(line.strip())
    return unique_preserve(out)

def detect_open(lines):
    out = []
    for line in lines:
        low = line.lower()
        if any(re.search(p, low) for p in OPEN_PATTERNS):
            out.append(line.strip())
    return unique_preserve(out)

def candidate_lines(lines, patterns):
    out = []
    for line in lines:
        low = line.lower()
        if any(re.search(p, low) for p in patterns):
            cleaned = line.strip()
            if cleaned:
                out.append(cleaned)
    return unique_preserve(out)

def write_candidates(path: Path, title: str, items):
    timestamp = datetime.now().isoformat()
    with path.open("a", encoding="utf-8") as f:
        f.write(f"\n## {title}\n")
        f.write(f"Generated at: {timestamp}\n\n")
        if items:
            for item in items:
                f.write(f"- {item}\n")
        else:
            f.write("- none\n")

def make_summary(topic_scores, phases, actions, completed, open_points, files):
    top_topics = [k for k, v in sorted(topic_scores.items(), key=lambda kv: kv[1], reverse=True) if v > 0]
    parts = []
    if top_topics:
        parts.append("De chat draaide vooral om: " + ", ".join(top_topics) + ".")
    if phases:
        parts.append("Gedetecteerde fase-/scriptverwijzingen: " + ", ".join(phases) + ".")
    parts.append(f"Belangrijke afgeronde punten: {len(completed)} items gedetecteerd.")
    parts.append(f"Openstaande of vervolgpunten: {len(open_points)} items gedetecteerd.")
    parts.append(f"Relevante bestanden/scripts gevonden: {len(files)}.")
    return " ".join(parts)

def build_continuation_prompt(summary, topic_scores, completed, open_points, files, canon_candidates, task_candidates, memory_candidates):
    top_topics = [f"- {k} ({v})" for k, v in sorted(topic_scores.items(), key=lambda kv: kv[1], reverse=True) if v > 0]
    lines = []
    lines.append("# CONTEXT CONTINUATION — ARC AI ANGELS")
    lines.append("")
    lines.append("## Korte samenvatting")
    lines.append(summary)
    lines.append("")
    lines.append("## Hoofdthema's uit vorige chat")
    lines.extend(top_topics or ["- none"])
    lines.append("")
    lines.append("## Belangrijke afgeronde punten")
    lines.extend(f"- {x}" for x in completed[:20]) or lines.append("- none")
    lines.append("")
    lines.append("## Openstaande punten")
    lines.extend(f"- {x}" for x in open_points[:20]) or lines.append("- none")
    lines.append("")
    lines.append("## Relevante bestanden / scripts")
    lines.extend(f"- {x}" for x in files[:30]) or lines.append("- none")
    lines.append("")
    lines.append("## Canon-kandidaten")
    lines.extend(f"- {x}" for x in canon_candidates[:20]) or lines.append("- none")
    lines.append("")
    lines.append("## TASKS-kandidaten")
    lines.extend(f"- {x}" for x in task_candidates[:20]) or lines.append("- none")
    lines.append("")
    lines.append("## MEMORY-kandidaten")
    lines.extend(f"- {x}" for x in memory_candidates[:20]) or lines.append("- none")
    lines.append("")
    lines.append("## Werkinstructie")
    lines.append("Ga verder waar de vorige chat stopte. Bewaak canon-consistentie, wees exact met bestandsnamen en wijzig niets zonder duidelijk doel.")
    return "\n".join(lines)

def main():
    if len(sys.argv) < 3:
        print("Gebruik:")
        print("  python3 chat_context_extractor_v3.py <pad_naar_chat_dump.txt> <chat_titel>")
        sys.exit(1)

    source_file = Path(sys.argv[1]).expanduser()
    chat_title_raw = sys.argv[2].strip()
    chat_slug = slugify(chat_title_raw)

    if not source_file.exists():
        print(f"Input file does not exist: {source_file}")
        sys.exit(1)

    raw = source_file.read_text(encoding="utf-8", errors="ignore")
    lines = [line.rstrip() for line in raw.splitlines() if line.strip()]

    topic_scores = score_topics(lines)
    files = detect_files(lines)
    phases = detect_phases(raw)
    actions = detect_actions(lines)
    completed = detect_completed(lines)
    open_points = detect_open(lines)

    canon_candidates = candidate_lines(lines, CANON_PATTERNS)
    task_candidates = candidate_lines(lines, TASK_PATTERNS)
    memory_candidates = candidate_lines(lines, MEMORY_PATTERNS)

    summary = make_summary(topic_scores, phases, actions, completed, open_points, files)
    continuation_prompt = build_continuation_prompt(
        summary,
        topic_scores,
        completed,
        open_points,
        files,
        canon_candidates,
        task_candidates,
        memory_candidates,
    )

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    chat_dir = CHAT_ANALYSIS / chat_slug
    chat_dir.mkdir(parents=True, exist_ok=True)

    report_txt = chat_dir / f"chat_context_extract_{timestamp}.txt"
    report_json = chat_dir / f"chat_context_extract_{timestamp}.json"
    clean_txt = chat_dir / f"{chat_slug}_clean.txt"
    prompt_txt = chat_dir / f"{chat_slug}_continuation_prompt.txt"

    clean_payload = {
        "chat_title": chat_title_raw,
        "chat_slug": chat_slug,
        "generated_at": datetime.now().isoformat(),
        "source_file": str(source_file),
        "source_sha1": sha1_text(raw),
        "summary": summary,
        "topics": topic_scores,
        "files": files,
        "phases": phases,
        "actions": actions,
        "completed_points": completed,
        "open_points": open_points,
        "canon_candidates": canon_candidates,
        "tasks_candidates": task_candidates,
        "memory_candidates": memory_candidates,
        "continuation_prompt": continuation_prompt,
    }

    clean_lines = []
    clean_lines.append(f"CHAT TITLE: {chat_title_raw}")
    clean_lines.append(f"CHAT SLUG: {chat_slug}")
    clean_lines.append(f"GENERATED AT: {clean_payload['generated_at']}")
    clean_lines.append(f"SOURCE FILE: {source_file}")
    clean_lines.append("")
    clean_lines.append("=== SUMMARY ===")
    clean_lines.append(summary)
    clean_lines.append("")
    clean_lines.append("=== COMPLETED POINTS ===")
    clean_lines.extend(f"- {x}" for x in completed) or clean_lines.append("- none")
    clean_lines.append("")
    clean_lines.append("=== OPEN POINTS ===")
    clean_lines.extend(f"- {x}" for x in open_points) or clean_lines.append("- none")
    clean_lines.append("")
    clean_lines.append("=== CANON CANDIDATES ===")
    clean_lines.extend(f"- {x}" for x in canon_candidates) or clean_lines.append("- none")
    clean_lines.append("")
    clean_lines.append("=== TASKS CANDIDATES ===")
    clean_lines.extend(f"- {x}" for x in task_candidates) or clean_lines.append("- none")
    clean_lines.append("")
    clean_lines.append("=== MEMORY CANDIDATES ===")
    clean_lines.extend(f"- {x}" for x in memory_candidates) or clean_lines.append("- none")
    clean_lines.append("")
    clean_lines.append("=== CONTINUATION PROMPT ===")
    clean_lines.append(continuation_prompt)
    clean_lines.append("")

    report_lines = []
    report_lines.append("=== ARC AI ANGELS — CHAT CONTEXT EXTRACTOR V3 ===")
    report_lines.append(f"Generated at: {clean_payload['generated_at']}")
    report_lines.append(f"Source file: {source_file}")
    report_lines.append(f"Chat title: {chat_title_raw}")
    report_lines.append(f"Chat slug: {chat_slug}")
    report_lines.append(f"Line count: {len(lines)}")
    report_lines.append("")
    report_lines.append("=== DETECTED TOPICS ===")
    for k, v in sorted(topic_scores.items(), key=lambda kv: kv[0]):
        report_lines.append(f"- {k}: {v}")
    report_lines.append("")
    report_lines.append("=== LIKELY FILES ===")
    if files:
        report_lines.extend(f"- {x}" for x in files)
    else:
        report_lines.append("- none")
    report_lines.append("")
    report_lines.append("=== LIKELY PHASES ===")
    if phases:
        report_lines.extend(f"- {x}" for x in phases)
    else:
        report_lines.append("- none")
    report_lines.append("")
    report_lines.append("=== LIKELY ACTIONS ===")
    if actions:
        report_lines.extend(f"- {x}" for x in actions)
    else:
        report_lines.append("- none")
    report_lines.append("")
    report_lines.append("=== COMPLETED POINTS ===")
    if completed:
        report_lines.extend(f"- {x}" for x in completed)
    else:
        report_lines.append("- none")
    report_lines.append("")
    report_lines.append("=== OPEN POINTS ===")
    if open_points:
        report_lines.extend(f"- {x}" for x in open_points)
    else:
        report_lines.append("- none")
    report_lines.append("")
    report_lines.append("=== CANON CANDIDATES ===")
    if canon_candidates:
        report_lines.extend(f"- {x}" for x in canon_candidates)
    else:
        report_lines.append("- none")
    report_lines.append("")
    report_lines.append("=== TASKS CANDIDATES ===")
    if task_candidates:
        report_lines.extend(f"- {x}" for x in task_candidates)
    else:
        report_lines.append("- none")
    report_lines.append("")
    report_lines.append("=== MEMORY CANDIDATES ===")
    if memory_candidates:
        report_lines.extend(f"- {x}" for x in memory_candidates)
    else:
        report_lines.append("- none")
    report_lines.append("")
    report_lines.append("=== SUMMARY ===")
    report_lines.append(summary)
    report_lines.append("")
    report_lines.append("=== CONTINUATION PROMPT ===")
    report_lines.append(continuation_prompt)
    report_lines.append("")

    report_txt.write_text("\n".join(report_lines) + "\n", encoding="utf-8")
    report_json.write_text(json.dumps(clean_payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    clean_txt.write_text("\n".join(clean_lines) + "\n", encoding="utf-8")
    prompt_txt.write_text(continuation_prompt + "\n", encoding="utf-8")

    canon_candidates_file = CHAT_ANALYSIS / "CANON_CANDIDATES.md"
    tasks_candidates_file = CHAT_ANALYSIS / "TASKS_CANDIDATES.md"
    memory_candidates_file = CHAT_ANALYSIS / "MEMORY_CANDIDATES.md"

    write_candidates(canon_candidates_file, chat_title_raw, canon_candidates)
    write_candidates(tasks_candidates_file, chat_title_raw, task_candidates)
    write_candidates(memory_candidates_file, chat_title_raw, memory_candidates)

    print(f"TXT report: {report_txt}")
    print(f"JSON report: {report_json}")
    print(f"CLEAN file: {clean_txt}")
    print(f"PROMPT file: {prompt_txt}")
    print(f"CANON candidates: {canon_candidates_file}")
    print(f"TASKS candidates: {tasks_candidates_file}")
    print(f"MEMORY candidates: {memory_candidates_file}")
    print("")
    print("Klaar.")
    print("Je kunt nu stoppen met Ctrl+C of gewoon het terminalvenster blijven gebruiken.")

if __name__ == "__main__":
    main()

