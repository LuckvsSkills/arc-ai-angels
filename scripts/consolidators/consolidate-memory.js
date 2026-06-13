#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

class MemoryConsolidator {
  constructor(options = {}) {
    this.dryRun = options.dryRun !== false;
    this.verbose = options.verbose || false;
    this.agentsPath = path.join(process.env.HOME, 'arc_ai_angels/agents');
    this.changes = [];
  }

  findAllMemories() {
    try {
      const cmd = "find " + this.agentsPath + " -name MEMORY.md -type f 2>/dev/null | sort";
      const output = execSync(cmd, { encoding: 'utf-8' });
      return output.trim().split('\n').filter(f => f && !f.includes('workspace/MEMORY'));
    } catch (error) {
      return [];
    }
  }

  extractAgentName(filePath) {
    const parts = filePath.split('/');
    if (filePath.includes('lead agent')) {
      const match = filePath.match(/lead agent (\w+)/);
      return match ? match[1] : 'unknown';
    } else if (filePath.includes('sentinels')) {
      const idx = parts.findIndex(p => p === 'sentinels');
      return idx >= 0 && idx + 1 < parts.length ? parts[idx + 1] : 'unknown';
    } else {
      const idx = parts.findIndex(p => p === 'agents');
      return idx >= 0 && idx + 1 < parts.length ? parts[idx + 1] : 'unknown';
    }
  }

  consolidateFile(filePath) {
    const agent = this.extractAgentName(filePath);
    const content = fs.readFileSync(filePath, 'utf-8');
    const lines = content.split('\n');
    const consolidated = [];
    const seenLearnings = {};
    let inLearnings = false;
    let removed = 0;

    for (const line of lines) {
      if (line.includes('## Learnings')) {
        inLearnings = true;
        consolidated.push(line);
      } else if (inLearnings && line.trim().startsWith('-')) {
        const normalized = line.trim().toLowerCase();
        const first30 = normalized.substring(0, 40);

        if (seenLearnings[first30]) {
          if (this.verbose) {
            console.log('  DUPLICATE: ' + line.substring(0, 50));
          }
          removed++;
        } else {
          consolidated.push(line);
          seenLearnings[first30] = true;
        }
      } else if (line.trim() === '' && inLearnings && consolidated[consolidated.length - 1] && consolidated[consolidated.length - 1].trim() === '') {
        continue;
      } else {
        if (line.includes('##') && !line.includes('## Learnings')) {
          inLearnings = false;
        }
        consolidated.push(line);
      }
    }

    const newContent = consolidated.join('\n').replace(/\n\n\n+/g, '\n\n');

    if (newContent !== content) {
      if (this.dryRun) {
        this.changes.push({
          agent: agent,
          file: filePath,
          action: 'would consolidate',
          removed: removed,
          before: content.length,
          after: newContent.length
        });
        console.log('DRY RUN: ' + agent + ' - would remove ' + removed + ' duplicates');
      } else {
        fs.writeFileSync(filePath, newContent, 'utf-8');
        this.changes.push({
          agent: agent,
          file: filePath,
          action: 'consolidated',
          removed: removed,
          before: content.length,
          after: newContent.length
        });
        console.log('CONSOLIDATE: ' + agent + ' - removed ' + removed + ' duplicates');
      }
    } else {
      if (this.verbose) {
        console.log('OK: ' + agent + ' - clean');
      }
    }
  }

  consolidateAll() {
    const files = this.findAllMemories();
    console.log('Consolidating ' + files.length + ' MEMORY.md files...');
    console.log('');

    if (this.dryRun) {
      console.log('DRY RUN MODE - No files will be modified');
      console.log('');
    }

    for (const file of files) {
      this.consolidateFile(file);
    }

    console.log('');
    console.log('='.repeat(80));
    console.log('Consolidation Summary');
    console.log('='.repeat(80));
    console.log('Files processed: ' + this.changes.length);
    console.log('');

    if (this.dryRun) {
      console.log('DRY RUN - Use --commit to actually apply changes');
    } else {
      const totalRemoved = this.changes.reduce((sum, c) => sum + (c.removed || 0), 0);
      const totalSaved = this.changes.reduce((sum, c) => sum + ((c.before || 0) - (c.after || 0)), 0);
      console.log('Total duplicates removed: ' + totalRemoved);
      console.log('Total bytes saved: ' + totalSaved + 'B');
    }
  }
}

const args = process.argv.slice(2);
const options = {
  dryRun: !args.includes('--commit'),
  verbose: args.includes('--verbose')
};
const consolidator = new MemoryConsolidator(options);
consolidator.consolidateAll();
