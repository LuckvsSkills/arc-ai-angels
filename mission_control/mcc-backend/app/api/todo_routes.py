from fastapi import APIRouter, HTTPException
import json, os, uuid
from datetime import datetime

router = APIRouter()
TODO_FILE = os.path.expanduser("~/.mcc_todos.json")

def load_todos():
    if os.path.exists(TODO_FILE):
        d = json.load(open(TODO_FILE))
        if isinstance(d, list): return {"items": d}
        return d
    return {"items": []}

def save_todos(data):
    json.dump(data, open(TODO_FILE,"w"), indent=2)

@router.get("/todo/items")
async def get_todos():
    return load_todos()

@router.post("/todo/items")
async def create_todo(body: dict):
    data = load_todos()
    item = {"id": str(uuid.uuid4())[:8], "title": body.get("title",""),
            "priority": body.get("priority","P3"), "status": body.get("status","open"),
            "created_at": datetime.now().isoformat()}
    data["items"].append(item)
    save_todos(data)
    return item

@router.put("/todo/{todo_id}")
async def update_todo(todo_id: str, body: dict):
    data = load_todos()
    item = next((i for i in data["items"] if i["id"]==todo_id), None)
    if not item: raise HTTPException(404, "Todo niet gevonden")
    item.update({k:v for k,v in body.items() if k in ["title","status","priority"]})
    save_todos(data)
    return item

@router.delete("/todo/{todo_id}")
async def delete_todo(todo_id: str):
    data = load_todos()
    data["items"] = [i for i in data["items"] if i["id"]!=todo_id]
    save_todos(data)
    return {"deleted": True}
