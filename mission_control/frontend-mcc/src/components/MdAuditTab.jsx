import React, { useState, useEffect, useCallback } from 'react'

const DC = { core:'#c9a84c', helix:'#38bdf8', finix:'#f472b6', matrix:'#34d399', quantix:'#a78bfa', zenix:'#fb923c' }
const DO = {
  nova:'core', flux:'core',
  cortexia:'helix', forge:'helix', nero:'helix', ventura:'helix', axon:'helix', clio:'helix',
  finoria:'finix', vector:'finix', kairo:'finix', kenzo:'finix', odis:'finix', zion:'finix',
  saelia:'matrix', tharos:'matrix', sora:'matrix', arix:'matrix', enki:'matrix', daxio:'matrix',
  lumeria:'quantix', kresta:'quantix', elora:'quantix', luvia:'quantix', nura:'quantix', vondra:'quantix',
  fluentia:'zenix', draven:'zenix', solis:'zenix', orizon:'zenix', unia:'zenix', zena:'zenix',
}
const FILE_META = {
  'IDENTITY.md':    { icon: 'ti-id',        color: '#38bdf8' },
  'SOUL.md':        { icon: 'ti-heart',     color: '#f472b6' },
  'TOOLS.md':       { icon: 'ti-tools',     color: '#fb923c' },
  'HEARTBEAT.md':   { icon: 'ti-heartbeat', color: '#ef4444' },
  'AGENTS.md':      { icon: 'ti-users',     color: '#a78bfa' },
  'MEMORY.md':      { icon: 'ti-brain',     color: '#34d399' },
  'README.md':      { icon: 'ti-book',      color: '#c9a84c' },
  'BOOTSTRAP.md':   { icon: 'ti-rocket',    color: '#60a5fa' },
  'AGENT_RULES.md': { icon: 'ti-shield',    color: '#22c55e' },
  'MODEL.md':       { icon: 'ti-cpu',       color: '#f59e0b' },
  'USER.md':        { icon: 'ti-user',      color: '#e879f9' },
}
const fmt = b => !b ? '—' : b < 1024 ? `${b}B` : `${(b/1024).toFixed(1)}KB`

// Detail panel — staat volledig op zichzelf
function AgentModal({ agent, onClose, t, acc }) {
  const [activeFile, setActiveFile] = useState(null)
  const [content, setContent] = useState(null)
  const [loading, setLoading] = useState(false)
  const color = DC[DO[agent.id]] || acc
  const scoreColor = agent.score === 100 ? '#22c55e' : agent.score >= 80 ? '#f59e0b' : '#ef4444'

  const loadFile = useCallback(async (fileName) => {
    setActiveFile(fileName)
    setContent(null)
    setLoading(true)
    try {
      const r = await fetch(`/api/md-audit/agent/${agent.id}/file?path=${encodeURIComponent(fileName)}`)
      const d = await r.json()
      setContent(d.content || d.detail || '— leeg —')
    } catch {
      setContent('Fout bij laden')
    }
    setLoading(false)
  }, [agent.id])

  // Laad eerste file automatisch bij openen
  useEffect(() => {
    const first = agent.files?.find(f => f.exists)
    if (first) loadFile(first.name)
  }, [agent.id])

  return (
    <div style={{ width: '100%', height: '100%', display: 'flex', flexDirection: 'column', overflow: 'hidden', background: '#000' }}>
      {/* Header */}
      <div style={{ padding: '14px 18px', borderBottom: `1px solid ${t.border}`, flexShrink: 0, background: `${color}08` }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 10 }}>
          <div style={{ width: 4, height: 26, background: color, borderRadius: 2 }} />
          <div style={{ flex: 1 }}>
            <div style={{ fontSize: 15, fontWeight: 800, color: t.text }}>{agent.name}</div>
            <div style={{ fontSize: 10, color: t.textMuted }}>{DO[agent.id]?.toUpperCase()} · {agent.files?.filter(f=>f.exists).length}/{agent.files?.length} bestanden</div>
          </div>
          <div style={{ fontSize: 20, fontWeight: 800, color: scoreColor, fontFamily: 'ui-monospace,monospace' }}>{agent.score}%</div>
          <button onClick={onClose} style={{ width: 28, height: 28, borderRadius: 7, border: `1px solid ${t.border}`, background: 'transparent', color: t.textMuted, cursor: 'pointer', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 15 }}>
            <i className="ti ti-x" />
          </button>
        </div>

        {/* File navigatie knoppen */}
        <div style={{ display: 'flex', gap: 5, flexWrap: 'wrap' }}>
          {agent.files?.map(f => {
            const meta = FILE_META[f.name] || { icon: 'ti-file', color: acc }
            const isActive = activeFile === f.name
            return (
              <button
                key={f.name}
                onClick={() => f.exists && loadFile(f.name)}
                disabled={!f.exists}
                style={{
                  display: 'flex', alignItems: 'center', gap: 4,
                  padding: '5px 8px', borderRadius: 7,
                  cursor: f.exists ? 'pointer' : 'not-allowed',
                  border: `1.5px solid ${isActive ? meta.color : f.exists ? meta.color+'40' : t.border}`,
                  background: isActive ? `${meta.color}25` : f.exists ? `${meta.color}10` : 'transparent',
                  opacity: f.exists ? 1 : 0.4,
                  transition: 'all .15s',
                }}
              >
                <i className={`ti ${meta.icon}`} style={{ fontSize: 12, color: isActive ? meta.color : f.exists ? meta.color : t.textMuted }} />
                <span style={{ fontSize: 10, fontWeight: isActive ? 700 : 500, color: isActive ? meta.color : f.exists ? t.text : t.textMuted }}>
                  {f.name.replace('.md', '')}
                </span>
              </button>
            )
          })}
        </div>
      </div>

      {/* Content viewer */}
      <div style={{ flex: 1, overflow: 'hidden', display: 'flex', flexDirection: 'column', padding: '12px 16px', background: t.bgSecondary }}>
        {activeFile && (
          <div style={{ fontSize: 9, fontWeight: 700, letterSpacing: '0.14em', textTransform: 'uppercase', color: t.textMuted, marginBottom: 8 }}>
            <i className={`ti ${FILE_META[activeFile]?.icon || 'ti-file'}`} style={{ fontSize: 10, marginRight: 5, color: FILE_META[activeFile]?.color || acc }} />
            {activeFile}
          </div>
        )}
        <div style={{ flex: 1, overflow: 'auto', background: t.bgTertiary, border: `1px solid ${t.border}`, borderRadius: 9, padding: '12px 14px', scrollbarWidth: 'thin', scrollbarColor: `${acc} transparent` }}>
          {!activeFile && (
            <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '100%', color: t.textMuted, gap: 8 }}>
              <i className="ti ti-file-text" style={{ fontSize: 28, opacity: 0.3 }} />
              <div style={{ fontSize: 12 }}>Klik een bestand hierboven</div>
            </div>
          )}
          {activeFile && loading && (
            <div style={{ color: t.textMuted, fontSize: 12 }}>Laden...</div>
          )}
          {activeFile && !loading && content && (
            <pre style={{ fontSize: 11, color: t.textSecondary || t.textMuted, lineHeight: 1.9, whiteSpace: 'pre-wrap', wordBreak: 'break-word', margin: 0, fontFamily: 'ui-monospace,monospace' }}>
              {content}
            </pre>
          )}
        </div>
      </div>
    </div>
  )
}

export default function MdAuditTab({ theme }) {
  const t = theme?.colors || {}
  const acc = t.accent || '#c9a84c'
  const [agents, setAgents] = useState([])
  const [loading, setLoading] = useState(true)
  const [selected, setSelected] = useState(null)
  const [selectedFile, setSelectedFile] = useState(null)
  const [fileContent, setFileContent] = useState(null)
  const [fileLoading, setFileLoading] = useState(false)
  const [filterScore, setFilterScore] = useState('all')
  const [search, setSearch] = useState('')
  const [winW, setWinW] = useState(window.innerWidth)
  const isMobile = winW < 768

  useEffect(() => {
    const h = () => setWinW(window.innerWidth)
    window.addEventListener('resize', h)
    return () => window.removeEventListener('resize', h)
  }, [])

  // Laad file content als selectedFile verandert
  useEffect(() => {
    if (!selected || !selectedFile) return
    setFileContent(null)
    setFileLoading(true)
    fetch(`/api/md-audit/agent/${selected.id}/file?path=${encodeURIComponent(selectedFile)}`)
      .then(r => r.json())
      .then(d => { setFileContent(d.content || d.detail || '— leeg —'); setFileLoading(false) })
      .catch(() => { setFileContent('Fout bij laden'); setFileLoading(false) })
  }, [selected?.id, selectedFile])

  // Reset file als agent wisselt
  useEffect(() => {
    if (selected) {
      const first = selected.files?.find(f => f.exists)
      if (first) setSelectedFile(first.name)
    } else {
      setSelectedFile(null)
      setFileContent(null)
    }
  }, [selected?.id])

  useEffect(() => {
    fetch('/api/md-audit/overview').then(r => r.json()).then(d => {
      setAgents(d.agents || [])
      setLoading(false)
    }).catch(() => setLoading(false))
  }, [])

  const filtered = agents
    .filter(a => filterScore === 'all' || (filterScore === '100' ? a.score === 100 : a.score < 100))
    .filter(a => !search || a.name?.toLowerCase().includes(search.toLowerCase()) || a.id?.toLowerCase().includes(search.toLowerCase()))

  const perfect = agents.filter(a => a.score === 100).length
  const incomplete = agents.filter(a => a.score < 100).length
  const avgScore = agents.length > 0 ? Math.round(agents.reduce((s, a) => s + (a.score || 0), 0) / agents.length) : 0
  const allFiles = agents[0]?.files?.map(f => f.name) || []

  if (loading) return <div style={{ padding: 32, color: t.textMuted, fontSize: 14 }}>MD Audit laden...</div>

  // Als er een agent geselecteerd is op mobiel — toon alleen detail
  if (isMobile && selected) {
    return (
      <div style={{ height: '100%', display: 'flex', flexDirection: 'column', overflow: 'hidden', background: t.bgSecondary }}>
        <AgentModal agent={selected} onClose={() => setSelected(null)} t={t} acc={acc} />
      </div>
    )
  }

  return (
    <div style={{ height: '100%', display: 'flex', flexDirection: 'column', overflow: 'hidden', background: t.bg }}>

      {/* Header */}
      <div style={{ flexShrink: 0, background: t.bgSecondary, borderBottom: `1px solid ${t.border}`, padding: isMobile ? '14px 16px' : '16px 22px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 14, flexWrap: 'wrap' }}>
          <div style={{ flex: 1 }}>
            <div style={{ fontSize: 18, fontWeight: 800, color: t.text }}>MD Audit</div>
            <div style={{ fontSize: 12, color: t.textMuted, marginTop: 3 }}>
              Documentatie volledigheid · {agents.length} agents · {allFiles.length} bestanden per agent
            </div>
          </div>
          <div style={{ display: 'flex', gap: 10 }}>
            {[
              { l: 'Compleet', v: perfect, c: '#22c55e' },
              { l: 'Incompleet', v: incomplete, c: incomplete > 0 ? '#f59e0b' : '#22c55e' },
              { l: 'Gemiddeld', v: `${avgScore}%`, c: acc },
            ].map(s => (
              <div key={s.l} style={{ textAlign: 'center', padding: '8px 14px', borderRadius: 9, background: `${s.c}12`, border: `1px solid ${s.c}30` }}>
                <div style={{ fontSize: 20, fontWeight: 800, color: s.c, fontFamily: 'ui-monospace,monospace', lineHeight: 1 }}>{s.v}</div>
                <div style={{ fontSize: 10, color: t.textMuted, marginTop: 4 }}>{s.l}</div>
              </div>
            ))}
          </div>
        </div>

        {/* File legenda */}
        <div style={{ display: 'flex', gap: 5, flexWrap: 'wrap', marginBottom: 12 }}>
          {allFiles.map(fn => {
            const meta = FILE_META[fn] || { icon: 'ti-file', color: acc }
            const pct = Math.round((agents.filter(a => a.files?.find(f => f.name === fn && f.exists)).length / agents.length) * 100)
            return (
              <div key={fn} title={`${fn}: ${pct}%`} style={{ display: 'flex', alignItems: 'center', gap: 4, padding: '3px 8px', borderRadius: 6, background: `${meta.color}12`, border: `1px solid ${meta.color}30` }}>
                <i className={`ti ${meta.icon}`} style={{ fontSize: 11, color: meta.color }} />
                <span style={{ fontSize: 9, color: meta.color, fontWeight: 700 }}>{fn.replace('.md', '')}</span>
                <span style={{ fontSize: 9, color: t.textMuted }}>{pct}%</span>
              </div>
            )
          })}
        </div>

        {/* Filters */}
        <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap', alignItems: 'center' }}>
          <input value={search} onChange={e => setSearch(e.target.value)} placeholder="Zoek agent..." style={{ padding: '7px 12px', background: t.bgTertiary, border: `1px solid ${t.border}`, borderRadius: 8, color: t.text, fontSize: 12, fontFamily: 'inherit', outline: 'none', width: 180 }} />
          {[['all', 'Alle'], ['100', '100%'], ['incomplete', 'Incompleet']].map(([v, l]) => (
            <button key={v} onClick={() => setFilterScore(v)} style={{ padding: '6px 14px', borderRadius: 7, fontSize: 11, cursor: 'pointer', fontWeight: filterScore === v ? 700 : 400, border: `1px solid ${filterScore === v ? acc+'60' : t.border}`, background: filterScore === v ? `${acc}15` : 'transparent', color: filterScore === v ? acc : t.textMuted }}>
              {l}
            </button>
          ))}
          <span style={{ fontSize: 11, color: t.textMuted }}>{filtered.length}/{agents.length}</span>
        </div>
      </div>

      {/* Split: kaarten links, detail rechts */}
      <div style={{ flex: 1, display: 'flex', overflow: 'hidden' }}>

        {/* Agent kaarten */}
        <div style={{ flex: 1, overflowY: 'auto', padding: isMobile ? '14px' : '16px 20px', scrollbarWidth: 'thin', scrollbarColor: `${acc} transparent` }}>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill,minmax(260px,1fr))', gap: 12 }}>
            {filtered.map(agent => {
              const color = DC[DO[agent.id]] || acc
              const isSelected = selected?.id === agent.id
              const scoreColor = agent.score === 100 ? '#22c55e' : agent.score >= 80 ? '#f59e0b' : '#ef4444'
              const existsCount = agent.files?.filter(f => f.exists).length || 0
              const totalCount = agent.files?.length || 0

              return (
                <div
                  key={agent.id}
                  style={{
                    position: isSelected ? 'relative' : 'relative',
                    zIndex: isSelected ? 10 : 1,
                    gridColumn: isSelected ? '1 / -1' : 'auto',
                  }}
                >
                  {/* Compacte header — altijd zichtbaar */}
                  <div
                    onClick={() => setSelected(isSelected ? null : agent)}
                    style={{
                      background: isSelected ? `${color}18` : t.bgSecondary,
                      border: `1px solid ${isSelected ? color+'80' : t.border}`,
                      borderTop: `4px solid ${color}`,
                      borderRadius: isSelected ? '12px 12px 0 0' : 12,
                      padding: '12px 16px',
                      cursor: 'pointer', transition: 'all .15s',
                    }}
                  >
                    <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
                      <div style={{ flex: 1 }}>
                        <div style={{ fontSize: 14, fontWeight: 700, color: t.text }}>{agent.name}</div>
                        <div style={{ fontSize: 10, color, fontWeight: 700, letterSpacing: '0.08em', textTransform: 'uppercase', marginTop: 1 }}>{DO[agent.id] || '—'}</div>
                      </div>
                      <div style={{ textAlign: 'right' }}>
                        <div style={{ fontSize: 20, fontWeight: 800, color: scoreColor, fontFamily: 'ui-monospace,monospace', lineHeight: 1 }}>{agent.score}%</div>
                        <div style={{ fontSize: 9, color: t.textMuted, marginTop: 1 }}>{existsCount}/{totalCount} files</div>
                      </div>
                      <i className={`ti ${isSelected ? 'ti-chevron-up' : 'ti-chevron-down'}`} style={{ fontSize: 14, color: t.textMuted, marginLeft: 4 }}/>
                    </div>
                    {/* Score bar */}
                    <div style={{ height: 3, background: t.border, borderRadius: 2, overflow: 'hidden', marginTop: 8 }}>
                      <div style={{ height: '100%', width: `${agent.score}%`, background: scoreColor }} />
                    </div>
                  </div>

                  {/* Expanded: file sidebar + content */}
                  {isSelected && (
                    <div style={{
                      border: `1px solid ${color+'80'}`, borderTop: 'none',
                      borderRadius: '0 0 12px 12px',
                      background: t.bg,
                      display: 'flex', height: 480,
                      overflow: 'hidden',
                      boxShadow: `0 8px 32px rgba(0,0,0,0.4)`,
                    }}>
                      {/* File lijst */}
                      <div style={{ width: 190, flexShrink: 0, borderRight: `1px solid ${t.border}`, background: t.bgSecondary, overflowY: 'auto', padding: '8px 6px', display: 'flex', flexDirection: 'column', gap: 3, scrollbarWidth: 'thin' }}>
                        <div style={{ fontSize: 9, fontWeight: 700, letterSpacing: '0.12em', textTransform: 'uppercase', color: t.textMuted, padding: '3px 8px', marginBottom: 4 }}>Bestanden</div>
                        {agent.files?.map(f => {
                          const meta = FILE_META[f.name] || { icon: 'ti-file', color: acc }
                          const isActiveFile = selected?.id === agent.id && /* use AgentModal activeFile */ false
                          return (
                            <button key={f.name} onClick={e => { e.stopPropagation(); if (f.exists) { setSelected(agent); setSelectedFile(f.name) } }} disabled={!f.exists} style={{
                              display: 'flex', alignItems: 'center', gap: 8,
                              padding: '8px 10px', borderRadius: 8,
                              cursor: f.exists ? 'pointer' : 'default',
                              border: `1px solid ${selectedFile === f.name ? meta.color+'60' : 'transparent'}`,
                              background: selectedFile === f.name ? `${meta.color}18` : 'transparent',
                              opacity: f.exists ? 1 : 0.35, textAlign: 'left',
                              transition: 'all .15s',
                            }}>
                              <div style={{ width: 26, height: 26, borderRadius: 6, background: `${meta.color}18`, display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0 }}>
                                <i className={`ti ${meta.icon}`} style={{ fontSize: 13, color: selectedFile === f.name ? meta.color : f.exists ? meta.color : t.textMuted }}/>
                              </div>
                              <div>
                                <div style={{ fontSize: 11, fontWeight: selectedFile === f.name ? 700 : 500, color: selectedFile === f.name ? meta.color : f.exists ? t.text : t.textMuted }}>
                                  {f.name.replace('.md', '')}
                                </div>
                                <div style={{ fontSize: 9, color: t.textMuted }}>{f.exists ? fmt(f.size) : 'ontbreekt'}</div>
                              </div>
                            </button>
                          )
                        })}
                      </div>

                      {/* Content */}
                      <div style={{ flex: 1, overflow: 'hidden', display: 'flex', flexDirection: 'column' }}>
                        {selectedFile && (
                          <div style={{ padding: '10px 16px', borderBottom: `1px solid ${t.border}`, flexShrink: 0, background: t.bgSecondary, display: 'flex', alignItems: 'center', gap: 8 }}>
                            <i className={`ti ${FILE_META[selectedFile]?.icon || 'ti-file'}`} style={{ fontSize: 14, color: FILE_META[selectedFile]?.color || acc }}/>
                            <span style={{ fontSize: 13, fontWeight: 700, color: t.text }}>{selectedFile}</span>
                          </div>
                        )}
                        <div style={{ flex: 1, overflow: 'auto', padding: '14px 18px', scrollbarWidth: 'thin', scrollbarColor: `${acc} transparent` }}>
                          {!selectedFile && (
                            <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '100%', color: t.textMuted, gap: 8 }}>
                              <i className="ti ti-file-text" style={{ fontSize: 32, opacity: 0.2 }}/>
                              <div style={{ fontSize: 13 }}>Selecteer een bestand links</div>
                            </div>
                          )}
                          {selectedFile && fileLoading && <div style={{ color: t.textMuted, fontSize: 13 }}>Laden...</div>}
                          {selectedFile && !fileLoading && fileContent && (
                            <pre style={{ fontSize: 13, color: t.textSecondary || t.textMuted, lineHeight: 1.9, whiteSpace: 'pre-wrap', wordBreak: 'break-word', margin: 0, fontFamily: 'ui-monospace,monospace' }}>
                              {fileContent}
                            </pre>
                          )}
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              )
            })}
          </div>
        </div>


      </div>
    </div>
  )
}
