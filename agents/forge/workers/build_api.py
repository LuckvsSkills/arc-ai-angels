#!/usr/bin/env python3
"""
build_api.py — Forge worker
Genereert een FastAPI backend structuur
Gebruik: python3 build_api.py "project-naam" "endpoint1,endpoint2"
"""
import os, sys

def build_api(project_name, endpoints_str):
    endpoints = [e.strip() for e in endpoints_str.split(',')]
    base_dir = f'/home/prime/arc_ai_angels/agents/forge/projects/{project_name}/backend'
    os.makedirs(f'{base_dir}/routes', exist_ok=True)

    # main.py
    with open(f'{base_dir}/main.py', 'w') as f:
        f.write(f'''from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
{"".join([f"from routes import {e}" + chr(10) for e in endpoints])}

app = FastAPI(title="{project_name} API", version="1.0.0")

app.add_middleware(CORSMiddleware,
    allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

{"".join([f"app.include_router({e}.router, prefix=" + '"/api"' + ")" + chr(10) for e in endpoints])}

@app.get("/health")
async def health():
    return {{"status": "ok", "project": "{project_name}"}}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
''')

    # Routes per endpoint
    for endpoint in endpoints:
        with open(f'{base_dir}/routes/{endpoint}.py', 'w') as f:
            f.write(f'''from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List

router = APIRouter()

class {endpoint.capitalize()}(BaseModel):
    id: int = None
    name: str
    description: str = ""

db = []

@router.get("/{endpoint}", response_model=List[{endpoint.capitalize()}])
async def get_{endpoint}():
    return db

@router.post("/{endpoint}", response_model={endpoint.capitalize()})
async def create_{endpoint}(item: {endpoint.capitalize()}):
    item.id = len(db) + 1
    db.append(item)
    return item
''')

    # requirements.txt
    with open(f'{base_dir}/requirements.txt', 'w') as f:
        f.write('fastapi==0.115.0\nuvicorn==0.32.0\npydantic==2.9.0\npython-dotenv==1.0.1\n')

    print(f'✅ API gebouwd: {base_dir}')
    print(f'Endpoints: {", ".join([f"/api/{e}" for e in endpoints])}')
    print(f'\nStarten: cd {base_dir} && pip install -r requirements.txt && python3 main.py')
    return base_dir

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Gebruik: python3 build_api.py "project-naam" "users,products,orders"')
        sys.exit(1)
    build_api(sys.argv[1], sys.argv[2])
