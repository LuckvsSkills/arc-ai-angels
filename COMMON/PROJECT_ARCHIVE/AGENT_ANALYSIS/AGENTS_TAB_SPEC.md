## GRID LAYOUT
- **4 agents per row** (repeat(4, 1fr))
- **Gap: 20px** between cards
- **Card height: auto** (minmax(420px, auto))
- **All 34 agents visible** (scrollable page)

---

## NEW OMNI STRUCTURE & DOMAINS

### OMNI LEAD 1: CORTEXIA → HELIX DOMAIN
**Omni Name:** `Cortexia`
**Domain Display:** `Tech`
**Agents:**
- Nero → "Security Sentinel" / "risicoanalyse, security" / **Cortexia / Tech**
- Forge → "Engineering Sentinel" / "code, builds, implementatie" / **Cortexia / Tech**
- Axon → "Automation Sentinel" / "workflows, scripts, pipelines" / **Cortexia / Tech**
- Ventura → "Infrastructure Sentinel" / "infra, runtime, deployment" / **Cortexia / Tech**
- Clio → "Documentation Sentinel" / "documentatie, structuur, overdracht" / **Cortexia / Tech**
- Helix → "Tech Domain Lead Sentinel" / "technische taakuitvoering" / **Cortexia / Tech**

### OMNI LEAD 2: SAELIA → MATRIX DOMAIN
**Omni Name:** `Saelia`
**Domain Display:** `Data/AI`
**Agents:**
- Arix → "Data Analysis Sentinel" / "data-analyse" / **Saelia / Data/AI**
- Daxio → "Data Processing Sentinel" / "data pipelines" / **Saelia / Data/AI**
- Enki → "Knowledge Sentinel" / "kennisstructuren" / **Saelia / Data/AI**
- Sora → "AI Sentinel" / "AI-modellen en logica" / **Saelia / Data/AI**
- Tharos → "Monitoring Sentinel" / "observability & tracking" / **Saelia / Data/AI**
- Matrix → "Data/AI Domain Lead Sentinel" / "data- en AI-taakuitvoering" / **Saelia / Data/AI**

### OMNI LEAD 3: LUMERIA → QUANTIX DOMAIN
**Omni Name:** `Lumeria`
**Domain Display:** `Logic`
**Agents:**
- Elora → "Logic Sentinel" / "logische analyse" / **Lumeria / Logic**
- Kresta → "Structure Sentinel" / "systeemstructuur" / **Lumeria / Logic**
- Luvia → "Flow Sentinel" / "proceslogica" / **Lumeria / Logic**
- Nura → "Reasoning Sentinel" / "redenering, optimalisatie" / **Lumeria / Logic**
- Vondra → "Optimization Sentinel" / "optimalisatie" / **Lumeria / Logic**
- Quantix → "Logic Domain Lead Sentinel" / "logica- en systeemtaakuitvoering" / **Lumeria / Logic**

### OMNI LEAD 4: FLUENTIA → ZENIX DOMAIN
**Omni Name:** `Fluentia`
**Domain Display:** `Creative`
**Agents:**
- Draven → "Writing Sentinel" / "tekstproductie" / **Fluentia / Creative**
- Orizon → "Visual Sentinel" / "visueel denken, design" / **Fluentia / Creative**
- Solis → "Branding Sentinel" / "branding" / **Fluentia / Creative**
- Unia → "Story Sentinel" / "storytelling" / **Fluentia / Creative**
- Zena → "Polish Sentinel" / "afwerking, refinement" / **Fluentia / Creative**
- Zenix → "Creative Domain Lead Sentinel" / "creatieve output, communicatie" / **Fluentia / Creative**

### OMNI LEAD 5: FINORIA → FINIX DOMAIN
**Omni Name:** `Finoria`
**Domain Display:** `Finance`
**Agents:**
- Kairo → "Analysis Sentinel" / "financiële analyse" / **Finoria / Finance**
- Kenzo → "Strategy Sentinel" / "financiële strategie" / **Finoria / Finance**
- Odis → "Operations Sentinel" / "financiële processen" / **Finoria / Finance**
- Vector → "Modeling Sentinel" / "financiële modellen" / **Finoria / Finance**
- Zion → "Risk Sentinel" / "risicoanalyse" / **Finoria / Finance**
- Finix → "Finance Domain Lead Sentinel" / "financiële taakuitvoering" / **Finoria / Finance**

---

## CORE LAYER AGENTS
- **Nova** → "First-Line Operator" / "intake, filtering, normalisatie" / **Openclaw / intake**
- **Flux** → "Central Orchestrator" / "routing, sequencing, governance" / **Brain / system**
- **Flux-Core** → "Deep Thinking Orchestrator" / "complex routing, deep analysis" / **Brain / system**
- **Main** → "System Core" / "system coordination" / **System / core**

---

## COLOR SCHEME PER AGENT

### Eye Colors (voor Omni/Domain text kleur)
- Cortexia agents: **Cyan** (#00d4ff)
- Saelia agents: **Purple** (#7c3aed)
- Lumeria agents: **Pink** (#ec4899)
- Fluentia agents: **Orange** (#f97316)
- Finoria agents: **Yellow** (#fbbf24)
- Nova: **Green** (#00ff88)
- Flux/Flux-Core: **Gold** (#ffd700)
- Main: **Cyan** (#00d4ff)

### Card Background (subtle)
- Uses agent's bodyColor with 0.3 opacity

---

## TEXT HIERARCHY
1. **Agent Name** → 14px, bold (600), white, centered
2. **Role** → 11px, bold (600), GLOW COLOR, centered
3. **Function** → 11px, bold (600), white, centered
4. **Omni / Domain** → 11px, bold (600), AGENT EYE COLOR, centered

---

## IMPLEMENTATION CHECKLIST
- agent_canon_mapping.json has ALL 34 agents with `omni` + `domain` fields
- AgentsView.jsx fetches from `/api/openclaw/agents`
- Agent data merges with AGENT_CANON
- Card displays: Name → Role → Function → Omni/Domain
- Eye color used for Omni/Domain text
- 3D rendering intact (THREE.js)
- Model dropdown works
- 4 per row grid
- All 34 agents visible
- Tested in Firefox

