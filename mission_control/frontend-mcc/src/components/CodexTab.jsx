import React, { useState, useEffect, useRef } from 'react'

function parseChapterNumber(id, filename) {
  const match = (filename || '').match(/CH(\d+)/)
  if (match) return parseInt(match[1])
  return id
}

function formatSidebarTitle(title) {
  return title.replace(/^CH\d+\s*[—\-]+\s*/, '')
}

function parseInline(text, t, acc, fontSize) {
  const parts = []
  const regex = /(\*\*[^*]+\*\*|\*[^*]+\*|`[^`]+`)/g
  let last = 0, match, k = 0
  while ((match = regex.exec(text)) !== null) {
    if (match.index > last) parts.push(<span key={k++}>{text.slice(last, match.index)}</span>)
    const token = match[0]
    if (token.startsWith('**')) parts.push(<strong key={k++} style={{ color: t.text, fontWeight: 700 }}>{token.slice(2, -2)}</strong>)
    else if (token.startsWith('*')) parts.push(<em key={k++} style={{ color: acc, fontStyle: 'italic' }}>{token.slice(1, -1)}</em>)
    else if (token.startsWith('`')) parts.push(<code key={k++} style={{ fontFamily: 'ui-monospace,monospace', fontSize: fontSize - 1, color: acc, background: `${acc}15`, padding: '1px 5px', borderRadius: 3 }}>{token.slice(1, -1)}</code>)
    last = match.index + token.length
  }
  if (last < text.length) parts.push(<span key={k++}>{text.slice(last)}</span>)
  return parts.length > 0 ? parts : text
}

function MermaidBlock({ code, t, acc }) {
  const ref = useRef(null)
  const [error, setError] = useState(false)
  const [svgContent, setSvgContent] = useState(null)
  const [fullscreen, setFullscreen] = useState(false)

  useEffect(() => {
    const tryRender = async () => {
      try {
        if (!window.mermaid) { setError(true); return }
        window.mermaid.initialize({
          startOnLoad: false,
          theme: 'dark',
          securityLevel: 'loose',
          themeVariables: {
            primaryColor: acc,
            primaryTextColor: t.text,
            primaryBorderColor: t.border,
            lineColor: t.textMuted,
            background: t.bgSecondary,
            mainBkg: t.bgSecondary,
            fontSize: '16px',
          }
        })
        const id = 'mermaid-' + Math.random().toString(36).slice(2)
        const { svg } = await window.mermaid.render(id, code)
        // Maak SVG responsive en groter
        const enlarged = svg
          .replace(/width="[^"]*"/, 'width="100%"')
          .replace(/height="[^"]*"/, 'height="auto"')
          .replace(/<svg /, '<svg style="min-width:100%;max-width:100%;height:auto;" ')
        setSvgContent(enlarged)
      } catch { setError(true) }
    }
    tryRender()
  }, [code])

  if (error) return (
    <pre style={{ background: t.bgTertiary, border: `1px solid ${t.border}`, borderRadius: 6, padding: '12px 16px', fontSize: 11, color: t.textMuted, fontFamily: 'ui-monospace,monospace', lineHeight: 1.6, margin: '16px 0', overflowX: 'auto' }}>{code}</pre>
  )

  if (!svgContent) return (
    <div style={{ margin: '24px 0', padding: 20, background: t.bgSecondary, border: `1px solid ${t.border}`, borderRadius: 8, color: t.textMuted, fontSize: 12, textAlign: 'center' }}>
      Diagram laden...
    </div>
  )

  return (
    <>
      {/* Fullscreen overlay */}
      {fullscreen && (
        <div
          onClick={() => setFullscreen(false)}
          style={{ position: 'fixed', inset: 0, zIndex: 1000, background: 'rgba(0,0,0,0.92)', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', padding: 20 }}
        >
          <button
            onClick={() => setFullscreen(false)}
            style={{ position: 'absolute', top: 16, right: 16, background: 'transparent', border: `1px solid ${t.border}`, borderRadius: 8, color: t.textMuted, cursor: 'pointer', padding: '6px 12px', fontSize: 12, display: 'flex', alignItems: 'center', gap: 6 }}
          >
            <i className="ti ti-x" /> Sluiten
          </button>
          <div
            style={{ width: '100%', maxWidth: 1000, overflowX: 'auto', overflowY: 'auto', maxHeight: '90vh' }}
            dangerouslySetInnerHTML={{ __html: svgContent }}
          />
        </div>
      )}

      {/* Inline diagram */}
      <div style={{ margin: '24px 0', background: t.bgSecondary, border: `1px solid ${t.border}`, borderRadius: 8, overflow: 'hidden' }}>
        <div style={{ overflowX: 'auto', overflowY: 'hidden', padding: '24px 20px', WebkitOverflowScrolling: 'touch' }}
          dangerouslySetInnerHTML={{ __html: svgContent }}
        />
        <div style={{ borderTop: `1px solid ${t.border}`, padding: '8px 16px', display: 'flex', justifyContent: 'flex-end' }}>
          <button
            onClick={() => setFullscreen(true)}
            style={{ display: 'flex', alignItems: 'center', gap: 6, background: 'transparent', border: `1px solid ${t.border}`, borderRadius: 6, color: t.textMuted, cursor: 'pointer', padding: '5px 10px', fontSize: 10, letterSpacing: '0.05em' }}
          >
            <i className="ti ti-maximize" style={{ fontSize: 12 }} /> Volledig scherm
          </button>
        </div>
      </div>
    </>
  )
}

function renderMarkdown(content, t, acc, fontSize) {
  if (!content) return null
  const lines = content.split('\n')
  const elements = []
  let i = 0, k = 0
  const key = () => k++

  while (i < lines.length) {
    const line = lines[i]
    if (line.trim() === '```mermaid') {
      const mermaidLines = []
      i++
      while (i < lines.length && lines[i].trim() !== '```') { mermaidLines.push(lines[i]); i++ }
      elements.push(<MermaidBlock key={key()} code={mermaidLines.join('\n')} t={t} acc={acc} />)
      i++; continue
    }
    if (line.trim().startsWith('```')) {
      const codeLines = []
      i++
      while (i < lines.length && !lines[i].trim().startsWith('```')) { codeLines.push(lines[i]); i++ }
      elements.push(<pre key={key()} style={{ background: t.bgTertiary, border: `1px solid ${t.border}`, borderRadius: 6, padding: '12px 16px', overflowX: 'auto', fontSize: fontSize - 1, color: acc, fontFamily: 'ui-monospace,monospace', lineHeight: 1.7, margin: '16px 0' }}>{codeLines.join('\n')}</pre>)
      i++; continue
    }
    if (line.startsWith('# ')) {
      const clean = line.slice(2).trim().replace(/^CH\d+\s*[—\-]+\s*/, '')
      elements.push(<h1 key={key()} style={{ fontSize: fontSize + 10, fontWeight: 700, color: t.text, margin: '0 0 6px 0', lineHeight: 1.2, letterSpacing: '-0.02em', fontFamily: 'Georgia,"Times New Roman",serif' }}>{clean}</h1>)
      i++; continue
    }
    if (line.startsWith('## ')) {
      elements.push(<h2 key={key()} style={{ fontSize: fontSize + 4, fontWeight: 600, color: t.text, margin: '32px 0 10px 0', paddingBottom: 8, borderBottom: `1px solid ${t.border}`, fontFamily: 'Georgia,"Times New Roman",serif' }}>{line.slice(3).trim()}</h2>)
      i++; continue
    }
    if (line.startsWith('### ')) {
      elements.push(<h3 key={key()} style={{ fontSize: fontSize + 2, fontWeight: 600, color: acc, margin: '24px 0 8px 0' }}>{line.slice(4).trim()}</h3>)
      i++; continue
    }
    if (line.trim() === '---') {
      elements.push(<div key={key()} style={{ margin: '28px 0', height: 1, background: `linear-gradient(90deg,${acc}40,${t.border},transparent)` }} />)
      i++; continue
    }
    if (line.trim().match(/^\*[^*]+\*$/) || line.trim().match(/^_[^_]+_$/)) {
      const text = line.trim().replace(/^\*|\*$|^_|_$/g, '')
      elements.push(<p key={key()} style={{ fontSize: fontSize + 1, color: acc, fontStyle: 'italic', margin: '0 0 20px 0', lineHeight: 1.7, fontFamily: 'Georgia,"Times New Roman",serif', opacity: 0.85 }}>{text}</p>)
      i++; continue
    }
    if (line.trim() === '') { i++; continue }
    elements.push(<p key={key()} style={{ fontSize, color: t.textSecondary, lineHeight: 1.9, margin: '0 0 14px 0', fontFamily: 'Georgia,"Times New Roman",serif' }}>{parseInline(line.trim(), t, acc, fontSize)}</p>)
    i++
  }
  return elements
}

const VOORWOORD = `# Voorwoord\n\n*Dit is het verhaal van ARC AI AGENTS — een levend systeem, gebouwd met intentie.*\n\n---\n\nDe CODEX is de bron van waarheid van ARC AI AGENTS. Niet een technische handleiding, maar een verhaal. Het verhaal van hoe een systeem van 32 agents tot leven kwam, hoe het denkt, hoe het werkt en waar het naartoe gaat.\n\nElk hoofdstuk beschrijft een laag van het systeem — van het ontstaan tot de toekomst. Lees het als een architect die zijn eigen ontwerp beschrijft. Met trots, maar ook met eerlijkheid over wat er nog moet komen.\n\n**Supreme Fea** — architect, eigenaar, de enige stem die de uiteindelijke richting bepaalt.\n\n---\n\n*Begin bij Hoofdstuk 1 — Het Ontstaan.*`

export default function CodexTab({ theme }) {
  const t = theme?.colors || {}
  const acc = t.accent || '#c9a84c'
  const [toc, setToc] = useState([])
  const [selected, setSelected] = useState(null)
  const [selectedNum, setSelectedNum] = useState(null)
  const [content, setContent] = useState('')
  const [loading, setLoading] = useState(false)
  const [fontSize, setFontSize] = useState(() => { try { return parseInt(localStorage.getItem('codex_fontsize') || '15') } catch { return 15 } })
  const [winW, setWinW] = useState(window.innerWidth)
  const isMobile = winW < 768
  const contentRef = useRef(null)

  useEffect(() => {
    const h = () => setWinW(window.innerWidth)
    window.addEventListener('resize', h)
    return () => window.removeEventListener('resize', h)
  }, [])

  useEffect(() => {
    if (!window.mermaid) {
      const s = document.createElement('script')
      s.src = 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js'
      document.head.appendChild(s)
    }
  }, [])

  useEffect(() => {
    fetch('/api/canon/toc').then(r => r.json()).then(d => {
      setToc(d.toc || [])
    }).catch(() => {})
  }, [])

  const loadChapter = (id, ch) => {
    setLoading(true)
    // Scroll naar boven bij nieuw hoofdstuk
    if (contentRef.current) contentRef.current.scrollTop = 0
    fetch(`/api/canon/chapter/${id}`).then(r => r.json()).then(d => {
      setSelected(id)
      setSelectedNum(parseChapterNumber(id, ch?.filename || ''))
      setContent(d.content || '')
      setLoading(false)
    }).catch(() => setLoading(false))
  }

  const openVoorwoord = () => {
    setSelected('voorwoord')
    setSelectedNum(0)
    setContent(VOORWOORD)
    setLoading(false)
    if (contentRef.current) contentRef.current.scrollTop = 0
  }

  const changeFontSize = (d) => setFontSize(f => {
    const n = Math.max(10, Math.min(24, f + d))
    try { localStorage.setItem('codex_fontsize', String(n)) } catch {}
    return n
  })

  // Navigatie helpers — werken op zowel mobiel als desktop
  const currentIdx = toc.findIndex(c => c.id === selected)
  const prevChapter = currentIdx > 0 ? toc[currentIdx - 1] : null
  const nextChapter = currentIdx >= 0 && currentIdx < toc.length - 1 ? toc[currentIdx + 1] : null

  const NavButtons = () => (
    <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: 48, paddingTop: 20, borderTop: `1px solid ${t.border}` }}>
      {prevChapter ? (
        <button onClick={() => loadChapter(prevChapter.id, prevChapter)} style={{ display: 'flex', alignItems: 'center', gap: 8, padding: '12px 16px', background: 'transparent', border: `1px solid ${t.border}`, borderRadius: 8, color: t.textMuted, cursor: 'pointer', fontSize: 12, minWidth: 120 }}>
          <i className="ti ti-arrow-left" />
          <div style={{ textAlign: 'left' }}>
            <div style={{ fontSize: 9, letterSpacing: '0.1em', textTransform: 'uppercase', marginBottom: 2 }}>Vorige</div>
            <div style={{ fontSize: 11, color: t.text }}>Hfst {parseChapterNumber(prevChapter.id, prevChapter.filename)}</div>
          </div>
        </button>
      ) : <div />}
      {nextChapter && (
        <button onClick={() => loadChapter(nextChapter.id, nextChapter)} style={{ display: 'flex', alignItems: 'center', gap: 8, padding: '12px 16px', background: `${acc}18`, border: `1px solid ${acc}50`, borderRadius: 8, color: acc, cursor: 'pointer', fontSize: 12, minWidth: 120 }}>
          <div style={{ textAlign: 'right' }}>
            <div style={{ fontSize: 9, letterSpacing: '0.1em', textTransform: 'uppercase', marginBottom: 2 }}>Volgende</div>
            <div style={{ fontSize: 11 }}>Hfst {parseChapterNumber(nextChapter.id, nextChapter.filename)}</div>
          </div>
          <i className="ti ti-arrow-right" />
        </button>
      )}
    </div>
  )

  // ── MOBILE ─────────────────────────────────────────────────
  if (isMobile) {
    if (selected) return (
      <div style={{ display: 'flex', flexDirection: 'column', height: '100%', background: t.bg, overflow: 'hidden' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 10, padding: '10px 14px', borderBottom: `1px solid ${t.border}`, background: t.bgSecondary, flexShrink: 0 }}>
          <button onClick={() => setSelected(null)} style={{ display: 'flex', alignItems: 'center', gap: 6, padding: '7px 10px', background: 'transparent', border: `1px solid ${t.border}`, borderRadius: 6, color: t.textMuted, cursor: 'pointer', fontSize: 12, flexShrink: 0 }}>
            <i className="ti ti-arrow-left" /> Terug
          </button>
          <div style={{ flex: 1, fontSize: 12, fontWeight: 600, color: t.text, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
            {selected === 'voorwoord' ? 'Voorwoord' : `Hoofdstuk ${selectedNum}`}
          </div>
          <div style={{ display: 'flex', gap: 4, flexShrink: 0 }}>
            {[[-1,'−'],[1,'+']].map(([d,l]) => (
              <button key={d} onClick={() => changeFontSize(d)} style={{ width: 28, height: 28, borderRadius: 6, background: t.bgTertiary, border: `1px solid ${t.border}`, color: t.textMuted, cursor: 'pointer', fontSize: 14, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>{l}</button>
            ))}
          </div>
        </div>
        <div ref={contentRef} style={{ flex: 1, overflowY: 'auto', padding: '24px 18px', WebkitOverflowScrolling: 'touch' }}>
          {loading ? (
            <div style={{ color: t.textMuted, fontSize: 13 }}>Laden...</div>
          ) : (
            <>
              {renderMarkdown(content, t, acc, fontSize)}
              {selected !== 'voorwoord' && <NavButtons />}
            </>
          )}
        </div>
      </div>
    )

    return (
      <div style={{ height: '100%', overflowY: 'auto', background: t.bg, WebkitOverflowScrolling: 'touch' }}>
        <div style={{ padding: '20px 16px 4px', fontSize: 9, letterSpacing: '0.18em', textTransform: 'uppercase', color: acc, fontWeight: 700 }}>Codex</div>
        <div style={{ padding: '0 16px 12px', fontSize: 9, letterSpacing: '0.1em', textTransform: 'uppercase', color: t.textMuted }}>{toc.length} Hoofdstukken</div>
        <div onClick={openVoorwoord} style={{ display: 'flex', alignItems: 'center', gap: 14, padding: '14px 16px', borderBottom: `1px solid ${t.border}`, cursor: 'pointer', background: selected === 'voorwoord' ? `${acc}10` : 'transparent' }}>
          <div style={{ width: 42, height: 42, borderRadius: 8, background: `${acc}15`, border: `1px solid ${acc}30`, display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0 }}>
            <i className="ti ti-book" style={{ color: acc, fontSize: 18 }} />
          </div>
          <div style={{ flex: 1 }}>
            <div style={{ fontSize: 14, fontWeight: 600, color: t.text, marginBottom: 2 }}>Voorwoord</div>
            <div style={{ fontSize: 11, color: t.textMuted }}>Inleiding tot de CODEX</div>
          </div>
          <i className="ti ti-chevron-right" style={{ color: t.textMuted, fontSize: 16 }} />
        </div>
        {toc.map(ch => {
          const chNum = parseChapterNumber(ch.id, ch.filename)
          const cleanTitle = formatSidebarTitle(ch.title)
          const isActive = selected === ch.id
          return (
            <div key={ch.id} onClick={() => loadChapter(ch.id, ch)} style={{ display: 'flex', alignItems: 'center', gap: 14, padding: '14px 16px', borderBottom: `1px solid ${t.border}`, cursor: 'pointer', background: isActive ? `${acc}10` : 'transparent' }}>
              <div style={{ width: 42, height: 42, borderRadius: 8, background: isActive ? `${acc}20` : t.bgSecondary, border: `1px solid ${isActive ? acc + '50' : t.border}`, display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0 }}>
                <span style={{ fontSize: 13, fontWeight: 700, color: isActive ? acc : t.textMuted, fontFamily: 'ui-monospace,monospace' }}>{String(chNum).padStart(2, '0')}</span>
              </div>
              <div style={{ flex: 1 }}>
                <div style={{ fontSize: 14, fontWeight: isActive ? 600 : 400, color: isActive ? t.text : t.textSecondary, marginBottom: 2 }}>{cleanTitle}</div>
                <div style={{ fontSize: 11, color: t.textMuted }}>{ch.length ? `${Math.round(ch.length / 250)} min leestijd` : ''}</div>
              </div>
              <i className="ti ti-chevron-right" style={{ color: t.textMuted, fontSize: 16 }} />
            </div>
          )
        })}
      </div>
    )
  }

  // ── DESKTOP ────────────────────────────────────────────────
  return (
    <div style={{ height: '100%', display: 'flex', flexDirection: 'row', overflow: 'hidden', background: t.bg }}>
      <div style={{ width: 240, flexShrink: 0, borderRight: `1px solid ${t.border}`, overflowY: 'auto', background: t.bgSecondary, padding: '20px 12px', display: 'flex', flexDirection: 'column', gap: 2 }}>
        <div style={{ fontSize: 9, letterSpacing: '0.18em', textTransform: 'uppercase', color: acc, fontWeight: 700, marginBottom: 4, paddingLeft: 10 }}>Codex</div>
        <div style={{ fontSize: 9, letterSpacing: '0.1em', textTransform: 'uppercase', color: t.textMuted, marginBottom: 16, paddingLeft: 10 }}>{toc.length} Hoofdstukken</div>
        <button onClick={openVoorwoord} style={{ display: 'flex', alignItems: 'flex-start', gap: 10, width: '100%', textAlign: 'left', padding: '9px 10px', marginBottom: 2, background: selected === 'voorwoord' ? `${acc}18` : 'transparent', border: 'none', borderLeft: `3px solid ${selected === 'voorwoord' ? acc : 'transparent'}`, borderRadius: '0 6px 6px 0', color: selected === 'voorwoord' ? acc : t.textMuted, fontSize: 11, cursor: 'pointer', transition: 'all .15s' }}>
          <span style={{ fontSize: 9, fontFamily: 'ui-monospace,monospace', minWidth: 28, opacity: 0.7 }}>—</span>
          <span style={{ fontStyle: 'italic' }}>Voorwoord</span>
        </button>
        {toc.map(ch => {
          const chNum = parseChapterNumber(ch.id, ch.filename)
          const cleanTitle = formatSidebarTitle(ch.title)
          const isActive = selected === ch.id
          return (
            <button key={ch.id} onClick={() => loadChapter(ch.id, ch)} style={{ display: 'flex', alignItems: 'flex-start', gap: 10, width: '100%', textAlign: 'left', padding: '9px 10px', marginBottom: 2, background: isActive ? `${acc}18` : 'transparent', border: 'none', borderLeft: `3px solid ${isActive ? acc : 'transparent'}`, borderRadius: '0 6px 6px 0', color: isActive ? acc : t.textSecondary, fontSize: 11, cursor: 'pointer', transition: 'all .15s', lineHeight: 1.4 }}>
              <span style={{ fontSize: 9, fontFamily: 'ui-monospace,monospace', color: isActive ? acc : t.textMuted, minWidth: 28, paddingTop: 1, opacity: 0.7, flexShrink: 0 }}>{String(chNum).padStart(2, '0')}</span>
              <span>{cleanTitle}</span>
            </button>
          )
        })}
      </div>
      <div ref={contentRef} style={{ flex: 1, overflow: 'auto', background: t.bg }}>
        {loading ? (
          <div style={{ padding: 40, color: t.textMuted, fontSize: 13 }}>Laden...</div>
        ) : selected ? (
          <div style={{ maxWidth: 740, margin: '0 auto', padding: '48px 56px' }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 32 }}>
              <div style={{ fontSize: 10, letterSpacing: '0.2em', textTransform: 'uppercase', color: acc, fontWeight: 700, opacity: 0.8 }}>
                {selected === 'voorwoord' ? 'Voorwoord' : `Hoofdstuk ${selectedNum}`}
              </div>
              <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
                {[[-1,'−'],[1,'+']].map(([d,l]) => (
                  <button key={d} onClick={() => changeFontSize(d)} style={{ width: 26, height: 26, borderRadius: 6, background: t.bgSecondary, border: `1px solid ${t.border}`, color: t.textMuted, cursor: 'pointer', fontSize: 14, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>{l}</button>
                ))}
                <span style={{ fontSize: 9, color: t.textMuted, minWidth: 28, textAlign: 'center' }}>{fontSize}px</span>
              </div>
            </div>
            <div style={{ animation: 'mcc-fadein .3s ease' }}>
              {renderMarkdown(content, t, acc, fontSize)}
            </div>
            {selected !== 'voorwoord' && <NavButtons />}
          </div>
        ) : (
          <div style={{ padding: 40, color: t.textMuted, fontSize: 13 }}>Selecteer een hoofdstuk</div>
        )}
      </div>
    </div>
  )
}
