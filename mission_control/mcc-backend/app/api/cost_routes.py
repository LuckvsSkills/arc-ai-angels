from fastapi import APIRouter, Request
import sqlite3, json, os, subprocess
from datetime import datetime, date

router = APIRouter()
DB_PATH = '/home/prime/arc_ai_angels/LITELLM/costs.db'

# Kosten per 1M tokens in euro
MODEL_COSTS = {
    'gemini/gemini-2.5-flash-lite': {'input': 0.018, 'output': 0.072},
    'gpt-4o-mini':                   {'input': 0.120, 'output': 0.480},
    'gemini/gemini-2.5-pro':        {'input': 1.000, 'output': 3.500},
    'gemini/gemini-2.5-flash':      {'input': 0.060, 'output': 0.240},
    'gpt-4o':                        {'input': 2.000, 'output': 8.000},
}

TOOL_COSTS = {
    'tavily':     {'cost': 0.008, 'free_quota': 1000, 'type': 'betaald'},
    'firecrawl':  {'cost': 0.001, 'free_quota': 500,  'type': 'betaald'},
    'exa':        {'cost': 0.008, 'free_quota': 1000, 'type': 'betaald'},
    'perplexity': {'cost': 0.004, 'free_quota': 150,  'type': 'betaald'},
    'duckduckgo': {'cost': 0.0,   'free_quota': -1,   'type': 'gratis'},
    'telegram':   {'cost': 0.0,   'free_quota': -1,   'type': 'gratis'},
    'webhooks':   {'cost': 0.0,   'free_quota': -1,   'type': 'gratis'},
    'elevenlabs': {'cost': 0.0003,'free_quota': 10000,'type': 'betaald'},
    'deepgram':   {'cost': 0.005, 'free_quota': 200,  'type': 'betaald'},
}

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute('''CREATE TABLE IF NOT EXISTS llm_calls (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT, agent_id TEXT, model TEXT,
        input_tokens INTEGER, output_tokens INTEGER,
        cost_eur REAL, success INTEGER, session_key TEXT, task TEXT
    )''')
    conn.execute('''CREATE TABLE IF NOT EXISTS tool_calls (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT, agent_id TEXT, tool_name TEXT,
        cost_eur REAL, success INTEGER, details TEXT
    )''')
    conn.commit()
    conn.close()

init_db()

@router.post("/costs/log-llm")
async def log_llm_call(request: Request):
    """MCC backend logt elke LiteLLM call hier"""
    data = await request.json()
    agent_id = data.get('agent_id', 'unknown')
    model = data.get('model', '')
    input_tokens = data.get('input_tokens', 0)
    output_tokens = data.get('output_tokens', 0)
    success = data.get('success', 1)
    session_key = data.get('session_key', '')
    task = data.get('task', '')
    
    # Bereken kosten
    cost = 0.0
    for model_key, rates in MODEL_COSTS.items():
        if model_key in model:
            cost = ((input_tokens / 1_000_000) * rates['input'] +
                   (output_tokens / 1_000_000) * rates['output'])
            break
    
    conn = get_db()
    conn.execute('''INSERT INTO llm_calls 
        (timestamp, agent_id, model, input_tokens, output_tokens, cost_eur, success, session_key, task)
        VALUES (?,?,?,?,?,?,?,?,?)''',
        (datetime.now().isoformat(), agent_id, model, input_tokens, output_tokens,
         round(cost, 6), success, session_key, task))
    conn.commit()
    conn.close()
    return {'ok': True, 'cost_eur': cost}

@router.post("/costs/log-tool")
async def log_tool_call(request: Request):
    """Log een tool call met kosten"""
    data = await request.json()
    agent_id = data.get('agent_id', 'unknown')
    tool_name = data.get('tool_name', '')
    success = data.get('success', 1)
    details = data.get('details', '')
    
    tool_info = TOOL_COSTS.get(tool_name, {'cost': 0.0})
    cost = tool_info['cost']
    
    conn = get_db()
    conn.execute('''INSERT INTO tool_calls
        (timestamp, agent_id, tool_name, cost_eur, success, details)
        VALUES (?,?,?,?,?,?)''',
        (datetime.now().isoformat(), agent_id, tool_name, cost, success, details))
    conn.commit()
    conn.close()
    return {'ok': True, 'cost_eur': cost}

@router.get("/costs/summary")
async def get_cost_summary():
    """Kosten overzicht voor MCC dashboard"""
    conn = get_db()
    
    # Totalen
    llm_total = conn.execute('SELECT COALESCE(SUM(cost_eur),0) FROM llm_calls WHERE success=1').fetchone()[0]
    tool_total = conn.execute('SELECT COALESCE(SUM(cost_eur),0) FROM tool_calls WHERE success=1').fetchone()[0]
    
    # Per agent
    agents = conn.execute('''
        SELECT agent_id, COUNT(*) as calls, 
               COALESCE(SUM(input_tokens+output_tokens),0) as tokens,
               COALESCE(SUM(cost_eur),0) as cost
        FROM llm_calls WHERE success=1
        GROUP BY agent_id ORDER BY cost DESC
    ''').fetchall()
    
    # Per model
    models = conn.execute('''
        SELECT model, COUNT(*) as calls, COALESCE(SUM(cost_eur),0) as cost
        FROM llm_calls WHERE success=1
        GROUP BY model ORDER BY cost DESC
    ''').fetchall()
    
    # Tool gebruik
    tools = conn.execute('''
        SELECT tool_name, COUNT(*) as calls, 
               COALESCE(SUM(cost_eur),0) as cost,
               SUM(CASE WHEN success=0 THEN 1 ELSE 0 END) as failures
        FROM tool_calls
        GROUP BY tool_name ORDER BY calls DESC
    ''').fetchall()
    
    # Vandaag
    today = date.today().isoformat()
    today_cost = conn.execute(
        "SELECT COALESCE(SUM(cost_eur),0) FROM llm_calls WHERE timestamp LIKE ? AND success=1",
        (f'{today}%',)
    ).fetchone()[0]
    
    # Recente calls
    recent = conn.execute('''
        SELECT timestamp, agent_id, model, input_tokens+output_tokens as tokens, cost_eur, task
        FROM llm_calls ORDER BY id DESC LIMIT 20
    ''').fetchall()
    
    conn.close()
    
    return {
        'ok': True,
        'totals': {
            'llm_eur': round(llm_total, 4),
            'tool_eur': round(tool_total, 4),
            'total_eur': round(llm_total + tool_total, 4),
            'today_eur': round(today_cost, 4),
        },
        'by_agent': [dict(r) for r in agents],
        'by_model': [dict(r) for r in models],
        'by_tool': [dict(r) for r in tools],
        'recent': [dict(r) for r in recent],
        'tool_info': TOOL_COSTS,
    }

@router.get("/costs/tool-tiers")
async def get_tool_tiers():
    """Tool tiers — gratis vs betaald vs alternatief"""
    return {
        'ok': True,
        'tiers': {
            'gratis': [
                {'name':'duckduckgo',    'desc':'Web search',          'limit':'onbeperkt'},
                {'name':'active-memory', 'desc':'Memory injectie',     'limit':'onbeperkt'},
                {'name':'skill-workshop','desc':'Skills opslaan',      'limit':'onbeperkt'},
                {'name':'memory-wiki',   'desc':'Kennisbase',          'limit':'onbeperkt'},
                {'name':'webhooks',      'desc':'HTTP triggers',       'limit':'onbeperkt'},
                {'name':'llm-task',      'desc':'Subtaken spawnen',    'limit':'onbeperkt'},
                {'name':'telegram',      'desc':'Messaging',           'limit':'onbeperkt'},
                {'name':'opencode',      'desc':'Code schrijven',      'limit':'onbeperkt'},
                {'name':'vercel',        'desc':'Website deploy',      'limit':'100GB/maand'},
            ],
            'betaald_met_gratis_tier': [
                {'name':'tavily',     'desc':'AI web search',    'free':'1000/maand', 'cost':'$0.008/search',  'alternative':'duckduckgo'},
                {'name':'firecrawl',  'desc':'Web scraping',     'free':'500/maand',  'cost':'$0.001/pagina',  'alternative':'web-readability'},
                {'name':'exa',        'desc':'Neural search',    'free':'1000/maand', 'cost':'$0.008/search',  'alternative':'tavily of duckduckgo'},
                {'name':'perplexity', 'desc':'AI search',        'free':'5/dag',      'cost':'$0.004/query',   'alternative':'tavily'},
            ],
            'betaald_per_gebruik': [
                {'name':'elevenlabs', 'desc':'Voice generatie',  'cost':'$0.0003/karakter', 'alternative':'geen — optioneel'},
                {'name':'deepgram',   'desc':'Speech-to-text',   'cost':'$0.005/minuut',    'alternative':'geen — optioneel'},
            ],
        }
    }

@router.get("/costs/openclaw-tool-logs")
async def get_openclaw_tool_logs():
    """Parse OpenClaw logs voor tool usage"""
    try:
        result = subprocess.run(
            ['journalctl', '--user', '-u', 'openclaw-gateway', 
             '--since', '7 days ago', '--no-pager'],
            capture_output=True, text=True, timeout=10
        )
        logs = result.stdout
        
        tool_usage = {}
        for tool in ['tavily', 'firecrawl', 'exa', 'perplexity', 'duckduckgo', 
                     'telegram', 'webhooks', 'elevenlabs']:
            calls = logs.lower().count(f'[tools] {tool}')
            failures = logs.lower().count(f'{tool} failed')
            if calls > 0 or failures > 0:
                tool_usage[tool] = {
                    'calls': calls,
                    'failures': failures,
                    'estimated_cost': round(calls * TOOL_COSTS.get(tool, {}).get('cost', 0), 4)
                }
        
        return {'ok': True, 'tool_usage': tool_usage}
    except Exception as e:
        return {'ok': False, 'error': str(e)}
