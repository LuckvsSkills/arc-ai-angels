import React, { useState, useEffect, useRef } from 'react'

const NAV_ITEMS = [
  { id: 'agents',    label: 'Agents',    icon: 'ti-robot' },
  { id: 'dashboard', label: 'Dashboard', icon: 'ti-layout-dashboard' },
  { id: 'openclaw',  label: 'OpenClaw',  icon: 'ti-heart-rate-monitor' },
  { id: 'kernel',    label: 'Kernel',    icon: 'ti-cpu' },
  { id: 'projects',  label: 'Projects',  icon: 'ti-briefcase' },
  { id: 'canon',     label: 'Codex',     icon: 'ti-book-2' },
  { id: 'diagrams',  label: 'Diagrams',  icon: 'ti-schema' },
  { id: 'comms',     label: 'Comms',     icon: 'ti-message' },
  { id: 'terminal',  label: 'Terminal',  icon: 'ti-terminal' },
]

export default function TopNav({ view, setView, theme, onOpenSettings, agentCount = 32 }) {
  const [time, setTime] = useState({ h:'00', m:'00', s:'00', date:'' })
  const [pulse, setPulse] = useState(false)
  const [width, setWidth] = useState(window.innerWidth)
  const [menuOpen, setMenuOpen] = useState(false)
  const [canScrollLeft, setCanScrollLeft] = useState(false)
  const [canScrollRight, setCanScrollRight] = useState(false)
  const menuRef = useRef(null)
  const navScrollRef = useRef(null)
  const t = theme.colors
  const acc = t.accent

  // Breakpoints — gebaseerd op effectieve breedte
  // < 520px  → alleen hamburger (mobiel)
  // 520-780px → logo icon + hamburger (klein tablet)
  // 780px+   → scrollbare tabs
  // 1200px+  → alles zichtbaar zonder scrollen (grote desktop)
  const isHamburger = width < 780
  const isMini = width < 520
  const isDesktop = width >= 1200

  useEffect(() => {
    const tick = () => {
      const n = new Date()
      setTime({
        h: String(n.getHours()).padStart(2,'0'),
        m: String(n.getMinutes()).padStart(2,'0'),
        s: String(n.getSeconds()).padStart(2,'0'),
        date: n.toLocaleDateString('nl',{weekday:'short',day:'numeric',month:'short'}),
      })
      setPulse(p => !p)
    }
    tick()
    const id = setInterval(tick, 1000)
    return () => clearInterval(id)
  }, [])

  useEffect(() => {
    const h = () => setWidth(window.innerWidth)
    window.addEventListener('resize', h)
    return () => window.removeEventListener('resize', h)
  }, [])

  useEffect(() => {
    const h = (e) => {
      if (menuRef.current && !menuRef.current.contains(e.target)) setMenuOpen(false)
    }
    document.addEventListener('mousedown', h)
    return () => document.removeEventListener('mousedown', h)
  }, [])

  // Scroll indicators voor tab bar
  const checkScroll = () => {
    const el = navScrollRef.current
    if (!el) return
    setCanScrollLeft(el.scrollLeft > 1)
    setCanScrollRight(el.scrollLeft < el.scrollWidth - el.clientWidth - 1)
  }

  useEffect(() => {
    const el = navScrollRef.current
    if (!el) return
    // Wacht op render dan check
    setTimeout(checkScroll, 100)
    el.addEventListener('scroll', checkScroll)
    window.addEventListener('resize', checkScroll)
    // ResizeObserver voor wanneer content verandert
    const ro = new ResizeObserver(checkScroll)
    ro.observe(el)
    return () => {
      ro.disconnect()
      el.removeEventListener('scroll', checkScroll)
      window.removeEventListener('resize', checkScroll)
    }
  }, [])

  // Scroll actieve tab in beeld
  useEffect(() => {
    const el = navScrollRef.current
    if (!el) return
    const active = el.querySelector('[data-active="true"]')
    if (active) {
      const rect = active.getBoundingClientRect()
      const containerRect = el.getBoundingClientRect()
      // Alleen scrollen als de actieve tab buiten beeld is
      if (rect.right > containerRect.right || rect.left < containerRect.left) {
        active.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'nearest' })
      }
    }
    setTimeout(checkScroll, 150)
  }, [view])

  const scrollNav = (dir) => {
    const el = navScrollRef.current
    if (el) el.scrollBy({ left: dir * 120, behavior: 'smooth' })
  }

  const activeItem = NAV_ITEMS.find(n => n.id === view)

  return (
    <>
      <style>{`
        @keyframes mcc-pulse{0%,100%{opacity:1}50%{opacity:0.3}}
        @keyframes mcc-fadein{from{opacity:0;transform:translateY(-8px)}to{opacity:1;transform:translateY(0)}}
        .mcc-tab:hover { color:${acc}!important; background:${acc}12!important; }
        .mcc-nav-scroll { scrollbar-width:none; -ms-overflow-style:none; }
        .mcc-nav-scroll::-webkit-scrollbar { display:none; }
        .mcc-menu-item:hover { background:${acc}15!important; color:${acc}!important; }
        .mcc-scroll-btn:hover { background:${acc}20!important; color:${acc}!important; }
        .mcc-settings-btn:hover { background:${acc}20!important; border-color:${acc}60!important; }
      `}</style>

      <nav style={{
        height: isMini ? '52px' : '60px',
        display:'flex', alignItems:'center',
        padding: isMini ? '0 10px' : '0 14px',
        background: t.bgSecondary,
        borderBottom: `1px solid ${t.border}`,
        flexShrink: 0, position:'relative', zIndex:50,
        gap: 0,
      }}>

        {/* ── KLOK ── */}
        <div style={{display:'flex',flexDirection:'column',alignItems:'flex-start',marginRight:'12px',flexShrink:0,gap:'1px'}}>
          <div style={{display:'flex',alignItems:'baseline',gap:'2px'}}>
            <span style={{
              fontSize: isMini ? '15px' : '20px',
              fontWeight:'600', color:t.text,
              fontVariantNumeric:'tabular-nums',
              letterSpacing:'0.04em', lineHeight:1,
              fontFamily:'ui-monospace,monospace',
            }}>
              {time.h}<span style={{opacity:pulse?1:0.25,transition:'opacity .5s'}}>:</span>{time.m}
            </span>
            {!isMini && <span style={{fontSize:'11px',color:t.textMuted,fontVariantNumeric:'tabular-nums',fontFamily:'ui-monospace,monospace'}}>{time.s}</span>}
          </div>
          <div style={{display:'flex',alignItems:'center',gap:'5px'}}>
            <span style={{fontSize:'8px',color:t.textMuted,letterSpacing:'0.06em',textTransform:'uppercase'}}>{isMini ? time.date.slice(0,6) : time.date}</span>
            <div style={{width:'4px',height:'4px',borderRadius:'50%',background:'#22c55e',boxShadow:'0 0 5px #22c55e80',animation:'mcc-pulse 2s infinite',flexShrink:0}}/>
            <span style={{fontSize:'8px',color:'#22c55e',letterSpacing:'0.04em'}}>{agentCount}{isMini?'':' online'}</span>
          </div>
          {false && (
            <div style={{display:'none'}}>
            </div>
          )}
        </div>

        {/* DIVIDER */}
        <div style={{width:'1px',height:'28px',background:t.border,marginRight:'12px',flexShrink:0}}/>

        {/* ── LOGO ── */}
        <div style={{display:'flex',alignItems:'center',gap:'8px',marginRight:'12px',flexShrink:0}}>
          {isMini ? (
            // Mini logo: ARC + AI AGENTS compact
            <div style={{display:'flex',flexDirection:'column',gap:'1px'}}>
              <div style={{display:'flex',alignItems:'baseline',gap:'0.3rem'}}>
                <span style={{
                  fontFamily:"ui-monospace,monospace", fontWeight:900, fontSize:'1.1rem',
                  letterSpacing:'-0.02em', color:acc, textShadow:`0 0 10px ${acc}`, lineHeight:1,
                }}>ARC</span>
                <span style={{
                  fontFamily:"ui-monospace,monospace", fontWeight:800, fontSize:'0.5rem',
                  letterSpacing:'0.18em', textTransform:'uppercase', color:'#dce8f8', lineHeight:1,
                }}>AI AGENTS</span>
              </div>
              <div style={{
                fontFamily:"ui-monospace,monospace", fontWeight:700, fontSize:'0.4rem',
                letterSpacing:'0.22em', textTransform:'uppercase', color:acc, opacity:0.65, lineHeight:1,
              }}>MISSION CONTROL</div>
            </div>
          ) : isHamburger ? (
            // Mobiel logo: ARC + AI AGENTS + MCC
            <div style={{display:'flex',flexDirection:'column',gap:'2px'}}>
              <div style={{display:'flex',alignItems:'baseline',gap:'0.4rem'}}>
                <span style={{
                  fontFamily:"ui-monospace,'Cascadia Code','Fira Code',Consolas,monospace",
                  fontWeight:900, fontSize:'1.4rem', letterSpacing:'-0.03em',
                  color:acc, textShadow:`0 0 14px ${acc}, 0 0 30px ${acc}`,
                  lineHeight:1,
                }}>ARC</span>
                <span style={{
                  fontFamily:"ui-monospace,monospace", fontWeight:800,
                  fontSize:'0.6rem', letterSpacing:'0.2em',
                  textTransform:'uppercase', color:'#dce8f8', lineHeight:1,
                }}>AI AGENTS</span>
              </div>
              <div style={{
                fontFamily:"ui-monospace,monospace", fontWeight:700,
                fontSize:'0.48rem', letterSpacing:'0.28em',
                textTransform:'uppercase', color:acc, opacity:0.65, lineHeight:1,
              }}>MISSION CONTROL CENTER</div>
            </div>
          ) : (
            // Volledig logo
            <div style={{display:'flex',flexDirection:'column',gap:'3px'}}>
              <div style={{display:'flex',alignItems:'baseline',gap:'0.6rem'}}>
                <span style={{
                  fontFamily:"ui-monospace,'Cascadia Code','Fira Code',Consolas,monospace",
                  fontWeight:900, fontSize:'2.1rem', letterSpacing:'-0.03em',
                  color:acc, textShadow:`0 0 14px ${acc}, 0 0 30px ${acc}, 0 0 60px ${acc}`,
                  lineHeight:1,
                }}>ARC</span>
                <span style={{
                  fontFamily:"ui-monospace,'Cascadia Code','Fira Code',Consolas,monospace",
                  fontWeight:800, fontSize:'0.82rem', letterSpacing:'0.28em',
                  textTransform:'uppercase', color:'#dce8f8', lineHeight:1,
                }}>AI AGENTS</span>
              </div>
              <div style={{
                fontFamily:"ui-monospace,'Cascadia Code','Fira Code',Consolas,monospace",
                fontWeight:700, fontSize:'0.58rem', letterSpacing:'0.32em',
                textTransform:'uppercase', color:acc, opacity:0.72, lineHeight:1,
              }}>MISSION CONTROL CENTER</div>
            </div>
          )}
        </div>

        {/* DIVIDER */}
        {!isMini && <div style={{width:'1px',height:'28px',background:t.border,marginRight:'10px',flexShrink:0}}/>}

        {/* ── NAV TABS (scrollbaar) of HAMBURGER ── */}
        {!isHamburger ? (
          // Desktop + tablet: scrollbare tab bar
          <div style={{display:'flex',alignItems:'stretch',flex:1,minWidth:0,height:'100%',overflow:'hidden'}}>
            {/* Scroll left indicator */}
            {canScrollLeft && (
              <button className="mcc-scroll-btn" onClick={() => scrollNav(-1)} style={{
                display:'flex', alignItems:'center', justifyContent:'center',
                width:'28px', minWidth:'28px',
                height:'100%', flexShrink:0,
                background:`linear-gradient(90deg,${t.bgSecondary} 60%,transparent)`,
                border:'none', borderRight:`1px solid ${t.border}`,
                color:acc, cursor:'pointer', fontSize:'16px', zIndex:2,
              }}>
                <i className="ti ti-chevron-left"/>
              </button>
            )}

            {/* Scrollbare tabs */}
            <div
              ref={navScrollRef}
              className="mcc-nav-scroll"
              style={{
                display:'flex', alignItems:'stretch', height:'100%',
                overflowX:'auto', flex:1,
              }}
            >
              {NAV_ITEMS.map(item => {
                const active = view === item.id
                return (
                  <button
                    key={item.id}
                    data-active={active}
                    className="mcc-tab"
                    onClick={() => setView(item.id)}
                    style={{
                      display:'flex', alignItems:'center', gap:'5px',
                      padding: isDesktop ? '0 13px' : '0 10px',
                      height:'100%', flexShrink:0,
                      background: active ? `${acc}18` : 'transparent',
                      border:'none',
                      borderBottom:`2px solid ${active ? acc : 'transparent'}`,
                      color: active ? acc : t.textMuted,
                      fontSize: isDesktop ? '11px' : '10px',
                      cursor:'pointer',
                      letterSpacing:'0.03em',
                      transition:'all .18s',
                      whiteSpace:'nowrap',
                      fontWeight: active ? 700 : 400,
                    }}
                  >
                    <i className={`ti ${item.icon}`} style={{fontSize: isDesktop ? '14px' : '13px'}}/>
                    {item.label}
                  </button>
                )
              })}
            </div>

            {/* Scroll right indicator */}
            {canScrollRight && (
              <button className="mcc-scroll-btn" onClick={() => scrollNav(1)} style={{
                display:'flex', alignItems:'center', justifyContent:'center',
                width:'28px', height:'100%', flexShrink:0,
                background:`linear-gradient(270deg,${t.bgSecondary} 60%,transparent)`,
                border:'none', borderLeft:`1px solid ${t.border}`,
                color:acc, cursor:'pointer', fontSize:'16px',
                zIndex:2,
              }}>
                <i className="ti ti-chevron-right"/>
              </button>
            )}
          </div>
        ) : (
          // Hamburger: toon actieve tab naam + menu knop
          <div style={{flex:1, display:'flex', alignItems:'center', gap:'8px', minWidth:0}}>
            {activeItem && (
              <div style={{display:'flex',alignItems:'center',gap:'6px',color:acc,fontSize:'12px',fontWeight:'600',overflow:'hidden'}}>
                <i className={`ti ${activeItem.icon}`} style={{fontSize:'15px',flexShrink:0}}/>
                <span style={{overflow:'hidden',textOverflow:'ellipsis',whiteSpace:'nowrap'}}>{activeItem.label}</span>
              </div>
            )}
          </div>
        )}

        {/* ── RIGHT CONTROLS ── */}
        <div style={{marginLeft:'auto',display:'flex',alignItems:'center',gap:'6px',flexShrink:0}}>
          {/* Settings knop */}
          <button
            className="mcc-settings-btn"
            onClick={onOpenSettings}
            style={{
              display:'flex', alignItems:'center', gap:'4px',
              padding: '4px 8px',
              height:'26px', borderRadius:'7px',
              border:`1px solid ${acc}40`,
              background:`${acc}15`,
              color:acc, cursor:'pointer',
              fontSize:'10px', fontWeight:'600',
              transition:'all .15s', flexShrink:0,
            }}
          >
            <i className="ti ti-palette" style={{fontSize:'12px'}}/>
            {!isMini && <span>Thema</span>}
          </button>

          {/* Hamburger menu knop */}
          {isHamburger && (
            <div ref={menuRef} style={{position:'relative'}}>
              <button
                onClick={() => setMenuOpen(o => !o)}
                style={{
                  width:'34px', height:'34px', borderRadius:'8px',
                  border:`1px solid ${t.border}`,
                  background: menuOpen ? `${acc}15` : 'transparent',
                  color: menuOpen ? acc : t.textMuted,
                  cursor:'pointer', fontSize:'18px',
                  display:'flex', alignItems:'center', justifyContent:'center',
                  transition:'all .15s',
                }}
              >
                <i className={menuOpen ? 'ti ti-x' : 'ti ti-menu-2'}/>
              </button>

              {menuOpen && (
                <div style={{
                  position:'absolute',
                  top:'calc(100% + 6px)',
                  right:0,
                  width:'220px',
                  background: t.bgSecondary,
                  border:`1px solid ${t.borderHover || t.border}`,
                  borderRadius:'12px',
                  overflow:'hidden',
                  boxShadow:`0 16px 48px rgba(0,0,0,0.7), 0 0 0 1px ${acc}20`,
                  animation:'mcc-fadein .15s ease',
                  zIndex:200,
                  maxHeight:'calc(100vh - 80px)',
                  overflowY:'auto',
                  scrollbarWidth:'thin',
                  scrollbarColor:`${acc} transparent`,
                }}>
                  {/* Menu header */}
                  <div style={{
                    padding:'10px 14px',
                    borderBottom:`1px solid ${t.border}`,
                    fontSize:'9px', fontWeight:'700',
                    letterSpacing:'0.15em', textTransform:'uppercase',
                    color:t.textMuted, position:'sticky', top:0,
                    background:t.bgSecondary, zIndex:1,
                  }}>
                    Navigatie
                  </div>
                  {NAV_ITEMS.map(item => {
                    const active = view === item.id
                    return (
                      <button
                        key={item.id}
                        className="mcc-menu-item"
                        onClick={() => { setView(item.id); setMenuOpen(false) }}
                        style={{
                          display:'flex', alignItems:'center', gap:'12px',
                          width:'100%', padding:'12px 16px',
                          background: active ? `${acc}18` : 'transparent',
                          border:'none',
                          borderLeft:`3px solid ${active ? acc : 'transparent'}`,
                          color: active ? acc : t.textSecondary,
                          fontSize:'13px', fontWeight: active ? 700 : 400,
                          cursor:'pointer', textAlign:'left',
                          transition:'all .15s',
                        }}
                      >
                        <i className={`ti ${item.icon}`} style={{fontSize:'17px',flexShrink:0,color:active?acc:t.textMuted}}/>
                        <span style={{flex:1}}>{item.label}</span>
                        {active && (
                          <div style={{width:6,height:6,borderRadius:'50%',background:acc,boxShadow:`0 0 6px ${acc}`,flexShrink:0}}/>
                        )}
                      </button>
                    )
                  })}
                </div>
              )}
            </div>
          )}
        </div>
      </nav>
    </>
  )
}
