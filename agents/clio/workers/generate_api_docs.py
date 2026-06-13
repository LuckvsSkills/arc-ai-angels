#!/usr/bin/env python3
import os, sys, re
def generate_api_docs(project_name):
    routes_dir = f'/home/prime/arc_ai_angels/agents/forge/projects/{project_name}/backend/routes'
    output_file = f'/home/prime/arc_ai_angels/agents/forge/projects/{project_name}/API.md'
    if not os.path.exists(routes_dir):
        print(f'❌ Geen routes voor {project_name}'); return
    docs = [f'# API Docs — {project_name}\n\nGegenereerd door Clio\n']
    for route_file in sorted(os.listdir(routes_dir)):
        if not route_file.endswith('.py'): continue
        route_name = route_file.replace('.py','')
        docs.append(f'\n## {route_name.capitalize()}\n')
        with open(f'{routes_dir}/{route_file}') as f: content = f.read()
        for method, path in re.findall(r'@router\.(get|post|put|delete)\("([^"]+)"', content):
            docs.append(f'### {method.upper()} /api{path}\n')
    with open(output_file,'w') as f: f.write('\n'.join(docs))
    print(f'✅ API docs: {output_file}')
if __name__=='__main__':
    generate_api_docs(sys.argv[1] if len(sys.argv)>1 else 'webshop-demo')
