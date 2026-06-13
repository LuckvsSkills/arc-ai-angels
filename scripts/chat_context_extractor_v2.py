#!/usr/bin/env python3
from pathlib import Path
from datetime import datetime
import json
import re
import shutil
import subprocess
import sys


BASE = Path.home() / "arc_ai_angels"
REPORTS = BASE / "reports"
ANALYSIS_DIR = REPORTS / "chat_analysis"

INBOX_DIR = ANALYSIS_DIR / "_inbox"
RAW_DIR = ANALYSIS_DIR / "raw_dumps"
CLEAN_DIR = ANALYSIS_DIR / "clean_context"
PROMPTS_DIR = ANALYSIS_DIR / "continuation_prompts"
CANON_DIR = ANALYSIS_DIR / "canon_candidates"
TASKS_DIR = ANALYSIS_DIR / "tasks_candidates"
MEMORY_DIR = ANALYSIS_DIR / "memory_candidates"
JSON_DIR = ANALYSIS_DIR / "json"

TOPIC_KEYWORDS = {
    "canon": [
        "canon", "domain", "sentinel", "lead agent", "omni", "routing", "governance"
    ],
    "tasks": [
        "task", "tasks", "todo", "next step", "phase", "cleanup", "audit", "script"
    ],
    "memory": [
        "memory", "remember", "context", "continuation", "summary", "chat history"
    ],
    "structure": [
        "directory", "folder", "agents", "workspace", "sessions", "runtime", "cleanup",
        "consolidation", "structure"
    ],
    "agents": [
        "nova", "flux", "flux_core", "flux-core", "main", "helix", "matrix", "quantix",
        "zenix", "finix", "nero", "solis", "sora", "vector", "vondra", "arix", "axon",
        "clio", "daxio", "draven", "elora", "enki", "forge", "kairo", "kenzo",
        "kresta", "luvia", "nura", "odis", "orizon", "tharos", "unia", "ventura",
        "zena", "zion"
    ],
}

PHASE_PATTERNS = {
    "phase_a": r"\bphase\s*a\b|\bfase\s*a\b",
    "phase_b": r"\bphase\s*b\b|\bfase\s*b\b",
    "phase_c": r"\bphase\s*c\b|\bfase\s*c\b",
    "phase_d": r"\bphase\s*d\b|\bfase\s*d\b",
    "phase_e": r"\bphase\s*e\b|\bfase\s*e\b",
    "phase_f": r"\bphase\s*f\b|\bfase\s*f\b",
    "phase_g": r"\bphase\s*g\b|\bfase\s*g\b",
}

ACTION_PATTERNS = {
    "cleanup": r"\bcleanup\b|\bcleaning\b|\bopschonen\b",
    "consolidation": r"\bconsolidat",
    "verify structure": r"\bverify structure\b|\bstructure check\b|\boverall_ok\b",
    "audit": r"\baudit\b",
    "canon": r"\bcanon\b",
    "memory": r"\bmemory\b",
    "tasks": r"\btasks\.md\b|\btasks\b",
}


def slugify(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[^a-z0-9._-]+", "_", text)
    text = re.sub(r"_+", "_", text).strip("_")
    return text or "untitled_chat"


def ensure_dirs():
    for d in [
        REPORTS,
        ANALYSIS_DIR,
        INBOX_DIR,
        RAW_DIR,
        CLEAN_DIR,
        PROMPTS_DIR,
        CANON_DIR,
        TASKS_DIR,
        MEMORY_DIR,
        JSON_DIR,
    ]:
        d.mkdir(parents=True, exist_ok=True)


def count_topics(text: str):
    lowered = text.lower()
    scores = {}
    for topic, words in TOPIC_KEYWORDS.items():
        count = 0
        for w in words:
            count += lowered.count(w.lower())
        if count:
            scores[topic] = count
    return dict(sorted(scores.items(), key=lambda kv: (-kv[1], kv[0])))


def detect_phases(text: str):
    lowered = text.lower()
    found = []
    for name, pattern in PHASE_PATTERNS.items():
        if re.search(pattern, lowered, re.IGNORECASE):
            found.append(name)
    return found


def detect_actions(text: str):
    lowered = text.lower()
    found = []
    for name, pattern in ACTION_PATTERNS.items():
        if re.search(pattern, lowered, re.IGNORECASE):
            found.append(name)
    return found


def detect_files(text: str):
    candidates = set()

    for m in re.findall(r"\b[A-Z0-9_./-]+\.md\b", text):
        candidates.add(m)

    known = [
        "CANON.md",
        "TASKS.md",
        "MEMORY.md",
        "TASKS_CANDIDATES.md",
        "MEMORY_CANDIDATES.md",
        "CANON_CANDIDATES.md",
        "PHASE_STATUS.md",
    ]
    lowered = text.lower()
    for k in known:
        if k.lower() in lowered:
            candidates.add(k)

    return sorted(candidates)


def extract_lines(text: str):
    raw_lines = text.splitlines()
    cleaned = []
    for line in raw_lines:
        s = line.strip()
        if not s:
            continue
        if s == "EOF":
            continue
        cleaned.append(s)
    return cleaned


def classify_lines(lines):
    completed = []
    open_points = []
    canon_candidates = []
    tasks_candidates = []
    memory_candidates = []

    for line in lines:
        lowered = line.lower()

        if any(x in lowered for x in [
            "afgerond", "uitgevoerd", "voltooid", "done", "overall_ok true", "overall_ok: true",
            "succesvol", "successfully", "safe_merge", "safe to remove"
        ]):
            completed.append(line)

        if any(x in lowered for x in [
            "volgende stap", "openstaand", "open points", "todo", "to do", "moet nog",
            "nalopen", "structureren", "verder gaan", "back on track"
        ]):
            open_points.append(line)

        if any(x in lowered for x in [
            "canon", "domain", "sentinel", "lead agent", "routing", "governance", "omni"
        ]):
            canon_candidates.append(line)

        if any(x in lowered for x in [
            "task", "tasks", "phase", "audit", "cleanup", "consolidation", "script", "next step"
        ]):
            tasks_candidates.append(line)

        if any(x in lowered for x in [
            "memory", "context", "summary", "chat history", "continuation", "remember"
        ]):
            memory_candidates.append(line)

    def dedupe(items):
        seen = set()
        out = []
        for item in items:
            if item not in seen:
                seen.add(item)
                out.append(item)
        return out

    return {
        "completed": dedupe(completed),
        "open_points": dedupe(open_points),
        "canon_candidates": dedupe(canon_candidates),
        "tasks_candidates": dedupe(tasks_candidates),
        "memory_candidates": dedupe(memory_candidates),
    }


def build_summary(topic_scores, phases, actions, classified, files_found):
    top_topics = ", ".join(topic_scores.keys()) if topic_scores else "geen duidelijke topics"
    phase_text = ", ".join(phases) if phases else "geen fases gedetecteerd"
    return (
        f"De chat draaide vooral om: {top_topics}. "
        f"Gedetecteerde fase-/scriptverwijzingen: {phase_text}. "
        f"Belangrijke afgeronde punten: {len(classified['completed'])} items gedetecteerd. "
        f"Openstaande of vervolgpunten: {len(classified['open_points'])} items gedetecteerd. "
        f"Relevante bestanden/scripts gevonden: {len(files_found)}."
    )


def write_list(path: Path, title: str, items):
    lines = [title, ""]
    if items:
        for item in items:
            lines.append(f"- {item}")
    else:
        lines.append("- none")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def build_continuation_prompt(summary, topic_scores, classified, files_found):
    lines = []
    lines.append("# CONTEXT CONTINUATION — ARC AI ANGELS")
    lines.append("")
    lines.append("## Korte samenvatting")
    lines.append(summary)
    lines.append("")
    lines.append("## Hoofdthema's uit vorige chat")
    if topic_scores:
        for k, v in topic_scores.items():
            lines.append(f"- {k} ({v})")
    else:
        lines.append("- none")
    lines.append("")
    lines.append("## Belangrijke afgeronde punten")
    if classified["completed"]:
        for item in classified["completed"]:
            lines.append(f"- {item}")
    else:
        lines.append("- none")
    lines.append("")
    lines.append("## Openstaande punten")
    if classified["open_points"]:
        for item in classified["open_points"]:
            lines.append(f"- {item}")
    else:
        lines.append("- none")
    lines.append("")
    lines.append("## Relevante bestanden / scripts")
    if files_found:
        for item in files_found:
            lines.append(f"- {item}")
    else:
        lines.append("- none")
    lines.append("")
    lines.append("## Werkinstructie")
    lines.append(
        "Ga verder waar de vorige chat stopte. Bewaak canon-consistentie, wees exact met bestandsnamen en wijzig niets zonder duidelijk doel."
    )
    lines.append("")
    return "\n".join(lines) + "\n"


def analyze_chat_dump(source_file: Path, clean_name: str):
    ensure_dirs()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    clean_slug = slugify(clean_name)

    raw_copy = RAW_DIR / f"{clean_slug}__raw_{timestamp}.txt"
    clean_txt = CLEAN_DIR / f"{clean_slug}__clean_{timestamp}.txt"
    prompt_txt = PROMPTS_DIR / f"{clean_slug}__prompt_{timestamp}.md"
    canon_txt = CANON_DIR / f"{clean_slug}__CANON_CANDIDATES_{timestamp}.md"
    tasks_txt = TASKS_DIR / f"{clean_slug}__TASKS_CANDIDATES_{timestamp}.md"
    memory_txt = MEMORY_DIR / f"{clean_slug}__MEMORY_CANDIDATES_{timestamp}.md"
    report_txt = ANALYSIS_DIR / f"{clean_slug}__analysis_{timestamp}.txt"
    report_json = JSON_DIR / f"{clean_slug}__analysis_{timestamp}.json"

    text = source_file.read_text(encoding="utf-8", errors="replace")
    shutil.copy2(source_file, raw_copy)

    lines = extract_lines(text)
    clean_txt.write_text("\n".join(lines) + "\n", encoding="utf-8")

    joined = "\n".join(lines)
    topic_scores = count_topics(joined)
    phases = detect_phases(joined)
    actions = detect_actions(joined)
    files_found = detect_files(joined)
    classified = classify_lines(lines)
    summary = build_summary(topic_scores, phases, actions, classified, files_found)
    continuation_prompt = build_continuation_prompt(summary, topic_scores, classified, files_found)

    prompt_txt.write_text(continuation_prompt, encoding="utf-8")
    write_list(canon_txt, "# CANON CANDIDATES", classified["canon_candidates"])
    write_list(tasks_txt, "# TASKS CANDIDATES", classified["tasks_candidates"])
    write_list(memory_txt, "# MEMORY CANDIDATES", classified["memory_candidates"])

    results = {
        "generated_at": datetime.now().isoformat(),
        "source_file": str(source_file),
        "raw_copy": str(raw_copy),
        "clean_file": str(clean_txt),
        "continuation_prompt_file": str(prompt_txt),
        "canon_candidates_file": str(canon_txt),
        "tasks_candidates_file": str(tasks_txt),
        "memory_candidates_file": str(memory_txt),
        "line_count": len(lines),
        "topics": topic_scores,
        "files_found": files_found,
        "phases": phases,
        "actions": actions,
        "completed_points": classified["completed"],
        "open_points": classified["open_points"],
        "summary": summary,
    }

    out = []
    out.append("=== ARC AI ANGELS — CHAT CONTEXT EXTRACTOR V2 ===")
    out.append(f"Generated at: {results['generated_at']}")
    out.append(f"Source file: {results['source_file']}")
    out.append(f"Line count: {results['line_count']}")
    out.append("")

    out.append("=== OUTPUT FILES ===")
    out.append(f"- raw_copy: {raw_copy}")
    out.append(f"- clean_file: {clean_txt}")
    out.append(f"- continuation_prompt: {prompt_txt}")
    out.append(f"- canon_candidates: {canon_txt}")
    out.append(f"- tasks_candidates: {tasks_txt}")
    out.append(f"- memory_candidates: {memory_txt}")
    out.append("")

    out.append("=== DETECTED TOPICS ===")
    if topic_scores:
        for k, v in topic_scores.items():
            out.append(f"- {k}: {v}")
    else:
        out.append("- none")
    out.append("")

    out.append("=== LIKELY FILES ===")
    if files_found:
        for item in files_found:
            out.append(f"- {item}")
    else:
        out.append("- none")
    out.append("")

    out.append("=== LIKELY PHASES ===")
    if phases:
        for item in phases:
            out.append(f"- {item}")
    else:
        out.append("- none")
    out.append("")

    out.append("=== LIKELY ACTIONS ===")
    if actions:
        for item in actions:
            out.append(f"- {item}")
    else:
        out.append("- none")
    out.append("")

    out.append("=== COMPLETED POINTS ===")
    if classified["completed"]:
        for item in classified["completed"]:
            out.append(f"- {item}")
    else:
        out.append("- none")
    out.append("")

    out.append("=== OPEN POINTS ===")
    if classified["open_points"]:
        for item in classified["open_points"]:
            out.append(f"- {item}")
    else:
        out.append("- none")
    out.append("")

    out.append("=== SUMMARY ===")
    out.append(summary)
    out.append("")

    out.append("=== CONTINUATION PROMPT ===")
    out.append(continuation_prompt.rstrip())
    out.append("")

    report_txt.write_text("\n".join(out) + "\n", encoding="utf-8")
    report_json.write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"TXT report: {report_txt}")
    print(f"JSON report: {report_json}")
    print("")
    print("Aangemaakte bestanden:")
    print(f"- Clean data:            {clean_txt}")
    print(f"- Continuation prompt:   {prompt_txt}")
    print(f"- Canon candidates:      {canon_txt}")
    print(f"- Tasks candidates:      {tasks_txt}")
    print(f"- Memory candidates:     {memory_txt}")

    return {
        "temp_source": source_file,
        "report_txt": report_txt,
        "report_json": report_json,
    }


def run_editor(temp_dump: Path):
    editor = shutil.which("nano") or shutil.which("vi") or shutil.which("vim")
    if not editor:
        print("Geen editor gevonden. Installeer nano of gebruik handmatig een bestand.")
        sys.exit(1)

    subprocess.run([editor, str(temp_dump)])


def prompt_yes_no(question: str) -> bool:
    while True:
        ans = input(f"{question} [j/n]: ").strip().lower()
        if ans in {"j", "ja", "y", "yes"}:
            return True
        if ans in {"n", "nee", "no"}:
            return False
        print("Typ j of n.")


def main():
    ensure_dirs()

    print("=== ARC AI ANGELS — CHAT CONTEXT EXTRACTOR V2 ===")
    print("")
    print(f"Outputmap: {ANALYSIS_DIR}")
    print("")

    while True:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        temp_dump = INBOX_DIR / f"chat_dump_{timestamp}.txt"

        temp_dump.write_text("", encoding="utf-8")

        print(f"Tijdelijke dumpfile: {temp_dump}")
        print("")
        print("Er wordt nu een editor geopend.")
        print("Plak daar de chatgeschiedenis in.")
        print("Sla op en sluit af.")
        print("In nano is dat: Ctrl+O, Enter, Ctrl+X")
        print("")

        run_editor(temp_dump)

        try:
            content = temp_dump.read_text(encoding="utf-8", errors="replace").strip()
        except Exception as e:
            print(f"Kon dumpfile niet lezen: {e}")
            if temp_dump.exists():
                try:
                    temp_dump.unlink()
                except Exception:
                    pass
            continue

        if not content:
            print("Dumpfile was leeg. Probeer opnieuw.")
            if temp_dump.exists():
                try:
                    temp_dump.unlink()
                except Exception:
                    pass
            continue

        clean_name = input("Hoe moet de clean analyse heten? ").strip()
        if not clean_name:
            clean_name = f"chat_{timestamp}"

        analyze_chat_dump(temp_dump, clean_name)

        # temp dump verwijderen na succesvolle analyse
        try:
            temp_dump.unlink()
            print(f"Tijdelijke dump verwijderd: {temp_dump}")
        except Exception as e:
            print(f"Kon tijdelijke dump niet verwijderen: {e}")

        print("")
        again = prompt_yes_no("Nog een chat analyseren?")
        if not again:
            print("Klaar. Script wordt afgesloten.")
            break
        print("")


if __name__ == "__main__":
    main()
