# NOVA Response Format Standard

## Cronjob Creation Response

### Format (Machine + Human Readable)
✅ CRONJOB CREATED
Task: [TASK_NAME]
Agent: [AGENT]
Schedule: [CRON_EXPR] ([HUMAN_READABLE])
Next Execution: [DATETIME_ISO]
Status: [pending|active|error]
Validation: [VALIDATED|AWAITING_EXECUTION]
Actions Taken:

Cronjob added to OpenClaw
Forwarded to [NEXT_AGENT]
Added to monitoring queue

Next Steps:

Execution: [DATE TIME]
Monitor: OpenClaw dashboard
Report: Post-execution status

Ref: [SESSION_ID] | [CRONJOB_ID]

### Example (Your Test)
✅ CRONJOB CREATED
Task: FORGE Test 2026-05-28
Agent: FORGE
Schedule: "2026-05-28 00:15:00" (One-time, 28 mei 00:15 CET)
Next Execution: 2026-05-28T00:15:00+02:00
Status: active
Validation: AWAITING_EXECUTION
Actions Taken:

Cronjob created via openclaw cron add
Validated with validate_cronjob.sh ✓
Added to monitoring: OpenClaw dashboard
Forwarded to FLUX for orchestration

Next Steps:

Execution: 2026-05-28 00:15 CET
Monitor: http://127.0.0.1:50506 (Sessions > FORGE)
Report: Post-execution in Telegram

Ref: SESSION_2026-05-27 | cronjob-forge-test-20260528

## Response Elements (Required)

- ✅ Status icon (✅/⏳/❌)
- ✅ Task name & agent
- ✅ Schedule (machine + human)
- ✅ Next execution (ISO format)
- ✅ Current status
- ✅ Actions taken (numbered)
- ✅ Next steps
- ✅ Reference ID

## Use This For All:
- Cronjob creation
- Status queries
- Error reports
- Monitoring updates

