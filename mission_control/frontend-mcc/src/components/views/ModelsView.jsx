import React, { useState, useEffect } from 'react'

const TIER_INFO = {
  A: { label:'Tier A', color:'#f59e0b', bg:'#f59e0b18', litellm:'arc-flux',  realModel:'gemini/gemini-2.5-pro',   displayModel:'gemini-2.5-pro',   provider:'Google',  price:'€1.15/1M',  desc:'Krachtig — orchestratie, zware taken' },
  B: { label:'Tier B', color:'#38bdf8', bg:'#38bdf818', litellm:'arc-mid',   realModel:'gpt-4o-mini',             displayModel:'gpt-4o-mini',      provider:'OpenAI',  price:'€0.14/1M',  desc:'Balans — leads, coordinatie, chat' },
  C: { label:'Tier C', color:'#34d399', bg:'#34d39918', litellm:'arc-low',   realModel:'gemini/gemini-2.5-flash-lite', displayModel:'gemini-flash-lite', provider:'Google', price:'€0.023/1M', desc:'Snel/goedkoop — sentinels, routinetaken' },
}

const DIRECT_PROVIDERS = [
  { model:'gemini/gemini-2.5-flash-lite', display:'gemini-2.5-flash-lite', provider:'Google',    tier:'C',    price:'€0.023/1M', litellm:'arc-low / arc-cron' },
  { model:'gpt-4o-mini',                  display:'gpt-4o-mini',           provider:'OpenAI',    tier:'B',    price:'€0.14/1M',  litellm:'arc-mid / arc-nova' },
  { model:'gemini/gemini-2.5-pro',        display:'gemini-2.5-pro',        provider:'Google',    tier:'A',    price:'€1.15/1M',  litellm:'arc-flux / arc-high' },
  { model:'gemini/gemini-2.5-flash',      display:'gemini-2.5-flash',      provider:'Google',    tier:'-',    price:'€0.075/1M', litellm:'arc-mid-gemini' },
  { model:'gpt-4o',                       display:'gpt-4o',                provider:'OpenAI',    tier:'A fb', price:'€2.30/1M',  litellm:'arc-high-openai' },
  { model:'claude-haiku-4-5',             display:'claude-haiku-4-5',      provider:'Anthropic', tier:'-',    price:'€0.74/1M',  litellm:'arc-claude' },
]

const OR_PROVIDERS = [
  { model:'openrouter/google/gemini-2.5-flash',      display:'google/gemini-2.5-flash',      provider:'Google via OR',    price:'€0.075/1M', litellm:'arc-low-or' },
  { model:'openrouter/deepseek/deepseek-v4-flash',   display:'deepseek/deepseek-v4-flash',   provider:'Deepseek via OR',  price:'€0.09/1M',  litellm:'arc-low-deepseek' },
  { model:'openrouter/openai/gpt-4o-mini',           display:'openai/gpt-4o-mini',           provider:'OpenAI via OR',    price:'€0.15/1M',  litellm:'arc-mid-or / arc-nova-or' },
  { model:'openrouter/google/gemini-2.5-pro',        display:'google/gemini-2.5-pro',        provider:'Google via OR',    price:'€1.15/1M',  litellm:'arc-high-or / arc-flux-or' },
  { model:'openrouter/anthropic/claude-haiku-4-5',   display:'anthropic/claude-haiku-4-5',   provider:'Anthropic via OR', price:'€0.74/1M',  litellm:'arc-claude-or' },
]

const AGENTS = [
  { id:'nova',     name:'Nova',     role:'Gateway',        domain:'core',    color:'#c9a84c', tier:'B', litellm:'arc-nova',  realModel:'gpt-4o-mini',               fallbacks:['arc-nova-or','arc-mid','arc-low'] },
  { id:'flux',     name:'Flux',     role:'Orchestrator',   domain:'core',    color:'#c9a84c', tier:'A', litellm:'arc-flux',  realModel:'gemini/gemini-2.5-pro',      fallbacks:['arc-flux-or','arc-high','arc-mid'] },
  { id:'cortexia', name:'Cortexia', role:'Omni Lead',      domain:'helix',   color:'#38bdf8', tier:'B', litellm:'arc-mid',   realModel:'gpt-4o-mini',               fallbacks:['arc-mid-or','arc-mid-gemini','arc-low'] },
  { id:'nero',     name:'Nero',     role:'Security',       domain:'helix',   color:'#38bdf8', tier:'B', litellm:'arc-mid',   realModel:'gpt-4o-mini',               fallbacks:['arc-mid-or','arc-mid-gemini','arc-low'] },
  { id:'forge',    name:'Forge',    role:'Engineering',    domain:'helix',   color:'#38bdf8', tier:'C', litellm:'arc-low',   realModel:'gemini/gemini-2.5-flash-lite', fallbacks:['arc-low-or','arc-low-deepseek','gemini-flash'] },
  { id:'axon',     name:'Axon',     role:'Automation',     domain:'helix',   color:'#38bdf8', tier:'C', litellm:'arc-low',   realModel:'gemini/gemini-2.5-flash-lite', fallbacks:['arc-low-or','arc-low-deepseek','gemini-flash'] },
  { id:'ventura',  name:'Ventura',  role:'Infrastructure', domain:'helix',   color:'#38bdf8', tier:'C', litellm:'arc-low',   realModel:'gemini/gemini-2.5-flash-lite', fallbacks:['arc-low-or','arc-low-deepseek','gemini-flash'] },
  { id:'clio',     name:'Clio',     role:'Documentation',  domain:'helix',   color:'#38bdf8', tier:'C', litellm:'arc-low',   realModel:'gemini/gemini-2.5-flash-lite', fallbacks:['arc-low-or','arc-low-deepseek','gemini-flash'] },
  { id:'finoria',  name:'Finoria',  role:'Omni Lead',      domain:'finix',   color:'#f472b6', tier:'B', litellm:'arc-mid',   realModel:'gpt-4o-mini',               fallbacks:['arc-mid-or','arc-mid-gemini','arc-low'] },
  { id:'kairo',    name:'Kairo',    role:'Finance Ops',    domain:'finix',   color:'#f472b6', tier:'B', litellm:'arc-mid',   realModel:'gpt-4o-mini',               fallbacks:['arc-mid-or','arc-mid-gemini','arc-low'] },
  { id:'kenzo',    name:'Kenzo',    role:'Modeling',       domain:'finix',   color:'#f472b6', tier:'C', litellm:'arc-low',   realModel:'gemini/gemini-2.5-flash-lite', fallbacks:['arc-low-or','arc-low-deepseek','gemini-flash'] },
  { id:'odis',     name:'Odis',     role:'Data',           domain:'finix',   color:'#f472b6', tier:'B', litellm:'arc-mid',   realModel:'gpt-4o-mini',               fallbacks:['arc-mid-or','arc-mid-gemini','arc-low'] },
  { id:'vector',   name:'Vector',   role:'Analytics',      domain:'finix',   color:'#f472b6', tier:'C', litellm:'arc-low',   realModel:'gemini/gemini-2.5-flash-lite', fallbacks:['arc-low-or','arc-low-deepseek','gemini-flash'] },
  { id:'zion',     name:'Zion',     role:'Risk',           domain:'finix',   color:'#f472b6', tier:'B', litellm:'arc-mid',   realModel:'gpt-4o-mini',               fallbacks:['arc-mid-or','arc-mid-gemini','arc-low'] },
  { id:'saelia',   name:'Saelia',   role:'Omni Lead',      domain:'matrix',  color:'#34d399', tier:'B', litellm:'arc-mid',   realModel:'gpt-4o-mini',               fallbacks:['arc-mid-or','arc-mid-gemini','arc-low'] },
  { id:'tharos',   name:'Tharos',   role:'Knowledge',      domain:'matrix',  color:'#34d399', tier:'B', litellm:'arc-mid',   realModel:'gpt-4o-mini',               fallbacks:['arc-mid-or','arc-mid-gemini','arc-low'] },
  { id:'sora',     name:'Sora',     role:'AI',             domain:'matrix',  color:'#34d399', tier:'B', litellm:'arc-mid',   realModel:'gpt-4o-mini',               fallbacks:['arc-mid-or','arc-mid-gemini','arc-low'] },
  { id:'arix',     name:'Arix',     role:'Structure',      domain:'matrix',  color:'#34d399', tier:'C', litellm:'arc-low',   realModel:'gemini/gemini-2.5-flash-lite', fallbacks:['arc-low-or','arc-low-deepseek','gemini-flash'] },
  { id:'enki',     name:'Enki',     role:'Logic',          domain:'matrix',  color:'#34d399', tier:'C', litellm:'arc-low',   realModel:'gemini/gemini-2.5-flash-lite', fallbacks:['arc-low-or','arc-low-deepseek','gemini-flash'] },
  { id:'daxio',    name:'Daxio',    role:'Processing',     domain:'matrix',  color:'#34d399', tier:'C', litellm:'arc-low',   realModel:'gemini/gemini-2.5-flash-lite', fallbacks:['arc-low-or','arc-low-deepseek','gemini-flash'] },
  { id:'lumeria',  name:'Lumeria',  role:'Omni Lead',      domain:'quantix', color:'#a78bfa', tier:'B', litellm:'arc-mid',   realModel:'gpt-4o-mini',               fallbacks:['arc-mid-or','arc-mid-gemini','arc-low'] },
  { id:'kresta',   name:'Kresta',   role:'Strategy',       domain:'quantix', color:'#a78bfa', tier:'C', litellm:'arc-low',   realModel:'gemini/gemini-2.5-flash-lite', fallbacks:['arc-low-or','arc-low-deepseek','gemini-flash'] },
  { id:'elora',    name:'Elora',    role:'Analysis',       domain:'quantix', color:'#a78bfa', tier:'B', litellm:'arc-mid',   realModel:'gpt-4o-mini',               fallbacks:['arc-mid-or','arc-mid-gemini','arc-low'] },
  { id:'luvia',    name:'Luvia',    role:'Modeling',       domain:'quantix', color:'#a78bfa', tier:'C', litellm:'arc-low',   realModel:'gemini/gemini-2.5-flash-lite', fallbacks:['arc-low-or','arc-low-deepseek','gemini-flash'] },
  { id:'nura',     name:'Nura',     role:'Optimization',   domain:'quantix', color:'#a78bfa', tier:'C', litellm:'arc-low',   realModel:'gemini/gemini-2.5-flash-lite', fallbacks:['arc-low-or','arc-low-deepseek','gemini-flash'] },
  { id:'vondra',   name:'Vondra',   role:'Monitoring',     domain:'quantix', color:'#a78bfa', tier:'C', litellm:'arc-low',   realModel:'gemini/gemini-2.5-flash-lite', fallbacks:['arc-low-or','arc-low-deepseek','gemini-flash'] },
  { id:'fluentia', name:'Fluentia', role:'Omni Lead',      domain:'zenix',   color:'#fb923c', tier:'B', litellm:'arc-mid',   realModel:'gpt-4o-mini',               fallbacks:['arc-mid-or','arc-mid-gemini','arc-low'] },
  { id:'draven',   name:'Draven',   role:'Flow',           domain:'zenix',   color:'#fb923c', tier:'B', litellm:'arc-mid',   realModel:'gpt-4o-mini',               fallbacks:['arc-mid-or','arc-mid-gemini','arc-low'] },
  { id:'solis',    name:'Solis',    role:'Operations',     domain:'zenix',   color:'#fb923c', tier:'C', litellm:'arc-low',   realModel:'gemini/gemini-2.5-flash-lite', fallbacks:['arc-low-or','arc-low-deepseek','gemini-flash'] },
  { id:'orizon',   name:'Orizon',   role:'Reasoning',      domain:'zenix',   color:'#fb923c', tier:'C', litellm:'arc-low',   realModel:'gemini/gemini-2.5-flash-lite', fallbacks:['arc-low-or','arc-low-deepseek','gemini-flash'] },
  { id:'unia',     name:'Unia',     role:'Polish',         domain:'zenix',   color:'#fb923c', tier:'C', litellm:'arc-low',   realModel:'gemini/gemini-2.5-flash-lite', fallbacks:['arc-low-or','arc-low-deepseek','gemini-flash'] },
  { id:'zena',     name:'Zena',     role:'Branding',       domain:'zenix',   color:'#fb923c', tier:'B', litellm:'arc-mid',   realModel:'gpt-4o-mini',               fallbacks:['arc-mid-or','arc-mid-gemini','arc-low'] },
]

export default function ModelsView({ theme: t }) {
  const [health, setHealth] = useState({})
  const [selectedTier, setSelectedTier] = useState('all')
  const [selectedAgent, setSelectedAgent] = useState(null)
  const [tab, setTab] = useState('agents')
  const [loading, setLoading] = useState(true)
  const acc = t?.accent || '#c9a84c'

  useEffect(() => {
    fetch('/api/models/live-status')
      .then(r => r.json())
      .then(d => { setHealth(d.litellm_health || {}); setLoading(false) })
      .catch(() => setLoading(false))
    const iv = setInterval(() => {
      fetch('/api/models/live-status')
        .then(r => r.json())
        .then(d => setHealth(d.litellm_health || {}))
        .catch(() => {})
    }, 30000)
    return () => clearInterval(iv)
  }, [])

  const getStatus = (model) => health[model] || 'unknown'
  const statusColor = (s) => s === 'healthy' ? '#22c55e' : s === 'unhealthy' ? '#ef4444' : '#6b7280'
  const statusIcon = (s) => s === 'healthy' ? 'ti-check' : s === 'unhealthy' ? 'ti-x' : 'ti-minus'

  const filtered = selectedTier === 'all' ? AGENTS : AGENTS.filter(a => a.tier === selectedTier)
  const tierCounts = { A: AGENTS.filter(a=>a.tier==='A').length, B: AGENTS.filter(a=>a.tier==='B').length, C: AGENTS.filter(a=>a.tier==='C').length }

  return (
    <div style={{ height:'100%', overflow:'auto', padding:'16px', display:'flex', flexDirection:'column', gap:14 }}>

      {/* HEADER */}
      <div style={{ display:'flex', alignItems:'center', justifyContent:'space-between' }}>
        <div>
          <div style={{ fontSize:17, fontWeight:700, color:t?.text }}>Model Tier Systeem</div>
          <div style={{ fontSize:11, color:t?.textMuted, marginTop:2 }}>32 agents · LiteLLM routing · live status</div>
        </div>
        <div style={{ display:'flex', alignItems:'center', gap:6 }}>
          {loading && <span style={{ fontSize:10, color:t?.textMuted }}>laden...</span>}
          <div style={{ width:6, height:6, borderRadius:'50%', background: Object.values(health).length > 0 ? '#22c55e' : '#6b7280', boxShadow: Object.values(health).length > 0 ? '0 0 6px #22c55e' : 'none' }}/>
          <span style={{ fontSize:10, color:t?.textMuted }}>LiteLLM</span>
        </div>
      </div>

      {/* TABS */}
      <div style={{ display:'flex', gap:6, borderBottom:`1px solid ${t?.border}`, paddingBottom:0 }}>
        {[['agents','ti-robot','Agents'],['providers','ti-server','Providers']].map(([id,icon,label]) => (
          <button key={id} onClick={() => setTab(id)} style={{ padding:'6px 14px', borderRadius:'7px 7px 0 0', border:`1px solid ${tab===id ? t?.border : 'transparent'}`, borderBottom: tab===id ? `1px solid ${t?.bgSecondary}` : 'none', background: tab===id ? t?.bgSecondary : 'transparent', color: tab===id ? acc : t?.textMuted, fontSize:12, fontWeight: tab===id ? 700 : 400, cursor:'pointer', display:'flex', alignItems:'center', gap:5, marginBottom:tab===id?-1:0 }}>
            <i className={`ti ${icon}`} style={{ fontSize:13 }}/>{label}
          </button>
        ))}
      </div>

      {tab === 'agents' && <>
        {/* TIER KAARTEN */}
        <div style={{ display:'grid', gridTemplateColumns:'repeat(3,1fr)', gap:10 }}>
          {['A','B','C'].map(tier => {
            const info = TIER_INFO[tier]
            const s = getStatus(info.realModel)
            return (
              <div key={tier} onClick={() => setSelectedTier(selectedTier===tier?'all':tier)}
                style={{ background: selectedTier===tier ? info.bg : t?.bgSecondary, border:`1.5px solid ${selectedTier===tier ? info.color : t?.border}`, borderRadius:10, padding:'12px 14px', cursor:'pointer', transition:'all .2s' }}>
                <div style={{ display:'flex', alignItems:'center', justifyContent:'space-between', marginBottom:5 }}>
                  <span style={{ fontWeight:800, fontSize:14, color:info.color }}>{info.label}</span>
                  <div style={{ display:'flex', alignItems:'center', gap:5 }}>
                    <div style={{ width:7, height:7, borderRadius:'50%', background:statusColor(s), boxShadow:`0 0 5px ${statusColor(s)}` }}/>
                    <span style={{ fontSize:10, color:t?.textMuted, background:t?.bg, borderRadius:4, padding:'1px 6px', border:`1px solid ${t?.border}` }}>{tierCounts[tier]} agents</span>
                  </div>
                </div>
                <div style={{ fontSize:12, fontWeight:600, color:t?.text, marginBottom:1 }}>{info.displayModel}</div>
                <div style={{ fontSize:10, color:t?.textMuted, marginBottom:4 }}>{info.provider} · {info.price} · <span style={{ fontFamily:'monospace' }}>{info.litellm}</span></div>
                <div style={{ fontSize:10, color:t?.textMuted, lineHeight:1.4 }}>{info.desc}</div>
              </div>
            )
          })}
        </div>

        {/* AGENT TABEL */}
        <div style={{ background:t?.bgSecondary, border:`1px solid ${t?.border}`, borderRadius:10, overflow:'hidden', flex:1 }}>
          <div style={{ padding:'8px 14px', borderBottom:`1px solid ${t?.border}`, display:'flex', alignItems:'center', gap:8 }}>
            {['all','A','B','C'].map(f => (
              <button key={f} onClick={() => setSelectedTier(f)}
                style={{ padding:'3px 10px', borderRadius:6, border:`1px solid ${selectedTier===f?acc:t?.border}`, background:selectedTier===f?acc+'20':'transparent', color:selectedTier===f?acc:t?.textMuted, fontSize:11, cursor:'pointer', fontWeight:selectedTier===f?700:400 }}>
                {f==='all'?'Alle':`Tier ${f}`}
              </button>
            ))}
            <span style={{ marginLeft:'auto', fontSize:11, color:t?.textMuted }}>{filtered.length} agents</span>
          </div>

          {/* Header */}
          <div style={{ display:'grid', gridTemplateColumns:'28px 110px 80px 65px 140px 1fr', padding:'7px 14px', borderBottom:`1px solid ${t?.border}`, background:t?.bg }}>
            {['','Agent','Domein','Tier','Model (echt)','Fallbacks'].map((h,i) => (
              <div key={i} style={{ fontSize:10, color:t?.textMuted, fontWeight:700, textTransform:'uppercase', letterSpacing:'0.07em' }}>{h}</div>
            ))}
          </div>

          <div style={{ maxHeight:320, overflow:'auto' }}>
            {filtered.map(agent => {
              const info = TIER_INFO[agent.tier]
              const s = getStatus(agent.realModel)
              const isSelected = selectedAgent === agent.id
              return (
                <div key={agent.id} onClick={() => setSelectedAgent(isSelected?null:agent.id)}
                  style={{ display:'grid', gridTemplateColumns:'28px 110px 80px 65px 140px 1fr', padding:'8px 14px', borderBottom:`1px solid ${t?.border}20`, cursor:'pointer', background:isSelected?agent.color+'10':'transparent', transition:'background .15s' }}>
                  <div style={{ display:'flex', alignItems:'center' }}>
                    <div style={{ width:7, height:7, borderRadius:'50%', background:statusColor(s), boxShadow:`0 0 5px ${statusColor(s)}60` }}/>
                  </div>
                  <div>
                    <div style={{ fontSize:12, fontWeight:600, color:t?.text }}>{agent.name}</div>
                    <div style={{ fontSize:10, color:t?.textMuted }}>{agent.role}</div>
                  </div>
                  <div style={{ display:'flex', alignItems:'center' }}>
                    <span style={{ fontSize:10, color:agent.color, background:agent.color+'15', borderRadius:4, padding:'2px 5px' }}>{agent.domain}</span>
                  </div>
                  <div style={{ display:'flex', alignItems:'center' }}>
                    <span style={{ fontSize:11, fontWeight:700, color:info.color, background:info.bg, border:`1px solid ${info.color}40`, borderRadius:5, padding:'2px 7px' }}>{info.label}</span>
                  </div>
                  <div style={{ display:'flex', alignItems:'center' }}>
                    <div>
                      <div style={{ fontSize:10, color:t?.text, fontFamily:'monospace' }}>{agent.realModel.replace('gemini/','').replace('gpt-','gpt-')}</div>
                      <div style={{ fontSize:9, color:t?.textMuted, fontFamily:'monospace' }}>{agent.litellm}</div>
                    </div>
                  </div>
                  <div style={{ display:'flex', alignItems:'center', gap:3, flexWrap:'wrap' }}>
                    {agent.fallbacks.map((fb,i) => (
                      <span key={i} style={{ fontSize:9, color:t?.textMuted, background:t?.bg, border:`1px solid ${t?.border}`, borderRadius:3, padding:'1px 4px', fontFamily:'monospace' }}>{fb}</span>
                    ))}
                  </div>
                </div>
              )
            })}
          </div>
        </div>

        {/* DETAIL PANEL */}
        {selectedAgent && (() => {
          const agent = AGENTS.find(a => a.id === selectedAgent)
          if (!agent) return null
          const info = TIER_INFO[agent.tier]
          const s = getStatus(agent.realModel)
          return (
            <div style={{ background:t?.bgSecondary, border:`1.5px solid ${agent.color}40`, borderRadius:10, padding:14 }}>
              <div style={{ display:'flex', alignItems:'center', gap:8, marginBottom:10 }}>
                <div style={{ width:9, height:9, borderRadius:'50%', background:agent.color, boxShadow:`0 0 7px ${agent.color}` }}/>
                <span style={{ fontWeight:700, fontSize:14, color:t?.text }}>{agent.name}</span>
                <span style={{ fontSize:10, color:agent.color, background:agent.color+'15', borderRadius:4, padding:'2px 7px' }}>{agent.domain}</span>
                <span style={{ fontSize:10, fontWeight:700, color:info.color, background:info.bg, border:`1px solid ${info.color}40`, borderRadius:5, padding:'2px 7px' }}>{info.label}</span>
                <div style={{ display:'flex', alignItems:'center', gap:4, marginLeft:'auto' }}>
                  <i className={`ti ${statusIcon(s)}`} style={{ fontSize:12, color:statusColor(s) }}/>
                  <span style={{ fontSize:10, color:statusColor(s) }}>{s}</span>
                </div>
              </div>
              <div style={{ display:'grid', gridTemplateColumns:'repeat(3,1fr)', gap:10 }}>
                <div style={{ background:t?.bg, borderRadius:7, padding:'10px 12px' }}>
                  <div style={{ fontSize:9, color:t?.textMuted, marginBottom:5, textTransform:'uppercase', letterSpacing:'0.08em' }}>Huidig model</div>
                  <div style={{ fontSize:11, fontWeight:600, color:t?.text }}>{agent.realModel}</div>
                  <div style={{ fontSize:10, color:t?.textMuted, fontFamily:'monospace', marginTop:2 }}>{agent.litellm}</div>
                  <div style={{ fontSize:10, color:info.color, marginTop:4 }}>{info.price}</div>
                </div>
                <div style={{ background:t?.bg, borderRadius:7, padding:'10px 12px' }}>
                  <div style={{ fontSize:9, color:t?.textMuted, marginBottom:5, textTransform:'uppercase', letterSpacing:'0.08em' }}>Tier opties</div>
                  {['A','B','C'].map(tier => (
                    <div key={tier} style={{ fontSize:10, color: tier===agent.tier ? TIER_INFO[tier].color : t?.textMuted, fontWeight: tier===agent.tier?700:400, marginBottom:3, display:'flex', gap:5 }}>
                      <span>{tier===agent.tier?'▶':'  '} Tier {tier}</span>
                      <span style={{ color:t?.textMuted }}>— {TIER_INFO[tier].displayModel}</span>
                      <span style={{ color: tier===agent.tier ? TIER_INFO[tier].color : t?.textMuted }}>{TIER_INFO[tier].price}</span>
                    </div>
                  ))}
                </div>
                <div style={{ background:t?.bg, borderRadius:7, padding:'10px 12px' }}>
                  <div style={{ fontSize:9, color:t?.textMuted, marginBottom:5, textTransform:'uppercase', letterSpacing:'0.08em' }}>Fallback keten</div>
                  {agent.fallbacks.map((fb,i) => (
                    <div key={i} style={{ fontSize:10, color:t?.textMuted, marginBottom:3, fontFamily:'monospace', display:'flex', alignItems:'center', gap:5 }}>
                      <span style={{ color:acc }}>{i+1}.</span> {fb}
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )
        })()}
      </>}

      {tab === 'providers' && <>
        {/* DIRECTE PROVIDERS */}
        <div style={{ background:t?.bgSecondary, border:`1px solid ${t?.border}`, borderRadius:10, overflow:'hidden' }}>
          <div style={{ padding:'10px 14px', borderBottom:`1px solid ${t?.border}`, display:'flex', alignItems:'center', gap:8 }}>
            <i className="ti ti-plug" style={{ fontSize:13, color:acc }}/>
            <span style={{ fontSize:13, fontWeight:600, color:t?.text }}>Directe API Providers</span>
            <span style={{ fontSize:10, color:t?.textMuted, marginLeft:'auto' }}>via LiteLLM direct</span>
          </div>
          {DIRECT_PROVIDERS.map(p => {
            const s = getStatus(p.model)
            return (
              <div key={p.model} style={{ display:'grid', gridTemplateColumns:'28px 1fr 120px 80px 100px', padding:'9px 14px', borderBottom:`1px solid ${t?.border}20`, alignItems:'center' }}>
                <div>
                  <i className={`ti ${statusIcon(s)}`} style={{ fontSize:12, color:statusColor(s) }}/>
                </div>
                <div>
                  <div style={{ fontSize:12, fontWeight:600, color:t?.text, fontFamily:'monospace' }}>{p.display}</div>
                  <div style={{ fontSize:10, color:t?.textMuted }}>{p.provider}</div>
                </div>
                <div style={{ fontSize:10, color:t?.textMuted, fontFamily:'monospace' }}>{p.litellm}</div>
                <div style={{ fontSize:10, color:t?.textMuted }}>{p.price}</div>
                <div>
                  {p.tier !== '-' && <span style={{ fontSize:9, color: TIER_INFO[p.tier]?.color || t?.textMuted, background: TIER_INFO[p.tier]?.bg || 'transparent', border:`1px solid ${TIER_INFO[p.tier]?.color || t?.border}40`, borderRadius:4, padding:'2px 6px', fontWeight:700 }}>Tier {p.tier}</span>}
                </div>
              </div>
            )
          })}
        </div>

        {/* OPENROUTER PROVIDERS */}
        <div style={{ background:t?.bgSecondary, border:`1px solid ${t?.border}`, borderRadius:10, overflow:'hidden' }}>
          <div style={{ padding:'10px 14px', borderBottom:`1px solid ${t?.border}`, display:'flex', alignItems:'center', gap:8 }}>
            <i className="ti ti-route" style={{ fontSize:13, color:'#a78bfa' }}/>
            <span style={{ fontSize:13, fontWeight:600, color:t?.text }}>Via OpenRouter</span>
            <span style={{ fontSize:10, color:t?.textMuted, marginLeft:'auto' }}>fallback routes</span>
          </div>
          {OR_PROVIDERS.map(p => {
            const s = getStatus(p.model)
            return (
              <div key={p.model} style={{ display:'grid', gridTemplateColumns:'28px 1fr 140px 80px', padding:'9px 14px', borderBottom:`1px solid ${t?.border}20`, alignItems:'center' }}>
                <div>
                  <i className={`ti ${statusIcon(s)}`} style={{ fontSize:12, color:statusColor(s) }}/>
                </div>
                <div>
                  <div style={{ fontSize:12, fontWeight:600, color:t?.text, fontFamily:'monospace' }}>{p.display}</div>
                  <div style={{ fontSize:10, color:t?.textMuted }}>{p.provider}</div>
                </div>
                <div style={{ fontSize:10, color:t?.textMuted, fontFamily:'monospace' }}>{p.litellm}</div>
                <div style={{ fontSize:10, color:t?.textMuted }}>{p.price}</div>
              </div>
            )
          })}
        </div>
      </>}

    </div>
  )
}
