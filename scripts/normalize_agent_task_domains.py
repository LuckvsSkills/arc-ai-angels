chmod +x ~/arc_ai_angels/scripts/normalize_agent_task_domains.py
#!/usr/bin/env python3
"""
normalize_agent_task_domains.py

Doel:
- Scan ARC AI ANGELS agent TASKS.md files
- Leid canonieke Domain labels af uit de echte filesystem-structuur
- Herstel fout gebruik van omni domeinnamen als agentnamen
- Maak backups
- Schrijf een rapport met wat aangepast is

Canon:
- Flux:    system/orchestration/core/flux
- Nova:    gateway/intake/core/nova
- Omni:    <domain>/<function>/lead/<agent>
- Sentinel:<domain>/<function>/<specialism>/<agent>

Gebruik:
    python3 normalize_agent_task_domains.py
    python3 normalize_agent_task_domains.py --dry-run
    python3 normalize_agent_task_domains.py --root ~/arc_ai_angels

Let op:
- Dit script past alleen TASKS.md files aan
- Het wijzigt geen CANON.md, HANDOFF.md of MEMORY.md
"""

from __future__ import annotations

import argparse
import re
import shutil
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple


OMNI_FUNCTIONS: Dict[str, str] = {
    "helix": "tech",
    "matrix": "intelligence",
    "quantix": "growth",
    "zenix": "operations",
    "finix": "assets",
}

SENTINEL_SPECIALISMS: Dict[str, Dict[str, str]] = {
    "helix": {
        "axon": "automation",
        "clio": "documentation",
        "forge": "engineering",
        "nero": "security",
        "ventura": "infrastructure",
    },
    "matrix": {
        "arix": "analysis",
        "daxio": "strategy",
        "enki": "knowledge",
        "sora": "research",
        "tharos": "planning",
    },
    "quantix": {
        "elora": "analytics",
        "kresta": "optimization",
        "luvia": "insights",
        "nura": "modeling",
        "vondra": "forecasting",
    },
    "zenix": {
        "draven": "execution",
        "orizon": "coordination",
        "solis": "monitoring",
        "unia": "support",
        "zena": "control",
    },
    "finix": {
        "kairo": "risk",
        "kenzo": "valuation",
        "odis": "flow",
        "vector": "transactions",
        "zion": "portfolio",
    },
}

CORE_DOMAIN_BY_AGENT: Dict[str, str] = {
    "flux": "system/orchestration/core/flux",
    "nova": "gateway/intake/core/nova",
}


@dataclass
class TaskFileContext:
    path: Path
    agent_name: Optional[str]
    canonical_domain: Optional[str]
    canonical_owner_agent: Optional[str]
    canonical_assigned_to: Optional[str]
    role_type: str  # core | omni_lead | sentinel | unknown


@dataclass
class FileChange:
    path: Path
    changed: bool
    backup_path: Optional[Path]
    notes: List[str]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--root",
        default=str(Path.home() / "arc_ai_angels"),
        help="Root van arc_ai_angels",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Laat zien wat aangepast zou worden zonder te schrijven",
    )
    return parser.parse_args()


def now_stamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def infer_context(task_file: Path, root: Path) -> TaskFileContext:
    rel = task_file.relative_to(root)
    parts = rel.parts

    # Core agents
    if len(parts) >= 3 and parts[0] == "agents" and parts[1] in CORE_DOMAIN_BY_AGENT and parts[-1] == "TASKS.md":
        agent = parts[1]
        return TaskFileContext(
            path=task_file,
            agent_name=agent,
            canonical_domain=CORE_DOMAIN_BY_AGENT[agent],
            canonical_owner_agent=agent,
            canonical_assigned_to=agent,
            role_type="core",
        )

    # Omni lead:
    # agents/omni/helix/lead agent cortexia/TASKS.md
    if (
        len(parts) >= 5
        and parts[0] == "agents"
        and parts[1] == "omni"
        and parts[2] in OMNI_FUNCTIONS
        and parts[3].startswith("lead agent ")
        and parts[-1] == "TASKS.md"
    ):
        domain = parts[2]
        function = OMNI_FUNCTIONS[domain]
        lead_name = parts[3].replace("lead agent ", "").strip().lower()

        return TaskFileContext(
            path=task_file,
            agent_name=lead_name,
            canonical_domain=f"{domain}/{function}/lead/{lead_name}",
            canonical_owner_agent=lead_name,
            canonical_assigned_to=lead_name,
            role_type="omni_lead",
        )

    # Sentinel:
    # agents/omni/helix/sentinels/nero/TASKS.md
    if (
        len(parts) >= 6
        and parts[0] == "agents"
        and parts[1] == "omni"
        and parts[2] in OMNI_FUNCTIONS
        and parts[3] == "sentinels"
        and parts[-1] == "TASKS.md"
    ):
        domain = parts[2]
        sentinel = parts[4].lower()
        function = OMNI_FUNCTIONS[domain]
        specialism = SENTINEL_SPECIALISMS.get(domain, {}).get(sentinel, "specialism")

        return TaskFileContext(
            path=task_file,
            agent_name=sentinel,
            canonical_domain=f"{domain}/{function}/{specialism}/{sentinel}",
            canonical_owner_agent=sentinel,
            canonical_assigned_to=sentinel,
            role_type="sentinel",
        )

    return TaskFileContext(
        path=task_file,
        agent_name=None,
        canonical_domain=None,
        canonical_owner_agent=None,
        canonical_assigned_to=None,
        role_type="unknown",
    )


def replace_first_line_value(text: str, field: str, new_value: str) -> Tuple[str, bool]:
    pattern = re.compile(rf"(^-\s*{re.escape(field)}:\s*)(.*)$", re.MULTILINE)
    match = pattern.search(text)
    if not match:
        return text, False

    old_value = match.group(2).strip()
    if old_value == new_value:
        return text, False

    new_text = pattern.sub(rf"\1{new_value}", text, count=1)
    return new_text, True


def replace_all_field_values(text: str, field: str, old_values: List[str], new_value: str) -> Tuple[str, int]:
    count = 0
    lines = text.splitlines()
    out: List[str] = []

    normalized_old = {v.lower() for v in old_values}

    prefix = f"- {field}:"
    for line in lines:
        if line.strip().startswith(prefix):
            current = line.split(":", 1)[1].strip()
            if current.lower() in normalized_old and current != new_value:
                out.append(f"- {field}: {new_value}")
                count += 1
                continue
        out.append(line)

    return "\n".join(out) + ("\n" if text.endswith("\n") else ""), count


def ensure_domain_line(text: str, canonical_domain: str) -> Tuple[str, bool]:
    if re.search(r"^-\s*Domain:\s*", text, flags=re.MULTILINE):
        return replace_first_line_value(text, "Domain", canonical_domain)

    # voeg Domain toe na Assigned To als mogelijk
    lines = text.splitlines()
    out: List[str] = []
    inserted = False

    for line in lines:
        out.append(line)
        if re.match(r"^-\s*Assigned To:\s*", line) and not inserted:
            out.append(f"- Domain: {canonical_domain}")
            inserted = True

    if not inserted:
        out.append(f"- Domain: {canonical_domain}")

    return "\n".join(out) + ("\n" if text.endswith("\n") else ""), True


def backup_file(path: Path, backup_root: Path) -> Path:
    backup_root.mkdir(parents=True, exist_ok=True)
    backup_path = backup_root / f"{path.parent.name}_{path.name}.bak"
    shutil.copy2(path, backup_path)
    return backup_path


def normalize_task_file(task_file: Path, context: TaskFileContext, backup_root: Path, dry_run: bool) -> FileChange:
    notes: List[str] = []
    original = task_file.read_text(encoding="utf-8")
    updated = original

    if context.role_type == "unknown" or not context.canonical_domain:
        return FileChange(path=task_file, changed=False, backup_path=None, notes=["SKIPPED: unknown role/path"])

    # Domain fix
    updated, changed_domain = ensure_domain_line(updated, context.canonical_domain)
    if changed_domain:
        notes.append(f"Domain -> {context.canonical_domain}")

    # Owner Agent fix for lead/core/sentinel task files
    if context.canonical_owner_agent:
        updated, changed_owner = replace_first_line_value(updated, "Owner Agent", context.canonical_owner_agent)
        if changed_owner:
            notes.append(f"Owner Agent -> {context.canonical_owner_agent}")

    # Assigned To fix
    if context.canonical_assigned_to:
        updated, changed_assigned_to = replace_first_line_value(updated, "Assigned To", context.canonical_assigned_to)
        if changed_assigned_to:
            notes.append(f"Assigned To -> {context.canonical_assigned_to}")

    # Replace bad omni-as-agent usage inside relevant fields
    omni_names = list(OMNI_FUNCTIONS.keys())

    if context.role_type == "omni_lead" and context.agent_name:
        # example: Owner Agent: helix -> cortexia
        for field in ("Owner Agent", "Assigned To"):
            updated, count = replace_all_field_values(updated, field, omni_names, context.agent_name)
            if count:
                notes.append(f"{field}: replaced omni-id with lead name ({count}x)")

    if context.role_type == "sentinel":
        # example: Origin: helix / Assigned By: helix should become cortexia for this domain
        domain = context.canonical_domain.split("/", 1)[0]
        lead_map = {
            "helix": "cortexia",
            "matrix": "saelia",
            "quantix": "lumeria",
            "zenix": "fluentia",
            "finix": "finoria",
        }
        correct_lead = lead_map.get(domain)
        if correct_lead:
            for field in ("Origin", "Assigned By"):
                updated, count = replace_all_field_values(updated, field, [domain], correct_lead)
                if count:
                    notes.append(f"{field}: replaced {domain} -> {correct_lead} ({count}x)")

            updated, changed_assigned_to = replace_first_line_value(updated, "Assigned To", context.agent_name)
            if changed_assigned_to:
                notes.append(f"Assigned To -> {context.agent_name}")

            updated, changed_owner = replace_first_line_value(updated, "Owner Agent", context.agent_name)
            if changed_owner:
                notes.append(f"Owner Agent -> {context.agent_name}")

    changed = updated != original
    backup_path: Optional[Path] = None

    if changed and not dry_run:
        backup_path = backup_file(task_file, backup_root)
        task_file.write_text(updated, encoding="utf-8")

    return FileChange(path=task_file, changed=changed, backup_path=backup_path, notes=notes)


def write_report(report_path: Path, changes: List[FileChange], dry_run: bool) -> None:
    lines: List[str] = []
    lines.append("# TASK DOMAIN NORMALIZATION REPORT")
    lines.append("")
    lines.append(f"- Timestamp: {datetime.now().isoformat(timespec='seconds')}")
    lines.append(f"- Mode: {'DRY RUN' if dry_run else 'WRITE'}")
    lines.append("")

    total = len(changes)
    changed = sum(1 for c in changes if c.changed)
    skipped = sum(1 for c in changes if not c.changed and any("SKIPPED" in n for n in c.notes))
    unchanged = total - changed - skipped

    lines.append("## Summary")
    lines.append(f"- Total TASKS.md files scanned: {total}")
    lines.append(f"- Changed: {changed}")
    lines.append(f"- Unchanged: {unchanged}")
    lines.append(f"- Skipped: {skipped}")
    lines.append("")

    lines.append("## Details")
    for change in changes:
        lines.append(f"### {change.path}")
        lines.append(f"- Changed: {'yes' if change.changed else 'no'}")
        if change.backup_path:
            lines.append(f"- Backup: {change.backup_path}")
        if change.notes:
            for note in change.notes:
                lines.append(f"- {note}")
        else:
            lines.append("- No modifications needed")
        lines.append("")

    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    args = parse_args()
    root = Path(args.root).expanduser().resolve()

    agents_root = root / "agents"
    if not agents_root.exists():
        print(f"ERROR: agents root not found: {agents_root}")
        return 1

    task_files = sorted(agents_root.rglob("TASKS.md"))

    backup_root = root / "backups" / f"task_domain_normalization_{now_stamp()}"
    report_path = root / "reports" / f"task_domain_normalization_{now_stamp()}.md"

    changes: List[FileChange] = []

    for task_file in task_files:
        context = infer_context(task_file, root)
        change = normalize_task_file(task_file, context, backup_root, args.dry_run)
        changes.append(change)

    write_report(report_path, changes, args.dry_run)

    print("Done.")
    print(f"Scanned: {len(changes)} TASKS.md files")
    print(f"Changed: {sum(1 for c in changes if c.changed)}")
    print(f"Report : {report_path}")
    if not args.dry_run:
        print(f"Backups: {backup_root}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
