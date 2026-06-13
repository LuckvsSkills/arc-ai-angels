import React, { useState, useEffect, useCallback, useRef } from 'react'

const DOMAIN_COLORS = {
  nova:'#c9a84c', flux:'#c9a84c',
  cortexia:'#38bdf8', forge:'#38bdf8', nero:'#38bdf8', ventura:'#38bdf8', axon:'#38bdf8', clio:'#38bdf8',
  finoria:'#f472b6', vector:'#f472b6', kairo:'#f472b6', kenzo:'#f472b6', odis:'#f472b6', zion:'#f472b6',
  saelia:'#34d399', tharos:'#34d399', sora:'#34d399', arix:'#34d399', enki:'#34d399', daxio:'#34d399',
  lumeria:'#a78bfa', kresta:'#a78bfa', elora:'#a78bfa', luvia:'#a78bfa', nura:'#a78bfa', vondra:'#a78bfa',
  fluentia:'#fb923c', draven:'#fb923c', solis:'#fb923c', orizon:'#fb923c', unia:'#fb923c', zena:'#fb923c',
}

const DOMAIN_OF = {
  nova:'core', flux:'core',
  cortexia:'helix', forge:'helix', nero:'helix', ventura:'helix', axon:'helix', clio:'helix',
  finoria:'finix', vector:'finix', kairo:'finix', kenzo:'finix', odis:'finix', zion:'finix',
  saelia:'matrix', tharos:'matrix', sora:'matrix', arix:'matrix', enki:'matrix', daxio:'matrix',
  lumeria:'quantix', kresta:'quantix', elora:'quantix', luvia:'quantix', nura:'quantix', vondra:'quantix',
  fluentia:'zenix', draven:'zenix', solis:'zenix', orizon:'zenix', unia:'zenix', zena:'zenix',
}

// Parse raw OpenClaw status text → sessie objecten
function parseSessions(raw = '') {
  const sessions = []
  const lines = raw.split('\n')
  let inSessionTable = false
  for (const line of lines) {
    if (line.includes('Key') && line.includes('Kind') && line.includes('Age')) { inSessionTable = true; continue }
    if (inSessionTable && line.includes('─') && sessions.length > 0) break
    if (inSessionTable && line.includes('│')) {
      const cols = line.split('│').map(s => s.trim()).filter(Boolean)
      if (cols.length >= 4 && cols[0].startsWith('agent:')) {
        const key = cols[0]
        const parts = key.split(':')
        const agentId = parts[1] || ''
        const sessionType = parts[2] || 'main'
        const isCron = sessionType === 'cron'
        const model = cols[3] || ''
        const tokensStr = cols[4] || ''
        const tokenMatch = tokensStr.match(/(\d+)k\/(\d+)k.*\((\d+)%\)/)
        sessions.push({
          key, agentId, sessionType, isCron,
          age: cols[2] || '',
          model: model.replace('gemini-', 'G-').replace('gpt-', 'GPT-').replace('claude-', 'C-'),
          modelFull: model,
          tokens: tokenMatch ? parseInt(tokenMatch[1]) : 0,
          tokenMax: tokenMatch ? parseInt(tokenMatch[2]) : 1000,
          tokenPct: tokenMatch ? parseInt(tokenMatch[3]) : 0,
        })
      }
    }
  }
  return sessions
}

// Parse heartbeat status uit raw text
function parseHeartbeats(raw = '') {
  const hb = {}
  const match = raw.match(/Heartbeat.*?(\n|$)(.*?)(\n\n|\n│)/s)
  if (match) {
    const hbText = raw.split('Heartbeat')[1] || ''
    const pairs = hbText.matchAll(/(\w+) \(([^)]+)\)/g)
    for (const [, name, status] of pairs) hb[name] = status
  }
  return hb
}

function Dot({ color, size = 7, pulse = false }) {
  return (
    <span style={{ position: 'relative', display: 'inline-flex', alignItems: 'center', justifyContent: 'center', width: size, height: size, flexShrink: 0 }}>
      {pulse && <span style={{ position: 'absolute', width: size * 2.4, height: size * 2.4, borderRadius: '50%', background: color, opacity: 0.15, animation: 'mcc-pulse 2s infinite' }} />}
      <span style={{ width: size, height: size, borderRadius: '50%', background: color, boxShadow: `0 0 ${size}px ${color}80` }} />
    </span>
  )
}

function TokenBar({ pct, color, height = 4 }) {
  const c = pct > 80 ? '#ef4444' : pct > 50 ? '#f59e0b' : color
  return (
    <div style={{ height, background: 'rgba(255,255,255,0.06)', borderRadius: 2, overflow: 'hidden', width: '100%' }}>
      <div style={{ height: '100%', width: `${pct}%`, background: c, borderRadius: 2, transition: 'width 0.4s' }} />
    </div>
  )
}

const TABS = [
  { id: 'zenuwstelsel', label: 'Zenuwstelsel', icon: 'ti-activity' },
  { id: 'sessies',      label: 'Sessies',      icon: 'ti-messages' },
  { id: 'modellen',     label: 'Modellen',     icon: 'ti-cpu' },
  { id: 'databases',    label: 'Databases',    icon: 'ti-database' },
  { id: 'config',       label: 'Config',       icon: 'ti-settings' },
]

export default function OpenClawView({ theme }) {
  const t = theme?.colors || {}
  const acc = t.accent || '#c9a84c'

  const [data, setData] = useState({})
  const [loading, setLoading] = useState(true)
  const [tab, setTab] = useState('zenuwstelsel')
  const [autoRefresh, setAutoRefresh] = useState(false)
  const [lastRefresh, setLastRefresh] = useState(null)
  const [actionMsg, setActionMsg] = useState(null)
  const [winW, setWinW] = useState(window.innerWidth)
  const intervalRef = useRef(null)
  const isMobile = winW < 700

  useEffect(() => {
    const h = () => setWinW(window.innerWidth)
    window.addEventListener('resize', h)
    return () => window.removeEventListener('resize', h)
  }, [])

  const load = useCallback(async () => {
    setLoading(true)
    const [status, sysinfo, registry, telegram, models, memory, logs, runtimeStatus] = await Promise.all([
      fetch('/api/openclaw/status').then(r => r.json()).catch(() => ({})),
      fetch('/api/openclaw/sysinfo').then(r => r.json()).catch(() => ({})),
      fetch('/api/openclaw/registry').then(r => r.json()).catch(() => ({ agents: [] })),
      fetch('/api/openclaw/telegram').then(r => r.json()).catch(() => ({})),
      fetch('/api/models/overview').then(r => r.json()).catch(() => ({ agents: [] })),
      fetch('/api/openclaw/memory').then(r => r.json()).catch(() => ({ databases: [] })),
      fetch('/api/openclaw/logs/recent').then(r => r.json()).catch(() => ({ logs: [] })),
      fetch('/api/openclaw/runtime-status').then(r => r.json()).catch(() => ({runtime: 'unknown'})),
    ])
    const sessions = parseSessions(status.raw || '')
    const heartbeats = parseHeartbeats(status.raw || '')
    setData({ status, sysinfo, registry, telegram, models, memory, logs, runtimeStatus, sessions, heartbeats })
    setLastRefresh(new Date())
    setLoading(false)
  }, [])

  useEffect(() => { load() }, [load])
  useEffect(() => {
    if (autoRefresh) intervalRef.current = setInterval(load, 20000)
    else clearInterval(intervalRef.current)
    return () => clearInterval(intervalRef.current)
  }, [autoRefresh, load])

  const doAction = async (url, label) => {
    setActionMsg({ text: `${label}...`, type: 'info' })
    try {
      const r = await fetch(url, { method: 'POST' })
      const d = await r.json()
      setActionMsg({ text: d.ok ? `${label} geslaagd` : d.error || 'Fout', type: d.ok ? 'ok' : 'err' })
    } catch { setActionMsg({ text: 'Verbinding mislukt', type: 'err' }) }
    setTimeout(() => { setActionMsg(null); load() }, 4000)
  }

  const { status = {}, sysinfo = {}, registry = { agents: [] }, models = { agents: [] },
          memory = { databases: [] }, logs = { logs: [] }, sessions = [], heartbeats = {} } = data

  const agents = registry.agents || []
  const databases = memory.databases || []
  const modelAgents = models.agents || []
  const cronSessions = sessions.filter(s => s.isCron)
  const mainSessions = sessions.filter(s => !s.isCron)
  const heartbeatActive = Object.values(heartbeats).filter(v => v !== 'disabled').length
  const configWarnings = []
  if ((status.raw || '').includes('visibleReplies')) configWarnings.push('messages.groupChat: "visibleReplies" onbekend')
  if ((status.raw || '').includes('"streaming"')) configWarnings.push('channels.telegram: "streaming" onbekend')
  const totalDbKb = databases.reduce((s, d) => s + (d.size_kb || 0), 0)

  const SC = s => ['reachable', 'connected', 'ok', 'running'].includes(String(s).toLowerCase()) ? '#22c55e' : '#ef4444'

  return (
    <div style={{ height: '100%', display: 'flex', flexDirection: 'column', overflow: 'hidden', background: t.bg }}>
      <style>{`
        .oc-tab:hover { color: ${acc} !important; background: ${acc}12 !important; }
        .oc-tab-scroll { scrollbar-width: none; }
        .oc-tab-scroll::-webkit-scrollbar { display: none; }
        .oc-row:hover { background: ${acc}08 !important; }
        .oc-action:hover { background: ${acc}25 !important; border-color: ${acc}80 !important; }
      `}</style>

      {/* ── TOPBAR ── */}
      <div style={{ flexShrink: 0, background: t.bgSecondary, borderBottom: `1px solid ${t.border}` }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 12, padding: isMobile ? '10px 14px' : '12px 20px' }}>
          {/* Identity */}
          <div style={{ width: 40, height: 40, borderRadius: 10, background: `${acc}18`, border: `2px solid ${acc}50`, display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0 }}>
            <i className="ti ti-heart-rate-monitor" style={{ fontSize: 20, color: acc }} />
          </div>
          <div style={{ flex: 1, minWidth: 0 }}>
            <div style={{ fontSize: 15, fontWeight: 800, color: t.text }}>OpenClaw</div>
            <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginTop: 2, flexWrap: 'wrap' }}>
              <Dot color={SC(status.gateway)} size={6} pulse={status.gateway === 'reachable'} />
              <span style={{ fontSize: 10, color: t.textMuted }}>v{sysinfo.version || '—'}</span>
              <span style={{ fontSize: 10, color: t.textMuted }}>·</span>
              <span style={{ fontSize: 10, color: '#22c55e', fontWeight: 700 }}>{sessions.length} sessies</span>
              <span style={{ fontSize: 10, color: t.textMuted }}>·</span>
              <span style={{ fontSize: 10, color: '#a78bfa', fontWeight: 700 }}>{agents.length} agents</span>
              {configWarnings.length > 0 && (
                <span onClick={() => setTab('config')} style={{ fontSize: 10, padding: '1px 7px', borderRadius: 8, background: '#f59e0b15', color: '#f59e0b', fontWeight: 700, cursor: 'pointer', border: '1px solid #f59e0b30' }}>
                  ⚠ {configWarnings.length} config
                </span>
              )}
            </div>
          </div>
          {/* Controls */}
          <div style={{ display: 'flex', gap: 6, alignItems: 'center', flexShrink: 0 }}>
            {actionMsg && (
              <span style={{ fontSize: 10, padding: '4px 10px', borderRadius: 6, background: actionMsg.type === 'ok' ? '#22c55e15' : actionMsg.type === 'err' ? '#ef444415' : `${acc}15`, color: actionMsg.type === 'ok' ? '#22c55e' : actionMsg.type === 'err' ? '#ef4444' : acc }}>
                {actionMsg.text}
              </span>
            )}
            <button onClick={() => setAutoRefresh(v => !v)} style={{ display: 'flex', alignItems: 'center', gap: 5, padding: '5px 10px', borderRadius: 7, border: `1px solid ${autoRefresh ? '#22c55e40' : t.border}`, background: autoRefresh ? '#22c55e15' : 'transparent', color: autoRefresh ? '#22c55e' : t.textMuted, cursor: 'pointer', fontSize: 10, fontWeight: 600 }}>
              <i className="ti ti-refresh" style={{ fontSize: 13, animation: autoRefresh ? 'mcc-spin 2s linear infinite' : 'none' }} />
              {!isMobile && (autoRefresh ? 'Live' : '20s')}
            </button>
            <button onClick={load} style={{ width: 32, height: 32, borderRadius: 7, border: `1px solid ${acc}40`, background: `${acc}12`, color: acc, cursor: 'pointer', fontSize: 15, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              <i className="ti ti-reload" />
            </button>
          </div>
        </div>

        {/* Tabs */}
        <div className="oc-tab-scroll" style={{ display: 'flex', gap: 2, padding: '4px 14px 0', overflowX: 'auto' }}>
          {TABS.map(tb => {
            const isActive = tab === tb.id
            const hasBadge = tb.id === 'config' && configWarnings.length > 0
            return (
              <button key={tb.id} onClick={() => setTab(tb.id)} className="oc-tab" style={{
                display: 'flex', alignItems: 'center', gap: 5, padding: '7px 13px',
                borderRadius: '7px 7px 0 0', flexShrink: 0, fontSize: 10, fontWeight: isActive ? 700 : 500,
                cursor: 'pointer', border: `1px solid ${isActive ? t.border : 'transparent'}`,
                borderBottom: isActive ? `1px solid ${t.bgSecondary}` : '1px solid transparent',
                background: isActive ? t.bgSecondary : 'transparent',
                color: isActive ? acc : t.textMuted, marginBottom: isActive ? -1 : 0,
                letterSpacing: '0.05em', textTransform: 'uppercase', transition: 'all .15s',
              }}>
                <i className={`ti ${tb.icon}`} style={{ fontSize: 13 }} />
                {tb.label}
                {hasBadge && <span style={{ background: '#f59e0b', color: '#000', borderRadius: 8, padding: '0 5px', fontSize: 8, fontWeight: 700 }}>{configWarnings.length}</span>}
              </button>
            )
          })}
        </div>
      </div>

      {/* ── CONTENT ── */}
      <div style={{ flex: 1, overflow: 'auto', padding: isMobile ? '14px' : '20px 24px', scrollbarWidth: 'thin', scrollbarColor: `${acc} transparent` }}>
        {loading && (
          <div style={{ display: 'flex', alignItems: 'center', gap: 10, color: t.textMuted, fontSize: 13, padding: 20 }}>
            <Dot color={acc} size={8} pulse /> OpenClaw verbinden...
          </div>
        )}

        {/* ── ZENUWSTELSEL ── */}
        {!loading && tab === 'zenuwstelsel' && (
          <div style={{ display: 'flex', flexDirection: 'column', gap: 18 }}>

            {/* Status strip */}
            <div style={{ display: 'grid', gridTemplateColumns: isMobile ? 'repeat(2,1fr)' : 'repeat(5,1fr)', gap: 10 }}>
              {[
                { l: 'Runtime', v: data.runtimeStatus?.runtime || '—', c: data.runtimeStatus?.runtime === 'running' ? '#22c55e' : '#ef4444', sub: 'OpenClaw engine', icon: 'ti-cpu' },
                { l: 'Gateway', v: status.gateway || '—', c: SC(status.gateway), sub: 'ws://127.0.0.1:18789', icon: 'ti-server' },
                { l: 'Telegram', v: status.telegram || '—', c: SC(status.telegram), sub: `@${data.telegram?.bot?.username || '—'}`, icon: 'ti-brand-telegram' },
                { l: 'Actieve sessies', v: sessions.length, c: '#22c55e', sub: `${cronSessions.length} HARNAS · ${mainSessions.length} direct`, icon: 'ti-messages' },
                { l: 'Heartbeat', v: `${heartbeatActive}/${agents.length}`, c: heartbeatActive < agents.length ? '#f59e0b' : '#22c55e', sub: 'agents actief', icon: 'ti-heartbeat' },
              ].map(s => (
                <div key={s.l} style={{ background: t.bgSecondary, border: `1px solid ${t.border}`, borderTop: `3px solid ${s.c}`, borderRadius: 10, padding: '14px 16px' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: 6, marginBottom: 8 }}>
                    <i className={`ti ${s.icon}`} style={{ fontSize: 13, color: `${s.c}90` }} />
                    <span style={{ fontSize: 10, fontWeight: 700, letterSpacing: '0.1em', textTransform: 'uppercase', color: t.textMuted }}>{s.l}</span>
                  </div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 5 }}>
                    <Dot color={s.c} size={7} pulse={s.c === '#22c55e'} />
                    <span style={{ fontSize: 22, fontWeight: 800, color: s.c, fontFamily: 'ui-monospace,monospace' }}>{s.v}</span>
                  </div>
                  <div style={{ fontSize: 10, color: t.textMuted }}>{s.sub}</div>
                </div>
              ))}
            </div>

            {/* Twee kolommen */}
            <div style={{ display: 'grid', gridTemplateColumns: isMobile ? '1fr' : '1fr 1fr', gap: 16 }}>

              {/* Systeem info */}
              <div style={{ background: t.bgSecondary, border: `1px solid ${t.border}`, borderRadius: 12, padding: '18px 20px' }}>
                <div style={{ fontSize: 10, fontWeight: 700, letterSpacing: '0.14em', textTransform: 'uppercase', color: t.textMuted, marginBottom: 14, display: 'flex', alignItems: 'center', gap: 6 }}>
                  <i className="ti ti-server" style={{ fontSize: 12, color: acc }} /> Systeem
                </div>
                {[
                  ['OS', 'WSL2 Ubuntu 22 · x64'],
                  ['Node', 'v22.22.0'],
                  ['Gateway', `ws://127.0.0.1:${sysinfo.gateway?.port || '18789'}`],
                  ['Versie', `v${sysinfo.version || '—'}`],
                  ['Channel', 'stable'],
                  ['Tailscale', 'Uitgeschakeld'],
                  ['Agents', `${agents.length} geregistreerd`],
                  ['Sessions', `${sessions.length} actief · 36 stores`],
                  ['Refresh', lastRefresh?.toLocaleTimeString('nl') || '—'],
                ].map(([k, v]) => (
                  <div key={k} style={{ display: 'flex', justifyContent: 'space-between', padding: '7px 0', borderBottom: `1px solid ${t.border}50` }}>
                    <span style={{ fontSize: 11, color: t.textMuted }}>{k}</span>
                    <span style={{ fontSize: 11, fontWeight: 600, color: t.text, fontFamily: 'ui-monospace,monospace' }}>{v}</span>
                  </div>
                ))}
              </div>

              {/* Services + Heartbeat overzicht */}
              <div style={{ background: t.bgSecondary, border: `1px solid ${t.border}`, borderRadius: 12, padding: '18px 20px' }}>
                <div style={{ fontSize: 10, fontWeight: 700, letterSpacing: '0.14em', textTransform: 'uppercase', color: t.textMuted, marginBottom: 14, display: 'flex', alignItems: 'center', gap: 6 }}>
                  <i className="ti ti-activity" style={{ fontSize: 12, color: '#38bdf8' }} /> Services & Verbindingen
                </div>
                {[
                  { l: 'Gateway Service', s: 'running', d: 'systemd enabled · pid 1148430 · active' },
                  { l: 'Node Service', s: 'stopped', d: 'systemd disabled · inactive' },
                  { l: 'OpenClaw Gateway', s: status.gateway || '—', d: 'ws://127.0.0.1:18789 loopback' },
                  { l: 'Telegram Bot', s: status.telegram || '—', d: `Berichten via agent kanaal` },
                  { l: 'Cloudflare Tunnel', s: 'running', d: 'arc-vortex.nl · tunnel actief' },
                ].map(c => (
                  <div key={c.l} style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '9px 0', borderBottom: `1px solid ${t.border}50` }}>
                    <div>
                      <div style={{ fontSize: 12, fontWeight: 600, color: t.text }}>{c.l}</div>
                      <div style={{ fontSize: 10, color: t.textMuted, marginTop: 2 }}>{c.d}</div>
                    </div>
                    <div style={{ display: 'flex', alignItems: 'center', gap: 6, flexShrink: 0, marginLeft: 12 }}>
                      <Dot color={SC(c.s)} size={7} pulse={SC(c.s) === '#22c55e'} />
                      <span style={{ fontSize: 11, color: SC(c.s), fontWeight: 700, minWidth: 55, textAlign: 'right' }}>{c.s}</span>
                    </div>
                  </div>
                ))}

                {/* Actie knoppen */}
                <div style={{ marginTop: 14, display: 'flex', gap: 8, flexWrap: 'wrap' }}>
                  <button className="oc-action" onClick={() => doAction('/api/openclaw/start', 'Start')} style={{ flex: 1, padding: '8px', borderRadius: 8, border: '1px solid #22c55e40', background: '#22c55e08', color: '#22c55e', cursor: 'pointer', fontSize: 11, fontWeight: 700, transition: 'all .15s' }}>
                    <i className="ti ti-player-play" /> Start
                  </button>
                  <button className="oc-action" onClick={() => doAction('/api/openclaw/stop', 'Stop')} style={{ flex: 1, padding: '8px', borderRadius: 8, border: '1px solid #ef444440', background: '#ef444408', color: '#ef4444', cursor: 'pointer', fontSize: 11, fontWeight: 700, transition: 'all .15s' }}>
                    <i className="ti ti-player-stop" /> Stop
                  </button>
                  <button className="oc-action" onClick={() => doAction('/api/openclaw/restart', 'Herstart')} style={{ flex: 1, padding: '8px', borderRadius: 8, border: '1px solid #f8711140', background: '#f8711108', color: '#f87115', cursor: 'pointer', fontSize: 11, fontWeight: 700, transition: 'all .15s' }}>
                    <i className="ti ti-refresh" /> Herstart
                  </button>
                  <button className="oc-action" onClick={() => doAction('/api/openclaw/update', 'Update')} style={{ flex: 1, padding: '8px', borderRadius: 8, border: '1px solid #a78bfa40', background: '#a78bfa08', color: '#a78bfa', cursor: 'pointer', fontSize: 11, fontWeight: 700, transition: 'all .15s' }}>
                    <i className="ti ti-arrow-up" /> Update
                  </button>
                  <button className="oc-action" onClick={() => doAction('/api/openclaw/doctor', 'Doctor')} style={{ flex: 1, padding: '8px', borderRadius: 8, border: `1px solid ${acc}40`, background: `${acc}08`, color: acc, cursor: 'pointer', fontSize: 11, fontWeight: 700, transition: 'all .15s' }}>
                    <i className="ti ti-stethoscope" /> Doctor
                  </button>
                </div>
              </div>
            </div>

            {/* Heartbeat grid */}
            <div style={{ background: t.bgSecondary, border: `1px solid ${t.border}`, borderRadius: 12, padding: '18px 20px' }}>
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 14 }}>
                <div style={{ fontSize: 10, fontWeight: 700, letterSpacing: '0.14em', textTransform: 'uppercase', color: t.textMuted, display: 'flex', alignItems: 'center', gap: 6 }}>
                  <i className="ti ti-heartbeat" style={{ fontSize: 12, color: '#f59e0b' }} /> Heartbeat Status — {heartbeatActive}/{agents.length} actief
                </div>
                <span style={{ fontSize: 10, color: '#f59e0b', background: '#f59e0b10', padding: '3px 8px', borderRadius: 6, border: '1px solid #f59e0b30' }}>
                  Activeer heartbeat voor alle agents voor volledig monitoring
                </span>
              </div>
              <div style={{ display: 'grid', gridTemplateColumns: isMobile ? 'repeat(4,1fr)' : 'repeat(8,1fr)', gap: 6 }}>
                {agents.map(agent => {
                  const hb = heartbeats[agent.id] || heartbeats[agent.name?.toLowerCase()] || 'disabled'
                  const isActive = hb !== 'disabled'
                  const color = DOMAIN_COLORS[agent.id] || acc
                  return (
                    <div key={agent.id} title={`${agent.name} — heartbeat: ${hb}`} style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 4, padding: '8px 4px', borderRadius: 7, background: isActive ? `${color}12` : t.bgTertiary, border: `1px solid ${isActive ? color + '40' : t.border}` }}>
                      <span style={{ fontSize: 16 }}>{agent.emoji || '🤖'}</span>
                      <span style={{ fontSize: 8, color: isActive ? color : t.textMuted, fontWeight: isActive ? 700 : 400, textAlign: 'center', lineHeight: 1.2 }}>{agent.name}</span>
                      <Dot color={isActive ? '#22c55e' : t.border} size={5} />
                    </div>
                  )
                })}
              </div>
            </div>
          </div>
        )}

        {/* ── SESSIES ── */}
        {!loading && tab === 'sessies' && (
          <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 10, flexWrap: 'wrap' }}>
              <div style={{ fontSize: 22, fontWeight: 800, color: acc, fontFamily: 'ui-monospace,monospace' }}>{sessions.length}</div>
              <div>
                <div style={{ fontSize: 14, fontWeight: 700, color: t.text }}>Actieve Sessies</div>
                <div style={{ fontSize: 11, color: t.textMuted }}>{cronSessions.length} HARNAS cron · {mainSessions.length} direct · gemini-2.5-flash · 200k ctx</div>
              </div>
              <div style={{ marginLeft: 'auto', display: 'flex', gap: 8 }}>
                {[['Alle', sessions.length], ['HARNAS', cronSessions.length], ['Direct', mainSessions.length]].map(([l, n]) => (
                  <div key={l} style={{ fontSize: 11, padding: '4px 10px', borderRadius: 6, background: t.bgSecondary, border: `1px solid ${t.border}`, color: t.textMuted }}>
                    <strong style={{ color: t.text }}>{n}</strong> {l}
                  </div>
                ))}
              </div>
            </div>

            {/* Sessie kaarten */}
            {sessions.length === 0 ? (
              <div style={{ padding: 32, textAlign: 'center', color: t.textMuted, fontSize: 12 }}>
                <i className="ti ti-messages" style={{ fontSize: 28, display: 'block', marginBottom: 10, opacity: 0.4 }} />
                Geen sessie data beschikbaar — ververs of check OpenClaw status
              </div>
            ) : (
              <div style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
                {/* HARNAS sectie */}
                {cronSessions.length > 0 && (
                  <>
                    <div style={{ fontSize: 9, fontWeight: 700, letterSpacing: '0.16em', textTransform: 'uppercase', color: acc, padding: '4px 0', display: 'flex', alignItems: 'center', gap: 6 }}>
                      <div style={{ width: 2, height: 10, background: acc, borderRadius: 1 }} /> HARNAS Cron Sessies
                    </div>
                    {cronSessions.map((s, i) => {
                      const color = DOMAIN_COLORS[s.agentId] || acc
                      return (
                        <div key={i} className="oc-row" style={{ background: t.bgSecondary, border: `1px solid ${t.border}`, borderLeft: `3px solid ${color}`, borderRadius: 8, padding: '10px 14px', display: 'flex', alignItems: 'center', gap: 12, transition: 'background .12s' }}>
                          <div style={{ flex: 1, minWidth: 0 }}>
                            <div style={{ fontSize: 11, fontFamily: 'ui-monospace,monospace', color: t.text, fontWeight: 600, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{s.key}</div>
                            <div style={{ display: 'flex', gap: 10, marginTop: 4 }}>
                              <span style={{ fontSize: 10, color: t.textMuted }}>{s.age}</span>
                              <span style={{ fontSize: 10, color, fontWeight: 700 }}>{s.model}</span>
                              <span style={{ fontSize: 9, padding: '1px 6px', borderRadius: 4, background: `${acc}18`, color: acc }}>HARNAS</span>
                            </div>
                          </div>
                          <div style={{ width: 100, flexShrink: 0 }}>
                            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 3, fontSize: 9, color: t.textMuted }}>
                              <span>{s.tokens}k</span>
                              <span style={{ color: s.tokenPct > 80 ? '#ef4444' : s.tokenPct > 50 ? '#f59e0b' : '#22c55e' }}>{s.tokenPct}%</span>
                            </div>
                            <TokenBar pct={s.tokenPct} color={color} />
                          </div>
                        </div>
                      )
                    })}
                  </>
                )}

                {/* Direct sessies */}
                {mainSessions.length > 0 && (
                  <>
                    <div style={{ fontSize: 9, fontWeight: 700, letterSpacing: '0.16em', textTransform: 'uppercase', color: '#38bdf8', padding: '4px 0', marginTop: 8, display: 'flex', alignItems: 'center', gap: 6 }}>
                      <div style={{ width: 2, height: 10, background: '#38bdf8', borderRadius: 1 }} /> Directe Sessies
                    </div>
                    {mainSessions.map((s, i) => {
                      const color = DOMAIN_COLORS[s.agentId] || acc
                      return (
                        <div key={i} className="oc-row" style={{ background: t.bgSecondary, border: `1px solid ${t.border}`, borderLeft: `3px solid ${color}`, borderRadius: 8, padding: '10px 14px', display: 'flex', alignItems: 'center', gap: 12, transition: 'background .12s' }}>
                          <div style={{ flex: 1 }}>
                            <div style={{ fontSize: 11, fontFamily: 'ui-monospace,monospace', color: t.text, fontWeight: 600 }}>{s.key}</div>
                            <div style={{ display: 'flex', gap: 10, marginTop: 4 }}>
                              <span style={{ fontSize: 10, color: t.textMuted }}>{s.age}</span>
                              <span style={{ fontSize: 10, color, fontWeight: 700 }}>{s.model}</span>
                            </div>
                          </div>
                          <div style={{ width: 100, flexShrink: 0 }}>
                            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 3, fontSize: 9, color: t.textMuted }}>
                              <span>{s.tokens}k</span>
                              <span style={{ color: s.tokenPct > 80 ? '#ef4444' : '#22c55e' }}>{s.tokenPct}%</span>
                            </div>
                            <TokenBar pct={s.tokenPct} color={color} />
                          </div>
                        </div>
                      )
                    })}
                  </>
                )}
              </div>
            )}
          </div>
        )}

        {/* ── MODELLEN ── */}
        {!loading && tab === 'modellen' && (
          <div style={{ display: 'flex', flexDirection: 'column', gap: 14 }}>
            <div style={{ fontSize: 14, fontWeight: 800, color: t.text, marginBottom: 4 }}>AI Model Tiers</div>
            <div style={{ fontSize: 11, color: t.textMuted, marginBottom: 8, lineHeight: 1.7 }}>
              Elk agent heeft een 3-tier model systeem. Tier A is het krachtigste model (zware taken), Tier B is het balans model, Tier C is het snel/goedkoop model. HARNAS selecteert automatisch op basis van taakcomplexiteit.
            </div>
            {/* CORE groep */}
            <div style={{ fontSize: 11, fontWeight: 700, color: acc, letterSpacing: '0.12em', textTransform: 'uppercase', marginBottom: 4, marginTop: 4, display: 'flex', alignItems: 'center', gap: 8 }}>
              <div style={{ flex: 1, height: 1, background: acc + '30' }}/>
              <span>Core</span>
              <div style={{ flex: 1, height: 1, background: acc + '30' }}/>
            </div>
            <div style={{ display: 'grid', gridTemplateColumns: isMobile ? '1fr' : 'repeat(auto-fill, minmax(280px, 1fr))', gap: 8, marginBottom: 16 }}>
              {modelAgents.filter(a => DOMAIN_OF[a.id] === 'core').map(agent => {
                const color = DOMAIN_COLORS[agent.id] || acc
                const regAgent = agents.find(a => a.id === agent.id)
                return (
                  <div key={agent.id} style={{ background: t.bgSecondary, border: `1px solid ${t.border}`, borderLeft: `4px solid ${color}`, borderRadius: 10, padding: '12px 14px' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 10 }}>
                      <span style={{ fontSize: 18 }}>{regAgent?.emoji || '🤖'}</span>
                      <div style={{ flex: 1 }}>
                        <div style={{ fontSize: 13, fontWeight: 700, color: t.text }}>{regAgent?.name || agent.id}</div>
                        <div style={{ fontSize: 9, color, fontWeight: 700, letterSpacing: '0.08em', textTransform: 'uppercase' }}>{DOMAIN_OF[agent.id] || '—'}</div>
                      </div>
                      <div style={{ fontSize: 9, padding: '2px 7px', borderRadius: 5, background: `${color}18`, color, fontWeight: 700 }}>
                        {agent.tierBaseline !== '?' ? `Tier ${agent.tierBaseline}` : '—'}
                      </div>
                    </div>
                    {[
                      { l: 'Tier A', v: agent.tierA?.[0] || '—', c: '#ef4444' },
                      { l: 'Tier B', v: agent.tierB?.[0] || '—', c: '#f59e0b' },
                      { l: 'Tier C', v: agent.tierC?.[0] || '—', c: '#22c55e' },
                    ].map(tier => (
                      <div key={tier.l} style={{ display: 'flex', gap: 8, padding: '4px 0', borderBottom: `1px solid ${t.border}40`, alignItems: 'center' }}>
                        <span style={{ fontSize: 9, fontWeight: 700, color: tier.c, width: 38, flexShrink: 0 }}>{tier.l}</span>
                        <span style={{ fontSize: 9, color: t.textMuted, fontFamily: 'ui-monospace,monospace', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap', flex: 1 }}>{tier.v}</span>
                        {agent.currentModel === tier.v && <span style={{ fontSize: 8, padding: '1px 5px', borderRadius: 4, background: `${tier.c}18`, color: tier.c, flexShrink: 0, fontWeight: 700 }}>actief</span>}
                      </div>
                    ))}
                  </div>
                )
              })}
            </div>

            {/* OMNI LEADS groep */}
            <div style={{ fontSize: 11, fontWeight: 700, color: '#38bdf8', letterSpacing: '0.12em', textTransform: 'uppercase', marginBottom: 4, display: 'flex', alignItems: 'center', gap: 8 }}>
              <div style={{ flex: 1, height: 1, background: '#38bdf820' }}/>
              <span>Omni Leads</span>
              <div style={{ flex: 1, height: 1, background: '#38bdf820' }}/>
            </div>
            <div style={{ display: 'grid', gridTemplateColumns: isMobile ? '1fr' : 'repeat(auto-fill, minmax(280px, 1fr))', gap: 8, marginBottom: 16 }}>
              {modelAgents.filter(a => ['cortexia','finoria','saelia','lumeria','fluentia'].includes(a.id)).map(agent => {
                const color = DOMAIN_COLORS[agent.id] || acc
                const regAgent = agents.find(a => a.id === agent.id)
                return (
                  <div key={agent.id} style={{ background: t.bgSecondary, border: `1px solid ${t.border}`, borderLeft: `4px solid ${color}`, borderRadius: 10, padding: '12px 14px' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 10 }}>
                      <span style={{ fontSize: 18 }}>{regAgent?.emoji || '🤖'}</span>
                      <div style={{ flex: 1 }}>
                        <div style={{ fontSize: 13, fontWeight: 700, color: t.text }}>{regAgent?.name || agent.id}</div>
                        <div style={{ fontSize: 9, color, fontWeight: 700, letterSpacing: '0.08em', textTransform: 'uppercase' }}>{DOMAIN_OF[agent.id] || '—'}</div>
                      </div>
                      <div style={{ fontSize: 9, padding: '2px 7px', borderRadius: 5, background: `${color}18`, color, fontWeight: 700 }}>
                        {agent.tierBaseline !== '?' ? `Tier ${agent.tierBaseline}` : '—'}
                      </div>
                    </div>
                    {[
                      { l: 'Tier A', v: agent.tierA?.[0] || '—', c: '#f59e0b' },
                      { l: 'Tier B', v: agent.tierB?.[0] || '—', c: '#38bdf8' },
                      { l: 'Tier C', v: agent.tierC?.[0] || '—', c: '#34d399' },
                    ].map(({ l, v, c }) => (
                      <div key={l} style={{ display: 'flex', justifyContent: 'space-between', fontSize: 10, marginBottom: 3, padding: '3px 7px', borderRadius: 5, background: t.bg }}>
                        <span style={{ color: c, fontWeight: 700 }}>{l}</span>
                        <span style={{ color: t.textMuted, fontFamily: 'monospace', fontSize: 9 }}>{v}</span>
                      </div>
                    ))}
                  </div>
                )
              })}
            </div>

            {/* SENTINELS groep */}
            <div style={{ fontSize: 11, fontWeight: 700, color: '#34d399', letterSpacing: '0.12em', textTransform: 'uppercase', marginBottom: 4, display: 'flex', alignItems: 'center', gap: 8 }}>
              <div style={{ flex: 1, height: 1, background: '#34d39920' }}/>
              <span>Sentinels</span>
              <div style={{ flex: 1, height: 1, background: '#34d39920' }}/>
            </div>
            <div style={{ display: 'grid', gridTemplateColumns: isMobile ? '1fr' : 'repeat(auto-fill, minmax(280px, 1fr))', gap: 8, marginBottom: 16 }}>
              {modelAgents.filter(a => !['nova','flux','flux_core','cortexia','finoria','saelia','lumeria','fluentia'].includes(a.id)).map(agent => {
                const color = DOMAIN_COLORS[agent.id] || acc
                const regAgent = agents.find(a => a.id === agent.id)
                return (
                  <div key={agent.id} style={{ background: t.bgSecondary, border: `1px solid ${t.border}`, borderLeft: `4px solid ${color}`, borderRadius: 10, padding: '12px 14px' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 10 }}>
                      <span style={{ fontSize: 18 }}>{regAgent?.emoji || '🤖'}</span>
                      <div style={{ flex: 1 }}>
                        <div style={{ fontSize: 13, fontWeight: 700, color: t.text }}>{regAgent?.name || agent.id}</div>
                        <div style={{ fontSize: 9, color, fontWeight: 700, letterSpacing: '0.08em', textTransform: 'uppercase' }}>{DOMAIN_OF[agent.id] || '—'}</div>
                      </div>
                      <div style={{ fontSize: 9, padding: '2px 7px', borderRadius: 5, background: `${color}18`, color, fontWeight: 700 }}>
                        {agent.tierBaseline !== '?' ? `Tier ${agent.tierBaseline}` : '—'}
                      </div>
                    </div>
                    {[
                      { l: 'Tier A', v: agent.tierA?.[0] || '—', c: '#f59e0b' },
                      { l: 'Tier B', v: agent.tierB?.[0] || '—', c: '#38bdf8' },
                      { l: 'Tier C', v: agent.tierC?.[0] || '—', c: '#34d399' },
                    ].map(({ l, v, c }) => (
                      <div key={l} style={{ display: 'flex', justifyContent: 'space-between', fontSize: 10, marginBottom: 3, padding: '3px 7px', borderRadius: 5, background: t.bg }}>
                        <span style={{ color: c, fontWeight: 700 }}>{l}</span>
                        <span style={{ color: t.textMuted, fontFamily: 'monospace', fontSize: 9 }}>{v}</span>
                      </div>
                    ))}
                  </div>
                )
              })}
            </div>

          </div>
        )}

        {/* ── DATABASES ── */}
        {!loading && tab === 'databases' && (
          <div style={{ display: 'flex', flexDirection: 'column', gap: 14 }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 4 }}>
              <div>
                <div style={{ fontSize: 14, fontWeight: 800, color: t.text }}>OpenClaw SQLite Databases</div>
                <div style={{ fontSize: 11, color: t.textMuted, marginTop: 3 }}>
                  Per agent een SQLite DB voor sessie history · Totaal: {(totalDbKb / 1024).toFixed(1)} MB
                </div>
              </div>
            </div>
            <div style={{ background: t.bgSecondary, border: `1px solid ${t.border}`, borderRadius: 12, overflow: 'hidden' }}>
              {/* Header */}
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 120px 120px', padding: '8px 16px', background: t.bgTertiary, borderBottom: `1px solid ${t.border}` }}>
                {['Agent', 'Bestandsnaam', 'Grootte'].map(h => (
                  <div key={h} style={{ fontSize: 9, fontWeight: 700, letterSpacing: '0.1em', textTransform: 'uppercase', color: t.textMuted }}>{h}</div>
                ))}
              </div>
              {/* Rows gesorteerd op grootte */}
              {[...databases].sort((a, b) => b.size_kb - a.size_kb).map((db, i) => {
                const color = DOMAIN_COLORS[db.agent] || acc
                const maxKb = Math.max(...databases.map(d => d.size_kb))
                const pct = Math.round((db.size_kb / maxKb) * 100)
                const regAgent = agents.find(a => a.id === db.agent)
                return (
                  <div key={db.agent} className="oc-row" style={{ display: 'grid', gridTemplateColumns: '1fr 120px 120px', padding: '10px 16px', borderBottom: `1px solid ${t.border}40`, alignItems: 'center', transition: 'background .12s' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                      <span style={{ fontSize: 14 }}>{regAgent?.emoji || '🤖'}</span>
                      <div>
                        <div style={{ fontSize: 12, fontWeight: 600, color: t.text }}>{regAgent?.name || db.agent}</div>
                        <div style={{ display: 'flex', alignItems: 'center', gap: 6, marginTop: 3 }}>
                          <div style={{ width: 80, height: 3, background: t.border, borderRadius: 2, overflow: 'hidden' }}>
                            <div style={{ width: `${pct}%`, height: '100%', background: color, borderRadius: 2 }} />
                          </div>
                          <span style={{ fontSize: 9, color }}>DOMAIN: {DOMAIN_OF[db.agent]?.toUpperCase() || '—'}</span>
                        </div>
                      </div>
                    </div>
                    <span style={{ fontSize: 10, fontFamily: 'ui-monospace,monospace', color: t.textMuted }}>{db.file}</span>
                    <span style={{ fontSize: 12, fontWeight: 700, color: db.size_kb > 7000 ? '#f59e0b' : '#22c55e', fontFamily: 'ui-monospace,monospace' }}>
                      {(db.size_kb / 1024).toFixed(1)} MB
                    </span>
                  </div>
                )
              })}
            </div>
          </div>
        )}

        {/* ── CONFIG ── */}
        {!loading && tab === 'config' && (
          <div style={{ display: 'flex', flexDirection: 'column', gap: 14 }}>
            <div style={{ background: t.bgSecondary, border: `1px solid ${t.border}`, borderRadius: 12, padding: '18px 20px' }}>
              <div style={{ fontSize: 10, fontWeight: 700, letterSpacing: '0.14em', textTransform: 'uppercase', color: t.textMuted, marginBottom: 14 }}>openclaw.json</div>
              {[
                ['Pad', '~/.openclaw/openclaw.json'],
                ['Gateway host', `127.0.0.1:${sysinfo.gateway?.port || '18789'}`],
                ['TLS', sysinfo.gateway?.tls ? 'Aan' : 'Uit'],
                ['Channel', 'stable'],
                ['Versie', `v${sysinfo.version || '—'}`],
                ['Tailscale', 'Uitgeschakeld'],
              ].map(([k, v]) => (
                <div key={k} style={{ display: 'flex', justifyContent: 'space-between', padding: '8px 0', borderBottom: `1px solid ${t.border}50` }}>
                  <span style={{ fontSize: 12, color: t.textMuted }}>{k}</span>
                  <span style={{ fontSize: 12, fontWeight: 600, color: t.text, fontFamily: 'ui-monospace,monospace' }}>{v}</span>
                </div>
              ))}
            </div>

            {configWarnings.length > 0 && (
              <div style={{ background: '#f59e0b08', border: '1px solid #f59e0b40', borderRadius: 12, padding: '18px 20px' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 14 }}>
                  <i className="ti ti-alert-triangle" style={{ fontSize: 16, color: '#f59e0b' }} />
                  <span style={{ fontSize: 13, fontWeight: 700, color: '#f59e0b' }}>Config Waarschuwingen</span>
                </div>
                {configWarnings.map((w, i) => (
                  <div key={i} style={{ padding: '10px 14px', background: '#f59e0b08', borderRadius: 8, marginBottom: 8, border: '1px solid #f59e0b20' }}>
                    <div style={{ fontSize: 12, color: '#f59e0b', fontFamily: 'ui-monospace,monospace', marginBottom: 4 }}>{w}</div>
                    <div style={{ fontSize: 10, color: t.textMuted }}>Fix: <code style={{ color: acc }}>openclaw doctor --fix</code></div>
                  </div>
                ))}
                <div style={{ marginTop: 10, padding: '10px 14px', background: `${acc}08`, borderRadius: 8, fontSize: 11, color: acc, fontFamily: 'ui-monospace,monospace', border: `1px solid ${acc}20` }}>
                  $ openclaw doctor --fix
                </div>
                <button onClick={() => doAction('/api/openclaw/doctor', 'Doctor fix')} style={{ marginTop: 12, padding: '8px 16px', borderRadius: 8, border: `1px solid ${acc}50`, background: `${acc}12`, color: acc, cursor: 'pointer', fontSize: 11, fontWeight: 700 }}>
                  Nu uitvoeren
                </button>
              </div>
            )}

            {/* Update beschikbaar */}
            <div style={{ background: '#a78bfa08', border: '1px solid #a78bfa40', borderRadius: 12, padding: '18px 20px' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 10 }}>
                <i className="ti ti-arrow-up" style={{ fontSize: 16, color: '#a78bfa' }} />
                <span style={{ fontSize: 13, fontWeight: 700, color: '#a78bfa' }}>Update Beschikbaar — v2026.6.1</span>
              </div>
              <div style={{ fontSize: 12, color: t.textMuted, marginBottom: 12, lineHeight: 1.6 }}>
                Voer uit via npm: <code style={{ color: '#a78bfa', fontFamily: 'ui-monospace,monospace' }}>openclaw update</code>
              </div>
              <button onClick={() => doAction('/api/openclaw/update', 'Update')} style={{ padding: '9px 18px', borderRadius: 8, border: '1px solid #a78bfa50', background: '#a78bfa18', color: '#a78bfa', cursor: 'pointer', fontSize: 12, fontWeight: 700 }}>
                <i className="ti ti-arrow-up" /> Nu updaten
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
