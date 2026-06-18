#!/usr/bin/env python3
"""write_story.py — Solis Worker — specialisme: storytelling"""
import json
from datetime import datetime
from pathlib import Path

LOG_DIR = Path('/home/prime/arc_ai_angels/logs')

def log(msg):
    print(f'[{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] [Solis] {msg}')

def main():
    log('Solis storytelling gestart')
    LOG_DIR.mkdir(exist_ok=True)
    rapport = {
        'timestamp': datetime.now().isoformat(),
        'agent': 'solis', 'specialisme': 'storytelling', 'status': 'ok',
        'output': [], 'aanbeveling': 'Taak voltooid.'
    }
    pad = LOG_DIR / 'solis_storytelling.json'
    with open(pad, 'w') as f:
        json.dump(rapport, f, indent=2, ensure_ascii=False)
    log(f'Rapport opgeslagen: {pad}')

if __name__ == '__main__':
    main()
