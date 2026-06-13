import React, { useState } from 'react'

export default function LoginPage({ onLogin }) {
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleLogin = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError('')
    try {
      const r = await fetch('/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ password })
      })
      const d = await r.json()
      if (r.ok && d.ok) {
        onLogin()
      } else {
        setError('Ongeldig wachtwoord')
      }
    } catch {
      setError('Verbinding mislukt')
    }
    setLoading(false)
  }

  return (
    <div style={{ minHeight:'100vh', display:'flex', alignItems:'center', justifyContent:'center', background:'#0e1320' }}>
      <div style={{ textAlign:'center', padding:'40px', width:'100%', maxWidth:'360px' }}>
        <div style={{ fontSize:'48px', marginBottom:'16px' }}>🤖</div>
        <h1 style={{ color:'#c9a84c', fontSize:'22px', fontWeight:'700', marginBottom:'4px', letterSpacing:'-0.02em' }}>ARC AI AGENTS</h1>
        <p style={{ color:'#5a6a8a', fontSize:'11px', marginBottom:'32px', letterSpacing:'0.15em', textTransform:'uppercase' }}>Mission Control Center</p>

        <form onSubmit={handleLogin} style={{ display:'flex', flexDirection:'column', gap:'12px' }}>
          <input
            type="password"
            value={password}
            onChange={e => setPassword(e.target.value)}
            placeholder="Wachtwoord"
            autoFocus
            style={{
              padding:'12px 16px', borderRadius:'10px',
              background:'#ffffff08', border:'1px solid #c9a84c30',
              color:'#e2e8f0', fontSize:'14px', outline:'none',
              textAlign:'center', letterSpacing:'0.1em',
            }}
          />
          {error && <div style={{ fontSize:'11px', color:'#ef4444' }}>{error}</div>}
          <button type="submit" disabled={loading || !password} style={{
            padding:'12px 32px', borderRadius:'10px',
            background: loading ? '#c9a84c10' : '#c9a84c20',
            border:'1px solid #c9a84c60',
            color:'#c9a84c', fontSize:'13px', fontWeight:'700',
            cursor: loading ? 'not-allowed' : 'pointer',
            letterSpacing:'0.05em',
          }}>
            {loading ? '⏳ Laden...' : '🔐 Inloggen'}
          </button>
        </form>
      </div>
    </div>
  )
}
