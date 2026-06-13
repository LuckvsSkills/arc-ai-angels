import React, { useState, useEffect, useRef } from 'react'
import PulseTab from './PulseTab'
import SchedulerView from './views/SchedulerView'
import MdAuditTab from './MdAuditTab'
import ToolsTab from './ToolsTab'
import SkillsTab from './SkillsTab'
import TiersTab from './TiersTab'
import KostenTab from './KostenTab'
import DomeinTab from './DomeinTab'
import ServicesTab from './ServicesTab'
import TasksView from './views/TasksView'
import TodoTab from './TodoTab'
import AnalyticsView from './views/AnalyticsView'

const TABS = [
  { id: 'services',  label: 'Services',  icon: 'ti-server' },
  { id: 'todo',      label: 'Todo',      icon: 'ti-check' },
  { id: 'tasks',     label: 'Tasks',     icon: 'ti-checklist' },
  { id: 'scheduler', label: 'Scheduler', icon: 'ti-calendar' },
  { id: 'pulse',     label: 'Pulse',     icon: 'ti-heartbeat' },
  { id: 'tiers',     label: 'Tiers',     icon: 'ti-layers-difference' },
  { id: 'domein',    label: 'Domein',    icon: 'ti-sitemap' },
  { id: 'md-audit',  label: 'MD Audit',  icon: 'ti-file-text' },
  { id: 'tools',     label: 'Tools',     icon: 'ti-tools' },
  { id: 'skills',    label: 'Skills',    icon: 'ti-sparkles' },
  { id: 'analytics', label: 'Analytics', icon: 'ti-chart-line' },
  { id: 'kosten',    label: 'Kosten',    icon: 'ti-coin' },
]

export default function SysteemTab({ theme }) {
  const t = theme?.colors || {}
  const acc = t.accent || '#c9a84c'
  const [tab, setTab] = useState('todo')
  const [winW, setWinW] = useState(window.innerWidth)
  const [menuOpen, setMenuOpen] = useState(false)
  const [canScrollLeft, setCanScrollLeft] = useState(false)
  const [canScrollRight, setCanScrollRight] = useState(false)
  const scrollRef = useRef(null)
  const menuRef = useRef(null)

  // Nooit hamburger — altijd scrollbaar
  const isHamburger = false

  useEffect(() => {
    const h = () => setWinW(window.innerWidth)
    window.addEventListener('resize', h)
    return () => window.removeEventListener('resize', h)
  }, [])

  // Sluit menu bij klik buiten
  useEffect(() => {
    const h = e => { if (menuRef.current && !menuRef.current.contains(e.target)) setMenuOpen(false) }
    document.addEventListener('mousedown', h)
    return () => document.removeEventListener('mousedown', h)
  }, [])

  // Scroll indicators
  const checkScroll = () => {
    const el = scrollRef.current
    if (!el) return
    setCanScrollLeft(el.scrollLeft > 4)
    setCanScrollRight(el.scrollLeft < el.scrollWidth - el.clientWidth - 4)
  }

  useEffect(() => {
    const el = scrollRef.current
    if (!el) return
    checkScroll()
    el.addEventListener('scroll', checkScroll)
    window.addEventListener('resize', checkScroll)
    return () => {
      el.removeEventListener('scroll', checkScroll)
      window.removeEventListener('resize', checkScroll)
    }
  }, [])

  // Actieve tab in beeld scrollen
  useEffect(() => {
    const el = scrollRef.current
    if (!el) return
    const active = el.querySelector('[data-active="true"]')
    if (active) active.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'nearest' })
    setTimeout(checkScroll, 100)
  }, [tab])

  const scrollNav = dir => {
    const el = scrollRef.current
    if (el) el.scrollBy({ left: dir * 120, behavior: 'smooth' })
  }

  const activeItem = TABS.find(tb => tb.id === tab)

  return (
    <div style={{ height: '100%', display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
      <style>{`
        .kernel-tab:hover { color: ${acc} !important; background: ${acc}10 !important; }
        .kernel-scroll { scrollbar-width: none; }
        .kernel-scroll::-webkit-scrollbar { display: none; }
        .kernel-menu-item:hover { background: ${acc}15 !important; color: ${acc} !important; }
        .kernel-scroll-btn:hover { color: ${acc} !important; }
      `}</style>

      {/* ── SUBNAV ── */}
      <div style={{ flexShrink: 0, background: t.bgSecondary, borderBottom: `1px solid ${t.border}`, display: 'flex', alignItems: 'stretch', height: 42 }}>

        {!isHamburger ? (
          // Scrollbare tabs
          <div style={{ display: 'flex', flex: 1, alignItems: 'stretch', overflow: 'hidden' }}>
            {/* Links pijl */}
            {canScrollLeft && (
              <button className="kernel-scroll-btn" onClick={() => scrollNav(-1)} style={{
                display: 'flex', alignItems: 'center', justifyContent: 'center',
                width: 28, flexShrink: 0,
                background: `linear-gradient(90deg, ${t.bgSecondary} 60%, transparent)`,
                border: 'none', borderRight: `1px solid ${t.border}`,
                color: t.textMuted, cursor: 'pointer', fontSize: 14,
              }}>
                <i className="ti ti-chevron-left" />
              </button>
            )}

            {/* Scrollbare tabs */}
            <div ref={scrollRef} className="kernel-scroll" style={{ display: 'flex', alignItems: 'stretch', flex: 1, overflowX: 'auto' }}>
              {TABS.map(item => {
                const isActive = tab === item.id
                return (
                  <button
                    key={item.id}
                    data-active={isActive}
                    className="kernel-tab"
                    onClick={() => setTab(item.id)}
                    style={{
                      display: 'flex', alignItems: 'center', gap: 5,
                      padding: '0 14px', height: '100%', flexShrink: 0,
                      background: isActive ? `${acc}15` : 'transparent',
                      border: 'none',
                      borderBottom: `2px solid ${isActive ? acc : 'transparent'}`,
                      color: isActive ? acc : t.textMuted,
                      cursor: 'pointer', fontSize: 11,
                      fontWeight: isActive ? 700 : 400,
                      transition: 'all .15s', whiteSpace: 'nowrap',
                    }}
                  >
                    <i className={`ti ${item.icon}`} style={{ fontSize: 13 }} />
                    {item.label}
                  </button>
                )
              })}
            </div>

            {/* Rechts pijl */}
            {canScrollRight && (
              <button className="kernel-scroll-btn" onClick={() => scrollNav(1)} style={{
                display: 'flex', alignItems: 'center', justifyContent: 'center',
                width: 28, flexShrink: 0,
                background: `linear-gradient(270deg, ${t.bgSecondary} 60%, transparent)`,
                border: 'none', borderLeft: `1px solid ${t.border}`,
                color: t.textMuted, cursor: 'pointer', fontSize: 14,
              }}>
                <i className="ti ti-chevron-right" />
              </button>
            )}
          </div>
        ) : (
          // Hamburger modus
          <div style={{ display: 'flex', alignItems: 'center', flex: 1, padding: '0 12px', gap: 10 }}>
            {/* Actieve tab naam */}
            <div style={{ display: 'flex', alignItems: 'center', gap: 7, flex: 1, color: acc, fontSize: 13, fontWeight: 700 }}>
              {activeItem && <i className={`ti ${activeItem.icon}`} style={{ fontSize: 15 }} />}
              {activeItem?.label}
            </div>

            {/* Hamburger knop */}
            <div ref={menuRef} style={{ position: 'relative' }}>
              <button
                onClick={() => setMenuOpen(o => !o)}
                style={{
                  display: 'flex', alignItems: 'center', gap: 6,
                  padding: '5px 10px', borderRadius: 7,
                  border: `1px solid ${menuOpen ? acc + '50' : t.border}`,
                  background: menuOpen ? `${acc}15` : 'transparent',
                  color: menuOpen ? acc : t.textMuted,
                  cursor: 'pointer', fontSize: 11, fontWeight: 600,
                }}
              >
                <i className={`ti ${menuOpen ? 'ti-x' : 'ti-menu-2'}`} style={{ fontSize: 15 }} />
                {!menuOpen && <span>Menu</span>}
              </button>

              {/* Dropdown menu */}
              {menuOpen && (
                <div style={{
                  position: 'absolute', top: 'calc(100% + 6px)', right: 0,
                  width: 200, background: t.bgSecondary,
                  border: `1px solid ${t.borderHover || t.border}`,
                  borderRadius: 10, overflow: 'hidden',
                  boxShadow: `0 12px 40px rgba(0,0,0,0.6), 0 0 0 1px ${acc}20`,
                  animation: 'mcc-fadein .15s ease', zIndex: 100,
                  maxHeight: 'calc(100vh - 120px)', overflowY: 'auto',
                }}>
                  <div style={{ padding: '8px 12px', borderBottom: `1px solid ${t.border}`, fontSize: 9, fontWeight: 700, letterSpacing: '0.15em', textTransform: 'uppercase', color: t.textMuted, position: 'sticky', top: 0, background: t.bgSecondary }}>
                    Kernel
                  </div>
                  {TABS.map(item => {
                    const isActive = tab === item.id
                    return (
                      <button
                        key={item.id}
                        className="kernel-menu-item"
                        onClick={() => { setTab(item.id); setMenuOpen(false) }}
                        style={{
                          display: 'flex', alignItems: 'center', gap: 10,
                          width: '100%', padding: '11px 14px',
                          background: isActive ? `${acc}15` : 'transparent',
                          border: 'none', borderLeft: `3px solid ${isActive ? acc : 'transparent'}`,
                          color: isActive ? acc : t.textSecondary,
                          fontSize: 12, fontWeight: isActive ? 700 : 400,
                          cursor: 'pointer', textAlign: 'left', transition: 'all .15s',
                        }}
                      >
                        <i className={`ti ${item.icon}`} style={{ fontSize: 15, color: isActive ? acc : t.textMuted }} />
                        <span style={{ flex: 1 }}>{item.label}</span>
                        {isActive && <div style={{ width: 6, height: 6, borderRadius: '50%', background: acc, boxShadow: `0 0 6px ${acc}` }} />}
                      </button>
                    )
                  })}
                </div>
              )}
            </div>
          </div>
        )}
      </div>

      {/* ── CONTENT ── */}
      <div style={{ flex: 1, overflow: 'hidden' }}>
        {tab === 'todo'      ? <TodoTab theme={theme} /> :
         tab === 'pulse'     ? <PulseTab theme={theme} /> :
         tab === 'scheduler' ? <SchedulerView theme={theme} /> :
         tab === 'md-audit'  ? <MdAuditTab theme={theme} /> :
         tab === 'tasks'     ? <TasksView theme={theme} /> :
         tab === 'tools'     ? <ToolsTab theme={theme} /> :
         tab === 'skills'    ? <SkillsTab theme={theme} /> :
         tab === 'services'  ? <ServicesTab theme={theme} /> :
         tab === 'tiers'     ? <TiersTab theme={theme} /> :
         tab === 'kosten'    ? <KostenTab theme={theme} /> :
         tab === 'domein'    ? <DomeinTab theme={theme} /> :
<AnalyticsView theme={theme} />}
      </div>
    </div>
  )
}
