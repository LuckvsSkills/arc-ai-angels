#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

class HandoffValidator {
  constructor(options = {}) {
    this.verbose = options.verbose || false;
    this.reportFormat = options.report || 'text';
    this.agentsPath = path.join(process.env.HOME, 'arc_ai_angels/agents');
  }

  findAllHandoffs() {
    try {
      const cmd = "find " + this.agentsPath + " -name HANDOFF.md -type f 2>/dev/null | sort";
      const output = execSync(cmd, { encoding: 'utf-8' });
      return output.trim().split('\n').filter(f => f);
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
      score: 100
    };

    try {
      const content = fs.readFileSync(filePath, 'utf-8');
      const sections = ['Current Focus', 'Next Action', 'Blockers', 'Resume Point'];
      
      for (const section of sections) {
        if (!content.includes('## ' + section)) {
          result.errors.push('Missing: ## ' + section);
          result.valid = false;
          result.score -= 25;
        }
      }

      if (content.length < 300) {
        result.warnings.push('File too short');
        result.score -= 5;
      }

      if (!content.toLowerCase().includes('functioneert als')) {
        result.warnings.push('Missing "functioneert als"');
        result.score -= 10;
      }

      if (!content.includes('canon-conform')) {
        result.warnings.push('Missing "canon-conform"');
        result.score -= 5;
      }

      result.score = Math.max(0, result.score);

    } catch (error) {
      result.valid = false;
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
    const files = this.findAllHandoffs();
    if (files.length === 0) {
      console.error('No HANDOFF.md files found!');
      process.exit(1);
    }

    console.log('Found ' + files.length + ' HANDOFF.md files\n');

    const results = [];
    for (const file of files) {
      const result = this.validateFile(file);
      results.push(result);
      if (this.verbose) {
        const status = result.valid ? 'OK' : 'FAIL';
        console.log(status + ' ' + result.agentName.padEnd(20) + ' [' + result.score + '/100]');
      }
    }

    this.renderReport(results);
    return results;
  }

  renderReport(results) {
    const valid = results.filter(r => r.valid).length;
    const invalid = results.filter(r => !r.valid).length;
    const avgScore = Math.round(results.reduce((sum, r) => sum + r.score, 0) / results.length);

    console.log('='.repeat(70));
    console.log('HANDOFF.md Validation Report');
    console.log('='.repeat(70));
    console.log('');
    console.log('Valid: ' + valid + '/' + results.length);
    console.log('Invalid: ' + invalid + '/' + results.length);
    console.log('Average Score: ' + avgScore + '/100');
    console.log('');
    console.log('Details:');
    console.log('-'.repeat(70));

    for (const r of results) {
      console.log((r.valid ? 'OK' : 'FAIL') + ' ' + r.agentName.padEnd(20) + ' [' + r.score + '/100]');
      if (r.errors.length > 0) {
        for (const e of r.errors) console.log('  ERROR: ' + e);
      }
      if (r.warnings.length > 0) {
        for (const w of r.warnings) console.log('  WARN: ' + w);
      }
    }

    console.log('='.repeat(70));
    if (invalid > 0) {
      console.log('');
      console.log('WARNING: ' + invalid + ' agents need attention!');
    } else {
      console.log('');
      console.log('SUCCESS: All agents are valid!');
    }
  }
}

const args = process.argv.slice(2);
const options = { verbose: args.includes('--verbose') };
const validator = new HandoffValidator(options);
validator.validateAll();
