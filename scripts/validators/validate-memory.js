#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

class MemoryValidator {
  constructor(options = {}) {
    this.verbose = options.verbose || false;
    this.agentsPath = path.join(process.env.HOME, 'arc_ai_angels/agents');
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

  validateFile(filePath) {
    const result = {
      file: filePath,
      agentName: this.extractAgentName(filePath),
      valid: true,
      errors: [],
      warnings: [],
      score: 100,
      size: 0,
      learningsCount: 0
    };

    try {
      const content = fs.readFileSync(filePath, 'utf-8');
      result.size = content.length;

      if (!content.includes('# MEMORY')) {
        result.errors.push('Missing # MEMORY header');
        result.valid = false;
        result.score -= 20;
      }

      if (!content.includes('## Structure Rules')) {
        result.errors.push('Missing ## Structure Rules');
        result.valid = false;
        result.score -= 20;
      }

      if (!content.includes('## Learnings')) {
        result.errors.push('Missing ## Learnings');
        result.valid = false;
        result.score -= 20;
      }

      const learningsMatch = content.match(/## Learnings\s*([\s\S]*?)$/);
      if (learningsMatch) {
        const learnings = learningsMatch[1].split('\n').filter(l => l.trim().startsWith('-'));
        result.learningsCount = learnings.length;

        if (learnings.length === 0) {
          result.warnings.push('No learnings found');
          result.score -= 10;
        }
      }

      if (result.size > 5000) {
        result.warnings.push('File too large (' + result.size + ' bytes, max 5KB)');
        result.score -= 15;
      }

      if (result.size < 300) {
        result.warnings.push('File too small (' + result.size + ' bytes, recommend >300)');
        result.score -= 5;
      }

      const lines = content.split('\n');
      const dupeWords = {};
      for (const line of lines) {
        if (line.trim().startsWith('-')) {
          const first10 = line.substring(0, 30).toLowerCase();
          if (dupeWords[first10]) {
            result.warnings.push('Possible duplicate: ' + line.substring(0, 40));
            result.score -= 5;
          }
          dupeWords[first10] = true;
        }
      }

      result.score = Math.max(0, result.score);

    } catch (error) {
      result.valid = false;
      result.errors.push('Error reading file');
      result.score = 0;
    }

    return result;
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

  validateAll() {
    const files = this.findAllMemories();
    if (files.length === 0) {
      console.error('No MEMORY.md files found!');
      process.exit(1);
    }

    console.log('Found ' + files.length + ' MEMORY.md files\n');

    const results = [];
    let totalSize = 0;
    let totalLearnings = 0;

    for (const file of files) {
      const result = this.validateFile(file);
      results.push(result);
      totalSize += result.size;
      totalLearnings += result.learningsCount;

      if (this.verbose) {
        const status = result.valid ? 'OK' : 'FAIL';
        console.log(status + ' ' + result.agentName.padEnd(20) + ' [' + result.score + '/100] ' + result.size + 'B ' + result.learningsCount + 'L');
      }
    }

    this.renderReport(results, totalSize, totalLearnings);
    return results;
  }

  renderReport(results, totalSize, totalLearnings) {
    const valid = results.filter(r => r.valid).length;
    const invalid = results.filter(r => !r.valid).length;
    const avgScore = Math.round(results.reduce((sum, r) => sum + r.score, 0) / results.length);
    const avgSize = Math.round(totalSize / results.length);

    console.log('='.repeat(80));
    console.log('MEMORY.md Validation Report');
    console.log('='.repeat(80));
    console.log('');
    console.log('Valid: ' + valid + '/' + results.length);
    console.log('Invalid: ' + invalid + '/' + results.length);
    console.log('Average Score: ' + avgScore + '/100');
    console.log('');
    console.log('Memory Usage:');
    console.log('  Total: ' + (totalSize / 1024).toFixed(2) + 'KB');
    console.log('  Average: ' + avgSize + 'B per agent');
    console.log('  Total Learnings: ' + totalLearnings);
    console.log('');
    console.log('Details:');
    console.log('-'.repeat(80));

    results.forEach(r => {
      console.log((r.valid ? 'OK' : 'FAIL') + ' ' + r.agentName.padEnd(20) + ' [' + r.score + '/100] ' + r.size + 'B ' + r.learningsCount + 'L');
      if (r.errors.length > 0) {
        r.errors.forEach(e => console.log('  ERROR: ' + e));
      }
      if (r.warnings.length > 0) {
        r.warnings.forEach(w => console.log('  WARN: ' + w));
      }
    });

    console.log('='.repeat(80));
    if (invalid > 0) {
      console.log('');
      console.log('WARNING: ' + invalid + ' agents need attention!');
    } else {
      console.log('');
      console.log('SUCCESS: All agents MEMORY.md files are valid!');
    }
  }
}

const args = process.argv.slice(2);
const options = { verbose: args.includes('--verbose') };
const validator = new MemoryValidator(options);
validator.validateAll();
