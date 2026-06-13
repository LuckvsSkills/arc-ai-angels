#!/usr/bin/env python3

from __future__ import annotations

import json
import re
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import List, Optional


ROOT = Path("/home/prime/arc_ai_angels")
AGENTS_DIR = ROOT / "agents"

RUNTIME_DIR = ROOT / "runtime" / "scheduler"
QUEUE_DIR = RUNTIME_DIR / "queue"
HISTORY_DIR = RUNTIME_DIR / "history"

DUE_TASKS_FILE = RUNTIME_DIR / "due_tasks.json"
STATE_FILE = RUNTIME_DIR / "scheduler.state.json"
LOG_FILE = RUNTIME_DIR / "scheduler.log"

ACTIVE_TASKS_FILE = QUEUE_DIR / "active_tasks.json"
MISSED_TASKS_FILE = QUEUE_DIR / "missed_tasks.json"
ESCALATIONS_FILE = QUEUE_DIR / "escalations.json"
EXECUTION_REQUESTS_FILE = QUEUE_DIR / "execution_requests.json"
RETRY_STATE_FILE = QUEUE_DIR / "retry_state.json"
COMPLETED_TASKS_FILE = HISTORY_DIR / "completed_tasks.json"

TASK_ID_RE = re.compile(r"^###\s+task_id:\s*(.+?)\s*$")
FIELD_RE = re.compile(r"^- ([a-zA-Z0-9_]+):\s*(.*)$")

ALLOWED_SOURCE_STATUSES = {"scheduled", "active"}
MAX_RETRIES_DEFAULT = 3


@dataclass
class Task:
    task_id: str
    title: str
    status: str
    priority: str
    owner: str
    created_at: str
    execute_at: str
    next_action: str
    source: str = ""
    related_session: str = ""
    related_journal: str = ""
    file_path: str = ""
    retry_count: int = 0
    max_retries: int = MAX_RETRIES_DEFAULT
    escalate_after: str = ""
    notes: str = ""
    runtime_status: str = ""
    detected_at: str = ""
    missed_at: str = ""


def utcnow() -> datetime:
    return datetime.utcnow()


def ensure_dirs() -> None:
    for directory in [RUNTIME_DIR, QUEUE_DIR, HISTORY_DIR]:
        directory.mkdir(parents=True, exist_ok=True)


def log(message: str) -> None:
    ensure_dirs()
    timestamp = utcnow().isoformat()
    line = f"[{timestamp}] {message}"
    print(line)
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(line + "\n")


def read_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


def write_json(path: Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def iso_to_dt(value: str) -> Optional[datetime]:
    value = str(value).strip()
    if not value or value.lower() == "none":
        return None
    try:
        return datetime.fromisoformat(value)
    except ValueError:
        return None


def safe_int(value: str, default: int = 0) -> int:
    try:
        return int(str(value).strip())
    except Exception:
        return default


def task_key_from_values(file_path: str, task_id: str) -> str:
    return f"{file_path}::{task_id}"


def task_key(task: Task) -> str:
    return task_key_from_values(task.file_path, task.task_id)


def safe_slug(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = value.strip("-")
    return value[:60] or "task-event"


def find_task_files(root: Path) -> List[Path]:
    paths: List[Path] = []
    for path in root.rglob("TASKS.md"):
        if any(part in path.parts for part in [
            "archive",
            "backups",
            "legacy_persona_20260412-200253",
            "legacy_persona_20260412-200254",
            "nexus-ai-kit-starter",
            ".npm-global",
        ]):
            continue
        paths.append(path)
    return sorted(paths)


def get_agent_dir_from_file_path(file_path: str) -> Optional[Path]:
    if not file_path:
        return None
    path = Path(file_path)
    if path.name != "TASKS.md":
        return None
    return path.parent


def journal_event_exists(journal_open_dir: Path, task_id: str, event_type: str) -> bool:
    if not journal_open_dir.exists():
        return False
    pattern = f"*_{event_type}_{safe_slug(task_id)}.md"
    return any(journal_open_dir.glob(pattern))


def write_journal_event(item: dict, event_type: str, message: str) -> None:
    file_path = item.get("file_path", "")
    agent_dir = get_agent_dir_from_file_path(file_path)
    if agent_dir is None:
        return

    journal_open_dir = agent_dir / "JOURNAL" / "open"
    journal_open_dir.mkdir(parents=True, exist_ok=True)

    task_id = item.get("task_id", "")
    if not task_id:
        return

    if journal_event_exists(journal_open_dir, task_id, event_type):
        return

    timestamp = utcnow()
    journal_file = journal_open_dir / (
        f"{timestamp.strftime('%Y-%m-%d')}_"
        f"{timestamp.strftime('%H%M%S')}_"
        f"{event_type}_{safe_slug(task_id)}.md"
    )

    content = f"""# Scheduler Event: {event_type}

## Metadata
- date: {timestamp.isoformat()}
- agent: {item.get("owner", "")}
- scope: scheduler
- status: open
- related_task: {task_id}
- related_files:
  - {file_path}
- author_layer: system_process

## Situation
A scheduled task lifecycle event was detected by the local ARC scheduler.

## What happened
{message}

## Task reference
- task_id: {task_id}
- title: {item.get("title", "")}
- owner: {item.get("owner", "")}
- execute_at: {item.get("execute_at", "")}
- escalate_after: {item.get("escalate_after", "")}
- retry_count: {item.get("runtime_retry_count", item.get("retry_count", 0))}
- max_retries: {item.get("max_retries", MAX_RETRIES_DEFAULT)}

## Continuity impact
This event preserves execution continuity so the agent or supervising layer can resume, inspect, retry, or escalate the task without relying on chat memory.

## Required follow-up
- Review the task state in TASKS.md and runtime scheduler queue.
- Complete, retry, cancel, or escalate the task according to governance.

## Promotion check
- move to MEMORY.md? no
- move to TASKS.md? already linked
- move to canon? no

## Closure condition
This journal entry may be closed when the linked task is completed, canceled, or formally escalated.
"""
    journal_file.write_text(content, encoding="utf-8")
    log(f"Journal event written | event={event_type} | task_id={task_id} | file={journal_file}")


def parse_tasks_md(path: Path) -> List[Task]:
    tasks: List[Task] = []
    lines = path.read_text(encoding="utf-8").splitlines()

    current_section = ""
    current_task_id = None
    current_fields = {}

    def flush_current() -> None:
        nonlocal current_task_id, current_fields

        if not current_task_id:
            return

        if current_section != "scheduled":
            current_task_id = None
            current_fields = {}
            return

        status = current_fields.get("status", "").strip().lower()
        if status not in ALLOWED_SOURCE_STATUSES:
            current_task_id = None
            current_fields = {}
            return

        execute_at = current_fields.get("execute_at", "").strip()
        if not execute_at:
            current_task_id = None
            current_fields = {}
            return

        tasks.append(Task(
            task_id=current_task_id.strip(),
            title=current_fields.get("title", "").strip(),
            status=status,
            priority=current_fields.get("priority", "").strip().lower(),
            owner=current_fields.get("owner", "").strip(),
            created_at=current_fields.get("created_at", "").strip(),
            execute_at=execute_at,
            next_action=current_fields.get("next_action", "").strip(),
            source=current_fields.get("source", "").strip(),
            related_session=current_fields.get("related_session", "").strip(),
            related_journal=current_fields.get("related_journal", "").strip(),
            file_path=str(path),
            retry_count=safe_int(current_fields.get("retry_count", "0")),
            max_retries=safe_int(current_fields.get("max_retries", str(MAX_RETRIES_DEFAULT)), MAX_RETRIES_DEFAULT),
            escalate_after=current_fields.get("escalate_after", "").strip(),
            notes=current_fields.get("notes", "").strip(),
        ))

        current_task_id = None
        current_fields = {}

    for raw_line in lines:
        line = raw_line.rstrip()

        if line.startswith("## "):
            flush_current()
            header = line[3:].strip().lower()
            current_section = "scheduled" if header.startswith("scheduled / time-bound") else "other"
            continue

        match_task = TASK_ID_RE.match(line)
        if match_task:
            flush_current()
            current_task_id = match_task.group(1).strip()
            current_fields = {}
            continue

        if current_task_id:
            match_field = FIELD_RE.match(line)
            if match_field:
                current_fields[match_field.group(1).strip()] = match_field.group(2).strip()

    flush_current()
    return tasks


def collect_due_tasks(tasks: List[Task], now: datetime) -> List[Task]:
    due: List[Task] = []
    for task in tasks:
        execute_dt = iso_to_dt(task.execute_at)
        if execute_dt is None:
            log(f"Skipping invalid execute_at | task_id={task.task_id} | file={task.file_path}")
            continue

        if execute_dt <= now:
            task.runtime_status = "active"
            task.detected_at = now.isoformat()
            due.append(task)

    return due


def update_active_queue(due_tasks: List[Task]) -> List[dict]:
    existing_payload = read_json(ACTIVE_TASKS_FILE, {"tasks": []})
    existing = existing_payload.get("tasks", [])

    existing_by_key = {
        task_key_from_values(item.get("file_path", ""), item.get("task_id", "")): item
        for item in existing
    }

    for task in due_tasks:
        key = task_key(task)

        if key not in existing_by_key:
            item = asdict(task)
            item["runtime_status"] = "active"
            item["detected_at"] = task.detected_at or utcnow().isoformat()
            item["runtime_retry_count"] = task.retry_count
            existing_by_key[key] = item

            log(f"Activated task | owner={task.owner} | task_id={task.task_id}")
            write_journal_event(
                item,
                "activated",
                "The scheduler detected that this scheduled task is now due and moved it into the active runtime queue."
            )
        else:
            existing_by_key[key]["last_seen_due_at"] = utcnow().isoformat()

    active_tasks = list(existing_by_key.values())

    write_json(ACTIVE_TASKS_FILE, {
        "generated_at": utcnow().isoformat(),
        "count": len(active_tasks),
        "tasks": active_tasks,
    })

    return active_tasks


def build_execution_requests(active_tasks: List[dict]) -> List[dict]:
    existing_payload = read_json(EXECUTION_REQUESTS_FILE, {"requests": []})
    existing = existing_payload.get("requests", [])

    existing_keys = {
        task_key_from_values(item.get("file_path", ""), item.get("task_id", ""))
        for item in existing
    }

    requests = list(existing)

    for item in active_tasks:
        key = task_key_from_values(item.get("file_path", ""), item.get("task_id", ""))

        if key in existing_keys:
            continue

        request = {
            "request_id": f"exec_{safe_slug(item.get('task_id', ''))}",
            "task_id": item.get("task_id", ""),
            "owner": item.get("owner", ""),
            "title": item.get("title", ""),
            "next_action": item.get("next_action", ""),
            "source": item.get("source", ""),
            "priority": item.get("priority", ""),
            "file_path": item.get("file_path", ""),
            "related_session": item.get("related_session", ""),
            "related_journal": item.get("related_journal", ""),
            "created_at": utcnow().isoformat(),
            "status": "pending_execution",
            "execution_mode": "manual_or_external",
            "api_calls": 0,
            "notes": "Created by local scheduler. No API call was made."
        }

        requests.append(request)
        existing_keys.add(key)

        write_journal_event(
            item,
            "execution-requested",
            "The scheduler created a local execution request for this active task. No API call was made."
        )

        log(f"Execution request created | owner={item.get('owner')} | task_id={item.get('task_id')}")

    write_json(EXECUTION_REQUESTS_FILE, {
        "generated_at": utcnow().isoformat(),
        "count": len(requests),
        "requests": requests,
    })

    return requests


def collect_missed_tasks(active_tasks: List[dict], now: datetime) -> List[dict]:
    missed = []

    for item in active_tasks:
        escalate_dt = iso_to_dt(item.get("escalate_after", ""))
        if escalate_dt is None:
            continue

        if escalate_dt <= now:
            item = dict(item)
            item["runtime_status"] = "missed"
            item["missed_at"] = now.isoformat()
            missed.append(item)

    return missed


def update_retry_and_escalations(missed_tasks: List[dict]) -> tuple[list[dict], list[dict]]:
    retry_payload = read_json(RETRY_STATE_FILE, {"items": []})
    retry_items = retry_payload.get("items", [])

    retry_by_key = {
        task_key_from_values(item.get("file_path", ""), item.get("task_id", "")): item
        for item in retry_items
    }

    escalations = []

    for item in missed_tasks:
        key = task_key_from_values(item.get("file_path", ""), item.get("task_id", ""))
        max_retries = safe_int(item.get("max_retries", MAX_RETRIES_DEFAULT), MAX_RETRIES_DEFAULT)

        existing_retry = retry_by_key.get(key, {})
        runtime_retry_count = safe_int(existing_retry.get("runtime_retry_count", item.get("runtime_retry_count", item.get("retry_count", 0))))

        if runtime_retry_count < max_retries:
            runtime_retry_count += 1
            retry_item = dict(item)
            retry_item["runtime_status"] = "retry_pending"
            retry_item["runtime_retry_count"] = runtime_retry_count
            retry_item["max_retries"] = max_retries
            retry_item["last_retry_marked_at"] = utcnow().isoformat()
            retry_item["api_calls"] = 0
            retry_by_key[key] = retry_item

            write_journal_event(
                retry_item,
                f"retry-{runtime_retry_count}",
                f"The scheduler marked this missed task for retry {runtime_retry_count} of {max_retries}. No API call was made."
            )

            log(
                f"RETRY PENDING | owner={item.get('owner')} | "
                f"task_id={item.get('task_id')} | retry={runtime_retry_count}/{max_retries}"
            )
        else:
            escalation = dict(item)
            escalation["runtime_status"] = "escalated"
            escalation["runtime_retry_count"] = runtime_retry_count
            escalation["max_retries"] = max_retries
            escalation["escalation_reason"] = "Task passed escalate_after and exceeded max retries"
            escalation["escalated_at"] = utcnow().isoformat()
            escalation["api_calls"] = 0
            escalations.append(escalation)

            write_journal_event(
                escalation,
                "escalated",
                "The scheduler escalated this task because it passed its escalation threshold and exceeded max retries."
            )

            log(
                f"ESCALATION | owner={item.get('owner')} | "
                f"task_id={item.get('task_id')} | retry={runtime_retry_count}/{max_retries}"
            )

    retry_items_out = list(retry_by_key.values())

    write_json(RETRY_STATE_FILE, {
        "generated_at": utcnow().isoformat(),
        "count": len(retry_items_out),
        "items": retry_items_out,
    })

    write_json(ESCALATIONS_FILE, {
        "generated_at": utcnow().isoformat(),
        "count": len(escalations),
        "tasks": escalations,
    })

    return retry_items_out, escalations


def write_due_tasks(due_tasks: List[Task]) -> None:
    write_json(DUE_TASKS_FILE, {
        "generated_at": utcnow().isoformat(),
        "count": len(due_tasks),
        "tasks": [asdict(task) for task in due_tasks],
    })


def write_missed_tasks(missed_tasks: List[dict]) -> None:
    write_json(MISSED_TASKS_FILE, {
        "generated_at": utcnow().isoformat(),
        "count": len(missed_tasks),
        "tasks": missed_tasks,
    })

    for item in missed_tasks:
        write_journal_event(
            item,
            "missed",
            "The scheduler detected that this task passed its escalate_after threshold without completion."
        )


def save_state(
    task_files_count: int,
    scheduled_count: int,
    due_count: int,
    active_count: int,
    execution_request_count: int,
    missed_count: int,
    retry_count: int,
    escalation_count: int,
) -> None:
    write_json(STATE_FILE, {
        "last_run_at": utcnow().isoformat(),
        "task_files_scanned": task_files_count,
        "scheduled_tasks_found": scheduled_count,
        "due_tasks_found": due_count,
        "active_runtime_tasks": active_count,
        "execution_requests": execution_request_count,
        "missed_tasks_found": missed_count,
        "retry_items": retry_count,
        "escalations": escalation_count,
        "api_calls": 0,
        "journal_events_enabled": True,
        "execution_requests_enabled": True,
        "retry_escalation_enabled": True,
    })


def main() -> int:
    ensure_dirs()
    now = utcnow()

    task_files = find_task_files(AGENTS_DIR)
    log(f"Scanning {len(task_files)} TASKS.md files")

    all_tasks: List[Task] = []
    for task_file in task_files:
        try:
            all_tasks.extend(parse_tasks_md(task_file))
        except Exception as exc:
            log(f"Failed to parse {task_file}: {exc}")

    due_tasks = collect_due_tasks(all_tasks, now)
    write_due_tasks(due_tasks)

    active_tasks = update_active_queue(due_tasks)
    execution_requests = build_execution_requests(active_tasks)

    missed_tasks = collect_missed_tasks(active_tasks, now)
    write_missed_tasks(missed_tasks)

    retry_items, escalations = update_retry_and_escalations(missed_tasks)

    log(f"Found scheduled/active source tasks: {len(all_tasks)}")
    log(f"Due task count: {len(due_tasks)}")
    log(f"Active runtime task count: {len(active_tasks)}")
    log(f"Execution request count: {len(execution_requests)}")
    log(f"Missed task count: {len(missed_tasks)}")
    log(f"Retry item count: {len(retry_items)}")
    log(f"Escalation count: {len(escalations)}")

    save_state(
        task_files_count=len(task_files),
        scheduled_count=len(all_tasks),
        due_count=len(due_tasks),
        active_count=len(active_tasks),
        execution_request_count=len(execution_requests),
        missed_count=len(missed_tasks),
        retry_count=len(retry_items),
        escalation_count=len(escalations),
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
