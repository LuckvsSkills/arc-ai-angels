import React, { useState } from 'react'

const DC = { core:'#c9a84c', helix:'#38bdf8', finix:'#f472b6', matrix:'#34d399', quantix:'#a78bfa', zenix:'#fb923c' }
const DO = {
  nova:'core', flux:'core',
  cortexia:'helix', forge:'helix', nero:'helix', ventura:'helix', axon:'helix', clio:'helix',
  finoria:'finix', vector:'finix', kairo:'finix', kenzo:'finix', odis:'finix', zion:'finix',
  saelia:'matrix', tharos:'matrix', sora:'matrix', arix:'matrix', enki:'matrix', daxio:'matrix',
  lumeria:'quantix', kresta:'quantix', elora:'quantix', luvia:'quantix', nura:'quantix', vondra:'quantix',
  fluentia:'zenix', draven:'zenix', solis:'zenix', orizon:'zenix', unia:'zenix', zena:'zenix',
}

const TIER_CONFIG = {
  A: { color:'#f59e0b', gradient:'linear-gradient(135deg, #f59e0b22 0%, #f59e0b08 100%)', border:'#f59e0b40', label:'Tier A', model:'gemini-2.5-pro', provider:'Google Direct', price:'€1.15', unit:'/1M tokens', litellm:'arc-flux / arc-high', desc:'Zware taken, complexe redenering, orchestratie', icon:'ti-crown', agents:2 },
  B: { color:'#38bdf8', gradient:'linear-gradient(135deg, #38bdf822 0%, #38bdf808 100%)', border:'#38bdf840', label:'Tier B', model:'gpt-4o-mini',    provider:'OpenAI Direct',  price:'€0.14', unit:'/1M tokens', litellm:'arc-mid / arc-nova', desc:'Balans kwaliteit en kosten, leads en coordinatie', icon:'ti-bolt', agents:15 },
  C: { color:'#34d399', gradient:'linear-gradient(135deg, #34d39922 0%, #34d39908 100%)', border:'#34d39940', label:'Tier C', model:'gemini-flash-lite', provider:'Google Direct', price:'€0.023', unit:'/1M tokens', litellm:'arc-low', desc:'Snel en goedkoop, sentinels en routinetaken', icon:'ti-leaf', agents:15 },
}

const AGENTS = [
  { id:'nova',     name:'Nova',     role:'Gateway',        tier:'B', emoji:'🌟' },
  { id:'flux',     name:'Flux',     role:'Orchestrator',   tier:'A', emoji:'⚡' },
  { id:'cortexia', name:'Cortexia', role:'Omni Lead',      tier:'B', emoji:'💡' },
  { id:'nero',     name:'Nero',     role:'Security',       tier:'B', emoji:'🛡️' },
  { id:'forge',    name:'Forge',    role:'Engineering',    tier:'C', emoji:'⚙️' },
  { id:'axon',     name:'Axon',     role:'Automation',     tier:'C', emoji:'🔧' },
  { id:'ventura',  name:'Ventura',  role:'Infrastructure', tier:'C', emoji:'🏗️' },
  { id:'clio',     name:'Clio',     role:'Documentation',  tier:'C', emoji:'📝' },
  { id:'finoria',  name:'Finoria',  role:'Omni Lead',      tier:'B', emoji:'💰' },
  { id:'kairo',    name:'Kairo',    role:'Finance Ops',    tier:'B', emoji:'📈' },
  { id:'kenzo',    name:'Kenzo',    role:'Modeling',       tier:'C', emoji:'🔢' },
  { id:'odis',     name:'Odis',     role:'Data',           tier:'B', emoji:'💎' },
  { id:'vector',   name:'Vector',   role:'Analytics',      tier:'C', emoji:'📊' },
  { id:'zion',     name:'Zion',     role:'Risk',           tier:'B', emoji:'⚖️' },
  { id:'saelia',   name:'Saelia',   role:'Omni Lead',      tier:'B', emoji:'🧠' },
  { id:'tharos',   name:'Tharos',   role:'Knowledge',      tier:'B', emoji:'📚' },
  { id:'sora',     name:'Sora',     role:'AI',             tier:'B', emoji:'🤖' },
  { id:'arix',     name:'Arix',     role:'Structure',      tier:'C', emoji:'🗂️' },
  { id:'enki',     name:'Enki',     role:'Logic',          tier:'C', emoji:'🔬' },
  { id:'daxio',    name:'Daxio',    role:'Processing',     tier:'C', emoji:'⚡' },
  { id:'lumeria',  name:'Lumeria',  role:'Omni Lead',      tier:'B', emoji:'✨' },
  { id:'kresta',   name:'Kresta',   role:'Strategy',       tier:'C', emoji:'🎯' },
  { id:'elora',    name:'Elora',    role:'Analysis',       tier:'B', emoji:'🔍' },
  { id:'luvia',    name:'Luvia',    role:'Modeling',       tier:'C', emoji:'📐' },
  { id:'nura',     name:'Nura',     role:'Optimization',   tier:'C', emoji:'⚡' },
  { id:'vondra',   name:'Vondra',   role:'Monitoring',     tier:'C', emoji:'👁️' },
  { id:'fluentia', name:'Fluentia', role:'Omni Lead',      tier:'B', emoji:'🌊' },
  { id:'draven',   name:'Draven',   role:'Flow',           tier:'B', emoji:'🌀' },
  { id:'solis',    name:'Solis',    role:'Operations',     tier:'C', emoji:'☀️' },
  { id:'orizon',   name:'Orizon',   role:'Reasoning',      tier:'C', emoji:'🌅' },
  { id:'unia',     name:'Unia',     role:'Polish',         tier:'C', emoji:'💫' },
  { id:'zena',     name:'Zena',     role:'Branding',       tier:'B', emoji:'🎨' },
]

const GROUPS = [
  { id:'core',    label:'Core',       color:'#c9a84c', agents:['nova','flux'] },
  { id:'leads',   label:'Omni Leads', color:'#38bdf8', agents:['cortexia','finoria','saelia','lumeria','fluentia'] },
  { id:'helix',   label:'Helix',      color:'#38bdf8', agents:['nero','forge','axon','ventura','clio'] },
  { id:'finix',   label:'Finix',      color:'#f472b6', agents:['kairo','kenzo','odis','vector','zion'] },
  { id:'matrix',  label:'Matrix',     color:'#34d399', agents:['tharos','sora','arix','enki','daxio'] },
  { id:'quantix', label:'Quantix',    color:'#a78bfa', agents:['kresta','elora','luvia','nura','vondra'] },
  { id:'zenix',   label:'Zenix',      color:'#fb923c', agents:['draven','solis','orizon','unia','zena'] },
]

const DIRECT = [
  { display:'gemini-2.5-flash-lite', provider:'Google',    price:'€0.023/1M', litellm:'arc-low, arc-cron',   tier:'C', note:'Tier C + alle cronjobs' },
  { display:'gpt-4o-mini',           provider:'OpenAI',    price:'€0.14/1M',  litellm:'arc-mid, arc-nova',   tier:'B', note:'Tier B + Nova speciaal' },
  { display:'gemini-2.5-pro',        provider:'Google',    price:'€1.15/1M',  litellm:'arc-flux, arc-high',  tier:'A', note:'Tier A + Flux speciaal' },
  { display:'gemini-2.5-flash',      provider:'Google',    price:'€0.075/1M', litellm:'arc-mid-gemini',      tier:'-', note:'Tier B fallback' },
  { display:'gpt-4o',                provider:'OpenAI',    price:'€2.30/1M',  litellm:'arc-high-openai',     tier:'-', note:'Tier A fallback' },
  { display:'claude-haiku-4-5',      provider:'Anthropic', price:'€0.74/1M',  litellm:'arc-claude',          tier:'-', note:'Geen credits — inactief' },
]

const OR = [
  { display:'google/gemini-2.5-flash',    provider:'Google',    price:'€0.075/1M', litellm:'arc-low-or',             note:'Tier C fallback 1' },
  { display:'deepseek/deepseek-v4-flash', provider:'Deepseek',  price:'€0.09/1M',  litellm:'arc-low-deepseek',       note:'Tier C fallback 2' },
  { display:'openai/gpt-4o-mini',         provider:'OpenAI',    price:'€0.15/1M',  litellm:'arc-mid-or, arc-nova-or',note:'Tier B fallback' },
  { display:'google/gemini-2.5-pro',      provider:'Google',    price:'€1.15/1M',  litellm:'arc-high-or, arc-flux-or',note:'Tier A fallback' },
  { display:'anthropic/claude-haiku-4-5', provider:'Anthropic', price:'€0.74/1M',  litellm:'arc-claude-or',          note:'Claude fallback' },
]

export default function TiersTab({ theme }) {
  const [winW, setWinW] = React.useState(window.innerWidth)
  const isMobile = winW < 768
  React.useEffect(() => {
    const h = () => setWinW(window.innerWidth)
    window.addEventListener('resize', h)
    return () => window.removeEventListener('resize', h)
  }, [])
  const t = theme?.colors || {}
  const acc = t.accent || '#c9a84c'
  const [tab, setTab] = useState('agents')

  return (
    <div style={{ height:'100%', display:'flex', flexDirection:'column', overflow:'hidden' }}>

      {/* SUB TABS */}
      <div style={{ display:'flex', gap:2, padding:'10px 16px 0', borderBottom:`1px solid ${t.border}`, flexShrink:0 }}>
        {[['agents','ti-robot','Agent Tiers'],['providers','ti-server','Providers & Routing']].map(([id,icon,label]) => (
          <button key={id} onClick={() => setTab(id)}
            style={{ padding:'6px 14px', borderRadius:'7px 7px 0 0', border:`1px solid ${tab===id?t.border:'transparent'}`, borderBottom:tab===id?`1px solid ${t.bgSecondary||'#111'}` :'none', background:tab===id?t.bgSecondary:'transparent', color:tab===id?acc:t.textMuted, fontSize:12, fontWeight:tab===id?700:400, cursor:'pointer', display:'flex', alignItems:'center', gap:5, marginBottom:tab===id?-1:0 }}>
            <i className={`ti ${icon}`} style={{fontSize:12}}/>{label}
          </button>
        ))}
      </div>

      <div style={{ flex:1, overflow:'auto', padding:'16px' }}>

        {tab === 'agents' && <>

          {/* INTRO */}
          <div style={{ fontSize:11, color:t.textMuted, marginBottom:16, lineHeight:1.6, maxWidth:700 }}>
            Elk agent heeft een <strong style={{color:t.text}}>Tier A, B of C</strong> baseline model. HARNAS kan automatisch naar een zwaardere of lichtere tier schakelen op basis van taakcomplexiteit. Cronjobs draaien altijd op het goedkoopste model.
          </div>

          {/* TIER KAARTEN — groot en opvallend */}
          <div style={{ display:'grid', gridTemplateColumns:isMobile?'1fr':'repeat(3,1fr)', gap:12, marginBottom:14 }}>
            {['A','B','C'].map(tier => {
              const info = TIER_CONFIG[tier]
              return (
                <div key={tier} style={{ background:info.gradient, border:`1.5px solid ${info.border}`, borderRadius:14, padding:'18px 20px', position:'relative', overflow:'hidden' }}>
                  {/* Achtergrond icon */}
                  <i className={`ti ${info.icon}`} style={{ position:'absolute', right:14, top:12, fontSize:32, color:info.color, opacity:0.12 }}/>
                  <div style={{ display:'flex', alignItems:'center', gap:8, marginBottom:10 }}>
                    <i className={`ti ${info.icon}`} style={{ fontSize:16, color:info.color }}/>
                    <span style={{ fontWeight:900, fontSize:16, color:info.color, letterSpacing:'-0.02em' }}>{info.label}</span>
                    <span style={{ fontSize:10, color:info.color, background:`${info.color}20`, border:`1px solid ${info.border}`, borderRadius:5, padding:'2px 7px', marginLeft:'auto' }}>{info.agents} agents</span>
                  </div>
                  <div style={{ fontSize:15, fontWeight:700, color:t.text, marginBottom:2 }}>{info.model}</div>
                  <div style={{ fontSize:11, color:t.textMuted, marginBottom:10 }}>{info.provider}</div>
                  <div style={{ display:'flex', alignItems:'baseline', gap:3, marginBottom:8 }}>
                    <span style={{ fontSize:22, fontWeight:900, color:info.color, fontFamily:'ui-monospace,monospace' }}>{info.price}</span>
                    <span style={{ fontSize:10, color:info.color, opacity:0.7 }}>{info.unit}</span>
                  </div>
                  <div style={{ fontSize:10, color:t.textMuted, lineHeight:1.5, marginBottom:8 }}>{info.desc}</div>
                  <div style={{ fontSize:9, color:info.color, fontFamily:'monospace', background:`${info.color}10`, borderRadius:5, padding:'4px 8px' }}>{info.litellm}</div>
                </div>
              )
            })}
          </div>

          {/* CRON KAART */}
          <div style={{ background:'linear-gradient(135deg, #ef444422 0%, #ef444408 100%)', border:'1.5px solid #ef444440', borderRadius:12, padding:'12px 16px', marginBottom:20, position:'relative', overflow:'hidden', display:'flex', alignItems:'center', gap:14 }}>
            <i className="ti ti-clock" style={{ position:'absolute', right:12, top:10, fontSize:28, color:'#ef4444', opacity:0.1 }}/>
            <i className="ti ti-clock" style={{ fontSize:18, color:'#ef4444', flexShrink:0 }}/>
            <div style={{ flex:1 }}>
              <div style={{ display:'flex', alignItems:'center', gap:8, marginBottom:4 }}>
                <span style={{ fontWeight:800, fontSize:13, color:'#ef4444' }}>Cron Model</span>
                <span style={{ fontSize:9, color:'#ef4444', background:'#ef444415', border:'1px solid #ef444430', borderRadius:4, padding:'1px 6px' }}>131 jobs · 32 agents</span>
              </div>
              <div style={{ fontSize:11, color:t.text, fontFamily:'monospace', marginBottom:2 }}>gemini-flash-lite</div>
              <div style={{ fontSize:9, color:t.textMuted }}>Google Direct · HARNAS scheduling, memory updates, health checks</div>
            </div>
            <div style={{ textAlign:'right', flexShrink:0 }}>
              <div style={{ fontSize:18, fontWeight:900, color:'#ef4444', fontFamily:'monospace' }}>€0.023</div>
              <div style={{ fontSize:9, color:'#ef4444', opacity:0.7 }}>/1M tokens</div>
              <div style={{ fontSize:9, color:'#ef4444', fontFamily:'monospace', background:'#ef444410', borderRadius:4, padding:'2px 6px', marginTop:4 }}>arc-cron</div>
            </div>
          </div>

          {/* AGENT GROEPEN */}
          {GROUPS.map(group => (
            <div key={group.id} style={{ marginBottom:18 }}>
              <div style={{ display:'flex', alignItems:'center', gap:8, marginBottom:8 }}>
                <div style={{ width:3, height:16, background:group.color, borderRadius:2 }}/>
                <span style={{ fontSize:11, fontWeight:700, color:group.color, textTransform:'uppercase', letterSpacing:'0.1em' }}>{group.label}</span>
                <div style={{ flex:1, height:1, background:`${group.color}20` }}/>
              </div>
              <div style={{ display:'grid', gridTemplateColumns:isMobile?'repeat(auto-fill, minmax(100px, 1fr))':'repeat(auto-fill, minmax(140px, 1fr))', gap:8 }}>
                {AGENTS.filter(a => group.agents.includes(a.id)).map(agent => {
                  const domainColor = DC[DO[agent.id]] || acc
                  const tierInfo = TIER_CONFIG[agent.tier]
                  return (
                    <div key={agent.id} style={{ background:`linear-gradient(135deg, ${domainColor}28 0%, ${domainColor}10 100%)`, border:`1.5px solid ${domainColor}35`, borderRadius:10, padding:'12px 10px', position:'relative', overflow:'hidden', display:'flex', flexDirection:'column', alignItems:'center', textAlign:'center', gap:0 }}>
                      {/* divider top */}
                      <div style={{ position:'absolute', top:0, left:0, right:0, height:3, background:`linear-gradient(90deg, ${domainColor}00, ${domainColor}80, ${domainColor}00)`, borderRadius:'10px 10px 0 0' }}/>
                      {/* emoji */}
                      <span style={{ fontSize:20, marginBottom:6, opacity:0.7 }}>{agent.emoji}</span>
                      {/* naam */}
                      <div style={{ fontSize:12, fontWeight:800, color:t.text, marginBottom:1 }}>{agent.name}</div>
                      {/* rol */}
                      <div style={{ fontSize:9, color:domainColor, fontWeight:700, textTransform:'uppercase', letterSpacing:'0.07em', marginBottom:8 }}>{agent.role}</div>
                      {/* divider */}
                      <div style={{ width:'100%', height:1, background:`${domainColor}30`, marginBottom:8 }}/>
                      {/* tier badge */}
                      <div style={{ fontSize:10, fontWeight:700, color:tierInfo.color, background:`${tierInfo.color}20`, border:`1px solid ${tierInfo.color}40`, borderRadius:5, padding:'2px 8px', marginBottom:4 }}>{tierInfo.label}</div>
                      {/* model */}
                      <div style={{ fontSize:9, color:t.textMuted, fontFamily:'monospace', marginBottom:8 }}>{tierInfo.model}</div>
                      {/* actief */}
                      <div style={{ display:'flex', alignItems:'center', gap:4, background:'#22c55e12', border:'1px solid #22c55e30', borderRadius:20, padding:'2px 8px' }}>
                        <div style={{ width:5, height:5, borderRadius:'50%', background:'#22c55e', boxShadow:'0 0 5px #22c55e80' }}/>
                        <span style={{ fontSize:9, fontWeight:700, color:'#22c55e' }}>actief</span>
                      </div>
                    </div>
                  )
                })}
              </div>
            </div>
          ))}
        </>}

        {tab === 'providers' && <>

          {/* INTRO + ARCHITECTUUR */}
          <div style={{ marginBottom:20 }}>
            <div style={{ fontSize:13, fontWeight:700, color:t.text, marginBottom:6 }}>LiteLLM Routing Architectuur</div>
            <div style={{ fontSize:11, color:t.textMuted, lineHeight:1.7, marginBottom:14, maxWidth:680 }}>
              <strong style={{color:t.text}}>LiteLLM</strong> is een proxy die draait op poort 4000 en fungeert als centrale model router. OpenClaw stuurt alle agent requests naar LiteLLM via <code style={{color:acc, background:`${acc}15`, borderRadius:3, padding:'1px 5px'}}>litellm/arc-*</code> model namen. LiteLLM vertaalt deze naar de juiste provider API — direct of via OpenRouter als fallback.
            </div>

            {/* Architectuur diagram */}
            <div style={{ background:t.bgSecondary, border:`1px solid ${t.border}`, borderRadius:12, padding:'16px 20px', marginBottom:20 }}>
              <div style={{ fontSize:10, fontWeight:700, color:t.textMuted, textTransform:'uppercase', letterSpacing:'0.1em', marginBottom:12 }}>Stroom</div>
              <div style={{ display:'flex', alignItems:'center', gap:0, flexWrap:'wrap', rowGap:8 }}>
                {[
                  { label:'OpenClaw', sub:'poort 50506', color:acc, icon:'ti-heart-rate-monitor' },
                  { arrow:'→', label:'LiteLLM Proxy', sub:'poort 4000', color:'#a78bfa', icon:'ti-git-branch' },
                  { arrow:'→', label:'Provider Direct', sub:'Google / OpenAI', color:'#34d399', icon:'ti-plug' },
                  { arrow:'/ OR', label:'OpenRouter', sub:'fallback', color:'#38bdf8', icon:'ti-route' },
                ].map((item, i) => item.arrow ? (
                  <div key={i} style={{ display:'flex', alignItems:'center', gap:6 }}>
                    <span style={{ fontSize:12, color:t.textMuted, padding:'0 6px' }}>{item.arrow}</span>
                    <div style={{ background:`${item.color}15`, border:`1px solid ${item.color}40`, borderRadius:8, padding:'8px 12px', textAlign:'center', minWidth:110 }}>
                      <i className={`ti ${item.icon}`} style={{ fontSize:14, color:item.color, display:'block', marginBottom:3 }}/>
                      <div style={{ fontSize:11, fontWeight:700, color:item.color }}>{item.label}</div>
                      <div style={{ fontSize:9, color:t.textMuted }}>{item.sub}</div>
                    </div>
                  </div>
                ) : (
                  <div key={i} style={{ background:`${item.color}15`, border:`1px solid ${item.color}40`, borderRadius:8, padding:'8px 12px', textAlign:'center', minWidth:110 }}>
                    <i className={`ti ${item.icon}`} style={{ fontSize:14, color:item.color, display:'block', marginBottom:3 }}/>
                    <div style={{ fontSize:11, fontWeight:700, color:item.color }}>{item.label}</div>
                    <div style={{ fontSize:9, color:t.textMuted }}>{item.sub}</div>
                  </div>
                ))}
              </div>
              <div style={{ fontSize:9, color:t.textMuted, marginTop:10, lineHeight:1.6 }}>
                Agent model namen in OpenClaw: <code style={{color:acc}}>litellm/arc-nova</code>, <code style={{color:acc}}>litellm/arc-mid</code>, <code style={{color:acc}}>litellm/arc-low</code>, etc.
              </div>
            </div>
          </div>

          {/* TWEE KOLOMMEN */}
          <div style={{ display:'grid', gridTemplateColumns:isMobile?'1fr':'1fr 1fr', gap:16 }}>

            {/* DIRECTE PROVIDERS */}
            <div>
              <div style={{ display:'flex', alignItems:'center', gap:8, marginBottom:10 }}>
                <div style={{ width:3, height:16, background:acc, borderRadius:2 }}/>
                <span style={{ fontSize:11, fontWeight:700, color:acc, textTransform:'uppercase', letterSpacing:'0.1em' }}>Directe API</span>
              </div>
              <div style={{ display:'flex', flexDirection:'column', gap:6 }}>
                {DIRECT.map(p => {
                  const tierInfo = TIER_CONFIG[p.tier]
                  return (
                    <div key={p.display} style={{ background:`linear-gradient(135deg, ${p.tier !== '-' && TIER_CONFIG[p.tier] ? TIER_CONFIG[p.tier].color+'18' : acc+'10'} 0%, ${p.tier !== '-' && TIER_CONFIG[p.tier] ? TIER_CONFIG[p.tier].color+'06' : acc+'04'} 100%)`, border:`1.5px solid ${p.tier !== '-' && TIER_CONFIG[p.tier] ? TIER_CONFIG[p.tier].color+'35' : t.border}`, borderRadius:10, padding:'12px 13px', position:'relative', overflow:'hidden' }}>
                      {p.tier !== '-' && TIER_CONFIG[p.tier] && <div style={{ position:'absolute', top:0, left:0, right:0, height:2, background:`linear-gradient(90deg, ${TIER_CONFIG[p.tier].color}00, ${TIER_CONFIG[p.tier].color}80, ${TIER_CONFIG[p.tier].color}00)` }}/>}
                      <div style={{ display:'flex', alignItems:'center', justifyContent:'space-between', marginBottom:6 }}>
                        <span style={{ fontSize:11, fontWeight:700, color:t.text, fontFamily:'monospace' }}>{p.display}</span>
                        {p.tier !== '-' && TIER_CONFIG[p.tier] ?
                          <span style={{ fontSize:9, fontWeight:700, color:TIER_CONFIG[p.tier].color, background:`${TIER_CONFIG[p.tier].color}20`, border:`1px solid ${TIER_CONFIG[p.tier].color}40`, borderRadius:4, padding:'1px 6px' }}>{TIER_CONFIG[p.tier].label}</span>
                          : <span style={{ fontSize:9, color:t.textMuted, background:t.bgSecondary, border:`1px solid ${t.border}`, borderRadius:4, padding:'1px 6px' }}>fallback</span>
                        }
                      </div>
                      <div style={{ display:'flex', justifyContent:'space-between', alignItems:'center', marginBottom:4 }}>
                        <span style={{ fontSize:10, fontWeight:600, color:t.text }}>{p.provider}</span>
                        <span style={{ fontSize:10, fontWeight:700, color: p.tier !== '-' && TIER_CONFIG[p.tier] ? TIER_CONFIG[p.tier].color : t.textMuted, fontFamily:'monospace' }}>{p.price}</span>
                      </div>
                      <div style={{ display:'flex', justifyContent:'space-between', alignItems:'center' }}>
                        <span style={{ fontSize:9, color:t.textMuted, fontStyle:'italic' }}>{p.note}</span>
                        <span style={{ fontSize:9, color:t.textMuted, fontFamily:'monospace', background:`${acc}10`, borderRadius:3, padding:'1px 5px' }}>{p.litellm}</span>
                      </div>
                    </div>
                  )
                })}
              </div>
            </div>

            {/* OPENROUTER FALLBACKS */}
            <div>
              <div style={{ display:'flex', alignItems:'center', gap:8, marginBottom:10 }}>
                <div style={{ width:3, height:16, background:'#a78bfa', borderRadius:2 }}/>
                <span style={{ fontSize:11, fontWeight:700, color:'#a78bfa', textTransform:'uppercase', letterSpacing:'0.1em' }}>OpenRouter Fallbacks</span>
              </div>
              <div style={{ background:`#a78bfa10`, border:`1px solid #a78bfa20`, borderRadius:9, padding:'10px 12px', marginBottom:8, fontSize:10, color:t.textMuted, lineHeight:1.6 }}>
                OpenRouter wordt gebruikt als fallback wanneer een directe provider niet bereikbaar is. Je betaalt OpenRouter per token — kosten zijn vergelijkbaar met direct maar zonder rate limit issues.
              </div>
              <div style={{ display:'flex', flexDirection:'column', gap:6 }}>
                {OR.map(p => (
                  <div key={p.display} style={{ background:'linear-gradient(135deg, #a78bfa18 0%, #a78bfa06 100%)', border:'1.5px solid #a78bfa30', borderRadius:10, padding:'12px 13px', position:'relative', overflow:'hidden' }}>
                    <div style={{ position:'absolute', top:0, left:0, right:0, height:2, background:'linear-gradient(90deg, #a78bfa00, #a78bfa80, #a78bfa00)' }}/>
                    <div style={{ display:'flex', alignItems:'center', justifyContent:'space-between', marginBottom:6 }}>
                      <span style={{ fontSize:11, fontWeight:700, color:t.text, fontFamily:'monospace' }}>{p.display}</span>
                      <span style={{ fontSize:9, color:'#a78bfa', background:'#a78bfa20', border:'1px solid #a78bfa40', borderRadius:4, padding:'1px 6px', fontWeight:700 }}>OR</span>
                    </div>
                    <div style={{ display:'flex', justifyContent:'space-between', alignItems:'center', marginBottom:4 }}>
                      <span style={{ fontSize:10, fontWeight:600, color:t.text }}>{p.provider}</span>
                      <span style={{ fontSize:10, fontWeight:700, color:'#a78bfa', fontFamily:'monospace' }}>{p.price}</span>
                    </div>
                    <div style={{ display:'flex', justifyContent:'space-between', alignItems:'center' }}>
                      <span style={{ fontSize:9, color:t.textMuted, fontStyle:'italic' }}>{p.note}</span>
                      <span style={{ fontSize:9, color:t.textMuted, fontFamily:'monospace', background:'#a78bfa10', borderRadius:3, padding:'1px 5px' }}>{p.litellm}</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>

          </div>
        </>}

      </div>
    </div>
  )
}
