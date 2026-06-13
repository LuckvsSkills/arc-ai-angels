import os

BASE_DIR = "/home/prime/arc_ai_angels"
AGENTS_DIR = f"{BASE_DIR}/agents"
CODEX_DIR = f"{BASE_DIR}/CODEX"
HARNAS_DIR = f"{BASE_DIR}/HARNAS"
MCC_DIR = f"{BASE_DIR}/MCC"
LOGS_DIR = f"{BASE_DIR}/logs"

OPENCLAW_GATEWAY = "http://localhost:50506"
OPENCLAW_TOKEN_FILE = os.path.expanduser("~/.openclaw/token")
OPENCLAW_ENV_FILE = os.path.expanduser("~/.openclaw/gateway.systemd.env")

def get_openclaw_token():
    # Probeer env bestand eerst
    try:
        for line in open(OPENCLAW_ENV_FILE).readlines():
            if line.startswith("OPENCLAW_GATEWAY_TOKEN="):
                return line.strip().split("=",1)[1]
    except: pass
    # Dan token bestand
    try:
        return open(OPENCLAW_TOKEN_FILE).read().strip()
    except: pass
    # Dan openclaw.json
    try:
        import json
        d = json.load(open(os.path.expanduser("~/.openclaw/openclaw.json")))
        return d.get("gateway",{}).get("token","")
    except: pass
    return ""
""

GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", "")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", "")
JWT_SECRET = os.environ.get("JWT_SECRET", "arc-ai-angels-secret-2026")
FRONTEND_URL = os.environ.get("FRONTEND_URL", "https://arc-vortex.nl")
