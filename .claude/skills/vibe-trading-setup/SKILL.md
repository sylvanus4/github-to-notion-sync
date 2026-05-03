---
name: vibe-trading-setup
description: >-
  Install Vibe-Trading, configure environment variables, register the MCP
  server in Cursor, and run health checks to verify connectivity. Use when the
  user asks to "install vibe-trading", "setup vibe trading", "configure
  vibe-trading", "vibe-trading-setup", "바이브 트레이딩 설치", "바이브 트레이딩 설정", or needs
  to set up the Vibe-Trading MCP integration. Do NOT use for running analysis
  (use vibe-trading-orchestrator). Do NOT use for MCP tool reference (use
  vibe-trading-mcp). Do NOT use for data fetching (use vibe-trading-data).
disable-model-invocation: true
---

# Vibe-Trading Setup

## Overview

Vibe-Trading is an AI-powered multi-agent finance workspace with 67 specialized
skills, 29 swarm team presets, and a vectorized backtest engine. This skill
handles installation, environment configuration, MCP server registration, and
health verification.

## Prerequisites

- Python 3.10+ (3.12 recommended)
- pip or uv package manager
- Cursor IDE with MCP support
- (Optional) Docker for containerized deployment

## Step 1: Verify Repository

The repository should already be cloned at `~/thaki/Vibe-Trading/`. Verify:

```bash
ls ~/thaki/Vibe-Trading/agent/mcp_server.py
```

If not present, clone:

```bash
git clone https://github.com/HKUDS/Vibe-Trading.git ~/thaki/Vibe-Trading
```

## Step 2: Install Vibe-Trading

### Option A: uv Editable Install (Recommended)

```bash
cd ~/thaki/Vibe-Trading
uv pip install -e .
```

This registers the `vibe-trading` and `vibe-trading-mcp` CLI commands in the
uv-managed virtual environment. Verify with:

```bash
uv run vibe-trading-mcp --help
```

### Option B: pip Editable Install

```bash
cd ~/thaki/Vibe-Trading
pip install -e .
```

### Option C: Docker

```bash
cd ~/thaki/Vibe-Trading
docker compose up -d
```

## Step 3: Configure Environment

Copy the example and edit `~/thaki/Vibe-Trading/agent/.env`:

```bash
cp ~/thaki/Vibe-Trading/agent/.env.example ~/thaki/Vibe-Trading/agent/.env
```

Then set at minimum:

```bash
OPENAI_API_KEY=sk-...          # Required: any OpenAI-compatible provider
OPENAI_BASE_URL=https://api.openai.com/v1
LANGCHAIN_PROVIDER=openai      # or "openrouter"
LANGCHAIN_MODEL_NAME=gpt-4o    # or "deepseek/deepseek-v3.2" for openrouter

# Optional: China A-share data (tushare.pro token)
TUSHARE_TOKEN=your_tushare_token

# Optional: Agent timeout
TIMEOUT_SECONDS=120
```

**Minimum viable config**: Only `OPENAI_API_KEY` is required. yfinance (US/HK)
and OKX (crypto) work without API keys.

## Step 4: Register MCP Server

Add to `.cursor/mcp.json` under `mcpServers`:

```json
{
  "user-vibe-trading": {
    "command": "uv",
    "args": ["run", "--project", "/Users/hanhyojung/thaki/Vibe-Trading", "vibe-trading-mcp"],
    "env": {},
    "description": "Vibe-Trading MCP — 16 finance research tools"
  }
}
```

The `uv run --project` approach avoids PATH issues by running within the
Vibe-Trading project's virtual environment directly.

**Fallback** (if uv is not available):

```json
{
  "user-vibe-trading": {
    "command": "python",
    "args": ["/Users/hanhyojung/thaki/Vibe-Trading/agent/mcp_server.py"],
    "transport": "stdio"
  }
}
```

## Step 5: Health Check

After registration, verify the MCP server responds:

1. Call `list_skills` via the `user-vibe-trading` MCP server
2. Expect a JSON array with 67+ skill entries
3. Each entry has `name` and `description` fields

```
CallMcpTool server=user-vibe-trading toolName=list_skills arguments={}
```

If the response contains skill entries, setup is complete.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `command not found: vibe-trading-mcp` | Not installed or not on PATH | Run `cd ~/thaki/Vibe-Trading && uv pip install -e .` or use the `uv run --project` MCP config |
| MCP server timeout | Missing OPENAI_API_KEY | Set key in `agent/.env` |
| `ModuleNotFoundError: fastmcp` | Dependencies not installed | `pip install fastmcp` |
| tushare returns empty data | Missing TUSHARE_TOKEN | Add token to `agent/.env` |
| Skills count < 67 | Incomplete clone | `cd ~/thaki/Vibe-Trading && git pull` |

## Integration Points

- **MCP server name**: `user-vibe-trading`
- **Transport**: stdio (subprocess)
- **16 exposed tools**: list_skills, load_skill, backtest, factor_analysis,
  analyze_options, pattern_recognition, read_url, read_document, write_file,
  read_file, list_swarm_presets, run_swarm, get_swarm_status, get_run_result,
  list_runs, get_market_data
