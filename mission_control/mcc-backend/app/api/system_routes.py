from fastapi import APIRouter
import subprocess, psutil, os

router = APIRouter()

SERVICES = {
    'openclaw': {
        'label': 'OpenClaw Gateway',
        'type': 'systemd',
        'unit': 'openclaw-gateway',
        'port': 50506,
        'icon': 'ti-heart-rate-monitor',
        'color': '#c9a84c',
    },
    'litellm': {
        'label': 'LiteLLM Proxy',
        'type': 'systemd',
        'unit': 'litellm',
        'port': 4000,
        'icon': 'ti-git-branch',
        'color': '#a78bfa',
    },
    'backend': {
        'label': 'MCC Backend',
        'type': 'process',
        'match': 'app.main',
        'port': 8000,
        'icon': 'ti-server',
        'color': '#38bdf8',
        'start_cmd': 'cd /home/prime/arc_ai_angels/mission_control/mcc-backend && nohup python3 -m app.main > /tmp/mcc-backend.log 2>&1 &',
    },
    'frontend': {
        'label': 'Vite Frontend',
        'type': 'process',
        'match': 'frontend-mcc',
        'port': 3002,
        'icon': 'ti-brand-react',
        'color': '#34d399',
        'start_cmd': 'cd /home/prime/arc_ai_angels/mission_control/frontend-mcc && nohup npx vite --port 3002 > /tmp/vite.log 2>&1 &',
    },
    'cloudflare': {
        'label': 'Cloudflare Tunnel',
        'type': 'process',
        'match': 'cloudflared',
        'port': None,
        'icon': 'ti-cloud',
        'color': '#fb923c',
    },
}

def get_systemd_status(unit):
    try:
        r = subprocess.run(['systemctl','--user','is-active', unit], capture_output=True, text=True, timeout=5)
        return r.stdout.strip()
    except:
        return 'unknown'

def get_process_status(match):
    try:
        for proc in psutil.process_iter(['pid','cmdline','status']):
            cmdline = ' '.join(proc.info['cmdline'] or [])
            if match in cmdline:
                return 'active'
        return 'inactive'
    except:
        return 'unknown'

def get_port_status(port):
    if not port:
        return None
    try:
        import socket
        s = socket.socket()
        s.settimeout(1)
        result = s.connect_ex(('127.0.0.1', port))
        s.close()
        return 'reachable' if result == 0 else 'unreachable'
    except:
        return 'unknown'

@router.get("/system/services")
async def get_services():
    result = []
    for key, svc in SERVICES.items():
        if svc['type'] == 'systemd':
            status = get_systemd_status(svc['unit'])
        else:
            status = get_process_status(svc['match'])
        
        port_status = get_port_status(svc.get('port'))
        
        result.append({
            'id': key,
            'label': svc['label'],
            'status': status,
            'port': svc.get('port'),
            'port_status': port_status,
            'icon': svc['icon'],
            'color': svc['color'],
            'type': svc['type'],
        })
    return {'services': result, 'ok': True}

@router.post("/system/service/{service_id}/start")
async def start_service(service_id: str):
    if service_id not in SERVICES:
        return {'ok': False, 'error': 'Onbekende service'}
    svc = SERVICES[service_id]
    try:
        if svc['type'] == 'systemd':
            subprocess.run(['systemctl','--user','start', svc['unit']], timeout=15)
            return {'ok': True, 'message': f"{svc['label']} gestart"}
        elif 'start_cmd' in svc:
            subprocess.Popen(svc['start_cmd'], shell=True)
            return {'ok': True, 'message': f"{svc['label']} gestart"}
        else:
            return {'ok': False, 'error': 'Geen start commando beschikbaar'}
    except Exception as e:
        return {'ok': False, 'error': str(e)}

@router.post("/system/service/{service_id}/stop")
async def stop_service(service_id: str):
    if service_id not in SERVICES:
        return {'ok': False, 'error': 'Onbekende service'}
    svc = SERVICES[service_id]
    try:
        if svc['type'] == 'systemd':
            subprocess.run(['systemctl','--user','stop', svc['unit']], timeout=15)
            return {'ok': True, 'message': f"{svc['label']} gestopt"}
        else:
            match = svc.get('match','')
            for proc in psutil.process_iter(['pid','cmdline']):
                cmdline = ' '.join(proc.info['cmdline'] or [])
                if match in cmdline:
                    proc.kill()
            return {'ok': True, 'message': f"{svc['label']} gestopt"}
    except Exception as e:
        return {'ok': False, 'error': str(e)}

@router.post("/system/service/{service_id}/restart")
async def restart_service(service_id: str):
    if service_id not in SERVICES:
        return {'ok': False, 'error': 'Onbekende service'}
    svc = SERVICES[service_id]
    try:
        if svc['type'] == 'systemd':
            subprocess.run(['systemctl','--user','restart', svc['unit']], timeout=15)
            return {'ok': True, 'message': f"{svc['label']} herstart"}
        else:
            # Stop dan start
            await stop_service(service_id)
            import asyncio
            await asyncio.sleep(2)
            return await start_service(service_id)
    except Exception as e:
        return {'ok': False, 'error': str(e)}

@router.post("/system/start-all")
async def start_all():
    results = []
    for service_id in ['openclaw', 'litellm', 'backend', 'frontend']:
        r = await start_service(service_id)
        results.append({'service': service_id, **r})
    return {'ok': True, 'results': results}
