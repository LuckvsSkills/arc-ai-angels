import React, { useState, useEffect } from 'react'

const DOMAIN_COLORS = {
  core:'#c9a84c', helix:'#38bdf8', finix:'#f472b6',
  matrix:'#34d399', quantix:'#a78bfa', zenix:'#fb923c'
}
const DOMAIN_AGENTS = {
  core:    ['nova','flux'],
  helix:   ['cortexia','nero','forge','axon','ventura','clio'],
  finix:   ['finoria','kairo','kenzo','odis','vector','zion'],
  matrix:  ['saelia','tharos','sora','arix','enki','daxio'],
  quantix: ['lumeria','kresta','elora','luvia','nura','vondra'],
  zenix:   ['fluentia','draven','solis','orizon','unia','zena'],
}
const AGENT_DOMAIN = {}
Object.entries(DOMAIN_AGENTS).forEach(([d,agents]) => agents.forEach(a => AGENT_DOMAIN[a]=d))
const AGENT_EMOJI = {
  nova:'🌟',flux:'⚡',cortexia:'💡',nero:'🛡️',forge:'⚙️',axon:'🔗',
  ventura:'🏗️',clio:'📝',finoria:'💰',kairo:'📈',kenzo:'🔢',odis:'💎',
  vector:'📊',zion:'⚖️',saelia:'🧠',tharos:'📚',sora:'🤖',arix:'🗂️',
  enki:'🔬',daxio:'⚡',lumeria:'✨',kresta:'🎯',elora:'🔍',luvia:'📐',
  nura:'⚡',vondra:'👁️',fluentia:'🌊',draven:'🌀',solis:'☀️',
  orizon:'🌅',unia:'💫',zena:'🎨'
}

export default function SkillsTab({ theme }) {
  const t = theme?.colors || {}
  const acc = t.accent || '#c9a84c'
  const [tab, setTab] = useState('pending')
  const [pending, setPending] = useState(null)
  const [approved, setApproved] = useState(null)
  const [loading, setLoading] = useState(true)
  const [expanded, setExpanded] = useState(null)
  const [rejectId, setRejectId] = useState(null)
  const [rejectReason, setRejectReason] = useState('')
  const [toast, setToast] = useState(null)
  const [selectedAgent, setSelectedAgent] = useState(null)
  const [selectedSkill, setSelectedSkill] = useState(null)
  const [skillContent, setSkillContent] = useState(null)

  const showToast = (msg, color='#22c55e') => {
    setToast({msg, color})
    setTimeout(() => setToast(null), 3000)
  }

  const load = () => {
    setLoading(true)
    Promise.all([
      fetch('/api/skills/pending').then(r=>r.json()).catch(()=>null),
      fetch('/api/skills/approved').then(r=>r.json()).catch(()=>null),
    ]).then(([p, a]) => {
      setPending(p)
      setApproved(a)
      setLoading(false)
    })
  }

  useEffect(() => { load() }, [])

  const approve = async (id, title) => {
    const r = await fetch(`/api/skills/approve/${id}`, {method:'POST'})
    const d = await r.json()
    if (d.ok) {
      showToast(`✅ ${title} goedgekeurd`)
      // Verwijder uit lokale state direct
      setPending(prev => prev ? {
        ...prev,
        skills: prev.skills.filter(s => s.id !== id),
        unique: prev.unique - 1,
        total: prev.total - 1,
      } : prev)
      load()
    } else {
      showToast(`❌ Fout: ${d.error}`, '#ef4444')
    }
  }

  const reject = async (id) => {
    const r = await fetch(`/api/skills/reject/${id}`, {
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body: JSON.stringify({reason: rejectReason || 'Afgewezen door Supreme Fea'})
    })
    const d = await r.json()
    if (d.ok) {
      showToast('❌ Skill afgewezen', '#f59e0b')
      // Verwijder uit lokale state direct
      setPending(prev => prev ? {
        ...prev,
        skills: prev.skills.filter(s => s.id !== id),
        unique: prev.unique - 1,
        total: prev.total - 1,
      } : prev)
      setRejectId(null)
      setRejectReason('')
    }
  }

  const loadSkillContent = (agent, skillName) => {
    setSelectedSkill(skillName)
    setSkillContent(null)
    fetch(`/api/skills/content/${agent}/${skillName}`)
      .then(r=>r.json())
      .then(d => setSkillContent(d.content))
      .catch(() => setSkillContent('Kon skill niet laden'))
  }

  const byAgent = approved?.by_agent || {}
  const pendingSkills = pending?.skills || []
  const pendingCount = pending?.unique || 0

  // Bouw skill bibliotheek — alle skills met welke agents ze hebben
  const skillLibrary = {}
  Object.entries(byAgent).forEach(([agent, skills]) => {
    skills.forEach(skill => {
      if (!skillLibrary[skill]) skillLibrary[skill] = []
      skillLibrary[skill].push(agent)
    })
  })
  const sortedLibrary = Object.entries(skillLibrary).sort((a,b) => b[1].length - a[1].length)

  return (
    <div style={{height:'100%',display:'flex',flexDirection:'column',overflow:'hidden',position:'relative'}}>

      {/* Toast */}
      {toast && (
        <div style={{position:'absolute',top:12,right:16,zIndex:100,background:toast.color,color:'#fff',padding:'8px 16px',borderRadius:8,fontSize:12,fontWeight:700,boxShadow:'0 4px 12px rgba(0,0,0,0.3)'}}>
          {toast.msg}
        </div>
      )}

      {/* Sub tabs */}
      <div style={{display:'flex',gap:2,padding:'10px 16px 0',borderBottom:`1px solid ${t.border}`,flexShrink:0}}>
        {[
          ['pending','ti-clock','Pending Approvals', pendingCount],
          ['active','ti-check','Actieve Skills', null],
          ['library','ti-books','Skill Bibliotheek', null],
        ].map(([id,icon,label,badge]) => (
          <button key={id} onClick={() => setTab(id)}
            style={{padding:'6px 14px',borderRadius:'7px 7px 0 0',border:`1px solid ${tab===id?t.border:'transparent'}`,borderBottom:tab===id?`1px solid ${t.bgSecondary||'#111'}`:'none',background:tab===id?t.bgSecondary:'transparent',color:tab===id?acc:t.textMuted,fontSize:12,fontWeight:tab===id?700:400,cursor:'pointer',display:'flex',alignItems:'center',gap:5,marginBottom:tab===id?-1:0}}>
            <i className={`ti ${icon}`} style={{fontSize:12}}/>{label}
            {badge > 0 && <span style={{background:'#ef4444',color:'#fff',borderRadius:10,padding:'0 5px',fontSize:9,fontWeight:700,minWidth:16,textAlign:'center'}}>{badge}</span>}
          </button>
        ))}
        <button onClick={load} style={{marginLeft:'auto',padding:'6px 10px',background:'transparent',border:'none',color:t.textMuted,cursor:'pointer',fontSize:12}}>
          <i className="ti ti-refresh"/>
        </button>
      </div>

      <div style={{flex:1,overflow:'auto',padding:'14px 16px'}}>

        {/* TAB 1 — PENDING APPROVALS */}
        {tab === 'pending' && (
          <div style={{display:'flex',flexDirection:'column',gap:10}}>
            {loading ? (
              <div style={{color:t.textMuted,fontSize:12,padding:20}}>Laden...</div>
            ) : pendingSkills.length === 0 ? (
              <div style={{textAlign:'center',color:t.textMuted,padding:40}}>
                <i className="ti ti-check" style={{fontSize:32,display:'block',marginBottom:10,opacity:0.3}}/>
                <div style={{fontSize:13}}>Geen skills ter goedkeuring</div>
              </div>
            ) : (
              <>
                <div style={{fontSize:11,color:t.textMuted,marginBottom:4}}>
                  <strong style={{color:acc}}>{pendingSkills.length}</strong> skills wachten op jouw goedkeuring
                </div>
                {pendingSkills.map(skill => {
                  const domainColor = DOMAIN_COLORS[AGENT_DOMAIN[skill.agent_id]] || acc
                  const isExpanded = expanded === skill.id
                  const isRejecting = rejectId === skill.id
                  return (
                    <div key={skill.id} style={{background:`linear-gradient(135deg,${domainColor}18 0%,${domainColor}06 100%)`,border:`1.5px solid ${domainColor}35`,borderRadius:12,padding:'14px 16px',position:'relative',overflow:'hidden'}}>
                      <div style={{position:'absolute',top:0,left:0,right:0,height:2,background:`linear-gradient(90deg,${domainColor}00,${domainColor}80,${domainColor}00)`}}/>

                      <div style={{display:'flex',alignItems:'flex-start',gap:10,marginBottom:8}}>
                        <span style={{fontSize:20}}>{AGENT_EMOJI[skill.agent_id]||'🤖'}</span>
                        <div style={{flex:1}}>
                          <div style={{display:'flex',alignItems:'center',gap:6,marginBottom:2}}>
                            <span style={{fontSize:12,fontWeight:700,color:t.text}}>{skill.title}</span>
                            <span style={{fontSize:9,fontWeight:700,color:domainColor,background:`${domainColor}15`,borderRadius:4,padding:'1px 6px',textTransform:'uppercase'}}>{skill.action}</span>
                          </div>
                          <div style={{display:'flex',gap:6,alignItems:'center'}}>
                            <span style={{fontSize:10,color:domainColor,fontWeight:700}}>{skill.agent_id}</span>
                            <span style={{fontSize:9,color:t.textMuted}}>·</span>
                            <span style={{fontSize:9,color:t.textMuted,fontFamily:'monospace'}}>{skill.skill_name}</span>
                            <span style={{fontSize:9,color:t.textMuted}}>·</span>
                            <span style={{fontSize:9,color:t.textMuted}}>{skill.timestamp?.slice(0,10)}</span>
                          </div>
                        </div>
                      </div>

                      <div style={{fontSize:11,color:t.textMuted,lineHeight:1.6,marginBottom:8}}>{skill.description}</div>

                      <div style={{fontSize:10,color:t.textMuted,background:'rgba(0,0,0,0.2)',borderRadius:6,padding:'6px 10px',marginBottom:10}}>
                        <strong style={{color:t.text}}>Reden: </strong>{skill.reason}
                      </div>

                      <button onClick={() => setExpanded(isExpanded ? null : skill.id)}
                        style={{background:'transparent',border:`1px solid ${t.border}`,color:t.textMuted,fontSize:10,padding:'4px 10px',borderRadius:6,cursor:'pointer',marginBottom:isExpanded?10:0,display:'flex',alignItems:'center',gap:4}}>
                        <i className={`ti ti-chevron-${isExpanded?'up':'down'}`} style={{fontSize:10}}/>
                        {isExpanded ? 'Verberg inhoud' : 'Bekijk volledige skill inhoud'}
                      </button>

                      {isExpanded && (
                        <div style={{background:'rgba(0,0,0,0.25)',borderRadius:8,padding:'10px 12px',marginBottom:10,fontFamily:'monospace',fontSize:10,color:t.text,lineHeight:1.7,whiteSpace:'pre-wrap',overflowX:'auto'}}>
                          {skill.body}
                        </div>
                      )}

                      {isRejecting && (
                        <div style={{marginBottom:10}}>
                          <input placeholder="Reden voor afwijzing (optioneel)..."
                            value={rejectReason} onChange={e => setRejectReason(e.target.value)}
                            style={{width:'100%',padding:'7px 10px',borderRadius:7,border:`1px solid #ef444440`,background:'rgba(0,0,0,0.2)',color:t.text,fontSize:11,outline:'none',boxSizing:'border-box'}}/>
                        </div>
                      )}

                      <div style={{display:'flex',gap:8,marginTop:10}}>
                        <button onClick={() => approve(skill.id, skill.title)}
                          style={{padding:'7px 16px',borderRadius:7,border:'1.5px solid #22c55e40',background:'#22c55e15',color:'#22c55e',cursor:'pointer',fontSize:11,fontWeight:700,display:'flex',alignItems:'center',gap:5}}>
                          <i className="ti ti-check" style={{fontSize:12}}/> Goedkeuren
                        </button>
                        {isRejecting ? (
                          <>
                            <button onClick={() => reject(skill.id)}
                              style={{padding:'7px 16px',borderRadius:7,border:'1.5px solid #ef444440',background:'#ef444415',color:'#ef4444',cursor:'pointer',fontSize:11,fontWeight:700}}>
                              Bevestig afwijzing
                            </button>
                            <button onClick={() => setRejectId(null)}
                              style={{padding:'7px 10px',borderRadius:7,border:`1px solid ${t.border}`,background:'transparent',color:t.textMuted,cursor:'pointer',fontSize:11}}>
                              Annuleer
                            </button>
                          </>
                        ) : (
                          <button onClick={() => setRejectId(skill.id)}
                            style={{padding:'7px 16px',borderRadius:7,border:'1.5px solid #ef444430',background:'#ef444410',color:'#ef4444',cursor:'pointer',fontSize:11,fontWeight:700,display:'flex',alignItems:'center',gap:5}}>
                            <i className="ti ti-x" style={{fontSize:12}}/> Afwijzen
                          </button>
                        )}
                      </div>
                    </div>
                  )
                })}
              </>
            )}
          </div>
        )}

        {/* TAB 2 — ACTIEVE SKILLS per agent */}
        {tab === 'active' && (
          <div style={{display:'flex',gap:12,height:'100%'}}>

            {/* Links — agent kaarten per domein */}
            <div style={{width:220,flexShrink:0,overflowY:'auto',display:'flex',flexDirection:'column',gap:12}}>
              {Object.entries(DOMAIN_AGENTS).map(([domain, agents]) => {
                const domainColor = DOMAIN_COLORS[domain]
                const activeAgents = agents.filter(a => byAgent[a])
                if (activeAgents.length === 0) return null
                return (
                  <div key={domain}>
                    <div style={{fontSize:9,fontWeight:700,color:domainColor,textTransform:'uppercase',letterSpacing:'0.1em',marginBottom:6,display:'flex',alignItems:'center',gap:4}}>
                      <div style={{width:8,height:8,borderRadius:'50%',background:domainColor}}/>
                      {domain}
                    </div>
                    <div style={{display:'flex',flexDirection:'column',gap:4}}>
                      {activeAgents.map(agent => {
                        const isSelected = selectedAgent === agent
                        return (
                          <div key={agent} onClick={() => {setSelectedAgent(agent); setSelectedSkill(null); setSkillContent(null)}}
                            style={{background:isSelected?`${domainColor}25`:t.bgSecondary,borderLeft:`3px solid ${isSelected?domainColor:domainColor+'50'}`,border:`1px solid ${isSelected?domainColor+'50':t.border}`,borderLeft:`3px solid ${isSelected?domainColor:domainColor+'50'}`,borderRadius:8,padding:'8px 10px',cursor:'pointer',display:'flex',alignItems:'center',gap:8,transition:'all .15s'}}>
                            <span style={{fontSize:14}}>{AGENT_EMOJI[agent]||'🤖'}</span>
                            <div style={{flex:1}}>
                              <div style={{fontSize:11,fontWeight:isSelected?700:400,color:isSelected?domainColor:t.text}}>{agent}</div>
                              <div style={{fontSize:9,color:t.textMuted}}>{byAgent[agent]?.length||0} skills</div>
                            </div>
                            {isSelected && <div style={{width:5,height:5,borderRadius:'50%',background:domainColor}}/>}
                          </div>
                        )
                      })}
                    </div>
                  </div>
                )
              })}
            </div>

            {/* Midden — skills van geselecteerde agent */}
            <div style={{flex:1,overflowY:'auto'}}>
              {!selectedAgent ? (
                <div style={{textAlign:'center',color:t.textMuted,padding:40,fontSize:12}}>
                  <i className="ti ti-arrow-left" style={{fontSize:24,display:'block',marginBottom:10,opacity:0.3}}/>
                  Selecteer een agent
                </div>
              ) : (
                <div style={{display:'flex',flexDirection:'column',gap:8}}>
                  <div style={{display:'flex',alignItems:'center',gap:10,marginBottom:4}}>
                    <span style={{fontSize:22}}>{AGENT_EMOJI[selectedAgent]||'🤖'}</span>
                    <div>
                      <div style={{fontSize:14,fontWeight:700,color:t.text}}>{selectedAgent}</div>
                      <div style={{fontSize:10,color:DOMAIN_COLORS[AGENT_DOMAIN[selectedAgent]]||acc}}>{byAgent[selectedAgent]?.length||0} skills actief</div>
                    </div>
                  </div>
                  <div style={{display:'grid',gridTemplateColumns:'repeat(auto-fill,minmax(180px,1fr))',gap:8}}>
                    {(byAgent[selectedAgent]||[]).map(skillName => {
                      const domainColor = DOMAIN_COLORS[AGENT_DOMAIN[selectedAgent]]||acc
                      const isSelected = selectedSkill === skillName
                      return (
                        <div key={skillName} onClick={() => loadSkillContent(selectedAgent, skillName)}
                          style={{background:`linear-gradient(135deg,${domainColor}4D 0%,${domainColor}26 100%)`,border:`1.5px solid ${isSelected?domainColor:domainColor+'50'}`,borderRadius:12,padding:'14px 12px',cursor:'pointer',position:'relative',overflow:'hidden',transition:'all .15s',textAlign:'center'}}>
                          <div style={{position:'absolute',top:0,left:0,right:0,height:isSelected?3:2,background:`linear-gradient(90deg,${domainColor}00,${domainColor}${isSelected?'90':'60'},${domainColor}00)`}}/>
                          <div style={{width:36,height:36,borderRadius:9,background:`${domainColor}20`,border:`1px solid ${domainColor}40`,display:'flex',alignItems:'center',justifyContent:'center',margin:'0 auto 8px'}}>
                            <i className="ti ti-file-text" style={{fontSize:18,color:domainColor}}/>
                          </div>
                          <div style={{fontSize:10,fontWeight:700,color:t.text,fontFamily:'monospace',lineHeight:1.3}}>{skillName}</div>
                        </div>
                      )
                    })}
                  </div>
                </div>
              )}
            </div>

            {/* Rechts — skill detail */}
            {selectedSkill && (
              <div style={{width:260,flexShrink:0,background:t.bgSecondary,border:`1px solid ${t.border}`,borderRadius:10,padding:'12px 14px',overflowY:'auto',display:'flex',flexDirection:'column',gap:8}}>
                <div style={{display:'flex',alignItems:'center',justifyContent:'space-between'}}>
                  <div style={{fontSize:11,fontWeight:700,color:t.text,fontFamily:'monospace'}}>{selectedSkill}</div>
                  <button onClick={() => {setSelectedSkill(null); setSkillContent(null)}}
                    style={{background:'transparent',border:'none',color:t.textMuted,cursor:'pointer',fontSize:14}}>
                    <i className="ti ti-x"/>
                  </button>
                </div>
                {skillContent ? (
                  <div style={{fontSize:9,color:t.textMuted,lineHeight:1.7,whiteSpace:'pre-wrap',fontFamily:'monospace',overflow:'auto'}}>
                    {skillContent}
                  </div>
                ) : (
                  <div style={{color:t.textMuted,fontSize:11}}>Laden...</div>
                )}
              </div>
            )}
          </div>
        )}

        {/* TAB 3 — SKILL BIBLIOTHEEK */}
        {tab === 'library' && (
          <div style={{display:'flex',flexDirection:'column',gap:10}}>
            <div style={{fontSize:11,color:t.textMuted,marginBottom:4}}>
              <strong style={{color:acc}}>{sortedLibrary.length}</strong> unieke skills in het systeem
            </div>
            <div style={{display:'grid',gridTemplateColumns:'repeat(auto-fill,minmax(240px,1fr))',gap:8}}>
              {sortedLibrary.map(([skillName, agents]) => (
                <div key={skillName} style={{background:`linear-gradient(135deg,${acc}4D 0%,${acc}1A 100%)`,border:`1.5px solid ${acc}25`,borderRadius:10,padding:'11px 13px',position:'relative',overflow:'hidden'}}>
                  <div style={{position:'absolute',top:0,left:0,right:0,height:2,background:`linear-gradient(90deg,${acc}00,${acc}60,${acc}00)`}}/>
                  <div style={{display:'flex',alignItems:'center',gap:6,marginBottom:8}}>
                    <i className="ti ti-file-text" style={{fontSize:14,color:acc}}/>
                    <span style={{fontSize:11,fontWeight:700,color:t.text,fontFamily:'monospace'}}>{skillName}</span>
                    <span style={{marginLeft:'auto',fontSize:9,color:acc,background:`${acc}15`,borderRadius:4,padding:'1px 6px',fontWeight:700}}>{agents.length} agents</span>
                  </div>
                  <div style={{display:'flex',gap:3,flexWrap:'wrap'}}>
                    {agents.map(agent => {
                      const domainColor = DOMAIN_COLORS[AGENT_DOMAIN[agent]] || acc
                      return (
                        <span key={agent} style={{fontSize:8,color:domainColor,background:'rgba(0,0,0,0.50)',border:`1px solid ${domainColor}40`,borderRadius:4,padding:'2px 6px',display:'flex',alignItems:'center',gap:3}}>
                          <span>{AGENT_EMOJI[agent]||'🤖'}</span>{agent}
                        </span>
                      )
                    })}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
