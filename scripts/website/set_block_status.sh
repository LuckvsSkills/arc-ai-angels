#!/usr/bin/env bash
set -euo pipefail

BASE="$HOME/arc_strategic_control_center"

if [ "$#" -ne 2 ]; then
  echo "Usage: $0 <block_id> <planned|started|finished>"
  exit 1
fi

python3 "$BASE/set_block_status.py" "$1" "$2"
"$BASE/rebuild_all.sh"
echo "Done. Refresh http://localhost:8080"
