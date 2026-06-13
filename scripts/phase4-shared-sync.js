#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

class SharedMemorySync {
  constructor() {
    this.agentsPath = path.join(process.env.HOME, 'arc_ai_angels/agents');
    this.sharedPath = path.join(process.env.HOME, 'arc_ai_angels/shared/memory');
    this.logPath = path.join(this.sharedPath, 'sync.log');
  }

  syncAgentLearningsToShared() {
    console.log('Phase 4: Agent Learning Synchronization');
    console.log('='.repeat(80));
    console.log('');

    let totalLearnings = 0;
    let agentsProcessed = 0;
    const timestamp = new Date().toISOString();

    // Collect all agent learnings
    const allLearnings = {};

    // Core agents
    for (const agentId of ['nova', 'flux']) {
      const learning = this.extractAgentLearnings(agentId);
      if (learning) {
        allLearnings[agentId] = learning;
        totalLearnings += learning.count;
        agentsProcessed++;
      }
    }

    // Omni agents
    const omniPath = path.join(this.agentsPath, 'omni');
    const domains = ['finix', 'helix', 'matrix', 'quantix', 'zenix'];

    for (const domain of domains) {
      const domainPath = path.join(omniPath, domain);
      if (!fs.existsSync(domainPath)) continue;

      // Lead agents
      const leadDirs = fs.readdirSync(domainPath).filter(d => d.includes('lead agent'));
      for (const leadDir of leadDirs) {
        const leadName = leadDir.match(/lead agent (\w+)/)[1].toLowerCase();
        const learning = this.extractAgentLearnings(leadName);
        if (learning) {
          allLearnings[leadName] = learning;
          totalLearnings += learning.count;
          agentsProcessed++;
        }
      }

      // Sentinels
      const sentinelsPath = path.join(domainPath, 'sentinels');
      if (fs.existsSync(sentinelsPath)) {
        const sentinels = fs.readdirSync(sentinelsPath);
        for (const sentinel of sentinels) {
          const learning = this.extractAgentLearnings(sentinel);
          if (learning) {
            allLearnings[sentinel] = learning;
            totalLearnings += learning.count;
            agentsProcessed++;
          }
        }
      }
    }

    // Create synchronized view
    const syncReport = {
      timestamp: timestamp,
      agents_processed: agentsProcessed,
      total_learnings: totalLearnings,
      learnings_by_agent: allLearnings,
      domains: this.analyzeDomainPatterns(allLearnings)
    };

    // Update SYSTEM_STATE with sync info
    this.updateSystemState(timestamp, agentsProcessed, totalLearnings);

    // Write sync report
    const reportPath = path.join(this.sharedPath, 'sync-' + timestamp.replace(/[:.]/g, '-') + '.json');
    fs.writeFileSync(reportPath, JSON.stringify(syncReport, null, 2));

    console.log('✅ Agents processed: ' + agentsProcessed);
    console.log('✅ Total learnings synchronized: ' + totalLearnings);
    console.log('✅ Sync report: ' + path.basename(reportPath));
    console.log('');
    console.log('='.repeat(80));
    console.log('Phase 4: Synchronization Complete');
    console.log('='.repeat(80));
  }

  extractAgentLearnings(agentId) {
    let agentPath = path.join(this.agentsPath, agentId, 'MEMORY.md');

    // Check omni agents
    if (!fs.existsSync(agentPath)) {
      const domains = ['finix', 'helix', 'matrix', 'quantix', 'zenix'];
      for (const domain of domains) {
        const leadPath = path.join(
          this.agentsPath,
          'omni',
          domain,
          'lead agent ' + agentId.charAt(0).toUpperCase() + agentId.slice(1),
          'MEMORY.md'
        );
        const sentinelPath = path.join(
          this.agentsPath,
          'omni',
          domain,
          'sentinels',
          agentId,
          'MEMORY.md'
        );

        if (fs.existsSync(leadPath)) {
          agentPath = leadPath;
          break;
        }
        if (fs.existsSync(sentinelPath)) {
          agentPath = sentinelPath;
          break;
        }
      }
    }

    if (!fs.existsSync(agentPath)) {
      return null;
    }

    try {
      const content = fs.readFileSync(agentPath, 'utf-8');
      const learnings = [];
      const lines = content.split('\n');

      for (const line of lines) {
        if (line.trim().startsWith('-') && line.length > 10) {
          learnings.push(line.trim());
        }
      }

      return { count: learnings.length, sample: learnings.slice(0, 3) };
    } catch (error) {
      return null;
    }
  }

  analyzeDomainPatterns(allLearnings) {
    const domains = {
      finix: ['finoria', 'zion', 'kairo', 'kenzo', 'vector', 'odis'],
      helix: ['cortexia', 'ventura', 'clio', 'forge', 'nero', 'axon'],
      matrix: ['saelia', 'arix', 'enki', 'daxio', 'sora', 'tharos'],
      quantix: ['lumeria', 'kresta', 'luvia', 'vondra', 'elora', 'nura'],
      zenix: ['fluentia', 'solis', 'zena', 'draven', 'unia', 'orizon']
    };

    const patterns = {};
    for (const [domain, agents] of Object.entries(domains)) {
      let total = 0;
      for (const agent of agents) {
        if (allLearnings[agent]) {
          total += allLearnings[agent].count;
        }
      }
      patterns[domain] = { agents_with_learning: agents.length, total_learnings: total };
    }

    return patterns;
  }

  updateSystemState(timestamp, agentsProcessed, totalLearnings) {
    const stateFile = path.join(this.sharedPath, 'SYSTEM_STATE.md');
    let content = fs.readFileSync(stateFile, 'utf-8');

    const updated = content.replace(
      /- Last Updated: .*/,
      '- Last Updated: ' + timestamp
    ).replace(
      /- Total Memory Used: .*/,
      '- Total Memory Used: 21KB (agents) + ' + totalLearnings + ' shared learnings'
    );

    fs.writeFileSync(stateFile, updated);
  }
}

const sync = new SharedMemorySync();
sync.syncAgentLearningsToShared();
