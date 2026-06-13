from pathlib import Path
import importlib.util

CFG_PATH = Path("/home/prime/arc_ai_angels/scripts/agent_02_config.py")

spec = importlib.util.spec_from_file_location("agent_02_config", CFG_PATH)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

AGENTS = mod.AGENTS


def bullets(lines):
    return "\n".join(f"- {line}" for line in lines)


def title_name(name):
    return name.capitalize()


def default_identity_bullets(cfg):
    role = cfg["role"]
    layer = cfg["layer"]
    domain = cfg["domain"]
    parent = cfg["parent"]

    if cfg["template_type"] == "custom_omni":
        return [
            f"{title_name(cfg['name'])} is Omni Lead binnen ARC AI ANGELS.",
            f"Stuurt het domein `{domain}` aan.",
            f"Werkt hiërarchisch onder `{parent}`.",
            f"Bewaakt domeincoördinatie, kwaliteit en continuity.",
            "Handelt niet buiten rol of domeingrens.",
        ]

    if cfg["template_type"] == "custom_sentinel":
        return [
            f"{title_name(cfg['name'])} is Sentinel binnen ARC AI ANGELS.",
            f"Werkt specialistisch binnen domein `{domain}`.",
            f"Rapporteert hiërarchisch aan `{parent}`.",
            "Bewaakt continuïteit en traceability binnen eigen scope.",
            "Handelt niet buiten rol of domeingrens.",
        ]

    if cfg["template_type"] == "custom_orchestrator":
        return [
            f"{title_name(cfg['name'])} is de centrale orchestrationlaag van ARC AI ANGELS.",
            f"Werkt binnen domein `{domain}`.",
            f"Ontvangt input van `{parent}`.",
            "Bewaakt routing, volgorde en domeincohesie.",
            "Handelt niet buiten rol of domeingrens.",
        ]

    if cfg["template_type"] == "custom_gateway":
        return [
            f"{title_name(cfg['name'])} is de gateway van ARC AI ANGELS.",
            f"Werkt binnen domein `{domain}`.",
            "Ontvangt en structureert externe input.",
            "Bewaakt duidelijkheid, intake en veilige doorstroom.",
            "Handelt niet buiten rol of domeingrens.",
        ]

    return [
        f"{title_name(cfg['name'])} opereert binnen ARC AI ANGELS als canon-conforme agent.",
        f"Rol is `{role}` binnen domein `{domain}`.",
        f"Parent is `{parent}`.",
        "Werkt hiërarchisch en traceable.",
        "Handelt niet buiten rol of domeingrens.",
    ]


def default_cognitive_style(cfg):
    if cfg["template_type"] == "custom_gateway":
        return ["scherp", "compact", "filterend", "oplossingsgericht", "gestructureerd"]
    if cfg["template_type"] == "custom_orchestrator":
        return ["systemisch", "analytisch", "besluitgericht", "governance-aware", "compact"]
    if cfg["template_type"] == "custom_omni":
        return ["coördinerend", "systematisch", "kwaliteitsgericht", "domeinbewust", "compact"]
    return ["gestructureerd", "doelgericht", "compact", "traceable", "verantwoordelijk"]


def default_decision_logic(cfg):
    if cfg["template_type"] == "custom_gateway":
        return [
            "externe input wordt eerst begrepen en opgeschoond",
            "kleine verzoeken kunnen direct afgehandeld worden",
            "grotere verzoeken worden strak voorbereid",
            "routingbeslissingen liggen niet op gateway-niveau",
            "output moet bruikbaar en canon-conform zijn",
        ]
    if cfg["template_type"] == "custom_orchestrator":
        return [
            "routing loopt via de hiërarchie",
            "minimale activatie heeft de voorkeur",
            "domeinselectie ligt bij de orchestrator",
            "execution ligt niet op orchestration-niveau",
            "traceability en samenhang gaan vóór snelheid",
        ]
    if cfg["template_type"] == "custom_omni":
        return [
            "werk wordt eerst beoordeeld op domeinfit",
            "subtaken worden verdeeld naar de juiste sentinels",
            "cross-domain routing loopt terug via flux",
            "alleen gevalideerde output mag omhoog terug",
            "continuïteit en kwaliteitscontrole gaan vóór snelheid",
        ]
    return [
        "handelt alleen binnen eigen rol en domein",
        "escalatie loopt via de hiërarchie",
        "geen roloverschrijding",
        "continuïteit en traceability gaan vóór snelheid",
        "output moet bruikbaar en canon-conform zijn",
    ]


def default_boundaries(cfg):
    if cfg["template_type"] == "custom_gateway":
        return [
            "geen orchestration",
            "geen domeinrouting",
            "geen selectie van Omni Leads",
            "geen selectie van Sentinels",
            "geen systeemarchitectuur wijzigen zonder opdracht",
        ]
    if cfg["template_type"] == "custom_orchestrator":
        return [
            "geen externe intake",
            "geen specialistische uitvoering",
            "geen ongecontroleerde cross-domain uitvoering",
            "geen Worker-aansturing buiten hiërarchie",
            "geen systeemarchitectuur wijzigen zonder opdracht",
        ]
    if cfg["template_type"] == "custom_omni":
        return [
            "geen externe intake",
            "geen cross-domain routing buiten flux om",
            "geen hiërarchiebypass",
            "geen specialistische uitvoering alsof omni een sentinel is",
            "geen systeemarchitectuur wijzigen zonder opdracht",
        ]
    return [
        "geen externe intake",
        "geen Omni-coördinatie",
        "geen cross-domain routing",
        "geen hiërarchiebypass",
        "geen systeemarchitectuur wijzigen zonder opdracht",
    ]


def default_position(cfg):
    parent = cfg["parent"]
    name = title_name(cfg["name"])

    if parent == "none":
        return f"none → {name}"
    return f"{title_name(parent)} → {name}"


def default_handoff_focus(cfg):
    return [
        f"{title_name(cfg['name'])} functioneert als {cfg['role']} binnen domein `{cfg['domain']}`.",
        "Focus ligt op canon-conforme uitvoering, continuity en consistente taakstructuur.",
    ]


def default_handoff_next(cfg):
    return [
        f"`IDENTITY.md`, `MEMORY.md`, `TASKS.md` en `HANDOFF.md` van {title_name(cfg['name'])} canon-conform houden.",
        "Daarna deze agent als stabiele bouwsteen gebruiken binnen verdere domeinuitrol.",
    ]


def default_handoff_blockers(cfg):
    return [
        "Geen harde blocker.",
        "Verdere verfijning mogelijk zodra volledige domeinset en skills definitief zijn vastgesteld.",
    ]


def default_handoff_resume(cfg):
    return f"Start altijd met `HANDOFF.md`, daarna `TASKS.md`, `MEMORY.md` en pas daarna de bredere context van {title_name(cfg['name'])}."


def default_memory_rules(cfg):
    return [
        "alleen herbruikbare learnings",
        "geen dagelijkse ruis",
        "geen duplicatie van actuele taakstatus",
        "escalatie van scopegrenzen loopt via de hiërarchie",
        "memory blijft compact, bruikbaar en canon-conform",
    ]


def default_memory_learnings(cfg):
    return [
        f"{title_name(cfg['name'])} opereert in laag `{cfg['layer']}`.",
        f"Domein van {cfg['name']} is `{cfg['domain']}`.",
        f"Parent van {cfg['name']} is `{cfg['parent']}`.",
        f"Rol van {cfg['name']} is: {cfg['role']}.",
        f"{title_name(cfg['name'])} werkt binnen afgebakende verantwoordelijkheid en mag niet buiten scope opereren.",
        "Continuïteit, traceability en rolzuiverheid zijn leidend.",
    ]


def default_task(cfg):
    name_up = cfg["name"].upper()
    return {
        "task_id": f"{name_up}-HARDENING-001",
        "project_id": "AUTONOMY-FOUNDATION-001",
        "origin": cfg["parent"] if cfg["parent"] != "none" else "system",
        "title": f"{title_name(cfg['name'])} normaliseren als canon-conforme agent",
        "summary": f"{title_name(cfg['name'])} structureren zodat identity, handoff, memory en taakdiscipline consistent, bruikbaar en herhaalbaar zijn binnen ARC AI ANGELS.",
        "priority": "HIGH",
        "project_priority": "HIGH",
        "effort_size": "S",
        "queue_group": "FOUNDATION",
        "blocking_impact": "true",
        "status": "IN_PROGRESS",
        "owner_layer": cfg["layer"],
        "owner_agent": cfg["name"],
        "assigned_by": cfg["parent"] if cfg["parent"] != "none" else "system",
        "assigned_to": cfg["name"],
        "domain": cfg["domain"],
        "sentinel": "n.v.t.",
        "depends_on": "canon alignment",
        "created_at": "2026-04-20",
        "updated_at": "2026-04-20",
        "started_at": "2026-04-20",
        "expected_end_at": "onbekend",
        "feasibility_check": "uitvoerbaar",
        "blocked_reason": "geen",
        "next_step": f"{title_name(cfg['name'])} definitief vastzetten als consistente agent binnen de huidige ARC-structuur.",
        "trace_link": "CANON.md / agents/*",
        "result_summary": "",
        "completion_validated_by": "",
        "notes": [
            f"{title_name(cfg['name'])} werkt binnen laag `{cfg['layer']}`.",
            f"{title_name(cfg['name'])} valt onder `{cfg['parent']}`." if cfg["parent"] != "none" else f"{title_name(cfg['name'])} staat bovenaan zijn eigen laag.",
            "Deze agent moet canon-conform, traceable en herbruikbaar blijven.",
        ],
    }


def fill_defaults(cfg):
    cfg = dict(cfg)
    cfg.setdefault("identity_bullets", default_identity_bullets(cfg))
    cfg.setdefault("cognitive_style", default_cognitive_style(cfg))
    cfg.setdefault("decision_logic", default_decision_logic(cfg))
    cfg.setdefault("boundaries", default_boundaries(cfg))
    cfg.setdefault("position", default_position(cfg))
    cfg.setdefault("handoff_focus", default_handoff_focus(cfg))
    cfg.setdefault("handoff_next", default_handoff_next(cfg))
    cfg.setdefault("handoff_blockers", default_handoff_blockers(cfg))
    cfg.setdefault("handoff_resume", default_handoff_resume(cfg))
    cfg.setdefault("memory_rules", default_memory_rules(cfg))
    cfg.setdefault("memory_learnings", default_memory_learnings(cfg))
    cfg.setdefault("task", default_task(cfg))
    return cfg


def render_identity(cfg):
    return f"""# IDENTITY — {cfg['name']}

## Layer
{cfg['layer']}

## Domain
{cfg['domain']}

## Parent
{cfg['parent']}

## Role
{cfg['role']}

## Mission
{cfg['mission']}

## Core Identity
{bullets(cfg['identity_bullets'])}

## Cognitive Style
{bullets(cfg['cognitive_style'])}

## Decision Logic
{bullets(cfg['decision_logic'])}

## Boundaries
{bullets(cfg['boundaries'])}

## Position
{cfg['position']}
""".strip() + "\n"


def render_handoff(cfg):
    return f"""# HANDOFF — {cfg['name']}

## Current Focus
{bullets(cfg['handoff_focus'])}

## Next Action
{bullets(cfg['handoff_next'])}

## Blockers
{bullets(cfg['handoff_blockers'])}

## Resume Point
- {cfg['handoff_resume']}
""".strip() + "\n"


def render_memory(cfg):
    return f"""# MEMORY — {cfg['name']}

## Structure Rules
{bullets(cfg['memory_rules'])}

## Learnings
{bullets(cfg['memory_learnings'])}
""".strip() + "\n"


def render_tasks(cfg):
    t = cfg["task"]
    notes = "\n".join(f"- {n}" for n in t["notes"])
    return f"""# TASKS.md — {cfg['name']}

## Active Tasks

### Task: {t['task_id']}
- Task ID: {t['task_id']}
- Project ID: {t['project_id']}
- Origin: {t['origin']}
- Title: {t['title']}
- Summary: {t['summary']}
- Priority: {t['priority']}
- Project Priority: {t['project_priority']}
- Effort Size: {t['effort_size']}
- Queue Group: {t['queue_group']}
- Blocking Impact: {t['blocking_impact']}
- Status: {t['status']}
- Owner Layer: {t['owner_layer']}
- Owner Agent: {t['owner_agent']}
- Assigned By: {t['assigned_by']}
- Assigned To: {t['assigned_to']}
- Domain: {t['domain']}
- Sentinel: {t['sentinel']}
- Depends On: {t['depends_on']}
- Created At: {t['created_at']}
- Updated At: {t['updated_at']}
- Started At: {t['started_at']}
- Expected End At: {t['expected_end_at']}
- Feasibility Check: {t['feasibility_check']}
- Blocked Reason: {t['blocked_reason']}
- Next Step: {t['next_step']}
- Trace Link: {t['trace_link']}
- Result Summary: {t['result_summary']}
- Completion Validated By: {t['completion_validated_by']}

## Notes
{notes}
""".strip() + "\n"


def check_file(path, expected):
    if not path.exists():
        return False, "missing"
    actual = path.read_text(encoding="utf-8")
    if actual != expected:
        return False, "content mismatch"
    return True, "ok"


def main():
    print("\n=== VALIDATION START ===\n")
    print(f"USING CONFIG: {CFG_PATH}\n")

    for name, raw_cfg in AGENTS.items():
        cfg = fill_defaults(raw_cfg)
        path = Path(cfg["path"])

        print(f"--- {name.upper()} ---")

        checks = {
            "IDENTITY.md": render_identity(cfg),
            "HANDOFF.md": render_handoff(cfg),
            "MEMORY.md": render_memory(cfg),
            "TASKS.md": render_tasks(cfg),
        }

        for filename, expected in checks.items():
            ok, reason = check_file(path / filename, expected)
            if ok:
                print(f"[OK] {filename}")
            else:
                print(f"[FAIL] {filename} {reason}")

        print()

    print("=== VALIDATION DONE ===")


if __name__ == "__main__":
    main()

