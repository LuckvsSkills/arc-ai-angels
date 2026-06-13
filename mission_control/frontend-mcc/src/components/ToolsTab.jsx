import React, { useState, useEffect } from 'react'

const CAT_CONFIG = {
  storage:       { color: '#c9a84c', icon: 'ti-database',      label: 'Storage' },
  memory:        { color: '#a78bfa', icon: 'ti-brain',          label: 'Memory' },
  search:        { color: '#38bdf8', icon: 'ti-search',         label: 'Search' },
  web:           { color: '#34d399', icon: 'ti-world',          label: 'Web' },
  automation:    { color: '#fb923c', icon: 'ti-robot',          label: 'Automation' },
  governance:    { color: '#f472b6', icon: 'ti-shield',         label: 'Governance' },
  voice:         { color: '#f59e0b', icon: 'ti-microphone',     label: 'Voice' },
  visual:        { color: '#60a5fa', icon: 'ti-photo',          label: 'Visual' },
  code:          { color: '#22c55e', icon: 'ti-code',           label: 'Code' },
  communication: { color: '#e879f9', icon: 'ti-message',        label: 'Communicatie' },
  'ai-model':    { color: '#f97316', icon: 'ti-cpu',            label: 'AI Model' },
}

export default function ToolsTab({ theme }) {
  const t = theme?.colors || {}
  const acc = t.accent || '#c9a84c'
  const [tools, setTools] = useState([])
  const [loading, setLoading] = useState(true)
  const [selected, setSelected] = useState(null)
  const [filterCat, setFilterCat] = useState('all')
  const [search, setSearch] = useState('')
  const [winW, setWinW] = useState(window.innerWidth)
  const isMobile = winW < 700

  useEffect(() => { const h=()=>setWinW(window.innerWidth); window.addEventListener('resize',h); return()=>window.removeEventListener('resize',h) },[])
  useEffect(() => {
    fetch('/api/tools').then(r=>r.json()).then(d=>{ setTools(d.tools||[]); setLoading(false) }).catch(()=>setLoading(false))
  }, [])

  const activeCats = [...new Set(tools.map(t=>t.category))]
  const filtered = tools
    .filter(t => filterCat==='all' || t.category===filterCat)
    .filter(t => !search || t.name?.toLowerCase().includes(search.toLowerCase()) || t.description?.toLowerCase().includes(search.toLowerCase()))

  if (loading) return <div style={{padding:32,color:t.textMuted,fontSize:14}}>Tools laden...</div>

  return (
    <div style={{height:'100%',display:'flex',flexDirection:'column',overflow:'hidden',background:t.bg}}>

      {/* Header */}
      <div style={{flexShrink:0,background:t.bgSecondary,borderBottom:`1px solid ${t.border}`,padding:isMobile?'14px 16px':'16px 22px'}}>
        <div style={{display:'flex',alignItems:'center',gap:12,marginBottom:14,flexWrap:'wrap'}}>
          <div style={{flex:1}}>
            <div style={{fontSize:18,fontWeight:800,color:t.text}}>Tools</div>
            <div style={{fontSize:12,color:t.textMuted,marginTop:3}}>{tools.length} tools beschikbaar · {tools.filter(t=>t.status==='active').length} actief</div>
          </div>
        </div>

        {/* Category filter pills */}
        <div style={{display:'flex',gap:6,flexWrap:'wrap',marginBottom:12}}>
          <button onClick={()=>setFilterCat('all')} style={{padding:'5px 14px',borderRadius:20,fontSize:11,cursor:'pointer',fontWeight:filterCat==='all'?700:400,border:`1px solid ${filterCat==='all'?acc+'60':t.border}`,background:filterCat==='all'?`${acc}15`:'transparent',color:filterCat==='all'?acc:t.textMuted,transition:'all .15s'}}>
            Alle ({tools.length})
          </button>
          {activeCats.map(k => {
            const cfg = CAT_CONFIG[k] || { color: acc, icon: 'ti-tool', label: k }
            const count = tools.filter(t=>t.category===k).length
            return (
              <button key={k} onClick={()=>setFilterCat(k)} style={{display:'flex',alignItems:'center',gap:5,padding:'5px 14px',borderRadius:20,fontSize:11,cursor:'pointer',fontWeight:filterCat===k?700:400,border:`1px solid ${filterCat===k?cfg.color+'60':t.border}`,background:filterCat===k?`${cfg.color}15`:'transparent',color:filterCat===k?cfg.color:t.textMuted,transition:'all .15s'}}>
                <i className={`ti ${cfg.icon}`} style={{fontSize:12}}/>{cfg.label} ({count})
              </button>
            )
          })}
        </div>

        <input value={search} onChange={e=>setSearch(e.target.value)} placeholder="Zoek tool op naam of beschrijving..." style={{padding:'8px 12px',background:t.bgTertiary,border:`1px solid ${t.border}`,borderRadius:8,color:t.text,fontSize:12,fontFamily:'inherit',outline:'none',width:'100%',maxWidth:340}}/>
      </div>

      {/* Grid */}
      <div style={{flex:1,overflow:'auto',padding:isMobile?'14px':'18px 22px',scrollbarWidth:'thin',scrollbarColor:`${acc} transparent`}}>
        <div style={{display:'grid',gridTemplateColumns:isMobile?'1fr':'repeat(auto-fill,minmax(280px,1fr))',gap:12}}>
          {filtered.map(tool => {
            const cfg = CAT_CONFIG[tool.category] || { color: acc, icon: 'ti-tool', label: tool.category }
            const isSelected = selected?.id === tool.id
            const coverage = Math.round(((tool.usedBy?.length||0)/32)*100)
            return (
              <div key={tool.id} onClick={()=>setSelected(isSelected?null:tool)} style={{background:isSelected?`${cfg.color}10`:t.bgSecondary,border:`1px solid ${isSelected?cfg.color+'60':t.border}`,borderTop:`4px solid ${cfg.color}`,borderRadius:12,padding:'14px 16px',cursor:'pointer',transition:'all .15s'}}>
                {/* Header */}
                <div style={{display:'flex',alignItems:'flex-start',gap:10,marginBottom:10}}>
                  <div style={{width:36,height:36,borderRadius:9,background:`${cfg.color}18`,display:'flex',alignItems:'center',justifyContent:'center',flexShrink:0}}>
                    <i className={`ti ${cfg.icon}`} style={{fontSize:18,color:cfg.color}}/>
                  </div>
                  <div style={{flex:1,minWidth:0}}>
                    <div style={{fontSize:14,fontWeight:700,color:t.text,overflow:'hidden',textOverflow:'ellipsis',whiteSpace:'nowrap'}}>{tool.name}</div>
                    <div style={{display:'flex',gap:5,marginTop:4}}>
                      <span style={{fontSize:9,padding:'2px 7px',borderRadius:4,background:`${cfg.color}18`,color:cfg.color,fontWeight:700}}>{cfg.label}</span>
                      <span style={{fontSize:9,padding:'2px 7px',borderRadius:4,background:'#22c55e12',color:'#22c55e',fontWeight:700}}>{tool.status}</span>
                    </div>
                  </div>
                </div>

                <div style={{fontSize:12,color:t.textMuted,lineHeight:1.7,marginBottom:12}}>{tool.description}</div>

                {/* Coverage */}
                <div style={{marginBottom:isSelected?12:0}}>
                  <div style={{display:'flex',justifyContent:'space-between',marginBottom:5,fontSize:11}}>
                    <span style={{color:t.textMuted,display:'flex',alignItems:'center',gap:4}}>
                      <i className="ti ti-users" style={{fontSize:11}}/> {tool.usedBy?.length||0} agents
                    </span>
                    <span style={{color:cfg.color,fontWeight:700}}>{coverage}%</span>
                  </div>
                  <div style={{height:5,background:t.border,borderRadius:3,overflow:'hidden'}}>
                    <div style={{height:'100%',width:`${coverage}%`,background:coverage===0?'#f59e0b':cfg.color,borderRadius:3,transition:'width 0.5s'}}/>
                  </div>
                </div>

                {/* Expanded agents */}
                {isSelected && tool.usedBy && tool.usedBy.length > 0 && (
                  <div style={{paddingTop:10,borderTop:`1px solid ${t.border}`}}>
                    <div style={{fontSize:9,color:t.textMuted,fontWeight:700,letterSpacing:'0.1em',textTransform:'uppercase',marginBottom:7}}>Gebruikt door</div>
                    <div style={{display:'flex',gap:4,flexWrap:'wrap'}}>
                      {tool.usedBy.map(id => (
                        <span key={id} style={{fontSize:10,padding:'3px 8px',borderRadius:5,background:`${cfg.color}12`,color:cfg.color,border:`1px solid ${cfg.color}25`,fontWeight:600}}>{id}</span>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )
          })}
        </div>
      </div>
    </div>
  )
}
