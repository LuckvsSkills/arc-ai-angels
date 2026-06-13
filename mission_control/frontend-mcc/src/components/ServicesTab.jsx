import React, { useState, useEffect } from 'react'

export default function ServicesTab({ theme }) {
  const t = theme?.colors || {}
  const acc = t.accent || '#c9a84c'
  const [services, setServices] = useState([])
  const [loading, setLoading] = useState(true)
  const [actionMsg, setActionMsg] = useState('')
  const [acting, setActing] = useState('')

  const load = () => {
    fetch('/api/system/services')
      .then(r => r.json())
      .then(d => { setServices(d.services || []); setLoading(false) })
      .catch(() => setLoading(false))
  }

  useEffect(() => { load(); const iv = setInterval(load, 15000); return () => clearInterval(iv) }, [])

  const doAction = async (serviceId, action) => {
    setActing(`${serviceId}-${action}`)
    setActionMsg(`${action} ${serviceId}...`)
    try {
      const r = await fetch(`/api/system/service/${serviceId}/${action}`, { method: 'POST' })
      const d = await r.json()
      setActionMsg(d.message || `${action} OK`)
      setTimeout(() => { load(); setActionMsg('') }, 3000)
    } catch {
      setActionMsg('Actie mislukt')
      setTimeout(() => setActionMsg(''), 3000)
    }
    setActing('')
  }

  const doStartAll = async () => {
    setActionMsg('Alle services starten...')
    await fetch('/api/system/start-all', { method: 'POST' })
    setTimeout(() => { load(); setActionMsg('') }, 4000)
  }

  const sc = (s) => s === 'active' || s === 'running' ? '#22c55e' : s === 'inactive' || s === 'failed' ? '#ef4444' : '#f59e0b'
  const pc = (s) => s === 'reachable' ? '#22c55e' : s === 'unreachable' ? '#ef4444' : '#6b7280'

  return (
    <div style={{ height:'100%', overflow:'auto', padding:'16px', display:'flex', flexDirection:'column', gap:14 }}>

      {/* Header */}
      <div style={{ display:'flex', alignItems:'center', justifyContent:'space-between' }}>
        <div>
          <div style={{ fontSize:14, fontWeight:700, color:t.text }}>System Services</div>
          <div style={{ fontSize:11, color:t.textMuted, marginTop:2 }}>
            {services.filter(s=>s.status==='active').length}/{services.length} actief
          </div>
        </div>
        <div style={{ display:'flex', gap:8, alignItems:'center' }}>
          {actionMsg && <span style={{ fontSize:11, color:acc }}>{actionMsg}</span>}
          <button onClick={doStartAll} style={{ padding:'7px 14px', borderRadius:8, border:`1.5px solid #22c55e40`, background:'#22c55e12', color:'#22c55e', cursor:'pointer', fontSize:11, fontWeight:700, display:'flex', alignItems:'center', gap:5 }}>
            <i className="ti ti-player-play" style={{ fontSize:13 }}/> Start Alles
          </button>
          <button onClick={load} style={{ padding:'7px 10px', borderRadius:8, border:`1px solid ${t.border}`, background:'transparent', color:t.textMuted, cursor:'pointer', fontSize:11 }}>
            <i className="ti ti-refresh" style={{ fontSize:13 }}/>
          </button>
        </div>
      </div>

      {/* Service kaarten */}
      {loading ? (
        <div style={{ color:t.textMuted, fontSize:12, padding:20 }}>Laden...</div>
      ) : (
        <div style={{ display:'grid', gridTemplateColumns:'repeat(auto-fill, minmax(280px,1fr))', gap:12 }}>
          {services.map(svc => {
            const statusColor = sc(svc.status)
            const portColor = pc(svc.port_status)
            const isActing = acting.startsWith(svc.id)
            return (
              <div key={svc.id} style={{ background:`linear-gradient(135deg, ${svc.color}15 0%, ${svc.color}05 100%)`, border:`1.5px solid ${svc.color}30`, borderRadius:12, padding:'14px 16px', position:'relative', overflow:'hidden' }}>
                {/* Top accent lijn */}
                <div style={{ position:'absolute', top:0, left:0, right:0, height:2, background:`linear-gradient(90deg, ${svc.color}00, ${svc.color}80, ${svc.color}00)` }}/>

                {/* Header */}
                <div style={{ display:'flex', alignItems:'center', gap:10, marginBottom:12 }}>
                  <div style={{ width:36, height:36, borderRadius:9, background:`${svc.color}20`, border:`1px solid ${svc.color}40`, display:'flex', alignItems:'center', justifyContent:'center', flexShrink:0 }}>
                    <i className={`ti ${svc.icon}`} style={{ fontSize:18, color:svc.color }}/>
                  </div>
                  <div style={{ flex:1 }}>
                    <div style={{ fontSize:13, fontWeight:700, color:t.text }}>{svc.label}</div>
                    {svc.port && <div style={{ fontSize:10, color:t.textMuted, fontFamily:'monospace' }}>poort {svc.port}</div>}
                  </div>
                  <div style={{ display:'flex', flexDirection:'column', alignItems:'flex-end', gap:4 }}>
                    <div style={{ display:'flex', alignItems:'center', gap:5 }}>
                      <div style={{ width:7, height:7, borderRadius:'50%', background:statusColor, boxShadow:`0 0 6px ${statusColor}80` }}/>
                      <span style={{ fontSize:10, fontWeight:700, color:statusColor }}>{svc.status}</span>
                    </div>
                    {svc.port_status && (
                      <div style={{ display:'flex', alignItems:'center', gap:4 }}>
                        <div style={{ width:5, height:5, borderRadius:'50%', background:portColor }}/>
                        <span style={{ fontSize:9, color:portColor }}>{svc.port_status}</span>
                      </div>
                    )}
                  </div>
                </div>

                {/* Controls */}
                <div style={{ display:'grid', gridTemplateColumns:'repeat(3,1fr)', gap:6 }}>
                  {[
                    { action:'start',   label:'Start',    icon:'ti-player-play',  color:'#22c55e' },
                    { action:'stop',    label:'Stop',     icon:'ti-player-stop',  color:'#ef4444' },
                    { action:'restart', label:'Herstart', icon:'ti-refresh',      color:'#f87115' },
                  ].map(btn => (
                    <button key={btn.action}
                      onClick={() => doAction(svc.id, btn.action)}
                      disabled={isActing}
                      style={{ padding:'7px 4px', borderRadius:7, border:`1px solid ${btn.color}30`, background:`${btn.color}10`, color:btn.color, cursor:isActing?'not-allowed':'pointer', fontSize:10, fontWeight:700, display:'flex', alignItems:'center', justifyContent:'center', gap:4, opacity:isActing?0.5:1, transition:'all .15s' }}>
                      <i className={`ti ${btn.icon}`} style={{ fontSize:11 }}/>{btn.label}
                    </button>
                  ))}
                </div>
              </div>
            )
          })}
        </div>
      )}

      {/* Info sectie */}
      <div style={{ background:t.bgSecondary, border:`1px solid ${t.border}`, borderRadius:10, padding:'12px 14px' }}>
        <div style={{ fontSize:10, fontWeight:700, color:t.textMuted, textTransform:'uppercase', letterSpacing:'0.1em', marginBottom:8 }}>Na reboot opstarten</div>
        <div style={{ fontSize:11, color:t.textMuted, lineHeight:1.7 }}>
          LiteLLM, MCC Backend en Vite starten automatisch op. OpenClaw Gateway start soms niet — gebruik dan de <strong style={{ color:acc }}>Start</strong> knop hierboven of klik <strong style={{ color:acc }}>Start Alles</strong>.
        </div>
      </div>
    </div>
  )
}
