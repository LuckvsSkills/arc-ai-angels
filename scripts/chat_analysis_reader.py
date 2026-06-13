#!/usr/bin/env python3
from pathlib import Path
from datetime import datetime
import os
import sys
import subprocess

BASE = Path.home() / "arc_ai_angels" / "reports" / "chat_analysis"

ANSI = {
    "reset": "\033[0m",
    "bold": "\033[1m",
    "dim": "\033[2m",
    "red": "\033[91m",
    "green": "\033[92m",
    "yellow": "\033[93m",
    "blue": "\033[94m",
    "magenta": "\033[95m",
    "cyan": "\033[96m",
    "gray": "\033[90m",
    "white": "\033[97m",
}

CATEGORY_ORDER = [
    "analysis",
    "continuation_prompts",
    "canon_candidates",
    "memory_candidates",
    "tasks_candidates",
    "clean_context",
    "raw_dumps",
    "json",
    "_inbox",
]

CATEGORY_META = {
    "analysis": {"label": "ANALYSIS", "color": "blue"},
    "continuation_prompts": {"label": "PROMPT", "color": "green"},
    "canon_candidates": {"label": "CANON", "color": "yellow"},
    "memory_candidates": {"label": "MEMORY", "color": "magenta"},
    "tasks_candidates": {"label": "TASKS", "color": "cyan"},
    "clean_context": {"label": "CLEAN", "color": "white"},
    "raw_dumps": {"label": "RAW", "color": "gray"},
    "json": {"label": "JSON", "color": "red"},
    "_inbox": {"label": "INBOX", "color": "gray"},
    "root": {"label": "ROOT", "color": "white"},
}

ROOT_AGGREGATES = {
    "CANON_CANDIDATES.md": "canon_candidates",
    "MEMORY_CANDIDATES.md": "memory_candidates",
    "TASKS_CANDIDATES.md": "tasks_candidates",
}

IGNORED_ROOT_FILES = {"chat_dump.txt"}

def color(text: str, name: str) -> str:
    return f"{ANSI.get(name, '')}{text}{ANSI['reset']}"

def clear_screen():
    os.system("clear")

def pause():
    input("\nDruk op Enter om verder te gaan...")

def safe_rel(path: Path) -> str:
    try:
        return str(path.relative_to(BASE))
    except Exception:
        return str(path)

def fmt_time(ts: float) -> str:
    return datetime.fromtimestamp(ts).strftime("%d-%m %H:%M")

def file_size_str(size: int) -> str:
    if size < 1024:
        return f"{size}B"
    if size < 1024 * 1024:
        return f"{size / 1024:.1f}K"
    return f"{size / (1024 * 1024):.1f}M"

def run_pager_for_file(path: Path):
    pager = os.environ.get("PAGER", "less")
    try:
        subprocess.run([pager, str(path)])
    except Exception:
        print(f"Kon pager niet openen. Bestand: {path}")

def run_nano(path: Path):
    try:
        subprocess.run(["nano", str(path)])
    except Exception:
        print(f"Kon nano niet openen. Bestand: {path}")

def read_preview(path: Path, mode: str = "head", lines: int = 40):
    try:
        content = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except Exception as e:
        print(f"Leesfout: {e}")
        return

    print()
    print(color(f"=== PREVIEW: {safe_rel(path)} ===", "bold"))

    if not content:
        print("(leeg bestand)")
        return

    if mode == "head":
        selected = content[:lines]
        start_no = 1
    elif mode == "tail":
        selected = content[-lines:]
        start_no = max(1, len(content) - len(selected) + 1)
    else:
        selected = content[:lines]
        start_no = 1

    for idx, line in enumerate(selected, start=start_no):
        print(f"{str(idx).rjust(4)} | {line}")

def grep_in_file(path: Path, needle: str):
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except Exception as e:
        print(f"Leesfout: {e}")
        return

    matches = []
    low = needle.lower()
    for i, line in enumerate(lines, start=1):
        if low in line.lower():
            matches.append((i, line))

    print()
    print(color(f"=== ZOEKRESULTATEN: {safe_rel(path)} ===", "bold"))
    print(f"Zoekterm: {needle}")
    print()

    if not matches:
        print("Geen matches gevonden.")
        return

    for i, line in matches[:100]:
        print(f"{str(i).rjust(4)} | {line}")

    if len(matches) > 100:
        print()
        print(f"... nog {len(matches) - 100} extra matches niet getoond.")

def detect_category(path: Path) -> str:
    rel = safe_rel(path)
    parts = Path(rel).parts
    if not parts:
        return "root"

    if parts[0] in CATEGORY_META:
        return parts[0]

    name = path.name
    if "__analysis_" in name and name.endswith(".txt"):
        return "analysis"
    if "__prompt_" in name:
        return "continuation_prompts"
    if "__CANON_CANDIDATES_" in name or name == "CANON_CANDIDATES.md":
        return "canon_candidates"
    if "__MEMORY_CANDIDATES_" in name or name == "MEMORY_CANDIDATES.md":
        return "memory_candidates"
    if "__TASKS_CANDIDATES_" in name or name == "TASKS_CANDIDATES.md":
        return "tasks_candidates"
    if "__clean_" in name:
        return "clean_context"
    if "__raw_" in name:
        return "raw_dumps"
    if name.endswith(".json"):
        return "json"

    return "root"

def normalize_title(name: str) -> str:
    for marker in [
        "__analysis_",
        "__prompt_",
        "__CANON_CANDIDATES_",
        "__MEMORY_CANDIDATES_",
        "__TASKS_CANDIDATES_",
        "__clean_",
        "__raw_",
    ]:
        if marker in name:
            return name.split(marker)[0]

    if name in ROOT_AGGREGATES:
        return name.replace(".md", "")

    return Path(name).stem

def collect_files():
    if not BASE.is_dir():
        return []

    files = []
    for path in BASE.rglob("*"):
        if not path.is_file():
            continue
        if path.name in IGNORED_ROOT_FILES:
            continue
        files.append(path)

    files.sort(key=lambda p: (safe_rel(p).lower()))
    return files

def build_records():
    records = []
    for p in collect_files():
        try:
            stat = p.stat()
            mtime = stat.st_mtime
            size = stat.st_size
        except Exception:
            mtime = 0
            size = 0

        category = detect_category(p)
        title = normalize_title(p.name)

        records.append({
            "path": p,
            "rel": safe_rel(p),
            "name": p.name,
            "category": category,
            "title": title,
            "mtime": mtime,
            "size": size,
        })

    return records

def compact_line(idx: int, rec: dict) -> str:
    meta = CATEGORY_META.get(rec["category"], CATEGORY_META["root"])
    label = meta["label"].ljust(8)
    label_colored = color(f"[{label}]", meta["color"])
    title = rec["title"][:38].ljust(38)
    dt = fmt_time(rec["mtime"])
    size = file_size_str(rec["size"]).rjust(6)
    return f"{str(idx).rjust(3)} {label_colored} {title} {color(dt, 'gray')} {color(size, 'dim')}"

def print_header(title: str):
    print(color("=== ARC AI ANGELS — CHAT ANALYSIS READER V2 ===", "bold"))
    print(f"Base map: {BASE}")
    print(color(title, "cyan"))
    print()

def choose_from_records(records, title=""):
    while True:
        clear_screen()
        print_header(title)

        if not records:
            print("Geen bestanden gevonden.")
            print()
            print("0. Terug")
            choice = input("\nKies: ").strip()
            if choice == "0":
                return None
            continue

        for i, rec in enumerate(records, start=1):
            print(compact_line(i, rec))

        print()
        print("  0 Terug")
        print()
        choice = input("Kies een bestandsnummer: ").strip()

        if choice == "0":
            return None
        if choice.isdigit():
            n = int(choice)
            if 1 <= n <= len(records):
                return records[n - 1]

def file_actions(rec: dict):
    path = rec["path"]

    while True:
        clear_screen()
        print_header(f"Bestand: {rec['rel']}")
        print(f"Titel:     {rec['title']}")
        print(f"Categorie: {rec['category']}")
        print(f"Grootte:   {file_size_str(rec['size'])}")
        print(f"Gewijzigd: {fmt_time(rec['mtime'])}")
        print()
        print("1. Lees preview (eerste 40 regels)")
        print("2. Lees preview (eerste 100 regels)")
        print("3. Lees preview (laatste 40 regels)")
        print("4. Lees volledig met less")
        print("5. Open met nano")
        print("6. Zoek woord in bestand")
        print("0. Terug")
        print()

        choice = input("Kies actie: ").strip()

        if choice == "0":
            return
        elif choice == "1":
            clear_screen()
            read_preview(path, "head", 40)
            pause()
        elif choice == "2":
            clear_screen()
            read_preview(path, "head", 100)
            pause()
        elif choice == "3":
            clear_screen()
            read_preview(path, "tail", 40)
            pause()
        elif choice == "4":
            run_pager_for_file(path)
        elif choice == "5":
            run_nano(path)
        elif choice == "6":
            needle = input("Zoekterm: ").strip()
            if needle:
                clear_screen()
                grep_in_file(path, needle)
                pause()

def records_by_category(records, category: str):
    return sorted(
        [r for r in records if r["category"] == category],
        key=lambda r: r["mtime"],
        reverse=True
    )

def newest_in_category(records, category: str):
    items = records_by_category(records, category)
    return items[0] if items else None

def search_titles(records):
    while True:
        clear_screen()
        print_header("Zoek op chat-titel")
        query = input("Voer deel van titel in (of 0 om terug te gaan): ").strip()
        if query == "0":
            return
        if not query:
            continue

        matches = [r for r in records if query.lower() in r["title"].lower()]
        matches.sort(key=lambda r: (r["title"].lower(), -r["mtime"]))

        chosen = choose_from_records(matches, f"Zoekresultaten voor: {query}")
        if chosen:
            file_actions(chosen)

def browse_by_category(records):
    while True:
        clear_screen()
        print_header("Bladeren per categorie")
        cats = []
        for c in CATEGORY_ORDER:
            items = records_by_category(records, c)
            if items:
                cats.append((c, len(items)))

        for i, (cat, count) in enumerate(cats, start=1):
            meta = CATEGORY_META.get(cat, CATEGORY_META["root"])
            label = color(meta["label"], meta["color"])
            print(f"{str(i).rjust(2)}. {label} ({count})")

        print()
        print(" 0. Terug")
        print()

        choice = input("Kies categorie: ").strip()
        if choice == "0":
            return
        if not choice.isdigit():
            continue

        idx = int(choice)
        if not (1 <= idx <= len(cats)):
            continue

        cat = cats[idx - 1][0]
        items = records_by_category(records, cat)
        chosen = choose_from_records(items, f"Categorie: {cat}")
        if chosen:
            file_actions(chosen)

def browse_by_title_cluster(records):
    while True:
        clear_screen()
        print_header("Bladeren per chat-titel")
        groups = {}
        for r in records:
            groups.setdefault(r["title"], []).append(r)

        titles = sorted(groups.keys(), key=lambda x: x.lower())

        for i, title in enumerate(titles, start=1):
            print(f"{str(i).rjust(3)}. {title} {color(f'({len(groups[title])})', 'gray')}")

        print()
        print("  0. Terug")
        print()

        choice = input("Kies titel: ").strip()
        if choice == "0":
            return
        if not choice.isdigit():
            continue

        idx = int(choice)
        if not (1 <= idx <= len(titles)):
            continue

        title = titles[idx - 1]
        items = sorted(groups[title], key=lambda r: (r["category"], -r["mtime"]))
        chosen = choose_from_records(items, f"Bestanden voor titel: {title}")
        if chosen:
            file_actions(chosen)

def show_newest_shortcuts(records):
    mapping = [
        ("Nieuwste analysis", "analysis"),
        ("Nieuwste prompt", "continuation_prompts"),
        ("Nieuwste canon candidate", "canon_candidates"),
        ("Nieuwste memory candidate", "memory_candidates"),
        ("Nieuwste tasks candidate", "tasks_candidates"),
        ("Nieuwste clean context", "clean_context"),
        ("Nieuwste raw dump", "raw_dumps"),
    ]

    while True:
        clear_screen()
        print_header("Nieuwste bestanden per type")

        available = []
        for label, cat in mapping:
            rec = newest_in_category(records, cat)
            if rec:
                available.append((label, cat, rec))

        for i, (label, cat, rec) in enumerate(available, start=1):
            meta = CATEGORY_META.get(cat, CATEGORY_META["root"])
            print(
                f"{str(i).rjust(2)}. "
                f"{color(meta['label'], meta['color']).ljust(18)} "
                f"{rec['title'][:36].ljust(36)} "
                f"{color(fmt_time(rec['mtime']), 'gray')}"
            )

        print()
        print(" 0. Terug")
        print()

        choice = input("Kies item: ").strip()
        if choice == "0":
            return
        if choice.isdigit():
            n = int(choice)
            if 1 <= n <= len(available):
                file_actions(available[n - 1][2])

def compact_overview(records):
    clear_screen()
    print_header("Compact overzicht")

    for cat in CATEGORY_ORDER:
        items = records_by_category(records, cat)
        if not items:
            continue
        meta = CATEGORY_META.get(cat, CATEGORY_META["root"])
        print(color(f"[{meta['label']}]", meta["color"]))
        for rec in items[:10]:
            print(f"  - {rec['title'][:40].ljust(40)} {color(fmt_time(rec['mtime']), 'gray')}")
        if len(items) > 10:
            print(f"  ... nog {len(items) - 10} bestanden")
        print()

    pause()

def main():
    if not BASE.is_dir():
        print(f"Map bestaat niet: {BASE}")
        sys.exit(1)

    while True:
        records = build_records()

        clear_screen()
        print_header("Hoofdmenu")
        print("1. Nieuwste bestanden per type")
        print("2. Zoek op chat-titel")
        print("3. Bladeren per categorie")
        print("4. Bladeren per chat-titel")
        print("5. Compact overzicht")
        print("0. Afsluiten")
        print()

        choice = input("Kies optie: ").strip()

        if choice == "0":
            print("Afgesloten.")
            return
        elif choice == "1":
            show_newest_shortcuts(records)
        elif choice == "2":
            search_titles(records)
        elif choice == "3":
            browse_by_category(records)
        elif choice == "4":
            browse_by_title_cluster(records)
        elif choice == "5":
            compact_overview(records)

if __name__ == "__main__":
    main()
