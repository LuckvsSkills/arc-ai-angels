#!/usr/bin/env bash
set -euo pipefail

PORT="18789"
ENV_FILE="$HOME/.openclaw/.env"
LOG_DIR="/tmp/openclaw"
TODAY="$(date +%F)"
LOG_FILE="$LOG_DIR/openclaw-$TODAY.log"
PID_FILE="$LOG_DIR/openclaw-gateway.pid"

echo "🚀 Starting OpenClaw Gateway (no systemd)"
echo "Port: $PORT"
echo "Env:  $ENV_FILE"
echo "Log:  $LOG_FILE"
echo ""

mkdir -p "$LOG_DIR"

# 1) Load env
if [ -f "$ENV_FILE" ]; then
  set -a
  # shellcheck disable=SC1090
  source "$ENV_FILE"
  set +a
else
  echo "❌ ERROR: Env file not found: $ENV_FILE"
  exit 1
fi

# 2) Validate keys
[ -n "${GEMINI_API_KEY:-}" ] && echo "✅ GEMINI_API_KEY detected (length: ${#GEMINI_API_KEY})" || { echo "❌ GEMINI_API_KEY missing"; exit 1; }
[ -n "${MOONSHOT_API_KEY:-}" ] && echo "✅ MOONSHOT_API_KEY detected (length: ${#MOONSHOT_API_KEY})" || echo "ℹ️  MOONSHOT_API_KEY not set (Kimi disabled)"

# 3) Map GEMINI -> GOOGLE (OpenClaw provider name is often 'google' for Gemini)
export GOOGLE_API_KEY="${GOOGLE_API_KEY:-$GEMINI_API_KEY}"

# 4) Stop anything already listening on PORT
OLDPID="$(ss -ltnp 2>/dev/null | awk -v p=":$PORT" '$0 ~ p {print $NF}' | head -n1 | sed -E 's/.*pid=([0-9]+).*/\1/' || true)"
if [ -n "${OLDPID:-}" ]; then
  echo "⚠️  Port $PORT already in use by PID=$OLDPID — stopping it"
  kill "$OLDPID" 2>/dev/null || true
  sleep 1
fi

# 5) Start gateway (foreground via nohup)
echo ""
echo "▶️  Launching: openclaw gateway --port $PORT"
nohup openclaw gateway --port "$PORT" >> "$LOG_FILE" 2>&1 &
sleep 0.7

# 6) Record REAL listener PID
PID="$(ss -ltnp 2>/dev/null | awk -v p=":$PORT" '$0 ~ p {print $NF; exit}' | sed -E 's/.*pid=([0-9]+).*/\1/' || true)"
if [ -z "${PID:-}" ]; then
  echo "❌ Gateway did not bind to port $PORT. Check log:"
  tail -n 120 "$LOG_FILE" || true
  exit 1
fi

echo "$PID" > "$PID_FILE"
echo "✅ Started. Listener PID=$PID"
echo "PID file: $PID_FILE"
