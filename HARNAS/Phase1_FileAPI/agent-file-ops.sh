#!/bin/bash

# AGENT FILE OPERATIONS LIBRARY
# Allows agents to manage their own JOURNAL, TASKS, MEMORY files
# Usage: agent-file-ops.sh <agent> <operation> <path> [content]

AGENT=$1
OPERATION=$2
AGENT_PATH="/home/prime/arc_ai_angels/agents/$AGENT"
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")

# Verify agent exists
if [ ! -d "$AGENT_PATH" ]; then
  echo "ERROR: Agent $AGENT not found at $AGENT_PATH"
  exit 1
fi

case $OPERATION in
  
  # READ: read_file <agent> <path>
  read)
    FILE_PATH=$3
    if [ ! -f "$AGENT_PATH/$FILE_PATH" ]; then
      echo "ERROR: File not found: $FILE_PATH"
      exit 1
    fi
    cat "$AGENT_PATH/$FILE_PATH"
    ;;
  
  # WRITE: write_file <agent> <path> <content>
  write)
    FILE_PATH=$3
    CONTENT=$4
    DIR=$(dirname "$AGENT_PATH/$FILE_PATH")
    mkdir -p "$DIR"
    echo "$CONTENT" > "$AGENT_PATH/$FILE_PATH"
    echo "✓ Written to $FILE_PATH"
    ;;
  
  # APPEND: append_file <agent> <path> <content>
  append)
    FILE_PATH=$3
    CONTENT=$4
    DIR=$(dirname "$AGENT_PATH/$FILE_PATH")
    mkdir -p "$DIR"
    echo "$CONTENT" >> "$AGENT_PATH/$FILE_PATH"
    echo "✓ Appended to $FILE_PATH"
    ;;
  
  # MOVE: move_file <agent> <source> <dest>
  move)
    SOURCE=$3
    DEST=$4
    if [ ! -f "$AGENT_PATH/$SOURCE" ]; then
      echo "ERROR: Source file not found: $SOURCE"
      exit 1
    fi
    DEST_DIR=$(dirname "$AGENT_PATH/$DEST")
    mkdir -p "$DEST_DIR"
    mv "$AGENT_PATH/$SOURCE" "$AGENT_PATH/$DEST"
    echo "✓ Moved $SOURCE → $DEST"
    ;;
  
  # LIST: list_directory <agent> <path>
  list)
    DIR=$3
    if [ ! -d "$AGENT_PATH/$DIR" ]; then
      echo "ERROR: Directory not found: $DIR"
      exit 1
    fi
    ls -1 "$AGENT_PATH/$DIR"
    ;;
  
  # STAT: stat_file <agent> <path>
  stat)
    FILE_PATH=$3
    if [ ! -f "$AGENT_PATH/$FILE_PATH" ]; then
      echo "ERROR: File not found: $FILE_PATH"
      exit 1
    fi
    wc -l "$AGENT_PATH/$FILE_PATH"
    ;;
  
  *)
    echo "ERROR: Unknown operation: $OPERATION"
    echo "Operations: read, write, append, move, list, stat"
    exit 1
    ;;
esac

