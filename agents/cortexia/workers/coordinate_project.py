#!/usr/bin/env python3
"""
coordinate_project.py — Cortexia worker
Vertaalt een project verzoek naar technische specs en taakverdeling
Gebruik: python3 coordinate_project.py "project-naam" "beschrijving" "features"
"""
import sys, json, os
from datetime import datetime

def coordinate_project(name, description, features_str):
    features = [f.strip() for f in features_str.split(',')]
    
    # Bepaal tech stack op basis van features
    needs_backend = any(f in features_str.lower() for f in ['login','auth','database','api','gebruiker','user','opslaan','save'])
    needs_db = any(f in features_str.lower() for f in ['database','opslaan','save','history','profiel'])
    
    specs = {
        "project_name": name.lower().replace(' ','-'),
        "description": description,
        "created_at": datetime.now().isoformat(),
        "frontend": "react" if len(features) > 4 else "html",
        "backend": "fastapi" if needs_backend else "none",
        "database": "sqlite" if needs_db else "none",
        "auth": "jwt" if needs_backend else "none",
        "features": features,
        "hosting": "vercel",
        "assigned_to": {
            "forge": "frontend" + (" + backend" if needs_backend else ""),
            "axon": "deploy pipeline" + (" + database" if needs_db else ""),
            "ventura": "vercel deploy + monitoring",
            "nero": "security audit",
            "clio": "readme + documentatie"
        },
        "workflow": [
            "1. Forge bouwt frontend" + (" + backend" if needs_backend else ""),
            "2. Axon configureert pipeline" + (" + database" if needs_db else ""),
            "3. Nero security audit",
            "4. Ventura deployt naar Vercel",
            "5. Clio schrijft documentatie",
            "6. Cortexia rapporteert live URL aan Flux"
        ]
    }
    
    # Sla specs op
    output_dir = f'/home/prime/arc_ai_angels/agents/forge/projects/{specs["project_name"]}'
    os.makedirs(output_dir, exist_ok=True)
    
    specs_file = f'{output_dir}/specs.json'
    with open(specs_file, 'w') as f:
        json.dump(specs, f, indent=2)
    
    print(f'✅ Project specs aangemaakt: {specs_file}')
    print(f'\nPROJECT: {name}')
    print(f'Stack: {specs["frontend"]} + {specs["backend"]} + {specs["database"]}')
    print(f'\nTAAKVERDELING:')
    for agent, taak in specs['assigned_to'].items():
        print(f'  {agent:<12} → {taak}')
    print(f'\nWORKFLOW:')
    for stap in specs['workflow']:
        print(f'  {stap}')
    
    return specs

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print('Gebruik: python3 coordinate_project.py "naam" "beschrijving" "feature1,feature2,feature3"')
        sys.exit(1)
    coordinate_project(sys.argv[1], sys.argv[2], sys.argv[3])
