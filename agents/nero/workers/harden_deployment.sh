#!/bin/bash
# harden_deployment.sh — Nero worker
# Past security hardening toe op website code
# Gebruik: bash harden_deployment.sh /pad/naar/code_dir

CODE_DIR=$1
if [ -z "$CODE_DIR" ]; then
    echo "Gebruik: bash harden_deployment.sh /pad/naar/code_dir"
    exit 1
fi

echo "🔒 Nero hardening: $CODE_DIR"

# .gitignore aanmaken/updaten
GITIGNORE="$CODE_DIR/.gitignore"
if [ ! -f "$GITIGNORE" ]; then
    cat > "$GITIGNORE" << 'GITEOF'
.env
.env.local
.env.production
node_modules/
__pycache__/
*.pyc
.DS_Store
dist/
build/
*.db
*.sqlite
GITEOF
    echo "✅ .gitignore aangemaakt"
else
    grep -q "^\.env$" "$GITIGNORE" || echo ".env" >> "$GITIGNORE"
    echo "✅ .gitignore bijgewerkt"
fi

# Security headers toevoegen aan FastAPI backend indien aanwezig
MAIN_PY=$(find "$CODE_DIR" -name "main.py" | head -1)
if [ ! -z "$MAIN_PY" ]; then
    if ! grep -q "X-Frame-Options" "$MAIN_PY"; then
        cat >> "$MAIN_PY" << 'PYEOF'

# Security headers middleware
from fastapi import Request
from fastapi.responses import Response

@app.middleware("http")
async def security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    return response
PYEOF
        echo "✅ Security headers toegevoegd aan $MAIN_PY"
    fi
fi

# Rate limiting dependency toevoegen aan requirements.txt
REQ=$(find "$CODE_DIR" -name "requirements.txt" | head -1)
if [ ! -z "$REQ" ]; then
    grep -q "slowapi" "$REQ" || echo "slowapi==0.1.9" >> "$REQ"
    echo "✅ Rate limiting dependency toegevoegd"
fi

echo "✅ Hardening voltooid: $CODE_DIR"
