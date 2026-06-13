from pathlib import Path
from typing import List
import importlib.util

CFG_PATH = Path("/home/prime/arc_ai_angels/scripts/agent_config.py")

spec = importlib.util.spec_from_file_location("agent_config", str(CFG_PATH))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

AGENTS = mod.AGENTS


def read_file(path):
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8").strip()


def ok(label):
    print("[OK] {}".format(label))


def fail(label):
    print("[FAIL] {}".format(label))


def contains_all(content, checks):
    content_lower = content.lower()
    return all(check.lower() in content_lower for check in checks)


def must_contain_identity(cfg, content):
    checks = [
        "# identity",
        "## layer",
        "## domain",
        "## parent",
        "## role",
        "## mission",
        "## core identity",
        "## cognitive style",
        "## decision logic",
        "## boundaries",
        "## position",
        cfg["layer"],
        cfg["domain"],
        cfg["parent"],
        cfg["role"],
    ]
    return contains_all(content, checks)


def must_contain_handoff(cfg, content):
    checks = [
        "# handoff",
        "## current focus",
        "## next action",
        "## blockers",
        "## resume point",
    ]
    return contains_all(content, checks)


def must_contain_memory(cfg, content):
    checks = [
        "# memory",
        "## structure rules",
        "## learnings",
    ]
    return contains_all(content, checks)


def must_contain_tasks(cfg, content):
    checks = [
        "# tasks.md",
        "## active tasks",
        "task id:",
        "project id:",
        "origin:",
        "title:",
        "summary:",
        "priority:",
        "project priority:",
        "effort size:",
        "queue group:",
        "blocking impact:",
        "status:",
        "owner layer:",
        "owner agent:",
        "assigned by:",
        "assigned to:",
        "domain:",
        "depends on:",
        "created at:",
        "updated at:",
        "started at:",
        "expected end at:",
        "blocked reason:",
        "next step:",
        "trace link:",
        cfg["domain"],
    ]
    return contains_all(content, checks)


print("\n=== VALIDATION START ===\n")

for agent_key, cfg in AGENTS.items():
    print("\n--- {} ---".format(agent_key.upper()))

    base_path = Path(cfg["path"])

    identity_path = base_path / "IDENTITY.md"
    handoff_path = base_path / "HANDOFF.md"
    memory_path = base_path / "MEMORY.md"
    tasks_path = base_path / "TASKS.md"

    identity_content = read_file(identity_path)
    handoff_content = read_file(handoff_path)
    memory_content = read_file(memory_path)
    tasks_content = read_file(tasks_path)

    if identity_content and must_contain_identity(cfg, identity_content):
        ok("IDENTITY.md")
    else:
        fail("IDENTITY.md content mismatch")

    if handoff_content and must_contain_handoff(cfg, handoff_content):
        ok("HANDOFF.md")
    else:
        fail("HANDOFF.md content mismatch")

    if memory_content and must_contain_memory(cfg, memory_content):
        ok("MEMORY.md")
    else:
        fail("MEMORY.md content mismatch")

    if tasks_content and must_contain_tasks(cfg, tasks_content):
        ok("TASKS.md")
    else:
        fail("TASKS.md content mismatch")

print("\n=== VALIDATION DONE ===\n")

