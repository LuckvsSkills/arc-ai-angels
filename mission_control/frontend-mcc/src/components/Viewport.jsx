import React from 'react'
import AgentsView from './views/AgentsView'
import Dashboard from './views/Dashboard'
import OpenClawView from './views/OpenClawView'
import CommsView from './views/CommsView'
import ProjectsView from './views/ProjectsView'
import TasksView from './views/TasksView'
import ModelsView from './views/ModelsView'
import SchedulerView from './views/SchedulerView'
import AnalyticsView from './views/AnalyticsView'
import OmniLeadsView from './views/OmniLeadsView'
import SettingsView from './views/SettingsView'
import SimulationView from './views/SimulationView'

export default function Viewport({ view, theme, setView }) {
  switch (view) {
    case 'agents':     return <AgentsView theme={theme} />
    case 'dashboard':  return <Dashboard theme={theme} />
    case 'openclaw':   return <OpenClawView theme={theme} />
    case 'comms':      return <CommsView theme={theme} />
    case 'projects':   return <ProjectsView theme={theme} />
    case 'tasks':      return <TasksView theme={theme} />
    case 'models':     return <ModelsView theme={theme} />
    case 'tiers':      return <ModelsView theme={theme} />
    case 'kernel':     return <SchedulerView theme={theme} />
    case 'analytics':  return <AnalyticsView theme={theme} />
    case 'omni':       return <OmniLeadsView theme={theme} />
    case 'settings':   return <SettingsView theme={theme} />
    case 'simulation': return <SimulationView theme={theme} />
    case 'canon':
    case 'codex':
    case 'diagrams':
    case 'terminal':
    default: return (
      <div style={{padding:'40px',color:theme?.colors?.textMuted||'#888',textAlign:'center',paddingTop:'80px'}}>
        <i className="ti ti-tools" style={{fontSize:'32px',marginBottom:'16px',display:'block'}} aria-hidden="true"/>
        <div style={{fontSize:'14px'}}>'{view}' — komt eraan</div>
      </div>
    )
  }
}
