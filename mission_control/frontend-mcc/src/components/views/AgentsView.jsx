import React, { useState, useEffect } from 'react'

const AGENTS = [
  { id:'nova',     name:'Nova',     role:'Gateway',        layer:'gateway',      domain:'core',    color:'#c9a84c' },
  { id:'flux',     name:'Flux',     role:'Orchestrator',   layer:'orchestrator', domain:'core',    color:'#c9a84c' },
  { id:'cortexia', name:'Cortexia', role:'Omni Lead',      layer:'lead',         domain:'helix',   color:'#38bdf8' },
  { id:'nero',     name:'Nero',     role:'Security',       layer:'sentinel',     domain:'helix',   color:'#38bdf8' },
  { id:'forge',    name:'Forge',    role:'Engineering',    layer:'sentinel',     domain:'helix',   color:'#38bdf8' },
  { id:'axon',     name:'Axon',     role:'Automation',     layer:'sentinel',     domain:'helix',   color:'#38bdf8' },
  { id:'ventura',  name:'Ventura',  role:'Infrastructure', layer:'sentinel',     domain:'helix',   color:'#38bdf8' },
  { id:'clio',     name:'Clio',     role:'Documentation',  layer:'sentinel',     domain:'helix',   color:'#38bdf8' },
  { id:'finoria',  name:'Finoria',  role:'Omni Lead',      layer:'lead',         domain:'finix',   color:'#f472b6' },
  { id:'kairo',    name:'Kairo',    role:'Treasury',       layer:'sentinel',     domain:'finix',   color:'#f472b6' },
  { id:'kenzo',    name:'Kenzo',    role:'Controls',       layer:'sentinel',     domain:'finix',   color:'#f472b6' },
  { id:'odis',     name:'Odis',     role:'Audit',          layer:'sentinel',     domain:'finix',   color:'#f472b6' },
  { id:'vector',   name:'Vector',   role:'Strategy',       layer:'sentinel',     domain:'finix',   color:'#f472b6' },
  { id:'zion',     name:'Zion',     role:'Accounting',     layer:'sentinel',     domain:'finix',   color:'#f472b6' },
  { id:'saelia',   name:'Saelia',   role:'Omni Lead',      layer:'lead',         domain:'matrix',  color:'#34d399' },
  { id:'arix',     name:'Arix',     role:'Research',       layer:'sentinel',     domain:'matrix',  color:'#34d399' },
  { id:'daxio',    name:'Daxio',    role:'Signals',        layer:'sentinel',     domain:'matrix',  color:'#34d399' },
  { id:'enki',     name:'Enki',     role:'Knowledge',      layer:'sentinel',     domain:'matrix',  color:'#34d399' },
  { id:'sora',     name:'Sora',     role:'Synthesis',      layer:'sentinel',     domain:'matrix',  color:'#34d399' },
  { id:'tharos',   name:'Tharos',   role:'Strategic',      layer:'sentinel',     domain:'matrix',  color:'#34d399' },
  { id:'lumeria',  name:'Lumeria',  role:'Omni Lead',      layer:'lead',         domain:'quantix', color:'#a78bfa' },
  { id:'elora',    name:'Elora',    role:'Data Research',  layer:'sentinel',     domain:'quantix', color:'#a78bfa' },
  { id:'kresta',   name:'Kresta',   role:'Analytics',      layer:'sentinel',     domain:'quantix', color:'#a78bfa' },
  { id:'luvia',    name:'Luvia',    role:'Forecasting',    layer:'sentinel',     domain:'quantix', color:'#a78bfa' },
  { id:'nura',     name:'Nura',     role:'Knowledge',      layer:'sentinel',     domain:'quantix', color:'#a78bfa' },
  { id:'vondra',   name:'Vondra',   role:'Signals',        layer:'sentinel',     domain:'quantix', color:'#a78bfa' },
  { id:'fluentia', name:'Fluentia', role:'Omni Lead',      layer:'lead',         domain:'zenix',   color:'#fb923c' },
  { id:'draven',   name:'Draven',   role:'Copy',           layer:'sentinel',     domain:'zenix',   color:'#fb923c' },
  { id:'orizon',   name:'Orizon',   role:'Strategy',       layer:'sentinel',     domain:'zenix',   color:'#fb923c' },
  { id:'solis',    name:'Solis',    role:'Storytelling',   layer:'sentinel',     domain:'zenix',   color:'#fb923c' },
  { id:'unia',     name:'Unia',     role:'Editorial',      layer:'sentinel',     domain:'zenix',   color:'#fb923c' },
  { id:'zena',     name:'Zena',     role:'Localization',   layer:'sentinel',     domain:'zenix',   color:'#fb923c' },
]

const DOMAIN_COLORS = {
  core: '#c9a84c', helix: '#38bdf8', finix: '#f472b6',
  matrix: '#34d399', quantix: '#a78bfa', zenix: '#fb923c'
}

function AgentAvatar({ agent, size = 80 }) {
  const isLead = ['lead','gateway','orchestrator'].includes(agent.layer)
  const initials = agent.name.slice(0,2).toUpperCase()
  const c = agent.color

  return (
    <svg width={size} height={size} viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <radialGradient id={`grad-${agent.id}`} cx="35%" cy="30%" r="70%">
          <stop offset="0%" stopColor={c} stopOpacity="0.9"/>
          <stop offset="100%" stopColor={c} stopOpacity="0.2"/>
        </radialGradient>
        <filter id={`glow-${agent.id}`}>
          <feGaussianBlur stdDeviation="3" result="blur"/>
          <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
        </filter>
      </defs>
      {/* Outer ring */}
      <circle cx="40" cy="40" r="38" fill="none" stroke={c} strokeWidth={isLead?2:1} strokeOpacity="0.4"/>
      {/* Inner glow ring */}
      {isLead && <circle cx="40" cy="40" r="34" fill="none" stroke={c} strokeWidth="1" strokeOpacity="0.2"/>}
      {/* Main circle */}
      <circle cx="40" cy="40" r="30" fill={`url(#grad-${agent.id})`} filter={`url(#glow-${agent.id})`}/>
      {/* Initials */}
      <text x="40" y="46" textAnchor="middle" fontSize={isLead?16:14} fontWeight="700"
        fill="#ffffff" fontFamily="monospace" letterSpacing="1">{initials}</text>
      {/* Online dot */}
      <circle cx="62" cy="18" r="5" fill="#22c55e"/>
      <circle cx="62" cy="18" r="5" fill="#22c55e" opacity="0.4">
        <animate attributeName="r" values="5;8;5" dur="2s" repeatCount="indefinite"/>
        <animate attributeName="opacity" values="0.4;0;0.4" dur="2s" repeatCount="indefinite"/>
      </circle>
      {/* Lead indicator */}
      {isLead && (
        <polygon points="40,4 44,12 36,12" fill={c} opacity="0.8"/>
      )}
    </svg>
  )
}

function AgentCard({ agent, theme, isSelected, onClick }) {
  const t = theme?.colors || {}
  const isLead = ['lead','gateway','orchestrator'].includes(agent.layer)
  const c = agent.color

  return (
    <div onClick={onClick} style={{
      background: isSelected ? `${c}12` : (t.bg2||'#111'),
      border: `1px solid ${isSelected ? c+'60' : (t.border||'#333')}`,
      borderLeft: `3px solid ${isLead ? c : c+'50'}`,
      borderRadius: '12px',
      padding: '16px',
      cursor: 'pointer',
      transition: 'all 0.15s',
    }}>
      <div style={{display:'flex',alignItems:'center',gap:'14px'}}>
        <AgentAvatar agent={agent} size={64}/>
        <div style={{flex:1,minWidth:0}}>
          <div style={{display:'flex',alignItems:'center',gap:'8px',marginBottom:'4px',flexWrap:'wrap'}}>
            <span style={{fontSize:'15px',fontWeight:isLead?'700':'600',color:isSelected?c:(t.text||'#e2e8f0')}}>
              {agent.name}
            </span>
            {isLead && (
              <span style={{fontSize:'9px',padding:'2px 6px',borderRadius:'4px',
                background:`${c}25`,color:c,border:`1px solid ${c}40`,fontWeight:'700',textTransform:'uppercase'}}>
                Lead
              </span>
            )}
            <span style={{fontSize:'9px',display:'flex',alignItems:'center',gap:'3px',
              padding:'2px 6px',borderRadius:'8px',background:'#22c55e15',border:'1px solid #22c55e30',color:'#22c55e'}}>
              <span style={{width:'4px',height:'4px',borderRadius:'50%',background:'#22c55e',display:'inline-block'}}/>
              online
            </span>
          </div>
          <div style={{fontSize:'12px',color:c,fontWeight:'500',marginBottom:'6px'}}>{agent.role}</div>
          <div style={{display:'flex',gap:'5px',flexWrap:'wrap'}}>
            <span style={{fontSize:'10px',padding:'2px 7px',borderRadius:'4px',
              background:`${c}15`,color:c,border:`1px solid ${c}30`,textTransform:'uppercase',letterSpacing:'0.05em'}}>
              {agent.domain}
            </span>
            <span style={{fontSize:'10px',padding:'2px 7px',borderRadius:'4px',
              background:`${t.border||'#333'}40`,color:t.textMuted||'#666',textTransform:'uppercase'}}>
              {agent.layer}
            </span>
          </div>
        </div>
      </div>
    </div>
  )
}

export default function AgentsView({ theme }) {
  const t = theme?.colors || {}
  const acc = t.accent || '#c9a84c'
  const [selected, setSelected] = useState(null)
  const [filter, setFilter] = useState('all')
  const [search, setSearch] = useState('')
  const [winW, setWinW] = useState(window.innerWidth)

  useEffect(() => {
    const h = () => setWinW(window.innerWidth)
    window.addEventListener('resize', h)
    return () => window.removeEventListener('resize', h)
  }, [])

  const isMobile = winW < 640
  const isTablet = winW < 1024

  const filtered = AGENTS.filter(a => {
    if (filter !== 'all' && a.domain !== filter) return false
    if (search && !a.name.toLowerCase().includes(search.toLowerCase()) &&
        !a.role.toLowerCase().includes(search.toLowerCase())) return false
    return true
  })

  const domains = ['all','core','helix','finix','matrix','quantix','zenix']

  return (
    <div style={{height:'100%',display:'flex',flexDirection:'column',overflow:'hidden'}}>

      {/* Header */}
      <div style={{padding:'12px 16px',borderBottom:`1px solid ${t.border||'#333'}`,flexShrink:0}}>
        <div style={{display:'flex',alignItems:'center',justifyContent:'space-between',marginBottom:'10px',gap:'8px',flexWrap:'wrap'}}>
          <h2 style={{margin:0,fontSize:'15px',color:t.text||'#e2e8f0',fontWeight:'500',display:'flex',alignItems:'center',gap:'8px'}}>
            <i className="ti ti-robot" style={{color:acc}}/>
            Agents
            <span style={{fontSize:'11px',color:t.textMuted||'#666',fontWeight:'400'}}>
              {filtered.length}/{AGENTS.length}
            </span>
          </h2>
          <input value={search} onChange={e => setSearch(e.target.value)}
            placeholder="Zoeken..."
            style={{padding:'6px 10px',background:t.bg2||'#1a1a1a',border:`1px solid ${t.border||'#333'}`,
              borderRadius:'6px',color:t.text||'#e2e8f0',fontSize:'12px',
              width:isMobile?'100%':'160px',outline:'none'}}/>
        </div>

        {/* Domain filter */}
        <div style={{display:'flex',gap:'5px',flexWrap:'wrap'}}>
          {domains.map(d => (
            <button key={d} onClick={() => setFilter(d)} style={{
              padding:'3px 10px',borderRadius:'6px',fontSize:'10px',cursor:'pointer',
              border:`1px solid ${filter===d?(DOMAIN_COLORS[d]||acc)+'60':(t.border||'#333')}`,
              background:filter===d?`${DOMAIN_COLORS[d]||acc}15`:'transparent',
              color:filter===d?(DOMAIN_COLORS[d]||acc):(t.textMuted||'#666'),
              textTransform:'capitalize',fontWeight:filter===d?'600':'400'
            }}>{d}</button>
          ))}
        </div>
      </div>

      {/* Grid */}
      <div style={{flex:1,overflow:'auto',padding:'12px 16px'}}>
        <div style={{
          display:'grid',
          gridTemplateColumns: isMobile ? '1fr' : isTablet ? 'repeat(2,1fr)' : 'repeat(auto-fill,minmax(300px,1fr))',
          gap:'10px'
        }}>
          {filtered.map(agent => (
            <AgentCard
              key={agent.id}
              agent={agent}
              theme={theme}
              isSelected={selected?.id === agent.id}
              onClick={() => setSelected(selected?.id === agent.id ? null : agent)}
            />
          ))}
        </div>
      </div>
    </div>
  )
}
