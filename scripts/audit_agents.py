#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import re
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List, Optional

REPO = Path.home() / "arc_ai_angels"
AGENTS_ROOT = REPO / "agents"

CANON = {
    "helix": {
        "lead": "cortexia",
        "sentinels": {
            "nero": "security",
            "forge": "engineering",
            "ventura": "infrastructure",
            "axon": "automation",
            "clio": "documentation",
        },
        "domain2": "tech",
    },
    "matrix": {
        "lead": "saelia",
        "sentinels": {
            "sora": "research",
            "daxio": "data-analysis",
            "enki": "strategy",
            "tharos": "knowledge-systems",
            "arix": "action",
        },
        "domain2": "intelligence",
    },
    "quantix": {
        "lead": "lumeria",
        "sentinels": {
            "vondra": "marketing",
            "nura": "content",
            "elora": "seo",
            "luvia": "affiliate",
            "kresta": "audience-growth",
        },
        "domain2": "growth",
    },
    "zenix": {
        "lead": "fluentia",
        "sentinels": {
            "solis": "workflow",
            "orizon": "process-systems",
            "zena": "project-coordination",
            "unia": "monitoring",
            "draven": "execution",
        },
        "domain2": "operations",
    },
    "finix": {
        "lead": "finoria",
        "sentinels": {
            "vector": "trading",
            "zion": "crypto",
            "odis": "real-estate",
            "kenzo": "portfolio",
            "kairo": "risk",
        },
        "domain2": "assets",
    },
}

CORE_AGENTS = {"nova", "flux", "flux_core", "main"}
NON_CANON_ROOTS = {"standalone", "workers"}

KERNFILES = ["IDENTITY.md", "TASKS.md", "MEMORY.md", "HANDOFF.md"]


@dataclass
class AgentAudit:
    agent: str
    layer: str
    domain_root: str
    path: str
    is_canon: bool
    missing_files: List[str]
    has_identity: bool
    has_tasks: bool
    has_memory: bool
    has_handoff: bool
    identity_role_present: bool
    identity_mission_present: bool
    identity_parent_or_position_present: bool
    identity_format_variant: bool
    task_has_active_real_content: bool
    task_is_stub: bool
    task_domain_found: Optional[str]
    task_domain_expected: Optional[str]
    task_domain_match: Optional[bool]
    memory_has_real_learnings: bool
    journal_dir_exists: bool
    maturity: str
    flags: List[str]


def slug(text: str) -> str:
    return text.strip().lower().replace("_", "-").replace(" ", "-")


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return ""


def detect_identity_signals(text: str) -> tuple[bool, bool, bool, bool]:
    role_present = bool(re.search(r"^##\s*Role\b", text, re.M))
    mission_present = bool(re.search(r"^##\s*Mission\b", text, re.M))
    parent_or_position = bool(
        re.search(r"^##\s*Parent\b", text, re.M) or re.search(r"^##\s*Position\b", text, re.M)
    )
    # Variant if it uses Layer/Domain/Parent style or misses the more common live pattern
    variant = bool(re.search(r"^##\s*Layer\b", text, re.M) or re.search(r"^##\s*Boundaries\b", text, re.M))
    return role_present, mission_present, parent_or_position, variant


def parse_task_domain(text: str) -> Optional[str]:
    m = re.search(r"^-?\s*Domain:\s*(.+?)\s*$", text, re.M)
    if not m:
        return None
    return m.group(1).strip()


def task_is_stub(text: str) -> bool:
    markers = [
        "<TASK_ID>",
        "- Task ID:",
        "- Title:",
        "- Summary:",
        "- Priority:",
        "- Status:",
    ]
    return "<TASK_ID>" in text or all(marker in text for marker in markers)


def task_has_real_content(text: str) -> bool:
    if task_is_stub(text):
        return False
    return bool(re.search(r"^###\s*Task:\s*(?!<TASK_ID>).*", text, re.M))


def memory_has_real_learnings(text: str) -> bool:
    if not text.strip():
        return False
    # anything after "## Learnings" besides whitespace
    m = re.search(r"^##\s*Learnings\s*$([\s\S]*)", text, re.M)
    if not m:
        return False
    tail = m.group(1).strip()
    if not tail:
        return False
    # ignore only bare bullets/placeholders
    if tail in {"-", "*"}:
        return False
    return True


def detect_position_sibling_drift(text: str, domain: str, agent: str) -> bool:
    m = re.search(r"^##\s*Position\s*$\s*([^\n]+)", text, re.M)
    if not m:
        return False
    pos = m.group(1)
    # Sentinel pointing to sibling sentinels rather than workers/execution
    sibs = set(CANON.get(domain, {}).get("sentinels", {}).keys()) - {agent}
    return any(re.search(rf"\b{re.escape(sib)}\b", pos, re.I) for sib in sibs)


def expected_task_domain(layer: str, domain: str, agent: str) -> Optional[str]:
    if domain not in CANON:
        return None
    dom2 = CANON[domain]["domain2"]
    if layer == "Omni Lead":
        lead = CANON[domain]["lead"]
        return f"{domain}/{dom2}/lead/{lead}"
    if layer == "Sentinel":
        spec = CANON[domain]["sentinels"].get(agent)
        if spec:
            return f"{domain}/{dom2}/{spec}/{agent}"
    return None


def classify_maturity(has_identity: bool, role_ok: bool, mission_ok: bool,
                      tasks_real: bool, memory_real: bool) -> str:
    if has_identity and role_ok and mission_ok and tasks_real and memory_real:
        return "Operational"
    if has_identity and (role_ok or mission_ok):
        return "Partial"
    return "Stub"


def build_agent_records() -> List[AgentAudit]:
    records: List[AgentAudit] = []

    # Core agents
    for core in CORE_AGENTS:
        path = AGENTS_ROOT / core
        if not path.exists():
            records.append(AgentAudit(
                agent=core, layer="Core", domain_root="core", path=str(path),
                is_canon=True, missing_files=KERNFILES.copy(),
                has_identity=False, has_tasks=False, has_memory=False, has_handoff=False,
                identity_role_present=False, identity_mission_present=False,
                identity_parent_or_position_present=False, identity_format_variant=False,
                task_has_active_real_content=False, task_is_stub=False,
                task_domain_found=None, task_domain_expected=None, task_domain_match=None,
                memory_has_real_learnings=False, journal_dir_exists=False,
                maturity="Stub", flags=["MISSING_AGENT_DIR"]
            ))
            continue

        # Core files may live in workspace for some agents
        direct_identity = path / "IDENTITY.md"
        workspace_identity = path / "workspace" / "IDENTITY.md"
        identity_path = direct_identity if direct_identity.exists() else workspace_identity

        direct_tasks = path / "TASKS.md"
        workspace_tasks = path / "workspace" / "TASKS.md"
        tasks_path = direct_tasks if direct_tasks.exists() else workspace_tasks

        direct_memory = path / "MEMORY.md"
        workspace_memory = path / "workspace" / "MEMORY.md"
        memory_path = direct_memory if direct_memory.exists() else workspace_memory

        direct_handoff = path / "HANDOFF.md"
        workspace_handoff = path / "workspace" / "HANDOFF.md"
        handoff_path = direct_handoff if direct_handoff.exists() else workspace_handoff

        journal_exists = (path / "JOURNAL").exists() or (path / "workspace" / "JOURNAL").exists()

        missing = []
        for label, p in {
            "IDENTITY.md": identity_path,
            "TASKS.md": tasks_path,
            "MEMORY.md": memory_path,
            "HANDOFF.md": handoff_path,
        }.items():
            if not p.exists():
                missing.append(label)

        identity_text = read_text(identity_path) if identity_path.exists() else ""
        tasks_text = read_text(tasks_path) if tasks_path.exists() else ""
        memory_text = read_text(memory_path) if memory_path.exists() else ""

        role_ok, mission_ok, parent_pos_ok, variant = detect_identity_signals(identity_text)
        tdomain = parse_task_domain(tasks_text)
        tstub = task_is_stub(tasks_text) if tasks_text else False
        treal = task_has_real_content(tasks_text) if tasks_text else False
        mreal = memory_has_real_learnings(memory_text) if memory_text else False

        flags = []
        if variant:
            flags.append("IDENTITY_FORMAT_VARIANT")
        if (path / "legacy_persona_20260412-200254").exists() or (path / "legacy_persona_20260412-200253").exists():
            flags.append("LEGACY_DIR_PRESENT")

        maturity = classify_maturity(identity_path.exists(), role_ok, mission_ok, treal, mreal)

        records.append(AgentAudit(
            agent=core, layer="Core", domain_root="core", path=str(path),
            is_canon=True, missing_files=missing,
            has_identity=identity_path.exists(), has_tasks=tasks_path.exists(),
            has_memory=memory_path.exists(), has_handoff=handoff_path.exists(),
            identity_role_present=role_ok, identity_mission_present=mission_ok,
            identity_parent_or_position_present=parent_pos_ok, identity_format_variant=variant,
            task_has_active_real_content=treal, task_is_stub=tstub,
            task_domain_found=tdomain, task_domain_expected=None, task_domain_match=None,
            memory_has_real_learnings=mreal, journal_dir_exists=journal_exists,
            maturity=maturity, flags=flags
        ))

    # Omni leads + sentinels
    for domain, conf in CANON.items():
        lead_name = conf["lead"]
        lead_dir = AGENTS_ROOT / "omni" / domain / f"lead agent {lead_name}"
        records.append(audit_dir(lead_dir, lead_name, "Omni Lead", domain))

        for sentinel in conf["sentinels"]:
            sdir = AGENTS_ROOT / "omni" / domain / "sentinels" / sentinel
            records.append(audit_dir(sdir, sentinel, "Sentinel", domain))

    # Non-canon roots
    for root in NON_CANON_ROOTS:
        rdir = AGENTS_ROOT / root
        if rdir.exists():
            for child in sorted([p for p in rdir.iterdir() if p.is_dir()]):
                records.append(AgentAudit(
                    agent=child.name, layer="Non-Canon", domain_root=root, path=str(child),
                    is_canon=False, missing_files=[],
                    has_identity=(child / "IDENTITY.md").exists(),
                    has_tasks=(child / "TASKS.md").exists(),
                    has_memory=(child / "MEMORY.md").exists(),
                    has_handoff=(child / "HANDOFF.md").exists(),
                    identity_role_present=False, identity_mission_present=False,
                    identity_parent_or_position_present=False, identity_format_variant=False,
                    task_has_active_real_content=False, task_is_stub=False,
                    task_domain_found=None, task_domain_expected=None, task_domain_match=None,
                    memory_has_real_learnings=False, journal_dir_exists=(child / "JOURNAL").exists(),
                    maturity="Non-Canon", flags=[f"NON_CANON_{root.upper()}"]
                ))
    return records


def audit_dir(path: Path, agent: str, layer: str, domain: str) -> AgentAudit:
    identity = path / "IDENTITY.md"
    tasks = path / "TASKS.md"
    memory = path / "MEMORY.md"
    handoff = path / "HANDOFF.md"
    journal = path / "JOURNAL"

    missing = [name for name, p in {
        "IDENTITY.md": identity,
        "TASKS.md": tasks,
        "MEMORY.md": memory,
        "HANDOFF.md": handoff,
    }.items() if not p.exists()]

    identity_text = read_text(identity)
    tasks_text = read_text(tasks)
    memory_text = read_text(memory)

    role_ok, mission_ok, parent_pos_ok, variant = detect_identity_signals(identity_text)
    tdomain = parse_task_domain(tasks_text)
    expected = expected_task_domain(layer, domain, agent)

    # normalize for comparison
    match = None
    if expected and tdomain:
        match = slug(tdomain) == slug(expected)

    tstub = task_is_stub(tasks_text) if tasks.exists() else False
    treal = task_has_real_content(tasks_text) if tasks.exists() else False
    mreal = memory_has_real_learnings(memory_text) if memory.exists() else False

    flags: List[str] = []
    if variant:
        flags.append("IDENTITY_FORMAT_VARIANT")
    if detect_position_sibling_drift(identity_text, domain, agent):
        flags.append("POSITION_SIBLING_DRIFT")
    if tasks.exists() and tstub:
        flags.append("TASK_STUB")
    if tasks.exists() and expected and tdomain and not match:
        flags.append("TASK_DOMAIN_MISMATCH")
    if memory.exists() and not mreal:
        flags.append("MEMORY_EMPTY_OR_TEMPLATE")
    if not journal.exists():
        flags.append("JOURNAL_DIR_MISSING")

    maturity = classify_maturity(identity.exists(), role_ok, mission_ok, treal, mreal)

    return AgentAudit(
        agent=agent,
        layer=layer,
        domain_root=domain,
        path=str(path),
        is_canon=True,
        missing_files=missing,
        has_identity=identity.exists(),
        has_tasks=tasks.exists(),
        has_memory=memory.exists(),
        has_handoff=handoff.exists(),
        identity_role_present=role_ok,
        identity_mission_present=mission_ok,
        identity_parent_or_position_present=parent_pos_ok,
        identity_format_variant=variant,
        task_has_active_real_content=treal,
        task_is_stub=tstub,
        task_domain_found=tdomain,
        task_domain_expected=expected,
        task_domain_match=match,
        memory_has_real_learnings=mreal,
        journal_dir_exists=journal.exists(),
        maturity=maturity,
        flags=flags
    )


def write_outputs(records: List[AgentAudit], outdir: Path) -> None:
    outdir.mkdir(parents=True, exist_ok=True)

    json_path = outdir / "agent_audit.json"
    csv_path = outdir / "agent_audit.csv"
    summary_path = outdir / "agent_audit_summary.md"

    json_path.write_text(
        json.dumps([asdict(r) for r in records], indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(asdict(records[0]).keys()))
        writer.writeheader()
        for r in records:
            row = asdict(r)
            row["missing_files"] = ";".join(row["missing_files"])
            row["flags"] = ";".join(row["flags"])
            writer.writerow(row)

    operational = [r for r in records if r.maturity == "Operational"]
    partial = [r for r in records if r.maturity == "Partial"]
    stub = [r for r in records if r.maturity == "Stub"]
    noncanon = [r for r in records if r.maturity == "Non-Canon"]

    lines = [
        "# Agent Audit Summary",
        "",
        f"- Total records: {len(records)}",
        f"- Operational: {len(operational)}",
        f"- Partial: {len(partial)}",
        f"- Stub: {len(stub)}",
        f"- Non-Canon: {len(noncanon)}",
        "",
        "## High-signal issues",
        "",
    ]

    for r in records:
        if r.flags:
            lines.append(f"- **{r.agent}** ({r.layer}, {r.domain_root}): {', '.join(r.flags)}")

    lines.extend([
        "",
        "## Suggested immediate fixes",
        "",
        "- Fix all `TASK_DOMAIN_MISMATCH` first.",
        "- Fix all `POSITION_SIBLING_DRIFT` next.",
        "- Normalize all `IDENTITY_FORMAT_VARIANT` files.",
        "- Then upgrade `TASK_STUB` + `MEMORY_EMPTY_OR_TEMPLATE` agents from Partial/Stub to Operational.",
        "",
    ])

    summary_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    if not REPO.exists():
        raise SystemExit(f"Repo not found: {REPO}")

    records = build_agent_records()
    outdir = REPO / "reports" / "agent_audit_live"
    write_outputs(records, outdir)

    print(f"Audit complete. Outputs written to: {outdir}")
    print(f"JSON:    {outdir / 'agent_audit.json'}")
    print(f"CSV:     {outdir / 'agent_audit.csv'}")
    print(f"Summary: {outdir / 'agent_audit_summary.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

