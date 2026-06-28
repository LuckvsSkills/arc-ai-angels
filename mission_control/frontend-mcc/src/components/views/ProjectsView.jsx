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
  const [modal, setModal] = useState(null)
  const [pin, setPin] = useState('')
  const [pinErr, setPinErr] = useState('')
  const [view, setView] = useState('list') // 'list' | 'detail'
  const [winW, setWinW] = useState(window.innerWidth)
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

  useEffect(() => { load(); const i = setInterval(load, 15000); return () => clearInterval(i) }, [filter])

  const project = projects.find(p => p.project_id === selectedId)
  const isLocked = project?.locked === true

  const openModal = (type) => { setModal(type); setPin(''); setPinErr('') }
  const closeModal = () => { setModal(null); setPin(''); setPinErr('') }

  const handleUnlock = () => {
    fetch(`${API}/projects/${selectedId}/unlock`, {
      method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify({pin})
    })
    .then(r => { if (!r.ok) throw new Error(); return r.json() })
    .then(() => fetch(`${API}/projects/${selectedId}`, {
      method: 'PATCH', headers: {'Content-Type':'application/json'}, body: JSON.stringify({locked: false})
    }))
    .then(() => { closeModal(); load(); if (isMobile) setView('detail') })
    .catch(() => setPinErr('Onjuiste PIN'))
  }

  const handleLock = () => {
    fetch(`${API}/projects/${selectedId}/unlock`, {
      method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify({pin})
    })
    .then(r => { if (!r.ok) throw new Error(); return r.json() })
    .then(() => fetch(`${API}/projects/${selectedId}`, {
      method: 'PATCH', headers: {'Content-Type':'application/json'}, body: JSON.stringify({locked: true})
    }))
    .then(() => { closeModal(); load() })
    .catch(() => setPinErr('Onjuiste PIN'))
  }

  const slaKleur = (p) => {
    if (!p.sla_deadline) return null
    const h = (new Date(p.sla_deadline) - new Date()) / 3600000
    if (['live','opgeleverd','afgesloten'].includes(p.status)) return '#10b981'
    return h < 0 ? '#ef4444' : h < 4 ? '#f59e0b' : '#10b981'
  }

  const selectProject = (id) => {
    setSelectedId(id)
    if (isMobile) setView('detail')
  }

  // PIN Modal
  const PinModal = () => modal ? (
    <div onClick={e => e.target === e.currentTarget && closeModal()}
      style={{position:'fixed',inset:0,background:'rgba(0,0,0,0.8)',zIndex:200,display:'flex',alignItems:'center',justifyContent:'center',padding:'20px'}}>
      <div style={{background:t.bg||'#0d0d0d',border:`1px solid ${t.border||'#333'}`,borderRadius:'16px',padding:'28px',width:'100%',maxWidth:'300px',textAlign:'center'}}>
        <div style={{fontSize:'36px',marginBottom:'10px'}}>{modal==='unlock'?'🔓':'🔒'}</div>
        <h3 style={{color:t.text||'#e2e8f0',marginBottom:'6px',fontSize:'15px'}}>
          {modal==='unlock' ? 'Project ontgrendelen' : 'Project vergrendelen'}
        </h3>
        <p style={{color:t.textMuted||'#666',fontSize:'12px',marginBottom:'16px'}}>Voer PIN in om te bevestigen</p>
        <input autoFocus type="password" value={pin}
          onChange={e => { setPin(e.target.value); setPinErr('') }}
          onKeyDown={e => e.key==='Enter' && (modal==='unlock' ? handleUnlock() : handleLock())}
          placeholder="● ● ● ●"
          style={{width:'100%',padding:'12px',borderRadius:'10px',
            border:`2px solid ${pinErr?'#ef4444':(t.border||'#444')}`,
            background:t.bg2||'#1a1a1a',color:t.text||'#fff',
            textAlign:'center',fontSize:'20px',letterSpacing:'8px',
            boxSizing:'border-box',outline:'none',marginBottom:'8px'}}/>
        {pinErr && <p style={{color:'#ef4444',fontSize:'12px',marginBottom:'8px'}}>{pinErr}</p>}
        <div style={{display:'flex',gap:'8px',marginTop:'8px'}}>
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
  ) : null

  // Project lijst
  const ListView = () => (
    <div style={{display:'flex',flexDirection:'column',height:'100%',overflow:'hidden'}}>
      <div style={{padding:'12px',display:'flex',gap:'6px',flexShrink:0}}>
        {['alle','klant','intern'].map(f => (
          <button key={f} onClick={() => setFilter(f)} style={{
            flex:1,padding:'6px',fontSize:'11px',borderRadius:'6px',cursor:'pointer',
            border:`1px solid ${filter===f?(t.accent||'#c9a84c'):(t.border||'#333')}`,
            background:filter===f?`${t.accent||'#c9a84c'}20`:'transparent',
            color:filter===f?(t.accent||'#c9a84c'):(t.textMuted||'#666'),
            fontWeight:filter===f?'600':'400',textTransform:'capitalize'
          }}>{f}</button>
        ))}
      </div>
      <div style={{padding:'0 14px 8px',fontSize:'11px',color:t.textMuted||'#555',textTransform:'uppercase',letterSpacing:'0.08em',flexShrink:0}}>
        {loading ? 'Laden...' : `${projects.length} project${projects.length!==1?'en':''}`}
      </div>
      <div style={{flex:1,overflow:'auto'}}>
        {projects.map(p => {
          const lck = p.locked === true
          const sla = slaKleur(p)
          const isSel = selectedId === p.project_id
          return (
            <div key={p.project_id} onClick={() => selectProject(p.project_id)}
              style={{padding:'12px 14px',cursor:'pointer',
                borderLeft:`3px solid ${isSel?(t.accent||'#c9a84c'):'transparent'}`,
                background:isSel?`${t.accent||'#c9a84c'}12`:'transparent',
                borderBottom:`1px solid ${t.border||'#222'}`}}>
              <div style={{display:'flex',alignItems:'center',gap:'6px',marginBottom:'4px'}}>
                {lck
                  ? <span style={{fontSize:'10px',padding:'2px 7px',borderRadius:'4px',background:'#ef444425',color:'#ef4444',fontWeight:'700',border:'1px solid #ef444440'}}>🔒 LOCKED</span>
                  : <span style={{fontSize:'10px',padding:'2px 7px',borderRadius:'4px',background:`${t.border||'#333'}40`,color:t.textMuted||'#666',fontWeight:'600',textTransform:'uppercase'}}>{p.type}</span>
                }
                {sla && <span style={{width:'6px',height:'6px',borderRadius:'50%',background:sla,marginLeft:'auto',flexShrink:0}}/>}
              </div>
              <div style={{fontSize:'13px',fontWeight:'600',marginBottom:'2px',color:t.text||'#e2e8f0'}}>
                {lck ? <span style={{filter:'blur(4px)',userSelect:'none'}}>████████████</span> : p.naam}
              </div>
              <div style={{fontSize:'11px',color:t.textMuted||'#555'}}>
                {lck ? 'Klik om te openen →' : (FASE_NAMEN[p.fase]||'')}
              </div>
            </div>
          )
        })}
        {!loading && projects.length === 0 && (
          <div style={{padding:'20px',fontSize:'12px',color:t.textMuted||'#555',textAlign:'center'}}>
            Geen projecten gevonden
          </div>
        )}
      </div>
    </div>
  )

  // Project detail
  const DetailView = () => (
    <div style={{flex:1,overflow:'auto',padding:'20px'}}>
      {isMobile && (
        <button onClick={() => setView('list')}
          style={{display:'flex',alignItems:'center',gap:'6px',fontSize:'12px',color:t.textMuted||'#666',
            background:'transparent',border:'none',cursor:'pointer',padding:'0 0 16px 0',width:'100%'}}>
          ← Terug
        </button>
      )}

      {isLocked ? (
        <div style={{maxWidth:'320px',margin:'40px auto',textAlign:'center'}}>
          <div style={{fontSize:'48px',marginBottom:'16px'}}>🔒</div>
          <h2 style={{color:t.text||'#e2e8f0',marginBottom:'8px',fontSize:'18px'}}>Vergrendeld project</h2>
          <p style={{color:t.textMuted||'#666',fontSize:'13px',marginBottom:'24px'}}>
            {project?.lock_hint || 'Voer PIN in om dit project te bekijken'}
          </p>
          <button onClick={() => openModal('unlock')}
            style={{padding:'14px 24px',borderRadius:'10px',border:'none',
              background:t.accent||'#c9a84c',color:'#000',fontWeight:'700',cursor:'pointer',fontSize:'14px',width:'100%'}}>
            🔓 Ontgrendelen
          </button>
        </div>
      ) : project ? (
        <>
          <div style={{display:'flex',alignItems:'flex-start',justifyContent:'space-between',gap:'12px',marginBottom:'20px',flexWrap:'wrap'}}>
            <div style={{flex:1,minWidth:0}}>
              <div style={{display:'flex',gap:'8px',marginBottom:'8px',flexWrap:'wrap'}}>
                <span style={{fontSize:'11px',padding:'3px 8px',borderRadius:'5px',background:'#f59e0b20',color:'#f59e0b',fontWeight:'600',textTransform:'uppercase'}}>
                  {project.status}
                </span>
                <span style={{fontSize:'11px',color:t.textMuted||'#666',padding:'3px 8px',border:`1px solid ${t.border||'#333'}`,borderRadius:'5px'}}>
                  {project.type}
                </span>
              </div>
              <h1 style={{fontSize:'18px',fontWeight:'800',color:t.text||'#e2e8f0',margin:'0 0 4px',wordBreak:'break-word'}}>{project.naam}</h1>
              <div style={{fontSize:'12px',color:t.textMuted||'#666'}}>Lead: <strong style={{color:t.accent||'#c9a84c'}}>{project.lead_agent}</strong></div>
            </div>
            <button onClick={() => openModal('lock')}
              style={{padding:'7px 12px',borderRadius:'8px',fontSize:'11px',fontWeight:'600',
                border:'1px solid #ef444450',background:'#ef444412',color:'#ef4444',cursor:'pointer',flexShrink:0}}>
              🔒 Lock
            </button>
          </div>

          <div style={{marginBottom:'20px'}}>
            <div style={{fontSize:'11px',fontWeight:'600',color:t.textMuted||'#666',textTransform:'uppercase',marginBottom:'8px'}}>Fase</div>
            <div style={{display:'flex',gap:'3px'}}>
              {FASE_NAMEN.map((n,i) => (
                <div key={i} style={{flex:1,textAlign:'center'}}>
                  <div style={{height:'5px',borderRadius:'999px',marginBottom:'3px',background:i<=project.fase?(t.accent||'#c9a84c'):`${t.border||'#333'}`}}/>
                  <span style={{fontSize:'8px',color:i<=project.fase?(t.text||'#e2e8f0'):(t.textMuted||'#555')}}>{n}</span>
                </div>
              ))}
            </div>
          </div>

          {project.voortgang_templates && (
            <div style={{marginBottom:'20px',padding:'14px',background:t.bg2||'#111',borderRadius:'10px',border:`1px solid ${t.border||'#333'}`}}>
              <div style={{display:'flex',justifyContent:'space-between',alignItems:'center',marginBottom:'8px'}}>
                <span style={{fontSize:'12px',color:t.text||'#e2e8f0',fontWeight:'600'}}>Template Voortgang</span>
                <span style={{fontSize:'16px',fontWeight:'800',color:t.accent||'#c9a84c'}}>
                  {project.voortgang_templates.klaar}/{project.voortgang_templates.totaal}
                </span>
              </div>
              <div style={{height:'6px',background:`${t.border||'#333'}`,borderRadius:'999px',overflow:'hidden'}}>
                <div style={{width:`${(project.voortgang_templates.klaar/project.voortgang_templates.totaal)*100}%`,height:'100%',background:t.accent||'#c9a84c'}}/>
              </div>
            </div>
          )}

          {project.tasks && Object.keys(project.tasks).length > 0 && (
            <div style={{marginBottom:'20px'}}>
              <div style={{fontSize:'11px',fontWeight:'600',color:t.textMuted||'#666',textTransform:'uppercase',marginBottom:'8px'}}>Agent Taken</div>
              {Object.entries(project.tasks).map(([agent, td]) => (
                <div key={agent} style={{display:'flex',alignItems:'center',gap:'10px',padding:'9px 12px',
                  background:t.bg2||'#111',borderRadius:'8px',border:`1px solid ${t.border||'#333'}`,marginBottom:'6px'}}>
                  <div style={{width:'7px',height:'7px',borderRadius:'50%',background:TASK_KLEUR[td.status]||'#666',flexShrink:0}}/>
                  <span style={{fontSize:'12px',color:t.text||'#e2e8f0',flex:1,textTransform:'capitalize'}}>{agent}</span>
                  <span style={{fontSize:'10px',color:TASK_KLEUR[td.status]||'#666',fontWeight:'700',flexShrink:0}}>{TASK_LABEL[td.status]||td.status}</span>
                </div>
              ))}
            </div>
          )}

          {project.notities?.length > 0 && (
            <div style={{marginBottom:'20px'}}>
              <div style={{fontSize:'11px',fontWeight:'600',color:t.textMuted||'#666',textTransform:'uppercase',marginBottom:'8px'}}>Notities</div>
              {project.notities.map((n,i) => (
                <div key={i} style={{padding:'10px 12px',background:t.bg2||'#111',borderRadius:'8px',
                  border:`1px solid ${t.border||'#333'}`,fontSize:'12px',color:t.textSecondary||'#aaa',marginBottom:'6px'}}>
                  <strong style={{color:t.accent||'#c9a84c'}}>{n.agent}</strong>: {n.tekst}
                </div>
              ))}
            </div>
          )}

          {project.sla_deadline && (
            <div style={{padding:'12px',background:t.bg2||'#111',borderRadius:'8px',border:`1px solid ${t.border||'#333'}`,fontSize:'12px',color:t.textMuted||'#666'}}>
              SLA: <strong style={{color:t.text||'#e2e8f0'}}>{new Date(project.sla_deadline).toLocaleString('nl-NL')}</strong>
            </div>
          )}
        </>
      ) : null}
    </div>
  )

  return (
    <div style={{height:'100%',display:'flex',flexDirection:'column',overflow:'hidden',position:'relative'}}>
      <PinModal/>
      {isMobile ? (
        view === 'list' ? <ListView/> : <DetailView/>
      ) : (
        <div style={{display:'flex',height:'100%',overflow:'hidden'}}>
          <div style={{width:'270px',minWidth:'270px',borderRight:`1px solid ${t.border||'#333'}`,overflow:'hidden',display:'flex',flexDirection:'column'}}>
            <ListView/>
          </div>
          <DetailView/>
        </div>
      )}
    </div>
  )
}
