import React, { useState, useEffect } from 'react'

const DOMAIN_COLORS = {
  core:'#c9a84c', helix:'#38bdf8', finix:'#f472b6',
  matrix:'#34d399', quantix:'#a78bfa', zenix:'#fb923c', unknown:'#6b7280'
}
const STATUS_COLORS = {
  IN_PROGRESS:'#38bdf8', BLOCKED:'#ef4444', OPEN:'#f59e0b',
  DONE:'#22c55e', CLOSED:'#6b7280', UNKNOWN:'#6b7280'
}
const PRIORITY_COLORS = { HIGH:'#ef4444', NORMAL:'#f59e0b', LOW:'#22c55e' }

export default function TasksView({ theme }) {
  const t = theme?.colors || {}
  const acc = t.accent || '#c9a84c'
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [filter, setFilter] = useState('active')
  const [domain, setDomain] = useState('all')
  const [selected, setSelected] = useState(null)

  const load = () => {
    setLoading(true)
    fetch('/api/tasks/all')
      .then(r => r.json())
      .then(d => { setData(d); setLoading(false) })
      .catch(() => setLoading(false))
  }

  useEffect(() => { load() }, [])

  if (loading) return <div style={{padding:32,color:t.textMuted,fontSize:13}}>Laden...</div>

  const tasks = data?.tasks || []

  // Filters
  const filtered = tasks.filter(t2 => {
    const statusOk = filter === 'all' ? true :
      filter === 'active' ? ['IN_PROGRESS','BLOCKED','OPEN'].includes(t2.status) :
      filter === 'blocked' ? t2.status === 'BLOCKED' :
      filter === 'done' ? ['DONE','CLOSED'].includes(t2.status) : true
    const domainOk = domain === 'all' ? true : t2.domain === domain
    return statusOk && domainOk
  })

  return (
    <div style={{height:'100%',display:'flex',flexDirection:'column',overflow:'hidden'}}>

      {/* Header */}
      <div style={{padding:'12px 16px',borderBottom:`1px solid ${t.border}`,flexShrink:0}}>
        <div style={{display:'flex',alignItems:'center',justifyContent:'space-between',marginBottom:10}}>
          <div>
            <div style={{fontSize:14,fontWeight:700,color:t.text}}>Task Manager</div>
            <div style={{fontSize:11,color:t.textMuted,marginTop:1}}>
              {data?.total} taken — {data?.by_status?.in_progress} actief · {data?.by_status?.blocked} geblokkeerd · {data?.by_status?.done} klaar
            </div>
          </div>
          <button onClick={load} style={{padding:'6px 10px',borderRadius:7,border:`1px solid ${t.border}`,background:'transparent',color:t.textMuted,cursor:'pointer',fontSize:11,display:'flex',alignItems:'center',gap:4}}>
            <i className="ti ti-refresh" style={{fontSize:12}}/> Vernieuwen
          </button>
        </div>

        {/* Status filter */}
        <div style={{display:'flex',gap:6,marginBottom:8,flexWrap:'wrap'}}>
          {[
            ['active','Actief',data?.by_status?.in_progress,'#38bdf8'],
            ['blocked','Geblokkeerd',data?.by_status?.blocked,'#ef4444'],
            ['done','Klaar',data?.by_status?.done,'#22c55e'],
            ['all','Alles',data?.total,'#6b7280'],
          ].map(([id,label,count,color]) => (
            <button key={id} onClick={() => setFilter(id)}
              style={{padding:'4px 10px',borderRadius:6,border:`1.5px solid ${filter===id?color:t.border}`,background:filter===id?`${color}15`:'transparent',color:filter===id?color:t.textMuted,fontSize:10,fontWeight:filter===id?700:400,cursor:'pointer',display:'flex',alignItems:'center',gap:4}}>
              {label} <span style={{fontSize:9,opacity:0.7}}>({count||0})</span>
            </button>
          ))}
        </div>

        {/* Domain filter */}
        <div style={{display:'flex',gap:4,flexWrap:'wrap'}}>
          {['all','core','helix','finix','matrix','quantix','zenix'].map(d => (
            <button key={d} onClick={() => setDomain(d)}
              style={{padding:'3px 8px',borderRadius:5,border:`1px solid ${domain===d?(DOMAIN_COLORS[d]||acc):t.border}`,background:domain===d?`${DOMAIN_COLORS[d]||acc}15`:'transparent',color:domain===d?(DOMAIN_COLORS[d]||acc):t.textMuted,fontSize:9,fontWeight:domain===d?700:400,cursor:'pointer',textTransform:'capitalize'}}>
              {d}
            </button>
          ))}
        </div>
      </div>

      <div style={{flex:1,overflow:'auto',display:'flex'}}>
        {/* Task lijst */}
        <div style={{flex:1,overflow:'auto',padding:'10px 16px',display:'flex',flexDirection:'column',gap:6}}>
          {filtered.length === 0 ? (
            <div style={{textAlign:'center',color:t.textMuted,padding:40,fontSize:12}}>
              <i className="ti ti-check" style={{fontSize:32,display:'block',marginBottom:10,opacity:0.3}}/>
              Geen taken gevonden
            </div>
          ) : filtered.map((task, i) => {
            const statusColor = STATUS_COLORS[task.status] || '#6b7280'
            const domainColor = DOMAIN_COLORS[task.domain] || '#6b7280'
            const priorityColor = PRIORITY_COLORS[task.priority?.toUpperCase()] || '#6b7280'
            const isSelected = selected?.task_id === task.task_id
            return (
              <div key={i} onClick={() => setSelected(isSelected ? null : task)}
                style={{background:`linear-gradient(135deg,${domainColor}15 0%,${domainColor}05 100%)`,border:`1.5px solid ${isSelected?domainColor:domainColor+'30'}`,borderLeft:`3px solid ${statusColor}`,borderRadius:10,padding:'10px 14px',cursor:'pointer',transition:'all .15s'}}>
                <div style={{display:'flex',alignItems:'center',gap:8,marginBottom:4}}>
                  {/* Status dot */}
                  <div style={{width:7,height:7,borderRadius:'50%',background:statusColor,boxShadow:`0 0 6px ${statusColor}80`,flexShrink:0}}/>
                  {/* Title */}
                  <div style={{flex:1,fontSize:11,fontWeight:700,color:t.text,overflow:'hidden',textOverflow:'ellipsis',whiteSpace:'nowrap'}}>
                    {task.title || task.task_id}
                  </div>
                  {/* Priority badge */}
                  <span style={{fontSize:8,fontWeight:700,color:priorityColor,background:`${priorityColor}15`,border:`1px solid ${priorityColor}30`,borderRadius:3,padding:'1px 5px',flexShrink:0}}>
                    {task.priority?.toUpperCase()||'NORMAL'}
                  </span>
                </div>
                <div style={{display:'flex',alignItems:'center',gap:8,paddingLeft:15}}>
                  <span style={{fontSize:9,color:domainColor,fontWeight:700,textTransform:'uppercase'}}>{task.domain}</span>
                  <span style={{fontSize:9,color:t.textMuted}}>·</span>
                  <span style={{fontSize:9,color:acc,fontWeight:700}}>{task.agent_id}</span>
                  <span style={{fontSize:9,color:t.textMuted}}>·</span>
                  <span style={{fontSize:9,color:statusColor,fontWeight:700}}>{task.status}</span>
                  {task.assigned_by && task.assigned_by !== 'unknown' && (
                    <>
                      <span style={{fontSize:9,color:t.textMuted}}>·</span>
                      <span style={{fontSize:9,color:t.textMuted}}>van {task.assigned_by}</span>
                    </>
                  )}
                  {task.created_at && (
                    <>
                      <span style={{fontSize:9,color:t.textMuted}}>·</span>
                      <span style={{fontSize:9,color:t.textMuted}}>{task.created_at}</span>
                    </>
                  )}
                </div>
              </div>
            )
          })}
        </div>

        {/* Detail panel */}
        {selected && (
          <div style={{width:320,flexShrink:0,borderLeft:`1px solid ${t.border}`,overflow:'auto',padding:'14px 16px',display:'flex',flexDirection:'column',gap:10}}>
            <div style={{display:'flex',alignItems:'center',justifyContent:'space-between',marginBottom:4}}>
              <span style={{fontSize:12,fontWeight:700,color:t.text}}>Taak Detail</span>
              <button onClick={() => setSelected(null)} style={{background:'transparent',border:'none',color:t.textMuted,cursor:'pointer',fontSize:16}}>
                <i className="ti ti-x"/>
              </button>
            </div>

            {/* Status + Priority */}
            <div style={{display:'flex',gap:6}}>
              <span style={{fontSize:10,fontWeight:700,color:STATUS_COLORS[selected.status]||'#6b7280',background:`${STATUS_COLORS[selected.status]||'#6b7280'}15`,border:`1px solid ${STATUS_COLORS[selected.status]||'#6b7280'}30`,borderRadius:5,padding:'2px 8px'}}>
                {selected.status}
              </span>
              <span style={{fontSize:10,fontWeight:700,color:PRIORITY_COLORS[selected.priority?.toUpperCase()]||'#6b7280',background:`${PRIORITY_COLORS[selected.priority?.toUpperCase()]||'#6b7280'}15`,borderRadius:5,padding:'2px 8px'}}>
                {selected.priority?.toUpperCase()||'NORMAL'}
              </span>
            </div>

            {/* Title */}
            <div style={{fontSize:13,fontWeight:700,color:t.text,lineHeight:1.4}}>
              {selected.title || selected.task_id}
            </div>

            {/* Info grid */}
            {[
              ['Task ID', selected.task_id],
              ['Agent', selected.agent_id],
              ['Domein', selected.domain],
              ['Toegewezen door', selected.assigned_by],
              ['Aangemaakt', selected.created_at],
              ['Verwacht klaar', selected.expected_end_at],
            ].filter(([,v]) => v && v !== 'unknown' && v !== 'onbekend').map(([label, val]) => (
              <div key={label} style={{display:'flex',flexDirection:'column',gap:2}}>
                <span style={{fontSize:9,fontWeight:700,color:t.textMuted,textTransform:'uppercase',letterSpacing:'0.07em'}}>{label}</span>
                <span style={{fontSize:11,color:t.text}}>{val}</span>
              </div>
            ))}

            {/* Summary */}
            {selected.summary && (
              <div>
                <div style={{fontSize:9,fontWeight:700,color:t.textMuted,textTransform:'uppercase',letterSpacing:'0.07em',marginBottom:4}}>Samenvatting</div>
                <div style={{fontSize:11,color:t.textMuted,lineHeight:1.6,background:'rgba(0,0,0,0.2)',borderRadius:6,padding:'8px 10px'}}>{selected.summary}</div>
              </div>
            )}

            {/* Next step */}
            {selected.next_step && (
              <div>
                <div style={{fontSize:9,fontWeight:700,color:t.textMuted,textTransform:'uppercase',letterSpacing:'0.07em',marginBottom:4}}>Volgende stap</div>
                <div style={{fontSize:11,color:acc,lineHeight:1.6,background:`${acc}10`,borderRadius:6,padding:'8px 10px',border:`1px solid ${acc}20`}}>{selected.next_step}</div>
              </div>
            )}

            {/* Result */}
            {selected.result_summary && selected.result_summary.length > 2 && (
              <div>
                <div style={{fontSize:9,fontWeight:700,color:t.textMuted,textTransform:'uppercase',letterSpacing:'0.07em',marginBottom:4}}>Resultaat</div>
                <div style={{fontSize:11,color:'#22c55e',lineHeight:1.6,background:'#22c55e10',borderRadius:6,padding:'8px 10px',border:'1px solid #22c55e20'}}>{selected.result_summary}</div>
              </div>
            )}

            {/* Blocked reason */}
            {selected.blocked_reason && selected.blocked_reason !== 'geen' && (
              <div>
                <div style={{fontSize:9,fontWeight:700,color:'#ef4444',textTransform:'uppercase',letterSpacing:'0.07em',marginBottom:4}}>Blokkade</div>
                <div style={{fontSize:11,color:'#ef4444',lineHeight:1.6,background:'#ef444410',borderRadius:6,padding:'8px 10px',border:'1px solid #ef444430'}}>{selected.blocked_reason}</div>
              </div>
            )}

            {/* File locatie */}
            <div style={{marginTop:'auto',padding:'8px 10px',background:'rgba(0,0,0,0.2)',borderRadius:6,fontSize:9,color:t.textMuted,fontFamily:'monospace'}}>
              📁 /agents/{selected.agent_id}/TASKS.md
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
