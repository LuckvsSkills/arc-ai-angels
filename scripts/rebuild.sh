
#!/bin/bash

TARGET="$HOME/arc_ai_angels/OPENCLAW SECURITY ROADMAP v1/OPENCLAW_SECURITY_ROADMAP_v1"

cd "$TARGET" || exit

echo "Rebuilding HTML..."

# Markdown naar HTML (simpele versie)
pandoc roadmap.md -o roadmap.html
pandoc action_blocks.md -o action_blocks.html

echo "Done."

