# Tmux Session Manager

Manage tmux sessions for long-running development processes.

## Usage

```bash
# Create a new session with a command
/tmux new devserver "python -m uvicorn backend.app.main:app --reload"

# List all sessions
/tmux list

# Send a command to a session
/tmux send devserver "echo hello"

# Capture recent output from a session
/tmux capture devserver

# Kill a session
/tmux kill devserver
```

## Instructions

Use the `tmux-session-manager` skill to execute this command. Read the skill at `.cursor/skills/standalone/tmux-session-manager/SKILL.md` and follow its workflow.

Key points:
- Sessions are named `{project}-{purpose}` by default
- Always create detached sessions (`-d` flag) so the agent maintains control
- Use `capture` to inspect output without attaching to the session
- Verify tmux is installed before any operation
