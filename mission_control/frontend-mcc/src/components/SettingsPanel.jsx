import React from 'react'
import { THEMES } from '../themes'

export default function SettingsPanel({ theme, themeName, setThemeName, fontSize, setFontSize, onClose }) {
  const t = theme?.colors || {}
  const acc = t.accent || '#c9a84c'

  return (
    <div style={{
      position:'fixed', top:0, right:0, bottom:0, width:'300px',
      background:t.bgSecondary, borderLeft:`1px solid ${t.border}`,
      zIndex:1000, display:'flex', flexDirection:'column',
      boxShadow:'-8px 0 32px rgba(0,0,0,0.4)',
    }}>
      {/* Header */}
      <div style={{display:'flex',alignItems:'center',justifyContent:'space-between',padding:'16px',borderBottom:`1px solid ${t.border}`,flexShrink:0}}>
        <div style={{fontSize:'14px',fontWeight:'600',color:t.text,display:'flex',alignItems:'center',gap:'8px'}}>
          <i className="ti ti-palette" style={{color:acc}}/> Instellingen
        </div>
        <button onClick={onClose} style={{background:'transparent',border:`1px solid ${t.border}`,color:t.textMuted,cursor:'pointer',fontSize:'16px',padding:'4px 8px',borderRadius:'6px'}}>
          <i className="ti ti-x"/>
        </button>
      </div>

      <div style={{flex:1,overflow:'auto',padding:'16px',display:'flex',flexDirection:'column',gap:'20px'}}>

        {/* Font size */}
        <div>
          <div style={{fontSize:'10px',color:t.textMuted,letterSpacing:'0.1em',textTransform:'uppercase',marginBottom:'10px',fontWeight:'500'}}>Tekstgrootte</div>
          <div style={{display:'flex',alignItems:'center',gap:'10px'}}>
            <button onClick={()=>setFontSize(Math.max(11,fontSize-1))} style={{width:'32px',height:'32px',borderRadius:'7px',border:`1px solid ${t.border}`,background:t.bg,color:t.text,cursor:'pointer',fontSize:'16px',display:'flex',alignItems:'center',justifyContent:'center'}}>−</button>
            <div style={{flex:1,textAlign:'center'}}>
              <div style={{fontSize:'22px',fontWeight:'600',color:acc}}>{fontSize}</div>
              <div style={{fontSize:'9px',color:t.textMuted}}>pixels</div>
            </div>
            <button onClick={()=>setFontSize(Math.min(18,fontSize+1))} style={{width:'32px',height:'32px',borderRadius:'7px',border:`1px solid ${t.border}`,background:t.bg,color:t.text,cursor:'pointer',fontSize:'16px',display:'flex',alignItems:'center',justifyContent:'center'}}>+</button>
          </div>
          <div style={{display:'flex',gap:'6px',marginTop:'8px'}}>
            {[11,12,13,14,15,16].map(s => (
              <button key={s} onClick={()=>setFontSize(s)} style={{flex:1,padding:'4px',borderRadius:'5px',fontSize:'10px',cursor:'pointer',border:`1px solid ${fontSize===s?acc+'60':t.border}`,background:fontSize===s?`${acc}20`:t.bg,color:fontSize===s?acc:t.textMuted}}>{s}</button>
            ))}
          </div>
        </div>

        {/* Thema */}
        <div>
          <div style={{fontSize:'10px',color:t.textMuted,letterSpacing:'0.1em',textTransform:'uppercase',marginBottom:'10px',fontWeight:'500'}}>Thema</div>
          <div style={{display:'flex',flexDirection:'column',gap:'6px'}}>
            {Object.entries(THEMES).map(([key, th]) => {
              const isActive = themeName === key
              return (
                <button key={key} onClick={()=>setThemeName(key)} style={{
                  display:'flex', alignItems:'center', gap:'12px',
                  padding:'10px 12px', borderRadius:'10px', cursor:'pointer',
                  border:`1.5px solid ${isActive ? th.colors.accent : t.border}`,
                  background: isActive ? `${th.colors.accent}18` : t.bg,
                  transition:'all .15s', textAlign:'left',
                }}>
                  {/* Preview */}
                  <div style={{width:'44px',height:'28px',borderRadius:'6px',background:th.colors.bg,border:`1px solid ${th.colors.border}`,flexShrink:0,overflow:'hidden',position:'relative'}}>
                    <div style={{position:'absolute',top:'4px',left:'4px',right:'4px',height:'4px',borderRadius:'2px',background:th.colors.bgSecondary}}/>
                    <div style={{position:'absolute',top:'12px',left:'4px',width:'12px',height:'3px',borderRadius:'2px',background:th.colors.accent}}/>
                    <div style={{position:'absolute',top:'12px',left:'20px',width:'8px',height:'3px',borderRadius:'2px',background:th.colors.bgTertiary}}/>
                    <div style={{position:'absolute',bottom:'4px',left:'4px',width:'20px',height:'8px',borderRadius:'3px',background:`${th.colors.accent}40`}}/>
                  </div>
                  <div style={{flex:1}}>
                    <div style={{fontSize:'12px',fontWeight:isActive?'600':'400',color:isActive?th.colors.accent:t.text}}>{th.name}</div>
                    <div style={{fontSize:'9px',color:t.textMuted,marginTop:'1px'}}>{th.mode === 'dark' ? '🌙 Dark mode' : '☀️ Light mode'}</div>
                  </div>
                  {isActive && <i className="ti ti-check" style={{color:th.colors.accent,fontSize:'14px',flexShrink:0}}/>}
                </button>
              )
            })}
          </div>
        </div>
      </div>
    </div>
  )
}
