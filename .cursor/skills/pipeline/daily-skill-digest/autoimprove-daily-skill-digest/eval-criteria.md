# Synthetic Eval Criteria for daily-skill-digest

## Binary Checks (pass/fail)

1. **EXEC_COMMAND**: Does the skill clearly specify the exact shell command to run? (yes/no)
2. **OUTPUT_SCHEMA**: Does the skill document the expected JSON fields the agent must read? (yes/no)
3. **KOREAN_TEMPLATE**: Does the skill provide a complete Slack mrkdwn template with all sections? (yes/no)
4. **EDGE_ZERO**: Does the skill explicitly handle zero-transcript and zero-commit edge cases? (yes/no)
5. **CATEGORY_MAPPING**: Does the skill map skill categories to Korean pattern characterizations? (yes/no)
6. **OMIT_EMPTY**: Does the skill instruct to omit sections with zero items rather than showing empty sections? (yes/no)

## Test Scenarios

### Scenario A: Standard full-day run (multi-project, many skills)
- Expected: Full output with all sections populated
- Key eval: All 6 binary checks should pass

### Scenario B: Zero transcripts day
- Expected: Minimal ":bar_chart:" message with "오늘 에이전트 세션이 없습니다."
- Key eval: EDGE_ZERO must pass

### Scenario C: Single-project filter (--project=ai-platform)
- Expected: Omit "Per-Project Activity" section
- Key eval: Skill must specify single-project behavior

### Scenario D: Pipeline invocation via eod-ship
- Expected: Return mrkdwn string (do NOT post to Slack directly)
- Key eval: Skill must differentiate standalone vs pipeline behavior

### Scenario E: Multi-project with one project having zero skills
- Expected: Show project in Per-Project Activity with 0 skills
- Key eval: EDGE_ZERO must cover partial-empty scenarios
