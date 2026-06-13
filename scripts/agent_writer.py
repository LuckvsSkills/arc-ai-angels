from pathlib import Path
from datetime import datetime
import shutil

from agent_config import AGENTS, PROTECTED_TEMPLATE_TYPES

TARGET_FILES = ["IDENTITY.md", "HANDOFF.md", "MEMORY.md", "TASKS.md"]


def bullets(lines):
    return "\n".join(f"- {line}" for line in lines)


def backup_file(path: Path):
    if path.exists():
        ts = datetime.now().strftime("%Y%m%d-%H%M%S")
        backup = path.with_name(f"{path.name}.bak.{ts}")
        shutil.copy2(path, backup)


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
"""


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
"""


def render_memory(cfg):
    return f"""# MEMORY — {cfg['name']}

## Structure Rules
{bullets(cfg['memory_rules'])}

## Learnings
{bullets(cfg['memory_learnings'])}
"""


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
"""


def validate_protected_template(name, cfg):
    expected = PROTECTED_TEMPLATE_TYPES.get(name)
    if expected and cfg["template_type"] != expected:
        raise ValueError(
            f"{name} must use template_type={expected}, got {cfg['template_type']}"
        )


def write_agent(cfg):
    path = Path(cfg["path"])
    if not path.exists():
        print(f"SKIPPED: {cfg['name']} (path not found)")
        return

    contents = {
        "IDENTITY.md": render_identity(cfg),
        "HANDOFF.md": render_handoff(cfg),
        "MEMORY.md": render_memory(cfg),
        "TASKS.md": render_tasks(cfg),
    }

    for filename, content in contents.items():
        target = path / filename
        backup_file(target)
        target.write_text(content.strip() + "\n", encoding="utf-8")

    print(f"UPDATED: {cfg['name']} -> {path}")


def main():
    for name, cfg in AGENTS.items():
        validate_protected_template(name, cfg)
        write_agent(cfg)


if __name__ == "__main__":
    main()

