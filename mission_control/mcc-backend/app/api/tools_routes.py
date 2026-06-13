from fastapi import APIRouter
import json, os
from app.config import MCC_DIR

router = APIRouter()
TOOLS_FILE = f"{MCC_DIR}/tools_api.json"

def load_tools():
    if os.path.exists(TOOLS_FILE):
        return json.load(open(TOOLS_FILE))
    return {"tools": [], "domains": []}

@router.get("/tools")
async def get_tools():
    d = load_tools()
    return {"tools": d["tools"], "total": len(d["tools"])}

@router.get("/tools/domains")
async def get_tools_domains():
    d = load_tools()
    for dom in d["domains"]:
        dom_tools = [t for t in d["tools"] if any(a in t["usedBy"] for a in dom["agents"])]
        dom["tools_detail"] = dom_tools
        dom["tool_count"] = len(dom_tools)
        dom["active_count"] = len([t for t in dom_tools if t["status"]=="active"])
        dom["wanted_count"] = len([t for t in dom_tools if t["status"]=="wanted"])
    return {"domains": d["domains"]}

@router.get("/tools/agents")
async def get_tools_agents():
    d = load_tools()
    result = {}
    for tool in d["tools"]:
        for agent in tool["usedBy"]:
            if agent not in result:
                result[agent] = []
            result[agent].append({"id":tool["id"],"name":tool["name"],"category":tool["category"],"status":tool["status"]})
    return {"agents": result, "total_agents": len(result)}
