#!/usr/bin/env python3
from __future__ import print_function

import os
import sys
import shutil
import subprocess
from pathlib import Path

BASE = Path.home() / "arc_ai_angels" / "reports" / "chat_analysis"

COLOR = True if "--color" in sys.argv else False

def c(text, code):
    if not COLOR:
        return text
    return "\033[" + code + "m" + text + "\033[0m"

def clear():
    os.system("clear")

def pause():
    input("\nDruk op Enter om verder te gaan...")

def relpath(p, base):
    try:
        return str(p.relative_to(base))
    except Exception:
        return str(p)

def slug_score(name):
    name = name.lower()
    score = 0
    interesting = [
        "clean", "prompt", "canon", "memory", "tasks",
        "analysis", "raw", "dump", "json"
    ]
    for word in interesting:
        if word in name:
            score += 1
    return score

def list_all_files(base):
    files = []
    if not base.exists():
        return files
    for p in sorted(base.rglob("*")):
        if p.is_file():
            files.append(p)
    return files

def group_files(base):
    groups = {}
    for p in list_all_files(base):
        rel = p.relative_to(base)
        parts = rel.parts
        if len(parts) == 1:
            group = "root"
        else:
            group = parts[0]
        groups.setdefault(group, []).append(p)

    for group in groups:
        groups[group] = sorted(
            groups[group],
            key=lambda x: (slug_score(x.name), x.name.lower())
        )
    return dict(sorted(groups.items(), key=lambda kv: kv[0].lower()))

def show_header(title):
    print(c("=== ARC AI ANGELS — CHAT ANALYSIS READER V2 ===", "1;36"))
    print(c(title, "1;33"))
    print("Base map: {}".format(BASE))
    print("")

def short_name(p, base):
    rp = relpath(p, base)
    if len(rp) > 90:
        return "..." + rp[-87:]
    return rp

def open_with_less(path):
    try:
        subprocess.call(["less", str(path)])
    except KeyboardInterrupt:
        pass

def print_file_in_terminal(path):
    clear()
    show_header("TERMINAL WEERGAVE")
    print(c(relpath(path, BASE), "1;32"))
    print(c("-" * 80, "2"))
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        print("Kon bestand niet lezen: {}".format(e))
        pause()
        return

    print(text)
    print(c("-" * 80, "2"))
    pause()

def preview_file(path, lines=40):
    clear()
    show_header("PREVIEW")
    print(c(relpath(path, BASE), "1;32"))
    print(c("-" * 80, "2"))
    try:
        with path.open("r", encoding="utf-8", errors="replace") as f:
            for i, line in enumerate(f, 1):
                if i > lines:
                    print(c("... preview afgekapt na {} regels ...".format(lines), "33"))
                    break
                print(line.rstrip("\n"))
    except Exception as e:
        print("Kon preview niet laden: {}".format(e))
    print(c("-" * 80, "2"))
    pause()

def file_info(path):
    clear()
    show_header("BESTANDSINFO")
    print(c(relpath(path, BASE), "1;32"))
    print("")
    try:
        st = path.stat()
        print("Grootte: {} bytes".format(st.st_size))
    except Exception as e:
        print("Stat fout: {}".format(e))
    print("Volledig pad: {}".format(path))
    print("")
    pause()

def choose_file_action(path):
    while True:
        clear()
        show_header("BESTAND GEKOZEN")
        print(c(relpath(path, BASE), "1;32"))
        print("")
        print("1. Preview")
        print("2. Lezen met less")
        print("3. In terminal tonen")
        print("4. Bestandsinfo")
        print("0. Terug")
        print("x. Afsluiten")
        print("")

        choice = input("Kies een actie: ").strip().lower()

        if choice == "1":
            preview_file(path)
        elif choice == "2":
            open_with_less(path)
        elif choice == "3":
            print_file_in_terminal(path)
        elif choice == "4":
            file_info(path)
        elif choice == "0":
            return
        elif choice == "x":
            sys.exit(0)
        else:
            print("Ongeldige keuze.")
            pause()

def choose_file_from_group(group_name, files, base):
    while True:
        clear()
        show_header("GROEP: {}".format(group_name))
        print("Aantal bestanden: {}".format(len(files)))
        print("")

        for idx, p in enumerate(files, 1):
            print("{:>3}. {}".format(idx, short_name(p, base)))

        print("")
        print("0. Terug")
        print("x. Afsluiten")
        print("")

        choice = input("Kies een bestand: ").strip().lower()

        if choice == "0":
            return
        if choice == "x":
            sys.exit(0)

        if not choice.isdigit():
            print("Voer een nummer in.")
            pause()
            continue

        idx = int(choice)
        if idx < 1 or idx > len(files):
            print("Nummer buiten bereik.")
            pause()
            continue

        choose_file_action(files[idx - 1])

def group_summary(groups, base):
    clear()
    show_header("OVERZICHT")
    total_files = 0
    total_groups = len(groups)

    print(c("Categorieën:", "1;34"))
    print("")

    for group, files in groups.items():
        total_files += len(files)
        print("- {:<24} {} bestanden".format(group, len(files)))

    print("")
    print(c("Samenvatting:", "1;34"))
    print("- Totaal categorieën: {}".format(total_groups))
    print("- Totaal bestanden: {}".format(total_files))
    print("")
    pause()

def search_files(groups, base):
    while True:
        clear()
        show_header("ZOEKEN")
        print("Zoek op deel van bestandsnaam of pad.")
        print("0 = terug")
        print("x = afsluiten")
        print("")

        query = input("Zoekterm: ").strip().lower()

        if query == "0":
            return
        if query == "x":
            sys.exit(0)
        if not query:
            continue

        results = []
        for group, files in groups.items():
            for p in files:
                rp = relpath(p, base).lower()
                if query in rp:
                    results.append(p)

        clear()
        show_header("ZOEKRESULTATEN")
        print("Zoekterm: {}".format(query))
        print("Aantal resultaten: {}".format(len(results)))
        print("")

        if not results:
            print("Geen resultaten gevonden.")
            print("")
            pause()
            continue

        for idx, p in enumerate(results, 1):
            print("{:>3}. {}".format(idx, short_name(p, base)))

        print("")
        print("0. Terug")
        print("x. Afsluiten")
        print("")

        choice = input("Kies een bestand: ").strip().lower()

        if choice == "0":
            continue
        if choice == "x":
            sys.exit(0)
        if not choice.isdigit():
            print("Voer een nummer in.")
            pause()
            continue

        idx = int(choice)
        if idx < 1 or idx > len(results):
            print("Nummer buiten bereik.")
            pause()
            continue

        choose_file_action(results[idx - 1])

def choose_category(groups, base):
    group_names = list(groups.keys())

    while True:
        clear()
        show_header("CATEGORIEËN")
        print("")

        for idx, group in enumerate(group_names, 1):
            print("{:>3}. {:<24} ({})".format(idx, group, len(groups[group])))

        print("")
        print("s. Zoeken")
        print("o. Overzicht")
        print("r. Herladen")
        print("0. Afsluiten")
        print("x. Afsluiten")
        print("")

        choice = input("Kies een categorie: ").strip().lower()

        if choice in ("0", "x"):
            sys.exit(0)

        if choice == "s":
            search_files(groups, base)
            continue

        if choice == "o":
            group_summary(groups, base)
            continue

        if choice == "r":
            return "reload"

        if not choice.isdigit():
            print("Voer een geldig nummer in.")
            pause()
            continue

        idx = int(choice)
        if idx < 1 or idx > len(group_names):
            print("Nummer buiten bereik.")
            pause()
            continue

        group_name = group_names[idx - 1]
        choose_file_from_group(group_name, groups[group_name], base)

def main():
    while True:
        if not BASE.exists():
            clear()
            show_header("FOUT")
            print("Map bestaat niet: {}".format(BASE))
            print("")
            print("0. Afsluiten")
            print("x. Afsluiten")
            print("")
            choice = input("Keuze: ").strip().lower()
            if choice in ("0", "x", ""):
                return
            continue

        groups = group_files(BASE)
        result = choose_category(groups, BASE)
        if result == "reload":
            continue

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nAfgesloten.")
