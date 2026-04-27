# Synthetic Eval Criteria for codex-image-to-eagle

8 binary evals (PASS=1, FAIL=0). Score = sum / 8.

| ID | Criterion | Pass Condition |
|----|-----------|----------------|
| E1 | Trigger Precision | ≥3 English triggers + Korean triggers + "Use when" + ≥1 "Do NOT use" boundary |
| E2 | Workflow Completeness | Steps cover identify → capture prompt → dry-run → execute → report with exact commands |
| E3 | Safety Pre-flight | Workflow mentions checking Eagle connectivity (--check-connection) BEFORE importing |
| E4 | Self-contained Examples | Examples include the SCRIPT variable or full path so they are copy-pasteable |
| E5 | Missing-prompt Handling | Skill explains what happens when --prompt is omitted (required vs optional) |
| E6 | Exit Code Documentation | Exit codes or return values documented for script automation |
| E7 | Node.js Version | Minimum Node.js version specified in Prerequisites |
| E8 | Error Recovery | ≥5 failure modes with specific actions |
