# MiroFish API Endpoints Reference

Base URL: `http://localhost:5001`

## Health Check

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Service health status |

## Graph API (`/api/graph`)

| Method | Path | Description |
|--------|------|-------------|
| GET | `/project/list` | List all projects |
| GET | `/project/<project_id>` | Get project details |
| DELETE | `/project/<project_id>` | Delete a project |
| POST | `/project/<project_id>/reset` | Reset project data |
| POST | `/ontology/generate` | Generate ontology from seed document. **multipart/form-data**: `files` (PDF/MD/TXT), `simulation_requirement` (required), `project_name` (optional), `additional_context` (optional). Returns `project_id` + generated ontology. |
| POST | `/build` | Build knowledge graph (requires Zep Cloud). **JSON body**: `{"project_id", "graph_name?", "chunk_size?", "chunk_overlap?", "force?"}` |
| GET | `/task/<task_id>` | Check graph build task status |
| GET | `/tasks` | List all graph build tasks |
| GET | `/data/<graph_id>` | Get graph data (nodes + edges) |
| DELETE | `/delete/<graph_id>` | Delete a graph |

## Simulation API (`/api/simulation`)

### Entity Management

| Method | Path | Description |
|--------|------|-------------|
| GET | `/entities/<graph_id>` | List entities from knowledge graph |
| GET | `/entities/<graph_id>/<entity_uuid>` | Get entity details |
| GET | `/entities/<graph_id>/by-type/<entity_type>` | Filter entities by type |

### Simulation Lifecycle

| Method | Path | Description |
|--------|------|-------------|
| POST | `/create` | Create simulation. Body: `{project_id (REQUIRED), graph_id (optional — inferred from project), enable_twitter, enable_reddit}` |
| POST | `/prepare` | Prepare simulation environment (persona generation). Body: `{simulation_id}` |
| POST | `/prepare/status` | Check preparation status. Body: `{simulation_id}` |
| POST | `/generate-profiles` | Generate agent profiles. Body: `{simulation_id}` |
| POST | `/start` | Start simulation. Body: `{simulation_id}` |
| POST | `/stop` | Stop running simulation. Body: `{simulation_id}` |
| GET | `/<simulation_id>` | Get simulation details |
| GET | `/list` | List all simulations |
| GET | `/history` | Get simulation history |

### Simulation Monitoring

| Method | Path | Description |
|--------|------|-------------|
| GET | `/<simulation_id>/run-status` | Basic run status (running/completed/failed) |
| GET | `/<simulation_id>/run-status/detail` | Detailed status with round progress |
| GET | `/<simulation_id>/profiles` | Get generated agent profiles |
| GET | `/<simulation_id>/profiles/realtime` | Real-time profile updates during simulation |
| GET | `/<simulation_id>/config/realtime` | Real-time config updates |
| GET | `/<simulation_id>/config` | Get simulation configuration |
| GET | `/<simulation_id>/config/download` | Download config as file |
| GET | `/script/<script_name>/download` | Download simulation script |

### Simulation Results

| Method | Path | Description |
|--------|------|-------------|
| GET | `/<simulation_id>/actions` | Agent actions log |
| GET | `/<simulation_id>/timeline` | Event timeline |
| GET | `/<simulation_id>/agent-stats` | Per-agent statistics |
| GET | `/<simulation_id>/posts` | Agent-generated posts/content |
| GET | `/<simulation_id>/comments` | Agent comments and interactions |

### Agent Interaction

| Method | Path | Description |
|--------|------|-------------|
| POST | `/interview` | Interview single agent. Body: `{simulation_id, agent_id, question}` |
| POST | `/interview/batch` | Batch interview. Body: `{simulation_id, agent_ids[], question}` |
| POST | `/interview/all` | Interview all agents. Body: `{simulation_id, question}` |
| POST | `/interview/history` | Get interview history. Body: `{simulation_id}` |

### Environment Control

| Method | Path | Description |
|--------|------|-------------|
| POST | `/env-status` | Check simulation environment status |
| POST | `/close-env` | Close simulation environment |

## Report API (`/api/report`)

### Report Lifecycle

| Method | Path | Description |
|--------|------|-------------|
| POST | `/generate` | Generate report. Body: `{simulation_id}` |
| POST | `/generate/status` | Check generation status. Body: `{report_id}` |
| GET | `/<report_id>` | Get report content |
| GET | `/by-simulation/<simulation_id>` | Get report by simulation ID |
| GET | `/list` | List all reports |
| GET | `/<report_id>/download` | Download report file |
| DELETE | `/<report_id>` | Delete report |

### Report Details

| Method | Path | Description |
|--------|------|-------------|
| GET | `/<report_id>/progress` | Report generation progress |
| GET | `/<report_id>/sections` | List report sections |
| GET | `/<report_id>/section/<section_index>` | Get specific section |
| GET | `/check/<simulation_id>` | Check if report exists for simulation |

### Report Agent Interaction

| Method | Path | Description |
|--------|------|-------------|
| POST | `/chat` | Chat with ReportAgent. Body: `{report_id, message}` |
| GET | `/<report_id>/agent-log` | Agent execution log |
| GET | `/<report_id>/agent-log/stream` | Stream agent log (SSE) |
| GET | `/<report_id>/console-log` | Console output log |
| GET | `/<report_id>/console-log/stream` | Stream console log (SSE) |

### Report Tools

| Method | Path | Description |
|--------|------|-------------|
| POST | `/tools/search` | Search within report data |
| POST | `/tools/statistics` | Statistical analysis of simulation results |
