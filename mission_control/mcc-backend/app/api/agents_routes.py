from fastapi import APIRouter, HTTPException
import httpx, json, os, subprocess
from app.config import OPENCLAW_GATEWAY, AGENTS_DIR, get_openclaw_token

LITELLM_URL = "http://localhost:4000"

# Model per agent tier
# Volledig tier systeem per agent
# Structuur: primary → tier-fallback → default-fallback
AGENT_TIER_CONFIG = {
    # ── CORE ──
    'nova':      {'model': 'arc-nova',  'tier': 'B', 'fallbacks': ['arc-nova-or', 'arc-mid', 'arc-low'], 'provider': 'OpenAI GPT-4o-mini'},
    'flux':      {'model': 'arc-flux',  'tier': 'A', 'fallbacks': ['arc-flux-or', 'arc-high', 'arc-mid'], 'provider': 'Kimi K2.6 Moonshot'},
    'flux_core': {'model': 'arc-flux',  'tier': 'A', 'fallbacks': ['arc-flux-or', 'arc-high', 'arc-mid'], 'provider': 'Kimi K2.6 Moonshot'},
    # ── OMNI LEADS ──
    'cortexia':  {'model': 'arc-mid',   'tier': 'B', 'fallbacks': ['arc-mid-or', 'arc-mid-gemini', 'arc-low'], 'provider': 'OpenAI GPT-4o-mini'},
    'finoria':   {'model': 'arc-mid',   'tier': 'B', 'fallbacks': ['arc-mid-or', 'arc-mid-gemini', 'arc-low'], 'provider': 'OpenAI GPT-4o-mini'},
    'saelia':    {'model': 'arc-mid',   'tier': 'B', 'fallbacks': ['arc-mid-or', 'arc-mid-gemini', 'arc-low'], 'provider': 'OpenAI GPT-4o-mini'},
    'lumeria':   {'model': 'arc-mid',   'tier': 'B', 'fallbacks': ['arc-mid-or', 'arc-mid-gemini', 'arc-low'], 'provider': 'OpenAI GPT-4o-mini'},
    'fluentia':  {'model': 'arc-mid',   'tier': 'B', 'fallbacks': ['arc-mid-or', 'arc-mid-gemini', 'arc-low'], 'provider': 'OpenAI GPT-4o-mini'},
    # ── SENTINELS — alle arc-low (Gemini Flash) ──
}
# Default voor alle sentinels
SENTINEL_CONFIG = {'model': 'arc-low', 'tier': 'C', 'fallbacks': ['arc-low-or', 'arc-low-deepseek', 'gemini-flash'], 'provider': 'Gemini 2.5 Flash'}

def get_agent_tier_config(agent_id):
    return AGENT_TIER_CONFIG.get(agent_id, SENTINEL_CONFIG)

def get_agent_model(agent_id):
    return get_agent_tier_config(agent_id)['model']

LITELLM_URL = "http://localhost:4000"

# Model per agent tier
# Volledig tier systeem per agent
# Structuur: primary → tier-fallback → default-fallback
AGENT_TIER_CONFIG = {
    # ── CORE ──
    'nova':      {'model': 'arc-nova',  'tier': 'B', 'fallbacks': ['arc-nova-or', 'arc-mid', 'arc-low'], 'provider': 'OpenAI GPT-4o-mini'},
    'flux':      {'model': 'arc-flux',  'tier': 'A', 'fallbacks': ['arc-flux-or', 'arc-high', 'arc-mid'], 'provider': 'Kimi K2.6 Moonshot'},
    'flux_core': {'model': 'arc-flux',  'tier': 'A', 'fallbacks': ['arc-flux-or', 'arc-high', 'arc-mid'], 'provider': 'Kimi K2.6 Moonshot'},
    # ── OMNI LEADS ──
    'cortexia':  {'model': 'arc-mid',   'tier': 'B', 'fallbacks': ['arc-mid-or', 'arc-mid-gemini', 'arc-low'], 'provider': 'OpenAI GPT-4o-mini'},
    'finoria':   {'model': 'arc-mid',   'tier': 'B', 'fallbacks': ['arc-mid-or', 'arc-mid-gemini', 'arc-low'], 'provider': 'OpenAI GPT-4o-mini'},
    'saelia':    {'model': 'arc-mid',   'tier': 'B', 'fallbacks': ['arc-mid-or', 'arc-mid-gemini', 'arc-low'], 'provider': 'OpenAI GPT-4o-mini'},
    'lumeria':   {'model': 'arc-mid',   'tier': 'B', 'fallbacks': ['arc-mid-or', 'arc-mid-gemini', 'arc-low'], 'provider': 'OpenAI GPT-4o-mini'},
    'fluentia':  {'model': 'arc-mid',   'tier': 'B', 'fallbacks': ['arc-mid-or', 'arc-mid-gemini', 'arc-low'], 'provider': 'OpenAI GPT-4o-mini'},
    # ── SENTINELS — alle arc-low (Gemini Flash) ──
}
# Default voor alle sentinels
SENTINEL_CONFIG = {'model': 'arc-low', 'tier': 'C', 'fallbacks': ['arc-low-or', 'arc-low-deepseek', 'gemini-flash'], 'provider': 'Gemini 2.5 Flash'}

def get_agent_tier_config(agent_id):
    return AGENT_TIER_CONFIG.get(agent_id, SENTINEL_CONFIG)

def get_agent_model(agent_id):
    return get_agent_tier_config(agent_id)['model']
import os

router = APIRouter()

AGENT_LIST = [
    {"id":"nova",     "name":"Nova",     "role":"Gateway",       "layer":"gateway",      "domain":"core"},
    {"id":"flux",     "name":"Flux",     "role":"Orchestrator",  "layer":"orchestrator", "domain":"core"},
    {"id":"cortexia", "name":"Cortexia", "role":"Omni Lead",     "layer":"lead",         "domain":"helix"},
    {"id":"nero",     "name":"Nero",     "role":"Security",      "layer":"sentinel",     "domain":"helix"},
    {"id":"forge",    "name":"Forge",    "role":"Engineering",   "layer":"sentinel",     "domain":"helix"},
    {"id":"axon",     "name":"Axon",     "role":"Automation",    "layer":"sentinel",     "domain":"helix"},
    {"id":"ventura",  "name":"Ventura",  "role":"Infrastructure","layer":"sentinel",     "domain":"helix"},
    {"id":"clio",     "name":"Clio",     "role":"Documentation", "layer":"sentinel",     "domain":"helix"},
    {"id":"finoria",  "name":"Finoria",  "role":"Omni Lead",     "layer":"lead",         "domain":"finix"},
    {"id":"kairo",    "name":"Kairo",    "role":"Finance Ops",   "layer":"sentinel",     "domain":"finix"},
    {"id":"kenzo",    "name":"Kenzo",    "role":"Modeling",      "layer":"sentinel",     "domain":"finix"},
    {"id":"odis",     "name":"Odis",     "role":"Data",          "layer":"sentinel",     "domain":"finix"},
    {"id":"vector",   "name":"Vector",   "role":"Analytics",     "layer":"sentinel",     "domain":"finix"},
    {"id":"zion",     "name":"Zion",     "role":"Risk",          "layer":"sentinel",     "domain":"finix"},
    {"id":"saelia",   "name":"Saelia",   "role":"Omni Lead",     "layer":"lead",         "domain":"matrix"},
    {"id":"arix",     "name":"Arix",     "role":"Structure",     "layer":"sentinel",     "domain":"matrix"},
    {"id":"daxio",    "name":"Daxio",    "role":"Processing",    "layer":"sentinel",     "domain":"matrix"},
    {"id":"enki",     "name":"Enki",     "role":"Logic",         "layer":"sentinel",     "domain":"matrix"},
    {"id":"sora",     "name":"Sora",     "role":"AI",            "layer":"sentinel",     "domain":"matrix"},
    {"id":"tharos",   "name":"Tharos",   "role":"Knowledge",     "layer":"sentinel",     "domain":"matrix"},
    {"id":"lumeria",  "name":"Lumeria",  "role":"Omni Lead",     "layer":"lead",         "domain":"quantix"},
    {"id":"elora",    "name":"Elora",    "role":"Analysis",      "layer":"sentinel",     "domain":"quantix"},
    {"id":"kresta",   "name":"Kresta",   "role":"Strategy",      "layer":"sentinel",     "domain":"quantix"},
    {"id":"luvia",    "name":"Luvia",    "role":"Modeling",      "layer":"sentinel",     "domain":"quantix"},
    {"id":"nura",     "name":"Nura",     "role":"Optimization",  "layer":"sentinel",     "domain":"quantix"},
    {"id":"vondra",   "name":"Vondra",   "role":"Monitoring",    "layer":"sentinel",     "domain":"quantix"},
    {"id":"fluentia", "name":"Fluentia", "role":"Omni Lead",     "layer":"lead",         "domain":"zenix"},
    {"id":"draven",   "name":"Draven",   "role":"Flow",          "layer":"sentinel",     "domain":"zenix"},
    {"id":"orizon",   "name":"Orizon",   "role":"Reasoning",     "layer":"sentinel",     "domain":"zenix"},
    {"id":"solis",    "name":"Solis",    "role":"Operations",    "layer":"sentinel",     "domain":"zenix"},
    {"id":"unia",     "name":"Unia",     "role":"Polish",        "layer":"sentinel",     "domain":"zenix"},
    {"id":"zena",     "name":"Zena",     "role":"Branding",      "layer":"sentinel",     "domain":"zenix"},
]

@router.get("/agents")
async def get_agents():
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            r = await client.get(f"{OPENCLAW_GATEWAY}/v1/models",
                headers={"Authorization": f"Bearer {get_openclaw_token()}"})
            oc_agents = r.json().get("data", [])
            oc_ids = {a["id"] for a in oc_agents}
    except:
        oc_ids = set()

    agents = []
    for a in AGENT_LIST:
        agent = dict(a)
        agent["status"] = "online" if a["id"] in oc_ids else "offline"
        agent["memory_file"] = os.path.exists(f"{AGENTS_DIR}/{a['id']}/MEMORY.md")
        agents.append(agent)
    return {"agents": agents, "total": len(agents)}

@router.get("/agents/{agent_id}")
async def get_agent(agent_id: str):
    agent = next((a for a in AGENT_LIST if a["id"] == agent_id), None)
    if not agent:
        raise HTTPException(404, f"Agent {agent_id} niet gevonden")
    result = dict(agent)
    # Lees IDENTITY.md
    identity_file = f"{AGENTS_DIR}/{agent_id}/IDENTITY.md"
    if os.path.exists(identity_file):
        result["identity"] = open(identity_file).read()
    return result

@router.post("/agents/{agent_id}/chat")
async def chat_with_agent(agent_id: str, body: dict):
    message = body.get("message", "")
    if not message:
        raise HTTPException(400, "Geen bericht")
    # Lees agent IDENTITY voor system prompt
    system_prompt = ""
    try:
        identity_path = f"{AGENTS_DIR}/{agent_id}/IDENTITY.md"
        if os.path.exists(identity_path):
            with open(identity_path, 'r') as f:
                identity = f.read()[:2000]
            soul_path = f"{AGENTS_DIR}/{agent_id}/SOUL.md"
            soul = ""
            if os.path.exists(soul_path):
                with open(soul_path, 'r') as f:
                    soul = f.read()[:1000]
            system_prompt = f"{identity}\n\n{soul}\n\nJij bent {agent_id}. Antwoord altijd in karakter, beknopt en direct."
    except: pass

    model = get_agent_model(agent_id)
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": message})

    # Probeer eerst LiteLLM
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            r = await client.post(
                f"{LITELLM_URL}/v1/chat/completions",
                headers={"Content-Type": "application/json"},
                json={"model": model, "messages": messages}
            )
            data = r.json()
            if "choices" in data:
                reply = data["choices"][0]["message"]["content"]
                return {"agent_id": agent_id, "reply": reply, "ok": True, "model": model}
    except Exception as e:
        pass

    # Fallback naar OpenClaw gateway
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            r = await client.post(
                f"{OPENCLAW_GATEWAY}/v1/chat/completions",
                headers={"Authorization": f"Bearer {get_openclaw_token()}"},
                json={"model": f"openclaw/{agent_id}", "messages": [{"role":"user","content":message}]}
            )
            data = r.json()
            reply = data["choices"][0]["message"]["content"]
            return {"agent_id": agent_id, "reply": reply, "ok": True, "model": "openclaw-fallback"}
    except Exception as e:
        return {"agent_id": agent_id, "reply": f"Agent niet bereikbaar: {e}", "ok": False}

@router.get("/voice/key")
def get_voice_key():
    key = ""
    for path in ["~/.openclaw/gateway.systemd.env", "~/.openclaw/.env"]:
        try:
            for line in open(os.path.expanduser(path)).readlines():
                if line.startswith("ELEVENLABS_API_KEY="):
                    val = line.strip().split("=",1)[1]
                    if val: key = val; break
        except: pass
        if key: break
    return {"key": key, "available": bool(key)}

# Agent rollen voor context
AGENT_ROLES = {
    "nova": "Consigliere — gateway en intake, spreekt namens Supreme Fea",
    "flux": "Underboss — orchestrator, neemt operationele besluiten",
    "cortexia": "Helix Lead — tech, systemen, infra, security, GitHub",
    "finoria": "Finix Lead — financien, trading, data, risicobeheer",
    "saelia": "Matrix Lead — data intelligence, research, archief, kennis",
    "lumeria": "Quantix Lead — analytics, forecasting, metrics, trends",
    "fluentia": "Zenix Lead — content, copy, SEO, social, email, brand",
    "nero": "Security Sentinel — bewaakt systeem integriteit",
    "forge": "GitHub Sentinel — code, repos, deployments",
    "axon": "Infra Sentinel — servers, netwerk, monitoring",
    "ventura": "Deploy Sentinel — releases, staging, productie",
    "clio": "Logging Sentinel — logs, audit trails, rapportage",
    "kairo": "Trading Sentinel — marktdata, signalen, posities",
    "kenzo": "Analytics Sentinel — data analyse, patronen",
    "odis": "DeFi Sentinel — decentralized finance protocollen",
    "vector": "Data Sentinel — datapijplijnen, kwaliteit",
    "zion": "Risk Sentinel — risicomodellen, exposure",
    "tharos": "Research Sentinel — diepgaand onderzoek",
    "sora": "Creative Sentinel — creatieve output, design",
    "arix": "Archive Sentinel — kennisarchief, documentatie",
    "enki": "Knowledge Sentinel — kennisbase, leren",
    "daxio": "Data Sentinel — datastromen, transformaties",
    "kresta": "Reports Sentinel — rapportages, dashboards",
    "elora": "Forecast Sentinel — voorspellingen, scenario analyses",
    "luvia": "Metrics Sentinel — KPIs, prestatiemeting",
    "nura": "Insights Sentinel — zakelijke inzichten",
    "vondra": "Trends Sentinel — markttrends, signalering",
    "draven": "Copy Sentinel — teksten, campagnes",
    "solis": "SEO Sentinel — zoekoptimalisatie, keywords",
    "orizon": "Social Sentinel — sociale media, engagement",
    "unia": "Email Sentinel — email marketing, automation",
    "zena": "Brand Sentinel — merkidentiteit, positionering",
}

CHAT_TYPES = {
    "core": "group",
    "leads": "council",
    "helix": "team", "finix": "team", "matrix": "team",
    "quantix": "team", "zenix": "team",
}

@router.post("/chat/group")
async def group_chat(body: dict):
    agents_list = body.get("agents", [])
    message = body.get("message", "")
    history = body.get("history", [])
    channel_label = body.get("channel_label", "groepsgesprek")
    channel_type = body.get("channel_type", "group")  # group|council|team
    sender_name = body.get("sender_name", "Supreme Fea")
    lead_agent = body.get("lead", agents_list[0] if agents_list else "nova")

    if not agents_list or not message:
        raise HTTPException(400, "agents en message verplicht")

    def build_history_str(all_history):
        lines = []
        for h in all_history[-14:]:
            who = "Supreme Fea" if h["from"] == "user" else h.get("name", h["from"])
            lines.append(f"{who}: {h['text']}")
        return "\n".join(lines) if lines else "(begin van gesprek)"

    def build_context(agent_id, msg, sender):
        role = AGENT_ROLES.get(agent_id, f"{agent_id} agent")
        hist = build_history_str(history)
        others = [a for a in agents_list if a != agent_id]
        other_names = ", ".join(others[:6])

        if channel_type == "council":
            return f"""[LEAD COUNCIL — {channel_label}]
[Jij bent: {agent_id.upper()} — {role}]
[Aanwezigen: {', '.join(agents_list)}]

[Gesprekshistorie:]
{hist}
{sender}: {msg}

Reageer als {agent_id} in deze council vergadering. Spreek vanuit jouw domein expertise. 
Richt je tot de relevante personen. Als Nova of Flux iets zegt neem dat mee.
Wees direct en zakelijk. Max 3 zinnen tenzij je een concreet punt te melden hebt.
Noem actiepunten als [ACTIE: beschrijving] als je concrete acties voorstelt."""

        elif channel_type == "team":
            is_lead = agent_id == lead_agent
            if is_lead:
                return f"""[TEAM BRIEFING — {channel_label}]
[Jij bent: {agent_id.upper()} — {role} — TEAM LEAD]
[Jouw team: {other_names}]

[Gesprekshistorie:]
{hist}
{sender}: {msg}

Als team lead reageer je op wat er gezegd is. Stuur het gesprek, geef richting aan je team.
Benoem wie wat moet doen. Wees besluitvaardig. Noem actiepunten als [ACTIE: agent: beschrijving]."""
            else:
                return f"""[TEAM BRIEFING — {channel_label}]
[Jij bent: {agent_id.upper()} — {role}]
[Team lead: {lead_agent}]
[Team: {', '.join(agents_list)}]

[Gesprekshistorie:]
{hist}
{sender}: {msg}

Reageer als {agent_id} vanuit jouw specifieke rol. Breng je domein-specifieke perspectief in.
Spreek je lead aan als relevant. Wees beknopt. Noem actiepunten als [ACTIE: beschrijving]."""

        else:  # group
            return f"""[GROEPSGESPREK — {channel_label}]
[Jij bent: {agent_id.upper()} — {role}]
[Anderen: {other_names}]

[Gesprekshistorie:]
{hist}
{sender}: {msg}

Reageer als jezelf. Spreek anderen direct aan. Wees natuurlijk en beknopt."""

    responses = []
    async with httpx.AsyncClient(timeout=45) as client:
        for agent_id in agents_list:
            try:
                ctx = build_context(agent_id, message, sender_name)
                model = get_agent_model(agent_id)
                # Lees system prompt
                sys_prompt = ""
                try:
                    ip = f"{AGENTS_DIR}/{agent_id}/IDENTITY.md"
                    if os.path.exists(ip):
                        sys_prompt = open(ip).read()[:1500]
                except: pass

                msgs = []
                if sys_prompt:
                    msgs.append({"role": "system", "content": sys_prompt})
                msgs.append({"role": "user", "content": ctx})

                # Probeer LiteLLM eerst
                litellm_ok = False
                try:
                    r2 = await client.post(
                        f"{LITELLM_URL}/v1/chat/completions",
                        headers={"Content-Type": "application/json"},
                        json={"model": model, "messages": msgs},
                        timeout=30
                    )
                    d2 = r2.json()
                    if "choices" in d2:
                        reply = d2["choices"][0]["message"]["content"]
                        litellm_ok = True
                except: pass

                if not litellm_ok:
                    r = await client.post(
                        f"{OPENCLAW_GATEWAY}/v1/chat/completions",
                        headers={"Authorization": f"Bearer {get_openclaw_token()}"},
                        json={"model": f"openclaw/{agent_id}", "messages": [{"role":"user","content":ctx}]}
                    )
                    d = r.json()
                    reply = d["choices"][0]["message"]["content"]
                # Extraheer actiepunten
                actions = []
                for line in reply.split("\n"):
                    if "[ACTIE:" in line:
                        actions.append(line.strip())
                responses.append({"agent_id": agent_id, "reply": reply, "ok": True, "actions": actions})
            except Exception as e:
                responses.append({"agent_id": agent_id, "reply": "Niet bereikbaar", "ok": False, "actions": []})

    # Verzamel alle actiepunten
    all_actions = [a for r in responses for a in r.get("actions", [])]
    return {"responses": responses, "ok": True, "actions": all_actions}


@router.post("/chat/meeting")
async def start_meeting(body: dict):
    """
    Start een gestructureerde meeting: agenda punt voor punt langs alle agents.
    Body: { agents: [], topic, agenda: [], channel_label }
    Elke agent geeft input op elk agenda punt.
    """
    agents_list = body.get("agents", [])
    topic = body.get("topic", "")
    agenda = body.get("agenda", [topic])
    channel_label = body.get("channel_label", "meeting")

    if not agents_list or not topic:
        raise HTTPException(400, "agents en topic verplicht")

    meeting_log = []
    async with httpx.AsyncClient(timeout=45) as client:
        for point in agenda[:4]:  # max 4 agenda punten
            point_responses = []
            for agent_id in agents_list[:5]:  # max 5 agents per punt
                try:
                    prompt = f"""[MEETING: {channel_label}]
[Onderwerp: {topic}]
[Huidig agendapunt: {point}]
[Deelnemers: {', '.join(agents_list)}]

Geef jouw input op dit agendapunt vanuit jouw rol. Wees specifiek en beknopt (2-3 zinnen). Noem concrete actiepunten als die relevant zijn."""
                    r = await client.post(
                        f"{OPENCLAW_GATEWAY}/v1/chat/completions",
                        headers={"Authorization": f"Bearer {get_openclaw_token()}"},
                        json={"model": f"openclaw/{agent_id}", "messages": [{"role": "user", "content": prompt}]}
                    )
                    d = r.json()
                    reply = d["choices"][0]["message"]["content"]
                    point_responses.append({"agent_id": agent_id, "reply": reply, "ok": True})
                except Exception as e:
                    point_responses.append({"agent_id": agent_id, "reply": "Niet bereikbaar", "ok": False})

            meeting_log.append({"point": point, "responses": point_responses})

    return {"topic": topic, "log": meeting_log, "ok": True}

# Agent rollen voor context
AGENT_ROLES = {
    "nova": "Consigliere — gateway en intake, spreekt namens Supreme Fea",
    "flux": "Underboss — orchestrator, neemt operationele besluiten",
    "cortexia": "Helix Lead — tech, systemen, infra, security, GitHub",
    "finoria": "Finix Lead — financien, trading, data, risicobeheer",
    "saelia": "Matrix Lead — data intelligence, research, archief, kennis",
    "lumeria": "Quantix Lead — analytics, forecasting, metrics, trends",
    "fluentia": "Zenix Lead — content, copy, SEO, social, email, brand",
    "nero": "Security Sentinel — bewaakt systeem integriteit",
    "forge": "GitHub Sentinel — code, repos, deployments",
    "axon": "Infra Sentinel — servers, netwerk, monitoring",
    "ventura": "Deploy Sentinel — releases, staging, productie",
    "clio": "Logging Sentinel — logs, audit trails, rapportage",
    "kairo": "Trading Sentinel — marktdata, signalen, posities",
    "kenzo": "Analytics Sentinel — data analyse, patronen",
    "odis": "DeFi Sentinel — decentralized finance protocollen",
    "vector": "Data Sentinel — datapijplijnen, kwaliteit",
    "zion": "Risk Sentinel — risicomodellen, exposure",
    "tharos": "Research Sentinel — diepgaand onderzoek",
    "sora": "Creative Sentinel — creatieve output, design",
    "arix": "Archive Sentinel — kennisarchief, documentatie",
    "enki": "Knowledge Sentinel — kennisbase, leren",
    "daxio": "Data Sentinel — datastromen, transformaties",
    "kresta": "Reports Sentinel — rapportages, dashboards",
    "elora": "Forecast Sentinel — voorspellingen, scenario analyses",
    "luvia": "Metrics Sentinel — KPIs, prestatiemeting",
    "nura": "Insights Sentinel — zakelijke inzichten",
    "vondra": "Trends Sentinel — markttrends, signalering",
    "draven": "Copy Sentinel — teksten, campagnes",
    "solis": "SEO Sentinel — zoekoptimalisatie, keywords",
    "orizon": "Social Sentinel — sociale media, engagement",
    "unia": "Email Sentinel — email marketing, automation",
    "zena": "Brand Sentinel — merkidentiteit, positionering",
}

CHAT_TYPES = {
    "core": "group",
    "leads": "council",
    "helix": "team", "finix": "team", "matrix": "team",
    "quantix": "team", "zenix": "team",
}

@router.post("/chat/group")
async def group_chat(body: dict):
    agents_list = body.get("agents", [])
    message = body.get("message", "")
    history = body.get("history", [])
    channel_label = body.get("channel_label", "groepsgesprek")
    channel_type = body.get("channel_type", "group")  # group|council|team
    sender_name = body.get("sender_name", "Supreme Fea")
    lead_agent = body.get("lead", agents_list[0] if agents_list else "nova")

    if not agents_list or not message:
        raise HTTPException(400, "agents en message verplicht")

    def build_history_str(all_history):
        lines = []
        for h in all_history[-14:]:
            who = "Supreme Fea" if h["from"] == "user" else h.get("name", h["from"])
            lines.append(f"{who}: {h['text']}")
        return "\n".join(lines) if lines else "(begin van gesprek)"

    def build_context(agent_id, msg, sender):
        role = AGENT_ROLES.get(agent_id, f"{agent_id} agent")
        hist = build_history_str(history)
        others = [a for a in agents_list if a != agent_id]
        other_names = ", ".join(others[:6])

        if channel_type == "council":
            return f"""[LEAD COUNCIL — {channel_label}]
[Jij bent: {agent_id.upper()} — {role}]
[Aanwezigen: {', '.join(agents_list)}]

[Gesprekshistorie:]
{hist}
{sender}: {msg}

Reageer als {agent_id} in deze council vergadering. Spreek vanuit jouw domein expertise. 
Richt je tot de relevante personen. Als Nova of Flux iets zegt neem dat mee.
Wees direct en zakelijk. Max 3 zinnen tenzij je een concreet punt te melden hebt.
Noem actiepunten als [ACTIE: beschrijving] als je concrete acties voorstelt."""

        elif channel_type == "team":
            is_lead = agent_id == lead_agent
            if is_lead:
                return f"""[TEAM BRIEFING — {channel_label}]
[Jij bent: {agent_id.upper()} — {role} — TEAM LEAD]
[Jouw team: {other_names}]

[Gesprekshistorie:]
{hist}
{sender}: {msg}

Als team lead reageer je op wat er gezegd is. Stuur het gesprek, geef richting aan je team.
Benoem wie wat moet doen. Wees besluitvaardig. Noem actiepunten als [ACTIE: agent: beschrijving]."""
            else:
                return f"""[TEAM BRIEFING — {channel_label}]
[Jij bent: {agent_id.upper()} — {role}]
[Team lead: {lead_agent}]
[Team: {', '.join(agents_list)}]

[Gesprekshistorie:]
{hist}
{sender}: {msg}

Reageer als {agent_id} vanuit jouw specifieke rol. Breng je domein-specifieke perspectief in.
Spreek je lead aan als relevant. Wees beknopt. Noem actiepunten als [ACTIE: beschrijving]."""

        else:  # group
            return f"""[GROEPSGESPREK — {channel_label}]
[Jij bent: {agent_id.upper()} — {role}]
[Anderen: {other_names}]

[Gesprekshistorie:]
{hist}
{sender}: {msg}

Reageer als jezelf. Spreek anderen direct aan. Wees natuurlijk en beknopt."""

    responses = []
    async with httpx.AsyncClient(timeout=45) as client:
        for agent_id in agents_list:
            try:
                ctx = build_context(agent_id, message, sender_name)
                model = get_agent_model(agent_id)
                # Lees system prompt
                sys_prompt = ""
                try:
                    ip = f"{AGENTS_DIR}/{agent_id}/IDENTITY.md"
                    if os.path.exists(ip):
                        sys_prompt = open(ip).read()[:1500]
                except: pass

                msgs = []
                if sys_prompt:
                    msgs.append({"role": "system", "content": sys_prompt})
                msgs.append({"role": "user", "content": ctx})

                # Probeer LiteLLM eerst
                litellm_ok = False
                try:
                    r2 = await client.post(
                        f"{LITELLM_URL}/v1/chat/completions",
                        headers={"Content-Type": "application/json"},
                        json={"model": model, "messages": msgs},
                        timeout=30
                    )
                    d2 = r2.json()
                    if "choices" in d2:
                        reply = d2["choices"][0]["message"]["content"]
                        litellm_ok = True
                except: pass

                if not litellm_ok:
                    r = await client.post(
                        f"{OPENCLAW_GATEWAY}/v1/chat/completions",
                        headers={"Authorization": f"Bearer {get_openclaw_token()}"},
                        json={"model": f"openclaw/{agent_id}", "messages": [{"role":"user","content":ctx}]}
                    )
                    d = r.json()
                    reply = d["choices"][0]["message"]["content"]
                # Extraheer actiepunten
                actions = []
                for line in reply.split("\n"):
                    if "[ACTIE:" in line:
                        actions.append(line.strip())
                responses.append({"agent_id": agent_id, "reply": reply, "ok": True, "actions": actions})
            except Exception as e:
                responses.append({"agent_id": agent_id, "reply": "Niet bereikbaar", "ok": False, "actions": []})

    # Verzamel alle actiepunten
    all_actions = [a for r in responses for a in r.get("actions", [])]
    return {"responses": responses, "ok": True, "actions": all_actions}


@router.post("/chat/meeting")
async def start_meeting(body: dict):
    """
    Start een gestructureerde meeting: agenda punt voor punt langs alle agents.
    Body: { agents: [], topic, agenda: [], channel_label }
    Elke agent geeft input op elk agenda punt.
    """
    agents_list = body.get("agents", [])
    topic = body.get("topic", "")
    agenda = body.get("agenda", [topic])
    channel_label = body.get("channel_label", "meeting")

    if not agents_list or not topic:
        raise HTTPException(400, "agents en topic verplicht")

    meeting_log = []
    async with httpx.AsyncClient(timeout=45) as client:
        for point in agenda[:4]:  # max 4 agenda punten
            point_responses = []
            for agent_id in agents_list[:5]:  # max 5 agents per punt
                try:
                    prompt = f"""[MEETING: {channel_label}]
[Onderwerp: {topic}]
[Huidig agendapunt: {point}]
[Deelnemers: {', '.join(agents_list)}]

Geef jouw input op dit agendapunt vanuit jouw rol. Wees specifiek en beknopt (2-3 zinnen). Noem concrete actiepunten als die relevant zijn."""
                    r = await client.post(
                        f"{OPENCLAW_GATEWAY}/v1/chat/completions",
                        headers={"Authorization": f"Bearer {get_openclaw_token()}"},
                        json={"model": f"openclaw/{agent_id}", "messages": [{"role": "user", "content": prompt}]}
                    )
                    d = r.json()
                    reply = d["choices"][0]["message"]["content"]
                    point_responses.append({"agent_id": agent_id, "reply": reply, "ok": True})
                except Exception as e:
                    point_responses.append({"agent_id": agent_id, "reply": "Niet bereikbaar", "ok": False})

            meeting_log.append({"point": point, "responses": point_responses})

    return {"topic": topic, "log": meeting_log, "ok": True}


@router.get("/models/live-status")
async def models_live_status():
    litellm_health = {}
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get("http://localhost:4000/health")
            h = r.json()
            for ep in h.get("healthy_endpoints", []):
                m = ep.get("model", ep.get("model_name", "?"))
                litellm_health[m] = "healthy"
            for ep in h.get("unhealthy_endpoints", []):
                m = ep.get("model", ep.get("model_name", "?"))
                litellm_health[m] = "unhealthy"
    except:
        pass

    agents_status = []
    for agent in AGENT_LIST:
        aid = agent["id"]
        config = get_agent_tier_config(aid)
        agents_status.append({
            "id": aid,
            "name": agent["name"],
            "domain": agent["domain"],
            "tier": config["tier"],
            "model": config["model"],
            "provider": config["provider"],
            "fallbacks": config["fallbacks"],
            "model_status": litellm_health.get(config["model"], "unknown"),
        })

    tier_summary = {
        "A": {"count": 0, "agents": [], "model": "arc-flux / arc-high", "provider": "Kimi K2.6"},
        "B": {"count": 0, "agents": [], "model": "arc-mid / arc-nova", "provider": "GPT-4o-mini"},
        "C": {"count": 0, "agents": [], "model": "arc-low", "provider": "Gemini Flash"},
    }
    for a in agents_status:
        t = a["tier"]
        if t in tier_summary:
            tier_summary[t]["count"] += 1
            tier_summary[t]["agents"].append(a["id"])

    return {"agents": agents_status, "tier_summary": tier_summary, "litellm_health": litellm_health, "ok": True}
