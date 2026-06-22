---
name: memory-consolidation
description: "Automates the process of consolidating daily logs into a long-term memory file (e.g., MEMORY.md). Th"
metadata: { "openclaw": { "emoji": "⭐", "approved_by": "Supreme Fea", "approved_at": "2026-06-22" } }
---
# Memory Consolidation Workflow

Automates the process of consolidating daily logs into a long-term memory file (e.g., MEMORY.md). This includes reviewing specified daily log files, confirming accuracy of existing summaries, removing consolidated daily log files, and documenting any new insights or tasks. It also includes error handling for cases where the memory or task files are not accessible.

## Workflow

- Identify and locate daily log files for a given period (e.g., memory/YYYY-MM-DD.md).
- Read and review specified daily log files.
- Read and review the long-term memory file (e.g., MEMORY.md).
- Confirm accuracy of existing summaries in the long-term memory file for the reviewed daily logs.
- If a task file (e.g., TASKS.md) is specified: 
  - Attempt to locate and read TASKS.md.
  - If not found directly, perform a general search (e.g., using tavily) to understand its nature (e.g., a file format for a system).
  - If direct access fails, report inability to access and await further instructions or clarification.
- If the long-term memory file (e.g., MEMORY.md) is specified:
  - Attempt to locate and read MEMORY.md.
  - If not found, report inability to access and await further instructions.
- Remove consolidated daily log files to maintain system cleanliness.
- Document any new insights or explicit tasks derived from the consolidation process.
- If any steps fail due to file inaccessibility, generate a report detailing the failures and reasons, and request guidance on how to access the necessary files for future procedures.
- Output a final report summarizing the consolidation status, including any issues encountered and necessary actions for the Omni Lead.
