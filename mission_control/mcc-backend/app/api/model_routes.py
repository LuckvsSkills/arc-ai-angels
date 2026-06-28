from fastapi import APIRouter
import os, json
from app.config import AGENTS_DIR

router = APIRouter()

AGENT_IDS = ["nova","flux","flux_core","cortexia","nero","forge","axon","ventura","clio",
             "finoria","kairo","kenzo","odis","vector","zion","saelia","arix",
             "daxio","enki","sora","tharos","lumeria","elora","kresta","luvia",
             "nura","vondra","fluentia","draven","orizon","solis","unia","zena"]

DOMAIN_MAP = {
    "core":    ["nova","flux","flux_core"],
    "helix":   ["cortexia","nero","forge","axon","ventura","clio"],
    "finix":   ["finoria","kairo","kenzo","odis","vector","zion"],
    "matrix":  ["saelia","arix","daxio","enki","sora","tharos"],
    "quantix": ["lumeria","elora","kresta","luvia","nura","vondra"],
    "zenix":   ["fluentia","draven","orizon","solis","unia","zena"]
}

def get_domain(agent_id):
    for d, agents in DOMAIN_MAP.items():
        if agent_id in agents: return d
    return "unknown"

def read_agent_model_config(agent_id):
    base = f"{AGENTS_DIR}/{agent_id}"
    result = {
        "id": agent_id,
        "domain": get_domain(agent_id),
        "tierBaseline": "?",
        "baselineModel": "?",
        "tierA": [],
        "tierB": [],
        "tierC": [],
        "currentModel": None,
        "lastUsed": None
    }
    models_json = f"{base}/agent/models.json"
    if os.path.exists(models_json):
        try:
            d = json.load(open(models_json, errors="ignore"))
            if "tierBaseline" in d:
                result["tierBaseline"] = d.get("tierBaseline", "?")
                result["baselineModel"] = d.get("baselineModel", "?")
                result["tierA"] = d.get("tierA", [])
                result["tierB"] = d.get("tierB", [])
                result["tierC"] = d.get("tierC", [])
                result["currentModel"] = d.get("baselineModel", "?")
        except:
            pass

    # Fallback: lees MODEL.md als geen tier-formaat gevonden
    if result["tierBaseline"] == "?":
        import re
        model_md = f"{base}/MODEL.md"
        if os.path.exists(model_md):
            try:
                md = open(model_md, errors="ignore").read()
                # Lees Baseline Tier
                m = re.search(r'\*\*Tier:\*\*\s*([ABC])', md)
                if m: result["tierBaseline"] = m.group(1)
                # Lees Baseline Model
                m = re.search(r'\*\*Model:\*\*\s*(.+)', md)
                if m:
                    result["baselineModel"] = m.group(1).strip()
                    result["currentModel"] = m.group(1).strip()
                # Lees tiers uit tabel
                for tier, key in [('A', 'tierA'), ('B', 'tierB'), ('C', 'tierC')]:
                    rows = re.findall(rf'\|\s*{tier}[^|]*\|\s*([^|]+)\|', md)
                    if rows:
                        models = [r.strip() for r in rows[0].split(',') if r.strip() and r.strip() != '—']
                        if models:
                            result[key] = models
            except:
                pass
    return result

@router.get("/api/models/overview")
def models_overview():
    agents = []
    for aid in AGENT_IDS:
        agents.append(read_agent_model_config(aid))
    summary = {
        "total": len(agents),
        "tierA": len([a for a in agents if a["tierBaseline"] == "A"]),
        "tierB": len([a for a in agents if a["tierBaseline"] == "B"]),
        "tierC": len([a for a in agents if a["tierBaseline"] == "C"]),
    }
    return {"agents": agents, "summary": summary}

@router.get("/api/models/agent/{agent_id}")
def agent_model(agent_id: str):
    return read_agent_model_config(agent_id)

@router.get("/api/models/domain/{domain}")
def domain_models(domain: str):
    agents = DOMAIN_MAP.get(domain, [])
    return {"domain": domain, "agents": [read_agent_model_config(a) for a in agents]}
