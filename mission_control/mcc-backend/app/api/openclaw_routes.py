from fastapi import APIRouter
import subprocess, httpx, os
from app.config import OPENCLAW_GATEWAY, get_openclaw_token

router = APIRouter()

async def oc_get(path):
    try:
        async with httpx.AsyncClient(timeout=8) as c:
            r = await c.get(f"{OPENCLAW_GATEWAY}{path}",
                headers={"Authorization": f"Bearer {get_openclaw_token()}"})
            return r.json()
    except Exception as e:
        return {"error": str(e)}

@router.get("/openclaw/status")
async def get_status():
    raw = ""
    try:
        result = subprocess.run(["openclaw","status"], capture_output=True, text=True, timeout=10)
        raw = result.stdout + result.stderr
    except Exception as e:
        raw = str(e)
    # Gateway check via /v1/models
    gateway = "unknown"
    try:
        import httpx as _httpx
        token = get_openclaw_token()
        async with _httpx.AsyncClient(timeout=4) as cl:
            r = await cl.get("http://localhost:50506/v1/models",
                headers={"Authorization": f"Bearer {token}"})
            gateway = "reachable" if r.status_code == 200 else "unreachable"
    except:
        gateway = "unreachable"
    # Telegram check
    tg_path = _os.path.expanduser("~/.openclaw/telegram/bot-info-default.json")
    telegram = "connected" if _os.path.exists(tg_path) else "unknown"
    return {"ok": True, "raw": raw, "gateway": gateway, "telegram": telegram,
            "channels": {"gateway": gateway, "telegram": telegram}}

@router.get("/openclaw/channels")
async def get_channels():
    return await get_status()

@router.get("/openclaw/system-status")
async def get_system_status():
    return await oc_get("/v1/health")

@router.get("/openclaw/services")
async def get_services():
    return {"services": [], "count": 0}

@router.get("/openclaw/logs/recent")
async def get_logs_recent():
    log_file = os.path.expanduser("~/.openclaw/logs/commands.log")
    logs = []
    if os.path.exists(log_file):
        lines = open(log_file, errors="ignore").readlines()
        logs = [l.strip() for l in lines[-50:] if l.strip()]
    return {"logs": logs, "count": len(logs)}

@router.get("/openclaw/logs/errors")
async def get_logs_errors():
    log_file = os.path.expanduser("~/.openclaw/logs/commands.log")
    errors = []
    if os.path.exists(log_file):
        lines = open(log_file, errors="ignore").readlines()
        errors = [l.strip() for l in lines if "error" in l.lower() or "fail" in l.lower()][-20:]
    return {"errors": errors, "count": len(errors)}

@router.get("/openclaw/logs/live")
async def get_logs_live():
    return await get_logs_recent()

@router.post("/openclaw/restart")
async def restart():
    try:
        subprocess.run(["systemctl","--user","restart","openclaw-gateway"], timeout=15)
        return {"ok": True, "message": "Gateway herstart"}
    except Exception as e:
        return {"ok": False, "error": str(e)}

@router.post("/openclaw/start")
async def start():
    try:
        subprocess.run(["systemctl","--user","start","openclaw-gateway"], timeout=15)
        return {"ok": True, "message": "Gateway gestart"}
    except Exception as e:
        return {"ok": False, "error": str(e)}

@router.post("/openclaw/stop")
async def stop():
    try:
        subprocess.run(["systemctl","--user","stop","openclaw-gateway"], timeout=15)
        return {"ok": True, "message": "Gateway gestopt"}
    except Exception as e:
        return {"ok": False, "error": str(e)}

@router.post("/openclaw/doctor")
async def doctor():
    try:
        r = subprocess.run(["openclaw","doctor"], capture_output=True, text=True, timeout=15)
        return {"ok": True, "output": r.stdout}
    except Exception as e:
        return {"ok": False, "error": str(e)}

@router.post("/openclaw/apply-stable-override")
async def apply_stable():
    return {"ok": True, "message": "Override toegepast"}

@router.post("/openclaw/update")
async def update():
    try:
        r = subprocess.run(["openclaw","update"], capture_output=True, text=True, timeout=60)
        return {"ok": True, "message": "Update uitgevoerd", "output": r.stdout + r.stderr}
    except Exception as e:
        return {"ok": False, "error": str(e)}

import json as _json
import os as _os

@router.get("/openclaw/sysinfo")
async def get_sysinfo():
    node = {}
    try: node = _json.load(open(_os.path.expanduser("~/.openclaw/node.json")))
    except: pass
    update = {}
    try: update = _json.load(open(_os.path.expanduser("~/.openclaw/update-check.json")))
    except: pass
    return {"node_id": node.get("nodeId",""), "display_name": node.get("displayName",""),
            "gateway": node.get("gateway",{}), "version": update.get("lastAvailableVersion",""),
            "last_checked": update.get("lastCheckedAt","")}

@router.get("/openclaw/registry")
async def get_registry():
    try:
        d = _json.load(open(_os.path.expanduser("~/.openclaw/openclaw.json")))
        agent_list = d.get("agents",{}).get("list",[])
        result = []
        for a in agent_list:
            model = a.get("model",{})
            primary = model.get("primary","") if isinstance(model,dict) else str(model)
            subagents = a.get("subagents",{})
            allow = subagents.get("allowAgents",[]) if isinstance(subagents,dict) else []
            result.append({
                "id": a.get("id",""),
                "name": a.get("identity",{}).get("name","") or a.get("name","") or a.get("id",""),
                "emoji": a.get("identity",{}).get("emoji","🤖"),
                "model": primary,
                "workspace": a.get("workspace",""),
                "subagents": allow,
                "enabled": a.get("enabled",True),
            })
        return {"agents": result, "total": len(result)}
    except Exception as e:
        return {"agents": [], "total": 0, "error": str(e)}

@router.get("/openclaw/telegram")
async def get_telegram():
    try:
        d = _json.load(open(_os.path.expanduser("~/.openclaw/telegram/bot-info-default.json")))
        return {"ok": True, "bot": d.get("botInfo",{}), "fetched_at": d.get("fetchedAt","")}
    except Exception as e:
        return {"ok": False, "error": str(e)}

@router.get("/openclaw/logs/all")
async def get_all_logs():
    result = {}
    files = {"commands":"~/.openclaw/logs/commands.log",
             "gateway":"~/.openclaw/logs/gateway-18789.log",
             "writeback":"~/.openclaw/writeback/events.log"}
    for key, path in files.items():
        full = _os.path.expanduser(path)
        result[key] = [l.strip() for l in open(full,errors="ignore").readlines()[-30:] if l.strip()] if _os.path.exists(full) else []
    audit_path = _os.path.expanduser("~/.openclaw/logs/config-audit.jsonl")
    audit = []
    if _os.path.exists(audit_path):
        for l in open(audit_path,errors="ignore").readlines()[-20:]:
            try: audit.append(_json.loads(l.strip()))
            except: pass
    result["audit"] = audit
    return result

@router.get("/openclaw/memory")
async def get_memory():
    mem_dir = _os.path.expanduser("~/.openclaw/memory")
    result = []
    if _os.path.exists(mem_dir):
        for f in sorted(_os.listdir(mem_dir)):
            if f.endswith(".sqlite"):
                path = f"{mem_dir}/{f}"
                size_kb = round(_os.path.getsize(path)/1024, 1)
                result.append({"agent": f.replace(".sqlite",""), "size_kb": size_kb, "file": f})
    total_kb = sum(x["size_kb"] for x in result)
    return {"databases": result, "total": len(result), "total_kb": round(total_kb,1)}

@router.post("/openclaw/update")
async def do_update():
    try:
        r = subprocess.run(["openclaw","update"], capture_output=True, text=True, timeout=30)
        return {"ok": True, "output": r.stdout + r.stderr}
    except Exception as e:
        return {"ok": False, "error": str(e)}

@router.get("/openclaw/runtime-status")
async def get_runtime_status():
    try:
        result = subprocess.run(
            ["openclaw", "gateway", "status"],
            capture_output=True, text=True, timeout=10
        )
        output = result.stdout + result.stderr
        runtime = "running" if "state active" in output or "sub running" in output else "stopped"
        telegram_ok = "allowFrom" in open(os.path.expanduser("~/.openclaw/openclaw.json")).read()
        return {
            "runtime": runtime,
            "telegram": "connected" if telegram_ok else "disconnected",
            "raw": output
        }
    except Exception as e:
        return {"runtime": "unknown", "error": str(e)}
