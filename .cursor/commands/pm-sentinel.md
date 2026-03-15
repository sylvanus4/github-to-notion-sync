---
description: "Run the PM Sentinel autonomous loop — continuous project improvement with YAML state DB, CLI validation gates, evidence-based completion, and forced reminders"
---

# PM Sentinel — Autonomous Project Improvement

## Skill Reference

Read and follow the skill at `.cursor/skills/pm-sentinel/SKILL.md`.

## Your Task

User input: $ARGUMENTS

### Step 1: Parse Request

Determine the **mode** from user input:

- **start**: Resume sentinel and seed all mission types. Begin executing the highest-priority mission.
- **status**: Run `python .cursor/sentinel/pm-sentinel-cli.py status` and present the results.
- **heartbeat**: Run a single heartbeat cycle — determine next action, execute it, validate evidence.
- **pause**: Pause the sentinel. No missions will execute until resumed.
- **resume**: Resume a paused sentinel.
- **report**: Generate a summary of completed missions and metrics.
- **seed [types]**: Seed missions from templates. Optional: comma-separated types to seed specific ones.
- **add <type>**: Add a specific mission type to the queue. Valid types: `project-health-scan`, `pipeline-optimizer`, `skill-ecosystem-growth`, `data-quality-patrol`, `security-dependency-sweep`, `test-coverage-patrol`, `doc-freshness-checker`.
- **No arguments / run / loop**: Run a full sentinel loop — resume, seed if empty, then execute missions until the queue is clear or time limit is reached.

### Step 2: Execute

Based on the parsed mode, execute the corresponding workflow from the skill file.

For **start** or **loop** mode:

1. Run `python .cursor/sentinel/pm-sentinel-cli.py resume`
2. Run `python .cursor/sentinel/pm-sentinel-cli.py seed`
3. Run `python .cursor/sentinel/pm-sentinel-cli.py heartbeat`
4. Parse the returned JSON action descriptor
5. Follow the action: start mission → execute phases with skills → collect evidence → complete phases → complete mission
6. After each mission completes, check `next` for the next mission
7. Continue until no pending missions remain or 3 missions have been completed in this session

For **heartbeat** mode:

1. Run `python .cursor/sentinel/pm-sentinel-cli.py heartbeat`
2. Execute exactly one mission cycle based on the returned action
3. Always read and follow the SENTINEL REMINDER block

### Step 3: Evidence Collection

When executing mission phases, you MUST:

1. Actually run the skill or command specified in the phase
2. Capture real output (file paths, error counts, metrics, scores)
3. Format evidence as JSON: `{"field1": "value1", "field2": 42}`
4. Pass to CLI: `python .cursor/sentinel/pm-sentinel-cli.py complete-phase <mission-id> <phase-id> --evidence '<json>'`

The CLI will REJECT completion if evidence is missing or empty. Read the REMEDIATION message and fix it.

### Step 4: Mission Outputs

Save mission outputs to `outputs/sentinel/` with the format:
`outputs/sentinel/<mission-type>-<date>.md`

## Examples

```
/pm-sentinel start         # Initialize and begin executing missions
/pm-sentinel status        # Check current state and next action
/pm-sentinel heartbeat     # Run one cycle
/pm-sentinel report        # View completed mission metrics
/pm-sentinel seed          # Replenish mission queue
/pm-sentinel add data-quality-patrol  # Add a specific mission
/pm-sentinel pause         # Pause the sentinel
/pm-sentinel               # Full loop (resume + seed + execute)
```

## Constraints

- All state mutations go through the CLI — never edit sentinel-state.yaml directly
- Evidence must be specific and verifiable — the CLI enforces this
- One mission at a time — complete or fail before starting another
- Maximum 3 missions per manual session to prevent context window exhaustion
- Always read the SENTINEL REMINDER at the end of every CLI output
