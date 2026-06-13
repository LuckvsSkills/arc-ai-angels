# PHASE 1 IMPLEMENTATION: Agent File API
## Building Agent File Operations

Date: 2026-06-01
Status: STARTING IMPLEMENTATION
Goal: Agents can read/write/move files independently

---

## 🎯 APPROACH

Since OpenClaw agents communicate via messages, we use:
1. **Agent Instructions** (in BOOTSTRAP) - Tell agents HOW to do file ops
2. **Wrapper Scripts** - Agents can call bash scripts
3. **File Operations** - Agents execute via bash commands

---

## 📝 FILE OPERATIONS LIBRARY

Create `/home/prime/arc_ai_angels/COMMON/agent-file-ops.sh`:
- read_file(agent, path)
- write_file(agent, path, content)
- append_file(agent, path, content)
- move_file(agent, source, dest)
- list_directory(agent, path)

---

## 🔧 IMPLEMENTATION STEPS

### STEP 1: Create File Operations Library
File: `/home/prime/arc_ai_angels/COMMON/agent-file-ops.sh`

```bash
#!/bin/bash

AGENT=$1
OPERATION=$2
AGENT_PATH="/home/prime/arc_ai_angels/agents/$AGENT"

case $OPERATION in
  read)
    FILE_PATH=$3
    cat "$AGENT_PATH/$FILE_PATH"
    ;;
  write)
    FILE_PATH=$3
    CONTENT=$4
    echo "$CONTENT" > "$AGENT_PATH/$FILE_PATH"
    ;;
  append)
    FILE_PATH=$3
    CONTENT=$4
    echo "$CONTENT" >> "$AGENT_PATH/$FILE_PATH"
    ;;
  move)
    SOURCE=$3
    DEST=$4
    mv "$AGENT_PATH/$SOURCE" "$AGENT_PATH/$DEST"
    ;;
  list)
    DIR=$3
    ls -1 "$AGENT_PATH/$DIR"
    ;;
esac
```

### STEP 2: Update ARIX BOOTSTRAP
Add instructions for file operations to ARIX's BOOTSTRAP.md

### STEP 3: Test with ARIX
1. ARIX reads JOURNAL/closed/
2. ARIX writes to MEMORY.md
3. ARIX moves JOURNAL files
4. Verify all operations work

### STEP 4: Rollout to All 32 Agents
Update all BOOTSTRAP files with file operation instructions

---

## ✅ SUCCESS CRITERIA

- ✅ agent-file-ops.sh works
- ✅ ARIX can read files
- ✅ ARIX can write files
- ✅ ARIX can move files
- ✅ All 32 agents have file operations

---

Ready to begin?

