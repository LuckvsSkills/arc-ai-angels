import React, { useState, useEffect } from 'react'

export default function CanonTab({ theme }) {
  const t = theme?.colors || {}
  const acc = t.accent || '#c9a84c'
  const [toc, setToc] = useState([])
  const [selected, setSelected] = useState(null)
  const [content, setContent] = useState('')
  const [loading, setLoading] = useState(false)
  const [fontSize, setFontSize] = useState(() => { try { return parseInt(localStorage.getItem('codex_fontsize')||'13') } catch { return 13 } })
  const [winW, setWinW] = useState(window.innerWidth)
  const isMobile = winW < 768

  const changeFontSize = (fn) => setFontSize(prev => { const next = fn(prev); try { localStorage.setItem('codex_fontsize', String(next)) } catch {} return next })

  useEffect(() => {
    const h = () => setWinW(window.innerWidth)
    window.addEventListener('resize', h)
    return () => window.removeEventListener('resize', h)
  }, [])

  useEffect(() => {
    fetch('/api/canon/toc').then(r=>r.json()).then(d => {
      setToc(d.toc||[])
      if (d.toc?.length > 0) loadChapter(d.toc[0].id)
    }).catch(()=>{})
  }, [])

  const loadChapter = (id) => {
    setLoading(true)
    fetch(`/api/canon/chapter/${id}`).then(r=>r.json()).then(d => {
      setSelected(id)
      setContent(d.content||'')
      setLoading(false)
    }).catch(()=>setLoading(false))
  }

  return (
    <div style={{height:'100%',display:'flex',flexDirection:isMobile?'column':'row',overflow:'hidden'}}>
      {/* Sidebar */}
      {(!isMobile || !selected) && (
        <div style={{width:isMobile?'100%':'280px',flexShrink:0,borderRight:isMobile?'none':`1px solid ${t.border}`,borderBottom:isMobile?`1px solid ${t.border}`:'none',overflowY:'auto',background:t.bg,padding:'16px 12px'}}>
          <div style={{fontSize:'9px',color:t.textMuted,letterSpacing:'0.1em',textTransform:'uppercase',marginBottom:'12px'}}>
            CODEX — {toc.length} hoofdstukken
          </div>
          {toc.map(ch => {
            const isActive = selected === ch.id
            return (
              <button key={ch.id} onClick={() => loadChapter(ch.id)} style={{display:'block',width:'100%',textAlign:'left',padding:'10px 12px',marginBottom:'4px',background:isActive?`${acc}15`:'transparent',border:`1px solid ${isActive?acc+'60':t.border}`,borderLeft:`3px solid ${isActive?acc:'transparent'}`,borderRadius:'8px',color:isActive?acc:t.textSecondary,fontSize:'11px',cursor:'pointer'}}>
                {ch.title}
              </button>
            )
          })}
        </div>
      )}

      {/* Content */}
      {(!isMobile || selected) && (
        <div style={{flex:1,overflow:'auto',padding:isMobile?'16px':'24px'}}>
          {isMobile && (
            <button onClick={()=>setSelected(null)} style={{display:'flex',alignItems:'center',gap:'6px',marginBottom:'16px',padding:'6px 12px',background:'transparent',border:`1px solid ${t.border}`,borderRadius:'6px',color:t.textMuted,cursor:'pointer',fontSize:'11px'}}>
              <i className="ti ti-arrow-left" aria-hidden="true"/> Terug
            </button>
          )}
          {loading ? (
            <div style={{color:t.textMuted,fontSize:'12px'}}>⏳ Laden...</div>
          ) : selected ? (
            <div>
              <div style={{display:'flex',alignItems:'center',justifyContent:'space-between',flexWrap:'wrap',gap:'8px',marginBottom:'20px'}}>
                <h2 style={{margin:0,fontSize:isMobile?'18px':'22px',color:t.text,fontWeight:'500'}}>
                  {toc.find(c=>c.id===selected)?.title}
                </h2>
                <div style={{display:'flex',alignItems:'center',gap:'6px'}}>
                  <button onClick={()=>changeFontSize(f=>Math.max(10,f-1))} style={{width:'26px',height:'26px',borderRadius:'6px',background:t.bgSecondary,border:`1px solid ${t.border}`,color:t.textMuted,cursor:'pointer',fontSize:'14px',display:'flex',alignItems:'center',justifyContent:'center'}}>−</button>
                  <span style={{fontSize:'10px',color:t.textMuted,minWidth:'28px',textAlign:'center'}}>{fontSize}px</span>
                  <button onClick={()=>changeFontSize(f=>Math.min(24,f+1))} style={{width:'26px',height:'26px',borderRadius:'6px',background:t.bgSecondary,border:`1px solid ${t.border}`,color:t.textMuted,cursor:'pointer',fontSize:'14px',display:'flex',alignItems:'center',justifyContent:'center'}}>+</button>
                </div>
              </div>
              <pre style={{fontSize:`${fontSize}px`,color:t.textSecondary,lineHeight:1.8,whiteSpace:'pre-wrap',wordBreak:'break-word',margin:0,fontFamily:'inherit'}}>{content}</pre>
            </div>
          ) : <div style={{color:t.textMuted,fontSize:'12px'}}>Selecteer een hoofdstuk</div>}
        </div>
      )}
    </div>
  )
}
