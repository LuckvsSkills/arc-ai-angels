import React, { useState, useEffect, useRef } from 'react'

const PRIO_CONFIG = {
  1: { label: 'P1', color: '#ef4444', bg: 'rgba(239,68,68,0.1)', border: 'rgba(239,68,68,0.3)', text: 'Urgent' },
  2: { label: 'P2', color: '#f59e0b', bg: 'rgba(245,158,11,0.1)', border: 'rgba(245,158,11,0.3)', text: 'Normaal' },
  3: { label: 'P3', color: '#22c55e', bg: 'rgba(34,197,94,0.1)', border: 'rgba(34,197,94,0.3)', text: 'Laag' },
}

const STATUS_CONFIG = {
  open:  { label: 'Open',  color: '#7098b8', icon: 'ti-circle' },
  bezig: { label: 'Bezig', color: '#f59e0b', icon: 'ti-loader' },
  done:  { label: 'Klaar', color: '#22c55e', icon: 'ti-circle-check' },
}

function formatDate(iso) {
  if (!iso) return ''
  const d = new Date(iso)
  return d.toLocaleDateString('nl', { day: 'numeric', month: 'short', year: '2-digit' })
}

function TaskDetailPanel({ task, onClose, onSave, onDelete, t, acc }) {
  const [title, setTitle] = useState(task.title)
  const [priority, setPriority] = useState(task.priority)
  const [status, setStatus] = useState(task.status)
  const [notes, setNotes] = useState(task.notes || '')
  const [saving, setSaving] = useState(false)
  const prio = PRIO_CONFIG[priority] || PRIO_CONFIG[2]
  const stat = STATUS_CONFIG[status] || STATUS_CONFIG.open

  const save = async () => {
    setSaving(true)
    await onSave(task.id, { title, priority: parseInt(priority), status, notes })
    setSaving(false)
  }

  return (
    <div style={{
      position: 'fixed', inset: 0, zIndex: 200,
      display: 'flex', alignItems: 'center', justifyContent: 'center',
      background: 'rgba(0,0,0,0.7)', backdropFilter: 'blur(4px)',
      animation: 'mcc-fadein .2s ease',
    }} onClick={e => e.target === e.currentTarget && onClose()}>
      <div style={{
        width: 'min(580px, 95vw)', maxHeight: '90vh',
        background: t.bgSecondary, border: `1px solid ${t.border}`,
        borderRadius: 14, display: 'flex', flexDirection: 'column',
        boxShadow: `0 24px 80px rgba(0,0,0,0.6), 0 0 0 1px ${acc}20`,
        overflow: 'hidden',
      }}>
        {/* Header */}
        <div style={{ padding: '16px 20px', borderBottom: `1px solid ${t.border}`, display: 'flex', alignItems: 'center', gap: 10, flexShrink: 0 }}>
          <div style={{ width: 4, height: 24, background: prio.color, borderRadius: 2, flexShrink: 0 }} />
          <span style={{ fontSize: 13, fontWeight: 700, color: t.text, flex: 1 }}>Taak Details</span>
          <span style={{ fontSize: 10, color: t.textMuted }}>#{task.id.slice(-6)}</span>
          <button onClick={onClose} style={{ width: 28, height: 28, borderRadius: 7, border: `1px solid ${t.border}`, background: 'transparent', color: t.textMuted, cursor: 'pointer', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 16 }}>
            <i className="ti ti-x" />
          </button>
        </div>

        {/* Body */}
        <div style={{ flex: 1, overflow: 'auto', padding: '20px', display: 'flex', flexDirection: 'column', gap: 16 }}>
          {/* Titel */}
          <div>
            <label style={{ fontSize: 10, fontWeight: 700, letterSpacing: '0.12em', textTransform: 'uppercase', color: t.textMuted, display: 'block', marginBottom: 8 }}>Titel</label>
            <textarea
              value={title}
              onChange={e => setTitle(e.target.value)}
              rows={3}
              style={{ width: '100%', background: t.bgTertiary, border: `1px solid ${t.border}`, borderRadius: 8, padding: '10px 12px', color: t.text, fontSize: 13, fontFamily: 'inherit', resize: 'vertical', outline: 'none', lineHeight: 1.6 }}
            />
          </div>

          {/* Prioriteit + Status */}
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 12 }}>
            <div>
              <label style={{ fontSize: 10, fontWeight: 700, letterSpacing: '0.12em', textTransform: 'uppercase', color: t.textMuted, display: 'block', marginBottom: 8 }}>Prioriteit</label>
              <div style={{ display: 'flex', gap: 6 }}>
                {[1, 2, 3].map(p => {
                  const pc = PRIO_CONFIG[p]
                  const isActive = parseInt(priority) === p
                  return (
                    <button key={p} onClick={() => setPriority(p)} style={{
                      flex: 1, padding: '8px 4px', borderRadius: 8, cursor: 'pointer',
                      border: `1.5px solid ${isActive ? pc.color : t.border}`,
                      background: isActive ? pc.bg : 'transparent',
                      color: isActive ? pc.color : t.textMuted,
                      fontSize: 11, fontWeight: isActive ? 700 : 400,
                      transition: 'all .15s',
                    }}>
                      <div style={{ fontFamily: 'ui-monospace,monospace', fontWeight: 800, fontSize: 13 }}>{pc.label}</div>
                      <div style={{ fontSize: 9, marginTop: 2 }}>{pc.text}</div>
                    </button>
                  )
                })}
              </div>
            </div>
            <div>
              <label style={{ fontSize: 10, fontWeight: 700, letterSpacing: '0.12em', textTransform: 'uppercase', color: t.textMuted, display: 'block', marginBottom: 8 }}>Status</label>
              <div style={{ display: 'flex', gap: 6 }}>
                {Object.entries(STATUS_CONFIG).map(([key, sc]) => {
                  const isActive = status === key
                  return (
                    <button key={key} onClick={() => setStatus(key)} style={{
                      flex: 1, padding: '8px 4px', borderRadius: 8, cursor: 'pointer',
                      border: `1.5px solid ${isActive ? sc.color : t.border}`,
                      background: isActive ? `${sc.color}15` : 'transparent',
                      color: isActive ? sc.color : t.textMuted,
                      fontSize: 9, fontWeight: isActive ? 700 : 400,
                      transition: 'all .15s', display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 3,
                    }}>
                      <i className={`ti ${sc.icon}`} style={{ fontSize: 14 }} />
                      {sc.label}
                    </button>
                  )
                })}
              </div>
            </div>
          </div>

          {/* Notes */}
          <div>
            <label style={{ fontSize: 10, fontWeight: 700, letterSpacing: '0.12em', textTransform: 'uppercase', color: t.textMuted, display: 'block', marginBottom: 8 }}>Notities / Context</label>
            <textarea
              value={notes}
              onChange={e => setNotes(e.target.value)}
              rows={4}
              placeholder="Voeg context, links of notities toe..."
              style={{ width: '100%', background: t.bgTertiary, border: `1px solid ${t.border}`, borderRadius: 8, padding: '10px 12px', color: t.text, fontSize: 12, fontFamily: 'inherit', resize: 'vertical', outline: 'none', lineHeight: 1.7 }}
            />
          </div>

          {/* Meta */}
          <div style={{ display: 'flex', gap: 16, fontSize: 10, color: t.textMuted, paddingTop: 4 }}>
            <span>Aangemaakt: {formatDate(task.created_at)}</span>
            {task.updated_at && <span>Bijgewerkt: {formatDate(task.updated_at)}</span>}
          </div>
        </div>

        {/* Footer */}
        <div style={{ padding: '14px 20px', borderTop: `1px solid ${t.border}`, display: 'flex', gap: 8, flexShrink: 0 }}>
          <button onClick={() => onDelete(task.id)} style={{ padding: '8px 14px', borderRadius: 8, border: '1px solid rgba(239,68,68,0.3)', background: 'rgba(239,68,68,0.08)', color: '#ef4444', cursor: 'pointer', fontSize: 11, fontWeight: 600, display: 'flex', alignItems: 'center', gap: 6 }}>
            <i className="ti ti-trash" style={{ fontSize: 13 }} /> Verwijderen
          </button>
          <div style={{ flex: 1 }} />
          <button onClick={onClose} style={{ padding: '8px 16px', borderRadius: 8, border: `1px solid ${t.border}`, background: 'transparent', color: t.textMuted, cursor: 'pointer', fontSize: 11 }}>
            Annuleren
          </button>
          <button onClick={save} disabled={saving} style={{ padding: '8px 20px', borderRadius: 8, border: `1px solid ${acc}60`, background: `${acc}20`, color: acc, cursor: 'pointer', fontSize: 11, fontWeight: 700, opacity: saving ? 0.7 : 1 }}>
            {saving ? 'Opslaan...' : 'Opslaan'}
          </button>
        </div>
      </div>
    </div>
  )
}

function TaskCard({ item, onOpen, onToggle, onDelete, t, acc }) {
  const prio = PRIO_CONFIG[item.priority] || PRIO_CONFIG[2]
  const stat = STATUS_CONFIG[item.status] || STATUS_CONFIG.open
  const isDone = item.status === 'done'

  return (
    <div
      onClick={() => onOpen(item)}
      style={{
        background: t.bgSecondary,
        border: `1px solid ${isDone ? t.border : prio.border}`,
        borderLeft: `4px solid ${isDone ? t.border : prio.color}`,
        borderRadius: 10, padding: '14px 14px',
        cursor: 'pointer', transition: 'all .15s',
        opacity: isDone ? 0.55 : 1,
        display: 'flex', flexDirection: 'column', gap: 10,
        WebkitTapHighlightColor: 'transparent',
        userSelect: 'none',
      }}
    >
      {/* Top row */}
      <div style={{ display: 'flex', alignItems: 'flex-start', gap: 10 }}>
        {/* Checkbox */}
        <button
          onClick={e => { e.stopPropagation(); onToggle(item) }}
          style={{
            width: 24, height: 24, borderRadius: 6, flexShrink: 0, marginTop: 1,
            border: `2px solid ${isDone ? '#22c55e' : stat.color}`,
            background: isDone ? '#22c55e' : 'transparent',
            cursor: 'pointer', display: 'flex', alignItems: 'center', justifyContent: 'center',
            transition: 'all .15s', WebkitTapHighlightColor: 'transparent',
          }}
        >
          {isDone && <i className="ti ti-check" style={{ fontSize: 12, color: '#000' }} />}
          {item.status === 'bezig' && !isDone && <i className="ti ti-loader" style={{ fontSize: 12, color: stat.color }} />}
        </button>
        {/* Title */}
        <span style={{
          fontSize: 12, lineHeight: 1.6, color: isDone ? t.textMuted : t.text,
          flex: 1, textDecoration: isDone ? 'line-through' : 'none',
        }}>
          {item.title}
        </span>
      </div>

      {/* Bottom row */}
      <div style={{ display: 'flex', alignItems: 'center', gap: 8, paddingLeft: 30 }}>
        <span style={{
          fontSize: 9, fontWeight: 700, padding: '2px 7px', borderRadius: 4,
          background: isDone ? 'transparent' : prio.bg,
          color: isDone ? t.textMuted : prio.color,
          border: `1px solid ${isDone ? t.border : prio.border}`,
          fontFamily: 'ui-monospace,monospace',
        }}>{prio.label}</span>
        <span style={{
          fontSize: 9, padding: '2px 7px', borderRadius: 4,
          background: `${stat.color}12`, color: stat.color,
          border: `1px solid ${stat.color}30`,
          display: 'flex', alignItems: 'center', gap: 4,
        }}>
          <i className={`ti ${stat.icon}`} style={{ fontSize: 9 }} />
          {stat.label}
        </span>
        {item.notes && <i className="ti ti-notes" style={{ fontSize: 10, color: t.textMuted }} title="Heeft notities" />}
        <span style={{ flex: 1 }} />
        <span style={{ fontSize: 9, color: t.textMuted }}>{formatDate(item.created_at)}</span>
        <button
          onClick={e => { e.stopPropagation(); onDelete(item.id) }}
          style={{ background: 'transparent', border: 'none', color: t.textMuted, cursor: 'pointer', fontSize: 13, padding: '0 2px', opacity: 0.5, transition: 'opacity .15s' }}
          title="Verwijderen"
        >
          <i className="ti ti-trash" />
        </button>
      </div>
    </div>
  )
}

export default function TodoTab({ theme }) {
  const t = theme?.colors || {}
  const acc = t.accent || '#c9a84c'

  const [items, setItems] = useState([])
  const [loading, setLoading] = useState(true)
  const [activeTab, setActiveTab] = useState('open')
  const [selectedTask, setSelectedTask] = useState(null)
  const [filterPrio, setFilterPrio] = useState('all')
  const [search, setSearch] = useState('')
  const [newTitle, setNewTitle] = useState('')
  const [newPrio, setNewPrio] = useState(2)
  const [adding, setAdding] = useState(false)
  const [showAddForm, setShowAddForm] = useState(false)
  const inputRef = useRef(null)
  const [winW, setWinW] = useState(window.innerWidth)
  const isMobile = winW < 680

  useEffect(() => {
    const h = () => setWinW(window.innerWidth)
    window.addEventListener('resize', h)
    return () => window.removeEventListener('resize', h)
  }, [])

  const load = () => {
    fetch('/api/todo/items').then(r => r.json()).then(d => {
      setItems(d.items || [])
      setLoading(false)
    }).catch(() => setLoading(false))
  }
  useEffect(() => { load() }, [])

  useEffect(() => {
    if (showAddForm && inputRef.current) inputRef.current.focus()
  }, [showAddForm])

  const add = async () => {
    if (!newTitle.trim()) return
    setAdding(true)
    await fetch('/api/todo/items', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title: newTitle.trim(), priority: newPrio, status: 'open' }),
    })
    setNewTitle('')
    setNewPrio(2)
    setShowAddForm(false)
    setAdding(false)
    load()
  }

  const save = async (id, updates) => {
    await fetch(`/api/todo/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(updates),
    })
    setSelectedTask(null)
    load()
  }

  const del = async (id) => {
    await fetch(`/api/todo/${id}`, { method: 'DELETE' })
    setSelectedTask(null)
    load()
  }

  const toggle = async (item) => {
    const next = item.status === 'done' ? 'open'
      : item.status === 'open' ? 'bezig'
      : 'done'
    await fetch(`/api/todo/${item.id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ status: next }),
    })
    load()
  }

  // Gefilterde items
  const filtered = items
    .filter(x => activeTab === 'done' ? x.status === 'done' : x.status !== 'done')
    .filter(x => filterPrio === 'all' || x.priority === parseInt(filterPrio))
    .filter(x => !search || x.title.toLowerCase().includes(search.toLowerCase()))
    .sort((a, b) => {
      if (activeTab !== 'done') return (a.priority || 3) - (b.priority || 3)
      return new Date(b.updated_at || b.created_at) - new Date(a.updated_at || a.created_at)
    })

  const openCount = items.filter(x => x.status !== 'done').length
  const doneCount = items.filter(x => x.status === 'done').length
  const p1Count = items.filter(x => x.priority === 1 && x.status !== 'done').length
  const bezigCount = items.filter(x => x.status === 'bezig').length

  return (
    <div style={{ height: '100%', display: 'flex', flexDirection: 'column', overflow: 'hidden', background: t.bg }}>

      {/* ── HEADER ── */}
      <div style={{ flexShrink: 0, background: t.bgSecondary, borderBottom: `1px solid ${t.border}`, padding: isMobile ? '12px 14px' : '16px 20px' }}>

        {/* Title + stats */}
        <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 14, flexWrap: 'wrap' }}>
          <div style={{ flex: 1 }}>
            <div style={{ fontSize: 16, fontWeight: 800, color: t.text, letterSpacing: '-0.01em' }}>Task Queue</div>
            <div style={{ display: 'flex', gap: 12, marginTop: 5, flexWrap: 'wrap' }}>
              {[
                { label: 'Open', val: openCount, color: t.textMuted },
                { label: 'Bezig', val: bezigCount, color: '#f59e0b' },
                { label: 'P1 Urgent', val: p1Count, color: '#ef4444' },
                { label: 'Klaar', val: doneCount, color: '#22c55e' },
              ].map(s => (
                <span key={s.label} style={{ fontSize: 11, color: s.color }}>
                  <strong style={{ fontFamily: 'ui-monospace,monospace', fontWeight: 800 }}>{s.val}</strong> {s.label}
                </span>
              ))}
            </div>
          </div>
          <button
            onClick={() => setShowAddForm(v => !v)}
            style={{
              display: 'flex', alignItems: 'center', gap: 7,
              padding: '9px 16px', borderRadius: 9,
              border: `1.5px solid ${showAddForm ? acc + '80' : acc + '50'}`,
              background: showAddForm ? `${acc}25` : `${acc}15`,
              color: acc, cursor: 'pointer', fontSize: 12, fontWeight: 700,
              transition: 'all .15s',
            }}
          >
            <i className={`ti ${showAddForm ? 'ti-x' : 'ti-plus'}`} style={{ fontSize: 15 }} />
            {showAddForm ? 'Annuleren' : 'Nieuwe Taak'}
          </button>
        </div>

        {/* Add form */}
        {showAddForm && (
          <div style={{
            marginBottom: 14, padding: '14px 16px',
            background: t.bgTertiary, border: `1px solid ${acc}30`,
            borderRadius: 10, display: 'flex', flexDirection: 'column', gap: 10,
            animation: 'mcc-fadein .2s ease',
          }}>
            <textarea
              ref={inputRef}
              value={newTitle}
              onChange={e => setNewTitle(e.target.value)}
              onKeyDown={e => e.key === 'Enter' && e.ctrlKey && add()}
              placeholder="Beschrijf de taak... (Ctrl+Enter om toe te voegen)"
              rows={2}
              style={{ background: t.bgSecondary, border: `1px solid ${t.border}`, borderRadius: 7, padding: '9px 12px', color: t.text, fontSize: 12, fontFamily: 'inherit', resize: 'none', outline: 'none', lineHeight: 1.6 }}
            />
            <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
              <span style={{ fontSize: 10, color: t.textMuted, fontWeight: 700, letterSpacing: '0.1em' }}>PRIORITEIT:</span>
              {[1, 2, 3].map(p => {
                const pc = PRIO_CONFIG[p]
                return (
                  <button key={p} onClick={() => setNewPrio(p)} style={{
                    padding: '5px 12px', borderRadius: 7, cursor: 'pointer',
                    border: `1.5px solid ${newPrio === p ? pc.color : t.border}`,
                    background: newPrio === p ? pc.bg : 'transparent',
                    color: newPrio === p ? pc.color : t.textMuted,
                    fontSize: 11, fontWeight: newPrio === p ? 700 : 400,
                    fontFamily: 'ui-monospace,monospace',
                  }}>{pc.label}</button>
                )
              })}
              <div style={{ flex: 1 }} />
              <button onClick={add} disabled={adding || !newTitle.trim()} style={{
                padding: '7px 18px', borderRadius: 8,
                border: `1px solid ${acc}60`, background: `${acc}20`,
                color: acc, cursor: 'pointer', fontSize: 12, fontWeight: 700,
                opacity: !newTitle.trim() ? 0.5 : 1,
              }}>
                {adding ? 'Toevoegen...' : 'Toevoegen'}
              </button>
            </div>
          </div>
        )}

        {/* Tabs + filters */}
        <div style={{ display: 'flex', alignItems: 'center', gap: 8, flexWrap: 'wrap' }}>
          {/* Tab switcher */}
          <div style={{ display: 'flex', background: t.bgTertiary, borderRadius: 8, padding: 3, gap: 2 }}>
            {[
              { id: 'open', label: `Actief (${openCount})` },
              { id: 'done', label: `Klaar (${doneCount})` },
            ].map(tab => (
              <button key={tab.id} onClick={() => setActiveTab(tab.id)} style={{
                padding: '5px 14px', borderRadius: 6, cursor: 'pointer',
                border: activeTab === tab.id ? `1px solid ${acc}40` : '1px solid transparent',
                background: activeTab === tab.id ? t.bgSecondary : 'transparent',
                color: activeTab === tab.id ? acc : t.textMuted,
                fontSize: 11, fontWeight: activeTab === tab.id ? 700 : 400,
                transition: 'all .15s',
              }}>{tab.label}</button>
            ))}
          </div>

          {/* Prio filter */}
          <div style={{ display: 'flex', gap: 4 }}>
            {[['all', 'Alle'], ['1', 'P1'], ['2', 'P2'], ['3', 'P3']].map(([v, l]) => {
              const pc = v !== 'all' ? PRIO_CONFIG[parseInt(v)] : null
              return (
                <button key={v} onClick={() => setFilterPrio(v)} style={{
                  padding: '5px 10px', borderRadius: 6, cursor: 'pointer', fontSize: 10,
                  border: `1px solid ${filterPrio === v ? (pc?.color || acc) + '60' : t.border}`,
                  background: filterPrio === v ? `${pc?.color || acc}15` : 'transparent',
                  color: filterPrio === v ? (pc?.color || acc) : t.textMuted,
                  fontWeight: filterPrio === v ? 700 : 400,
                }}>{l}</button>
              )
            })}
          </div>

          {/* Search */}
          <div style={{ flex: 1, minWidth: 140, maxWidth: 260 }}>
            <input
              value={search}
              onChange={e => setSearch(e.target.value)}
              placeholder="Zoek taak..."
              style={{ width: '100%', padding: '6px 10px', background: t.bgTertiary, border: `1px solid ${t.border}`, borderRadius: 7, color: t.text, fontSize: 11, fontFamily: 'inherit', outline: 'none' }}
            />
          </div>
        </div>
      </div>

      {/* ── TASK LIST ── */}
      <div style={{ flex: 1, overflowY: 'auto', padding: isMobile ? '12px 14px' : '16px 20px', scrollbarWidth: 'thin', scrollbarColor: `${acc} transparent` }}>
        {loading ? (
          <div style={{ color: t.textMuted, fontSize: 13, padding: 20 }}>Laden...</div>
        ) : filtered.length === 0 ? (
          <div style={{ textAlign: 'center', padding: '48px 20px', color: t.textMuted }}>
            <i className={`ti ${activeTab === 'done' ? 'ti-mood-happy' : 'ti-check'}`} style={{ fontSize: 32, display: 'block', marginBottom: 12, opacity: 0.4 }} />
            <div style={{ fontSize: 13, fontWeight: 600, marginBottom: 4 }}>
              {activeTab === 'done' ? 'Nog niets voltooid' : 'Geen taken gevonden'}
            </div>
            <div style={{ fontSize: 11 }}>
              {search ? 'Pas de zoekopdracht aan' : activeTab === 'done' ? 'Voltooide taken verschijnen hier' : 'Maak een nieuwe taak aan'}
            </div>
          </div>
        ) : (
          <div style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
            {/* P1 group header */}
            {activeTab === 'open' && filtered.some(x => x.priority === 1) && (
              <>
                <div style={{ fontSize: 9, fontWeight: 700, letterSpacing: '0.16em', textTransform: 'uppercase', color: '#ef4444', padding: '4px 0', display: 'flex', alignItems: 'center', gap: 6 }}>
                  <div style={{ width: 2, height: 10, background: '#ef4444', borderRadius: 1 }} />
                  Urgent — P1
                </div>
                {filtered.filter(x => x.priority === 1).map(item => (
                  <TaskCard key={item.id} item={item} onOpen={setSelectedTask} onToggle={toggle} onDelete={del} t={t} acc={acc} />
                ))}
              </>
            )}

            {/* P2 group */}
            {activeTab === 'open' && filtered.some(x => x.priority === 2) && (
              <>
                <div style={{ fontSize: 9, fontWeight: 700, letterSpacing: '0.16em', textTransform: 'uppercase', color: '#f59e0b', padding: '4px 0', marginTop: filtered.some(x => x.priority === 1) ? 8 : 0, display: 'flex', alignItems: 'center', gap: 6 }}>
                  <div style={{ width: 2, height: 10, background: '#f59e0b', borderRadius: 1 }} />
                  Normaal — P2
                </div>
                {filtered.filter(x => x.priority === 2).map(item => (
                  <TaskCard key={item.id} item={item} onOpen={setSelectedTask} onToggle={toggle} onDelete={del} t={t} acc={acc} />
                ))}
              </>
            )}

            {/* P3 group */}
            {activeTab === 'open' && filtered.some(x => x.priority === 3) && (
              <>
                <div style={{ fontSize: 9, fontWeight: 700, letterSpacing: '0.16em', textTransform: 'uppercase', color: '#22c55e', padding: '4px 0', marginTop: filtered.some(x => x.priority <= 2) ? 8 : 0, display: 'flex', alignItems: 'center', gap: 6 }}>
                  <div style={{ width: 2, height: 10, background: '#22c55e', borderRadius: 1 }} />
                  Laag — P3
                </div>
                {filtered.filter(x => x.priority === 3).map(item => (
                  <TaskCard key={item.id} item={item} onOpen={setSelectedTask} onToggle={toggle} onDelete={del} t={t} acc={acc} />
                ))}
              </>
            )}

            {/* Done tab — geen groepen */}
            {activeTab === 'done' && filtered.map(item => (
              <TaskCard key={item.id} item={item} onOpen={setSelectedTask} onToggle={toggle} onDelete={del} t={t} acc={acc} />
            ))}
          </div>
        )}
      </div>

      {/* ── DETAIL PANEL ── */}
      {selectedTask && (
        <TaskDetailPanel
          task={selectedTask}
          onClose={() => setSelectedTask(null)}
          onSave={save}
          onDelete={del}
          t={t}
          acc={acc}
        />
      )}
    </div>
  )
}
