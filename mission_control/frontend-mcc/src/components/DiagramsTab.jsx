import React, { useState, useEffect, useRef } from 'react'

const TYPE_ICONS = {
  graph:    'ti-hierarchy',
  sequence: 'ti-arrows-exchange',
  timeline: 'ti-timeline',
}

const CHAPTER_COLORS = {
  CH01: '#c9a84c', CH02: '#38bdf8', CH03: '#34d399',
  CH04: '#a78bfa', CH05: '#f472b6', CH06: '#fb923c',
  CH07: '#ef4444', CH08: '#60a5fa', CH09: '#4ade80',
  CH10: '#facc15', CH11: '#e879f9', CH12: '#38bdf8',
}

function chLabel(ch) {
  const num = parseInt((ch || '').replace('CH', ''))
  return isNaN(num) ? ch : `Hoofdstuk ${num}`
}

function loadMermaid() {
  return new Promise((resolve) => {
    if (window.mermaid) { resolve(); return }
    const s = document.createElement('script')
    s.src = 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js'
    s.onload = () => {
      window.mermaid.initialize({ startOnLoad: false, theme: 'dark', securityLevel: 'loose' })
      resolve()
    }
    document.head.appendChild(s)
  })
}

function MermaidRenderer({ diag, t }) {
  const ref = useRef(null)
  const [svg, setSvg] = useState(null)
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (!diag?.content) return
    setSvg(null)
    setError(null)
    setLoading(true)

    loadMermaid().then(async () => {
      try {
        const id = 'mermaid-diag-' + diag.id + '-' + Date.now()
        const { svg: result } = await window.mermaid.render(id, diag.content)
        setSvg(result)
      } catch (e) {
        setError(e.message)
      } finally {
        setLoading(false)
      }
    })
  }, [diag?.id])

  if (loading) return (
    <div style={{ padding: 32, textAlign: 'center', color: t.textMuted, fontSize: 12 }}>
      Diagram renderen...
    </div>
  )

  if (error) return (
    <div>
      <div style={{ color: '#ef4444', fontSize: 11, marginBottom: 12, padding: '8px 12px', background: 'rgba(239,68,68,0.08)', borderRadius: 6, border: '1px solid rgba(239,68,68,0.2)' }}>
        Render fout — broncode:
      </div>
      <pre style={{ fontSize: 11, color: t.textMuted, background: t.bgSecondary, padding: 16, borderRadius: 8, overflow: 'auto', lineHeight: 1.6, margin: 0 }}>
        {diag.content}
      </pre>
    </div>
  )

  return (
    <div
      ref={ref}
      style={{ background: '#0d1117', borderRadius: 8, padding: 24, overflowX: 'auto', display: 'flex', justifyContent: 'center' }}
      dangerouslySetInnerHTML={{ __html: svg }}
    />
  )
}

export default function DiagramsTab({ theme }) {
  const [winW, setWinW] = React.useState(window.innerWidth)
  const isMobile = winW < 768
  React.useEffect(() => {
    const h = () => setWinW(window.innerWidth)
    window.addEventListener('resize', h)
    return () => window.removeEventListener('resize', h)
  }, [])
  const t = theme?.colors || {}
  const acc = t.accent || '#c9a84c'
  const [diagrams, setDiagrams] = useState([])
  const [showDetail, setShowDetail] = React.useState(false)
  const [selected, setSelected] = useState(null)
  const [loading, setLoading] = useState(true)
  const [filter, setFilter] = useState('all')

  useEffect(() => {
    fetch('/api/diagrams/')
      .then(r => r.json())
      .catch(() => ({ diagrams: [] }))
      .then(d => {
        const list = d.diagrams || []
        setDiagrams(list)
        setLoading(false)
        if (list.length > 0) setSelected(list[0])
      })
  }, [])

  const chapters = [...new Set(diagrams.map(d => d.chapter))].sort()
  const filtered = filter === 'all' ? diagrams : diagrams.filter(d => d.chapter === filter)

  if (loading) return (
    <div style={{ padding: 24, color: t.textMuted, fontSize: 12 }}>Diagrammen laden...</div>
  )

  return (
    <div style={{ height: '100%', display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>

      {/* Header */}
      <div style={{ padding: '12px 16px', borderBottom: `1px solid ${t.border}`, flexShrink: 0 }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 10 }}>
          <div style={{ fontSize: 12, fontWeight: 600, color: t.text, display: 'flex', alignItems: 'center', gap: 8 }}>
            <i className="ti ti-schema" style={{ color: acc }} />
            Systeem Diagrammen
          </div>
          <span style={{ fontSize: 10, color: t.textMuted }}>{diagrams.length} diagrammen</span>
        </div>
        {/* Filter buttons */}
        <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap' }}>
          <button onClick={() => setFilter('all')} style={{
            padding: '3px 10px', borderRadius: 12, fontSize: 10, cursor: 'pointer',
            border: `1px solid ${filter === 'all' ? acc : t.border}`,
            background: filter === 'all' ? `${acc}20` : 'transparent',
            color: filter === 'all' ? acc : t.textMuted,
          }}>
            Alle ({diagrams.length})
          </button>
          {chapters.map(ch => {
            const color = CHAPTER_COLORS[ch] || acc
            const count = diagrams.filter(d => d.chapter === ch).length
            return (
              <button key={ch} onClick={() => setFilter(ch)} style={{
                padding: '3px 10px', borderRadius: 12, fontSize: 10, cursor: 'pointer',
                border: `1px solid ${filter === ch ? color : t.border}`,
                background: filter === ch ? `${color}20` : 'transparent',
                color: filter === ch ? color : t.textMuted,
              }}>
                {chLabel(ch)} ({count})
              </button>
            )
          })}
        </div>
      </div>

      {/* Body */}
      <div style={{ flex: 1, display: 'flex', overflow: 'hidden' }}>

        {/* Sidebar */}
        {(!isMobile || !showDetail) && <div style={{ width: isMobile?'100%':240, borderRight: isMobile?'none':`1px solid ${t.border}`, overflowY: 'auto', flexShrink: 0 }}>
          {filtered.map(diag => {
            const color = CHAPTER_COLORS[diag.chapter] || acc
            const icon = TYPE_ICONS[diag.type] || 'ti-schema'
            const isSelected = selected?.id === diag.id
            return (
              <div key={diag.id} onClick={() => setSelected(diag)} style={{
                padding: '10px 14px', cursor: 'pointer',
                borderBottom: `1px solid ${t.border}`,
                background: isSelected ? `${color}12` : 'transparent',
                borderLeft: `3px solid ${isSelected ? color : 'transparent'}`,
                transition: 'all 0.15s',
              }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: 6, marginBottom: 3 }}>
                  <i className={`ti ${icon}`} style={{ color, fontSize: 12 }} />
                  <span style={{ fontSize: 10, fontFamily: 'ui-monospace, monospace', color: isSelected ? color : t.textMuted }}>
                    D{String(diag.id).padStart(2, '0')}
                  </span>
                  <span style={{ fontSize: 9, padding: '1px 6px', borderRadius: 6, background: `${color}18`, color, marginLeft: 'auto' }}>
                    {chLabel(diag.chapter)}
                  </span>
                </div>
                <div style={{ fontSize: 11, color: isSelected ? t.text : t.textSecondary, fontWeight: isSelected ? 600 : 400, marginBottom: 2 }}>
                  {diag.title}
                </div>
                <div style={{ fontSize: 10, color: t.textMuted, lineHeight: 1.4 }}>
                  {diag.description}
                </div>
              </div>
            )
          })}
        </div>

        {/* Diagram weergave */}
        <div style={{ flex: 1, overflowY: 'auto', padding: 20 }}>
          {selected ? (
            <div>
              {/* Diagram header */}
              <div style={{ marginBottom: 20 }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 6, flexWrap: 'wrap' }}>
                  <h3 style={{ margin: 0, fontSize: 16, color: t.text, fontWeight: 600 }}>{selected.title}</h3>
                  <span style={{ fontSize: 9, padding: '2px 8px', borderRadius: 8, background: `${CHAPTER_COLORS[selected.chapter] || acc}18`, color: CHAPTER_COLORS[selected.chapter] || acc }}>
                    {chLabel(selected.chapter)}
                  </span>
                  <span style={{ fontSize: 9, padding: '2px 8px', borderRadius: 8, background: t.bgSecondary, color: t.textMuted, border: `1px solid ${t.border}` }}>
                    {selected.type}
                  </span>
                </div>
                <p style={{ margin: 0, fontSize: 12, color: t.textMuted, lineHeight: 1.6 }}>{selected.description}</p>
              </div>

              {/* Mermaid */}
              <MermaidRenderer key={selected.id} diag={selected} t={t} />

              {/* Broncode toggle */}
              <details style={{ marginTop: 16 }}>
                <summary style={{ fontSize: 10, color: t.textMuted, cursor: 'pointer', letterSpacing: '0.08em', textTransform: 'uppercase' }}>
                  Broncode
                </summary>
                <pre style={{ marginTop: 8, fontSize: 10, color: t.textMuted, background: t.bgSecondary, padding: 14, borderRadius: 8, overflow: 'auto', lineHeight: 1.6, border: `1px solid ${t.border}` }}>
                  {selected.content}
                </pre>
              </details>
            </div>
          ) : (
            <div style={{ color: t.textMuted, fontSize: 12 }}>Selecteer een diagram</div>
          )}
        </div>
      </div>
    </div>
  )
}
