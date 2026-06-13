# FORGE Cronjob Setup Plan - Live Test 2026-05-28 00:15 NL Time

## Objective
- NOVA creates & manages FORGE cronjobs
- Test NOVA → cronjob system integration
- First execution: 2026-05-28 00:15 CET (Europe/Amsterdam)
- Monitor in OpenClaw dashboard real-time

## FORGE Cronjobs to Create (9 total)

### Search Phase
1. **FORGE GitHub Searcher**
   - Schedule: 0 7 * * 1,3,5 (Mon/Wed/Fri 07:00)
   - Command: python3 workers/github_searcher.py
   - Output: Searches 7 domains, finds 200-400 repos

### Analysis Phase
2. **FORGE GitHub Analyzer**
   - Schedule: 0 10 * * 3 (Wed 10:00)
   - Command: python3 workers/github_analyzer.py
   - Output: Analyzes & scores repos (TIER1/2/3)

3. **FORGE GitHub Packager**
   - Schedule: 30 10 * * 3 (Wed 10:30)
   - Command: python3 workers/github_packager.py
   - Output: Packages analysis for downstream

4. **FORGE GitHub Validator**
   - Schedule: 0 18 * * 3 (Wed 18:00)
   - Command: python3 workers/github_validator.py
   - Output: Validates all repo data

### Skill Extraction Phase
5. **FORGE Skill Searcher**
   - Schedule: 0 15 * * 3 (Wed 15:00)
   - Command: python3 workers/skill_searcher.py
   - Output: Extracts skills from repos

6. **FORGE Skill Reader**
   - Schedule: 30 15 * * 3 (Wed 15:30)
   - Command: python3 workers/skill_reader.py
   - Output: Reads & analyzes skills

7. **FORGE Skill Security Validator**
   - Schedule: 0 16 * * 3 (Wed 16:00)
   - Command: python3 workers/skill_security_validator.py
   - Output: Security analysis of skills

8. **FORGE Skill Rewriter**
   - Schedule: 30 16 * * 3 (Wed 16:30)
   - Command: python3 workers/skill_rewriter.py
   - Output: Optimizes skill format

9. **FORGE Skill Archiver**
   - Schedule: 0 17 * * 3 (Wed 17:00)
   - Command: python3 workers/skill_archiver.py
   - Output: Archives processed skills

## Live Test Schedule

**2026-05-28 00:15 CET (Europe/Amsterdam)**

Test cronjob (immediate execution):
- Name: "FORGE Test Cronjob 2026-05-28"
- Schedule: 2026-05-28 00:15:00
- Command: echo "FORGE cronjob test executed successfully"
- Monitor: OpenClaw dashboard in real-time

## NOVA Configuration Needed

NOVA must:
1. ✅ Create cronjob via openclaw cron add
2. ✅ Validate via cronjob_add.sh
3. ✅ Monitor execution in dashboard
4. ✅ Report status to Telegram
5. ✅ Handle errors gracefully

## Implementation Steps

1. Send message to @Nova_Lens_bot
2. NOVA creates test cronjob for 2026-05-28 00:15
3. NOVA monitors OpenClaw dashboard
4. Report execution status
5. If success: create all 9 FORGE production cronjobs

## Success Criteria

✅ Test cronjob executes at 00:15 CET
✅ NOVA detects execution in OpenClaw
✅ Execution appears in dashboard
✅ NOVA reports status to Telegram
✅ NOVA ready to create production cronjobs

