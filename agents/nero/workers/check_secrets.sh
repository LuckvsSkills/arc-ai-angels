#!/bin/bash
# check_secrets.sh — Nero worker
# Finale secrets check voor deploy
# Gebruik: bash check_secrets.sh /pad/naar/code_dir

CODE_DIR=$1
if [ -z "$CODE_DIR" ]; then
    echo "Gebruik: bash check_secrets.sh /pad/naar/code_dir"
    exit 1
fi

echo "🔑 Nero secrets check: $CODE_DIR"
ISSUES=0

# Check op .env bestanden in repo
if find "$CODE_DIR" -name ".env" -not -name ".env.example" | grep -q .; then
    echo "❌ KRITIEK: .env bestand gevonden in repo"
    ((ISSUES++))
fi

# Check op hardcoded tokens
if grep -r "sk_live_" "$CODE_DIR" --include="*.py" --include="*.js" -l 2>/dev/null | grep -q .; then
    echo "❌ KRITIEK: Stripe live key gevonden"
    ((ISSUES++))
fi

if grep -r "ghp_" "$CODE_DIR" --include="*.py" --include="*.js" -l 2>/dev/null | grep -q .; then
    echo "❌ KRITIEK: GitHub token gevonden"
    ((ISSUES++))
fi

# Check op wachtwoorden
if grep -rE "password\s*=\s*['\"][^'\"]{4,}['\"]" "$CODE_DIR" --include="*.py" -l 2>/dev/null | grep -q .; then
    echo "⚠️  WARNING: Mogelijk hardcoded password"
fi

if [ $ISSUES -eq 0 ]; then
    echo "✅ Geen kritieke secrets gevonden"
    exit 0
else
    echo "❌ $ISSUES kritieke secrets gevonden — deploy geblokkeerd"
    exit 1
fi
