import React, { useState, useEffect } from 'react'

const TOOL_COLORS = {
  gratis: '#22c55e',
  betaald: '#f59e0b',
  kritiek: '#ef4444',
}

export default function KostenTab({ theme }) {
  const [winW, setWinW] = React.useState(window.innerWidth)
  const isMobile = winW < 768
  React.useEffect(() => {
    const h = () => setWinW(window.innerWidth)
    window.addEventListener('resize', h)
    return () => window.removeEventListener('resize', h)
  }, [])
  const t = theme?.colors || {}
  const acc = t.accent || '#c9a84c'
  const [summary, setSummary] = useState(null)
  const [tiers, setTiers] = useState(null)
  const [ocLogs, setOcLogs] = useState(null)
  const [loading, setLoading] = useState(true)
  const [tab, setTab] = useState('overzicht')

  useEffect(() => {
    Promise.all([
      fetch('/api/costs/summary').then(r=>r.json()).catch(()=>null),
      fetch('/api/costs/tool-tiers').then(r=>r.json()).catch(()=>null),
      fetch('/api/costs/openclaw-tool-logs').then(r=>r.json()).catch(()=>null),
    ]).then(([s, ti, oc]) => {
      setSummary(s)
      setTiers(ti)
      setOcLogs(oc)
      setLoading(false)
    })
  }, [])

  const reload = () => {
    setLoading(true)
    Promise.all([
      fetch('/api/costs/summary').then(r=>r.json()).catch(()=>null),
      fetch('/api/costs/openclaw-tool-logs').then(r=>r.json()).catch(()=>null),
    ]).then(([s, oc]) => {
      setSummary(s)
      setOcLogs(oc)
      setLoading(false)
    })
  }

  if (loading) return <div style={{padding:32,color:t.textMuted,fontSize:13}}>Laden...</div>

  const totals = summary?.totals || {}
  const byTool = ocLogs?.tool_usage || {}

  return (
    <div style={{height:'100%',display:'flex',flexDirection:'column',overflow:'hidden'}}>
      {/* Sub tabs */}
      <div style={{display:'flex',gap:2,padding:'10px 16px 0',borderBottom:`1px solid ${t.border}`,flexShrink:0}}>
        {[['overzicht','ti-coin','Overzicht'],['tools','ti-tools','Tool Tiers'],['log','ti-list','Activiteit Log']].map(([id,icon,label]) => (
          <button key={id} onClick={() => setTab(id)}
            style={{padding:'6px 14px',borderRadius:'7px 7px 0 0',border:`1px solid ${tab===id?t.border:'transparent'}`,borderBottom:tab===id?`1px solid ${t.bgSecondary||'#111'}`:'none',background:tab===id?t.bgSecondary:'transparent',color:tab===id?acc:t.textMuted,fontSize:12,fontWeight:tab===id?700:400,cursor:'pointer',display:'flex',alignItems:'center',gap:5,marginBottom:tab===id?-1:0}}>
            <i className={`ti ${icon}`} style={{fontSize:12}}/>{label}
          </button>
        ))}
        <button onClick={reload} style={{marginLeft:'auto',padding:'6px 10px',background:'transparent',border:'none',color:t.textMuted,cursor:'pointer',fontSize:12}}>
          <i className="ti ti-refresh"/>
        </button>
      </div>

      <div style={{flex:1,overflow:'auto',padding:'16px'}}>

        {tab === 'overzicht' && (
          <div style={{display:'flex',flexDirection:'column',gap:14}}>

            {/* Totaal kaarten */}
            <div style={{display:'grid',gridTemplateColumns:isMobile?'repeat(2,1fr)':'repeat(4,1fr)',gap:10}}>
              {[
                {l:'LLM Kosten',    v:`€${totals.llm_eur?.toFixed(4)||'0.0000'}`,  c:'#38bdf8', icon:'ti-brain',     sub:'token verbruik'},
                {l:'Tool Kosten',   v:`€${totals.tool_eur?.toFixed(4)||'0.0000'}`, c:'#f59e0b', icon:'ti-tools',     sub:'API calls'},
                {l:'Totaal',        v:`€${totals.total_eur?.toFixed(4)||'0.0000'}`,c:acc,       icon:'ti-coin',      sub:'alle kosten'},
                {l:'Vandaag',       v:`€${totals.today_eur?.toFixed(4)||'0.0000'}`,c:'#22c55e', icon:'ti-calendar',  sub:'huidig dag'},
              ].map(s => (
                <div key={s.l} style={{background:`linear-gradient(135deg,${s.c}22 0%,${s.c}08 100%)`,border:`1.5px solid ${s.c}35`,borderRadius:12,padding:'14px 16px',position:'relative',overflow:'hidden'}}>
                  <div style={{position:'absolute',top:0,left:0,right:0,height:2,background:`linear-gradient(90deg,${s.c}00,${s.c}80,${s.c}00)`}}/>
                  <div style={{display:'flex',alignItems:'center',gap:6,marginBottom:8}}>
                    <i className={`ti ${s.icon}`} style={{fontSize:12,color:s.c}}/>
                    <span style={{fontSize:9,fontWeight:700,color:t.textMuted,textTransform:'uppercase',letterSpacing:'0.1em'}}>{s.l}</span>
                  </div>
                  <div style={{fontSize:20,fontWeight:800,color:s.c,fontFamily:'monospace'}}>{s.v}</div>
                  <div style={{fontSize:9,color:t.textMuted,marginTop:2}}>{s.sub}</div>
                </div>
              ))}
            </div>

            {/* Tool gebruik uit OpenClaw logs */}
            <div style={{background:t.bgSecondary,border:`1px solid ${t.border}`,borderRadius:12,padding:'14px 16px'}}>
              <div style={{display:'flex',alignItems:'center',gap:8,marginBottom:12}}>
                <div style={{width:3,height:16,background:'#f59e0b',borderRadius:2}}/>
                <span style={{fontSize:11,fontWeight:700,color:'#f59e0b',textTransform:'uppercase',letterSpacing:'0.1em'}}>Tool Gebruik (OpenClaw logs — 7 dagen)</span>
              </div>
              {Object.keys(byTool).length === 0 ? (
                <div style={{fontSize:11,color:t.textMuted}}>Geen betaalde tool calls gedetecteerd in de logs</div>
              ) : (
                <div style={{display:'flex',flexDirection:'column',gap:6}}>
                  {Object.entries(byTool).map(([tool, data]) => (
                    <div key={tool} style={{background:`linear-gradient(135deg,#f59e0b15 0%,#f59e0b05 100%)`,border:'1.5px solid #f59e0b30',borderRadius:8,padding:'10px 14px',display:'grid',gridTemplateColumns:isMobile?'1fr':'150px 80px 80px 80px 1fr',alignItems:'center',gap:10}}>
                      <span style={{fontSize:12,fontWeight:700,color:t.text,fontFamily:'monospace'}}>{tool}</span>
                      <span style={{fontSize:11,color:t.textMuted}}>{data.calls} calls</span>
                      <span style={{fontSize:11,color:data.failures>0?'#ef4444':'#22c55e'}}>{data.failures} fouten</span>
                      <span style={{fontSize:11,fontWeight:700,color:'#f59e0b'}}>€{data.estimated_cost.toFixed(4)}</span>
                      <div style={{fontSize:9,color:t.textMuted}}>geschatte kosten op basis van call count</div>
                    </div>
                  ))}
                </div>
              )}
            </div>

            {/* Budget waarschuwing */}
            <div style={{background:'linear-gradient(135deg,#ef444415 0%,#ef444405 100%)',border:'1.5px solid #ef444430',borderRadius:12,padding:'14px 16px'}}>
              <div style={{display:'flex',alignItems:'center',gap:8,marginBottom:10}}>
                <i className="ti ti-alert-triangle" style={{fontSize:14,color:'#ef4444'}}/>
                <span style={{fontSize:12,fontWeight:700,color:'#ef4444'}}>Budget Bewaking</span>
              </div>
              <div style={{display:'grid',gridTemplateColumns:isMobile?'1fr':'repeat(2,1fr)',gap:8}}>
                {[
                  {tool:'firecrawl', free:500,  used: byTool.firecrawl?.calls||0, alt:'web-readability'},
                  {tool:'tavily',    free:1000, used: byTool.tavily?.calls||0,    alt:'duckduckgo'},
                  {tool:'exa',       free:1000, used: byTool.exa?.calls||0,       alt:'tavily'},
                  {tool:'perplexity',free:150,  used: byTool.perplexity?.calls||0,alt:'tavily'},
                ].map(item => {
                  const pct = Math.min((item.used/item.free)*100, 100)
                  const color = pct > 80 ? '#ef4444' : pct > 50 ? '#f59e0b' : '#22c55e'
                  return (
                    <div key={item.tool} style={{background:'rgba(0,0,0,0.2)',borderRadius:8,padding:'10px 12px'}}>
                      <div style={{display:'flex',justifyContent:'space-between',marginBottom:4}}>
                        <span style={{fontSize:11,fontWeight:700,color:t.text,fontFamily:'monospace'}}>{item.tool}</span>
                        <span style={{fontSize:10,color}}>
                          {item.used}/{item.free} ({pct.toFixed(0)}%)
                        </span>
                      </div>
                      <div style={{height:4,background:`${t.border}`,borderRadius:2,overflow:'hidden',marginBottom:6}}>
                        <div style={{height:'100%',width:`${pct}%`,background:color,borderRadius:2,transition:'width .4s'}}/>
                      </div>
                      <div style={{fontSize:9,color:t.textMuted}}>Alternatief: <span style={{color:'#22c55e'}}>{item.alt}</span></div>
                    </div>
                  )
                })}
              </div>
            </div>
          </div>
        )}

        {tab === 'tools' && tiers && (
          <div style={{display:'flex',flexDirection:'column',gap:14}}>

            {/* Gratis tools */}
            <div>
              <div style={{display:'flex',alignItems:'center',gap:8,marginBottom:10}}>
                <div style={{width:3,height:16,background:'#22c55e',borderRadius:2}}/>
                <span style={{fontSize:11,fontWeight:700,color:'#22c55e',textTransform:'uppercase',letterSpacing:'0.1em'}}>Gratis Tools — altijd gebruiken</span>
              </div>
              <div style={{display:'grid',gridTemplateColumns:'repeat(auto-fill,minmax(200px,1fr))',gap:8}}>
                {tiers.tiers.gratis.map(tool => (
                  <div key={tool.name} style={{background:'linear-gradient(135deg,#22c55e12 0%,#22c55e04 100%)',border:'1.5px solid #22c55e25',borderRadius:10,padding:'10px 12px'}}>
                    <div style={{fontSize:11,fontWeight:700,color:'#22c55e',fontFamily:'monospace',marginBottom:3}}>{tool.name}</div>
                    <div style={{fontSize:10,color:t.textMuted,marginBottom:4}}>{tool.desc}</div>
                    <div style={{fontSize:9,color:'#22c55e',background:'#22c55e10',borderRadius:4,padding:'1px 6px',display:'inline-block'}}>{tool.limit}</div>
                  </div>
                ))}
              </div>
            </div>

            {/* Betaald met gratis tier */}
            <div>
              <div style={{display:'flex',alignItems:'center',gap:8,marginBottom:10}}>
                <div style={{width:3,height:16,background:'#f59e0b',borderRadius:2}}/>
                <span style={{fontSize:11,fontWeight:700,color:'#f59e0b',textTransform:'uppercase',letterSpacing:'0.1em'}}>Betaald — gratis tier beschikbaar</span>
              </div>
              <div style={{display:'flex',flexDirection:'column',gap:8}}>
                {tiers.tiers.betaald_met_gratis_tier.map(tool => (
                  <div key={tool.name} style={{background:'linear-gradient(135deg,#f59e0b15 0%,#f59e0b05 100%)',border:'1.5px solid #f59e0b30',borderRadius:10,padding:'12px 14px',display:'grid',gridTemplateColumns:isMobile?'1fr':'120px 120px 100px 1fr',alignItems:'center',gap:10}}>
                    <span style={{fontSize:12,fontWeight:700,color:t.text,fontFamily:'monospace'}}>{tool.name}</span>
                    <div>
                      <div style={{fontSize:10,color:'#22c55e'}}>{tool.free} gratis/maand</div>
                      <div style={{fontSize:9,color:'#f59e0b'}}>daarna {tool.cost}</div>
                    </div>
                    <div style={{fontSize:10,color:t.textMuted}}>{tool.desc}</div>
                    <div style={{display:'flex',alignItems:'center',gap:4}}>
                      <span style={{fontSize:9,color:t.textMuted}}>Alternatief:</span>
                      <span style={{fontSize:9,color:'#22c55e',fontWeight:700}}>{tool.alternative}</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Betaald per gebruik */}
            <div>
              <div style={{display:'flex',alignItems:'center',gap:8,marginBottom:10}}>
                <div style={{width:3,height:16,background:'#ef4444',borderRadius:2}}/>
                <span style={{fontSize:11,fontWeight:700,color:'#ef4444',textTransform:'uppercase',letterSpacing:'0.1em'}}>Betaald per gebruik — bewust inzetten</span>
              </div>
              <div style={{display:'flex',flexDirection:'column',gap:8}}>
                {tiers.tiers.betaald_per_gebruik.map(tool => (
                  <div key={tool.name} style={{background:'linear-gradient(135deg,#ef444415 0%,#ef444405 100%)',border:'1.5px solid #ef444430',borderRadius:10,padding:'12px 14px',display:'grid',gridTemplateColumns:isMobile?'1fr':'120px 150px 1fr',alignItems:'center',gap:10}}>
                    <span style={{fontSize:12,fontWeight:700,color:t.text,fontFamily:'monospace'}}>{tool.name}</span>
                    <span style={{fontSize:10,color:'#ef4444'}}>{tool.cost}</span>
                    <div style={{display:'flex',alignItems:'center',gap:4}}>
                      <span style={{fontSize:9,color:t.textMuted}}>{tool.desc} — Alternatief:</span>
                      <span style={{fontSize:9,color:'#22c55e',fontWeight:700}}>{tool.alternative}</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {tab === 'log' && (
          <div style={{display:'flex',flexDirection:'column',gap:10}}>
            <div style={{fontSize:11,color:t.textMuted,lineHeight:1.6,marginBottom:4}}>
              LLM calls worden gelogd via de MCC backend. Tool calls worden gedetecteerd uit OpenClaw gateway logs.
              <strong style={{color:'#f59e0b'}}> Logging is actief — elke agent turn wordt bijgehouden.</strong>
            </div>
            {summary?.recent?.length > 0 ? (
              <div style={{display:'flex',flexDirection:'column',gap:5}}>
                <div style={{display:'grid',gridTemplateColumns:isMobile?'1fr 80px':'140px 100px 1fr 80px 80px',gap:8,padding:'6px 12px',fontSize:9,fontWeight:700,color:t.textMuted,textTransform:'uppercase',letterSpacing:'0.07em'}}>
                  <span>Tijd</span><span>Agent</span><span>Model</span><span>Tokens</span><span>Kosten</span>
                </div>
                {summary.recent.map((r,i) => (
                  <div key={i} style={{background:t.bgSecondary,border:`1px solid ${t.border}`,borderRadius:8,padding:'8px 12px',display:'grid',gridTemplateColumns:isMobile?'1fr 80px':'140px 100px 1fr 80px 80px',gap:8,alignItems:'center'}}>
                    <span style={{fontSize:9,color:t.textMuted,fontFamily:'monospace'}}>{r.timestamp?.slice(0,16)}</span>
                    <span style={{fontSize:10,fontWeight:700,color:acc}}>{r.agent_id}</span>
                    <span style={{fontSize:9,color:t.textMuted,fontFamily:'monospace',overflow:'hidden',textOverflow:'ellipsis',whiteSpace:'nowrap'}}>{r.model}</span>
                    <span style={{fontSize:10,color:t.text}}>{r.tokens?.toLocaleString()}</span>
                    <span style={{fontSize:10,fontWeight:700,color:'#f59e0b'}}>€{r.cost_eur?.toFixed(4)}</span>
                  </div>
                ))}
              </div>
            ) : (
              <div style={{textAlign:'center',color:t.textMuted,padding:32,fontSize:12}}>
                <i className="ti ti-database" style={{fontSize:28,display:'block',marginBottom:10,opacity:0.4}}/>
                Nog geen LLM calls gelogd. Calls worden gelogd zodra agents actief zijn via de MCC backend.
              </div>
            )}
          </div>
        )}

      </div>
    </div>
  )
}
