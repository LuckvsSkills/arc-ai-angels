import React, { useState } from 'react'

const DC = { core:'#c9a84c', helix:'#38bdf8', finix:'#f472b6', matrix:'#34d399', quantix:'#a78bfa', zenix:'#fb923c' }
const TC = { A:'#f59e0b', B:'#38bdf8', C:'#34d399' }

const CORE_AGENTS = [
  {
    id:'nova', name:'Nova', emoji:'🌟', role:'Consigliere', layer:'Gateway', domain:'core', tier:'B', model:'gpt-4o-mini',
    desc:'De eerste stem die Supreme Fea hoort. Nova ontvangt alle input, analyseert intent en beslist: zelf afhandelen of doorsturen naar Flux. Zij is de poort van het systeem.',
    tools:['active-memory','skill-workshop','thread-ownership','telegram','tavily','duckduckgo','exa','perplexity'],
    skills:[
      {name:'taskflow', desc:'Multi-step taken orkestreren die langer duren dan één prompt'},
      {name:'wiki-maintainer', desc:'Memory Wiki bijhouden met patronen en learnings'},
      {name:'healthcheck', desc:'Systeem gezondheidscheck uitvoeren'},
    ],
    workers:[],
    workflows:['Intake & routing — verzoek analyseren en intent bepalen','Direct afhandelen — enkelvoudige vragen zelf beantwoorden','Flux-ready maken — complexe taken structureren voor Flux'],
    escalatie:'Flux bij multi-agent taken of domeinspecifieke expertise',
  },
  {
    id:'flux', name:'Flux', emoji:'⚡', role:'Underboss', layer:'Orchestrator', domain:'core', tier:'A', model:'gemini-2.5-pro',
    desc:'De brain van ARC AI Agents. Flux regelt het dagelijkse reilen en zeilen. Hij ontvangt van Nova, maakt strategische beslissingen en routeert naar de juiste Omni Lead per domein.',
    tools:['active-memory','skill-workshop','thread-ownership','llm-task','oc-path','webhooks','tavily','exa','perplexity'],
    skills:[
      {name:'taskflow', desc:'Durable multi-step projecten starten en bewaken'},
      {name:'wiki-maintainer', desc:'Systeem-brede kennisbase beheren'},
      {name:'healthcheck', desc:'Cross-domain systeem audits'},
    ],
    workers:[],
    workflows:['Cross-domain routing — juiste Omni Lead selecteren','Project orkestratie — meerdere domains parallel aansturen','Strategische beslissingen — escalatie en prioritering'],
    escalatie:'Nova bij Supreme Fea rapportage of urgente escalaties',
  },
]

const DOMAINS = [
  {
    id:'helix', label:'Helix', emoji:'🔧', color:'#38bdf8',
    desc:'Tech domein — website fabriek, code development, security monitoring, automation pipelines en infrastructure management',
    lead:'cortexia',
    agents:[
      {
        id:'cortexia', name:'Cortexia', emoji:'💡', role:'Omni Lead', tier:'B', model:'gpt-4o-mini',
        desc:'Technisch directeur van Helix. Handelt 80% van tech taken zelf af met haar brede toolset. Delegeert alleen gespecialiseerde taken naar sentinels.',
        tools:[
          {name:'tavily', desc:'Tech nieuws en releases scannen'},
          {name:'exa', desc:'Diepgaande tech research'},
          {name:'perplexity', desc:'Actuele tech info met bronnen'},
          {name:'firecrawl', desc:'GitHub repos en docs scrapen'},
          {name:'llm-task', desc:'Sentinels parallel aansturen'},
          {name:'oc-path', desc:'Workflow paden definiëren'},
          {name:'opencode', desc:'Code review uitvoeren'},
          {name:'policy', desc:'Governance regels afdwingen'},
        ],
        skills:[
          {name:'project-coordinator', desc:'Requirements vertalen naar technische specs en taakverdeling'},
          {name:'agent-dispatcher', desc:'Sentinels parallel aansturen via LLM Task'},
          {name:'tech-researcher', desc:'Gestructureerde tech research via Tavily, Exa en Perplexity'},
          {name:'status-reporter', desc:'Gestructureerde rapporten opstellen voor Flux'},
          {name:'taskflow', desc:'Multi-step projecten orkestreren'},
        ],
        workers:[
          {name:'coordinate_project.py', desc:'Vertaalt project verzoek naar specs en taakverdeling voor alle sentinels'},
        ],
        workflows:['Website Fabriek — requirements → specs → parallel sentinels aansturen → live URL','Code Review — code analyseren met OpenCode en Exa best practices','Tech Research — Tavily + Exa + Perplexity parallel voor gefundeerde beslissingen','Security Incident — Nero coördineren bij kritieke CVEs'],
        escalatie:'Flux bij cross-domain of strategische beslissingen',
      },
      {
        id:'forge', name:'Forge', emoji:'⚙️', role:'Engineering', tier:'A', model:'gemini-2.5-pro',
        desc:'Engineering specialist — bouwt frontend, backend en API. Beheert GitHub repos en zorgt voor code kwaliteit. Gebruikt Tier A voor zware code taken.',
        tools:[
          {name:'opencode', desc:'Code schrijven, reviewen en debuggen'},
          {name:'github-copilot', desc:'Code suggesties en completion'},
          {name:'tavily', desc:'Tech docs en best practices zoeken'},
          {name:'firecrawl', desc:'GitHub repos en changelogs scrapen'},
          {name:'browser', desc:'GitHub interface navigeren'},
          {name:'webhooks', desc:'GitHub webhooks ontvangen'},
        ],
        skills:[
          {name:'code-architect', desc:'Architectuur beslissingen nemen — frontend/backend/database keuze'},
          {name:'git-workflow', desc:'Git commit conventies, branches en GitHub management'},
          {name:'api-builder', desc:'REST APIs bouwen met FastAPI'},
          {name:'frontend-builder', desc:'Moderne frontends met HTML/CSS/JS of React'},
          {name:'browser-automation', desc:'Complexe web flows automatiseren'},
        ],
        workers:[
          {name:'generate_website.py', desc:'Genereert complete website structuur (HTML/CSS/JS) op basis van naam en features'},
          {name:'build_api.py', desc:'Genereert FastAPI backend met routes per endpoint'},
          {name:'deploy_website.sh', desc:'Pusht code naar GitHub en deployt naar Vercel productie'},
        ],
        workflows:['Website Frontend — HTML/CSS/JS of React bouwen op basis van specs','Backend API — FastAPI endpoints genereren per feature','Code Review — OWASP checklist + best practices verificatie','GitHub Monitoring — dagelijks releases en issues scannen'],
        escalatie:'Cortexia bij architectuur beslissingen of scope wijzigingen',
      },
      {
        id:'nero', name:'Nero', emoji:'🛡️', role:'Security', tier:'B', model:'gpt-4o-mini',
        desc:'Security specialist — bewaakt CVEs, voert code audits uit en monitort het ARC AI Agents systeem op dreigingen en onverwacht gedrag.',
        tools:[
          {name:'tavily', desc:'CVE databases en security advisories zoeken'},
          {name:'exa', desc:'Diepgaande analyse van kritieke kwetsbaarheden'},
          {name:'perplexity', desc:'Actuele security nieuws met bronvermelding'},
          {name:'firecrawl', desc:'Security bulletins en patch notes scrapen'},
          {name:'policy', desc:'Security policies afdwingen en controleren'},
        ],
        skills:[
          {name:'cve-analyzer', desc:'CVEs prioriteren op CVSS score en impact voor ARC AI Agents'},
          {name:'code-security-audit', desc:'OWASP Top 10 checklist uitvoeren op project code'},
          {name:'security-reporter', desc:'Gestructureerde security rapporten voor Cortexia'},
          {name:'system-monitor', desc:'Config bestanden en services bewaken op onverwachte wijzigingen'},
        ],
        workers:[
          {name:'code_audit.py', desc:'Scant project code op hardcoded secrets, XSS, injection en andere kwetsbaarheden'},
          {name:'cve_scan.sh', desc:'Zoekt nieuwe CVEs voor ARC AI Agents technologieën'},
          {name:'system_monitor.sh', desc:'Controleert service status en detecteert config wijzigingen'},
        ],
        workflows:['CVE Monitoring — dagelijks Tavily + Exa scan op nieuwe kwetsbaarheden','Security Audit — code_audit.py + OWASP checklist voor deployment goedkeuring','System Monitor — config hashes vergelijken en services bewaken','Policy Enforcement — governance regels controleren en afdwingen'],
        escalatie:'Cortexia bij alle bevindingen, direct naar Flux bij kritieke systeem-brede issues',
      },
      {
        id:'axon', name:'Axon', emoji:'🔗', role:'Automation', tier:'B', model:'gpt-4o-mini',
        desc:'Automation specialist — bouwt deployment pipelines, beheert databases en automatiseert workflows. Verbindt systemen via webhooks.',
        tools:[
          {name:'webhooks', desc:'Externe triggers ontvangen en sturen'},
          {name:'llm-task', desc:'Parallelle subtaken spawnen'},
          {name:'oc-path', desc:'Workflow paden definiëren'},
          {name:'opencode', desc:'Automation scripts schrijven'},
          {name:'browser', desc:'Web interfaces automatiseren'},
        ],
        skills:[
          {name:'webhook-handler', desc:'GitHub, Vercel en handmatige webhooks verwerken'},
          {name:'pipeline-builder', desc:'CI/CD pipelines ontwerpen voor static, React en FastAPI projecten'},
          {name:'database-designer', desc:'SQLite schemas ontwerpen op basis van project features'},
          {name:'taskflow', desc:'Durable multi-step automation jobs'},
          {name:'taskflow-inbox-triage', desc:'Inbox berichten verwerken en routeren'},
        ],
        workers:[
          {name:'build_pipeline.py', desc:'Voert deployment pipeline uit — validatie, build check en pre-deploy checks'},
          {name:'setup_database.py', desc:'Maakt SQLite database aan met correcte tabellen op basis van project specs'},
          {name:'run_pipeline.sh', desc:'Bash pipeline runner voor deploy, backup en andere automation taken'},
        ],
        workflows:['Deploy Pipeline — code validatie → build → pre-deploy checks → Ventura triggeren','Database Setup — specs analyseren → tabellen aanmaken → backend koppelen','Webhook Handler — GitHub push → pipeline starten → Cortexia notificeren','Integraties — API docs lezen → integratie bouwen → endpoint configureren'],
        escalatie:'Cortexia bij complexe architectuur of scope wijzigingen',
      },
      {
        id:'ventura', name:'Ventura', emoji:'🏗️', role:'Infrastructure', tier:'B', model:'gpt-4o-mini',
        desc:'Infrastructure specialist — deployt naar Vercel, beheert alle ARC AI Agents services en monitort de infrastructure gezondheid.',
        tools:[
          {name:'webhooks', desc:'Deploy triggers en health alerts ontvangen'},
          {name:'browser', desc:'Monitoring dashboards en Vercel interface'},
          {name:'web-readability', desc:'Infra docs en runbooks lezen'},
          {name:'tavily', desc:'Infra best practices en troubleshooting'},
          {name:'policy', desc:'Infrastructure policies controleren'},
        ],
        skills:[
          {name:'vercel-deployer', desc:'Vercel deployments beheren — deploy, verify, rollback'},
          {name:'service-manager', desc:'ARC AI Agents services starten, stoppen en monitoren'},
          {name:'infra-reporter', desc:'Infrastructure rapporten voor Cortexia'},
          {name:'cloudflare-manager', desc:'Cloudflare tunnel en DNS voor arc-vortex.nl'},
        ],
        workers:[
          {name:'deploy.sh', desc:'Deployt project naar Vercel productie en voert health check uit op live URL'},
          {name:'health_check.sh', desc:'Checkt bereikbaarheid van alle services op hun poorten'},
          {name:'infra_status.py', desc:'Volledige infrastructure status — services, disk en memory'},
        ],
        workflows:['Vercel Deploy — pre-check → vercel --prod → health check → URL rapporteren','Health Check — alle services pingen → status rapporteren → escaleren bij problemen','Service Management — services starten/stoppen/herstarten via systemd','Cloudflare DNS — subdomein koppelen aan Vercel project'],
        escalatie:'Cortexia bij kritieke infra problemen, Nero bij security gerelateerde infra issues',
      },
      {
        id:'clio', name:'Clio', emoji:'📝', role:'Documentation', tier:'C', model:'gemini-flash-lite',
        desc:'Documentation specialist — schrijft technische docs, beheert de domein kennisbase en voert wekelijkse audits uit op alle Helix agents.',
        tools:[
          {name:'web-readability', desc:'Externe docs en referenties lezen'},
          {name:'firecrawl', desc:'Docs websites scrapen'},
          {name:'document-extract', desc:'Bestaande docs importeren'},
          {name:'memory-wiki', desc:'Domein kennisbase structureren'},
          {name:'tavily', desc:'Referenties en voorbeelden zoeken'},
        ],
        skills:[
          {name:'doc-writer', desc:'Technische README, DEPLOYMENT en API documentatie schrijven'},
          {name:'api-documenter', desc:'REST API endpoints documenteren met voorbeelden'},
          {name:'audit-checker', desc:'Wekelijkse audit op Helix agent documentatie volledigheid'},
          {name:'knowledge-curator', desc:'Domein kennisbase beheren via Memory Wiki'},
          {name:'diagram-maker', desc:'SVG/HTML diagrammen maken voor architectuur en flows'},
        ],
        workers:[
          {name:'generate_readme.py', desc:'Genereert professionele README.md met tech stack, live URL en installatie instructies'},
          {name:'generate_api_docs.py', desc:'Extraheert API endpoints uit FastAPI code en genereert API.md'},
          {name:'domain_audit.py', desc:'Controleert alle Helix agents op MD bestanden, workers en skills volledigheid'},
        ],
        workflows:['Website Docs — README + DEPLOYMENT + API docs schrijven na succesvolle deploy','API Docs — backend code analyseren en endpoints documenteren','Domein Audit — wekelijks alle agent .md bestanden op volledigheid checken','Knowledge Base — Memory Wiki bijhouden met domein learnings en patronen'],
        escalatie:'Cortexia bij grote documentatie gaps of inconsistenties',
      },
    ]
  },
  {
    id:'finix', label:'Finix', emoji:'💰', color:'#f472b6',
    desc:'Finance domein — treasury bewaking, marktdata analyse, risk management en financiële rapportage',
    lead:'finoria',
    agents:[
      { id:'finoria', name:'Finoria', emoji:'💰', role:'Omni Lead', tier:'B', model:'gpt-4o-mini', desc:'Finance directeur — coördineert alle financiële analyse, bewaking en rapportage voor het Finix domein.', tools:[{name:'tavily',desc:'Marktdata en financieel nieuws'},{name:'exa',desc:'Diepgaande financiële research'}], skills:[{name:'taskflow',desc:'Multi-step financiële analyses'},{name:'wiki-maintainer',desc:'Finance kennisbase'}], workers:[], workflows:['Finance Rapportage — dagelijkse samenvatting aan Flux','Risk Assessment — portfolio risico beoordelen','Budget Bewaking — uitgaven monitoren','Sentinel Coördinatie — taken verdelen'], escalatie:'Flux bij cross-domain of strategische financiële beslissingen' },
      { id:'kairo', name:'Kairo', emoji:'📈', role:'Treasury', tier:'B', model:'gpt-4o-mini', desc:'Treasury specialist — liquiditeit en cashflow bewaking. Bewaakt vroege signalen van financiële afwijkingen.', tools:[{name:'tavily',desc:'Treasury rates en liquiditeitsdata'},{name:'exa',desc:'Treasury best practices'}], skills:[{name:'taskflow',desc:'Treasury monitoring jobs'}], workers:[], workflows:['Liquiditeit Monitor — dagelijkse balans check','Cashflow Analyse — in/out flows analyseren','Vroege Signalering — afwijkingen detecteren'], escalatie:'Finoria bij significante afwijkingen' },
      { id:'kenzo', name:'Kenzo', emoji:'🔢', role:'Modeling', tier:'C', model:'gemini-flash-lite', desc:'Financieel modellering en forecasting specialist.', tools:[{name:'tavily',desc:'Financiële model data'}], skills:[], workers:[], workflows:['Financial Models bouwen','Forecasting uitvoeren','Scenario analyses'], escalatie:'Finoria bij model validatie' },
      { id:'odis', name:'Odis', emoji:'💎', role:'Data', tier:'B', model:'gpt-4o-mini', desc:'Financiële data analyse en rapportage specialist.', tools:[{name:'tavily',desc:'Financiële data bronnen'},{name:'exa',desc:'Data research'}], skills:[], workers:[], workflows:['Data Analyse','Rapportage opstellen','Data kwaliteit bewaken'], escalatie:'Finoria bij data inconsistenties' },
      { id:'vector', name:'Vector', emoji:'📊', role:'Analytics', tier:'C', model:'gemini-flash-lite', desc:'Markt analytics en trend analyse specialist.', tools:[{name:'tavily',desc:'Marktdata'}], skills:[], workers:[], workflows:['Markt Analytics','Trend Analyse','Benchmark rapportage'], escalatie:'Finoria bij significante marktbewegingen' },
      { id:'zion', name:'Zion', emoji:'⚖️', role:'Risk', tier:'B', model:'gpt-4o-mini', desc:'Risk management en compliance specialist.', tools:[{name:'tavily',desc:'Risk data en compliance nieuws'},{name:'policy',desc:'Compliance policies'}], skills:[], workers:[], workflows:['Risk Monitor','Compliance Check','Risk Rapportage'], escalatie:'Finoria bij hoog risico bevindingen' },
    ]
  },
  {
    id:'matrix', label:'Matrix', emoji:'🧠', color:'#34d399',
    desc:'Data & AI domein — kennisverwerking, data structurering, AI evaluatie en logische redenering',
    lead:'saelia',
    agents:[
      { id:'saelia', name:'Saelia', emoji:'🧠', role:'Omni Lead', tier:'B', model:'gpt-4o-mini', desc:'Matrix directeur — coördineert AI en data taken voor het domein.', tools:[{name:'tavily',desc:'AI nieuws en research'},{name:'exa',desc:'AI model research'}], skills:[{name:'taskflow',desc:'Multi-step data projecten'}], workers:[], workflows:['Data Coördinatie','AI Routing','Research Verdeling','Sentinel Coördinatie'], escalatie:'Flux bij cross-domain data behoeften' },
      { id:'tharos', name:'Tharos', emoji:'📚', role:'Knowledge', tier:'B', model:'gpt-4o-mini', desc:'Kennisbase beheer en research specialist.', tools:[{name:'tavily',desc:'Research bronnen'},{name:'exa',desc:'Semantische kenniszoekopdrachten'}], skills:[], workers:[], workflows:['Research uitvoeren','Kennisbase bijhouden','Bronnen verifiëren'], escalatie:'Saelia bij kennisconflicten' },
      { id:'sora', name:'Sora', emoji:'🤖', role:'AI', tier:'B', model:'gpt-4o-mini', desc:'AI model evaluatie en optimalisatie specialist.', tools:[{name:'tavily',desc:'AI model nieuws'},{name:'exa',desc:'AI benchmark research'}], skills:[], workers:[], workflows:['AI Model Evaluatie','Benchmark Testing','Model Vergelijking'], escalatie:'Saelia bij model beslissingen' },
      { id:'arix', name:'Arix', emoji:'🗂️', role:'Structure', tier:'C', model:'gemini-flash-lite', desc:'Data structurering en organisatie specialist.', tools:[{name:'tavily',desc:'Data structuur best practices'}], skills:[], workers:[], workflows:['Data Structurering','Schema Ontwerp','Data Organisatie'], escalatie:'Saelia bij structuur beslissingen' },
      { id:'enki', name:'Enki', emoji:'🔬', role:'Logic', tier:'C', model:'gemini-flash-lite', desc:'Logica verificatie en redenering specialist.', tools:[], skills:[], workers:[], workflows:['Logica Verificatie','Redenering Checks','Consistentie Analyse'], escalatie:'Saelia bij logische conflicten' },
      { id:'daxio', name:'Daxio', emoji:'⚡', role:'Processing', tier:'C', model:'gemini-flash-lite', desc:'Data verwerking en transformatie specialist.', tools:[], skills:[], workers:[], workflows:['Data Processing','Transformaties uitvoeren','Batch verwerking'], escalatie:'Saelia bij verwerkingsproblemen' },
    ]
  },
  {
    id:'quantix', label:'Quantix', emoji:'✨', color:'#a78bfa',
    desc:'Strategy & Analytics domein — strategische planning, kwantitatieve analyse, optimalisatie en monitoring',
    lead:'lumeria',
    agents:[
      { id:'lumeria', name:'Lumeria', emoji:'✨', role:'Omni Lead', tier:'B', model:'gpt-4o-mini', desc:'Quantix directeur — coördineert strategie en analytics voor het domein.', tools:[{name:'tavily',desc:'Strategie nieuws'},{name:'exa',desc:'Strategische research'}], skills:[{name:'taskflow',desc:'Multi-step strategie projecten'}], workers:[], workflows:['Strategie Coördinatie','Analytics Verdeling','Optimalisatie Bewaking','Sentinel Coördinatie'], escalatie:'Flux bij strategische besluiten met grote impact' },
      { id:'kresta', name:'Kresta', emoji:'🎯', role:'Strategy', tier:'C', model:'gemini-flash-lite', desc:'Strategische planning en uitvoering specialist.', tools:[{name:'tavily',desc:'Strategie data'}], skills:[], workers:[], workflows:['Strategische Planning','Roadmap opstellen','Prioritering'], escalatie:'Lumeria bij strategische conflicten' },
      { id:'elora', name:'Elora', emoji:'🔍', role:'Analysis', tier:'B', model:'gpt-4o-mini', desc:'Diepgaande analyse en inzichten specialist.', tools:[{name:'tavily',desc:'Analyse bronnen'},{name:'exa',desc:'Diepgaande research'}], skills:[], workers:[], workflows:['Diepgaande Analyse','Inzichten genereren','Trend Rapportage'], escalatie:'Lumeria bij conflicterende inzichten' },
      { id:'luvia', name:'Luvia', emoji:'📐', role:'Modeling', tier:'C', model:'gemini-flash-lite', desc:'Kwantitatieve modellen bouwen specialist.', tools:[], skills:[], workers:[], workflows:['Kwantitatief Modelleren','Simulaties uitvoeren','Model Validatie'], escalatie:'Lumeria bij model beslissingen' },
      { id:'nura', name:'Nura', emoji:'⚡', role:'Optimization', tier:'C', model:'gemini-flash-lite', desc:'Proces optimalisatie en efficiency specialist.', tools:[], skills:[], workers:[], workflows:['Optimalisatie','Efficiency Analyse','Verbeter Voorstellen'], escalatie:'Lumeria bij grote optimalisatie projecten' },
      { id:'vondra', name:'Vondra', emoji:'👁️', role:'Monitoring', tier:'C', model:'gemini-flash-lite', desc:'Continue monitoring en alerting specialist.', tools:[], skills:[], workers:[], workflows:['Continue Monitoring','Alert Configuratie','Afwijking Detectie'], escalatie:'Lumeria bij kritieke alerts' },
    ]
  },
  {
    id:'zenix', label:'Zenix', emoji:'🌊', color:'#fb923c',
    desc:'Operations & Branding domein — dagelijkse operaties, workflow management, merkstrategie en communicatie',
    lead:'fluentia',
    agents:[
      { id:'fluentia', name:'Fluentia', emoji:'🌊', role:'Omni Lead', tier:'B', model:'gpt-4o-mini', desc:'Zenix directeur — coördineert operations en branding voor het domein.', tools:[{name:'tavily',desc:'Operations en branding nieuws'},{name:'exa',desc:'Brand research'}], skills:[{name:'taskflow',desc:'Multi-step operations projecten'}], workers:[], workflows:['Operations Coördinatie','Brand Management','Workflow Bewaking','Sentinel Coördinatie'], escalatie:'Flux bij strategische brand of operations beslissingen' },
      { id:'draven', name:'Draven', emoji:'🌀', role:'Flow', tier:'B', model:'gpt-4o-mini', desc:'Workflow en process management specialist.', tools:[{name:'webhooks',desc:'Process triggers'},{name:'tavily',desc:'Process best practices'}], skills:[], workers:[], workflows:['Workflow Design','Process Optimalisatie','Flow Monitoring'], escalatie:'Fluentia bij process conflicten' },
      { id:'solis', name:'Solis', emoji:'☀️', role:'Operations', tier:'C', model:'gemini-flash-lite', desc:'Dagelijkse operaties uitvoeren specialist.', tools:[], skills:[], workers:[], workflows:['Dagelijkse Ops','Operationele Checks','Routine Taken'], escalatie:'Fluentia bij operationele blokkades' },
      { id:'orizon', name:'Orizon', emoji:'🌅', role:'Reasoning', tier:'C', model:'gemini-flash-lite', desc:'Redenering en beslissingsondersteuning specialist.', tools:[], skills:[], workers:[], workflows:['Redenering Ondersteuning','Beslissings Analyse','Scenario Evaluatie'], escalatie:'Fluentia bij complexe redenering' },
      { id:'unia', name:'Unia', emoji:'💫', role:'Polish', tier:'C', model:'gemini-flash-lite', desc:'Kwaliteitscontrole en verfijning specialist.', tools:[], skills:[], workers:[], workflows:['Kwaliteitscontrole','Output Verfijning','Standaard Bewaking'], escalatie:'Fluentia bij kwaliteitsproblemen' },
      { id:'zena', name:'Zena', emoji:'🎨', role:'Branding', tier:'B', model:'gpt-4o-mini', desc:'Merkidentiteit en communicatie specialist.', tools:[{name:'tavily',desc:'Branding trends'},{name:'exa',desc:'Brand research'},{name:'firecrawl',desc:'Competitor analyse'}], skills:[], workers:[], workflows:['Merkidentiteit Beheer','Communicatie Strategie','Brand Consistentie'], escalatie:'Fluentia bij grote brand beslissingen' },
    ]
  },
]

function SectionLabel({ color, children }) {
  return (
    <div style={{display:'flex',alignItems:'center',gap:8,marginBottom:10}}>
      <div style={{width:3,height:16,background:color,borderRadius:2}}/>
      <span style={{fontSize:11,fontWeight:700,color,textTransform:'uppercase',letterSpacing:'0.1em'}}>{children}</span>
      <div style={{flex:1,height:1,background:`${color}20`}}/>
    </div>
  )
}

function AgentDetailPanel({ agent, color, t, onClose }) {
  const tierColor = TC[agent.tier]
  return (
    <div style={{background:`${color}33`,border:`1.5px solid ${color}40`,borderRadius:12,padding:'16px 18px',marginTop:12,position:'relative'}}>
      <button onClick={onClose} style={{position:'absolute',top:12,right:12,width:24,height:24,borderRadius:6,border:`1px solid ${t.border}`,background:'transparent',color:t.textMuted,cursor:'pointer',fontSize:14,display:'flex',alignItems:'center',justifyContent:'center'}}>
        <i className="ti ti-x"/>
      </button>

      {/* Header */}
      <div style={{display:'flex',alignItems:'center',gap:10,marginBottom:12}}>
        <span style={{fontSize:26}}>{agent.emoji}</span>
        <div style={{flex:1}}>
          <div style={{fontSize:15,fontWeight:800,color:t.text}}>{agent.name}</div>
          <div style={{fontSize:10,color,fontWeight:700,textTransform:'uppercase',letterSpacing:'0.1em'}}>{agent.role}</div>
        </div>
        <span style={{fontSize:10,fontWeight:700,color:tierColor,background:`${tierColor}15`,border:`1px solid ${tierColor}30`,borderRadius:5,padding:'3px 10px'}}>Tier {agent.tier} — {agent.model}</span>
      </div>

      <div style={{fontSize:11,color:t.textMuted,lineHeight:1.7,marginBottom:14}}>{agent.desc}</div>

      <div style={{display:'grid',gridTemplateColumns:'repeat(2,1fr)',gap:10,marginBottom:10}}>
        {/* Workflows */}
        <div style={{background:'rgba(0,0,0,0.40)',border:`1px solid ${t.border}`,borderRadius:8,padding:'10px 12px'}}>
          <div style={{fontSize:9,fontWeight:700,color:t.textMuted,textTransform:'uppercase',letterSpacing:'0.1em',marginBottom:8}}>Workflows</div>
          {agent.workflows?.map((w,i) => (
            <div key={i} style={{display:'flex',gap:6,marginBottom:5,alignItems:'flex-start'}}>
              <div style={{width:5,height:5,borderRadius:'50%',background:color,flexShrink:0,marginTop:3}}/>
              <span style={{fontSize:10,color:t.text,lineHeight:1.5}}>{w}</span>
            </div>
          ))}
          <div style={{marginTop:8,padding:'6px 8px',background:`${color}10`,borderRadius:6,border:`1px solid ${color}20`}}>
            <div style={{fontSize:9,fontWeight:700,color:color,marginBottom:2}}>Escalatie</div>
            <div style={{fontSize:9,color:t.textMuted}}>{agent.escalatie}</div>
          </div>
        </div>

        {/* Skills */}
        <div style={{background:'rgba(0,0,0,0.40)',border:`1px solid ${t.border}`,borderRadius:8,padding:'10px 12px'}}>
          <div style={{fontSize:9,fontWeight:700,color:t.textMuted,textTransform:'uppercase',letterSpacing:'0.1em',marginBottom:8}}>Skills</div>
          {agent.skills?.length > 0 ? agent.skills.map((s,i) => (
            <div key={i} style={{display:'flex',gap:6,marginBottom:5,alignItems:'flex-start'}}>
              <div style={{width:5,height:5,borderRadius:'50%',background:'#a78bfa',flexShrink:0,marginTop:3}}/>
              <div>
                <div style={{fontSize:10,fontWeight:700,color:'#a78bfa',marginBottom:1}}>{s.name}</div>
                <div style={{fontSize:9,color:t.textMuted,lineHeight:1.4}}>{s.desc}</div>
              </div>
            </div>
          )) : <div style={{fontSize:10,color:t.textMuted}}>In ontwikkeling</div>}
        </div>
      </div>

      <div style={{display:'grid',gridTemplateColumns:'repeat(2,1fr)',gap:10}}>
        {/* Tools */}
        <div style={{background:'rgba(0,0,0,0.40)',border:`1px solid ${t.border}`,borderRadius:8,padding:'10px 12px'}}>
          <div style={{fontSize:9,fontWeight:700,color:t.textMuted,textTransform:'uppercase',letterSpacing:'0.1em',marginBottom:8}}>Tools</div>
          {agent.tools?.length > 0 ? agent.tools.map((tool,i) => (
            <div key={i} style={{display:'flex',gap:6,marginBottom:5,alignItems:'flex-start'}}>
              <div style={{width:5,height:5,borderRadius:'50%',background:'#38bdf8',flexShrink:0,marginTop:3}}/>
              <div>
                <div style={{fontSize:10,fontWeight:700,color:'#38bdf8',marginBottom:1}}>{tool.name}</div>
                <div style={{fontSize:9,color:t.textMuted,lineHeight:1.4}}>{tool.desc}</div>
              </div>
            </div>
          )) : <div style={{fontSize:10,color:t.textMuted}}>Standaard tools</div>}
        </div>

        {/* Workers */}
        <div style={{background:'rgba(0,0,0,0.40)',border:`1px solid ${t.border}`,borderRadius:8,padding:'10px 12px'}}>
          <div style={{fontSize:9,fontWeight:700,color:t.textMuted,textTransform:'uppercase',letterSpacing:'0.1em',marginBottom:8}}>Workers & Scripts</div>
          {agent.workers?.length > 0 ? agent.workers.map((w,i) => (
            <div key={i} style={{display:'flex',gap:6,marginBottom:5,alignItems:'flex-start'}}>
              <div style={{width:5,height:5,borderRadius:'50%',background:'#22c55e',flexShrink:0,marginTop:3}}/>
              <div>
                <div style={{fontSize:10,fontWeight:700,color:'#22c55e',marginBottom:1}}>{w.name}</div>
                <div style={{fontSize:9,color:t.textMuted,lineHeight:1.4}}>{w.desc}</div>
              </div>
            </div>
          )) : <div style={{fontSize:10,color:t.textMuted}}>Geen workers — coördineert via LLM</div>}
        </div>
      </div>
    </div>
  )
}

export default function DomeinTab({ theme }) {
  const t = theme?.colors || {}
  const acc = t.accent || '#c9a84c'
  const [selectedDomain, setSelectedDomain] = useState('helix')
  const [selectedAgent, setSelectedAgent] = useState(null)
  const [view, setView] = useState('domains')
  const [flowDomain, setFlowDomain] = useState('helix')

  const domain = DOMAINS.find(d => d.id === selectedDomain)
  const flowDomainData = DOMAINS.find(d => d.id === flowDomain)

  return (
    <div style={{height:'100%',display:'flex',flexDirection:'column',overflow:'hidden'}}>
      {/* Sub tabs */}
      <div style={{display:'flex',gap:2,padding:'10px 16px 0',borderBottom:`1px solid ${t.border}`,flexShrink:0}}>
        {[['domains','ti-sitemap','Domein Overzicht'],['flow','ti-arrow-right','Command Flow']].map(([id,icon,label]) => (
          <button key={id} onClick={() => setView(id)}
            style={{padding:'6px 14px',borderRadius:'7px 7px 0 0',border:`1px solid ${view===id?t.border:'transparent'}`,borderBottom:view===id?`1px solid ${t.bgSecondary||'#111'}`:'none',background:view===id?t.bgSecondary:'transparent',color:view===id?acc:t.textMuted,fontSize:12,fontWeight:view===id?700:400,cursor:'pointer',display:'flex',alignItems:'center',gap:5,marginBottom:view===id?-1:0}}>
            <i className={`ti ${icon}`} style={{fontSize:12}}/>{label}
          </button>
        ))}
      </div>

      <div style={{flex:1,overflow:'auto',padding:'16px'}}>

        {view === 'domains' && <>
          {/* CORE */}
          <div style={{marginBottom:20}}>
            <SectionLabel color={acc}>Core — Commandolijn</SectionLabel>
            <div style={{display:'grid',gridTemplateColumns:'1fr 1fr',gap:10}}>
              {CORE_AGENTS.map(agent => {
                const isSelected = selectedAgent?.id === agent.id
                const tierColor = TC[agent.tier]
                return (
                  <div key={agent.id} onClick={() => setSelectedAgent(isSelected ? null : agent)}
                    style={{background:`linear-gradient(135deg, ${agent.id==='nova'?'#c9a84c':'#f59e0b'}22 0%, ${agent.id==='nova'?'#c9a84c':'#f59e0b'}08 100%)`,border:`2px solid ${isSelected ? agent.color : agent.id==='nova'?'#c9a84c60':'#f59e0b60'}`,borderRadius:12,padding:'16px 18px',cursor:'pointer',position:'relative',overflow:'hidden',transition:'all .15s'}}>
                    <div style={{position:'absolute',top:0,left:0,right:0,height:3,background:`linear-gradient(90deg, transparent, ${agent.id==='nova'?'#c9a84c':'#f59e0b'}, transparent)`}}/>
                    <div style={{display:'flex',alignItems:'center',gap:10,marginBottom:8}}>
                      <span style={{fontSize:22}}>{agent.emoji}</span>
                      <div style={{flex:1}}>
                        <div style={{fontSize:14,fontWeight:800,color:t.text}}>{agent.name}</div>
                        <div style={{fontSize:10,color:agent.color,fontWeight:700,textTransform:'uppercase',letterSpacing:'0.08em'}}>{agent.role} — {agent.layer}</div>
                      </div>
                      <span style={{fontSize:10,fontWeight:700,color:tierColor,background:`${tierColor}15`,border:`1px solid ${tierColor}30`,borderRadius:5,padding:'2px 8px'}}>Tier {agent.tier}</span>
                    </div>
                    <div style={{fontSize:11,color:t.textMuted,lineHeight:1.5,marginBottom:8}}>{agent.desc}</div>
                    <div style={{display:'flex',gap:4,flexWrap:'wrap'}}>
                      {agent.workflows.slice(0,2).map(w => (
                        <span key={w} style={{fontSize:9,color:agent.color,background:`${agent.color}12`,borderRadius:4,padding:'2px 6px'}}>{w.split(' — ')[0]}</span>
                      ))}
                    </div>
                    {isSelected && <div style={{position:'absolute',bottom:8,right:10,fontSize:9,color:agent.color}}>▲ details</div>}
                  </div>
                )
              })}
            </div>
            {selectedAgent && CORE_AGENTS.find(a => a.id === selectedAgent.id) && (
              <AgentDetailPanel agent={selectedAgent} color={acc} t={t} onClose={() => setSelectedAgent(null)}/>
            )}
          </div>

          {/* Domain selector */}
          <div style={{display:'flex',gap:6,marginBottom:12,flexWrap:'wrap'}}>
            {DOMAINS.map(d => (
              <button key={d.id} onClick={() => {setSelectedDomain(d.id); setSelectedAgent(null)}}
                style={{padding:'6px 12px',borderRadius:8,border:`1.5px solid ${selectedDomain===d.id?d.color:t.border}`,background:selectedDomain===d.id?`${d.color}15`:'transparent',color:selectedDomain===d.id?d.color:t.textMuted,fontSize:11,fontWeight:selectedDomain===d.id?700:400,cursor:'pointer',display:'flex',alignItems:'center',gap:4}}>
                <span>{d.emoji}</span>{d.label}
              </button>
            ))}
          </div>

          {/* Domein info */}
          {domain && <>
            <div style={{background:`linear-gradient(135deg, ${domain.color}22 0%, ${domain.color}08 100%)`,border:`1.5px solid ${domain.color}30`,borderRadius:12,padding:'12px 16px',marginBottom:12}}>
              <div style={{display:'flex',alignItems:'center',gap:10}}>
                <span style={{fontSize:22}}>{domain.emoji}</span>
                <div style={{flex:1}}>
                  <div style={{fontSize:14,fontWeight:800,color:t.text}}>{domain.label} Domain</div>
                  <div style={{fontSize:11,color:t.textMuted,marginTop:2}}>{domain.desc}</div>
                </div>
                <div style={{fontSize:10,color:t.textMuted}}>Lead: <strong style={{color:domain.color}}>{domain.lead}</strong></div>
              </div>
            </div>

            <div style={{display:'grid',gridTemplateColumns:'repeat(auto-fill, minmax(240px, 1fr))',gap:10}}>
              {domain.agents.map(agent => {
                const isSelected = selectedAgent?.id === agent.id
                const tierColor = TC[agent.tier]
                const isLead = agent.id === domain.lead
                return (
                  <div key={agent.id} onClick={() => setSelectedAgent(isSelected ? null : agent)}
                    style={{background:`linear-gradient(135deg, ${domain.color}${isLead?'28':'22'} 0%, ${domain.color}${isLead?'10':'08'} 100%)`,border:`1.5px solid ${isSelected ? domain.color : domain.color+(isLead?'40':'25')}`,borderRadius:12,padding:'13px 14px',cursor:'pointer',position:'relative',overflow:'hidden',transition:'all .15s'}}>
                    <div style={{position:'absolute',top:0,left:0,right:0,height:isLead?3:2,background:`linear-gradient(90deg, ${domain.color}00, ${domain.color}${isLead?'90':'50'}, ${domain.color}00)`}}/>
                    {isLead && <div style={{position:'absolute',top:8,right:10,fontSize:8,color:domain.color,fontWeight:700,background:`${domain.color}15`,borderRadius:3,padding:'1px 5px'}}>LEAD</div>}
                    <div style={{display:'flex',alignItems:'center',gap:8,marginBottom:6}}>
                      <span style={{fontSize:isLead?20:16}}>{agent.emoji}</span>
                      <div style={{flex:1}}>
                        <div style={{fontSize:12,fontWeight:700,color:t.text}}>{agent.name}</div>
                        <div style={{fontSize:9,color:domain.color,fontWeight:700,textTransform:'uppercase',letterSpacing:'0.07em'}}>{agent.role}</div>
                      </div>
                      <span style={{fontSize:9,fontWeight:700,color:tierColor,background:`${tierColor}15`,border:`1px solid ${tierColor}30`,borderRadius:4,padding:'1px 6px'}}>Tier {agent.tier}</span>
                    </div>
                    <div style={{fontSize:10,color:t.textMuted,lineHeight:1.5,marginBottom:8}}>{agent.desc}</div>
                    <div style={{display:'flex',gap:3,flexWrap:'wrap'}}>
                      {agent.workers?.map(w => (
                        <span key={w.name} style={{fontSize:8,color:'#22c55e',background:'#22c55e10',border:'1px solid #22c55e20',borderRadius:3,padding:'1px 4px',fontFamily:'monospace'}}>{w.name}</span>
                      ))}
                      {agent.workers?.length === 0 && agent.skills?.slice(0,2).map(s => (
                        <span key={s.name} style={{fontSize:8,color:'#a78bfa',background:'#a78bfa10',borderRadius:3,padding:'1px 4px',fontFamily:'monospace'}}>{s.name}</span>
                      ))}
                    </div>
                    {isSelected && <div style={{position:'absolute',bottom:8,right:10,fontSize:9,color:domain.color}}>▲ details</div>}
                  </div>
                )
              })}
            </div>

            {selectedAgent && domain.agents.find(a => a.id === selectedAgent.id) && (
              <AgentDetailPanel agent={selectedAgent} color={domain.color} t={t} onClose={() => setSelectedAgent(null)}/>
            )}
          </>}
        </>}

        {view === 'flow' && <>
          <div style={{fontSize:13,fontWeight:700,color:t.text,marginBottom:4}}>Command Flow per Domein</div>
          <div style={{fontSize:11,color:t.textMuted,marginBottom:14,lineHeight:1.6}}>
            Commando's stromen <strong style={{color:t.text}}>omlaag</strong>: Supreme Fea → Nova → Flux → Omni Lead → Sentinels.
            Status rapportages stromen <strong style={{color:t.text}}>omhoog</strong> terug.
          </div>

          {/* Systeem flow */}
          <div style={{background:t.bgSecondary,border:`1px solid ${t.border}`,borderRadius:12,padding:'14px 16px',marginBottom:16}}>
            <SectionLabel color={acc}>Systeem Niveau</SectionLabel>
            <div style={{display:'flex',alignItems:'center',gap:0,overflowX:'auto',paddingBottom:4}}>
              {[
                {emoji:'👑',name:'Supreme Fea',role:'Il Capo',color:acc},
                {arrow:'→'},
                {emoji:'🌟',name:'Nova',role:'Gateway',color:acc},
                {arrow:'→'},
                {emoji:'⚡',name:'Flux',role:'Orchestrator',color:acc},
                {arrow:'→'},
                {emoji:'🏢',name:'Omni Leads',role:'5 domains',color:'#6b7280'},
                {arrow:'→'},
                {emoji:'👥',name:'Sentinels',role:'25 agents',color:'#6b7280'},
              ].map((item,i) => item.arrow ? (
                <div key={i} style={{fontSize:14,color:t.textMuted,padding:'0 8px',flexShrink:0}}>→</div>
              ) : (
                <div key={i} style={{background:`${item.color}15`,border:`1.5px solid ${item.color}30`,borderRadius:10,padding:'10px 14px',textAlign:'center',minWidth:100,flexShrink:0}}>
                  <div style={{fontSize:18}}>{item.emoji}</div>
                  <div style={{fontSize:11,fontWeight:700,color:item.color}}>{item.name}</div>
                  <div style={{fontSize:9,color:t.textMuted}}>{item.role}</div>
                </div>
              ))}
            </div>
          </div>

          {/* Domain flow selector */}
          <div style={{display:'flex',gap:6,marginBottom:12,flexWrap:'wrap'}}>
            {DOMAINS.map(d => (
              <button key={d.id} onClick={() => setFlowDomain(d.id)}
                style={{padding:'5px 12px',borderRadius:7,border:`1.5px solid ${flowDomain===d.id?d.color:t.border}`,background:flowDomain===d.id?`${d.color}15`:'transparent',color:flowDomain===d.id?d.color:t.textMuted,fontSize:11,fontWeight:flowDomain===d.id?700:400,cursor:'pointer',display:'flex',alignItems:'center',gap:4}}>
                <span>{d.emoji}</span>{d.label}
              </button>
            ))}
          </div>

          {/* Domain flow */}
          {flowDomainData && (
            <div style={{background:`linear-gradient(135deg, ${flowDomainData.color}10 0%, ${flowDomainData.color}03 100%)`,border:`1.5px solid ${flowDomainData.color}25`,borderRadius:12,padding:'16px'}}>
              <div style={{display:'flex',alignItems:'center',gap:8,marginBottom:14}}>
                <span style={{fontSize:20}}>{flowDomainData.emoji}</span>
                <div>
                  <div style={{fontSize:13,fontWeight:800,color:t.text}}>{flowDomainData.label} Domain Flow</div>
                  <div style={{fontSize:10,color:t.textMuted}}>{flowDomainData.desc}</div>
                </div>
              </div>

              {/* Flux → Lead */}
              <div style={{display:'flex',alignItems:'center',gap:8,marginBottom:12}}>
                <div style={{background:`${acc}15`,border:`1.5px solid ${acc}30`,borderRadius:8,padding:'8px 14px',textAlign:'center',minWidth:80}}>
                  <div style={{fontSize:14}}>⚡</div>
                  <div style={{fontSize:10,fontWeight:700,color:acc}}>Flux</div>
                </div>
                <div style={{display:'flex',flexDirection:'column',alignItems:'center',flex:1}}>
                  <div style={{height:1,width:'100%',background:`${flowDomainData.color}40`}}/>
                  <div style={{fontSize:9,color:t.textMuted,marginTop:2}}>taak → {flowDomainData.lead}</div>
                </div>
                {(() => {
                  const lead = flowDomainData.agents.find(a => a.id === flowDomainData.lead)
                  return (
                    <div style={{background:`${flowDomainData.color}20`,border:`1.5px solid ${flowDomainData.color}50`,borderRadius:8,padding:'8px 14px',textAlign:'center',minWidth:100}}>
                      <div style={{fontSize:16}}>{lead?.emoji}</div>
                      <div style={{fontSize:11,fontWeight:700,color:flowDomainData.color}}>{lead?.name}</div>
                      <div style={{fontSize:9,color:t.textMuted}}>Omni Lead</div>
                    </div>
                  )
                })()}
              </div>

              {/* Lead → Sentinels */}
              <div style={{marginLeft:80}}>
                <div style={{fontSize:9,color:t.textMuted,marginBottom:8,display:'flex',alignItems:'center',gap:6}}>
                  <div style={{width:1,height:12,background:`${flowDomainData.color}40`}}/>
                  delegeert naar sentinels
                </div>
                <div style={{display:'grid',gridTemplateColumns:'repeat(auto-fill, minmax(160px,1fr))',gap:8}}>
                  {flowDomainData.agents.filter(a => a.id !== flowDomainData.lead).map(agent => {
                    const tierColor = TC[agent.tier]
                    return (
                      <div key={agent.id} style={{background:t.bgSecondary,border:`1px solid ${flowDomainData.color}20`,borderLeft:`3px solid ${flowDomainData.color}`,borderRadius:8,padding:'9px 11px'}}>
                        <div style={{display:'flex',alignItems:'center',gap:6,marginBottom:4}}>
                          <span style={{fontSize:14}}>{agent.emoji}</span>
                          <div style={{flex:1}}>
                            <div style={{fontSize:11,fontWeight:700,color:t.text}}>{agent.name}</div>
                            <div style={{fontSize:8,color:flowDomainData.color,textTransform:'uppercase'}}>{agent.role}</div>
                          </div>
                          <span style={{fontSize:8,color:tierColor,background:`${tierColor}15`,borderRadius:3,padding:'1px 4px'}}>T{agent.tier}</span>
                        </div>
                        {agent.workflows?.slice(0,2).map((w,i) => (
                          <div key={i} style={{fontSize:8,color:t.textMuted,display:'flex',gap:3,alignItems:'center',marginBottom:1}}>
                            <div style={{width:3,height:3,borderRadius:'50%',background:flowDomainData.color,flexShrink:0}}/>
                            {w.split(' — ')[0]}
                          </div>
                        ))}
                        {agent.workers?.length > 0 && (
                          <div style={{marginTop:4,fontSize:8,color:'#22c55e',fontFamily:'monospace'}}>
                            {agent.workers.map(w => w.name).join(', ')}
                          </div>
                        )}
                      </div>
                    )
                  })}
                </div>
              </div>

              {/* Status flow omhoog */}
              <div style={{marginTop:12,padding:'8px 12px',background:`${flowDomainData.color}08`,borderRadius:8,display:'flex',alignItems:'center',gap:8}}>
                <i className="ti ti-arrow-up" style={{fontSize:12,color:flowDomainData.color}}/>
                <span style={{fontSize:10,color:t.textMuted}}>Status rapportages stromen omhoog: Sentinels → {flowDomainData.agents.find(a=>a.id===flowDomainData.lead)?.name} → Flux → Nova → Supreme Fea</span>
              </div>
            </div>
          )}
        </>}
      </div>
    </div>
  )
}
