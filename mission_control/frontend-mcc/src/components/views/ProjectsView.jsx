import React, { useState, useEffect } from 'react'

const FASE_NAMEN = ['Intake', 'Setup', 'Uitvoering', 'QA', 'Deploy', 'Nazorg']
const TASK_KLEUR = {
  done: '#10b981',
  in_progress: '#f59e0b',
  open: '#6b7280',
  wacht_op: '#6b7280',
  parallel_met: '#3b82f6',
  geblokkeerd: '#ef4444',
  overgeslagen: '#6b7280',
}
const TASK_LABEL = {
  done: 'Klaar',
  in_progress: 'Bezig',
  open: 'Open',
  wacht_op: 'Wacht',
  parallel_met: 'Parallel',
  geblokkeerd: 'Geblokkeerd',
  overgeslagen: 'N.v.t.',
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
  const isLocked = project?.locked && project?.status === 'locked'

  const handleUnlock = () => {
    fetch(`${API_BASE}/projects/${selectedId}/unlock`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ pin: pinInput })
    })
      .then(r => {
        if (!r.ok) throw new Error('Onjuiste PIN')
        return r.json()
      })
      .then(() => {
        setPinError('')
        setPinInput('')
        loadProjects()
      })
      .catch(() => setPinError('Onjuiste PIN, probeer opnieuw'))
  }

  const handleToggleLock = () => {
    if (!project) return
    const endpoint = project.locked ? 'unlock' : 'lock'
    const opts = endpoint === 'unlock'
      ? { method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify({pin: 'admin-override'}) }
      : { method: 'POST' }
    // Lock direct via PATCH naar locked:true/false (Fea heeft al toegang)
    fetch(`${API_BASE}/projects/${selectedId}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ locked: !project.locked })
    }).then(loadProjects)
  }

  const slaStatus = (p) => {
    if (!p.sla_deadline) return null
    const deadline = new Date(p.sla_deadline)
    const now = new Date()
    const diffH = (deadline - now) / 1000 / 3600
    if (p.status === 'live' || p.status === 'opgeleverd' || p.status === 'afgesloten') return 'groen'
    if (diffH < 0) return 'rood'
    if (diffH < 4) return 'oranje'
    return 'groen'
  }

  const SLA_KLEUR = { groen: '#10b981', oranje: '#f59e0b', rood: '#ef4444' }

  return (
    <div style={{display:'flex',height:'100%',overflow:'hidden'}}>

      {/* Sidebar */}
      <div style={{width:'280px',minWidth:'280px',borderRight:`1px solid ${t.border||'#333'}`,overflow:'auto',padding:'16px 0',display:'flex',flexDirection:'column'}}>

        <div style={{padding:'0 16px 12px',display:'flex',gap:'6px'}}>
          {['alle','klant','intern'].map(f => (
            <button key={f} onClick={() => setFilter(f)}
              style={{
                flex:1, padding:'6px 8px', fontSize:'11px', borderRadius:'6px', cursor:'pointer',
                border:`1px solid ${filter===f ? (t.accent||'#c9a84c') : (t.border||'#333')}`,
                background: filter===f ? `${t.accent||'#c9a84c'}20` : 'transparent',
                color: filter===f ? (t.accent||'#c9a84c') : (t.textMuted||'#666'),
                fontWeight: filter===f ? '600' : '400',
                textTransform:'capitalize'
              }}>
              {f}
            </button>
          ))}
        </div>

        <div style={{padding:'0 16px 12px',fontSize:'11px',color:t.textMuted||'#666',textTransform:'uppercase',letterSpacing:'0.08em'}}>
          Projecten {loading ? '(laden...)' : `(${projects.length})`}
        </div>

        {projects.map(p => {
          const locked = p.locked && p.status === 'locked'
          const sla = slaStatus(p)
          return (
            <div key={p.project_id} onClick={() => { setSelectedId(p.project_id); setPinError(''); setPinInput('') }}
              style={{padding:'12px 16px',cursor:'pointer',
                borderLeft: selectedId===p.project_id ? `3px solid ${t.accent||'#c9a84c'}` : '3px solid transparent',
                background: selectedId===p.project_id ? `${t.accent||'#c9a84c'}10` : 'transparent',
                opacity: locked ? 0.6 : 1}}>
              <div style={{display:'flex',alignItems:'center',gap:'8px',marginBottom:'4px'}}>
                {locked && <span style={{fontSize:'12px'}}>🔒</span>}
                <span style={{fontSize:'10px',padding:'2px 6px',borderRadius:'4px',
                  background:`${t.border||'#333'}40`,color:t.textMuted||'#888',fontWeight:'600',textTransform:'uppercase'}}>
                  {p.type || 'onbekend'}
                </span>
                {sla && !locked && (
                  <span style={{width:'6px',height:'6px',borderRadius:'50%',background:SLA_KLEUR[sla]}}/>
                )}
              </div>
              <div style={{fontSize:'13px',color:t.text||'#e2e8f0',fontWeight:'500'}}>{p.naam}</div>
              <div style={{fontSize:'11px',color:t.textMuted||'#666',marginTop:'2px'}}>
                {locked ? '🔒 Vergrendeld' : (FASE_NAMEN[p.fase] || p.fase_naam || '')}
              </div>
            </div>
          )
        })}

        {projects.length === 0 && !loading && (
          <div style={{padding:'16px',fontSize:'12px',color:t.textMuted||'#666'}}>
            Geen projecten gevonden.
          </div>
        )}
      </div>

      {/* Detail */}
      {project && (
        <div style={{flex:1,overflow:'auto',padding:'32px'}}>

          {isLocked ? (
            <div style={{maxWidth:'320px',margin:'80px auto',textAlign:'center'}}>
              <div style={{fontSize:'40px',marginBottom:'16px'}}>🔒</div>
              <h2 style={{color:t.text||'#e2e8f0',marginBottom:'8px'}}>{project.naam}</h2>
              <p style={{color:t.textMuted||'#666',fontSize:'13px',marginBottom:'20px'}}>
                {project.lock_hint || 'Dit project is vergrendeld'}
              </p>
              <input type="password" value={pinInput} onChange={e => setPinInput(e.target.value)}
                placeholder="PIN" onKeyDown={e => e.key === 'Enter' && handleUnlock()}
                style={{width:'100%',padding:'10px',borderRadius:'8px',border:`1px solid ${t.border||'#333'}`,
                  background:t.bg2||'#111',color:t.text||'#fff',marginBottom:'8px',textAlign:'center'}}/>
              {pinError && <div style={{color:'#ef4444',fontSize:'12px',marginBottom:'8px'}}>{pinError}</div>}
              <button onClick={handleUnlock}
                style={{width:'100%',padding:'10px',borderRadius:'8px',border:'none',
                  background:t.accent||'#c9a84c',color:'#000',fontWeight:'600',cursor:'pointer'}}>
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
                    {project.template_type || project.type}
                  </span>
                  <span style={{fontSize:'12px',color:t.textMuted||'#666'}}>
                    Lead: <strong style={{color:t.textSecondary||'#aaa'}}>{project.lead_agent}</strong>
                  </span>
                  <button onClick={handleToggleLock}
                    style={{marginLeft:'auto',fontSize:'11px',padding:'4px 10px',borderRadius:'6px',
                      border:`1px solid ${t.border||'#333'}`,background:'transparent',color:t.textMuted||'#666',cursor:'pointer'}}>
                    {project.locked ? '🔓 Unlock' : '🔒 Lock'}
                  </button>
                </div>
                <h1 style={{fontSize:'22px',fontWeight:'800',color:t.text||'#e2e8f0',margin:'0 0 8px'}}>{project.naam}</h1>
                {project.live_url && (
                  <a href={project.live_url} target="_blank" rel="noopener noreferrer" style={{color:t.accent||'#c9a84c',fontSize:'13px'}}>
                    {project.live_url} ↗
                  </a>
                )}
              </div>

              {/* Voortgangsbalk fase */}
              <div style={{marginBottom:'28px'}}>
                <div style={{fontSize:'12px',fontWeight:'600',color:t.textMuted||'#666',textTransform:'uppercase',letterSpacing:'0.08em',marginBottom:'12px'}}>Fase</div>
                <div style={{display:'flex',gap:'4px',marginBottom:'8px'}}>
                  {FASE_NAMEN.map((naam, i) => (
                    <div key={i} style={{flex:1,textAlign:'center'}}>
                      <div style={{height:'6px',borderRadius:'999px',
                        background: i <= project.fase ? (t.accent||'#c9a84c') : `${t.border||'#333'}`,marginBottom:'4px'}}/>
                      <span style={{fontSize:'9px',color: i <= project.fase ? (t.text||'#e2e8f0') : (t.textMuted||'#666')}}>{naam}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Agent tasks */}
              <div style={{marginBottom:'28px'}}>
                <div style={{fontSize:'12px',fontWeight:'600',color:t.textMuted||'#666',textTransform:'uppercase',letterSpacing:'0.08em',marginBottom:'12px'}}>Agent Taken</div>
                <div style={{display:'flex',flexDirection:'column',gap:'8px'}}>
                  {project.tasks && Object.entries(project.tasks).map(([agent, taskData]) => (
                    <div key={agent} style={{display:'flex',alignItems:'center',gap:'12px',padding:'10px 14px',background:t.bg2||'#111',borderRadius:'8px',border:`1px solid ${t.border||'#333'}`}}>
                      <div style={{width:'8px',height:'8px',borderRadius:'50%',background:TASK_KLEUR[taskData.status]||'#666',flexShrink:0}}/>
                      <span style={{fontSize:'13px',color:t.text||'#e2e8f0',flex:1,textTransform:'capitalize'}}>{agent}</span>
                      {taskData.wacht_op && <span style={{fontSize:'10px',color:t.textMuted||'#666'}}>wacht op {taskData.wacht_op.join(', ')}</span>}
                      <span style={{fontSize:'11px',color:TASK_KLEUR[taskData.status]||'#666',fontWeight:'600'}}>{TASK_LABEL[taskData.status]||taskData.status}</span>
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
                      <span key={doc} style={{fontSize:'11px',padding:'4px 10px',borderRadius:'4px',background:`${t.accent||'#c9a84c'}15`,color:t.accent||'#c9a84c',border:`1px solid ${t.accent||'#c9a84c'}30`}}>
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
                        <strong>{n.agent}</strong>: {n.tekst}
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
