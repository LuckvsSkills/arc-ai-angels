#!/usr/bin/env python3
"""coordinate_intelligence.py — Saelia Worker
Coördineert intelligence-taken binnen het Matrix-domein."""
import json
from datetime import datetime
from pathlib import Path

MATRIX_SENTINELS = {
    'research': 'arix',
    'signals': 'daxio',
    'knowledge': 'enki',
    'synthesis': 'sora',
    'strategic': 'tharos',
}
LOG_DIR = Path('/home/prime/arc_ai_angels/logs')

def log(msg):
    print(f'[{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] [Saelia] {msg}')

def generate_domain_report() -> dict:
    agents_dir = Path('/home/prime/arc_ai_angels/agents')
    report = {
        'timestamp': datetime.now().isoformat(),
        'domain': 'matrix/intelligence',
        'lead': 'saelia',
        'sentinels': {agent: {'specialisme': spec, 'actief': (agents_dir / agent / 'IDENTITY.md').exists()}
                      for spec, agent in MATRIX_SENTINELS.items()}
    }
    return report

def main():
    log('Saelia intelligence-coördinatie gestart')
    LOG_DIR.mkdir(exist_ok=True)
    rapport = generate_domain_report()
    pad = LOG_DIR / 'matrix_domain_status.json'
    with open(pad, 'w') as f:
        json.dump(rapport, f, indent=2, ensure_ascii=False)
    log(f'Domain-rapport opgeslagen: {pad}')
    log('Saelia intelligence-coördinatie klaar')

if __name__ == '__main__':
    main()
