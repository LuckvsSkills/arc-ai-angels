#!/usr/bin/env python3
"""
monitor_live_site.py — Ventura worker
Monitort live website status, uptime en performance
Gebruik: python3 monitor_live_site.py /pad/naar/PROJECT_BRIEF.json
         python3 monitor_live_site.py --all (monitor alle bekende sites)
"""
import os, sys, json, urllib.request, urllib.error, time
from datetime import datetime

BUILDS_DIR = '/home/prime/arc_ai_angels/projects/website_builds'

def log(msg):
    ts = datetime.now().strftime('%H:%M:%S')
    print(f'[{ts}] {msg}')

def check_site(url, timeout=10):
    start = time.time()
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'ARC-AI-Angels-Monitor/1.0'})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            status = resp.status
            elapsed = int((time.time() - start) * 1000)
            return {'url': url, 'status': status, 'ms': elapsed, 'ok': status == 200}
    except urllib.error.HTTPError as e:
        return {'url': url, 'status': e.code, 'ms': -1, 'ok': False, 'error': str(e)}
    except Exception as e:
        return {'url': url, 'status': 0, 'ms': -1, 'ok': False, 'error': str(e)[:50]}

def monitor_brief(brief_path):
    with open(brief_path) as f:
        brief = json.load(f)
    naam = brief['project_naam']
    deploy = brief.get('deploy', {})
    url = deploy.get('url', '')
    if not url:
        return None
    log(f'🔍 Check: {naam} — {url}')
    result = check_site(url)
    status_icon = '✅' if result['ok'] else '❌'
    log(f'   {status_icon} HTTP {result["status"]} — {result["ms"]}ms')
    return {'naam': naam, 'url': url, **result}

def monitor_all():
    results = []
    for d in os.listdir(BUILDS_DIR):
        brief_path = f'{BUILDS_DIR}/{d}/PROJECT_BRIEF.json'
        if os.path.exists(brief_path):
            r = monitor_brief(brief_path)
            if r:
                results.append(r)
    return results

def monitor_arc_system():
    services = [
        ('OpenClaw', 'http://localhost:50506'),
        ('LiteLLM', 'http://localhost:4000'),
        ('MCC Backend', 'http://localhost:8000'),
        ('MCC Frontend', 'http://localhost:3002'),
    ]
    results = []
    for naam, url in services:
        r = check_site(url, timeout=5)
        status_icon = '✅' if r['ok'] else '❌'
        log(f'   {status_icon} {naam}: HTTP {r["status"]} — {r["ms"]}ms')
        results.append({'naam': naam, 'url': url, **r})
    return results

def main():
    if len(sys.argv) > 1 and sys.argv[1] == '--all':
        log('🔍 Monitor alle actieve sites + ARC systeem')
        print('\n=== ARC SYSTEEM ===')
        sys_results = monitor_arc_system()
        print('\n=== LIVE SITES ===')
        site_results = monitor_all()
        all_ok = all(r['ok'] for r in sys_results + site_results)
        print('\n' + '='*50)
        print(f'{"✅" if all_ok else "⚠️"} MONITOR RAPPORT')
        print(f'   Systeem: {sum(1 for r in sys_results if r["ok"])}/{len(sys_results)} online')
        print(f'   Sites: {sum(1 for r in site_results if r["ok"])}/{len(site_results)} online')
        print('='*50)
    elif len(sys.argv) > 1:
        result = monitor_brief(sys.argv[1])
        if result:
            print('\n' + '='*50)
            print(f'{"✅" if result["ok"] else "❌"} SITE STATUS')
            print(f'   URL: {result["url"]}')
            print(f'   HTTP: {result["status"]}')
            print(f'   Laadtijd: {result["ms"]}ms')
            print('='*50)
    else:
        print('Gebruik: python3 monitor_live_site.py /pad/PROJECT_BRIEF.json')
        print('         python3 monitor_live_site.py --all')

if __name__ == '__main__':
    main()
