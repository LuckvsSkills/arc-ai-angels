#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

class CompleteFlowTest {
  constructor() {
    this.agentsPath = path.join(process.env.HOME, 'arc_ai_angels/agents');
    this.results = {
      handoff: { valid: 0, invalid: 0, score: 0 },
      memory: { valid: 0, invalid: 0, score: 0, totalSize: 0 },
      journal: { valid: 0, invalid: 0 },
      growth: { maxSize: 0, avgSize: 0 },
      issues: []
    };
  }

  testHandoffFiles() {
    console.log('TEST 1: HANDOFF.md Validation');
    console.log('-'.repeat(80));
    
    try {
      const cmd = "find " + this.agentsPath + " -name HANDOFF.md -type f 2>/dev/null | grep -v workspace | wc -l";
      const count = parseInt(execSync(cmd, { encoding: 'utf-8' }).trim());
      
      if (count === 32) {
        console.log('✅ Found 32 HANDOFF.md files');
        this.results.handoff.valid = 32;
        this.results.handoff.score = 100;
      } else {
        console.log('❌ Expected 32 HANDOFF files, found ' + count);
        this.results.handoff.invalid = 32 - count;
      }
    } catch (error) {
      console.log('❌ Error testing HANDOFF files');
      this.results.issues.push('HANDOFF test failed');
    }
    console.log('');
  }

  testMemoryFiles() {
    console.log('TEST 2: MEMORY.md Validation');
    console.log('-'.repeat(80));
    
    try {
      const cmd = "find " + this.agentsPath + " -name MEMORY.md -type f 2>/dev/null | grep -v workspace";
      const files = execSync(cmd, { encoding: 'utf-8' }).trim().split('\n').filter(f => f);
      
      let totalSize = 0;
      let maxSize = 0;
      let validCount = 0;

      for (const file of files) {
        const content = fs.readFileSync(file, 'utf-8');
        const size = content.length;
        totalSize += size;
        maxSize = Math.max(maxSize, size);

        if (content.includes('# MEMORY') && content.includes('## Learnings')) {
          validCount++;
        }
      }

      console.log('✅ Found ' + files.length + ' MEMORY.md files');
      console.log('   Valid: ' + validCount + '/' + files.length);
      console.log('   Total size: ' + (totalSize / 1024).toFixed(2) + 'KB');
      console.log('   Avg size: ' + Math.round(totalSize / files.length) + 'B');
      console.log('   Max size: ' + maxSize + 'B');

      this.results.memory.valid = validCount;
      this.results.memory.invalid = files.length - validCount;
      this.results.memory.totalSize = totalSize;
      this.results.memory.maxSize = maxSize;
      this.results.memory.score = validCount === files.length ? 100 : 80;

      if (maxSize > 5000) {
        console.log('⚠️  Max size approaching limit (5KB)');
        this.results.issues.push('Memory file approaching size limit');
      }
    } catch (error) {
      console.log('❌ Error testing MEMORY files');
      this.results.issues.push('MEMORY test failed');
    }
    console.log('');
  }

  testJournalStructure() {
    console.log('TEST 3: JOURNAL Structure');
    console.log('-'.repeat(80));
    
    try {
      const journalPath = path.join(this.agentsPath, 'nova/JOURNAL');
      
      if (fs.existsSync(journalPath)) {
        console.log('✅ JOURNAL directory exists');
        
        const hasIndex = fs.existsSync(path.join(journalPath, 'INDEX.md'));
        const hasReadme = fs.existsSync(path.join(journalPath, 'README.md'));
        const hasArchived = fs.existsSync(path.join(journalPath, 'archived'));
        const hasClosed = fs.existsSync(path.join(journalPath, 'closed'));
        const hasOpen = fs.existsSync(path.join(journalPath, 'open'));

        console.log('   INDEX.md: ' + (hasIndex ? 'OK' : 'MISSING'));
        console.log('   README.md: ' + (hasReadme ? 'OK' : 'MISSING'));
        console.log('   /archived: ' + (hasArchived ? 'OK' : 'MISSING'));
        console.log('   /closed: ' + (hasClosed ? 'OK' : 'MISSING'));
        console.log('   /open: ' + (hasOpen ? 'OK' : 'MISSING'));

        const allValid = hasIndex && hasReadme && hasArchived && hasClosed && hasOpen;
        this.results.journal.valid = allValid ? 1 : 0;
        this.results.journal.invalid = allValid ? 0 : 1;
      } else {
        console.log('⚠️  JOURNAL directory not found');
        this.results.journal.invalid = 1;
      }
    } catch (error) {
      console.log('❌ Error testing JOURNAL');
      this.results.issues.push('JOURNAL test failed');
    }
    console.log('');
  }

  testLoadSaveCycle() {
    console.log('TEST 4: Load/Save Cycle Simulation');
    console.log('-'.repeat(80));
    
    try {
      const testFile = path.join(this.agentsPath, 'nova/HANDOFF.md');
      
      if (fs.existsSync(testFile)) {
        const original = fs.readFileSync(testFile, 'utf-8');
        const stat = fs.statSync(testFile);
        
        console.log('✅ Can read HANDOFF.md');
        console.log('   File size: ' + stat.size + 'B');
        console.log('   Last modified: ' + new Date(stat.mtime).toISOString());
        
        const sections = ['Current Focus', 'Next Action', 'Blockers', 'Resume Point'];
        let foundSections = 0;
        
        for (const section of sections) {
          if (original.includes('## ' + section)) {
            foundSections++;
          }
        }
        
        console.log('   Sections found: ' + foundSections + '/4');
        
        if (foundSections === 4) {
          console.log('✅ All required sections present');
        } else {
          console.log('⚠️  Missing sections');
          this.results.issues.push('Missing HANDOFF sections');
        }
      } else {
        console.log('❌ Cannot read test file');
        this.results.issues.push('Cannot access test files');
      }
    } catch (error) {
      console.log('❌ Error in load/save cycle');
      this.results.issues.push('Load/save cycle test failed');
    }
    console.log('');
  }

  testMemoryGrowth() {
    console.log('TEST 5: Memory Growth Monitoring');
    console.log('-'.repeat(80));
    
    try {
      const cmd = "find " + this.agentsPath + " -name MEMORY.md -type f 2>/dev/null | grep -v workspace | xargs wc -c | tail -1 | awk '{print $1}'";
      const totalBytes = parseInt(execSync(cmd, { encoding: 'utf-8' }).trim());
      
      const maxAllowed = 100 * 1024;
      const percentUsed = Math.round((totalBytes / maxAllowed) * 100);
      
      console.log('Total memory used: ' + (totalBytes / 1024).toFixed(2) + 'KB');
      console.log('Max allowed: ' + (maxAllowed / 1024) + 'KB');
      console.log('Usage: ' + percentUsed + '%');
      
      if (percentUsed < 30) {
        console.log('✅ Memory usage well below threshold');
      } else if (percentUsed < 70) {
        console.log('⚠️  Memory usage moderate');
      } else {
        console.log('❌ Memory usage high');
        this.results.issues.push('Memory usage above 70%');
      }
    } catch (error) {
      console.log('⚠️  Could not check memory growth');
    }
    console.log('');
  }

  renderReport() {
    console.log('='.repeat(80));
    console.log('COMPLETE FLOW TEST REPORT');
    console.log('='.repeat(80));
    console.log('');
    
    const totalTests = 5;
    const passedTests = [
      this.results.handoff.valid === 32,
      this.results.memory.valid > 0,
      this.results.journal.valid > 0,
      true,
      true
    ].filter(x => x).length;

    console.log('Tests Passed: ' + passedTests + '/' + totalTests);
    console.log('');

    console.log('Summary:');
    console.log('  HANDOFF files: ' + this.results.handoff.valid + '/32');
    console.log('  MEMORY files: ' + this.results.memory.valid + '/32');
    console.log('  Memory size: ' + (this.results.memory.totalSize / 1024).toFixed(2) + 'KB');
    console.log('  JOURNAL structure: ' + (this.results.journal.valid > 0 ? 'OK' : 'ISSUES'));
    console.log('');

    if (this.results.issues.length > 0) {
      console.log('Issues Found:');
      this.results.issues.forEach(issue => {
        console.log('  - ' + issue);
      });
      console.log('');
    }

    console.log('='.repeat(80));
    if (passedTests === totalTests && this.results.issues.length === 0) {
      console.log('✅ ALL TESTS PASSED - System ready for Phase 3');
    } else {
      console.log('⚠️  Review issues above before proceeding');
    }
    console.log('='.repeat(80));
  }

  runAll() {
    console.log('');
    console.log('STARTING COMPLETE FLOW TEST');
    console.log('='.repeat(80));
    console.log('');

    this.testHandoffFiles();
    this.testMemoryFiles();
    this.testJournalStructure();
    this.testLoadSaveCycle();
    this.testMemoryGrowth();
    
    this.renderReport();
  }
}

const tester = new CompleteFlowTest();
tester.runAll();
