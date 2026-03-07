## Google Workspace CLI Setup

Install, authenticate, and configure the Google Workspace CLI for terminal-based Workspace control.

### Usage

```
/gws-setup
```

### Workflow

1. **Install** the gws CLI: `npm install -g @googleworkspace/cli`
2. **Verify** installation: `gws --version`
3. **Authenticate** with Google: `gws auth setup` (or `gws auth login --scopes drive,gmail,calendar`)
4. **Test** a read command: `gws drive files list --params '{"pageSize": 3}'`
5. **Optionally** configure MCP server for AI agent integration

### Execution

Read and follow the `gws-workspace` skill (`.cursor/skills/gws-workspace/SKILL.md`) for detailed instructions, MCP server configuration, troubleshooting, and advanced auth options.
