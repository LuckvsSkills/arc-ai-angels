from fastapi import APIRouter, HTTPException
import json, os
from app.config import BASE_DIR

router = APIRouter()
DIAGRAMS_FILE = f"{BASE_DIR}/MCC/diagrams.json"

def load_diagrams():
    if os.path.exists(DIAGRAMS_FILE):
        return json.load(open(DIAGRAMS_FILE))
    return {"diagrams": []}

@router.get("/diagrams/")
async def get_diagrams():
    d = load_diagrams()
    return d

@router.get("/diagrams/{diagram_id}")
async def get_diagram(diagram_id: str):
    d = load_diagrams()
    diag = next((x for x in d["diagrams"] if str(x["id"])==str(diagram_id)), None)
    if not diag: raise HTTPException(404, "Diagram niet gevonden")
    return diag
