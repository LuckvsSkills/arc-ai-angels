#!/usr/bin/env python3
"""
scan_template_security.py — Nero worker
Security gate scan voor website builds op basis van PROJECT_BRIEF.json
Gebruik: python3 scan_template_security.py /pad/naar/PROJECT_BRIEF.json
"""
import os, sys, json, re
from datetime import datetime

CRITICAL_PATTERNS = [
    (r'sk_live_[a-zA-Z0-9]+', 'Stripe live secret key'),
    (r'sk_test_[a-zA-Z0-9]{20,}', 'Stripe test key (hardcoded)'),
    (r'ghp_[a-zA-Z0-9]+', 'GitHub token'),
    (r'password\s*=\s*["\'][^"\']{4,}["\']', 'Hardcoded password'),
    (r'secret\s*=\s*["\'][^"\']{4,}["\']', 'Hardcoded secret'),
    (r'api_key\s*=\s*["\'][^"\']{8,}["\']', 'Hardcoded API key'),
    (r'Bearer\s+[a-zA-Z0-9\-_]{20,}', 'Hardcoded Bearer token'),
]

WARNING_PATTERNS = [
    (r'eval\s*\(', 'eval() gebruik — XSS risico'),
    (r'innerHTML\s*=', 'innerHTML assignment — XSS risico'),
    (r'SELECT\s+\*\s+FROM.*\+', 'Mogelijk SQL injection'),
    (r'os\.system\s*\(', 'os.system() — command injection risico'),
    (r'subprocess\.call.*shell=True', 'shell=True — injection risico'),
    (r'DEBUG\s*=\s*True', 'Debug mode aan in productie'),
    (r'ALLOWED_HOSTS\s*=\s*\[.*\*.*\]', 'ALLOWED_HOSTS te breed'),
]

REQUIRED_SECURITY = [
    ('CORS', ['CORSMiddleware', 'cors']),
    ('Auth', ['jwt', 'JWT', 'authenticate', 'auth_required', 'Depends']),
    ('Rate limiting', ['slowapi', 'RateLimiter', 'rate_limit']),
    ('Security headers', ['X-Frame-Options', 'X-Content-Type', 'helmet']),
]

def log(msg):
    ts = datetime.now().strftime('%H:%M:%S')
    print(f'[{ts}] {msg}')

def load_brief(path):
    with open(path) as f:
        return json.load(f)

def scan_directory(code_dir):
    critical = []
    warnings = []
    files_scanned = 0

    for root, dirs, files in os.walk(code_dir):
        dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules', '__pycache__', '.env']]
        for fname in files:
            if not fname.endswith(('.py', '.js', '.jsx', '.ts', '.tsx', '.env.example', '.sh')):
                continue
            fpath = os.path.join(root, fname)
            try:
                with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                files_scanned += 1
                rel_path = os.path.relpath(fpath, code_dir)

                for pattern, desc in CRITICAL_PATTERNS:
                    matches = re.findall(pattern, content, re.IGNORECASE)
                    if matches:
                        critical.append({
                            'bestand': rel_path,
                            'type': 'KRITIEK',
                            'beschrijving': desc,
                            'matches': len(matches)
                        })

                for pattern, desc in WARNING_PATTERNS:
                    matches = re.findall(pattern, content, re.IGNORECASE)
                    if matches:
                        warnings.append({
                            'bestand': rel_path,
                            'type': 'WARNING',
                            'beschrijving': desc,
                            'matches': len(matches)
                        })
            except Exception:
                pass

    return critical, warnings, files_scanned

def check_security_features(code_dir):
    aanwezig = []
    ontbreekt = []

    all_content = ''
    for root, dirs, files in os.walk(code_dir):
        dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules', '__pycache__']]
        for fname in files:
            if fname.endswith(('.py', '.js', '.jsx', '.ts', '.tsx')):
                try:
                    with open(os.path.join(root, fname), 'r', encoding='utf-8', errors='ignore') as f:
                        all_content += f.read()
                except: pass

    for feature, indicators in REQUIRED_SECURITY:
        if any(ind in all_content for ind in indicators):
            aanwezig.append(feature)
        else:
            ontbreekt.append(feature)

    return aanwezig, ontbreekt

def check_env_files(code_dir):
    issues = []
    env_path = os.path.join(code_dir, '.env')
    if os.path.exists(env_path):
        issues.append('KRITIEK: .env bestand aanwezig in code directory — mag niet in repo!')
    gitignore_path = os.path.join(code_dir, '.gitignore')
    if os.path.exists(gitignore_path):
        with open(gitignore_path) as f:
            content = f.read()
        if '.env' not in content:
            issues.append('WARNING: .env staat niet in .gitignore')
    else:
        issues.append('WARNING: geen .gitignore aanwezig')
    return issues

def determine_status(critical, warnings, env_issues):
    kritiek_count = len(critical) + len([i for i in env_issues if 'KRITIEK' in i])
    if kritiek_count > 0:
        return 'ROOD', '🔴'
    elif len(warnings) > 3:
        return 'GEEL', '🟡'
    else:
        return 'GROEN', '🟢'

def generate_rapport(brief, critical, warnings, features_ok, features_missing, env_issues, status, status_emoji, files_scanned, scan_dir):
    naam = brief['project_naam']
    ts = datetime.now().strftime('%Y-%m-%d %H:%M')

    rapport = f"""# Security Rapport — {naam}
**Datum:** {ts}
**Status:** {status_emoji} {status}
**Bestanden gescand:** {files_scanned}

---

## Samenvatting

| Check | Resultaat |
|-------|-----------|
| Kritieke issues | {len(critical)} |
| Warnings | {len(warnings)} |
| Security features aanwezig | {', '.join(features_ok) if features_ok else 'Geen'} |
| Security features ontbreekt | {', '.join(features_missing) if features_missing else 'Geen'} |
| Deploy | {'✅ GOEDGEKEURD' if status == 'GROEN' else '🟡 CONDITIE' if status == 'GEEL' else '❌ GEBLOKKEERD'} |

---
"""
    if critical:
        rapport += "## Kritieke Issues — VERPLICHT OPLOSSEN\n\n"
        for issue in critical:
            rapport += f"**{issue['bestand']}**\n"
            rapport += f"- Type: {issue['beschrijving']}\n"
            rapport += f"- Gevonden: {issue['matches']}x\n\n"

    if warnings:
        rapport += "## Warnings\n\n"
        for w in warnings[:5]:
            rapport += f"- **{w['bestand']}**: {w['beschrijving']}\n"

    if env_issues:
        rapport += "\n## Environment Issues\n\n"
        for issue in env_issues:
            rapport += f"- {issue}\n"

    if features_missing:
        rapport += f"\n## Ontbrekende Security Features\n\n"
        for f in features_missing:
            rapport += f"- {f} — implementeer voor deploy\n"

    rapport += f"""
---

## Advies

{'⛔ Deploy GEBLOKKEERD. Los alle kritieke issues op voor deploy.' if status == 'ROOD' else '⚠️ Deploy mogelijk maar fix warnings.' if status == 'GEEL' else '✅ Deploy goedgekeurd. Geen kritieke issues gevonden.'}

*Rapport door Nero — ARC AI Agents Security*
"""
    rapport_path = f'{scan_dir}/SECURITY_RAPPORT.md'
    with open(rapport_path, 'w') as f:
        f.write(rapport)
    return rapport_path

def update_brief(brief_path, brief, status, rapport_path, critical, warnings):
    brief['security'] = {
        'status': status,
        'kritieke_issues': len(critical),
        'warnings': len(warnings),
        'rapport': rapport_path,
        'gescand_op': datetime.now().isoformat(),
        'deploy_goedgekeurd': status in ['GROEN', 'GEEL']
    }
    brief['sentinels']['nero'] = status
    with open(brief_path, 'w') as f:
        json.dump(brief, f, indent=2, ensure_ascii=False)

def main():
    if len(sys.argv) < 2:
        print('Gebruik: python3 scan_template_security.py /pad/naar/PROJECT_BRIEF.json')
        sys.exit(1)

    brief_path = sys.argv[1]
    brief = load_brief(brief_path)
    project_dir = os.path.dirname(brief_path)
    code_dir = brief.get('code_dir', f'{project_dir}/code')

    if not os.path.exists(code_dir):
        log(f'⚠️  code_dir niet gevonden: {code_dir} — basis scan uitvoeren')
        code_dir = project_dir

    log(f'🔍 Security scan: {brief["project_naam"]}')
    log(f'   Directory: {code_dir}')

    critical, warnings, files_scanned = scan_directory(code_dir)
    features_ok, features_missing = check_security_features(code_dir)
    env_issues = check_env_files(code_dir)
    status, emoji = determine_status(critical, warnings, env_issues)

    log(f'   Bestanden gescand: {files_scanned}')
    log(f'   Kritieke issues: {len(critical)}')
    log(f'   Warnings: {len(warnings)}')
    log(f'   Status: {emoji} {status}')

    rapport_path = generate_rapport(brief, critical, warnings, features_ok, features_missing, env_issues, status, emoji, files_scanned, project_dir)
    update_brief(brief_path, brief, status, rapport_path, critical, warnings)

    print('\n' + '='*50)
    print(f'{"✅" if status == "GROEN" else "⚠️" if status == "GEEL" else "❌"} NERO SECURITY GATE: {status}')
    print(f'   Kritiek: {len(critical)} | Warnings: {len(warnings)}')
    print(f'   Deploy: {"GOEDGEKEURD" if status in ["GROEN","GEEL"] else "GEBLOKKEERD"}')
    print(f'   Rapport: {rapport_path}')
    print('='*50)

if __name__ == '__main__':
    main()
