#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path.home() / "arc_ai_angels" / "agents"

def read(p):
    try:
        return p.read_text(encoding="utf-8", errors="ignore")
    except:
        return ""

def write(p, content):
    p.write_text(content, encoding="utf-8")

def normalize_identity(path, agent):
    text = read(path)

    def extract(section):
        m = re.search(rf"## {section}([\s\S]*?)(\n## |\Z)", text)
        return m.group(1).strip() if m else ""

    role = extract("Role")
    mission = extract("Mission")
    core = extract("Core Identity")
    style = extract("Cognitive Style")
    logic = extract("Decision Logic")
    boundaries = extract("Boundaries")
    position = extract("Position")

    new = f"""# IDENTITY — {agent}

## Layer
<SET>

## Domain
<SET>

## Parent
<SET>

## Role
{role}

## Mission
{mission}

## Core Identity
{core}

## Cognitive Style
{style}

## Decision Logic
{logic}

## Boundaries
{boundaries}

## Position
{position}
"""
    write(path, new)


def normalize_tasks(path, agent):
    text = read(path)

    # behoud alles onder Active Tasks
    m = re.search(r"## Active Tasks([\s\S]*)", text)
    tasks = m.group(1).strip() if m else ""

    new = f"""# TASKS.md — {agent}

## Active Tasks

{tasks}
"""
    write(path, new)


def normalize_memory(path, agent):
    text = read(path)

    m = re.search(r"## Learnings([\s\S]*)", text)
    learnings = m.group(1).strip() if m else ""

    new = f"""# MEMORY — {agent}

## Structure rules
- keep only reusable learnings
- no daily noise
- no duplicated task status
- escalate domain boundary issues to parent

## Learnings

{learnings}
"""
    write(path, new)


def normalize_handoff(path, agent):
    text = read(path)

    new = f"""# HANDOFF — {agent}

## Current State
{text[:200]}

## Active Context
- extracted from previous version

## Next Actions
- continue task flow
"""
    write(path, new)


def process_agent(folder):
    agent = folder.name.lower()

    for file in folder.glob("*.md"):
        if file.name == "IDENTITY.md":
            normalize_identity(file, agent)
        elif file.name == "TASKS.md":
            normalize_tasks(file, agent)
        elif file.name == "MEMORY.md":
            normalize_memory(file, agent)
        elif file.name == "HANDOFF.md":
            normalize_handoff(file, agent)


def main():
    for path in ROOT.rglob("*"):
        if path.is_dir():
            process_agent(path)

    print("Normalization complete.")

if __name__ == "__main__":
    main()

