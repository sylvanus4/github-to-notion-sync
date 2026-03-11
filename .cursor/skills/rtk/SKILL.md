---
name: rtk
description: >-
  Manage RTK (Rust Token Killer) CLI proxy for token-optimized command
  execution. Use when the user asks to "check token savings", "rtk gain",
  "optimize tokens", "reduce token usage", "rtk discover", "rtk status",
  "토큰 절감", "토큰 사용량", "RTK 상태", "RTK 분석",
  or wants to view/manage RTK analytics and configuration.
  Do NOT use for general shell commands — the rtk-token-optimization
  rule handles auto-prefixing transparently.
metadata:
  author: thaki
  version: 1.0.0
---

# RTK — Token Optimization Proxy Management

RTK compresses CLI output before it reaches the LLM context window, reducing token consumption by 60-90%. This skill covers analytics, configuration, and troubleshooting — not command rewriting (handled by the always-on `rtk-token-optimization` rule).

## Workflow

### Step 1: Token Savings Analytics

```bash
rtk gain                    # Summary stats
rtk gain --graph            # ASCII graph (last 30 days)
rtk gain --daily            # Day-by-day breakdown
rtk gain --history          # Recent command history
rtk gain --all --format json  # JSON export for dashboards
```

Present the results in Korean with:
- Total tokens saved (absolute number and percentage)
- Top 5 commands by savings
- Trend over the last 7 days
- Comparison to previous period if data available

### Step 2: Discover Optimization Opportunities

```bash
rtk discover                # Current project
rtk discover --all          # All projects
rtk discover --all --since 7  # All projects, last 7 days
```

For each opportunity found:
1. Show the command that could benefit from RTK
2. Estimate potential token savings
3. Confirm whether the command is already covered by the `rtk-token-optimization` rule

### Step 3: Health Check

Run these commands and report status:

```bash
rtk --version               # Should show rtk 0.27.x
which rtk                   # Should be in PATH
rtk gain                    # Should not error
```

Check configuration file exists:
- macOS: `~/Library/Application Support/rtk/config.toml`
- Linux: `~/.config/rtk/config.toml`

Verify the `rtk-token-optimization` Cursor rule is loaded by checking:
- `.cursor/rules/rtk-token-optimization.mdc` exists and has `alwaysApply: true`

### Step 4: Configuration

**Config file location** (macOS): `~/Library/Application Support/rtk/config.toml`

Available settings:

```toml
[tracking]
database_path = "~/.local/share/rtk/history.db"

[hooks]
exclude_commands = ["curl", "playwright"]

[tee]
enabled = true
mode = "failures"   # "failures" | "always" | "never"
max_files = 20
```

| Setting | Default | Description |
|---------|---------|-------------|
| `tracking.database_path` | `~/.local/share/rtk/history.db` | Token savings database |
| `hooks.exclude_commands` | `[]` | Commands to skip rewriting |
| `tee.enabled` | `true` | Save full output on failure |
| `tee.mode` | `"failures"` | When to save: failures, always, never |
| `tee.max_files` | `20` | Max tee log rotation |

### Step 5: Troubleshooting

| Problem | Diagnosis | Fix |
|---------|-----------|-----|
| `rtk: command not found` | Not in PATH | `brew install rtk` or add `~/.local/bin` to PATH |
| `rtk gain` shows no data | No rtk commands run yet | Start using `rtk` prefix on commands |
| Wrong `rtk` binary (Rust Type Kit) | `rtk gain` shows unknown command | `cargo uninstall rtk && brew install rtk` |
| Tee logs filling disk | Too many saved outputs | Set `tee.max_files` lower or `tee.mode = "failures"` |
| RTK adds latency | Rarely — RTK adds <10ms | Check with `time rtk git status` vs `time git status` |
| Compressed output missing info | RTK filtered too aggressively | Read tee log: `~/.local/share/rtk/tee/<timestamp>_<cmd>.log` |

## Examples

### Example 1: Weekly savings review

User says: "이번 주 토큰 절감 현황 보여줘"

Actions:
1. `rtk gain --daily` — show daily breakdown
2. `rtk gain --graph` — show trend graph
3. Summarize in Korean: "이번 주 총 X 토큰 절감 (Y%), 가장 효과적인 명령: git diff (-85%)"

### Example 2: Discover missed opportunities

User says: "/rtk discover"

Actions:
1. `rtk discover --all --since 7` — scan all projects
2. List commands not using RTK that could benefit
3. Suggest adding any missing commands to the rule mapping

### Example 3: Troubleshoot RTK

User says: "RTK가 안 되는 것 같아"

Actions:
1. `rtk --version` — verify binary
2. `which rtk` — verify PATH
3. `rtk gain` — verify database
4. Check `.cursor/rules/rtk-token-optimization.mdc` exists
5. Report findings and fix
