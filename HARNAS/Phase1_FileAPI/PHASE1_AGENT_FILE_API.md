# PHASE 1: AGENT FILE API
## Implementation of File Operations for Agent Independence

Date: 2026-06-01
Status: IMPLEMENTATION IN PROGRESS
Goal: Agents manage own JOURNAL, TASKS, MEMORY files

---

## 🎯 WHAT WE'RE BUILDING

A set of **file operations** that agents can call to:
1. Read files (JOURNAL/closed/, MEMORY.md, etc)
2. Write files (JOURNAL/open/, MEMORY.md updates)
3. Move files (JOURNAL/open/ → /closed/)
4. Append to files (adding steps to JOURNAL)
5. List directories (check what files exist)

---

## 📝 REQUIRED FILE OPERATIONS

### 1. READ FILE
```bash
read_agent_file(agent, path)
├─ Input: Agent name, file path
├─ Returns: File contents
└─ Example: read_agent_file("arix", "JOURNAL/closed/task-001.md")
```

### 2. WRITE FILE
```bash
write_agent_file(agent, path, content)
├─ Input: Agent name, path, content
├─ Returns: Success/failure
└─ Example: write_agent_file("arix", "MEMORY.md", "Method X: 93%")
```

### 3. APPEND FILE
```bash
append_agent_file(agent, path, content)
├─ Input: Agent name, path, content to append
├─ Returns: Success/failure
└─ Example: append_agent_file("arix", "JOURNAL/open/task-001.md", "- 10:05 Extracted: SUCCESS")
```

### 4. MOVE FILE
```bash
move_agent_file(agent, source, dest)
├─ Input: Agent name, source path, destination path
├─ Returns: Success/failure
└─ Example: move_agent_file("arix", "JOURNAL/open/task-001.md", "JOURNAL/closed/task-001.md")
```

### 5. LIST DIRECTORY
```bash
list_agent_directory(agent, path)
├─ Input: Agent name, directory path
├─ Returns: List of files in directory
└─ Example: list_agent_directory("arix", "JOURNAL/closed/")
```

---

## 🔧 IMPLEMENTATION APPROACH

### Option A: OpenClaw Custom Tools
If OpenClaw supports custom tools, we can add these as new tools:
- `agent_read_file`
- `agent_write_file`
- `agent_move_file`
- `agent_append_file`
- `agent_list_directory`

### Option B: Wrapper Scripts
Create bash scripts that agents can call via exec:
- `/home/prime/arc_ai_angels/COMMON/agent-file-ops.sh`
- Agents call: `exec "bash agent-file-ops.sh read arix JOURNAL/closed/"`

### Option C: Agent Bootstrap Enhancement
Update BOOTSTRAP.md to include these operations:
- Agents already have access via OpenClaw tools
- Just document how to use them

---

## 📋 TESTING PLAN

### Test with ARIX
1. ARIX reads own JOURNAL/closed/ files
2. ARIX extracts learnings
3. ARIX writes to MEMORY.md
4. ARIX appends to JOURNAL/open/
5. ARIX moves JOURNAL to /closed/

### Success Criteria
- ✅ All file operations work
- ✅ No permission errors
- ✅ Files updated correctly
- ✅ ARIX can do this repeatedly

---

## 🚀 NEXT: DETERMINE APPROACH

We need to know:
1. Does OpenClaw support custom file operation tools?
2. Can agents execute bash scripts?
3. Do agents have direct file system access?

---

## FILES TO CREATE/MODIFY

1. **File Operations Library** - `/home/prime/arc_ai_angels/COMMON/agent-file-ops.sh`
2. **ARIX Bootstrap Update** - Add file operation instructions
3. **Test Script** - Verify operations work
4. **Documentation** - How agents use file operations

Ready to implement?

