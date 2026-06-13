#!/usr/bin/env bash
set -euo pipefail

BASE="$HOME/arc_strategic_control_center"

echo "==> Building progress.json"
python3 "$BASE/build_progress.py"

echo "==> Rebuilding chapter pages"
python3 "$BASE/rebuild_chapters_v2.py"

echo "==> Ensuring prompt library exists"
python3 "$BASE/build_prompt_library.py"

echo "==> Re-adding copy buttons to prompt library"
python3 "$BASE/add_copy_buttons.py"

echo "==> Re-linking homepage to progress.json"
python3 "$BASE/upgrade_home_progress.py"

echo "==> Done"
