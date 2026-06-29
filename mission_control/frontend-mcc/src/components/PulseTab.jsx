import React, { useState, useEffect, useCallback } from 'react'

const DOMAIN_COLORS = {
  core:'#c9a84c', helix:'#38bdf8', finix:'#f472b6',
  matrix:'#34d399', quantix:'#a78bfa', zenix:'#fb923c',
}

function successColor(r) {
  if (r === null || r === undefined) return '#4a5568'
  if (r >= 80) return '#22c55e'
  if (r >= 50) return '#f59e0b'
  if (r >= 20) return '#ef4444'
  return '#7f1d1d'
}

function memColor(kb) {
  if (kb > 8) return '#ef4444'
  if (kb > 5) return '#f59e0b'
  return '#22c55e'
}

function Dot({ color, size = 6, pulse = false }) {
  return (
    <span style={{ position: 'relative', display: 'inline-flex', alignItems: 'center', justifyContent: 'center', width: size, height: size, flexShrink: 0 }}>
      {pulse && <span style={{ position: 'absolute', width: size * 2.5, height: size * 2.5, borderRadius: '50%', background: color, opacity: 0.2, animation: 'mcc-pulse 2s infinite' }} />}
      <span style={{ width: size, height: size, borderRadius: '50%', background: color, boxShadow: `0 0 ${size}px ${color}` }} />
    </span>
  )
}

function AgentBlock({ agent, domainColor, onClick, selected }) {
  const sc = successColor(agent.success_rate)
  const isSelected = selected?.id === agent.id

  return (
    <div
      onClick={() => onClick(agent)}
      title={`${agent.id} — success: ${agent.success_rate}% — ${agent.memory_kb}KB — ${agent.tasks_today} taken`}
      style={{
        display: 'flex', flexDirection: 'column', gap: 4,
        padding: '8px 10px', borderRadius: 8, cursor: 'pointer',
        background: isSelected ? `${domainColor}20` : 'var(--p-bg2)',
        border: `1px solid ${isSelected ? domainColor : 'var(--p-border)'}`,
        borderTop: `3px solid ${sc}`,
        transition: 'all .15s', minWidth: 0,
      }}
    >
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: 4 }}>
        <span style={{ fontSize: 11, fontWeight: 700, color: isSelected ? domainColor : 'var(--p-text)', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{agent.id}</span>
        <Dot color={sc} size={5} pulse={agent.success_rate >= 80} />
      </div>
      <div style={{ display: 'flex', gap: 6, fontSize: 9, color: 'var(--p-muted)' }}>
        <span style={{ color: memColor(agent.memory_kb) }}>{agent.memory_kb}KB</span>
        <span>·</span>
        <span style={{ color: sc, fontWeight: 700 }}>{agent.success_rate ?? '—'}%</span>
        <span>·</span>
        <span>{agent.tasks_today ?? 0}t</span>
      </div>
      {/* Mini memory bar */}
      <div style={{ height: 2, background: 'var(--p-border)', borderRadius: 1, overflow: 'hidden' }}>
        <div style={{ height: '100%', width: `${Math.min(100, (agent.memory_lines / 300) * 100)}%`, background: domainColor, opacity: 0.7 }} />
      </div>
    </div>
  )
}

export default function PulseTab({ theme }) {
  const t = theme?.colors || {}
  const acc = t.accent || '#c9a84c'

  const [pulse, setPulse] = useState([])
  const [domains, setDomains] = useState([])
  const [sysStatus, setSysStatus] = useState(null)
  const [loading, setLoading] = useState(true)
  const [selected, setSelected] = useState(null)
  const [memory, setMemory] = useState(null)
  const [memLoading, setMemLoading] = useState(false)
  const [winW, setWinW] = useState(window.innerWidth)
  const isMobile = winW < 768

  useEffect(() => {
    const h = () => setWinW(window.innerWidth)
    window.addEventListener('resize', h)
    return () => window.removeEventListener('resize', h)
  }, [])

  const load = useCallback(async () => {
    setLoading(true)
    const [pulseData, domainData, sysData] = await Promise.all([
      fetch('/api/memory/pulse').then(r => r.json()).catch(() => ({ agents: [], summary: {} })),
      fetch('/api/memory/domains').then(r => r.json()).catch(() => ({ domains: [] })),
      fetch('/api/memory/system-status').then(r => r.json()).catch(() => null),
    ])
    setPulse(pulseData.agents || [])
    setDomains(domainData.domains || [])
    setSysStatus(sysData)
    setLoading(false)
  }, [])

  useEffect(() => { load() }, [load])

  const selectAgent = async (agent) => {
    if (selected?.id === agent.id) { setSelected(null); setMemory(null); return }
    setSelected(agent)
    setMemory(null)
    setMemLoading(true)
    try {
      const d = await fetch(`/api/memory/agents/${agent.id}`).then(r => r.json())
      setMemory(d)
    } catch { setMemory(undefined) }
    setMemLoading(false)
  }

  const getAgent = (id) => pulse.find(a => a.id === id)
  const summary = {
    healthy: pulse.filter(a => a.success_rate >= 50).length,
    warn: pulse.filter(a => a.success_rate < 50 && a.success_rate >= 20).length,
    crit: pulse.filter(a => a.success_rate < 20).length,
    totalKB: pulse.reduce((s, a) => s + (a.memory_kb || 0), 0).toFixed(1),
    totalTasks: pulse.reduce((s, a) => s + (a.tasks_today || 0), 0),
  }

  const cssVars = { '--p-bg': t.bg, '--p-bg2': t.bgSecondary, '--p-bg3': t.bgTertiary, '--p-border': t.border, '--p-text': t.text, '--p-muted': t.textMuted }

  if (loading) return (
    <div style={{ ...cssVars, padding: 32, color: t.textMuted, fontSize: 13, display: 'flex', alignItems: 'center', gap: 10 }}>
      <Dot color={acc} size={8} pulse /> Memory Pulse laden...
    </div>
  )

  return (
    <div style={{ ...cssVars, height: '100%', display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>

      {/* ── HEADER STRIP ── */}
      <div style={{ flexShrink: 0, padding: '12px 18px', background: t.bgSecondary, borderBottom: `1px solid ${t.border}`, display: 'flex', alignItems: 'center', gap: 16, flexWrap: 'wrap' }}>
        <div style={{ flex: 1 }}>
          <div style={{ fontSize: 15, fontWeight: 800, color: t.text }}>Memory Pulse</div>
          <div style={{ fontSize: 10, color: t.textMuted, marginTop: 2 }}>HARNAS geheugen gezondheid · {pulse.length} agents · {summary.totalKB}KB totaal</div>
        </div>

        {/* KPI chips */}
        <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap' }}>
          {[
            { l: 'Gezond', v: summary.healthy, c: '#22c55e' },
            { l: 'Check', v: summary.warn, c: '#f59e0b' },
            { l: 'Kritiek', v: summary.crit, c: '#ef4444' },
            { l: 'Taken', v: summary.totalTasks, c: acc },
          ].map(s => (
            <div key={s.l} style={{ display: 'flex', alignItems: 'center', gap: 5, padding: '4px 10px', borderRadius: 20, background: `${s.c}12`, border: `1px solid ${s.c}30` }}>
              <Dot color={s.c} size={5} pulse={s.v > 0 && s.l !== 'Taken'} />
              <span style={{ fontSize: 12, fontWeight: 800, color: s.c, fontFamily: 'ui-monospace,monospace' }}>{s.v}</span>
              <span style={{ fontSize: 10, color: t.textMuted }}>{s.l}</span>
            </div>
          ))}
        </div>

        {/* Systeem status */}
        {sysStatus && (
          <div style={{ display: 'flex', align: 'center', gap: 6, padding: '4px 12px', borderRadius: 20, background: `${acc}10`, border: `1px solid ${acc}30`, fontSize: 10, color: acc, fontWeight: 700 }}>
            <i className="ti ti-database" style={{ fontSize: 12 }} />
            {sysStatus.agent_memory_used_kb}KB / {sysStatus.agent_memory_limit_kb}KB · {sysStatus.memory_health_percent}% health
          </div>
        )}

        <button onClick={load} style={{ width: 30, height: 30, borderRadius: 7, border: `1px solid ${t.border}`, background: 'transparent', color: t.textMuted, cursor: 'pointer', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 14 }}>
          <i className="ti ti-reload" />
        </button>
      </div>

      {/* ── MAIN SPLIT ── */}
      <div style={{ flex: 1, display: 'flex', overflow: 'hidden', flexDirection: 'row' }}>

        {/* ── DOMEIN HEATMAP ── */}
        {(!isMobile || !selected) && <div style={{ flex: selected ? '0 0 55%' : 1, overflowY: 'auto', padding: '16px 18px', scrollbarWidth: 'thin', scrollbarColor: `${acc} transparent` }}>}
          {domains.map(domain => {
            const color = domain.color || DOMAIN_COLORS[domain.id] || acc
            const domainAgents = domain.agents.map(id => getAgent(id)).filter(Boolean)
            const domainHealthy = domainAgents.filter(a => a.success_rate >= 50).length
            const domainAvgSuccess = domainAgents.length > 0
              ? Math.round(domainAgents.reduce((s, a) => s + (a.success_rate || 0), 0) / domainAgents.length) : 0
            const domainTasks = domainAgents.reduce((s, a) => s + (a.tasks_today || 0), 0)

            return (
              <div key={domain.id} style={{ marginBottom: 20 }}>
                {/* Domain header */}
                <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 10, paddingBottom: 8, borderBottom: `1px solid ${color}30` }}>
                  <div style={{ width: 10, height: 10, borderRadius: '50%', background: color, boxShadow: `0 0 8px ${color}` }} />
                  <span style={{ fontSize: 12, fontWeight: 800, color, letterSpacing: '0.08em', textTransform: 'uppercase' }}>{domain.name}</span>
                  <div style={{ flex: 1, height: 1, background: `${color}20` }} />
                  <span style={{ fontSize: 10, color: t.textMuted }}>{domainHealthy}/{domainAgents.length} gezond</span>
                  <span style={{ fontSize: 10, color, fontWeight: 700 }}>{domainAvgSuccess}% avg</span>
                  <span style={{ fontSize: 10, color: t.textMuted }}>{domainTasks} taken</span>
                </div>

                {/* Agent blokken grid */}
                <div style={{ display: 'grid', gridTemplateColumns: `repeat(auto-fill, minmax(${selected ? '120px' : '140px'}, 1fr))`, gap: 8 }}>
                  {domainAgents.map(agent => (
                    <AgentBlock key={agent.id} agent={agent} domainColor={color} onClick={selectAgent} selected={selected} />
                  ))}
                </div>
              </div>
            )
          })}
        </div>

        {(!isMobile || !selected) && null}
        {/* ── DETAIL PANEL ── */}
        {selected && (
          <div style={{
            width: isMobile ? '100%' : '45%', flexShrink: 0,
            borderLeft: isMobile ? 'none' : `1px solid ${t.border}`,
            display: 'flex', flexDirection: 'column', overflow: isMobile ? 'auto' : 'hidden',
            background: t.bgSecondary,
          }}>
            {/* Detail header */}
            {(() => {
              const domainId = domains.find(d => d.agents.includes(selected.id))?.id
              const color = DOMAIN_COLORS[domainId] || acc
              const sc = successColor(selected.success_rate)
              return (
                <>
                  {isMobile && <button onClick={() => { setSelected(null); setMemory(null) }} style={{fontSize:12,color:t.textMuted,background:'transparent',border:'none',cursor:'pointer',padding:'8px 16px 0',display:'block'}}>← Terug</button>}
                  <div style={{ padding: '14px 16px', borderBottom: `1px solid ${t.border}`, flexShrink: 0, background: `${color}08` }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 8 }}>
                      <div style={{ width: 3, height: 24, background: color, borderRadius: 2 }} />
                      <div style={{ flex: 1 }}>
                        <div style={{ fontSize: 14, fontWeight: 800, color: t.text }}>{selected.id}</div>
                        <div style={{ fontSize: 10, color: t.textMuted, marginTop: 1 }}>{domainId?.toUpperCase()} · memory monitor</div>
                      </div>
                      <div style={{ textAlign: 'right' }}>
                        <div style={{ fontSize: 16, fontWeight: 800, color: sc, fontFamily: 'ui-monospace,monospace' }}>{selected.success_rate ?? '—'}%</div>
                        <div style={{ fontSize: 9, color: t.textMuted }}>success rate</div>
                      </div>
                      <button onClick={() => { setSelected(null); setMemory(null) }} style={{ width: 26, height: 26, borderRadius: 6, border: `1px solid ${t.border}`, background: 'transparent', color: t.textMuted, cursor: 'pointer', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 14 }}>
                        <i className="ti ti-x" />
                      </button>
                    </div>

                    {/* Stats rij */}
                    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4,1fr)', gap: 6 }}>
                      {[
                        { l: 'Memory', v: `${selected.memory_kb}KB`, c: memColor(selected.memory_kb) },
                        { l: 'Regels', v: selected.memory_lines, c: color },
                        { l: 'Taken', v: selected.tasks_today ?? 0, c: acc },
                        { l: 'Crons', v: selected.cronjobs, c: selected.cronjobs >= 4 ? '#22c55e' : '#f59e0b' },
                      ].map(s => (
                        <div key={s.l} style={{ background: t.bgTertiary, borderRadius: 6, padding: '7px 8px', textAlign: 'center' }}>
                          <div style={{ fontSize: 15, fontWeight: 800, color: s.c, fontFamily: 'ui-monospace,monospace', lineHeight: 1 }}>{s.v}</div>
                          <div style={{ fontSize: 8, color: t.textMuted, marginTop: 3, letterSpacing: '0.08em' }}>{s.l}</div>
                        </div>
                      ))}
                    </div>
                  </div>

                  {/* Memory bar */}
                  <div style={{ padding: '10px 16px', borderBottom: `1px solid ${t.border}`, flexShrink: 0 }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 5, fontSize: 10 }}>
                      <span style={{ color: t.textMuted }}>MEMORY.md gebruik</span>
                      <span style={{ color: color, fontWeight: 700 }}>{Math.round((selected.memory_lines / 300) * 100)}% van limiet</span>
                    </div>
                    <div style={{ height: 6, background: t.border, borderRadius: 3, overflow: 'hidden' }}>
                      <div style={{ height: '100%', width: `${Math.min(100, (selected.memory_lines / 300) * 100)}%`, background: color, borderRadius: 3, transition: 'width 0.5s' }} />
                    </div>
                    <div style={{ fontSize: 9, color: t.textMuted, marginTop: 4 }}>
                      Laatste consolidatie: {selected.last_consolidation?.slice(0, 16) || '—'}
                    </div>
                  </div>

                  {/* MEMORY.md content */}
                  <div style={{ flex: 1, overflow: 'hidden', display: 'flex', flexDirection: 'column', padding: '12px 16px' }}>
                    <div style={{ fontSize: 9, fontWeight: 700, letterSpacing: '0.14em', textTransform: 'uppercase', color: t.textMuted, marginBottom: 8, display: 'flex', alignItems: 'center', gap: 6 }}>
                      <i className="ti ti-file-text" style={{ fontSize: 11 }} /> MEMORY.md
                    </div>
                    <div style={{ flex: 1, overflow: 'auto', background: t.bgTertiary, border: `1px solid ${t.border}`, borderRadius: 8, padding: '10px 12px', scrollbarWidth: 'thin', scrollbarColor: `${acc} transparent` }}>
                      {memLoading ? (
                        <div style={{ color: t.textMuted, fontSize: 11, display: 'flex', alignItems: 'center', gap: 6 }}>
                          <Dot color={acc} size={5} pulse /> Laden...
                        </div>
                      ) : memory === undefined ? (
                        <div style={{ color: '#ef4444', fontSize: 11 }}>Niet beschikbaar</div>
                      ) : memory ? (
                        <pre style={{ fontSize: 10, color: t.textSecondary || t.textMuted, lineHeight: 1.8, whiteSpace: 'pre-wrap', wordBreak: 'break-word', margin: 0, fontFamily: 'ui-monospace,monospace' }}>
                          {memory.memory_content || '— MEMORY.md is leeg —'}
                        </pre>
                      ) : null}
                    </div>
                  </div>
                </>
              )
            })()}
          </div>
        )}
      </div>
    </div>
  )
}
