#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

class JournalToMemoryConsolidator {
  constructor(options = {}) {
    this.agentsPath = path.join(process.env.HOME, 'arc_ai_angels/agents');
    this.verbose = options.verbose || false;
    this.dryRun = options.dryRun !== false;
    this.results = {
      processed: 0,
      moved: 0,
      totalLearnings: 0,
      errors: []
    };
  }

  findAllAgents() {
    try {
      const dirs = fs.readdirSync(this.agentsPath);
      return dirs.filter(d => {
        const stat = fs.statSync(path.join(this.agentsPath, d));
        return stat.isDirectory() && d !== 'omni' && d !== '.backups';
      });
    } catch (error) {
      return ['nova', 'flux'];
    }
  }

  processJournalForAgent(agentName) {
    const journalPath = path.join(this.agentsPath, agentName, 'JOURNAL');
    const openDir = path.join(journalPath, 'open');
    const closedDir = path.join(journalPath, 'closed');
    const memoryFile = path.join(this.agentsPath, agentName, 'MEMORY.md');

    if (!fs.existsSync(openDir) || !fs.existsSync(memoryFile)) {
      return { processed: 0, moved: 0, learnings: 0 };
    }

    let processed = 0;
    let moved = 0;
    let newLearnings = 0;

    try {
      const openFiles = fs.readdirSync(openDir).filter(f => f.endsWith('.md'));

      for (const file of openFiles) {
        const filePath = path.join(openDir, file);
        const content = fs.readFileSync(filePath, 'utf-8');

        processed++;

        const learnings = this.extractLearnings(content);
        if (learnings.length > 0) {
          this.addToMemory(memoryFile, learnings);
          newLearnings += learnings.length;
        }

        if (!this.dryRun) {
          const closedPath = path.join(closedDir, file);
          fs.renameSync(filePath, closedPath);
          moved++;
        } else {
          moved++;
        }

        if (this.verbose) {
          console.log('  ' + file + ' → ' + learnings.length + ' learnings');
        }
      }

    } catch (error) {
      this.results.errors.push(agentName + ': ' + error.message);
    }

    return { processed, moved, learnings: newLearnings };
  }

  extractLearnings(content) {
    const learnings = [];
    const lines = content.split('\n');

    for (const line of lines) {
      if (line.trim().startsWith('-') && line.length > 10 && line.length < 120) {
        const learning = line.trim();
        if (!learning.includes('TODO') && !learning.includes('FIXME')) {
          learnings.push(learning);
        }
      }
    }

    return learnings.slice(0, 3);
  }

  addToMemory(memoryFile, learnings) {
    let content = fs.readFileSync(memoryFile, 'utf-8');
    const lines = content.split('\n');

    const learningsIndex = lines.findIndex(l => l.includes('## Learnings'));
    if (learningsIndex === -1) {
      return;
    }

    const existingSet = new Set();
    for (let i = learningsIndex + 1; i < lines.length; i++) {
      if (lines[i].trim().startsWith('-')) {
        existingSet.add(lines[i].trim().toLowerCase());
      } else if (lines[i].trim().startsWith('##')) {
        break;
      }
    }

    const newLines = [];
    for (const learning of learnings) {
      if (!existingSet.has(learning.toLowerCase())) {
        newLines.push(learning);
      }
    }

    if (newLines.length > 0) {
      const insertIndex = learningsIndex + 1;
      const updated = [
        ...lines.slice(0, insertIndex),
        ...newLines,
        ...lines.slice(insertIndex)
      ].join('\n');

      if (!this.dryRun) {
        fs.writeFileSync(memoryFile, updated, 'utf-8');
      }
    }
  }

  consolidateOmniAgents() {
    const omniPath = path.join(this.agentsPath, 'omni');
    if (!fs.existsSync(omniPath)) {
      return;
    }

    const domains = ['finix', 'helix', 'matrix', 'quantix', 'zenix'];
    for (const domain of domains) {
      const domainPath = path.join(omniPath, domain);
      if (!fs.existsSync(domainPath)) continue;

      const leadDir = fs.readdirSync(domainPath).find(d => d.includes('lead agent'));
      const sentinelDir = path.join(domainPath, 'sentinels');

      if (leadDir) {
        this.processJournalForOmniAgent(path.join(domainPath, leadDir));
      }

      if (fs.existsSync(sentinelDir)) {
        const sentinels = fs.readdirSync(sentinelDir);
        for (const sentinel of sentinels) {
          this.processJournalForOmniAgent(path.join(sentinelDir, sentinel));
        }
      }
    }
  }

  processJournalForOmniAgent(agentPath) {
    const journalPath = path.join(agentPath, 'JOURNAL');
    const openDir = path.join(journalPath, 'open');
    const closedDir = path.join(journalPath, 'closed');
    const memoryFile = path.join(agentPath, 'MEMORY.md');

    if (!fs.existsSync(openDir) || !fs.existsSync(memoryFile)) {
      return;
    }

    try {
      const openFiles = fs.readdirSync(openDir).filter(f => f.endsWith('.md'));

      for (const file of openFiles) {
        const filePath = path.join(openDir, file);
        const content = fs.readFileSync(filePath, 'utf-8');

        const learnings = this.extractLearnings(content);
        if (learnings.length > 0) {
          this.addToMemory(memoryFile, learnings);
          this.results.totalLearnings += learnings.length;
        }

        if (!this.dryRun) {
          const closedPath = path.join(closedDir, file);
          fs.renameSync(filePath, closedPath);
        }

        this.results.moved++;
      }
    } catch (error) {
      this.results.errors.push(agentPath + ': ' + error.message);
    }
  }

  consolidateAll() {
    console.log('JOURNAL → MEMORY Consolidation');
    console.log('='.repeat(80));
    console.log('');

    if (this.dryRun) {
      console.log('DRY RUN MODE - No files will be modified');
      console.log('');
    }

    const agents = this.findAllAgents();
    console.log('Processing ' + agents.length + ' core agents...');

    for (const agent of agents) {
      const result = this.processJournalForAgent(agent);
      if (result.processed > 0) {
        console.log('✅ ' + agent + ': ' + result.processed + ' entries, ' + result.learnings + ' learnings');
        this.results.processed += result.processed;
        this.results.moved += result.moved;
        this.results.totalLearnings += result.learnings;
      }
    }

    console.log('');
    console.log('Processing Omni agents (Lead + Sentinels)...');
    this.consolidateOmniAgents();

    console.log('');
    console.log('='.repeat(80));
    console.log('Consolidation Summary');
    console.log('='.repeat(80));
    console.log('Total entries processed: ' + this.results.processed);
    console.log('Entries moved to /closed: ' + this.results.moved);
    console.log('Learnings extracted to MEMORY: ' + this.results.totalLearnings);

    if (this.results.errors.length > 0) {
      console.log('');
      console.log('Errors:');
      this.results.errors.forEach(e => console.log('  - ' + e));
    }

    if (this.dryRun) {
      console.log('');
      console.log('DRY RUN - Use --commit to apply changes');
    } else {
      console.log('');
      console.log('✅ CONSOLIDATION COMPLETE');
    }
  }
}

const args = process.argv.slice(2);
const options = {
  dryRun: !args.includes('--commit'),
  verbose: args.includes('--verbose')
};

const consolidator = new JournalToMemoryConsolidator(options);
consolidator.consolidateAll();
