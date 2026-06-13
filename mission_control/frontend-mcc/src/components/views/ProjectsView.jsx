import React, { useState } from 'react'

const PROJECTS = [
  {
    id: 'P1',
    title: 'Website Factory',
    status: 'BEZIG',
    revenue: '€500 – €10.000+/site',
    description: 'Volledig autonome website fabriek. Agents bouwen, deployen en beheren websites op verzoek vanuit GitHub templates.',
    lead: 'Cortexia',
    domain: 'Helix/Tech',
    phases: [
      { name: 'GitHub Templates (10x)', status: '🔴' },
      { name: 'Prijslijst vastleggen', status: '🔴' },
      { name: 'Helix agents configureren', status: '🟡' },
      { name: 'Nova + Flux routing', status: '🔴' },
      { name: 'Test run', status: '🔴' },
      { name: 'Productie', status: '🔴' },
    ],
    metrics: [
      { label: 'Bouwtijd doel', value: '< 2 uur' },
      { label: 'AI kosten doel', value: '< €15/site' },
      { label: 'Kwaliteit doel', value: '> 90/100' },
      { label: 'Sites per dag', value: '3+' },
    ],
    templates: ['landing','portfolio','blog','saas','ecommerce','directory','marketplace','dashboard','community','booking'],
    agents: ['Cortexia','Forge','Axon','Nero','Ventura','Clio'],
  }
]

const FASE_COLOR = { '🔴': '#6b7280', '🟡': '#f59e0b', '🟢': '#10b981' }
const FASE_LABEL = { '🔴': 'Open', '🟡': 'Bezig', '🟢': 'Done' }

export default function ProjectsView({ theme }) {
  const t = theme?.colors || {}
  const [selected, setSelected] = useState('P1')
  const project = PROJECTS.find(p => p.id === selected)

  return (
    <div style={{display:'flex',height:'100%',overflow:'hidden'}}>

      {/* Sidebar */}
      <div style={{width:'260px',minWidth:'260px',borderRight:`1px solid ${t.border||'#333'}`,overflow:'auto',padding:'16px 0'}}>
        <div style={{padding:'0 16px 12px',fontSize:'11px',color:t.textMuted||'#666',textTransform:'uppercase',letterSpacing:'0.08em'}}>
          Actieve projecten
        </div>
        {PROJECTS.map(p => (
          <div key={p.id} onClick={() => setSelected(p.id)}
            style={{padding:'12px 16px',cursor:'pointer',
              borderLeft: selected===p.id ? `3px solid ${t.accent||'#c9a84c'}` : '3px solid transparent',
              background: selected===p.id ? `${t.accent||'#c9a84c'}10` : 'transparent'}}>
            <div style={{display:'flex',alignItems:'center',gap:'8px',marginBottom:'4px'}}>
              <span style={{fontSize:'11px',fontWeight:'600',color:t.accent||'#c9a84c'}}>{p.id}</span>
              <span style={{fontSize:'10px',padding:'2px 6px',borderRadius:'4px',background:'#f59e0b20',color:'#f59e0b',fontWeight:'600'}}>{p.status}</span>
            </div>
            <div style={{fontSize:'13px',color:t.text||'#e2e8f0',fontWeight:'500'}}>{p.title}</div>
            <div style={{fontSize:'11px',color:t.textMuted||'#666',marginTop:'2px'}}>{p.revenue}</div>
          </div>
        ))}
        <div style={{margin:'16px',padding:'12px',background:`${t.accent||'#c9a84c'}10`,borderRadius:'8px',border:`1px solid ${t.accent||'#c9a84c'}30`}}>
          <div style={{fontSize:'10px',color:t.textMuted||'#666',marginBottom:'4px'}}>Year 1 potentieel</div>
          <div style={{fontSize:'16px',fontWeight:'700',color:t.accent||'#c9a84c'}}>€500.000+</div>
        </div>
      </div>

      {/* Detail */}
      {project && (
        <div style={{flex:1,overflow:'auto',padding:'32px'}}>

          <div style={{marginBottom:'24px'}}>
            <div style={{display:'flex',alignItems:'center',gap:'12px',marginBottom:'8px'}}>
              <span style={{fontSize:'13px',fontWeight:'700',color:t.accent||'#c9a84c'}}>{project.id}</span>
              <span style={{fontSize:'12px',padding:'3px 10px',borderRadius:'6px',background:'#f59e0b20',color:'#f59e0b',fontWeight:'600'}}>{project.status}</span>
              <span style={{fontSize:'12px',color:t.textMuted||'#666',padding:'3px 8px',border:`1px solid ${t.border||'#333'}`,borderRadius:'6px'}}>{project.domain}</span>
              <span style={{fontSize:'12px',color:t.textMuted||'#666'}}>Lead: <strong style={{color:t.textSecondary||'#aaa'}}>{project.lead}</strong></span>
            </div>
            <h1 style={{fontSize:'24px',fontWeight:'800',color:t.text||'#e2e8f0',margin:'0 0 8px'}}>{project.title}</h1>
            <p style={{fontSize:'14px',color:t.textSecondary||'#aaa',lineHeight:'1.6',margin:0}}>{project.description}</p>
          </div>

          <div style={{display:'inline-flex',alignItems:'center',gap:'8px',padding:'8px 16px',background:`${t.accent||'#c9a84c'}15`,border:`1px solid ${t.accent||'#c9a84c'}40`,borderRadius:'8px',marginBottom:'28px'}}>
            <span style={{fontSize:'14px',fontWeight:'600',color:t.accent||'#c9a84c'}}>{project.revenue}</span>
          </div>

          {/* Fases */}
          <div style={{marginBottom:'28px'}}>
            <div style={{fontSize:'12px',fontWeight:'600',color:t.textMuted||'#666',textTransform:'uppercase',letterSpacing:'0.08em',marginBottom:'12px'}}>Fasering</div>
            <div style={{display:'flex',flexDirection:'column',gap:'8px'}}>
              {project.phases.map((fase, i) => (
                <div key={i} style={{display:'flex',alignItems:'center',gap:'12px',padding:'10px 14px',background:t.bg2||'#111',borderRadius:'8px',border:`1px solid ${t.border||'#333'}`}}>
                  <div style={{width:'8px',height:'8px',borderRadius:'50%',background:FASE_COLOR[fase.status],flexShrink:0}}/>
                  <span style={{fontSize:'13px',color:t.text||'#e2e8f0',flex:1}}>Fase {i+1} — {fase.name}</span>
                  <span style={{fontSize:'11px',color:FASE_COLOR[fase.status],fontWeight:'600'}}>{FASE_LABEL[fase.status]}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Metrics */}
          <div style={{marginBottom:'28px'}}>
            <div style={{fontSize:'12px',fontWeight:'600',color:t.textMuted||'#666',textTransform:'uppercase',letterSpacing:'0.08em',marginBottom:'12px'}}>Doelstellingen</div>
            <div style={{display:'grid',gridTemplateColumns:'repeat(auto-fill,minmax(160px,1fr))',gap:'12px'}}>
              {project.metrics.map((m, i) => (
                <div key={i} style={{padding:'14px',background:t.bg2||'#111',borderRadius:'8px',border:`1px solid ${t.border||'#333'}`}}>
                  <div style={{fontSize:'11px',color:t.textMuted||'#666',marginBottom:'6px'}}>{m.label}</div>
                  <div style={{fontSize:'18px',fontWeight:'700',color:t.accent||'#c9a84c'}}>{m.value}</div>
                </div>
              ))}
            </div>
          </div>

          {/* Templates */}
          <div style={{marginBottom:'28px'}}>
            <div style={{fontSize:'12px',fontWeight:'600',color:t.textMuted||'#666',textTransform:'uppercase',letterSpacing:'0.08em',marginBottom:'12px'}}>GitHub Templates</div>
            <div style={{display:'flex',flexWrap:'wrap',gap:'6px'}}>
              {project.templates.map(type => (
                <span key={type} style={{fontSize:'11px',padding:'4px 10px',borderRadius:'4px',background:`${t.accent||'#c9a84c'}15`,color:t.accent||'#c9a84c',fontWeight:'500',border:`1px solid ${t.accent||'#c9a84c'}30`}}>
                  template-{type}
                </span>
              ))}
            </div>
          </div>

          {/* Agents */}
          <div>
            <div style={{fontSize:'12px',fontWeight:'600',color:t.textMuted||'#666',textTransform:'uppercase',letterSpacing:'0.08em',marginBottom:'12px'}}>Betrokken agents</div>
            <div style={{display:'flex',flexWrap:'wrap',gap:'6px'}}>
              {project.agents.map(agent => (
                <span key={agent} style={{fontSize:'11px',padding:'4px 10px',borderRadius:'4px',background:`${t.border||'#333'}40`,color:t.textSecondary||'#aaa',fontWeight:'500',border:`1px solid ${t.border||'#333'}`}}>
                  {agent}
                </span>
              ))}
            </div>
          </div>

        </div>
      )}
    </div>
  )
}
