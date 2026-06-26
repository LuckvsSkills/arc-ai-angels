import React, { useState, useEffect } from 'react'

const FASE_NAMEN = ['Intake', 'Setup', 'Uitvoering', 'QA', 'Deploy', 'Nazorg']
const TASK_KLEUR = {
  done: '#10b981', in_progress: '#f59e0b', open: '#6b7280',
  wacht_op: '#6b7280', parallel_met: '#3b82f6', geblokkeerd: '#ef4444', overgeslagen: '#6b7280',
}
const TASK_LABEL = {
  done: 'Klaar', in_progress: 'Bezig', open: 'Open',
  wacht_op: 'Wacht', parallel_met: 'Parallel', geblokkeerd: 'Geblokkeerd', overgeslagen: 'N.v.t.',
}
const API_BASE = '/api'

export default function ProjectsView({ theme }) {
  const t = theme?.colors || {}
  const [projects, setProjects] = useState([])
  const [selectedId, setSelectedId] = useState(null)
  const [filter, setFilter] = useState('alle')
  const [loading, setLoading] = useState(true)
  const [pinInput, setPinInput] = useState('')
  const [pinError, setPinError] = useState('')
  const [showLockModal, setShowLockModal] = useState(false)
  const [lockPin, setLockPin] = useState('')
  const [lockError, setLockError] = useState('')

  const loadProjects = () => {
    fetch(`${API_BASE}/projects?filter=${filter}`)
      .then(r => r.json())
      .then(data => {
        setProjects(Array.isArray(data) ? data : [])
        setLoading(false)
        if (!selectedId && Array.isArray(data) && data.length > 0) {
          setSelectedId(data[0].project_id)
        }
      })
      .catch(() => setLoading(false))
  }

  useEffect(() => {
    loadProjects()
    const interval = setInterval(loadProjects, 15000)
    return () => clearInterval(interval)
  }, [filter])

  const project = projects.find(p => p.project_id === selectedId)
  // Project is locked als locked=true EN status='locked' (server stuurt dit terug)
  const isLocked = project?.locked === true

  const handleUnlock = () => {
    fetch(`${API_BASE}/projects/${selectedId}/unlock`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ pin: pinInput })
    })
      .then(r => { if (!r.ok) throw new Error('fout'); return r.json() })
      .then(() => { setPinError(''); setPinInput(''); loadProjects() })
      .catch(() => setPinError('Onjuiste PIN, probeer opnieuw'))
  }

  const handleLock = () => {
    // Vergrendelen vereist ook PIN-bevestiging
    fetch(`${API_BASE}/projects/${selectedId}/unlock`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ pin: lockPin })
    })
      .then(r => { if (!r.ok) throw new Error('fout'); return r.json() })
      .then(() => {
        // PIN correct, nu locken via PATCH
        return fetch(`${API_BASE}/projects/${selectedId}`, {
          method: 'PATCH',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ locked: true })
        })
      })
      .then(() => { setShowLockModal(false); setLockPin(''); setLockError(''); loadProjects() })
      .catch(() => setLockError('Onjuiste PIN'))
  }

  const handleUnlockToggle = () => {
    fetch(`${API_BASE}/projects/${selectedId}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ locked: false })
    }).then(loadProjects)
  }

  const slaKleur = (p) => {
    if (!p.sla_deadline) return null
    const diffH = (new Date(p.sla_deadline) - new Date()) / 3600000
    if (['live','opgeleverd','afgesloten'].includes(p.status)) return '#10b981'
    if (diffH < 0) return '#ef4444'
    if (diffH < 4) return '#f59e0b'
    return '#10b981'
  }

  return (
    <div style={{display:'flex',height:'100%',overflow:'hidden'}}>

      {/* Sidebar */}
      <div style={{width:'280px',minWidth:'280px',borderRight:`1px solid ${t.border||'#333'}`,overflow:'auto',padding:'16px 0',display:'flex',flexDirection:'column'}}>
        <div style={{padding:'0 16px 12px',display:'flex',gap:'6px'}}>
          {['alle','klant','intern'].map(f => (
            <button key={f} onClick={() => setFilter(f)} style={{
              flex:1,padding:'6px 8px',fontSize:'11px',borderRadius:'6px',cursor:'pointer',
              border:`1px solid ${filter===f?(t.accent||'#c9a84c'):(t.border||'#333')}`,
              background:filter===f?`${t.accent||'#c9a84c'}20`:'transparent',
              color:filter===f?(t.accent||'#c9a84c'):(t.textMuted||'#666'),
              fontWeight:filter===f?'600':'400',textTransform:'capitalize'
            }}>{f}</button>
          ))}
        </div>
        <div style={{padding:'0 16px 12px',fontSize:'11px',color:t.textMuted||'#666',textTransform:'uppercase',letterSpacing:'0.08em'}}>
          Projecten {loading?'(laden...)':`(${projects.length})`}
        </div>
        {projects.map(p => {
          const locked = p.locked === true
          const sla = slaKleur(p)
          return (
            <div key={p.project_id}
              onClick={() => { setSelectedId(p.project_id); setPinError(''); setPinInput('') }}
              style={{padding:'12px 16px',cursor:'pointer',
                borderLeft:selectedId===p.project_id?`3px solid ${t.accent||'#c9a84c'}`:'3px solid transparent',
                background:selectedId===p.project_id?`${t.accent||'#c9a84c'}10`:'transparent'}}>
              <div style={{display:'flex',alignItems:'center',gap:'8px',marginBottom:'4px'}}>
                <span style={{fontSize:'10px',padding:'2px 6px',borderRadius:'4px',
                  background:locked?'#ef444420':'#33333340',
                  color:locked?'#ef4444':(t.textMuted||'#888'),fontWeight:'600',textTransform:'uppercase'}}>
                  {locked ? '🔒 vergrendeld' : (p.type||'onbekend')}
                </span>
                {sla && !locked && <span style={{width:'6px',height:'6px',borderRadius:'50%',background:sla,flexShrink:0}}/>}
              </div>
              <div style={{fontSize:'13px',color:locked?(t.textMuted||'#666'):(t.text||'#e2e8f0'),fontWeight:'500',
                filter:locked?'blur(3px)':'none',userSelect:locked?'none':'auto'}}>
                {locked ? '██████████' : p.naam}
              </div>
              <div style={{fontSize:'11px',color:t.textMuted||'#666',marginTop:'2px'}}>
                {locked ? 'Klik om te ontgrendelen' : (FASE_NAMEN[p.fase]||p.fase_naam||'')}
              </div>
            </div>
          )
        })}
        {projects.length === 0 && !loading && (
          <div style={{padding:'16px',fontSize:'12px',color:t.textMuted||'#666'}}>Geen projecten gevonden.</div>
        )}
      </div>

      {/* Detail */}
      {project && (
        <div style={{flex:1,overflow:'auto',padding:'32px',position:'relative'}}>

          {/* Lock modal */}
          {showLockModal && (
            <div style={{position:'fixed',top:0,left:0,right:0,bottom:0,background:'rgba(0,0,0,0.7)',zIndex:100,display:'flex',alignItems:'center',justifyContent:'center'}}>
              <div style={{background:t.bg2||'#1a1a1a',border:`1px solid ${t.border||'#333'}`,borderRadius:'16px',padding:'32px',width:'320px',textAlign:'center'}}>
                <div style={{fontSize:'32px',marginBottom:'12px'}}>🔒</div>
                <h3 style={{color:t.text||'#e2e8f0',marginBottom:'8px'}}>Project vergrendelen</h3>
                <p style={{color:t.textMuted||'#666',fontSize:'13px',marginBottom:'20px'}}>Voer PIN in om te bevestigen</p>
                <input type="password" value={lockPin} onChange={e => setLockPin(e.target.value)}
                  placeholder="PIN" onKeyDown={e => e.key==='Enter'&&handleLock()}
                  style={{width:'100%',padding:'10px',borderRadius:'8px',border:`1px solid ${t.border||'#333'}`,
                    background:t.bg2||'#111',color:t.text||'#fff',marginBottom:'8px',textAlign:'center',boxSizing:'border-box'}}/>
                {lockError && <div style={{color:'#ef4444',fontSize:'12px',marginBottom:'8px'}}>{lockError}</div>}
                <div style={{display:'flex',gap:'8px'}}>
                  <button onClick={() => { setShowLockModal(false); setLockPin(''); setLockError('') }}
                    style={{flex:1,padding:'10px',borderRadius:'8px',border:`1px solid ${t.border||'#333'}`,
                      background:'transparent',color:t.textMuted||'#666',cursor:'pointer'}}>Annuleer</button>
                  <button onClick={handleLock}
                    style={{flex:1,padding:'10px',borderRadius:'8px',border:'none',
                      background:'#ef4444',color:'#fff',fontWeight:'600',cursor:'pointer'}}>Vergrendel</button>
                </div>
              </div>
            </div>
          )}

          {isLocked ? (
            <div style={{maxWidth:'320px',margin:'80px auto',textAlign:'center'}}>
              <div style={{fontSize:'48px',marginBottom:'16px'}}>🔒</div>
              <h2 style={{color:t.text||'#e2e8f0',marginBottom:'8px'}}>Vergrendeld project</h2>
              <p style={{color:t.textMuted||'#666',fontSize:'13px',marginBottom:'24px'}}>
                {project.lock_hint || 'Voer PIN in om dit project te bekijken'}
              </p>
              <input type="password" value={pinInput} onChange={e => setPinInput(e.target.value)}
                placeholder="Voer PIN in" onKeyDown={e => e.key==='Enter'&&handleUnlock()}
                style={{width:'100%',padding:'12px',borderRadius:'8px',border:`1px solid ${pinError?'#ef4444':(t.border||'#333')}`,
                  background:t.bg2||'#111',color:t.text||'#fff',marginBottom:'8px',
                  textAlign:'center',fontSize:'18px',letterSpacing:'4px',boxSizing:'border-box'}}/>
              {pinError && <div style={{color:'#ef4444',fontSize:'12px',marginBottom:'12px'}}>{pinError}</div>}
              <button onClick={handleUnlock}
                style={{width:'100%',padding:'12px',borderRadius:'8px',border:'none',
                  background:t.accent||'#c9a84c',color:'#000',fontWeight:'700',cursor:'pointer',fontSize:'14px'}}>
                Ontgrendelen
              </button>
            </div>
          ) : (
            <>
              <div style={{marginBottom:'24px'}}>
                <div style={{display:'flex',alignItems:'center',gap:'12px',marginBottom:'8px',flexWrap:'wrap'}}>
                  <span style={{fontSize:'12px',padding:'3px 10px',borderRadius:'6px',background:'#f59e0b20',color:'#f59e0b',fontWeight:'600',textTransform:'uppercase'}}>
                    {project.status}
                  </span>
                  <span style={{fontSize:'12px',color:t.textMuted||'#666',padding:'3px 8px',border:`1px solid ${t.border||'#333'}`,borderRadius:'6px'}}>
                    {project.template_type||project.type}
                  </span>
                  <span style={{fontSize:'12px',color:t.textMuted||'#666'}}>
                    Lead: <strong style={{color:t.textSecondary||'#aaa'}}>{project.lead_agent}</strong>
                  </span>
                  <button onClick={() => setShowLockModal(true)}
                    style={{marginLeft:'auto',fontSize:'11px',padding:'5px 12px',borderRadius:'6px',
                      border:`1px solid #ef444460`,background:'#ef444410',color:'#ef4444',cursor:'pointer',fontWeight:'600'}}>
                    🔒 Vergrendelen
                  </button>
                </div>
                <h1 style={{fontSize:'22px',fontWeight:'800',color:t.text||'#e2e8f0',margin:'0 0 8px'}}>{project.naam}</h1>
                {project.live_url && (
                  <a href={project.live_url} target="_blank" rel="noopener noreferrer" style={{color:t.accent||'#c9a84c',fontSize:'13px'}}>
                    {project.live_url} ↗
                  </a>
                )}
              </div>

              {/* Fase voortgang */}
              <div style={{marginBottom:'28px'}}>
                <div style={{fontSize:'12px',fontWeight:'600',color:t.textMuted||'#666',textTransform:'uppercase',letterSpacing:'0.08em',marginBottom:'12px'}}>Fase</div>
                <div style={{display:'flex',gap:'4px'}}>
                  {FASE_NAMEN.map((naam, i) => (
                    <div key={i} style={{flex:1,textAlign:'center'}}>
                      <div style={{height:'6px',borderRadius:'999px',marginBottom:'4px',
                        background:i<=project.fase?(t.accent||'#c9a84c'):`${t.border||'#333'}`}}/>
                      <span style={{fontSize:'9px',color:i<=project.fase?(t.text||'#e2e8f0'):(t.textMuted||'#666')}}>{naam}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Template voortgang (alleen voor intern type met voortgang_templates) */}
              {project.voortgang_templates && (
                <div style={{marginBottom:'28px'}}>
                  <div style={{fontSize:'12px',fontWeight:'600',color:t.textMuted||'#666',textTransform:'uppercase',letterSpacing:'0.08em',marginBottom:'12px'}}>Template Voortgang</div>
                  <div style={{padding:'14px 16px',background:t.bg2||'#111',borderRadius:'8px',border:`1px solid ${t.border||'#333'}`}}>
                    <div style={{display:'flex',justifyContent:'space-between',marginBottom:'8px'}}>
                      <span style={{fontSize:'13px',color:t.textMuted||'#666'}}>Maand {project.voortgang_templates.huidige_maand} — {project.voortgang_templates.huidige_variant}</span>
                      <span style={{fontSize:'13px',fontWeight:'700',color:t.accent||'#c9a84c'}}>{project.voortgang_templates.klaar}/{project.voortgang_templates.totaal}</span>
                    </div>
                    <div style={{width:'100%',height:'8px',background:`${t.border||'#333'}`,borderRadius:'999px',overflow:'hidden'}}>
                      <div style={{width:`${(project.voortgang_templates.klaar/project.voortgang_templates.totaal)*100}%`,height:'100%',background:t.accent||'#c9a84c',borderRadius:'999px'}}/>
                    </div>
                  </div>
                </div>
              )}

              {/* Agent tasks */}
              <div style={{marginBottom:'28px'}}>
                <div style={{fontSize:'12px',fontWeight:'600',color:t.textMuted||'#666',textTransform:'uppercase',letterSpacing:'0.08em',marginBottom:'12px'}}>Agent Taken</div>
                <div style={{display:'flex',flexDirection:'column',gap:'8px'}}>
                  {project.tasks && Object.entries(project.tasks).map(([agent, td]) => (
                    <div key={agent} style={{display:'flex',alignItems:'center',gap:'12px',padding:'10px 14px',background:t.bg2||'#111',borderRadius:'8px',border:`1px solid ${t.border||'#333'}`}}>
                      <div style={{width:'8px',height:'8px',borderRadius:'50%',background:TASK_KLEUR[td.status]||'#666',flexShrink:0}}/>
                      <span style={{fontSize:'13px',color:t.text||'#e2e8f0',flex:1,textTransform:'capitalize'}}>{agent}</span>
                      {td.notitie && <span style={{fontSize:'11px',color:t.textMuted||'#666',maxWidth:'200px',overflow:'hidden',textOverflow:'ellipsis',whiteSpace:'nowrap'}}>{td.notitie}</span>}
                      <span style={{fontSize:'11px',color:TASK_KLEUR[td.status]||'#666',fontWeight:'600',flexShrink:0}}>{TASK_LABEL[td.status]||td.status}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Documenten */}
              {project._docs && project._docs.length > 0 && (
                <div style={{marginBottom:'28px'}}>
                  <div style={{fontSize:'12px',fontWeight:'600',color:t.textMuted||'#666',textTransform:'uppercase',letterSpacing:'0.08em',marginBottom:'12px'}}>Documenten</div>
                  <div style={{display:'flex',flexWrap:'wrap',gap:'6px'}}>
                    {project._docs.map(doc => (
                      <span key={doc} style={{fontSize:'11px',padding:'4px 10px',borderRadius:'4px',
                        background:`${t.accent||'#c9a84c'}15`,color:t.accent||'#c9a84c',border:`1px solid ${t.accent||'#c9a84c'}30`}}>
                        {doc}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {/* SLA */}
              {project.sla_deadline && (
                <div style={{marginBottom:'28px'}}>
                  <div style={{fontSize:'12px',fontWeight:'600',color:t.textMuted||'#666',textTransform:'uppercase',letterSpacing:'0.08em',marginBottom:'12px'}}>SLA Deadline</div>
                  <div style={{padding:'12px 16px',background:t.bg2||'#111',borderRadius:'8px',border:`1px solid ${t.border||'#333'}`,fontSize:'13px',color:t.text||'#e2e8f0'}}>
                    {new Date(project.sla_deadline).toLocaleString('nl-NL')}
                  </div>
                </div>
              )}

              {/* Notities */}
              {project.notities && project.notities.length > 0 && (
                <div>
                  <div style={{fontSize:'12px',fontWeight:'600',color:t.textMuted||'#666',textTransform:'uppercase',letterSpacing:'0.08em',marginBottom:'12px'}}>Notities</div>
                  <div style={{display:'flex',flexDirection:'column',gap:'6px'}}>
                    {project.notities.map((n, i) => (
                      <div key={i} style={{padding:'10px 14px',background:t.bg2||'#111',borderRadius:'8px',border:`1px solid ${t.border||'#333'}`,fontSize:'12px',color:t.textSecondary||'#aaa'}}>
                        <strong style={{color:t.accent||'#c9a84c'}}>{n.agent}</strong>: {n.tekst}
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </>
          )}
        </div>
      )}

      {!project && !loading && (
        <div style={{flex:1,display:'flex',alignItems:'center',justifyContent:'center',color:t.textMuted||'#666'}}>
          Selecteer een project
        </div>
      )}
    </div>
  )
}
