import React, { useState, useEffect, useCallback } from 'react'
import {
  AreaChart, Area, BarChart, Bar, RadialBarChart, RadialBar,
  PieChart, Pie, Cell, ResponsiveContainer,
  XAxis, YAxis, Tooltip, Legend
} from 'recharts'

const SC = s => !s ? '#f59e0b'
  : ['reachable','connected','ok','operational','healthy','success'].includes(String(s).toLowerCase())
  ? '#22c55e' : '#ef4444'

const DOMAIN_COLORS = {
  core:'#c9a84c', helix:'#38bdf8', finix:'#f472b6',
  matrix:'#34d399', quantix:'#a78bfa', zenix:'#fb923c',
}

const DOMAIN_AGENTS = {
  core:['nova','flux'],
  helix:['cortexia','forge','nero','ventura','axon','clio'],
  finix:['finoria','vector','kairo','kenzo','odis','zion'],
  matrix:['saelia','tharos','sora','arix','enki','daxio'],
  quantix:['lumeria','kresta','elora','luvia','nura','vondra'],
  zenix:['fluentia','draven','solis','orizon','unia','zena'],
}

function Dot({ color, size=7, pulse=false }) {
  return (
    <span style={{position:'relative',display:'inline-flex',alignItems:'center',justifyContent:'center',width:size,height:size,flexShrink:0}}>
      {pulse && <span style={{position:'absolute',width:size*2.5,height:size*2.5,borderRadius:'50%',background:color,opacity:0.15,animation:'mcc-pulse 2s infinite'}}/>}
      <span style={{width:size,height:size,borderRadius:'50%',background:color,boxShadow:`0 0 ${size}px ${color}80`}}/>
    </span>
  )
}

function SectionLabel({ children, color }) {
  return (
    <div style={{display:'flex',alignItems:'center',gap:8,marginBottom:14}}>
      <div style={{width:3,height:14,background:color,borderRadius:2,flexShrink:0}}/>
      <span style={{fontSize:10,fontWeight:700,letterSpacing:'0.16em',textTransform:'uppercase',color:'var(--db-text)'}}>{children}</span>
    </div>
  )
}

function StatBlock({ label, value, sub, color, warn=false }) {
  return (
    <div style={{background:'var(--db-bg2)',border:`1px solid ${warn?color+'50':'var(--db-border)'}`,borderTop:`3px solid ${color}`,borderRadius:10,padding:'16px 18px',position:'relative'}}>
      {warn && <span style={{position:'absolute',top:10,right:10,width:7,height:7,borderRadius:'50%',background:color,boxShadow:`0 0 8px ${color}`,animation:'mcc-pulse 2s infinite'}}/>}
      <div style={{fontSize:10,fontWeight:700,letterSpacing:'0.12em',textTransform:'uppercase',color:'var(--db-muted)',marginBottom:10}}>{label}</div>
      <div style={{fontSize:28,fontWeight:800,color,lineHeight:1,fontFamily:'ui-monospace,monospace',letterSpacing:'-0.02em'}}>{value}</div>
      {sub && <div style={{fontSize:11,color:'var(--db-muted)',marginTop:7,lineHeight:1.4}}>{sub}</div>}
    </div>
  )
}

function ProgressBar({ value, color, height=5 }) {
  return (
    <div style={{height,background:'var(--db-border)',borderRadius:3,overflow:'hidden'}}>
      <div style={{height:'100%',width:`${Math.min(100,Math.max(0,value))}%`,background:color,borderRadius:3,transition:'width 0.6s ease'}}/>
    </div>
  )
}

const CustomTooltip = ({ active, payload, label, t, acc }) => {
  if (!active || !payload?.length) return null
  return (
    <div style={{background:t?.bgSecondary||'#0d1530',border:`1px solid ${acc||'#00d9ff'}40`,borderRadius:8,padding:'8px 12px',fontSize:11,color:t?.text||'#dce8f8'}}>
      {label && <div style={{fontSize:10,color:t?.textMuted,marginBottom:4}}>{label}</div>}
      {payload.map((p,i) => (
        <div key={i} style={{display:'flex',alignItems:'center',gap:6,marginBottom:2}}>
          <div style={{width:6,height:6,borderRadius:'50%',background:p.color||p.fill}}/>
          <span style={{color:t?.textMuted}}>{p.name}:</span>
          <span style={{fontWeight:700,color:p.color||p.fill}}>{p.value}</span>
        </div>
      ))}
    </div>
  )
}

export default function Dashboard({ theme }) {
  const t = theme?.colors || {}
  const acc = t.accent || '#c9a84c'

  const [data, setData] = useState({
    openclaw: null, systemStatus: null, pulse: [],
    mdAudit: null, todos: [], cronjobs: [],
  })
  const [loading, setLoading] = useState(true)
  const [lastUpdate, setLastUpdate] = useState(null)
  const [winW, setWinW] = useState(window.innerWidth)

  useEffect(() => {
    const h = () => setWinW(window.innerWidth)
    window.addEventListener('resize', h)
    return () => window.removeEventListener('resize', h)
  }, [])

  const isMobile = winW < 700
  const isTablet = winW >= 700 && winW < 1100

  const load = useCallback(async () => {
    const [openclaw, systemStatus, pulseData, mdAudit, todoData, cronData, modelsData, statsData] = await Promise.all([
      fetch('/api/openclaw/status').then(r=>r.json()).catch(()=>null),
      fetch('/api/memory/system-status').then(r=>r.json()).catch(()=>null),
      fetch('/api/memory/pulse').then(r=>r.json()).catch(()=>({agents:[]})),
      fetch('/api/md-audit/overview').then(r=>r.json()).catch(()=>null),
      fetch('/api/todo/items').then(r=>r.json()).catch(()=>({items:[]})),
      fetch('/api/memory/cronjobs').then(r=>r.json()).catch(()=>({cronjobs:[]})),
      fetch('/api/models/overview').then(r=>r.json()).catch(()=>({agents:[]})),
      fetch('/api/stats').then(r=>r.json()).catch(()=>null),
    ])
    setData({
      openclaw, systemStatus,
      pulse: pulseData?.agents || [],
      mdAudit,
      todos: todoData?.items || [],
      cronjobs: cronData?.cronjobs || [],
      models: modelsData?.agents || [],
      stats: statsData,
    })
    setLastUpdate(new Date())
    setLoading(false)
  }, [])

  useEffect(() => { load() }, [load])
  useEffect(() => { const id = setInterval(load, 60000); return () => clearInterval(id) }, [load])

  // ── Afgeleide data ──
  const todos = data.todos
  const models = data.models || []
  const statsData = data.stats
  const p1 = todos.filter(x => x.priority === 1 || x.priority === 'P1')
  const openTodos = todos.filter(x => x.status === 'open')
  const pulseAgents = data.pulse
  const healthyAgents = pulseAgents.filter(a => a.status === 'healthy').length
  const mdAgents = data.mdAudit?.agents || []
  const mdScore = mdAgents.length > 0
    ? Math.round(mdAgents.reduce((s,a) => s+(a.score||0), 0) / mdAgents.length) : 0
  const activeCrons = data.cronjobs.filter(j => j.enabled).length
  const errorCrons = data.cronjobs.filter(j => j.errors > 0).length
  const memHealth = data.systemStatus?.memory_health_percent || 0
  const sysStatus = data.systemStatus?.system_status || '—'
  const totalTasks = pulseAgents.reduce((s,a) => s+(a.tasks_today||0), 0)
  const avgSuccess = pulseAgents.length > 0
    ? Math.round(pulseAgents.reduce((s,a) => s+(a.success_rate||0), 0) / pulseAgents.length) : 0

  // ── Chart data ──

  // Domein bar chart
  const domainChartData = Object.entries(DOMAIN_AGENTS).map(([domain, agents]) => {
    const dp = pulseAgents.filter(a => agents.includes(a.id))
    const healthy = dp.filter(a => a.status==='healthy').length
    const tasks = dp.reduce((s,a) => s+(a.tasks_today||0), 0)
    return { name: domain, healthy, total: agents.length, tasks, color: DOMAIN_COLORS[domain] }
  })

  // MD Audit pie
  const mdPieData = [
    { name: '100%', value: mdAgents.filter(a=>a.score===100).length, color: '#22c55e' },
    { name: '80-99%', value: mdAgents.filter(a=>a.score>=80&&a.score<100).length, color: '#f59e0b' },
    { name: '<80%', value: mdAgents.filter(a=>a.score<80).length, color: '#ef4444' },
  ].filter(d => d.value > 0)

  // Radial health chart
  const radialData = [
    { name: 'Memory', value: memHealth, fill: acc },
    { name: 'MD Score', value: mdScore, fill: '#22c55e' },
    { name: 'Success', value: avgSuccess, fill: '#a78bfa' },
    { name: 'Agents', value: Math.round(healthyAgents/(pulseAgents.length||32)*100), fill: '#38bdf8' },
  ]

  // Todo priority area data (gesimuleerd over tijd)
  const todoAreaData = [
    { dag: 'Ma', p1: 3, p2: 5, p3: 2 },
    { dag: 'Di', p1: 4, p2: 6, p3: 3 },
    { dag: 'Wo', p1: 2, p2: 4, p3: 4 },
    { dag: 'Do', p1: 3, p2: 5, p3: 2 },
    { dag: 'Vr', p1: p1.length, p2: todos.filter(x=>x.priority===2).length, p3: todos.filter(x=>x.priority===3).length },
  ]

  // Agent tasks bar
  const agentTaskData = [...pulseAgents]
    .sort((a,b) => (b.tasks_today||0)-(a.tasks_today||0))
    .slice(0, 10)
    .map(a => ({
      name: a.id.slice(0,6),
      taken: a.tasks_today || 0,
      success: a.success_rate || 0,
    }))

  const cols4 = isMobile ? '1fr' : isTablet ? 'repeat(2,1fr)' : 'repeat(4,1fr)'
  const cols2 = isMobile ? '1fr' : 'repeat(2,1fr)'
  const cols3 = isMobile ? '1fr' : isTablet ? 'repeat(2,1fr)' : 'repeat(3,1fr)'

  const cssVars = {
    '--db-bg':t.bg,'--db-bg2':t.bgSecondary,'--db-bg3':t.bgTertiary,
    '--db-border':t.border,'--db-border-soft':`${t.border}60`,
    '--db-text':t.text,'--db-muted':t.textMuted,'--db-acc':acc,
  }

  if (loading) return (
    <div style={{...cssVars,display:'flex',alignItems:'center',gap:12,padding:40,color:t.textMuted,fontSize:13}}>
      <Dot color={acc} size={10} pulse/> Systeem data laden...
    </div>
  )

  return (
    <div style={{...cssVars,padding:isMobile?14:20,maxWidth:1400,display:'flex',flexDirection:'column',gap:18}}>

      {/* ── HEADER ── */}
      <div style={{display:'flex',alignItems:'center',justifyContent:'space-between',flexWrap:'wrap',gap:10}}>
        <div>
          <div style={{fontSize:isMobile?16:20,fontWeight:800,color:t.text,letterSpacing:'-0.01em'}}>Systeem Dashboard</div>
          <div style={{display:'flex',alignItems:'center',gap:10,marginTop:4,flexWrap:'wrap'}}>
            <Dot color={SC(sysStatus)} size={7} pulse={sysStatus==='OPERATIONAL'}/>
            <span style={{fontSize:12,color:SC(sysStatus),fontWeight:700}}>{sysStatus}</span>
            <span style={{fontSize:11,color:t.textMuted}}>· Silver-Surfer · WSL2</span>
            {lastUpdate && <span style={{fontSize:10,color:t.textMuted}}>· {lastUpdate.toLocaleTimeString('nl')}</span>}
          </div>
        </div>
        <button onClick={load} style={{display:'flex',alignItems:'center',gap:6,padding:'7px 14px',borderRadius:8,border:`1px solid ${t.border}`,background:'transparent',color:t.textMuted,cursor:'pointer',fontSize:11,fontWeight:600}}>
          <i className="ti ti-reload" style={{fontSize:14}}/> Refresh
        </button>
      </div>

      {/* ── STAT KAARTEN ── */}
      <div style={{display:'grid',gridTemplateColumns:cols4,gap:12}}>
        <StatBlock label="Agents Healthy" value={`${healthyAgents}/${pulseAgents.length||32}`} sub={`${totalTasks} taken · ${avgSuccess}% success`} color={healthyAgents>=28?'#22c55e':'#f59e0b'}/>
        <StatBlock label="Gateway" value={data.openclaw?.gateway||'—'} sub={`Telegram: ${data.openclaw?.telegram||'—'}`} color={SC(data.openclaw?.gateway)}/>
        <StatBlock label="MD Audit" value={`${mdScore}%`} sub={`${mdAgents.filter(a=>a.score===100).length}/${mdAgents.length} volledig`} color={mdScore>=90?'#22c55e':mdScore>=70?'#f59e0b':'#ef4444'} warn={mdScore<90}/>
        <StatBlock label="Todo Open" value={openTodos.length} sub={`${p1.length} P1 urgent`} color={p1.length>0?'#ef4444':'#22c55e'} warn={p1.length>0}/>
      </div>

      {/* ── RIJ 2: Radial + Domein bar ── */}
      <div style={{display:'grid',gridTemplateColumns:cols2,gap:14}}>

        {/* Radial health gauges */}
        <div style={{background:t.bgSecondary,border:`1px solid ${t.border}`,borderRadius:12,padding:'18px 20px'}}>
          <SectionLabel color={acc}>Systeem Gezondheid</SectionLabel>
          <div style={{display:'flex',alignItems:'center',gap:16,flexWrap:'wrap'}}>
            <div style={{flex:'0 0 160px',height:160}}>
              <ResponsiveContainer width="100%" height="100%">
                <RadialBarChart cx="50%" cy="50%" innerRadius="25%" outerRadius="95%" data={radialData} startAngle={180} endAngle={-180}>
                  <RadialBar minAngle={5} dataKey="value" cornerRadius={4} background={{fill:t.bgTertiary}}/>
                  <Tooltip content={<CustomTooltip t={t} acc={acc}/>}/>
                </RadialBarChart>
              </ResponsiveContainer>
            </div>
            <div style={{flex:1,display:'flex',flexDirection:'column',gap:10,minWidth:120}}>
              {radialData.map(d => (
                <div key={d.name}>
                  <div style={{display:'flex',justifyContent:'space-between',marginBottom:4}}>
                    <span style={{fontSize:11,color:t.textMuted}}>{d.name}</span>
                    <span style={{fontSize:12,fontWeight:700,color:d.fill,fontFamily:'ui-monospace,monospace'}}>{d.value}%</span>
                  </div>
                  <ProgressBar value={d.value} color={d.fill} height={4}/>
                </div>
              ))}
              <div style={{marginTop:4,fontSize:10,color:t.textMuted}}>
                Cronjobs: <strong style={{color:errorCrons>0?'#f59e0b':'#22c55e'}}>{activeCrons}/{data.cronjobs.length}</strong> actief
                {errorCrons>0 && <span style={{color:'#ef4444'}}> · {errorCrons} errors</span>}
              </div>
            </div>
          </div>
        </div>

        {/* Domein taken bar chart */}
        <div style={{background:t.bgSecondary,border:`1px solid ${t.border}`,borderRadius:12,padding:'18px 20px'}}>
          <SectionLabel color="#38bdf8">Taken per Domein</SectionLabel>
          <div style={{height:160}}>
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={domainChartData} barSize={18} margin={{top:0,right:0,bottom:0,left:-20}}>
                <XAxis dataKey="name" tick={{fill:t.textMuted,fontSize:9}} axisLine={false} tickLine={false}/>
                <YAxis tick={{fill:t.textMuted,fontSize:9}} axisLine={false} tickLine={false}/>
                <Tooltip content={<CustomTooltip t={t} acc={acc}/>}/>
                <Bar dataKey="taken" name="Taken" radius={[3,3,0,0]}>
                  {domainChartData.map((d,i) => <Cell key={i} fill={d.color}/>)}
                </Bar>
                <Bar dataKey="healthy" name="Healthy" radius={[3,3,0,0]} fill={`${acc}40`}/>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* ── RIJ 3: Agent taken + MD pie + Todo area ── */}
      <div style={{display:'grid',gridTemplateColumns:cols3,gap:14}}>

        {/* Top agent activiteit */}
        <div style={{background:t.bgSecondary,border:`1px solid ${t.border}`,borderRadius:12,padding:'18px 20px'}}>
          <SectionLabel color="#a78bfa">Top Agents Vandaag</SectionLabel>
          <div style={{height:200}}>
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={agentTaskData} layout="vertical" barSize={10} margin={{top:0,right:40,bottom:0,left:0}}>
                <XAxis type="number" tick={{fill:t.textMuted,fontSize:8}} axisLine={false} tickLine={false}/>
                <YAxis type="category" dataKey="name" tick={{fill:t.textMuted,fontSize:9}} axisLine={false} tickLine={false} width={42}/>
                <Tooltip content={<CustomTooltip t={t} acc={acc}/>}/>
                <Bar dataKey="taken" name="Taken" fill={acc} radius={[0,3,3,0]}/>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* MD Audit pie */}
        <div style={{background:t.bgSecondary,border:`1px solid ${t.border}`,borderRadius:12,padding:'18px 20px'}}>
          <SectionLabel color="#22c55e">MD Audit Distributie</SectionLabel>
          <div style={{display:'flex',alignItems:'center',gap:12}}>
            <div style={{width:140,height:140,flexShrink:0}}>
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie data={mdPieData} cx="50%" cy="50%" innerRadius={38} outerRadius={60} paddingAngle={3} dataKey="value">
                    {mdPieData.map((d,i) => <Cell key={i} fill={d.color}/>)}
                  </Pie>
                  <Tooltip content={<CustomTooltip t={t} acc={acc}/>}/>
                </PieChart>
              </ResponsiveContainer>
            </div>
            <div style={{flex:1,display:'flex',flexDirection:'column',gap:8}}>
              {mdPieData.map(d => (
                <div key={d.name} style={{display:'flex',alignItems:'center',gap:8}}>
                  <div style={{width:10,height:10,borderRadius:2,background:d.color,flexShrink:0}}/>
                  <span style={{fontSize:11,color:t.textMuted,flex:1}}>{d.name}</span>
                  <span style={{fontSize:13,fontWeight:700,color:d.color,fontFamily:'ui-monospace,monospace'}}>{d.value}</span>
                </div>
              ))}
              <div style={{marginTop:4,paddingTop:8,borderTop:`1px solid ${t.border}`,fontSize:11,color:t.textMuted}}>
                Gem score: <strong style={{color:mdScore>=90?'#22c55e':'#f59e0b'}}>{mdScore}%</strong>
              </div>
            </div>
          </div>
        </div>

        {/* Todo area chart */}
        <div style={{background:t.bgSecondary,border:`1px solid ${t.border}`,borderRadius:12,padding:'18px 20px'}}>
          <SectionLabel color="#f59e0b">Todo Trend (week)</SectionLabel>
          <div style={{height:140,marginBottom:10}}>
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={todoAreaData} margin={{top:0,right:0,bottom:0,left:-20}}>
                <defs>
                  <linearGradient id="gP1" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#ef4444" stopOpacity={0.3}/>
                    <stop offset="95%" stopColor="#ef4444" stopOpacity={0}/>
                  </linearGradient>
                  <linearGradient id="gP2" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#f59e0b" stopOpacity={0.3}/>
                    <stop offset="95%" stopColor="#f59e0b" stopOpacity={0}/>
                  </linearGradient>
                  <linearGradient id="gP3" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#22c55e" stopOpacity={0.3}/>
                    <stop offset="95%" stopColor="#22c55e" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <XAxis dataKey="dag" tick={{fill:t.textMuted,fontSize:9}} axisLine={false} tickLine={false}/>
                <YAxis tick={{fill:t.textMuted,fontSize:9}} axisLine={false} tickLine={false}/>
                <Tooltip content={<CustomTooltip t={t} acc={acc}/>}/>
                <Area type="monotone" dataKey="p1" name="P1" stroke="#ef4444" fill="url(#gP1)" strokeWidth={2}/>
                <Area type="monotone" dataKey="p2" name="P2" stroke="#f59e0b" fill="url(#gP2)" strokeWidth={2}/>
                <Area type="monotone" dataKey="p3" name="P3" stroke="#22c55e" fill="url(#gP3)" strokeWidth={2}/>
              </AreaChart>
            </ResponsiveContainer>
          </div>
          <div style={{display:'flex',gap:12,justifyContent:'center'}}>
            {[['P1','#ef4444'],['P2','#f59e0b'],['P3','#22c55e']].map(([l,c])=>(
              <div key={l} style={{display:'flex',alignItems:'center',gap:4,fontSize:10,color:t.textMuted}}>
                <div style={{width:16,height:2,background:c,borderRadius:1}}/>
                {l}
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* ── RIJ 4: Agent pulse grid + P1 alerts ── */}
      <div style={{display:'grid',gridTemplateColumns:isMobile?'1fr':p1.length>0?'1fr 300px':'1fr',gap:14}}>

        {/* Agent pulse grid */}
        <div style={{background:t.bgSecondary,border:`1px solid ${t.border}`,borderRadius:12,padding:'18px 20px'}}>
          <div style={{display:'flex',alignItems:'center',justifyContent:'space-between',marginBottom:14,flexWrap:'wrap',gap:8}}>
            <SectionLabel color={acc}>Agent Pulse</SectionLabel>
            <div style={{display:'flex',gap:10,fontSize:10,color:t.textMuted}}>
              <span style={{display:'flex',alignItems:'center',gap:4}}><Dot color="#22c55e" size={5}/> Healthy</span>
              <span style={{display:'flex',alignItems:'center',gap:4}}><Dot color="#f59e0b" size={5}/> Actief</span>
              <span style={{display:'flex',alignItems:'center',gap:4}}><Dot color={t.border} size={5}/> Geen data</span>
            </div>
          </div>
          <div style={{display:'flex',flexDirection:'column',gap:8}}>
            {Object.entries(DOMAIN_AGENTS).map(([domain, agents]) => {
              const color = DOMAIN_COLORS[domain]
              return (
                <div key={domain} style={{display:'flex',alignItems:'center',gap:10}}>
                  <div style={{width:54,fontSize:9,fontWeight:700,letterSpacing:'0.1em',textTransform:'uppercase',color,textAlign:'right',flexShrink:0}}>{domain}</div>
                  <div style={{display:'flex',gap:4,flex:1,flexWrap:'wrap'}}>
                    {agents.map(id => {
                      const pa = pulseAgents.find(a => a.id===id)
                      const isHealthy = pa?.status==='healthy'
                      const dotColor = isHealthy ? color : pa ? '#f59e0b' : t.border
                      return (
                        <div key={id} title={`${id} — ${pa?.status||'?'} — ${pa?.tasks_today||0} taken`} style={{
                          display:'flex',flexDirection:'column',alignItems:'center',gap:2,
                          padding:'5px 6px',borderRadius:6,minWidth:40,
                          background:isHealthy?`${color}10`:t.bgTertiary,
                          border:`1px solid ${isHealthy?color+'30':t.border}`,
                        }}>
                          <Dot color={dotColor} size={5} pulse={isHealthy}/>
                          <span style={{fontSize:8,color:isHealthy?color:t.textMuted,fontWeight:isHealthy?700:400}}>{id.slice(0,5)}</span>
                          {pa && <span style={{fontSize:7,color:t.textMuted,fontFamily:'ui-monospace,monospace'}}>{pa.tasks_today||0}t</span>}
                        </div>
                      )
                    })}
                  </div>
                </div>
              )
            })}
          </div>
        </div>

        {/* P1 alerts */}
        {p1.length > 0 && (
          <div style={{background:'rgba(239,68,68,0.05)',border:'1px solid rgba(239,68,68,0.2)',borderRadius:12,padding:'18px 20px'}}>
            <SectionLabel color="#ef4444">P1 — Actie Vereist</SectionLabel>
            <div style={{display:'flex',flexDirection:'column',gap:6}}>
              {p1.map(todo => (
                <div key={todo.id} style={{display:'flex',alignItems:'flex-start',gap:8,padding:'9px 11px',background:'rgba(239,68,68,0.06)',borderRadius:7,border:'1px solid rgba(239,68,68,0.12)'}}>
                  <Dot color="#ef4444" size={6} pulse/>
                  <span style={{fontSize:11,color:t.text,lineHeight:1.5}}>{todo.title}</span>
                </div>
              ))}
            </div>
            <div style={{marginTop:12,paddingTop:10,borderTop:'1px solid rgba(239,68,68,0.15)',fontSize:11,color:'rgba(239,68,68,0.7)'}}>
              {openTodos.length} open · {todos.filter(x=>x.status==='done'||x.status==='closed').length} gedaan
            </div>
          </div>
        )}
      </div>

    </div>
  )
}
