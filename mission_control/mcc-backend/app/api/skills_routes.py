from fastapi import APIRouter
import json, os
router = APIRouter()

SKILLS_FILE = "/home/prime/arc_ai_angels/MCC/skills_api.json"

def load_skills():
    if os.path.exists(SKILLS_FILE):
        return json.load(open(SKILLS_FILE))
    return {"skills": [], "domains": [], "catalog": {}}

@router.get("/skills")
async def get_skills():
    d = load_skills()
    return {"skills": d["skills"], "total": len(d["skills"]), "catalog": d.get("catalog", {})}

@router.get("/skills/domains")
async def get_skills_domains():
    d = load_skills()
    return {"domains": d["domains"]}

@router.get("/skills/agents")
async def get_skills_agents():
    d = load_skills()
    result = {}
    for skill in d["skills"]:
        for agent in skill["usedBy"]:
            if agent not in result:
                result[agent] = []
            result[agent].append({
                "id": skill["id"],
                "name": skill["name"],
                "category": skill["category"],
                "source": skill["source"]
            })
    return {"agents": result, "total_agents": len(result)}

@router.get("/skills/agent/{agent_id}")
async def get_agent_skills(agent_id: str):
    d = load_skills()
    skills = [s for s in d["skills"] if agent_id in s["usedBy"]]
    return {"agent": agent_id, "skills": skills, "total": len(skills)}
