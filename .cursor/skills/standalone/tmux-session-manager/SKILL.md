---
name: tmux-session-manager
version: 1.0.0
description: "Manage tmux sessions for long-running development processes — create named sessions, split panes, send commands, capture output, and monitor background processes."
---

# Tmux Session Manager

Manage tmux sessions for long-running development processes (dev servers, test watchers, database processes) that persist across agent context windows. Provides structured session lifecycle management.

## Trigger Phrases

- "tmux", "tmux session", "background process", "long-running command"
- "tmux 세션", "백그라운드 프로세스", "장시간 명령"
- `/tmux` command

## Do NOT Use For

- Short-lived commands that complete quickly (run directly via Shell)
- Docker container management (use `local-dev-runner` or `sre-devops-expert`)
- CI/CD pipeline execution (use `ci-quality-gate`)
- Process monitoring dashboards (use `service-health-doctor`)

## Prerequisites

- `tmux` must be installed (`brew install tmux` on macOS)
- Run `which tmux` to verify availability before operations

## Session Naming Convention

Format: `{project}-{purpose}`

Examples:
- `stock-analytics-devserver`
- `stock-analytics-tests`
- `stock-analytics-db`

## Operations

### 1. Create Session (`new`)

Create a new named tmux session and optionally run a command:

```bash
tmux new-session -d -s {session-name} -c {working-directory}
tmux send-keys -t {session-name} '{command}' Enter
```

Always create detached (`-d`) so the agent maintains control.

### 2. List Sessions (`list`)

```bash
tmux list-sessions 2>/dev/null || echo "No active tmux sessions"
```

### 3. Send Command (`send`)

Send a command to a running session:

```bash
tmux send-keys -t {session-name} '{command}' Enter
```

### 4. Capture Output (`capture`)

Capture the current pane output for inspection:

```bash
tmux capture-pane -t {session-name} -p -S -50
```

The `-S -50` captures the last 50 lines. Adjust as needed.

### 5. Kill Session (`kill`)

```bash
tmux kill-session -t {session-name}
```

### 6. Split Pane

Split the session into multiple panes for parallel monitoring:

```bash
tmux split-window -t {session-name} -h  # horizontal split
tmux split-window -t {session-name} -v  # vertical split
```

## Workflow

### Step 1: Check tmux Availability
```bash
which tmux
```
If not found, inform the user and suggest installation.

### Step 2: Execute Requested Operation
Based on the subcommand (`new`, `list`, `send`, `capture`, `kill`), run the appropriate tmux commands.

### Step 3: Verify
- After `new`: confirm session exists with `tmux has-session -t {name} 2>/dev/null && echo "OK"`
- After `send`: capture a few lines of output to confirm the command ran
- After `kill`: confirm session is gone

### Step 4: Report
Provide a concise status update:
```
tmux session 'stock-analytics-devserver' created
  Working dir: /Users/.../ai-model-event-stock-analytics
  Running: python -m uvicorn backend.app.main:app --reload
  Status: Active
```

## Common Patterns

### Dev Server Pattern
```bash
tmux new-session -d -s dev -c /path/to/project
tmux send-keys -t dev 'python -m uvicorn backend.app.main:app --reload --port 8000' Enter
```

### Test Watcher Pattern
```bash
tmux new-session -d -s tests -c /path/to/project
tmux send-keys -t tests 'pytest-watch -- -x --tb=short' Enter
```

### Multi-Pane Dashboard Pattern
```bash
tmux new-session -d -s dashboard -c /path/to/project
tmux send-keys -t dashboard 'python -m uvicorn backend.app.main:app --reload' Enter
tmux split-window -t dashboard -h
tmux send-keys -t dashboard 'tail -f logs/app.log' Enter
tmux split-window -t dashboard -v
tmux send-keys -t dashboard 'htop' Enter
```

## Examples

### Example 1: Start Dev Server
```
User: "Start the dev server in tmux"
Agent: Creates session 'stock-analytics-devserver' → Runs uvicorn → Confirms running
```

### Example 2: Check Running Sessions
```
User: "/tmux list"
Agent: Lists all active tmux sessions with names and status
```

### Example 3: Capture Server Output
```
User: "What's the dev server showing?"
Agent: Captures last 50 lines from the dev session → Displays output
```

## Error Handling

- If tmux is not installed, report with installation instructions
- If a session name already exists on `new`, inform the user and offer to reuse or rename
- If a session doesn't exist on `send`/`capture`/`kill`, report that it's not found
- If tmux server is not running (no sessions), handle gracefully on `list`
