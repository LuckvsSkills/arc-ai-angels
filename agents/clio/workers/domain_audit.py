#!/usr/bin/env python3
import os
from datetime import datetime
agents_dir = '/home/prime/arc_ai_angels/agents'
helix = ['cortexia','nero','forge','axon','ventura','clio']
required = ['IDENTITY.md','SOUL.md','TOOLS.md','WORKFLOW.md','MEMORY.md','TASKS.md','MODEL.md']
print(f'🔎 CLIO DOMEIN AUDIT — {datetime.now().strftime("%Y-%m-%d")}')
print('='*50)
gaps = []
for agent in helix:
    d = f'{agents_dir}/{agent}'
    missing = [f for f in required if not os.path.exists(f'{d}/{f}')]
    has_w = os.path.exists(f'{d}/workers') and len(os.listdir(f'{d}/workers')) > 0
    has_s = os.path.exists(f'{d}/skills') and len(os.listdir(f'{d}/skills')) > 0
    ok = not missing and has_w and has_s
    print(f'\n{"✅" if ok else "⚠️ "} {agent.upper()}')
    print(f'   MD: {len(required)-len(missing)}/{len(required)} | Workers: {"✅" if has_w else "❌"} | Skills: {"✅" if has_s else "❌"}')
    if missing: gaps.append(f'{agent}: {", ".join(missing)}')
print(f'\n{"="*50}')
print('✅ COMPLEET' if not gaps else f'⚠️  {len(gaps)} gaps: {gaps}')
