#!/usr/bin/env python3
"""
coordinate_finance.py — Finoria Worker
Coördineert financiële taken binnen het Finix-domein.
Verdeelt werk naar de juiste Finix Sentinels op basis van taaktype.
"""
import json
import os
from datetime import datetime
from pathlib import Path

FINIX_SENTINELS = {
    'treasury': 'kairo',
    'controls': 'kenzo',
    'accounting': 'zion',
    'audit': 'odis',
}

AGENTS_DIR = Path('/home/prime/arc_ai_angels/agents')
LOG_DIR = Path('/home/prime/arc_ai_angels/logs')

def log(msg):
    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f'[{ts}] [Finoria] {msg}')

def route_task(task: dict) -> str:
    """Bepaal welke sentinel de taak moet uitvoeren."""
    taaktype = task.get('type', '').lower()
    for domein, agent in FINIX_SENTINELS.items():
        if domein in taaktype:
            return agent
    return None

def load_tasks() -> list:
    """Laad openstaande financiële taken."""
    tasks_file = AGENTS_DIR / 'finoria' / 'TASKS.md'
    if not tasks_file.exists():
        return []
    tasks = []
    with open(tasks_file) as f:
        for line in f:
            if line.strip().startswith('- [') and 'status: scheduled' in line.lower():
                tasks.append({'raw': line.strip(), 'type': line.strip()})
    return tasks

def generate_finance_report() -> dict:
    """Genereer een overzicht van de Finix-domain status."""
    report = {
        'timestamp': datetime.now().isoformat(),
        'domain': 'finix/finance',
        'lead': 'finoria',
        'sentinels': {},
    }
    for domein, agent in FINIX_SENTINELS.items():
        memory_file = AGENTS_DIR / agent / 'MEMORY.md'
        tasks_file = AGENTS_DIR / agent / 'TASKS.md'
        report['sentinels'][agent] = {
            'specialisme': domein,
            'memory_aanwezig': memory_file.exists(),
            'tasks_aanwezig': tasks_file.exists(),
        }
    return report

def main():
    log('Finoria finance-coördinatie gestart')
    LOG_DIR.mkdir(exist_ok=True)

    # Genereer domain-rapport
    rapport = generate_finance_report()
    rapport_path = LOG_DIR / 'finix_domain_status.json'
    with open(rapport_path, 'w') as f:
        json.dump(rapport, f, indent=2, ensure_ascii=False)
    log(f'Domain-rapport opgeslagen: {rapport_path}')

    # Laad en route taken
    taken = load_tasks()
    log(f'{len(taken)} openstaande taken gevonden')
    for taak in taken:
        sentinel = route_task(taak)
        if sentinel:
            log(f'Taak gerouteerd naar {sentinel}: {taak["raw"][:60]}...')
        else:
            log(f'Geen routing gevonden voor taak: {taak["raw"][:60]}...')

    log('Finoria finance-coördinatie klaar')
    return rapport

if __name__ == '__main__':
    main()
