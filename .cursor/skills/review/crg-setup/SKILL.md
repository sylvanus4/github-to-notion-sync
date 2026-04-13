# CRG Setup

Install, configure, and verify the code-review-graph AST-based knowledge graph for token-efficient code reviews.

## Triggers

Use when the user asks to "install code-review-graph", "setup CRG", "CRG 설치", "코드 리뷰 그래프 설정", "configure code review graph", or needs first-time setup of the graph infrastructure.

Do NOT use for building/updating the graph after setup (use crg-build-graph). Do NOT use for reviewing code with the graph (use crg-review-delta or crg-review-pr). Do NOT use for querying architecture (use crg-query).

## Steps

### Step 1: Install Package

```bash
pip install code-review-graph
code-review-graph --version
```

Verify the CLI prints a version number (e.g., `code-review-graph 2.3.1`).

### Step 2: Register MCP Server

Ensure `.cursor/mcp.json` contains the `code-review-graph` entry:

```json
"code-review-graph": {
  "command": "uvx",
  "args": ["code-review-graph", "serve"],
  "description": "Code Review Graph — AST-based knowledge graph with 22 MCP tools for token-efficient code reviews, blast-radius analysis, and architecture queries"
}
```

### Step 3: Create Ignore File

Create `.code-review-graphignore` at the repo root with patterns for non-code directories:

```
outputs/
.cursor/skills/
.cursor/hooks/
node_modules/
__pycache__/
*.pyc
.venv/
venv/
memory/
knowledge-bases/
docs/
*.md
*.json
*.yaml
*.yml
*.csv
*.tsv
*.xlsx
*.docx
*.pdf
lat.md/
```

### Step 4: Initial Full Build

```bash
code-review-graph build --full
```

### Step 5: Verify

```bash
code-review-graph status
```

Confirm the output shows nodes, edges, and indexed files. Report the stats to the user.

## Output

Report installation status, graph stats (nodes, edges, files), and any errors encountered.
