## MCP Builder

Build high-quality MCP (Model Context Protocol) servers that connect LLMs to external APIs and services. Supports Python (FastMCP) and Node/TypeScript (MCP SDK).

### Usage

```
/mcp-builder <api-name>            # Start MCP server project for an API
/mcp-builder --python <api-name>   # Use Python/FastMCP template
/mcp-builder --typescript <api>    # Use Node/TypeScript template
/mcp-builder --eval <eval.xml>     # Run evaluation suite against MCP server
/mcp-builder --register <name>     # Register MCP server in .cursor/mcp.json
```

### Workflow

1. **Research** — Study target API docs, MCP protocol, and SDK documentation
2. **Plan** — Design tools, shared utilities, error handling, and pagination
3. **Implement** — Set up project, implement tools with Zod/Pydantic schemas
4. **Test** — Build, test with MCP Inspector, review code quality
5. **Evaluate** — Create 10 QA pairs, run evaluation harness
6. **Register** — Add to `.cursor/mcp.json` for Cursor integration

### Execution

Read and follow the `anthropic-mcp-builder` skill (`.cursor/skills/anthropic-mcp-builder/SKILL.md`) for the complete 4-phase workflow, reference documentation, and evaluation scripts.

### Examples

Build an MCP server for the GitHub API:

```
/mcp-builder github-api
```

Build a Python MCP server for Slack:

```
/mcp-builder --python slack-api
```

Run evaluations:

```
/mcp-builder --eval eval.xml
```
