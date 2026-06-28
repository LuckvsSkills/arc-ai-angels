import React, { useState, useEffect } from 'react'

const FASE_NAMEN = ['Intake', 'Setup', 'Uitvoering', 'QA', 'Deploy', 'Nazorg']
const TASK_KLEUR = { done:'#10b981', in_progress:'#f59e0b', open:'#6b7280', wacht_op:'#6b7280', parallel_met:'#3b82f6', geblokkeerd:'#ef4444' }
const TASK_LABEL = { done:'Klaar', in_progress:'Bezig', open:'Open', wacht_op:'Wacht', parallel_met:'Parallel', geblokkeerd:'Geblokkeerd' }
const API = '/api'

export default function ProjectsView({ theme }) {
  const t = theme?.colors || {}
  const [projects, setProjects] = useState([])
  const [selectedId, setSelectedId] = useState(null)
  const [filter, setFilter] = useState('alle')
  const [loading, setLoading] = useState(true)
  const [modal, setModal] = useState(null) // 'unlock' | 'lock' | null
  const [pin, setPin] = useState('')
  const [pinErr, setPinErr] = useState('')
  const [winW, setWinW] = useState(window.innerWidth)
  const [showDetail, setShowDetail] = useState(false)
  const isMobile = winW < 768

  useEffect(() => {
    const h = () => setWinW(window.innerWidth)
    window.addEventListener('resize', h)
    return () => window.removeEventListener('resize', h)
  }, [])

  const load = () => {
    fetch(`${API}/projects?filter=${filter}`)
      .then(r => r.json())
      .then(data => {
        const arr = Array.isArray(data) ? data : []
        setProjects(arr)
        setLoading(false)
        if (!selectedId && arr.length > 0) setSelectedId(arr[0].project_id)
      })
      .catch(() => setLoading(false))
  }

  useEffect(() => { load(); const t = setInterval(load, 15000); return () => clearInterval(t) }, [filter])

  const project = projects.find(p => p.project_id === selectedId)
  const isLocked = project?.locked === true

  const openModal = (type) => { setModal(type); setPin(''); setPinErr('') }
  const closeModal = () => { setModal(null); setPin(''); setPinErr('') }

  const handleUnlock = () => {
    // Unlock: valideer PIN dan zet locked:false in bestand
    fetch(`${API}/projects/${selectedId}/unlock`, {
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify({pin})
    })
    .then(r => { if (!r.ok) throw new Error(); return r.json() })
    .then(() => {
      // PIN correct — zet nu locked:false permanent in bestand
      return fetch(`${API}/projects/${selectedId}`, {
        method: 'PATCH',
        headers: {'Content-Type':'application/json'},
        body: JSON.stringify({locked: false})
      })
    })
    .then(() => { closeModal(); load() })
    .catch(() => setPinErr('Onjuiste PIN'))
  }

  const handleLock = () => {
    // Lock: valideer PIN dan zet locked:true in bestand
    fetch(`${API}/projects/${selectedId}/unlock`, {
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify({pin})
    })
    .then(r => { if (!r.ok) throw new Error(); return r.json() })
    .then(() => {
      return fetch(`${API}/projects/${selectedId}`, {
        method: 'PATCH',
        headers: {'Content-Type':'application/json'},
        body: JSON.stringify({locked: true})
      })
    })
    .then(() => { closeModal(); load() })
    .catch(() => setPinErr('Onjuiste PIN'))
  }

  const slaKleur = (p) => {
    if (!p.sla_deadline) return null
    const h = (new Date(p.sla_deadline) - new Date()) / 3600000
    if (['live','opgeleverd','afgesloten'].includes(p.status)) return '#10b981'
    return h < 0 ? '#ef4444' : h < 4 ? '#f59e0b' : '#10b981'
  }

  return (
    <div style={{display:'flex',height:'100%',overflow:'hidden'}}>

      {/* PIN Modal */}
      {modal && (
        <div style={{position:'fixed',inset:0,background:'rgba(0,0,0,0.75)',zIndex:200,display:'flex',alignItems:'center',justifyContent:'center'}}
          onClick={e => e.target===e.currentTarget && closeModal()}>
          <div style={{background:t.bg||'#0d0d0d',border:`1px solid ${t.border||'#333'}`,borderRadius:'16px',padding:'32px',width:'300px',textAlign:'center'}}>
            <div style={{fontSize:'40px',marginBottom:'12px'}}>{modal==='unlock'?'🔓':'🔒'}</div>
            <h3 style={{color:t.text||'#e2e8f0',marginBottom:'6px',fontSize:'16px'}}>
              {modal==='unlock' ? 'Ontgrendelen' : 'Vergrendelen'}
            </h3>
            <p style={{color:t.textMuted||'#666',fontSize:'12px',marginBottom:'20px'}}>
              Voer PIN in om te bevestigen
            </p>
            <input
              autoFocus
              type="password"
              value={pin}
              onChange={e => { setPin(e.target.value); setPinErr('') }}
              onKeyDown={e => e.key==='Enter' && (modal==='unlock' ? handleUnlock() : handleLock())}
              placeholder="● ● ● ●"
              style={{width:'100%',padding:'14px',borderRadius:'10px',
                border:`2px solid ${pinErr?'#ef4444':(t.border||'#444')}`,
                background:t.bg2||'#1a1a1a',color:t.text||'#fff',
                textAlign:'center',fontSize:'20px',letterSpacing:'8px',
                boxSizing:'border-box',outline:'none',marginBottom:'10px'}}
            />
            {pinErr && <p style={{color:'#ef4444',fontSize:'12px',marginBottom:'10px'}}>{pinErr}</p>}
            <div style={{display:'flex',gap:'8px',marginTop:'4px'}}>
              <button onClick={closeModal}
                style={{flex:1,padding:'10px',borderRadius:'8px',border:`1px solid ${t.border||'#333'}`,
                  background:'transparent',color:t.textMuted||'#666',cursor:'pointer',fontSize:'13px'}}>
                Annuleer
              </button>
              <button onClick={modal==='unlock' ? handleUnlock : handleLock}
                style={{flex:1,padding:'10px',borderRadius:'8px',border:'none',
                  background:modal==='unlock'?(t.accent||'#c9a84c'):'#ef4444',
                  color:modal==='unlock'?'#000':'#fff',cursor:'pointer',fontSize:'13px',fontWeight:'700'}}>
                {modal==='unlock' ? 'Ontgrendel' : 'Vergrendel'}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Sidebar */}
      {(!isMobile || !showDetail) && (
      <div style={{width:isMobile?'100%':'270px',minWidth:isMobile?'unset':'270px',borderRight:isMobile?'none':`1px solid ${t.border||'#333'}`,overflow:'auto',padding:'16px 0'}}>
        <div style={{padding:'0 12px 12px',display:'flex',gap:'6px'}}>
          {['alle','klant','intern'].map(f => (
            <button key={f} onClick={() => setFilter(f)} style={{
              flex:1,padding:'5px',fontSize:'11px',borderRadius:'6px',cursor:'pointer',
              border:`1px solid ${filter===f?(t.accent||'#c9a84c'):(t.border||'#333')}`,
              background:filter===f?`${t.accent||'#c9a84c'}20`:'transparent',
              color:filter===f?(t.accent||'#c9a84c'):(t.textMuted||'#666'),
              fontWeight:filter===f?'600':'400',textTransform:'capitalize'
            }}>{f}</button>
          ))}
        </div>

        <div style={{padding:'0 14px 10px',fontSize:'11px',color:t.textMuted||'#555',textTransform:'uppercase',letterSpacing:'0.08em'}}>
          {loading ? 'Laden...' : `${projects.length} project${projects.length!==1?'en':''}`}
        </div>

        {projects.map(p => {
          const lck = p.locked === true
          const sla = slaKleur(p)
          const isSelected = selectedId === p.project_id
          return (
            <div key={p.project_id}
              onClick={() => setSelectedId(p.project_id)}
              style={{padding:'10px 14px',cursor:'pointer',
                borderLeft:isSelected?`3px solid ${t.accent||'#c9a84c'}`:'3px solid transparent',
                background:isSelected?`${t.accent||'#c9a84c'}12`:'transparent',
                borderBottom:`1px solid ${t.border||'#222'}`}}>
              <div style={{display:'flex',alignItems:'center',gap:'6px',marginBottom:'4px'}}>
                {lck
                  ? <span style={{fontSize:'10px',padding:'2px 7px',borderRadius:'4px',background:'#ef444425',color:'#ef4444',fontWeight:'700',border:'1px solid #ef444440'}}>🔒 LOCKED</span>
                  : <span style={{fontSize:'10px',padding:'2px 7px',borderRadius:'4px',background:`${t.border||'#333'}40`,color:t.textMuted||'#666',fontWeight:'600',textTransform:'uppercase'}}>{p.type}</span>
                }
                {sla && !lck && <span style={{width:'6px',height:'6px',borderRadius:'50%',background:sla,marginLeft:'auto'}}/>}
              </div>
              <div style={{fontSize:'13px',fontWeight:'600',marginBottom:'2px',
                color:lck?(t.textMuted||'#555'):(t.text||'#e2e8f0'),
                filter:lck?'blur(4px)':'none',
                userSelect:lck?'none':'auto',
                pointerEvents:lck?'none':'auto'}}>
                {p.naam}
              </div>
              <div style={{fontSize:'11px',color:t.textMuted||'#555'}}>
                {lck ? '🔒 Vergrendeld — klik om te openen' : (FASE_NAMEN[p.fase]||'')}
              </div>
            </div>
          )
        })}

        {!loading && projects.length === 0 && (
          <div style={{padding:'20px 14px',fontSize:'12px',color:t.textMuted||'#555',textAlign:'center'}}>
            Geen projecten gevonden
          </div>
        )}
      </div>

      )}
      {/* Detail panel */}
      {project && (!isMobile || showDetail) ? (
        <div style={{flex:1,overflow:'auto',padding:'28px 32px'}}>

          {isMobile && (
            <button onClick={() => { setShowDetail(false); setSelectedId(null) }}
              style={{display:'flex',alignItems:'center',gap:'6px',fontSize:'12px',color:t.textMuted||'#666',
                background:'transparent',border:'none',cursor:'pointer',padding:'0 0 12px 0'}}>
              ← Terug naar projecten
            </button>
          )}
          {isLocked ? (
            /* LOCKED STATE */
            <div style={{maxWidth:'340px',margin:'60px auto',textAlign:'center'}}>
              <div style={{width:'80px',height:'80px',borderRadius:'50%',background:'#ef444415',border:'2px solid #ef444440',
                display:'flex',alignItems:'center',justifyContent:'center',fontSize:'36px',margin:'0 auto 20px'}}>
                🔒
              </div>
              <h2 style={{color:t.text||'#e2e8f0',marginBottom:'8px',fontSize:'20px'}}>Project vergrendeld</h2>
              <p style={{color:t.textMuted||'#666',fontSize:'13px',lineHeight:'1.5',marginBottom:'28px'}}>
                {project.lock_hint || 'Dit project is beveiligd met een PIN. Voer de PIN in om de inhoud te bekijken.'}
              </p>
              <button onClick={() => openModal('unlock')}
                style={{padding:'14px 32px',borderRadius:'10px',border:'none',
                  background:t.accent||'#c9a84c',color:'#000',fontWeight:'700',cursor:'pointer',fontSize:'14px',
                  width:'100%'}}>
                🔓 Ontgrendelen met PIN
              </button>
            </div>
          ) : (
            /* UNLOCKED STATE */
            <>
              {/* Header */}
              <div style={{display:'flex',alignItems:'flex-start',justifyContent:'space-between',marginBottom:'24px',gap:'16px'}}>
                <div style={{flex:1}}>
                  <div style={{display:'flex',alignItems:'center',gap:'8px',marginBottom:'8px',flexWrap:'wrap'}}>
                    <span style={{fontSize:'11px',padding:'3px 8px',borderRadius:'5px',background:'#f59e0b20',color:'#f59e0b',fontWeight:'600',textTransform:'uppercase'}}>
                      {project.status}
                    </span>
                    <span style={{fontSize:'11px',color:t.textMuted||'#666',padding:'3px 8px',border:`1px solid ${t.border||'#333'}`,borderRadius:'5px'}}>
                      {project.template_type||project.type}
                    </span>
                    <span style={{fontSize:'11px',color:t.textMuted||'#666'}}>
                      Lead: <strong style={{color:t.accent||'#c9a84c'}}>{project.lead_agent}</strong>
                    </span>
                  </div>
                  <h1 style={{fontSize:'20px',fontWeight:'800',color:t.text||'#e2e8f0',margin:'0 0 4px'}}>{project.naam}</h1>
                  {project.live_url && (
                    <a href={project.live_url} target="_blank" rel="noopener noreferrer"
                      style={{color:t.accent||'#c9a84c',fontSize:'12px'}}>{project.live_url} ↗</a>
                  )}
                </div>
                <button onClick={() => openModal('lock')}
                  style={{flexShrink:0,padding:'7px 14px',borderRadius:'8px',fontSize:'12px',fontWeight:'600',
                    border:'1px solid #ef444450',background:'#ef444412',color:'#ef4444',cursor:'pointer'}}>
                  🔒 Lock
                </button>
              </div>

              {/* Fase balk */}
              <div style={{marginBottom:'24px'}}>
                <div style={{fontSize:'11px',fontWeight:'600',color:t.textMuted||'#666',textTransform:'uppercase',letterSpacing:'0.08em',marginBottom:'10px'}}>Fase voortgang</div>
                <div style={{display:'flex',gap:'3px'}}>
                  {FASE_NAMEN.map((n,i) => (
                    <div key={i} style={{flex:1,textAlign:'center'}}>
                      <div style={{height:'5px',borderRadius:'999px',marginBottom:'4px',
                        background:i<=project.fase?(t.accent||'#c9a84c'):`${t.border||'#333'}`}}/>
                      <span style={{fontSize:'9px',color:i<=project.fase?(t.text||'#e2e8f0'):(t.textMuted||'#555')}}>{n}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Template voortgang */}
              {project.voortgang_templates && (
                <div style={{marginBottom:'24px',padding:'16px',background:t.bg2||'#111',borderRadius:'10px',border:`1px solid ${t.border||'#333'}`}}>
                  <div style={{display:'flex',justifyContent:'space-between',alignItems:'center',marginBottom:'10px'}}>
                    <div>
                      <div style={{fontSize:'12px',fontWeight:'600',color:t.text||'#e2e8f0'}}>Template Library Voortgang</div>
                      <div style={{fontSize:'11px',color:t.textMuted||'#666'}}>Maand {project.voortgang_templates.huidige_maand} — Variant {project.voortgang_templates.huidige_variant}</div>
                    </div>
                    <div style={{fontSize:'22px',fontWeight:'800',color:t.accent||'#c9a84c'}}>
                      {project.voortgang_templates.klaar}<span style={{fontSize:'14px',color:t.textMuted||'#666'}}>/{project.voortgang_templates.totaal}</span>
                    </div>
                  </div>
                  <div style={{height:'8px',background:`${t.border||'#333'}`,borderRadius:'999px',overflow:'hidden'}}>
                    <div style={{width:`${(project.voortgang_templates.klaar/project.voortgang_templates.totaal)*100}%`,
                      height:'100%',background:t.accent||'#c9a84c',borderRadius:'999px',transition:'width 0.5s'}}/>
                  </div>
                  <div style={{display:'flex',flexWrap:'wrap',gap:'4px',marginTop:'10px'}}>
                    {project.voortgang_templates.klaar_lijst?.map(t2 => (
                      <span key={t2} style={{fontSize:'10px',padding:'2px 7px',borderRadius:'4px',
                        background:`${t.accent||'#c9a84c'}20`,color:t.accent||'#c9a84c',border:`1px solid ${t.accent||'#c9a84c'}30`}}>
                        ✓ {t2}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {/* Agent taken */}
              {project.tasks && Object.keys(project.tasks).length > 0 && (
                <div style={{marginBottom:'24px'}}>
                  <div style={{fontSize:'11px',fontWeight:'600',color:t.textMuted||'#666',textTransform:'uppercase',letterSpacing:'0.08em',marginBottom:'10px'}}>Agent Taken</div>
                  <div style={{display:'flex',flexDirection:'column',gap:'6px'}}>
                    {Object.entries(project.tasks).map(([agent, td]) => (
                      <div key={agent} style={{display:'flex',alignItems:'center',gap:'10px',padding:'10px 14px',
                        background:t.bg2||'#111',borderRadius:'8px',border:`1px solid ${t.border||'#333'}`}}>
                        <div style={{width:'8px',height:'8px',borderRadius:'50%',background:TASK_KLEUR[td.status]||'#666',flexShrink:0}}/>
                        <span style={{fontSize:'13px',color:t.text||'#e2e8f0',flex:1,textTransform:'capitalize',fontWeight:'500'}}>{agent}</span>
                        {td.notitie && <span style={{fontSize:'11px',color:t.textMuted||'#555',maxWidth:'220px',overflow:'hidden',textOverflow:'ellipsis',whiteSpace:'nowrap'}}>{td.notitie}</span>}
                        <span style={{fontSize:'11px',color:TASK_KLEUR[td.status]||'#666',fontWeight:'700',flexShrink:0}}>{TASK_LABEL[td.status]||td.status}</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Notities */}
              {project.notities?.length > 0 && (
                <div style={{marginBottom:'24px'}}>
                  <div style={{fontSize:'11px',fontWeight:'600',color:t.textMuted||'#666',textTransform:'uppercase',letterSpacing:'0.08em',marginBottom:'10px'}}>Notities</div>
                  {project.notities.map((n,i) => (
                    <div key={i} style={{padding:'10px 14px',background:t.bg2||'#111',borderRadius:'8px',
                      border:`1px solid ${t.border||'#333'}`,fontSize:'12px',color:t.textSecondary||'#aaa',marginBottom:'6px'}}>
                      <strong style={{color:t.accent||'#c9a84c'}}>{n.agent}</strong>: {n.tekst}
                    </div>
                  ))}
                </div>
              )}

              {/* SLA */}
              {project.sla_deadline && (
                <div style={{padding:'12px 14px',background:t.bg2||'#111',borderRadius:'8px',border:`1px solid ${t.border||'#333'}`,fontSize:'12px',color:t.textMuted||'#666'}}>
                  SLA deadline: <strong style={{color:t.text||'#e2e8f0'}}>{new Date(project.sla_deadline).toLocaleString('nl-NL')}</strong>
                </div>
              )}
            </>
          )}
        </div>
      ) : (
        <div style={{flex:1,display:'flex',alignItems:'center',justifyContent:'center',color:t.textMuted||'#555',fontSize:'13px'}}>
          {loading ? 'Projecten laden...' : 'Selecteer een project'}
        </div>
      )}
    </div>
  )
}
