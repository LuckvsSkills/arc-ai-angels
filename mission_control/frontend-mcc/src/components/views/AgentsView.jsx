import React, { useState, useEffect, useRef } from 'react'
import * as THREE from 'three'

const AGENTS = [
  { id:'nova',     name:'Nova',     role:'Gateway',       layer:'gateway',      domain:'core',    color:'#c9a84c' },
  { id:'flux',     name:'Flux',     role:'Orchestrator',  layer:'orchestrator', domain:'core',    color:'#c9a84c' },
  { id:'cortexia', name:'Cortexia', role:'Omni Lead',     layer:'lead',         domain:'helix',   color:'#38bdf8' },
  { id:'nero',     name:'Nero',     role:'Security',      layer:'sentinel',     domain:'helix',   color:'#38bdf8' },
  { id:'forge',    name:'Forge',    role:'Engineering',   layer:'sentinel',     domain:'helix',   color:'#38bdf8' },
  { id:'axon',     name:'Axon',     role:'Automation',    layer:'sentinel',     domain:'helix',   color:'#38bdf8' },
  { id:'ventura',  name:'Ventura',  role:'Infrastructure',layer:'sentinel',     domain:'helix',   color:'#38bdf8' },
  { id:'clio',     name:'Clio',     role:'Documentation', layer:'sentinel',     domain:'helix',   color:'#38bdf8' },
  { id:'finoria',  name:'Finoria',  role:'Omni Lead',     layer:'lead',         domain:'finix',   color:'#f472b6' },
  { id:'kairo',    name:'Kairo',    role:'Finance Ops',   layer:'sentinel',     domain:'finix',   color:'#f472b6' },
  { id:'kenzo',    name:'Kenzo',    role:'Modeling',      layer:'sentinel',     domain:'finix',   color:'#f472b6' },
  { id:'odis',     name:'Odis',     role:'Data',          layer:'sentinel',     domain:'finix',   color:'#f472b6' },
  { id:'vector',   name:'Vector',   role:'Analytics',     layer:'sentinel',     domain:'finix',   color:'#f472b6' },
  { id:'zion',     name:'Zion',     role:'Risk',          layer:'sentinel',     domain:'finix',   color:'#f472b6' },
  { id:'saelia',   name:'Saelia',   role:'Omni Lead',     layer:'lead',         domain:'matrix',  color:'#34d399' },
  { id:'arix',     name:'Arix',     role:'Structure',     layer:'sentinel',     domain:'matrix',  color:'#34d399' },
  { id:'daxio',    name:'Daxio',    role:'Processing',    layer:'sentinel',     domain:'matrix',  color:'#34d399' },
  { id:'enki',     name:'Enki',     role:'Logic',         layer:'sentinel',     domain:'matrix',  color:'#34d399' },
  { id:'sora',     name:'Sora',     role:'AI',            layer:'sentinel',     domain:'matrix',  color:'#34d399' },
  { id:'tharos',   name:'Tharos',   role:'Knowledge',     layer:'sentinel',     domain:'matrix',  color:'#34d399' },
  { id:'lumeria',  name:'Lumeria',  role:'Omni Lead',     layer:'lead',         domain:'quantix', color:'#a78bfa' },
  { id:'elora',    name:'Elora',    role:'Analysis',      layer:'sentinel',     domain:'quantix', color:'#a78bfa' },
  { id:'kresta',   name:'Kresta',   role:'Strategy',      layer:'sentinel',     domain:'quantix', color:'#a78bfa' },
  { id:'luvia',    name:'Luvia',    role:'Modeling',      layer:'sentinel',     domain:'quantix', color:'#a78bfa' },
  { id:'nura',     name:'Nura',     role:'Optimization',  layer:'sentinel',     domain:'quantix', color:'#a78bfa' },
  { id:'vondra',   name:'Vondra',   role:'Monitoring',    layer:'sentinel',     domain:'quantix', color:'#a78bfa' },
  { id:'fluentia', name:'Fluentia', role:'Omni Lead',     layer:'lead',         domain:'zenix',   color:'#fb923c' },
  { id:'draven',   name:'Draven',   role:'Flow',          layer:'sentinel',     domain:'zenix',   color:'#fb923c' },
  { id:'orizon',   name:'Orizon',   role:'Reasoning',     layer:'sentinel',     domain:'zenix',   color:'#fb923c' },
  { id:'solis',    name:'Solis',    role:'Operations',    layer:'sentinel',     domain:'zenix',   color:'#fb923c' },
  { id:'unia',     name:'Unia',     role:'Polish',        layer:'sentinel',     domain:'zenix',   color:'#fb923c' },
  { id:'zena',     name:'Zena',     role:'Branding',      layer:'sentinel',     domain:'zenix',   color:'#fb923c' },
]

const SHAPES = ['sphere','box','octahedron','tetrahedron','cone','dodecahedron','cylinder','torus','icosahedron']

// WebGL context manager — max 8 tegelijk
const activeRenderers = new Set()
const MAX_RENDERERS = 12
const pendingQueue = []

function requestRenderer(id, callback) {
  if (activeRenderers.size < MAX_RENDERERS) {
    activeRenderers.add(id)
    callback(true)
  } else {
    pendingQueue.push({ id, callback })
  }
}

function releaseRenderer(id) {
  activeRenderers.delete(id)
  if (pendingQueue.length > 0) {
    const next = pendingQueue.shift()
    activeRenderers.add(next.id)
    next.callback(true)
  }
}

function useAgentPrefs(id) {
  const key = `agent_custom_${id}`
  const load = () => { try { return JSON.parse(localStorage.getItem(key)||'null') } catch { return null } }
  const [prefs, setPrefs] = useState(load)
  const save = (p) => { setPrefs(p); try { localStorage.setItem(key, JSON.stringify(p)) } catch {} }
  return [prefs, save]
}

const KERN_STYLES = ['metallic','chrome','crystal','plasma','matte','hologram']
const EYE_STYLES  = ['scanner','hex','diamond','visor','orb','cross']

function AgentCanvas({ color, glowColor, eyeColor, shape, kernStyle, eyeStyle, agentIndex = 99, rotDir = -1 }) {
  const mountRef = useRef(null)
  const stateRef = useRef({ animId:null, mouseX:0, mouseY:0, hovering:false, returning:false, rotY:0, rotX:0, velY:0.03, velX:0 })

  useEffect(() => {
    const el = mountRef.current
    if (!el) return
    const W = 180, H = 180
    const s = stateRef.current
    s.rotY=0; s.rotX=0; s.velY=0; s.velX=0; s.rotDir=rotDir

    let granted = false
    const renderId = color + shape + kernStyle
    requestRenderer(renderId, (ok) => { granted = ok })
    if (!granted) return

    const scene = new THREE.Scene()
    const camera = new THREE.PerspectiveCamera(42,1,0.1,100)
    camera.position.z = 3.5

    let renderer
    try {
      renderer = new THREE.WebGLRenderer({ antialias:true, alpha:true })
      renderer.setSize(W,H)
      renderer.setPixelRatio(Math.min(window.devicePixelRatio,2))
      renderer.setClearColor(0x000000,0)
      el.appendChild(renderer.domElement)
    } catch { return }

    const kc = new THREE.Color(color)
    const gc = new THREE.Color(glowColor)
    const ec = new THREE.Color(eyeColor)

    // Verlichting
    scene.add(new THREE.AmbientLight(0x223344, 0.8))
    const kl = new THREE.DirectionalLight(0xffffff, 2.2); kl.position.set(3,4,3); scene.add(kl)
    const fl = new THREE.PointLight(gc, 2.2, 10); fl.position.set(-2,0,2); scene.add(fl)
    const rl = new THREE.DirectionalLight(gc, 1.0); rl.position.set(-2,1,-2); scene.add(rl)

    // KERN GEOMETRIE
    let geo
    switch(shape) {
      case 'box':          geo = new THREE.BoxGeometry(1.3,1.3,1.3); break
      case 'octahedron':   geo = new THREE.OctahedronGeometry(1.05); break
      case 'tetrahedron':  geo = new THREE.TetrahedronGeometry(1.15); break
      case 'cone':         geo = new THREE.ConeGeometry(0.8,1.5,8); break
      case 'dodecahedron': geo = new THREE.DodecahedronGeometry(1.0); break
      case 'cylinder':     geo = new THREE.CylinderGeometry(0.7,0.7,1.3,10); break
      case 'torus':        geo = new THREE.TorusGeometry(0.8,0.32,12,24); break
      case 'icosahedron':  geo = new THREE.IcosahedronGeometry(1.0); break
      default:             geo = new THREE.SphereGeometry(1.05,32,32)
    }

    // KERN MATERIAAL per stijl
    let mat
    switch(kernStyle) {
      case 'chrome':
        mat = new THREE.MeshPhongMaterial({ color:0xaaaaaa, shininess:300, specular:new THREE.Color(0xffffff), emissive:kc, emissiveIntensity:0.1 }); break
      case 'crystal':
        mat = new THREE.MeshPhongMaterial({ color:kc, shininess:250, specular:new THREE.Color(0xffffff), transparent:true, opacity:0.75, emissive:kc, emissiveIntensity:0.25 }); break
      case 'plasma':
        mat = new THREE.MeshPhongMaterial({ color:kc, shininess:50, emissive:kc, emissiveIntensity:0.5 }); break
      case 'matte':
        mat = new THREE.MeshPhongMaterial({ color:kc, shininess:15, emissive:kc, emissiveIntensity:0.08 }); break
      case 'hologram':
        mat = new THREE.MeshPhongMaterial({ color:kc, shininess:200, specular:new THREE.Color(0xffffff), transparent:true, opacity:0.5, wireframe:false, emissive:kc, emissiveIntensity:0.4 }); break
      default: // metallic
        mat = new THREE.MeshPhongMaterial({ color:kc, shininess:200, specular:new THREE.Color(0xffffff), emissive:kc, emissiveIntensity:0.18 })
    }
    const mesh = new THREE.Mesh(geo, mat)
    scene.add(mesh)

    // TWEEDE WIREFRAME LAAG
    const wire2Geo = geo.clone()
    const wire2Mat = new THREE.MeshBasicMaterial({ color:gc, wireframe:true, transparent:true, opacity:0.08 })
    const wire2 = new THREE.Mesh(wire2Geo, wire2Mat)
    mesh.add(wire2)

    // OUTER GLOW SPHERE
    const outerGeo = new THREE.SphereGeometry(1.6,28,28)
    const outerMat = new THREE.MeshBasicMaterial({ color:gc, transparent:true, opacity:0.08, side:THREE.BackSide })
    const outer = new THREE.Mesh(outerGeo, outerMat)
    scene.add(outer)

    // ENERGIE WIREFRAME
    const wireGeo = new THREE.IcosahedronGeometry(1.46,1)
    const wireMat = new THREE.MeshBasicMaterial({ color:gc, wireframe:true, transparent:true, opacity:0.14 })
    const wire = new THREE.Mesh(wireGeo, wireMat)
    scene.add(wire)

    // OOG SYSTEEM
    const buildEye = (xPos) => {
      const g = new THREE.Group()
      g.position.set(xPos, 0.18, 0)

      switch(eyeStyle) {
        case 'hex': {
          // Hexagonaal oog
          const hGeo = new THREE.CylinderGeometry(0.14,0.14,0.06,6)
          const hMat = new THREE.MeshBasicMaterial({ color:0x111122 })
          const hex = new THREE.Mesh(hGeo, hMat)
          hex.rotation.x = Math.PI/2
          hex.position.z = 0.9
          mesh.add(hex)
          const hRimGeo = new THREE.TorusGeometry(0.14,0.025,6,6)
          const hRimMat = new THREE.MeshBasicMaterial({ color:ec })
          const hRim = new THREE.Mesh(hRimGeo, hRimMat)
          hRim.position.set(xPos,0.18,0.95)
          mesh.add(hRim)
          const hGlowGeo = new THREE.SphereGeometry(0.07,8,8)
          const hGlowMat = new THREE.MeshBasicMaterial({ color:ec })
          const hGlow = new THREE.Mesh(hGlowGeo, hGlowMat)
          hGlow.position.set(xPos,0.18,1.0)
          mesh.add(hGlow)
          return { rimMat: hRimMat, glowMat: hGlowMat, rimMesh: hRim }
        }
        case 'visor': {
          // Visor — brede band
          const vGeo = new THREE.BoxGeometry(0.3,0.1,0.05)
          const vMat = new THREE.MeshBasicMaterial({ color:0x000520 })
          const visor = new THREE.Mesh(vGeo, vMat)
          visor.position.set(xPos,0.18,0.92)
          mesh.add(visor)
          const vGlowGeo = new THREE.BoxGeometry(0.26,0.06,0.02)
          const vGlowMat = new THREE.MeshBasicMaterial({ color:ec, transparent:true, opacity:0.9 })
          const vGlow = new THREE.Mesh(vGlowGeo, vGlowMat)
          vGlow.position.set(xPos,0.18,0.96)
          mesh.add(vGlow)
          return { glowMat: vGlowMat }
        }
        case 'orb': {
          // Grote energie orb
          const oGeo = new THREE.SphereGeometry(0.18,16,16)
          const oMat = new THREE.MeshBasicMaterial({ color:ec, transparent:true, opacity:0.9 })
          const orb = new THREE.Mesh(oGeo, oMat)
          orb.position.set(xPos,0.18,0.88)
          mesh.add(orb)
          const oRingGeo = new THREE.TorusGeometry(0.2,0.02,6,20)
          const oRingMat = new THREE.MeshBasicMaterial({ color:ec, transparent:true, opacity:0.6 })
          const oRing = new THREE.Mesh(oRingGeo, oRingMat)
          oRing.position.set(xPos,0.18,0.88)
          mesh.add(oRing)
          return { glowMat: oMat, rimMat: oRingMat, rimMesh: oRing }
        }
        case 'cross': {
          // Kruis oog — militaristisch
          const cH = new THREE.BoxGeometry(0.3,0.04,0.04)
          const cV = new THREE.BoxGeometry(0.04,0.3,0.04)
          const cMat = new THREE.MeshBasicMaterial({ color:ec })
          const ch = new THREE.Mesh(cH, cMat)
          const cv = new THREE.Mesh(cV, cMat)
          ch.position.set(xPos,0.18,0.94)
          cv.position.set(xPos,0.18,0.94)
          mesh.add(ch); mesh.add(cv)
          return { glowMat: cMat }
        }
        default: { // AI scanner — futuristisch
          // Socket — donkere verdieping
          const sGeo = new THREE.CylinderGeometry(0.15,0.15,0.04,16)
          const sMat = new THREE.MeshBasicMaterial({ color:0x000008 })
          const sock = new THREE.Mesh(sGeo, sMat)
          sock.rotation.x = Math.PI/2
          sock.position.set(xPos,0.18,0.88)
          mesh.add(sock)
          // Buitenste ring — groot
          const r1Geo = new THREE.TorusGeometry(0.14,0.018,6,24)
          const r1Mat = new THREE.MeshBasicMaterial({ color:ec, transparent:true, opacity:0.5 })
          const r1 = new THREE.Mesh(r1Geo, r1Mat)
          r1.position.set(xPos,0.18,0.92)
          mesh.add(r1)
          // Middelste ring
          const r2Geo = new THREE.TorusGeometry(0.09,0.022,6,20)
          const r2Mat = new THREE.MeshBasicMaterial({ color:ec, transparent:true, opacity:0.85 })
          const r2 = new THREE.Mesh(r2Geo, r2Mat)
          r2.position.set(xPos,0.18,0.96)
          mesh.add(r2)
          // Kern punt — fel gloeiend
          const cGeo = new THREE.SphereGeometry(0.055,10,10)
          const cMat = new THREE.MeshBasicMaterial({ color:ec })
          const core = new THREE.Mesh(cGeo, cMat)
          core.position.set(xPos,0.18,1.01)
          mesh.add(core)
          // Kruis scan lijnen
          const hGeo = new THREE.BoxGeometry(0.28,0.008,0.008)
          const vGeo = new THREE.BoxGeometry(0.008,0.28,0.008)
          const crossMat = new THREE.MeshBasicMaterial({ color:ec, transparent:true, opacity:0.35 })
          const hLine = new THREE.Mesh(hGeo, crossMat)
          const vLine = new THREE.Mesh(vGeo, crossMat)
          hLine.position.set(xPos,0.18,0.93)
          vLine.position.set(xPos,0.18,0.93)
          mesh.add(hLine); mesh.add(vLine)
          return { irisMat: r2Mat, rimMesh: r1, glowMat: cMat, r1Mat }
        }
      }
    }

    const eyeDataL = buildEye(-0.31)
    const eyeDataR = buildEye( 0.31)

    // Scan lijn
    const scanGeo = new THREE.BoxGeometry(0.7,0.01,0.01)
    const scanMat = new THREE.MeshBasicMaterial({ color:ec, transparent:true, opacity:0.8 })
    const scan = new THREE.Mesh(scanGeo, scanMat)
    scan.position.set(0,0.05,0.94)
    mesh.add(scan)

    let frame = 0
    const animate = () => {
      s.animId = requestAnimationFrame(animate)
      frame++

      if (s.hovering) {
        s.velY += (s.mouseX * 0.055 - s.velY) * 0.12
        s.velX += (-s.mouseY * 0.04 - s.velX) * 0.12
        s.rotY += s.velY
        s.rotX += s.velX
        s.rotX = Math.max(-0.7, Math.min(0.7, s.rotX))
      } else if (s.returning) {
        s.rotY *= 0.85
        s.rotX *= 0.85
        if (Math.abs(s.rotY)<0.01 && Math.abs(s.rotX)<0.01) {
          s.rotY=0; s.rotX=0; s.returning=false
        }
      } else {
        if (s.rotDir === 0) { s.rotX -= 0.03 }
        else if (s.rotDir === 2) { s.rotX += 0.03 }
        else if (s.rotDir === 3) { s.rotY += 0.03 }
        else { s.rotY -= 0.03 }
      }

      mesh.rotation.y = s.rotY
      mesh.rotation.x = s.rotX
      wire.rotation.y = -s.rotY * 0.22
      wire.rotation.x = s.rotX * 0.4

      outerMat.opacity = 0.07 + Math.sin(frame*0.028)*0.04
      outer.scale.setScalar(1 + Math.sin(frame*0.028)*0.014)

      if (eyeDataL?.irisMat) {
        eyeDataL.irisMat.opacity = 0.7 + Math.sin(frame*0.06)*0.3
        eyeDataR.irisMat.opacity = 0.7 + Math.sin(frame*0.06)*0.3
      }
      if (eyeDataL?.r1Mat) {
        eyeDataL.r1Mat.opacity = 0.3 + Math.sin(frame*0.04+1)*0.2
        eyeDataR.r1Mat.opacity = 0.3 + Math.sin(frame*0.04+1)*0.2
      }
      if (eyeDataL?.rimMesh) { eyeDataL.rimMesh.rotation.z = frame*0.04; eyeDataR.rimMesh.rotation.z = -frame*0.04 }
      if (eyeDataL?.glowMat) eyeDataL.glowMat.opacity = 0.7 + Math.sin(frame*0.08)*0.25
      if (eyeDataR?.glowMat) eyeDataR.glowMat.opacity = 0.7 + Math.sin(frame*0.08)*0.25

      scan.position.y = Math.sin(frame*0.06)*0.15
      scanMat.opacity = 0.4 + Math.sin(frame*0.1)*0.4
      mat.emissiveIntensity = 0.15 + Math.sin(frame*0.032)*0.1

      renderer.render(scene, camera)
    }
    animate()

    const onMove = (e) => { const r=el.getBoundingClientRect(); s.mouseX=((e.clientX-r.left)/W-0.5)*2; s.mouseY=-((e.clientY-r.top)/H-0.5)*2 }
    const onTouch = (e) => { e.preventDefault(); const t=e.touches[0]; const r=el.getBoundingClientRect(); s.mouseX=((t.clientX-r.left)/W-0.5)*2; s.mouseY=-((t.clientY-r.top)/H-0.5)*2 }
    const onEnter = () => { s.returning=true }  // eerst terug naar voorzijde
    const onStartControl = () => { s.hovering=true; s.returning=false }  // dan sturen
    const onLeave = () => { s.hovering=false; s.returning=false }  // gewoon door draaien
    let controlTimer = null
    const onMouseEnter = () => {
      s.returning=true
      clearTimeout(controlTimer)
      controlTimer = setTimeout(() => { s.hovering=true; s.returning=false }, 400)
    }
    const onMouseLeave = () => {
      clearTimeout(controlTimer)
      s.hovering=false; s.returning=false
    }
    const onTouchStart = () => {
      s.returning=true
      clearTimeout(controlTimer)
      controlTimer = setTimeout(() => { s.hovering=true; s.returning=false }, 400)
    }
    const onTouchEnd = () => {
      clearTimeout(controlTimer)
      s.hovering=false; s.returning=false
    }
    el.addEventListener('mousemove',onMove)
    el.addEventListener('mouseenter',onMouseEnter)
    el.addEventListener('mouseleave',onMouseLeave)
    el.addEventListener('touchstart',onTouchStart,{passive:true})
    el.addEventListener('touchmove',onTouch,{passive:false})
    el.addEventListener('touchend',onTouchEnd,{passive:true})

    return () => {
      cancelAnimationFrame(s.animId)
      clearTimeout(controlTimer)
      el.removeEventListener('mousemove',onMove)
      el.removeEventListener('mouseenter',onMouseEnter)
      el.removeEventListener('mouseleave',onMouseLeave)
      el.removeEventListener('touchstart',onTouchStart)
      el.removeEventListener('touchmove',onTouch)
      el.removeEventListener('touchend',onTouchEnd)
      renderer.dispose(); renderer.renderLists.dispose(); scene.clear()
      if (el.contains(renderer.domElement)) el.removeChild(renderer.domElement)
      releaseRenderer(color + shape + kernStyle)
    }
  }, [color, glowColor, eyeColor, shape, kernStyle, eyeStyle])
  const [shouldRender, setShouldRender] = React.useState(agentIndex < 6)
  useEffect(() => {
    if (agentIndex < 6) return
    const timer = setTimeout(() => setShouldRender(true), (agentIndex - 5) * 150)
    return () => clearTimeout(timer)
  }, [agentIndex])
  return (
    <div style={{width:'180px',height:'180px',flexShrink:0,cursor:'crosshair',position:'relative'}}>
      {shouldRender
        ? <div ref={mountRef} style={{width:'180px',height:'180px'}}/>
        : <div style={{width:'180px',height:'180px',display:'flex',alignItems:'center',justifyContent:'center'}}>
            <div style={{width:'80px',height:'80px',borderRadius:'50%',background:`radial-gradient(circle at 35% 30%, ${color}60, ${color}20)`,border:`2px solid ${color}40`,boxShadow:`0 0 15px ${glowColor}30`}}/>
          </div>
      }
    </div>
  )
}

function ColorPick({ label, value, onChange, t }) {
  return (
    <div style={{display:'flex',alignItems:'center',gap:'8px',marginBottom:'6px'}}>
      <span style={{fontSize:'10px',color:t.textMuted,width:'60px',flexShrink:0}}>{label}</span>
      <input type="color" value={value} onChange={e=>onChange(e.target.value)}
        style={{width:'32px',height:'22px',padding:'0',border:`1px solid ${t.border}`,borderRadius:'4px',cursor:'pointer',background:'transparent'}}/>
      <span style={{fontSize:'9px',color:t.textMuted}}>{value}</span>
    </div>
  )
}

function AgentCard({ agent, theme, isSelected, onClick, agentIndex }) {
  const t = theme?.colors || {}
  const [prefs, savePrefs] = useAgentPrefs(agent.id)
  const [showEditor, setShowEditor] = useState(false)
  const isLead = agent.layer === 'lead' || agent.layer === 'gateway' || agent.layer === 'orchestrator'

  const shape     = prefs?.shape      || (isLead ? 'octahedron' : 'sphere')
  const rotDir     = prefs?.rotDir !== undefined ? Number(prefs.rotDir) : -1
  const kernColor = prefs?.body       || agent.color
  const glowColor = prefs?.glow       || agent.color
  const eyeColor  = prefs?.eye        || '#ffffff'
  const kernStyle = prefs?.kernStyle  || 'metallic'
  const eyeStyle  = prefs?.eyeStyle   || 'scanner'

  const upd = (key, val) => savePrefs({ ...prefs, [key]: val })

  return (
    <div style={{
      background: isSelected ? `${agent.color}15` : t.bgSecondary,
      border: `1px solid ${isSelected ? kernColor+'70' : t.border}`,
      borderLeft: `3px solid ${isLead ? kernColor : kernColor+'70'}`,
      borderRadius: '12px', overflow: 'hidden', transition: 'all .2s',
    }}>
      <div onClick={onClick} style={{cursor:'pointer',padding:'14px 16px'}}>
        <div style={{display:'flex',alignItems:'flex-start',gap:'16px',flexWrap:'wrap'}}>
        <AgentCanvas color={kernColor} glowColor={glowColor} eyeColor={eyeColor} shape={shape} kernStyle={kernStyle} eyeStyle={eyeStyle} agentIndex={agentIndex} rotDir={rotDir}/>
        <div style={{flex:1,minWidth:'160px'}}>
          {/* Naam + status */}
          <div style={{display:'flex',alignItems:'center',gap:'8px',marginBottom:'6px'}}>
            <div style={{fontSize:'18px',fontWeight:isLead?'700':'600',color:isSelected?kernColor:t.text,letterSpacing:'0.01em'}}>{agent.name}</div>
            <div style={{display:'flex',alignItems:'center',gap:'4px',padding:'2px 7px',borderRadius:'10px',background:'#22c55e18',border:'1px solid #22c55e40'}}>
              <div style={{width:'5px',height:'5px',borderRadius:'50%',background:'#22c55e',boxShadow:'0 0 5px #22c55e'}}/>
              <span style={{fontSize:'9px',color:'#22c55e',fontWeight:'500'}}>online</span>
            </div>
          </div>
          {/* Rol */}
          <div style={{fontSize:'13px',color:kernColor,fontWeight:'500',marginBottom:'8px'}}>{agent.role}</div>
          {/* Domain + layer badges */}
          <div style={{display:'flex',gap:'6px',marginBottom:'12px',flexWrap:'wrap'}}>
            <span style={{fontSize:'10px',padding:'3px 8px',borderRadius:'6px',background:`${kernColor}18`,border:`1px solid ${kernColor}40`,color:kernColor,textTransform:'uppercase',letterSpacing:'0.06em'}}>{agent.domain}</span>
            <span style={{fontSize:'10px',padding:'3px 8px',borderRadius:'6px',background:`${t.border}`,border:`1px solid ${t.border}`,color:t.textSecondary,textTransform:'uppercase',letterSpacing:'0.06em'}}>{agent.layer}</span>
          </div>
          {/* Stats rij */}
          <div style={{display:'grid',gridTemplateColumns:'1fr 1fr',gap:'6px',marginBottom:'12px'}}>
            {[
              {l:'Domain',  v:agent.domain},
              {l:'Layer',   v:agent.layer},
              {l:'Status',  v:'active'},
              {l:'ID',      v:agent.id},
            ].map(x => (
              <div key={x.l} style={{background:t.bg,borderRadius:'6px',padding:'5px 8px'}}>
                <div style={{fontSize:'8px',color:t.textMuted,textTransform:'uppercase',letterSpacing:'0.08em',marginBottom:'2px'}}>{x.l}</div>
                <div style={{fontSize:'11px',color:t.textSecondary,fontWeight:'500'}}>{x.v}</div>
              </div>
            ))}
          </div>
          <button onClick={e=>{e.stopPropagation();setShowEditor(v=>!v)}} style={{fontSize:'10px',padding:'5px 12px',borderRadius:'6px',border:`1px solid ${kernColor}50`,background:showEditor?`${kernColor}20`:`${kernColor}10`,color:kernColor,cursor:'pointer',fontWeight:'500'}}>
            ✏️ {showEditor ? 'Sluiten' : 'Aanpassen'}
          </button>
        </div>
        </div>
      </div>

      {showEditor && (
        <div style={{borderTop:`1px solid ${t.border}`,padding:'12px 14px',background:t.bg}} onClick={e=>e.stopPropagation()}>

          {/* Kleuren */}
          <div style={{marginBottom:'10px'}}>
            <div style={{fontSize:'9px',color:t.textMuted,letterSpacing:'0.1em',textTransform:'uppercase',marginBottom:'8px'}}>Kleuren</div>
            <ColorPick label="Kern"   value={kernColor}  onChange={v=>upd('body',v)}  t={t}/>
            <ColorPick label="Glow"   value={glowColor}  onChange={v=>upd('glow',v)}  t={t}/>
            <ColorPick label="Ogen"   value={eyeColor}   onChange={v=>upd('eye',v)}   t={t}/>
          </div>

          {/* Rotatie richting */}
          <div style={{marginBottom:'10px'}}>
            <div style={{fontSize:'9px',color:t.textMuted,letterSpacing:'0.1em',textTransform:'uppercase',marginBottom:'6px'}}>Rotatie richting</div>
            <div style={{display:'grid',gridTemplateColumns:'1fr 1fr',gap:'5px'}}>
              {[[-1,'⟳ Rechts'],[3,'⟲ Links'],[0,'↑ Omhoog'],[2,'↓ Omlaag']].map(([dir,label]) => (
                <button key={dir} onClick={()=>upd('rotDir', Number(dir))} style={{
                  fontSize:'10px', padding:'6px 8px', borderRadius:'6px', cursor:'pointer',
                  border:`1px solid ${rotDir===Number(dir)?kernColor+'80':t.border}`,
                  background:rotDir===Number(dir)?`${kernColor}25`:t.bgSecondary,
                  color:rotDir===Number(dir)?kernColor:t.textMuted,
                  fontWeight:rotDir===Number(dir)?'500':'400',
                }}>{label}</button>
              ))}
            </div>
          </div>

          {/* Vorm */}
          <div style={{marginBottom:'10px'}}>
            <div style={{fontSize:'9px',color:t.textMuted,letterSpacing:'0.1em',textTransform:'uppercase',marginBottom:'6px'}}>Vorm</div>
            <div style={{display:'flex',flexWrap:'wrap',gap:'4px'}}>
              {SHAPES.map(sv => (
                <button key={sv} onClick={()=>upd('shape',sv)} style={{fontSize:'9px',padding:'2px 7px',borderRadius:'4px',border:`1px solid ${shape===sv?agent.color+'80':t.border}`,background:shape===sv?`${agent.color}20`:t.bgSecondary,color:shape===sv?agent.color:t.textMuted,cursor:'pointer'}}>
                  {sv}
                </button>
              ))}
            </div>
          </div>

          {/* Kern stijl */}
          <div style={{marginBottom:'10px'}}>
            <div style={{fontSize:'9px',color:t.textMuted,letterSpacing:'0.1em',textTransform:'uppercase',marginBottom:'6px'}}>Kern stijl</div>
            <div style={{display:'flex',flexWrap:'wrap',gap:'4px'}}>
              {KERN_STYLES.map(ks => (
                <button key={ks} onClick={()=>upd('kernStyle',ks)} style={{fontSize:'9px',padding:'2px 7px',borderRadius:'4px',border:`1px solid ${kernStyle===ks?agent.color+'80':t.border}`,background:kernStyle===ks?`${agent.color}20`:t.bgSecondary,color:kernStyle===ks?agent.color:t.textMuted,cursor:'pointer'}}>
                  {ks}
                </button>
              ))}
            </div>
          </div>

          {/* Oog stijl */}
          <div>
            <div style={{fontSize:'9px',color:t.textMuted,letterSpacing:'0.1em',textTransform:'uppercase',marginBottom:'6px'}}>Oog stijl</div>
            <div style={{display:'flex',flexWrap:'wrap',gap:'4px'}}>
              {EYE_STYLES.map(es => (
                <button key={es} onClick={()=>upd('eyeStyle',es)} style={{fontSize:'9px',padding:'2px 7px',borderRadius:'4px',border:`1px solid ${eyeStyle===es?agent.color+'80':t.border}`,background:eyeStyle===es?`${agent.color}20`:t.bgSecondary,color:eyeStyle===es?agent.color:t.textMuted,cursor:'pointer'}}>
                  {es}
                </button>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default function AgentsView({ theme }) {
  const t = theme?.colors || {}
  const acc = t.accent || '#c9a84c'
  const [selected, setSelected] = useState(null)
  const [filter, setFilter] = useState('all')
  const [search, setSearch] = useState('')
  const [winW, setWinW] = useState(window.innerWidth)
  const isMobile = winW < 768

  useEffect(() => {
    const h = () => setWinW(window.innerWidth)
    window.addEventListener('resize', h)
    return () => window.removeEventListener('resize', h)
  }, [])

  const filtered = AGENTS.filter(a => {
    if (filter !== 'all' && a.domain !== filter) return false
    if (search && !a.name.toLowerCase().includes(search.toLowerCase()) && !a.role.toLowerCase().includes(search.toLowerCase())) return false
    return true
  })

  return (
    <div style={{height:'100%',display:'flex',flexDirection:'column',overflow:'auto'}}>
      <div style={{padding:'12px 16px',borderBottom:`1px solid ${t.border}`,flexShrink:0}}>
        <div style={{display:'flex',alignItems:'center',justifyContent:'space-between',marginBottom:'10px',flexWrap:'wrap',gap:'8px'}}>
          <h2 style={{margin:0,fontSize:'16px',color:t.text,fontWeight:'500'}}>
            <i className="ti ti-robot" style={{marginRight:'8px',color:acc}} aria-hidden="true"/>
            Agents <span style={{fontSize:'12px',color:t.textMuted,fontWeight:'400'}}>— {filtered.length}/{AGENTS.length}</span>
          </h2>
          <input value={search} onChange={e=>setSearch(e.target.value)} placeholder="Zoeken..." style={{padding:'6px 10px',background:t.bgSecondary,border:`1px solid ${t.border}`,borderRadius:'6px',color:t.text,fontSize:'11px',width:'160px'}}/>
        </div>
        <div style={{display:'flex',gap:'6px',flexWrap:'wrap'}}>
          {['all','core','helix','finix','matrix','quantix','zenix'].map(d => (
            <button key={d} onClick={()=>setFilter(d)} style={{padding:'3px 10px',borderRadius:'6px',fontSize:'10px',cursor:'pointer',border:`1px solid ${filter===d?acc+'60':t.border}`,background:filter===d?`${acc}15`:'transparent',color:filter===d?acc:t.textMuted,textTransform:'capitalize'}}>
              {d}
            </button>
          ))}
        </div>
      </div>
      <div style={{flex:1,overflow:'visible',padding:'12px 16px'}}>
        <div style={{display:'grid',gridTemplateColumns:`repeat(auto-fill,minmax(${isMobile?'100%':'280px'},1fr))`,gap:'12px'}}>
          {filtered.map((agent, idx) => (
            <AgentCard key={agent.id} agent={agent} theme={theme} isSelected={selected?.id===agent.id} onClick={()=>setSelected(selected?.id===agent.id?null:agent)} agentIndex={idx}/>
          ))}
        </div>
      </div>
    </div>
  )
}
