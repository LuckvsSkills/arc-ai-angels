#!/usr/bin/env bash
set -euo pipefail

BASE="$HOME/arc_ai_angels"
REPORTS="$BASE/reports"
ANALYSIS_DIR="$REPORTS/chat_analysis"
SCRIPTS="$BASE/scripts"
EXTRACTOR="$SCRIPTS/chat_context_extractor_v21.py"

mkdir -p "$REPORTS" "$ANALYSIS_DIR"

if [ ! -f "$EXTRACTOR" ]; then
  echo "Extractor niet gevonden: $EXTRACTOR"
  exit 1
fi

echo "=== ARC AI ANGELS — CHAT ANALYSE INTERACTIEF ==="
echo

# --- stap 1: naam ---
read -r -p "Geef een naam voor deze chat/analyse: " CHAT_TITLE

if [ -z "${CHAT_TITLE// }" ]; then
  echo "Geen naam ingevuld."
  exit 1
fi

SAFE_TITLE=$(printf '%s' "$CHAT_TITLE" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9._-]/_/g')
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# --- stap 2: map per chat ---
CHAT_DIR="$ANALYSIS_DIR/${SAFE_TITLE}_${TIMESTAMP}"
mkdir -p "$CHAT_DIR"

DUMP_FILE="$CHAT_DIR/chat_dump.txt"

echo
echo "📁 Alles voor deze chat wordt opgeslagen in:"
echo "$CHAT_DIR"
echo
echo "📝 Dump bestand:"
echo "$DUMP_FILE"
echo

# --- stap 3: input ---
echo "Plak nu de volledige chatgeschiedenis."
echo "Als je klaar bent: druk Enter en daarna Ctrl+D op een lege regel."
echo
echo "----- BEGIN PLAKKEN -----"

cat > "$DUMP_FILE"

echo "----- EINDE PLAKKEN -----"
echo
echo "✅ Chat dump opgeslagen."
echo

# --- stap 4: analyse ---
echo "🔍 Analyse wordt uitgevoerd..."
echo

python3 "$EXTRACTOR" "$DUMP_FILE" --title "$CHAT_TITLE"

# --- stap 5: verplaats output naar chat map ---
echo
echo "📦 Verplaatsen van analysebestanden naar chat map..."

LATEST_FILES=$(find "$ANALYSIS_DIR" -maxdepth 1 -type f -name '*v21*' | sort | tail -n 3)

for f in $LATEST_FILES; do
  mv "$f" "$CHAT_DIR/" 2>/dev/null || true
done

echo "✅ Alles opgeslagen in:"
echo "$CHAT_DIR"

# --- stap 6: preview ---
echo
LATEST_TXT=$(find "$CHAT_DIR" -type f -name 'chat_context_extract_v21_*.txt' | head -n 1 || true)
LATEST_PROMPT=$(find "$CHAT_DIR" -type f -name 'continuation_prompt_v21_*.md' | head -n 1 || true)

if [ -n "${LATEST_TXT:-}" ]; then
  echo
  echo "=== TXT RAPPORT ==="
  echo "$LATEST_TXT"
  sed -n '1,200p' "$LATEST_TXT"
fi

if [ -n "${LATEST_PROMPT:-}" ]; then
  echo
  echo "=== CONTINUATION PROMPT ==="
  echo "$LATEST_PROMPT"
  sed -n '1,200p' "$LATEST_PROMPT"
fi

# --- stap 7: afsluit optie ---
echo
read -r -p "Druk [Enter] om opnieuw te starten of typ 'q' om te stoppen: " EXIT_CHOICE

if [[ "$EXIT_CHOICE" == "q" ]]; then
  echo "👋 Script gestopt."
  exit 0
else
  echo
  echo "🔁 Script wordt opnieuw gestart..."
  exec "$0"
fi
