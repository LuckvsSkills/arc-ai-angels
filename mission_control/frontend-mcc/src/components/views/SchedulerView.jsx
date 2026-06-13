import React, { useState, useEffect, useCallback } from 'react'

const DC = {
  nova:'#c9a84c', flux:'#c9a84c',
  cortexia:'#38bdf8', forge:'#38bdf8', nero:'#38bdf8', ventura:'#38bdf8', axon:'#38bdf8', clio:'#38bdf8',
  finoria:'#f472b6', vector:'#f472b6', kairo:'#f472b6', kenzo:'#f472b6', odis:'#f472b6', zion:'#f472b6',
  saelia:'#34d399', tharos:'#34d399', sora:'#34d399', arix:'#34d399', enki:'#34d399', daxio:'#34d399',
  lumeria:'#a78bfa', kresta:'#a78bfa', elora:'#a78bfa', luvia:'#a78bfa', nura:'#a78bfa', vondra:'#a78bfa',
  fluentia:'#fb923c', draven:'#fb923c', solis:'#fb923c', orizon:'#fb923c', unia:'#fb923c', zena:'#fb923c',
}
const DO = {
  nova:'core', flux:'core',
  cortexia:'helix', forge:'helix', nero:'helix', ventura:'helix', axon:'helix', clio:'helix',
  finoria:'finix', vector:'finix', kairo:'finix', kenzo:'finix', odis:'finix', zion:'finix',
  saelia:'matrix', tharos:'matrix', sora:'matrix', arix:'matrix', enki:'matrix', daxio:'matrix',
  lumeria:'quantix', kresta:'quantix', elora:'quantix', luvia:'quantix', nura:'quantix', vondra:'quantix',
  fluentia:'zenix', draven:'zenix', solis:'zenix', orizon:'zenix', unia:'zenix', zena:'zenix',
}
const SLOTS = [
  { time:'00:00', h:0,  label:'Middernacht' },
  { time:'06:00', h:6,  label:'Ochtend' },
  { time:'12:00', h:12, label:'Middag' },
  { time:'18:00', h:18, label:'Avond' },
]
const DCC = { core:'#c9a84c', helix:'#38bdf8', finix:'#f472b6', matrix:'#34d399', quantix:'#a78bfa', zenix:'#fb923c' }

function Dot({ color, size=7, pulse=false }) {
  return (
    <span style={{position:'relative',display:'inline-flex',alignItems:'center',justifyContent:'center',width:size,height:size,flexShrink:0}}>
      {pulse && <span style={{position:'absolute',width:size*2.4,height:size*2.4,borderRadius:'50%',background:color,opacity:0.15,animation:'mcc-pulse 2s infinite'}}/>}
      <span style={{width:size,height:size,borderRadius:'50%',background:color,boxShadow:`0 0 ${size}px ${color}80`}}/>
    </span>
  )
}

function Countdown({ nextSlot }) {
  const [diff, setDiff] = useState('')
  useEffect(() => {
    const tick = () => {
      const now = new Date()
      const utcH = now.getUTCHours(), utcM = now.getUTCMinutes(), utcS = now.getUTCSeconds()
      const [nh] = nextSlot.split(':').map(Number)
      let d = ((nh*3600) - (utcH*3600 + utcM*60 + utcS) + 86400) % 86400
      const h = Math.floor(d/3600), m = Math.floor((d%3600)/60), s = d%60
      setDiff(`${String(h).padStart(2,'0')}:${String(m).padStart(2,'0')}:${String(s).padStart(2,'0')}`)
    }
    tick(); const id = setInterval(tick,1000); return ()=>clearInterval(id)
  }, [nextSlot])
  return <span style={{fontFamily:'ui-monospace,monospace',fontWeight:800}}>{diff}</span>
}

export default function SchedulerView({ theme }) {
  const t = theme?.colors || {}
  const acc = t.accent || '#c9a84c'
  const [agents, setAgents] = useState([])
  const [overview, setOverview] = useState({})
  const [cronjobs, setCronjobs] = useState([])
  const [selected, setSelected] = useState(null)
  const [loading, setLoading] = useState(true)
  const [search, setSearch] = useState('')
  const [filterDomain, setFilterDomain] = useState('all')
  const [winW, setWinW] = useState(window.innerWidth)
  const isMobile = winW < 700

  useEffect(() => { const h=()=>setWinW(window.innerWidth); window.addEventListener('resize',h); return()=>window.removeEventListener('resize',h) },[])

  const load = useCallback(async () => {
    setLoading(true)
    const [full, ov, crons] = await Promise.all([
      fetch('/api/scheduler/full').then(r=>r.json()).catch(()=>({agents:[]})),
      fetch('/api/scheduler/overview').then(r=>r.json()).catch(()=>({})),
      fetch('/api/memory/cronjobs').then(r=>r.json()).catch(()=>({cronjobs:[]})),
    ])
    setAgents(full.agents || [])
    setOverview(ov)
    setCronjobs(crons.cronjobs || [])
    setLoading(false)
  }, [])

  useEffect(() => { load() }, [load])

  const now = new Date()
  const utcH = now.getUTCHours()
  const curSlotIdx = SLOTS.reduce((best,slot,i) => slot.h <= utcH ? i : best, 0)
  const nextSlotIdx = (curSlotIdx+1)%4
  const nextSlot = SLOTS[nextSlotIdx].time
  const completedToday = SLOTS.filter(s => s.h < utcH).length

  const getAgentCrons = (agentId) => cronjobs.filter(j => j.agent_id === agentId)
  const harnasCrons = cronjobs.filter(j => j.id.startsWith('HARNAS-'))
  const otherCrons = cronjobs.filter(j => !j.id.startsWith('HARNAS-'))

  const domains = ['all', ...new Set(agents.map(a => DO[a.agent_id]).filter(Boolean))]
  const filtered = agents
    .filter(a => filterDomain === 'all' || DO[a.agent_id] === filterDomain)
    .filter(a => !search || a.agent_id.toLowerCase().includes(search.toLowerCase()))

  if (loading) return <div style={{padding:32,color:t.textMuted,fontSize:13,display:'flex',alignItems:'center',gap:10}}><Dot color={acc} size={8} pulse/> Scheduler laden...</div>

  return (
    <div style={{height:'100%',display:'flex',flexDirection:'column',overflow:'hidden',background:t.bg}}>

      {/* ── COMPACT HEADER ── */}
      <div style={{flexShrink:0,background:t.bgSecondary,borderBottom:`1px solid ${t.border}`,padding:isMobile?'12px 14px':'14px 20px'}}>

        {/* Title + refresh */}
        <div style={{display:'flex',alignItems:'center',gap:12,marginBottom:12}}>
          <div style={{flex:1}}>
            <div style={{fontSize:16,fontWeight:800,color:t.text}}>Agent Scheduler</div>
            <div style={{fontSize:11,color:t.textMuted,marginTop:2}}>{agents.length} agents · {harnasCrons.length} HARNAS · {otherCrons.length} overige cronjobs</div>
          </div>
          <button onClick={load} style={{width:30,height:30,borderRadius:7,border:`1px solid ${t.border}`,background:'transparent',color:t.textMuted,cursor:'pointer',display:'flex',alignItems:'center',justifyContent:'center',fontSize:14}}>
            <i className="ti ti-reload"/>
          </button>
        </div>

        {/* Stats rij + compacte tijdlijn naast elkaar */}
        <div style={{display:'grid',gridTemplateColumns:isMobile?'1fr':'1fr 1fr',gap:10,marginBottom:12}}>

          {/* Stat blokken */}
          <div style={{display:'grid',gridTemplateColumns:'repeat(4,1fr)',gap:8}}>
            {[
              {l:'Actief', v:overview.active_count||0, c:'#22c55e'},
              {l:'Gemist', v:overview.missed_count||0, c:overview.missed_count>0?'#f59e0b':'#22c55e'},
              {l:'Escalaties', v:overview.escalation_count||0, c:overview.escalation_count>0?'#ef4444':'#22c55e'},
              {l:'Jobs', v:cronjobs.length, c:acc},
            ].map(s => (
              <div key={s.l} style={{background:t.bgTertiary,border:`1px solid ${t.border}`,borderTop:`3px solid ${s.c}`,borderRadius:8,padding:'8px 10px'}}>
                <div style={{fontSize:18,fontWeight:800,color:s.c,fontFamily:'ui-monospace,monospace',lineHeight:1}}>{s.v}</div>
                <div style={{fontSize:9,color:t.textMuted,marginTop:4,letterSpacing:'0.08em',textTransform:'uppercase'}}>{s.l}</div>
              </div>
            ))}
          </div>

          {/* Compacte HARNAS tijdlijn */}
          <div style={{background:t.bgTertiary,border:`1px solid ${t.border}`,borderRadius:8,padding:'10px 14px',display:'flex',alignItems:'center',gap:12}}>
            {/* Slots */}
            <div style={{flex:1,position:'relative'}}>
              <div style={{position:'absolute',top:'50%',left:'8%',right:'8%',height:2,background:t.border,zIndex:0,transform:'translateY(-50%)'}}>
                <div style={{height:'100%',width:`${(completedToday/4)*100}%`,background:acc,transition:'width 1s'}}/>
              </div>
              <div style={{display:'flex',justifyContent:'space-between',position:'relative',zIndex:1}}>
                {SLOTS.map((slot,i) => {
                  const isPast = slot.h < utcH
                  const isCur = i === curSlotIdx
                  const isNext = i === nextSlotIdx
                  return (
                    <div key={slot.time} style={{display:'flex',flexDirection:'column',alignItems:'center',gap:3}}>
                      <div style={{width:isCur?20:13,height:isCur?20:13,borderRadius:'50%',background:isPast?acc:isCur?acc:t.bgSecondary,border:`2px solid ${isPast||isCur?acc:t.border}`,boxShadow:isCur?`0 0 12px ${acc}`:'none',display:'flex',alignItems:'center',justifyContent:'center',transition:'all .3s'}}>
                        {isPast && <i className="ti ti-check" style={{fontSize:8,color:'#000'}}/>}
                        {isCur && <div style={{width:7,height:7,borderRadius:'50%',background:'#000'}}/>}
                      </div>
                      <div style={{fontSize:9,fontFamily:'ui-monospace,monospace',color:isCur?acc:isPast?`${acc}80`:t.textMuted,fontWeight:isCur?700:400}}>{slot.time}</div>
                      {isCur && <div style={{fontSize:7,color:acc,fontWeight:700}}>NU</div>}
                      {isPast && <div style={{fontSize:7,color:'#22c55e'}}>✓</div>}
                      {isNext && !isCur && <div style={{fontSize:7,color:t.textMuted}}>next</div>}
                    </div>
                  )
                })}
              </div>
            </div>
            {/* Countdown */}
            <div style={{flexShrink:0,textAlign:'right'}}>
              <div style={{fontSize:8,color:t.textMuted,letterSpacing:'0.1em',textTransform:'uppercase'}}>Volgende</div>
              <div style={{fontSize:16,color:acc}}><Countdown nextSlot={nextSlot}/></div>
              <div style={{fontSize:9,color:t.textMuted}}>{nextSlot} UTC</div>
            </div>
          </div>
        </div>

        {/* Filters */}
        <div style={{display:'flex',gap:8,flexWrap:'wrap',alignItems:'center'}}>
          <input value={search} onChange={e=>setSearch(e.target.value)} placeholder="Zoek agent..." style={{padding:'6px 10px',background:t.bgTertiary,border:`1px solid ${t.border}`,borderRadius:7,color:t.text,fontSize:11,fontFamily:'inherit',outline:'none',width:160}}/>
          <div style={{display:'flex',gap:4,flexWrap:'wrap'}}>
            {domains.map(d => {
              const color = d==='all' ? acc : DCC[d] || acc
              return (
                <button key={d} onClick={()=>setFilterDomain(d)} style={{padding:'4px 10px',borderRadius:6,fontSize:10,cursor:'pointer',fontWeight:filterDomain===d?700:400,border:`1px solid ${filterDomain===d?color+'60':t.border}`,background:filterDomain===d?`${color}15`:'transparent',color:filterDomain===d?color:t.textMuted,transition:'all .15s'}}>
                  {d==='all'?'Alle':d}
                </button>
              )
            })}
          </div>
          <span style={{fontSize:10,color:t.textMuted}}>{filtered.length}/{agents.length} agents</span>
        </div>
      </div>

      {/* ── CONTENT SPLIT ── */}
      <div style={{flex:1,display:'flex',overflow:'hidden',flexDirection:isMobile&&selected?'column':'row'}}>

        {/* Agent kaarten */}
        <div style={{flex:selected&&!isMobile?'0 0 55%':1,overflowY:'auto',padding:isMobile?'12px 14px':'14px 20px',scrollbarWidth:'thin',scrollbarColor:`${acc} transparent`}}>
          <div style={{display:'grid',gridTemplateColumns:isMobile?'1fr':selected?'repeat(auto-fill,minmax(220px,1fr))':'repeat(auto-fill,minmax(240px,1fr))',gap:10}}>
            {filtered.map(agent => {
              const color = DC[agent.agent_id] || acc
              const hc = agent.health==='active'?'#22c55e':agent.health==='warning'?'#f59e0b':'#ef4444'
              const agentCrons = getAgentCrons(agent.agent_id)
              const harnaCount = agentCrons.filter(j=>j.id.startsWith('HARNAS-')).length
              const otherCount = agentCrons.filter(j=>!j.id.startsWith('HARNAS-')).length
              const hasError = agentCrons.some(j=>j.errors>0)
              const isSelected = selected?.agent_id === agent.agent_id

              return (
                <div key={agent.agent_id} onClick={()=>setSelected(isSelected?null:agent)} style={{background:isSelected?`${color}10`:t.bgSecondary,border:`1px solid ${isSelected?color+'60':t.border}`,borderLeft:`4px solid ${color}`,borderRadius:10,padding:'12px 14px',cursor:'pointer',transition:'all .15s'}}>
                  {/* Header */}
                  <div style={{display:'flex',alignItems:'center',gap:8,marginBottom:10}}>
                    <Dot color={hc} size={7} pulse={agent.health==='active'}/>
                    <span style={{fontSize:13,fontWeight:700,color:t.text,flex:1}}>{agent.agent_id}</span>
                    <span style={{fontSize:9,padding:'2px 7px',borderRadius:4,background:`${color}18`,color,fontWeight:700,letterSpacing:'0.08em'}}>{DO[agent.agent_id]?.toUpperCase()||'—'}</span>
                    {hasError && <span style={{fontSize:9,padding:'2px 5px',borderRadius:4,background:'#f59e0b15',color:'#f59e0b',fontWeight:700}}>!</span>}
                  </div>

                  {/* Stats grid */}
                  <div style={{display:'grid',gridTemplateColumns:'repeat(4,1fr)',gap:5,marginBottom:10}}>
                    {[
                      {l:'Actief',  v:agent.active||0,       c:'#22c55e'},
                      {l:'Gemist',  v:agent.missed||0,       c:agent.missed>0?'#f59e0b':'#22c55e'},
                      {l:'Retry',   v:agent.retry||0,        c:agent.retry>0?'#f59e0b':'#22c55e'},
                      {l:'Escal.',  v:agent.escalations||0,  c:agent.escalations>0?'#ef4444':'#22c55e'},
                    ].map(s => (
                      <div key={s.l} style={{textAlign:'center',padding:'5px 4px',background:t.bgTertiary,borderRadius:5}}>
                        <div style={{fontSize:14,fontWeight:800,color:s.c,fontFamily:'ui-monospace,monospace',lineHeight:1}}>{s.v}</div>
                        <div style={{fontSize:8,color:t.textMuted,marginTop:2,letterSpacing:'0.06em'}}>{s.l}</div>
                      </div>
                    ))}
                  </div>

                  {/* Cronjob info */}
                  <div style={{display:'flex',gap:8,fontSize:10,color:t.textMuted,paddingTop:8,borderTop:`1px solid ${t.border}50`}}>
                    <span style={{color:'#38bdf8',fontWeight:600}}>{harnaCount} HARNAS</span>
                    {otherCount>0 && <span style={{color:t.textMuted}}>+ {otherCount} overig</span>}
                    <span style={{marginLeft:'auto',color:agent.health==='active'?'#22c55e':t.textMuted,fontWeight:600}}>{agent.health}</span>
                  </div>
                </div>
              )
            })}
          </div>
        </div>

        {/* Detail panel */}
        {selected && (
          <div style={{width:isMobile?'100%':'45%',flexShrink:0,borderLeft:isMobile?'none':`1px solid ${t.border}`,borderTop:isMobile?`1px solid ${t.border}`:'none',display:'flex',flexDirection:'column',overflow:'hidden',background:t.bgSecondary}}>
            {(() => {
              const color = DC[selected.agent_id] || acc
              const hc = selected.health==='active'?'#22c55e':selected.health==='warning'?'#f59e0b':'#ef4444'
              const agentCrons = getAgentCrons(selected.agent_id)
              const harnasCronList = agentCrons.filter(j=>j.id.startsWith('HARNAS-'))
              const otherCronList = agentCrons.filter(j=>!j.id.startsWith('HARNAS-'))

              return (
                <>
                  {/* Detail header */}
                  <div style={{padding:'14px 18px',borderBottom:`1px solid ${t.border}`,flexShrink:0,background:`${color}08`}}>
                    <div style={{display:'flex',alignItems:'center',gap:10,marginBottom:12}}>
                      <div style={{width:4,height:28,background:color,borderRadius:2}}/>
                      <div style={{flex:1}}>
                        <div style={{fontSize:15,fontWeight:800,color:t.text}}>{selected.agent_id}</div>
                        <div style={{fontSize:10,color:t.textMuted,marginTop:2}}>{DO[selected.agent_id]?.toUpperCase()} · {agentCrons.length} cronjobs</div>
                      </div>
                      <Dot color={hc} size={8} pulse={selected.health==='active'}/>
                      <span style={{fontSize:12,color:hc,fontWeight:700}}>{selected.health}</span>
                      <button onClick={()=>setSelected(null)} style={{width:28,height:28,borderRadius:7,border:`1px solid ${t.border}`,background:'transparent',color:t.textMuted,cursor:'pointer',display:'flex',alignItems:'center',justifyContent:'center',fontSize:15}}>
                        <i className="ti ti-x"/>
                      </button>
                    </div>

                    {/* Stats */}
                    <div style={{display:'grid',gridTemplateColumns:'repeat(4,1fr)',gap:8,marginBottom:12}}>
                      {[
                        {l:'Actief', v:selected.active||0, c:'#22c55e', icon:'ti-check'},
                        {l:'Gemist', v:selected.missed||0, c:selected.missed>0?'#f59e0b':'#22c55e', icon:'ti-clock-off'},
                        {l:'Retry',  v:selected.retry||0,  c:selected.retry>0?'#f59e0b':'#22c55e', icon:'ti-refresh'},
                        {l:'Escal.', v:selected.escalations||0, c:selected.escalations>0?'#ef4444':'#22c55e', icon:'ti-alert-triangle'},
                      ].map(s => (
                        <div key={s.l} style={{background:t.bgTertiary,border:`1px solid ${t.border}`,borderRadius:8,padding:'10px',textAlign:'center'}}>
                          <i className={`ti ${s.icon}`} style={{fontSize:16,color:s.c,display:'block',marginBottom:5}}/>
                          <div style={{fontSize:20,fontWeight:800,color:s.c,fontFamily:'ui-monospace,monospace'}}>{s.v}</div>
                          <div style={{fontSize:9,color:t.textMuted,marginTop:3}}>{s.l}</div>
                        </div>
                      ))}
                    </div>

                    {/* HARNAS slots voor deze agent */}
                    <div style={{background:t.bgTertiary,border:`1px solid ${t.border}`,borderRadius:8,padding:'10px 14px'}}>
                      <div style={{fontSize:9,fontWeight:700,letterSpacing:'0.12em',textTransform:'uppercase',color:t.textMuted,marginBottom:8}}>HARNAS Schema</div>
                      <div style={{display:'flex',gap:6}}>
                        {SLOTS.map((slot,i) => {
                          const isDone = slot.h < utcH
                          const isCur = i === curSlotIdx
                          const cronForSlot = harnasCronList[i]
                          return (
                            <div key={slot.time} style={{flex:1,textAlign:'center'}}>
                              <div style={{width:16,height:16,borderRadius:'50%',margin:'0 auto 5px',background:isDone?color:isCur?color:t.bgSecondary,border:`2px solid ${isDone||isCur?color:t.border}`,boxShadow:isCur?`0 0 10px ${color}`:'none',display:'flex',alignItems:'center',justifyContent:'center'}}>
                                {isDone && <i className="ti ti-check" style={{fontSize:8,color:'#000'}}/>}
                                {isCur && <div style={{width:6,height:6,borderRadius:'50%',background:'#000'}}/>}
                              </div>
                              <div style={{fontSize:9,color:isCur?color:isDone?`${color}80`:t.textMuted,fontFamily:'ui-monospace,monospace',fontWeight:isCur?700:400}}>{slot.time}</div>
                              <div style={{fontSize:8,color:t.textMuted}}>{slot.label.slice(0,4)}</div>
                            </div>
                          )
                        })}
                      </div>
                    </div>
                  </div>

                  {/* Cronjob lijst */}
                  <div style={{flex:1,overflowY:'auto',padding:'14px 18px',scrollbarWidth:'thin',scrollbarColor:`${acc} transparent`}}>

                    {harnasCronList.length > 0 && (
                      <>
                        <div style={{fontSize:9,fontWeight:700,letterSpacing:'0.14em',textTransform:'uppercase',color:'#38bdf8',marginBottom:8,display:'flex',alignItems:'center',gap:6}}>
                          <div style={{width:2,height:10,background:'#38bdf8',borderRadius:1}}/> HARNAS Cronjobs
                        </div>
                        {harnasCronList.map((job,i) => {
                          const sc = job.errors>0?'#ef4444':job.last_run==='nooit'?'#f59e0b':'#22c55e'
                          return (
                            <div key={i} style={{background:t.bgTertiary,border:`1px solid ${t.border}`,borderLeft:`3px solid ${sc}`,borderRadius:7,padding:'9px 12px',marginBottom:6}}>
                              <div style={{fontSize:11,fontWeight:600,color:t.text,marginBottom:5}}>{job.id}</div>
                              <div style={{display:'flex',gap:12,fontSize:10,color:t.textMuted,flexWrap:'wrap'}}>
                                {job.schedule && <span style={{color:acc,fontFamily:'ui-monospace,monospace'}}>{job.schedule}</span>}
                                <span>Laatste: <strong style={{color:t.text}}>{job.last_run}</strong></span>
                                <span>Volgende: <strong style={{color:t.text}}>{job.next_run}</strong></span>
                                {job.errors>0 && <span style={{color:'#ef4444',fontWeight:700}}>{job.errors} errors</span>}
                              </div>
                            </div>
                          )
                        })}
                      </>
                    )}

                    {otherCronList.length > 0 && (
                      <>
                        <div style={{fontSize:9,fontWeight:700,letterSpacing:'0.14em',textTransform:'uppercase',color:t.textMuted,margin:'12px 0 8px',display:'flex',alignItems:'center',gap:6}}>
                          <div style={{width:2,height:10,background:t.textMuted,borderRadius:1}}/> Overige Cronjobs
                        </div>
                        {otherCronList.map((job,i) => (
                          <div key={i} style={{background:t.bgTertiary,border:`1px solid ${t.border}`,borderRadius:7,padding:'9px 12px',marginBottom:6}}>
                            <div style={{fontSize:11,fontWeight:600,color:t.text,marginBottom:5}}>{job.id}</div>
                            <div style={{display:'flex',gap:12,fontSize:10,color:t.textMuted}}>
                              <span>Laatste: <strong style={{color:t.text}}>{job.last_run}</strong></span>
                              <span style={{color:job.errors>0?'#ef4444':'#22c55e',fontWeight:600}}>{job.errors>0?`${job.errors} errors`:'OK'}</span>
                            </div>
                          </div>
                        ))}
                      </>
                    )}

                    {agentCrons.length === 0 && (
                      <div style={{color:t.textMuted,fontSize:12,textAlign:'center',padding:24}}>Geen cronjobs voor deze agent</div>
                    )}
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
