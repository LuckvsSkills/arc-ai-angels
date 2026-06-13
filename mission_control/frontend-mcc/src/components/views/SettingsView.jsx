import React from 'react'
export default function SettingsView({ theme }) {
  const t = theme?.colors || {}
  return (
    <div style={{padding:'40px',color:t.textMuted||'#888',textAlign:'center',paddingTop:'80px'}}>
      <i className="ti ti-tools" style={{fontSize:'32px',marginBottom:'16px',display:'block'}} aria-hidden="true"/>
      <div style={{fontSize:'14px'}}>SettingsView — komt eraan</div>
    </div>
  )
}
