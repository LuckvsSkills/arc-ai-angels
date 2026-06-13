---
name: api-builder
description: "Bouw REST APIs met FastAPI voor ARC AI Agents projecten."
metadata: { "openclaw": { "emoji": "⚡" } }
---
# API Builder

Gebruik deze skill voor het bouwen van FastAPI backends.

## Standaard FastAPI structuur
```python
# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import items

app = FastAPI(title="Project API", version="1.0.0")

app.add_middleware(CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"])

app.include_router(items.router, prefix="/api")

@app.get("/health")
async def health():
    return {"status": "ok"}
```

## CRUD endpoint template
```python
# routes/items.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List

router = APIRouter()

class Item(BaseModel):
    id: int = None
    name: str
    description: str = ""

items_db = []

@router.get("/items", response_model=List[Item])
async def get_items():
    return items_db

@router.post("/items", response_model=Item)
async def create_item(item: Item):
    item.id = len(items_db) + 1
    items_db.append(item)
    return item

@router.get("/items/{item_id}")
async def get_item(item_id: int):
    item = next((i for i in items_db if i.id == item_id), None)
    if not item:
        raise HTTPException(404, "Item niet gevonden")
    return item
```

## Requirements.txt template
fastapi==0.115.0
uvicorn==0.32.0
pydantic==2.9.0
python-dotenv==1.0.1

## Starten
```bash
pip install -r requirements.txt
uvicorn main:app --reload --port 8001
```
