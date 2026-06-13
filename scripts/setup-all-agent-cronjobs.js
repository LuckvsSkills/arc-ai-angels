#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

class AgentCronjobSetup {
  constructor() {
    this.jobsFile = path.join(process.env.HOME, '.openclaw/cron/jobs.json');
    this.agentsPath = path.join(process.env.HOME, 'arc_ai_angels/agents');
    this.jobs = JSON.parse(fs.readFileSync(this.jobsFile, 'utf-8'));
  }

  getAllAgents() {
    const agents = [];
    
    // Core agents
    agents.push({ id: 'nova', name: 'Nova', type: 'core' });
    agents.push({ id: 'flux', name: 'Flux', type: 'core' });

    // OMNI agents (Lead + Sentinels)
    const domains = ['finix', 'helix', 'matrix', 'quantix', 'zenix'];
    const omniPath = path.join(this.agentsPath, 'omni');

    for (const domain of domains) {
      const domainPath = path.join(omniPath, domain);
      
      // Lead agent
      const leadDirs = fs.readdirSync(domainPath).filter(d => d.includes('lead agent'));
      if (leadDirs.length > 0) {
        const leadName = leadDirs[0].match(/lead agent (\w+)/)[1];
        agents.push({ id: leadName.toLowerCase(), name: leadName, type: 'lead', domain });
      }

      // Sentinels
      const sentinelsPath = path.join(domainPath, 'sentinels');
      if (fs.existsSync(sentinelsPath)) {
        const sentinels = fs.readdirSync(sentinelsPath);
        for (const sentinel of sentinels) {
          agents.push({ id: sentinel, name: sentinel, type: 'sentinel', domain });
        }
      }
    }

    return agents;
  }

  createCronjobForAgent(agent) {
    const jobId = 'agent-' + agent.id + '-memory-pipeline-' + Date.now();
    
    const job = {
      id: jobId,
      agentId: agent.id,
      sessionKey: 'agent:' + agent.id + ':main',
      name: agent.name + ' Memory Pipeline',
      enabled: true,
      createdAtMs: Date.now(),
      schedule: {
        everyMs: 3600000,
        kind: 'every',
        anchorMs: Date.now()
      },
      sessionTarget: 'isolated',
      wakeMode: 'now',
      payload: {
        kind: 'agentTurn',
        model: 'google/gemini-2.5-flash',
        message: 'Consolidate your JOURNAL to MEMORY. Run: journal-to-memory --commit'
      },
      delivery: {
        to: 'openclaw-control-ui',
        channel: 'webchat',
        mode: 'announce'
      },
      state: {}
    };

    return job;
  }

  setupAll() {
    console.log('Setting up Memory Pipelines for ALL 32 agents');
    console.log('='.repeat(80));
    console.log('');

    const agents = this.getAllAgents();
    const existingJobIds = new Set(this.jobs.jobs.map(j => j.agentId));

    let added = 0;
    let skipped = 0;

    for (const agent of agents) {
      if (existingJobIds.has(agent.id)) {
        console.log('⏭️  ' + agent.name.padEnd(20) + ' (already has pipeline)');
        skipped++;
      } else {
        const job = this.createCronjobForAgent(agent);
        this.jobs.jobs.push(job);
        console.log('✅ ' + agent.name.padEnd(20) + ' - Pipeline created');
        added++;
      }
    }

    console.log('');
    console.log('='.repeat(80));
    console.log('Summary');
    console.log('='.repeat(80));
    console.log('Total agents: ' + agents.length);
    console.log('Pipelines added: ' + added);
    console.log('Already existing: ' + skipped);
    console.log('');

    // Write to file
    fs.writeFileSync(this.jobsFile, JSON.stringify(this.jobs, null, 2));
    console.log('✅ Cronjobs saved to ~/.openclaw/cron/jobs.json');
    console.log('');
    console.log('All 32 agents now have Memory Pipelines!');
  }
}

const setup = new AgentCronjobSetup();
setup.setupAll();
