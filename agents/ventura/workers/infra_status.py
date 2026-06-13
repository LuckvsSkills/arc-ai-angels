#!/usr/bin/env python3
import subprocess, socket, shutil
from datetime import datetime

def check_port(port):
    try:
        s = socket.socket(); s.settimeout(2)
        result = s.connect_ex(('127.0.0.1', port)); s.close()
        return result == 0
    except: return False

print(f'🏗️  VENTURA INFRA STATUS — {datetime.now().strftime("%Y-%m-%d %H:%M")}')
services = [('OpenClaw',50506),('LiteLLM',4000),('MCC Backend',8000),('Vite',3002)]
for name, port in services:
    ok = check_port(port)
    print(f'  {"✅" if ok else "❌"} {name:<20} poort {port}')
disk = shutil.disk_usage('/home/prime')
used = (disk.used/disk.total)*100
print(f'\n  💾 Disk: {used:.1f}% gebruikt')
