import React, { useState, useEffect } from 'react'
import { THEMES, getCompatTheme } from './themes'
import LoginPage from './components/LoginPage'
import TopNav from './components/TopNav'
import SettingsPanel from './components/SettingsPanel'
import Viewport from './components/Viewport'
import CodexTab from './components/CodexTab'
import DiagramsTab from './components/DiagramsTab'
import TodoTab from './components/TodoTab'
import MdAuditTab from './components/MdAuditTab'
import SysteemTab from './components/SysteemTab'
import SkillsTab from './components/SkillsTab'

class ErrorBoundary extends React.Component {
  constructor(props) { super(props); this.state = { hasError: false, error: null } }
  static getDerivedStateFromError(error) { return { hasError: true, error } }
  render() {
    if (this.state.hasError) {
      const t = this.props.theme?.colors || {}
      return (
        <div style={{padding:'40px',color:t.danger||'#f87171'}}>
          <h2>⚠️ Component fout</h2>
          <pre style={{fontSize:'11px',color:t.textMuted||'#888',marginTop:'12px'}}>{this.state.error?.message}</pre>
          <button onClick={() => this.setState({hasError:false,error:null})} style={{marginTop:'16px',padding:'8px 16px',background:'transparent',border:`1px solid ${t.border||'#444'}`,color:t.textSecondary||'#aaa',borderRadius:'6px',cursor:'pointer'}}>
            Opnieuw proberen
          </button>
        </div>
      )
    }
    return this.props.children
  }
}

export default function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false)
  const [authChecked, setAuthChecked] = useState(false)
  const [view, setView] = useState('agents')
  const [themeName, setThemeName] = useState(() => {
    try { return localStorage.getItem('mcc_theme') || 'imperial' } catch { return 'imperial' }
  })
  const [fontSize, setFontSize] = useState(() => {
    try { return parseInt(localStorage.getItem('mcc_fontsize') || '16') } catch { return 16 }
  })
  const setFontSizePersist = (s) => {
    setFontSize(s)
    try { localStorage.setItem('mcc_fontsize', String(s)) } catch {}
  }
  const [dropdownOpacity, setDropdownOpacity] = useState(80)
  const [settingsOpen, setSettingsOpen] = useState(false)
  const [agentCount, setAgentCount] = useState(32)

  const setThemeNamePersist = (name) => {
    setThemeName(name)
    try { localStorage.setItem('mcc_theme', name) } catch {}
  }

  const theme = getCompatTheme(themeName)
  const t = theme.colors

  useEffect(() => {
    // Zoom op body schaalt alles mee inclusief hardcoded px
    const scale = fontSize / 14
    document.body.style.zoom = String(scale)
    document.body.style.width = `${100/scale}%`
  }, [fontSize])

  useEffect(() => {
    fetch('/auth/me')
      .then(r => {
        if (r.ok) return r.json()
        throw new Error('Niet ingelogd')
      })
      .then(d => { if (d.email || d.logged_in) setIsLoggedIn(true) })
      .catch(() => { setIsLoggedIn(false) })
      .finally(() => setAuthChecked(true))
  }, [])

  if (!authChecked) {
    return <div style={{minHeight:'100vh',background:'#0e1320',display:'flex',alignItems:'center',justifyContent:'center',color:'#c9a84c',fontSize:'14px'}}>⏳ Laden...</div>
  }

  if (!isLoggedIn) {
    return <LoginPage onLogin={() => setIsLoggedIn(true)} />
  }

  const renderView = () => {
    switch (view) {
      case 'canon':    return <CodexTab theme={theme} />
      case 'diagrams': return <DiagramsTab theme={theme} />
      case 'todo':     return <TodoTab theme={theme} />
      case 'kernel':   return <SysteemTab theme={theme} />
      case 'skills':   return <SkillsTab theme={theme} />
      default: return <Viewport view={view} theme={theme} setView={setView} />
    }
  }

  return (
    <div id="mcc-root" style={{display:'flex',flexDirection:'column',height:'100vh',background:t.bg,color:t.text,overflow:'hidden',position:'relative',fontSize:`${fontSize}px`}}>
      <style>{`
        * { box-sizing: border-box; }
        body, button, input, select, textarea { font-size: inherit; }
        p, span, div, label, li, td, th, a { font-size: inherit; }
        ::-webkit-scrollbar { width: 4px; height: 4px; }
        ::-webkit-scrollbar-track { background: transparent; }
        ::-webkit-scrollbar-thumb { background: ${t.accent}40; border-radius: 2px; }
        ::-webkit-scrollbar-thumb:hover { background: ${t.accent}70; }
        @keyframes mcc-fadein { from{opacity:0;transform:translateY(4px)} to{opacity:1;transform:translateY(0)} }
        @keyframes mcc-pulse { 0%,100%{opacity:1} 50%{opacity:0.3} }
        button { font-family: inherit; }
        input, textarea, select { font-family: inherit; }
      `}</style>

      <TopNav
        view={view}
        setView={setView}
        theme={theme}
        dropdownOpacity={dropdownOpacity}
        agentCount={agentCount}
        fontSize={fontSize}
        onOpenSettings={() => setSettingsOpen(s => !s)}
      />

      <div style={{flex:1,overflow:'auto',position:'relative'}}>
        <ErrorBoundary theme={theme}>
          {renderView()}
        </ErrorBoundary>
      </div>

      {settingsOpen && (
        <SettingsPanel
          theme={theme}
          themeName={themeName}
          setThemeName={setThemeNamePersist}
          fontSize={fontSize}
          setFontSize={setFontSizePersist}
          dropdownOpacity={dropdownOpacity}
          setDropdownOpacity={setDropdownOpacity}
          onClose={() => setSettingsOpen(false)}
        />
      )}
    </div>
  )
}
