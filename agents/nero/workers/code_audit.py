#!/usr/bin/env python3
"""
code_audit.py — Nero worker
Basis security scan op een project directory
Gebruik: python3 code_audit.py /pad/naar/project
"""
import os, sys, re

PATTERNS = [
    (r'password\s*=\s*["\'][^"\']+["\']', '🔴 KRITIEK', 'Hardcoded wachtwoord gevonden'),
    (r'api_key\s*=\s*["\'][^"\']+["\']', '🔴 KRITIEK', 'Hardcoded API key gevonden'),
    (r'secret\s*=\s*["\'][^"\']+["\']', '🔴 KRITIEK', 'Hardcoded secret gevonden'),
    (r'eval\(', '🟠 HOOG', 'eval() gebruik — code injection risico'),
    (r'exec\(', '🟠 HOOG', 'exec() gebruik — code injection risico'),
    (r'innerHTML\s*=', '🟠 HOOG', 'innerHTML — XSS risico'),
    (r'dangerouslySetInnerHTML', '🟠 HOOG', 'dangerouslySetInnerHTML — XSS risico'),
    (r'console\.log\(', '🟢 LAAG', 'console.log() in productie code'),
    (r'TODO|FIXME|HACK', '🟡 MEDIUM', 'Onafgemaakte code gevonden'),
    (r'http://', '🟡 MEDIUM', 'HTTP in plaats van HTTPS'),
]

def audit_file(filepath):
    findings = []
    try:
        with open(filepath, 'r', errors='ignore') as f:
            content = f.read()
            for pattern, severity, message in PATTERNS:
                matches = re.findall(pattern, content, re.IGNORECASE)
                if matches:
                    findings.append((severity, message, filepath))
    except:
        pass
    return findings

def audit_project(project_dir):
    print(f'🔍 Code Security Audit: {project_dir}')
    print('='*50)
    
    all_findings = []
    extensions = ['.py', '.js', '.jsx', '.ts', '.tsx', '.html', '.env']
    
    for root, dirs, files in os.walk(project_dir):
        dirs[:] = [d for d in dirs if d not in ['node_modules', '.git', '__pycache__']]
        for file in files:
            if any(file.endswith(ext) for ext in extensions):
                filepath = os.path.join(root, file)
                findings = audit_file(filepath)
                all_findings.extend(findings)
    
    critical = [f for f in all_findings if '🔴' in f[0]]
    high     = [f for f in all_findings if '🟠' in f[0]]
    medium   = [f for f in all_findings if '🟡' in f[0]]
    low      = [f for f in all_findings if '🟢' in f[0]]
    
    for severity, msg, filepath in critical:
        print(f'{severity} {msg}\n   in: {filepath}')
    for severity, msg, filepath in high:
        print(f'{severity} {msg}\n   in: {filepath}')
    for severity, msg, filepath in medium:
        print(f'{severity} {msg}\n   in: {filepath}')
    
    print(f'\n{"="*50}')
    verdict = 'BLOCKED' if critical else 'APPROVED' if not high else 'APPROVED MET OPMERKINGEN'
    print(f'CONCLUSIE: {verdict}')
    print(f'Kritiek: {len(critical)} | Hoog: {len(high)} | Medium: {len(medium)} | Laag: {len(low)}')
    return verdict

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Gebruik: python3 code_audit.py /pad/naar/project')
        sys.exit(1)
    audit_project(sys.argv[1])
