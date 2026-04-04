# open-multi-agent

Build and orchestrate multi-agent TypeScript applications using the `open-multi-agent` framework (`@jackchen_me/open-multi-agent`). Provides three execution modes: single-agent runs (`runAgent`), auto-orchestrated team runs with coordinator decomposition (`runTeam`), and explicit task-list runs (`runTasks`). Model-agnostic — supports Anthropic, OpenAI, Grok, GitHub Copilot, and local models (Ollama, vLLM, LM Studio).

## When to Use

Use when the user asks to:
- "build a multi-agent app", "create an agent team", "orchestrate agents", "open-multi-agent"
- "auto-decompose a goal into agent tasks", "run agents in parallel"
- "set up agent coordination with shared memory"
- "멀티 에이전트 앱 만들기", "에이전트 팀 구성", "에이전트 오케스트레이션"
- "TypeScript agent framework", "agent team with coordinator"
- Build Node.js/TypeScript applications that require multiple LLM agents collaborating on complex tasks
- Set up agent teams with dependency-aware task execution, shared memory, and message passing

## When NOT to Use

- For Cursor skill orchestration or subagent dispatch within Cursor → use `harness`, `mission-control`, or `workflow-parallel`
- For Python-based multi-agent frameworks → use AutoResearchClaw, CrewAI, or LangGraph
- For single LLM API calls without agent abstraction → use `anthropic-claude-api` or call the API directly
- For MCP server development → use `anthropic-mcp-builder`
- For designing multi-agent architecture theory without implementation → use `ce-multi-agent-patterns`

## Prerequisites

- Node.js >= 18.0.0
- npm or pnpm package manager
- At least one LLM provider API key (Anthropic, OpenAI, etc.) or a local model server

## Installation

```bash
npm install open-multi-agent
# or
pnpm add open-multi-agent
```

## Core Concepts

### Three Execution Modes

| Mode | Method | Coordinator | Use Case |
|------|--------|-------------|----------|
| Single Agent | `runAgent(config, prompt)` | No | One-shot queries, simple tasks |
| Auto-Orchestrated Team | `runTeam(team, goal)` | Yes (auto) | Complex goals needing decomposition |
| Explicit Tasks | `runTasks(team, tasks)` | No | Pre-planned task lists with dependencies |

### Coordinator Pattern (runTeam — Flagship Feature)

`runTeam()` automatically creates a coordinator agent that:
1. Receives the goal and the team roster
2. Decomposes the goal into JSON task specs with assignees and dependencies
3. Loads tasks into a dependency-aware queue
4. Executes tasks in parallel (up to `maxConcurrency`), respecting dependency order
5. Persists results to shared memory so subsequent agents can read them
6. Synthesises a final answer from all task outputs

### Shared Memory & Message Bus

- Agents write results to shared memory after task completion
- Subsequent agents receive a summary of prior results in their prompt
- Inter-agent messages are injected into the task prompt for targeted communication

## Workflow

### Step 1: Initialize the Orchestrator

```typescript
import { OpenMultiAgent } from 'open-multi-agent'

const orchestrator = new OpenMultiAgent({
  defaultModel: 'claude-sonnet-4-20250514',
  defaultProvider: 'anthropic',
  maxConcurrency: 5,
  onProgress: (event) => console.log(`[${event.type}]`, event),
})
```

### Step 2: Create a Team

```typescript
const team = orchestrator.createTeam('research-team', {
  name: 'research-team',
  agents: [
    {
      name: 'researcher',
      model: 'claude-sonnet-4-20250514',
      systemPrompt: 'You research topics thoroughly using web sources.',
      tools: ['bash', 'file_write'],
    },
    {
      name: 'writer',
      model: 'claude-sonnet-4-20250514',
      systemPrompt: 'You write clear, well-structured documentation.',
      tools: ['file_read', 'file_write'],
    },
    {
      name: 'reviewer',
      model: 'claude-sonnet-4-20250514',
      systemPrompt: 'You review content for accuracy and clarity.',
    },
  ],
  sharedMemory: true,
})
```

### Step 3A: Auto-Orchestrated Run (runTeam)

```typescript
const result = await orchestrator.runTeam(
  team,
  'Write a comprehensive guide on TypeScript generics with examples'
)

console.log(result.agentResults.get('coordinator')?.output)
console.log('Tokens used:', result.totalTokenUsage)
```

### Step 3B: Explicit Tasks Run (runTasks)

```typescript
const result = await orchestrator.runTasks(team, [
  {
    title: 'Research TypeScript generics',
    description: 'Find key concepts, patterns, and edge cases for TS generics',
    assignee: 'researcher',
  },
  {
    title: 'Write the guide',
    description: 'Write a structured guide based on research findings',
    assignee: 'writer',
    dependsOn: ['Research TypeScript generics'],
  },
  {
    title: 'Review the guide',
    description: 'Review for accuracy, clarity, and completeness',
    assignee: 'reviewer',
    dependsOn: ['Write the guide'],
  },
])
```

### Step 3C: Single Agent Run (runAgent)

```typescript
const result = await orchestrator.runAgent(
  {
    name: 'analyst',
    model: 'claude-sonnet-4-20250514',
    systemPrompt: 'You analyze data and provide insights.',
  },
  'Summarize the key trends in AI agent frameworks for 2026'
)
```

## Structured Output with Zod

```typescript
import { z } from 'zod'

const result = await orchestrator.runAgent(
  {
    name: 'extractor',
    model: 'claude-sonnet-4-20250514',
    systemPrompt: 'Extract structured data from text.',
    outputSchema: z.object({
      companies: z.array(z.object({
        name: z.string(),
        valuation: z.string(),
        sector: z.string(),
      })),
    }),
  },
  'Extract company info from: NVIDIA ($3.4T, Semiconductors), Apple ($3.2T, Tech)...'
)

console.log(result.structured)
```

## Custom Tools

```typescript
import { defineTool } from 'open-multi-agent'
import { z } from 'zod'

const weatherTool = defineTool({
  name: 'get_weather',
  description: 'Get current weather for a city',
  schema: z.object({
    city: z.string().describe('City name'),
    units: z.enum(['celsius', 'fahrenheit']).default('celsius'),
  }),
  execute: async ({ city, units }) => {
    const data = await fetchWeather(city, units)
    return `${city}: ${data.temp}° ${units}, ${data.condition}`
  },
})

const agent = {
  name: 'weather-bot',
  model: 'claude-sonnet-4-20250514',
  systemPrompt: 'You help users check weather.',
  tools: [weatherTool],
}
```

## Built-in Tools

| Tool | Description |
|------|-------------|
| `bash` | Execute shell commands |
| `file_read` | Read file contents |
| `file_write` | Write content to files |
| `file_edit` | Edit specific parts of files |
| `grep` | Search file contents with patterns |

## Model Provider Configuration

```typescript
// Anthropic (default)
{ model: 'claude-sonnet-4-20250514', provider: 'anthropic' }

// OpenAI
{ model: 'gpt-4o', provider: 'openai' }

// Local models (Ollama, vLLM, LM Studio)
{ model: 'llama3', provider: 'openai', baseURL: 'http://localhost:11434/v1' }

// Grok
{ model: 'grok-3', provider: 'openai', baseURL: 'https://api.x.ai/v1' }

// GitHub Copilot
{ model: 'gpt-4o', provider: 'openai', baseURL: 'https://models.inference.ai.azure.com' }
```

## Task Retry Configuration

Tasks support automatic retry with exponential backoff:

```typescript
{
  title: 'Flaky API call',
  description: 'Fetch data from unreliable endpoint',
  assignee: 'fetcher',
  maxRetries: 3,
  retryDelayMs: 1000,
  retryBackoff: 2,
}
```

## Progress Events and Tracing

```typescript
const orchestrator = new OpenMultiAgent({
  onProgress: (event) => {
    switch (event.type) {
      case 'agent_start': console.log(`Agent ${event.agent} started`); break
      case 'task_complete': console.log(`Task ${event.task} done`); break
      case 'task_retry': console.log(`Retrying task ${event.task}`); break
      case 'error': console.error(`Error: ${event.data}`); break
    }
  },
  onTrace: (trace) => {
    // Full trace events for observability
    console.log(JSON.stringify(trace))
  },
})
```

## Error Handling

- **Graceful failure**: A failed task marks itself `failed` and its direct dependents remain `blocked`; all non-dependent tasks continue executing
- **Retry with backoff**: Configure `maxRetries`, `retryDelayMs`, `retryBackoff` per task
- **Coordinator fallback**: If the coordinator fails to produce structured JSON task output, the framework falls back to creating one task per agent using the original goal

## Examples

<example>
User: "TypeScript로 리서치 + 작문 에이전트 팀을 만들어줘"

Agent reads this skill, then:
1. Creates a new Node.js project with `npm init` and `npm install open-multi-agent`
2. Scaffolds `src/index.ts` with OpenMultiAgent, researcher + writer agents
3. Configures `sharedMemory: true` for inter-agent context sharing
4. Uses `runTeam()` for auto-orchestration with a high-level goal
5. Adds `onProgress` callbacks for execution visibility
</example>

<example>
User: "open-multi-agent로 코드 리뷰 파이프라인을 만들어줘. security, performance, style 3개 에이전트가 병렬로 리뷰하고 결과를 종합하는 구조"

Agent reads this skill, then:
1. Creates three reviewer agents with specialized system prompts
2. Uses `runTasks()` with explicit task list (3 parallel review tasks + 1 synthesis task)
3. Sets `dependsOn` so synthesis task depends on all three review tasks
4. Configures `file_read` tool for all reviewers to access source code
5. Adds structured output schema for standardized review format
</example>

<example>
User: "로컬 Ollama 모델로 멀티 에이전트 앱을 만들고 싶어"

Agent reads this skill, then:
1. Configures `provider: 'openai'` with `baseURL: 'http://localhost:11434/v1'`
2. Sets appropriate local model name (e.g., `'llama3'`)
3. Reduces `maxConcurrency` to match local GPU capacity
4. Uses `runAgent()` first to verify connectivity before building a full team
</example>

## References

- [API Reference](references/api-reference.md)
- [GitHub Repository](https://github.com/JackChen-me/open-multi-agent)
- [npm Package](https://www.npmjs.com/package/@jackchen_me/open-multi-agent)
