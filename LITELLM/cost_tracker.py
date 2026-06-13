#!/usr/bin/env python3
"""
cost_tracker.py — ARC AI Agents Cost Tracker
Leest LiteLLM logs en bouwt een kosten database
"""
import sqlite3, json, re, os
from datetime import datetime

DB_PATH = '/home/prime/arc_ai_angels/LITELLM/costs.db'
LOG_PATH = '/tmp/litellm.log'

# Kosten per 1M tokens in euro
COSTS = {
    'gemini/gemini-2.5-flash-lite': {'input': 0.018, 'output': 0.072},
    'gpt-4o-mini':                   {'input': 0.12,  'output': 0.48},
    'gemini/gemini-2.5-pro':        {'input': 1.00,  'output': 3.50},
    'gemini/gemini-2.5-flash':      {'input': 0.06,  'output': 0.24},
    'gpt-4o':                        {'input': 2.00,  'output': 8.00},
    'openrouter/google/gemini-2.5-flash': {'input': 0.06, 'output': 0.24},
    'openrouter/deepseek/deepseek-v4-flash': {'input': 0.07, 'output': 0.28},
}

# Tool kosten per call in euro
TOOL_COSTS = {
    'tavily':     0.008,
    'firecrawl':  0.001,
    'exa':        0.008,
    'perplexity': 0.004,
    'elevenlabs': 0.0003,
    'deepgram':   0.005,
    'duckduckgo': 0.0,
    'telegram':   0.0,
    'webhooks':   0.0,
}

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute('''CREATE TABLE IF NOT EXISTS llm_calls (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        agent_id TEXT,
        model TEXT,
        input_tokens INTEGER,
        output_tokens INTEGER,
        cost_eur REAL,
        success INTEGER,
        session_key TEXT
    )''')
    conn.execute('''CREATE TABLE IF NOT EXISTS tool_calls (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        agent_id TEXT,
        tool_name TEXT,
        cost_eur REAL,
        success INTEGER,
        details TEXT
    )''')
    conn.execute('''CREATE TABLE IF NOT EXISTS daily_summary (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        agent_id TEXT,
        llm_calls INTEGER,
        tool_calls INTEGER,
        total_tokens INTEGER,
        total_cost_eur REAL
    )''')
    conn.commit()
    return conn

def get_cost(model, input_tokens, output_tokens):
    for model_key, rates in COSTS.items():
        if model_key in model:
            input_cost = (input_tokens / 1_000_000) * rates['input']
            output_cost = (output_tokens / 1_000_000) * rates['output']
            return round(input_cost + output_cost, 6)
    return 0.0

def get_summary(conn):
    print('\n📊 ARC AI Agents Cost Summary')
    print('='*60)
    
    # Totale kosten
    cur = conn.execute('SELECT SUM(cost_eur) FROM llm_calls WHERE success=1')
    llm_total = cur.fetchone()[0] or 0
    
    cur = conn.execute('SELECT SUM(cost_eur) FROM tool_calls WHERE success=1')
    tool_total = cur.fetchone()[0] or 0
    
    print(f'\n💰 TOTALE KOSTEN:')
    print(f'  LLM calls:  €{llm_total:.4f}')
    print(f'  Tool calls: €{tool_total:.4f}')
    print(f'  TOTAAL:     €{(llm_total+tool_total):.4f}')
    
    # Per agent
    print(f'\n🤖 KOSTEN PER AGENT:')
    cur = conn.execute('''
        SELECT agent_id, COUNT(*), SUM(input_tokens+output_tokens), SUM(cost_eur)
        FROM llm_calls WHERE success=1
        GROUP BY agent_id ORDER BY SUM(cost_eur) DESC
    ''')
    for row in cur.fetchall():
        print(f'  {row[0]:<12} {row[1]:>4} calls  {row[2]:>8} tokens  €{row[3]:.4f}')
    
    # Per model
    print(f'\n🧠 KOSTEN PER MODEL:')
    cur = conn.execute('''
        SELECT model, COUNT(*), SUM(cost_eur)
        FROM llm_calls WHERE success=1
        GROUP BY model ORDER BY SUM(cost_eur) DESC
    ''')
    for row in cur.fetchall():
        print(f'  {row[0]:<35} {row[1]:>4} calls  €{row[2]:.4f}')
    
    # Tool usage
    print(f'\n🔧 TOOL GEBRUIK:')
    cur = conn.execute('''
        SELECT tool_name, COUNT(*), SUM(cost_eur)
        FROM tool_calls
        GROUP BY tool_name ORDER BY COUNT(*) DESC
    ''')
    for row in cur.fetchall():
        cost_str = f'€{row[2]:.4f}' if row[2] > 0 else 'gratis'
        print(f'  {row[0]:<20} {row[1]:>4}x  {cost_str}')

if __name__ == '__main__':
    conn = init_db()
    get_summary(conn)
    conn.close()
