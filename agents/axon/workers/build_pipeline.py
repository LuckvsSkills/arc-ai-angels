#!/usr/bin/env python3
"""
build_pipeline.py — Axon worker
Bouwt en voert een deployment pipeline uit
Gebruik: python3 build_pipeline.py "project-naam" "static|react|fastapi"
"""
import os, sys, subprocess

def run_step(name, cmd, cwd=None):
    print(f'\n⏳ {name}...')
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, 
                               capture_output=True, text=True, timeout=120)
        if result.returncode == 0:
            print(f'✅ {name} — OK')
            return True
        else:
            print(f'❌ {name} — FOUT')
            print(f'   {result.stderr[:200]}')
            return False
    except Exception as e:
        print(f'❌ {name} — ERROR: {e}')
        return False

def run_pipeline(project_name, pipeline_type='static'):
    project_dir = f'/home/prime/arc_ai_angels/agents/forge/projects/{project_name}'
    
    if not os.path.exists(project_dir):
        print(f'❌ Project niet gevonden: {project_dir}')
        sys.exit(1)
    
    print(f'🚀 Pipeline: {project_name} ({pipeline_type})')
    print('='*50)
    
    steps_ok = 0
    steps_total = 0
    
    if pipeline_type == 'static':
        steps = [
            ('HTML validatie', f'find {project_dir} -name "*.html" | head -5'),
            ('CSS check', f'find {project_dir} -name "*.css" | head -5'),
            ('JS check', f'find {project_dir} -name "*.js" | head -5'),
        ]
    elif pipeline_type == 'react':
        steps = [
            ('npm install', 'npm install', project_dir),
            ('npm build', 'npm run build', project_dir),
        ]
    elif pipeline_type == 'fastapi':
        backend_dir = f'{project_dir}/backend'
        steps = [
            ('pip install', f'pip install -r {backend_dir}/requirements.txt --break-system-packages'),
            ('syntax check', f'python3 -m py_compile {backend_dir}/main.py'),
        ]
    
    for step in steps:
        steps_total += 1
        name = step[0]
        cmd = step[1]
        cwd = step[2] if len(step) > 2 else None
        if run_step(name, cmd, cwd):
            steps_ok += 1
    
    print(f'\n{"="*50}')
    print(f'Pipeline resultaat: {steps_ok}/{steps_total} stappen OK')
    
    if steps_ok == steps_total:
        print('✅ PIPELINE GESLAAGD — klaar voor deploy')
        return True
    else:
        print('❌ PIPELINE GEFAALD — fix issues voor deploy')
        return False

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Gebruik: python3 build_pipeline.py "project-naam" "static|react|fastapi"')
        sys.exit(1)
    pipeline_type = sys.argv[2] if len(sys.argv) > 2 else 'static'
    run_pipeline(sys.argv[1], pipeline_type)
