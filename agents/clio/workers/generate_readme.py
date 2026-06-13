#!/usr/bin/env python3
import sys, os
def generate_readme(name, desc, tech, url=''):
    content = f"""# {name}\n\n{desc}\n\n## 🌐 Live\n{f'[{url}]({url})' if url else 'Pending'}\n\n## 🛠️ Tech Stack\n{chr(10).join([f'- {t.strip()}' for t in tech.split(',')])}\n\n## 🤖 Gebouwd door ARC AI Agents\nHelix domain — Cortexia, Forge, Axon, Ventura, Nero, Clio\n"""
    output = f'/home/prime/arc_ai_angels/agents/forge/projects/{name}/README.md'
    if os.path.exists(os.path.dirname(output)):
        with open(output,'w') as f: f.write(content)
        print(f'✅ README: {output}')
    else:
        print(content)
if __name__=='__main__':
    generate_readme(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4] if len(sys.argv)>4 else '')
