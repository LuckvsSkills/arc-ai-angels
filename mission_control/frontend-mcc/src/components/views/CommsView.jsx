import React, { useState, useEffect, useRef, useCallback } from 'react'

const AGENTS = {
  nova:     { name:'Nova',     role:'Consigliere',  domain:'core',    color:'#c9a84c', voice:'EXAVITQu4vr4xnSDxMaL', emoji:'🌟' },
  flux:     { name:'Flux',     role:'Underboss',    domain:'core',    color:'#c9a84c', voice:'onwK4e9ZLuTAKqWW03F9', emoji:'⚡' },
  cortexia: { name:'Cortexia', role:'Helix Lead',   domain:'helix',   color:'#38bdf8', voice:'XrExE9yKIg1WjnnlVkGX', emoji:'🛠️' },
  finoria:  { name:'Finoria',  role:'Finix Lead',   domain:'finix',   color:'#f472b6', voice:'pFZP5JQG7iQjIQuC4Bku', emoji:'💰' },
  saelia:   { name:'Saelia',   role:'Matrix Lead',  domain:'matrix',  color:'#34d399', voice:'XrExE9yKIg1WjnnlVkGX', emoji:'🧩' },
  lumeria:  { name:'Lumeria',  role:'Quantix Lead', domain:'quantix', color:'#a78bfa', voice:'FGY2WhTYpPnrIDTdsKH5', emoji:'📊' },
  fluentia: { name:'Fluentia', role:'Zenix Lead',   domain:'zenix',   color:'#fb923c', voice:'pFZP5JQG7iQjIQuC4Bku', emoji:'✍️' },
  nero:     { name:'Nero',     role:'Security',     domain:'helix',   color:'#38bdf8', emoji:'🔐' },
  forge:    { name:'Forge',    role:'GitHub',       domain:'helix',   color:'#38bdf8', emoji:'⚒️' },
  axon:     { name:'Axon',     role:'Infra',        domain:'helix',   color:'#38bdf8', emoji:'🔧' },
  ventura:  { name:'Ventura',  role:'Deploy',       domain:'helix',   color:'#38bdf8', emoji:'🚀' },
  clio:     { name:'Clio',     role:'Logging',      domain:'helix',   color:'#38bdf8', emoji:'📋' },
  kairo:    { name:'Kairo',    role:'Trading',      domain:'finix',   color:'#f472b6', emoji:'📈' },
  kenzo:    { name:'Kenzo',    role:'Analytics',    domain:'finix',   color:'#f472b6', emoji:'📉' },
  odis:     { name:'Odis',     role:'DeFi',         domain:'finix',   color:'#f472b6', emoji:'🏦' },
  vector:   { name:'Vector',   role:'Data',         domain:'finix',   color:'#f472b6', emoji:'🔢' },
  zion:     { name:'Zion',     role:'Risk',         domain:'finix',   color:'#f472b6', emoji:'⚖️' },
  tharos:   { name:'Tharos',   role:'Research',     domain:'matrix',  color:'#34d399', emoji:'🔬' },
  sora:     { name:'Sora',     role:'Creative',     domain:'matrix',  color:'#34d399', emoji:'🎨' },
  arix:     { name:'Arix',     role:'Archive',      domain:'matrix',  color:'#34d399', emoji:'🗄️' },
  enki:     { name:'Enki',     role:'Knowledge',    domain:'matrix',  color:'#34d399', emoji:'📚' },
  daxio:    { name:'Daxio',    role:'Data',         domain:'matrix',  color:'#34d399', emoji:'🗃️' },
  kresta:   { name:'Kresta',   role:'Reports',      domain:'quantix', color:'#a78bfa', emoji:'📊' },
  elora:    { name:'Elora',    role:'Forecast',     domain:'quantix', color:'#a78bfa', emoji:'🔮' },
  luvia:    { name:'Luvia',    role:'Metrics',      domain:'quantix', color:'#a78bfa', emoji:'📐' },
  nura:     { name:'Nura',     role:'Insights',     domain:'quantix', color:'#a78bfa', emoji:'💡' },
  vondra:   { name:'Vondra',   role:'Trends',       domain:'quantix', color:'#a78bfa', emoji:'📡' },
  draven:   { name:'Draven',   role:'Copy',         domain:'zenix',   color:'#fb923c', emoji:'✍️' },
  solis:    { name:'Solis',    role:'SEO',          domain:'zenix',   color:'#fb923c', emoji:'🔍' },
  orizon:   { name:'Orizon',   role:'Social',       domain:'zenix',   color:'#fb923c', emoji:'📱' },
  unia:     { name:'Unia',     role:'Email',        domain:'zenix',   color:'#fb923c', emoji:'📧' },
  zena:     { name:'Zena',     role:'Brand',        domain:'zenix',   color:'#fb923c', emoji:'🎯' },
}

const CHATS = [
  { id:'nova',    label:'Nova',         type:'direct', agents:['nova'],    color:'#c9a84c', icon:'🌟', channelType:'direct' },
  { id:'flux',    label:'Flux',         type:'direct', agents:['flux'],    color:'#c9a84c', icon:'⚡', channelType:'direct' },
  { id:'core',    label:'Nova x Flux',  type:'group',  agents:['nova','flux'], color:'#c9a84c', icon:'🤝', lead:'nova', channelType:'group' },
  { id:'leads',   label:'Lead Council', type:'group',  agents:['nova','flux','cortexia','finoria','saelia','lumeria','fluentia'], color:'#c9a84c', icon:'👑', lead:'nova', channelType:'council' },
  { id:'helix',   label:'Helix Team',   type:'team',   agents:['cortexia','nero','forge','axon','ventura','clio'],   color:'#38bdf8', icon:'🛠', lead:'cortexia', channelType:'team' },
  { id:'finix',   label:'Finix Team',   type:'team',   agents:['finoria','kairo','kenzo','odis','vector','zion'],    color:'#f472b6', icon:'💰', lead:'finoria',  channelType:'team' },
  { id:'matrix',  label:'Matrix Team',  type:'team',   agents:['saelia','tharos','sora','arix','enki','daxio'],      color:'#34d399', icon:'🧩', lead:'saelia',   channelType:'team' },
  { id:'quantix', label:'Quantix Team', type:'team',   agents:['lumeria','kresta','elora','luvia','nura','vondra'],  color:'#a78bfa', icon:'📊', lead:'lumeria',  channelType:'team' },
  { id:'zenix',   label:'Zenix Team',   type:'team',   agents:['fluentia','draven','solis','orizon','unia','zena'],  color:'#fb923c', icon:'✍', lead:'fluentia', channelType:'team' },
]

const saveHistory = (chatId, msgs) => {
  try { localStorage.setItem('comms_' + chatId, JSON.stringify(msgs.slice(-100))) } catch {}
}
const loadHistory = (chatId) => {
  try { return JSON.parse(localStorage.getItem('comms_' + chatId) || '[]') } catch { return [] }
}

let elevenKey = null
const getKey = async () => {
  if (elevenKey !== null) return elevenKey
  try {
    const r = await fetch('/api/voice/key')
    const d = await r.json()
    elevenKey = d.key || ''
  } catch { elevenKey = '' }
  return elevenKey
}

const speakText = async (text, agentId) => {
  const agent = AGENTS[agentId]
  if (!agent || !agent.voice) return
  const key = await getKey()
  if (key) {
    try {
      const res = await fetch('https://api.elevenlabs.io/v1/text-to-speech/' + agent.voice, {
        method: 'POST',
        headers: { 'xi-api-key': key, 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: text.slice(0, 500), model_id: 'eleven_multilingual_v2', voice_settings: { stability: 0.5, similarity_boost: 0.75 } })
      })
      if (res.ok) {
        const blob = await res.blob()
        const url = URL.createObjectURL(blob)
        const audio = new Audio(url)
        audio.onended = () => URL.revokeObjectURL(url)
        audio.play()
        return
      }
    } catch {}
  }
  const synth = window.speechSynthesis
  if (synth) { synth.cancel(); const u = new SpeechSynthesisUtterance(text); u.lang = 'nl-NL'; synth.speak(u) }
}

function useVoiceInput(onResult) {
  const [listening, setListening] = useState(false)
  const start = useCallback(() => {
    const SR = window.SpeechRecognition || window.webkitSpeechRecognition
    if (!SR) return
    const rec = new SR()
    rec.lang = 'nl-NL'; rec.continuous = false; rec.interimResults = false
    rec.onstart = () => setListening(true)
    rec.onresult = e => { onResult(e.results[0][0].transcript); setListening(false) }
    rec.onerror = () => setListening(false)
    rec.onend = () => setListening(false)
    rec.start()
  }, [onResult])
  return { listening, start }
}

function Avatar({ agentId, size }) {
  const s = size || 36
  const a = AGENTS[agentId]
  const col = (a && a.color) || '#888'
  return (
    <div style={{ width:s, height:s, borderRadius:s*0.28, flexShrink:0, display:'flex', alignItems:'center', justifyContent:'center', fontSize:s*0.5, background:col+'20', border:'1.5px solid '+col+'40' }}>
      {(a && a.emoji) || '🤖'}
    </div>
  )
}

function Bubble({ msg, t, acc, autoVoice }) {
  const isUser = msg.from === 'user'
  const agent = AGENTS[msg.from]
  const col = isUser ? acc : ((agent && agent.color) || acc)
  const [played, setPlayed] = useState(false)

  useEffect(() => {
    if (!isUser && autoVoice && !played && msg.ok !== false) {
      setPlayed(true)
      speakText(msg.text, msg.from)
    }
  }, [msg.id])

  if (msg.isMeta) return (
    <div style={{ textAlign:'center', margin:'8px 0', fontSize:11, color:t.textMuted }}>
      <span style={{ padding:'3px 12px', borderRadius:10, background:t.bgTertiary, border:'1px solid '+t.border }}>{msg.text}</span>
    </div>
  )

  return (
    <div style={{ display:'flex', gap:8, marginBottom:4, flexDirection:isUser?'row-reverse':'row', alignItems:'flex-end' }}>
      {!isUser && <Avatar agentId={msg.from} size={30} />}
      <div style={{ maxWidth:'70%', display:'flex', flexDirection:'column', alignItems:isUser?'flex-end':'flex-start' }}>
        {!isUser && (
          <div style={{ fontSize:10, fontWeight:700, color:col, marginBottom:3, paddingLeft:4 }}>
            {(agent && agent.name) || msg.from}
          </div>
        )}
        <div style={{ display:'flex', alignItems:'flex-end', gap:5, flexDirection:isUser?'row-reverse':'row' }}>
          <div style={{ padding:'9px 13px', borderRadius:isUser?'16px 4px 16px 16px':'4px 16px 16px 16px', background:isUser?acc+'25':col+'15', border:'1px solid '+(isUser?acc+'30':col+'25'), fontSize:13, color:msg.error?'#ef4444':t.text, lineHeight:1.65, wordBreak:'break-word' }}>
            {msg.text}
          </div>
          {!isUser && agent && agent.voice && (
            <button onClick={() => speakText(msg.text, msg.from)} style={{ width:22, height:22, borderRadius:5, border:'1px solid '+t.border, background:'transparent', color:t.textMuted, cursor:'pointer', display:'flex', alignItems:'center', justifyContent:'center', fontSize:11, flexShrink:0, marginBottom:2 }}>
              <i className="ti ti-volume"/>
            </button>
          )}
        </div>
        <div style={{ fontSize:9, color:t.textMuted, marginTop:3, paddingLeft:isUser?0:4, paddingRight:isUser?4:0 }}>{msg.time}</div>
      </div>
      {isUser && (
        <div style={{ width:30, height:30, borderRadius:8, flexShrink:0, background:acc+'20', border:'1.5px solid '+acc+'40', display:'flex', alignItems:'center', justifyContent:'center', fontSize:15 }}>👤</div>
      )}
    </div>
  )
}

function ChatWindow({ chat, t, acc }) {
  const [messages, setMessages] = useState(() => loadHistory(chat.id))
  const [input, setInput] = useState('')
  const [sending, setSending] = useState(false)
  const [autoVoice, setAutoVoice] = useState(false)
  const [showMembers, setShowMembers] = useState(true)
  const [meetingOpen, setMeetingOpen] = useState(false)
  const [meetingTopic, setMeetingTopic] = useState('')
  const [meetingAgenda, setMeetingAgenda] = useState('')
  const [meetingRunning, setMeetingRunning] = useState(false)
  const bottomRef = useRef(null)
  const inputRef = useRef(null)
  const chatColor = chat.color || acc
  const isMulti = chat.type !== 'direct'
  const primaryAgent = chat.lead || chat.agents[0]
  const primaryInfo = AGENTS[primaryAgent] || {}

  useEffect(() => { bottomRef.current && bottomRef.current.scrollIntoView({ behavior:'smooth' }) }, [messages])
  useEffect(() => { inputRef.current && inputRef.current.focus() }, [chat.id])

  const addMsg = useCallback((msg) => {
    setMessages(prev => {
      const next = [...prev, msg]
      saveHistory(chat.id, next)
      return next
    })
  }, [chat.id])

  const send = useCallback(async (text) => {
    const msg = (text || input).trim()
    if (!msg || sending) return
    setInput('')
    setSending(true)
    const time = () => new Date().toLocaleTimeString('nl', { hour:'2-digit', minute:'2-digit' })
    addMsg({ id:Date.now(), from:'user', text:msg, time:time(), ts:Date.now() })

    if (chat.type === 'direct') {
      try {
        const res = await fetch('/api/agents/' + chat.agents[0] + '/chat', {
          method:'POST', headers:{'Content-Type':'application/json'},
          body: JSON.stringify({ message: msg })
        })
        const d = await res.json()
        const replyText = d.reply||d.response||'...'
        addMsg({ id:Date.now()+1, from:chat.agents[0], text:replyText, time:time(), ok:d.ok, error:!d.ok, ts:Date.now() })
        if (d.ok && autoVoice) speakText(replyText, chat.agents[0])
      } catch {
        addMsg({ id:Date.now()+1, from:chat.agents[0], text:'Verbinding mislukt', time:time(), error:true, ts:Date.now() })
      }
    } else {
      try {
        const historyForApi = messages.slice(-12).map(m => ({
          from: m.from, text: m.text,
          name: m.from === 'user' ? 'Supreme Fea' : ((AGENTS[m.from] && AGENTS[m.from].name) || m.from)
        }))
        const res = await fetch('/api/chat/group', {
          method:'POST', headers:{'Content-Type':'application/json'},
          body: JSON.stringify({
            agents: chat.agents,
            message: msg,
            history: historyForApi,
            channel_label: chat.label,
            channel_type: chat.channelType || chat.type,
            lead: chat.lead,
            sender_name: 'Supreme Fea'
          })
        })
        const d = await res.json()
        for (let i = 0; i < (d.responses||[]).length; i++) {
          const r = d.responses[i]
          if (!r.ok) continue
          await new Promise(resolve => setTimeout(resolve, i === 0 ? 0 : 700 + i * 400))
          addMsg({ id:Date.now()+i+1, from:r.agent_id, text:r.reply, time:time(), ok:true, ts:Date.now() })
          if (autoVoice) await speakText(r.reply, r.agent_id)
        }
        const actions = d.actions || []
        if (actions.length > 0) {
          await new Promise(r => setTimeout(r, 300))
          addMsg({ id:Date.now()+999, from:'user', text:'Actiepunten: ' + actions.join(' | '), time:time(), ts:Date.now(), isMeta:true })
        }
      } catch {
        addMsg({ id:Date.now()+1, from:primaryAgent, text:'Groepsgesprek mislukt', time:time(), error:true, ts:Date.now() })
      }
    }
    setSending(false)
  }, [input, sending, chat, addMsg, messages])

  const { listening, start: startVoice } = useVoiceInput(useCallback((transcript) => {
    send(transcript)
  }, [send]))

  const startMeeting = async () => {
    if (!meetingTopic.trim()) return
    setMeetingRunning(true)
    setMeetingOpen(false)
    const time = () => new Date().toLocaleTimeString('nl', { hour:'2-digit', minute:'2-digit' })
    const agenda = meetingAgenda.trim() ? meetingAgenda.split('\n').filter(Boolean).slice(0,4) : [meetingTopic]
    addMsg({ id:Date.now(), from:'user', text:'Meeting gestart: ' + meetingTopic, time:time(), ts:Date.now(), isMeta:true })
    try {
      const res = await fetch('/api/chat/meeting', {
        method:'POST', headers:{'Content-Type':'application/json'},
        body: JSON.stringify({ agents:chat.agents, topic:meetingTopic, agenda, channel_label:chat.label })
      })
      const d = await res.json()
      let delay = 0
      for (const point of (d.log||[])) {
        await new Promise(r => setTimeout(r, delay))
        addMsg({ id:Date.now()+Math.random(), from:'user', text:'Agendapunt: ' + point.point, time:time(), ts:Date.now(), isMeta:true })
        delay = 400
        for (const r of (point.responses||[])) {
          if (!r.ok) continue
          await new Promise(resolve => setTimeout(resolve, delay))
          addMsg({ id:Date.now()+Math.random(), from:r.agent_id, text:r.reply, time:time(), ok:true, ts:Date.now() })
          delay = 600
        }
      }
      addMsg({ id:Date.now()+999, from:'user', text:'Meeting afgesloten: ' + meetingTopic, time:time(), ts:Date.now(), isMeta:true })
    } catch {
      addMsg({ id:Date.now()+1, from:primaryAgent, text:'Meeting kon niet worden gestart', time:time(), error:true, ts:Date.now() })
    }
    setMeetingRunning(false)
    setMeetingTopic('')
    setMeetingAgenda('')
  }

  return (
    <div style={{ height:'100%', display:'flex', flexDirection:'column', overflow:'hidden' }}>

      {/* Topbar */}
      <div style={{ flexShrink:0, padding:'10px 16px', borderBottom:'1px solid '+t.border, background:t.bgSecondary, display:'flex', alignItems:'center', gap:10 }}>
        <div style={{ fontSize:22 }}>{chat.icon}</div>
        <div style={{ flex:1 }}>
          <div style={{ fontSize:14, fontWeight:800, color:t.text }}>{chat.label}</div>
          <div style={{ fontSize:10, color:t.textMuted }}>{chat.agents.length} {chat.agents.length===1?'agent':'agents'} · {messages.length} berichten</div>
        </div>
        <div style={{ display:'flex', gap:6 }}>
          <button onClick={() => { setAutoVoice(v => !v) }} style={{ height:28, padding:'0 10px', borderRadius:7, border:'1.5px solid '+(autoVoice?chatColor:t.border), background:autoVoice?chatColor:'transparent', color:autoVoice?'#000':t.textMuted, cursor:'pointer', fontSize:11, fontWeight:700, display:'flex', alignItems:'center', gap:5, transition:'all .2s' }}>
            <i className="ti ti-headphones" style={{fontSize:13}}/>{autoVoice?'Voice ON':'Voice'}
          </button>
          {isMulti && (
            <button onClick={() => setShowMembers(v => !v)} style={{ height:28, padding:'0 10px', borderRadius:7, border:'1px solid '+t.border, background:'transparent', color:t.textMuted, cursor:'pointer', fontSize:11, display:'flex', alignItems:'center', gap:5 }}>
              <i className="ti ti-users" style={{fontSize:13}}/>Leden
            </button>
          )}
          {isMulti && (
            <button onClick={() => setMeetingOpen(true)} style={{ height:28, padding:'0 10px', borderRadius:7, border:'1px solid #a78bfa40', background:'#a78bfa10', color:'#a78bfa', cursor:'pointer', fontSize:11, fontWeight:600, display:'flex', alignItems:'center', gap:5 }}>
              <i className="ti ti-speakerphone" style={{fontSize:13}}/>Meeting
            </button>
          )}
          <button onClick={() => { setMessages([]); localStorage.removeItem('comms_'+chat.id) }} style={{ width:28, height:28, borderRadius:7, border:'1px solid '+t.border, background:'transparent', color:t.textMuted, cursor:'pointer', display:'flex', alignItems:'center', justifyContent:'center', fontSize:13 }}>
            <i className="ti ti-trash"/>
          </button>
        </div>
      </div>

      {/* Members strip */}
      {isMulti && showMembers && (
        <div style={{ flexShrink:0, padding:'10px 16px', borderBottom:'1px solid '+t.border, background:chatColor+'05', overflowX:'auto' }}>
          <div style={{ display:'flex', gap:8, minWidth:'max-content' }}>
            {chat.agents.map(id => {
              const a = AGENTS[id]
              const col = (a && a.color) || chatColor
              const isLead = id === chat.lead
              return (
                <div key={id} style={{ display:'flex', flexDirection:'column', alignItems:'center', gap:5, padding:'8px 12px', borderRadius:10, background:col+'08', border:'1px solid '+col+(isLead?'50':'20'), minWidth:75, position:'relative' }}>
                  {isLead && <div style={{ position:'absolute', top:-6, right:-4, fontSize:10 }}>👑</div>}
                  <div style={{ fontSize:24 }}>{(a && a.emoji) || '🤖'}</div>
                  <div style={{ fontSize:11, fontWeight:700, color:t.text }}>{(a && a.name) || id}</div>
                  <div style={{ fontSize:9, color:col, fontWeight:600, textTransform:'uppercase', letterSpacing:'0.06em' }}>{(a && a.role) || ''}</div>
                </div>
              )
            })}
          </div>
        </div>
      )}

      {/* Messages */}
      <div style={{ flex:1, overflowY:'auto', padding:'16px', display:'flex', flexDirection:'column', gap:2, scrollbarWidth:'thin', scrollbarColor:chatColor+' transparent' }}>
        {messages.length === 0 && (
          <div style={{ flex:1, display:'flex', flexDirection:'column', alignItems:'center', justifyContent:'center', color:t.textMuted, gap:12 }}>
            <div style={{ fontSize:52 }}>{chat.icon}</div>
            <div style={{ fontSize:16, fontWeight:700, color:t.text }}>{chat.label}</div>
            <div style={{ fontSize:12, color:t.textMuted, textAlign:'center', maxWidth:280 }}>
              {chat.type==='direct' ? 'Start een gesprek met ' + ((AGENTS[chat.agents[0]] && AGENTS[chat.agents[0]].name) || chat.agents[0]) : 'Stuur een bericht naar ' + chat.label}
            </div>
            <div style={{ display:'flex', gap:8, marginTop:8, flexWrap:'wrap', justifyContent:'center' }}>
              {['Wat is je status?', 'Geef een update', 'Wat loopt er nu?'].map(s => (
                <button key={s} onClick={() => send(s)} style={{ padding:'7px 14px', borderRadius:20, border:'1px solid '+chatColor+'40', background:chatColor+'10', color:chatColor, cursor:'pointer', fontSize:11, fontWeight:600 }}>{s}</button>
              ))}
            </div>
          </div>
        )}
        {messages.map(msg => <Bubble key={msg.id} msg={msg} t={t} acc={acc} autoVoice={autoVoice}/>)}
        {sending && (
          <div style={{ display:'flex', gap:8, alignItems:'flex-end', marginTop:4 }}>
            <Avatar agentId={primaryAgent} size={30}/>
            <div style={{ padding:'10px 14px', borderRadius:'4px 16px 16px 16px', background:chatColor+'12', border:'1px solid '+chatColor+'20' }}>
              <div style={{ display:'flex', gap:4, alignItems:'center' }}>
                {[0,1,2].map(i => <div key={i} style={{ width:7, height:7, borderRadius:'50%', background:chatColor, animation:'mcc-pulse 1.2s '+(i*0.25)+'s infinite' }}/>)}
              </div>
            </div>
          </div>
        )}
        <div ref={bottomRef}/>
      </div>

      {/* Input */}
      <div style={{ flexShrink:0, padding:'10px 14px', borderTop:'1px solid '+t.border, background:t.bgSecondary }}>
        <div style={{ display:'flex', gap:8, alignItems:'flex-end' }}>
          <button onClick={startVoice} title={autoVoice?'Spreek - antwoord wordt automatisch uitgesproken':'Spraak naar tekst'} style={{ width:40, height:40, borderRadius:12, border:'1.5px solid '+(listening?'#ef4444':autoVoice?chatColor+'80':t.border), background:listening?'#ef444415':autoVoice?chatColor+'15':'transparent', color:listening?'#ef4444':autoVoice?chatColor:t.textMuted, cursor:'pointer', display:'flex', alignItems:'center', justifyContent:'center', fontSize:18, flexShrink:0, transition:'all .2s', animation:listening?'mcc-pulse 0.8s infinite':'none', boxShadow:autoVoice&&!listening?'0 0 12px '+chatColor+'60':'none' }}>
            <i className={listening?'ti ti-microphone-off':'ti ti-microphone'}/>
          </button>
          <div style={{ flex:1, background:t.bg, border:'1.5px solid '+(sending?chatColor+'50':t.border), borderRadius:20, padding:'9px 16px', transition:'border-color .2s' }}>
            <textarea
              ref={inputRef}
              value={input}
              onChange={e => setInput(e.target.value)}
              onKeyDown={e => { if (e.key==='Enter' && !e.shiftKey) { e.preventDefault(); send() } }}
              placeholder={'Bericht naar ' + chat.label + '...'}
              rows={1}
              style={{ width:'100%', background:'transparent', border:'none', outline:'none', color:t.text, fontSize:13, fontFamily:'inherit', resize:'none', lineHeight:1.6, maxHeight:100, overflowY:'auto' }}
            />
          </div>
          <button onClick={() => send()} disabled={!input.trim()||sending} style={{ width:40, height:40, borderRadius:12, border:'1.5px solid '+(input.trim()&&!sending?chatColor+'70':t.border), background:input.trim()&&!sending?chatColor:'transparent', color:input.trim()&&!sending?'#000':t.textMuted, cursor:input.trim()&&!sending?'pointer':'default', display:'flex', alignItems:'center', justifyContent:'center', fontSize:17, flexShrink:0, transition:'all .2s' }}>
            <i className="ti ti-send"/>
          </button>
        </div>
      </div>

      {/* Meeting Modal */}
      {meetingOpen && (
        <div style={{ position:'fixed', inset:0, zIndex:400, background:'rgba(0,0,0,0.8)', backdropFilter:'blur(6px)', display:'flex', alignItems:'center', justifyContent:'center', padding:20 }}
          onClick={e => e.target===e.currentTarget && setMeetingOpen(false)}>
          <div style={{ width:'min(560px,95vw)', background:t.bgSecondary, border:'1px solid #a78bfa50', borderRadius:14, overflow:'hidden', boxShadow:'0 24px 80px rgba(0,0,0,0.6)' }}>
            <div style={{ padding:'16px 20px', borderBottom:'1px solid '+t.border, display:'flex', alignItems:'center', gap:10, background:'#a78bfa08' }}>
              <i className="ti ti-speakerphone" style={{ fontSize:20, color:'#a78bfa' }}/>
              <div style={{ flex:1 }}>
                <div style={{ fontSize:15, fontWeight:800, color:t.text }}>Meeting starten</div>
                <div style={{ fontSize:11, color:t.textMuted }}>{chat.label} · {chat.agents.length} agents</div>
              </div>
              <button onClick={() => setMeetingOpen(false)} style={{ width:28, height:28, borderRadius:7, border:'1px solid '+t.border, background:'transparent', color:t.textMuted, cursor:'pointer', display:'flex', alignItems:'center', justifyContent:'center', fontSize:15 }}>
                <i className="ti ti-x"/>
              </button>
            </div>
            <div style={{ padding:'20px' }}>
              <div style={{ marginBottom:14 }}>
                <div style={{ fontSize:11, fontWeight:700, color:t.textMuted, marginBottom:6, letterSpacing:'0.08em', textTransform:'uppercase' }}>Onderwerp</div>
                <input value={meetingTopic} onChange={e=>setMeetingTopic(e.target.value)} placeholder="bv. Q2 strategie, systeem status, prioriteiten..." style={{ width:'100%', padding:'9px 12px', background:t.bgTertiary, border:'1px solid '+t.border, borderRadius:8, color:t.text, fontSize:13, fontFamily:'inherit', outline:'none' }}/>
              </div>
              <div style={{ marginBottom:20 }}>
                <div style={{ fontSize:11, fontWeight:700, color:t.textMuted, marginBottom:6, letterSpacing:'0.08em', textTransform:'uppercase' }}>Agenda punten (max 4 regels)</div>
                <textarea value={meetingAgenda} onChange={e=>setMeetingAgenda(e.target.value)} placeholder="Status update / Knelpunten / Prioriteiten" rows={4} style={{ width:'100%', padding:'9px 12px', background:t.bgTertiary, border:'1px solid '+t.border, borderRadius:8, color:t.text, fontSize:12, fontFamily:'inherit', outline:'none', resize:'none', lineHeight:1.6 }}/>
              </div>
              <div style={{ display:'flex', gap:6, flexWrap:'wrap', marginBottom:20 }}>
                {chat.agents.map(id => {
                  const a = AGENTS[id]
                  const isLead = id === chat.lead
                  return (
                    <div key={id} style={{ display:'flex', alignItems:'center', gap:5, padding:'4px 9px', borderRadius:20, background:((a&&a.color)||'#888')+'12', border:'1px solid '+((a&&a.color)||'#888')+'30' }}>
                      <span style={{fontSize:12}}>{(a&&a.emoji)||'🤖'}</span>
                      <span style={{fontSize:11, fontWeight:isLead?700:400, color:(a&&a.color)||t.text}}>{(a&&a.name)||id}</span>
                      {isLead && <span style={{fontSize:9,color:'#f59e0b'}}>lead</span>}
                    </div>
                  )
                })}
              </div>
              <button onClick={startMeeting} disabled={!meetingTopic.trim()||meetingRunning} style={{ width:'100%', padding:'11px', borderRadius:9, border:'none', background:meetingTopic.trim()?'#a78bfa':'#a78bfa40', color:meetingTopic.trim()?'#fff':'#ffffff60', cursor:meetingTopic.trim()?'pointer':'default', fontSize:13, fontWeight:700 }}>
                {meetingRunning ? 'Meeting loopt...' : 'Start Meeting'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default function CommsView({ theme }) {
  const t = theme?.colors || {}
  const acc = t.accent || '#c9a84c'
  const [activeChat, setActiveChat] = useState('nova')
  const [winW, setWinW] = useState(window.innerWidth)
  const isMobile = winW < 768

  useEffect(() => { const h=()=>setWinW(window.innerWidth); window.addEventListener('resize',h); return()=>window.removeEventListener('resize',h) },[])

  const currentChat = CHATS.find(c => c.id === activeChat) || CHATS[0]

  const SECTIONS = [
    { label:'Direct', chats: CHATS.filter(c => c.type==='direct') },
    { label:'Groepen', chats: CHATS.filter(c => c.type==='group') },
    { label:'Teams', chats: CHATS.filter(c => c.type==='team') },
  ]

  return (
    <div style={{ height:'100%', display:'flex', overflow:'hidden', background:t.bg }}>

      {/* Sidebar */}
      {(!isMobile || !activeChat) && (
        <div style={{ width:isMobile?'100%':230, flexShrink:0, borderRight:isMobile?'none':'1px solid '+t.border, background:t.bgSecondary, display:'flex', flexDirection:'column', overflow:'hidden' }}>
          <div style={{ padding:'14px 16px 10px', borderBottom:'1px solid '+t.border }}>
            <div style={{ fontSize:16, fontWeight:800, color:t.text }}>Comms</div>
            <div style={{ fontSize:10, color:t.textMuted, marginTop:2 }}>ARC AI Agents · {CHATS.length} kanalen</div>
          </div>
          <div style={{ flex:1, overflowY:'auto', scrollbarWidth:'thin' }}>
            {SECTIONS.map(section => (
              <div key={section.label}>
                <div style={{ padding:'10px 16px 4px', fontSize:9, fontWeight:700, letterSpacing:'0.14em', textTransform:'uppercase', color:t.textMuted }}>{section.label}</div>
                {section.chats.map(chat => {
                  const isActive = activeChat === chat.id
                  const col = chat.color || acc
                  const history = loadHistory(chat.id)
                  const lastMsg = history[history.length-1]
                  return (
                    <button key={chat.id} onClick={() => setActiveChat(chat.id)} style={{ display:'flex', alignItems:'center', gap:10, padding:'9px 14px', background:isActive?col+'15':'transparent', border:'none', borderLeft:'3px solid '+(isActive?col:'transparent'), cursor:'pointer', textAlign:'left', width:'100%', transition:'all .12s' }}>
                      <div style={{ width:38, height:38, borderRadius:10, background:col+'18', border:'1.5px solid '+col+'35', display:'flex', alignItems:'center', justifyContent:'center', fontSize:19, flexShrink:0 }}>
                        {chat.icon}
                      </div>
                      <div style={{ flex:1, minWidth:0 }}>
                        <div style={{ fontSize:13, fontWeight:isActive?700:500, color:isActive?col:t.text, overflow:'hidden', textOverflow:'ellipsis', whiteSpace:'nowrap' }}>{chat.label}</div>
                        <div style={{ fontSize:10, color:t.textMuted, overflow:'hidden', textOverflow:'ellipsis', whiteSpace:'nowrap' }}>
                          {lastMsg ? ((lastMsg.from==='user'?'Jij: ':((AGENTS[lastMsg.from]&&AGENTS[lastMsg.from].name)||lastMsg.from)+': ')+lastMsg.text.slice(0,28)+'...') : (chat.agents.length+' agents')}
                        </div>
                      </div>
                      {isActive && <div style={{ width:7, height:7, borderRadius:'50%', background:col, flexShrink:0, boxShadow:'0 0 6px '+col }}/>}
                    </button>
                  )
                })}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Chat */}
      {(!isMobile || activeChat) && (
        <div style={{ flex:1, overflow:'hidden', display:'flex', flexDirection:'column' }}>
          {isMobile && (
            <button onClick={() => setActiveChat(null)} style={{ display:'flex', alignItems:'center', gap:6, padding:'9px 14px', background:t.bgSecondary, border:'none', borderBottom:'1px solid '+t.border, color:t.textMuted, cursor:'pointer', fontSize:12, flexShrink:0 }}>
              <i className="ti ti-arrow-left"/> Terug
            </button>
          )}
          <ChatWindow key={activeChat} chat={currentChat} t={t} acc={acc}/>
        </div>
      )}
    </div>
  )
}
