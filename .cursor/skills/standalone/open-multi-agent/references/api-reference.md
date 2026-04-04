# open-multi-agent API Reference

## Package: `@jackchen_me/open-multi-agent` v0.2.0

Node.js >= 18.0.0 required.

---

## Public Exports

```typescript
import {
  OpenMultiAgent,  // Main orchestrator class
  Agent,           // Agent executor
  Team,            // Team container
  defineTool,      // Custom tool factory
  type AgentConfig,
  type TeamConfig,
  type Task,
  type OrchestratorConfig,
  type AgentResult,
  type TeamResult,
  type ToolUseContext,
  type LLMAdapter,
  type MemoryStore,
  type TraceEvent,
  type OrchestratorEvent,
} from 'open-multi-agent'
```

---

## OpenMultiAgent (Main Class)

### Constructor

```typescript
new OpenMultiAgent(config?: OrchestratorConfig)
```

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `defaultModel` | `string` | `'claude-sonnet-4-20250514'` | Default LLM model |
| `defaultProvider` | `string` | `'anthropic'` | Default LLM provider |
| `maxConcurrency` | `number` | `5` | Max parallel task execution |
| `onProgress` | `(event: OrchestratorEvent) => void` | — | Progress callback |
| `onTrace` | `(trace: TraceEvent) => void` | — | Trace/observability callback |

### Methods

#### `createTeam(name: string, config: TeamConfig): Team`

Create a named team of agents. Returns a `Team` instance.

#### `runAgent(config: AgentConfig, prompt: string): Promise<AgentResult>`

Execute a single agent with the given prompt. Returns the agent result including output text, structured data, and token usage.

#### `runTeam(team: Team, goal: string): Promise<TeamResult>`

Auto-orchestrated team execution:
1. Creates a temporary coordinator agent
2. Coordinator decomposes `goal` into tasks with assignees and dependencies
3. Executes tasks respecting dependency DAG, up to `maxConcurrency` in parallel
4. Coordinator synthesises final answer from all task outputs

Returns `TeamResult` containing per-agent results, token usage totals, and the coordinator's final synthesis.

#### `runTasks(team: Team, tasks: TaskInput[]): Promise<TeamResult>`

Execute an explicit list of tasks without coordinator decomposition. Same parallel + dependency logic as `runTeam`, but you define the tasks.

```typescript
type TaskInput = {
  title: string
  description: string
  assignee?: string      // agent name; auto-assigned if omitted
  dependsOn?: string[]   // task titles this depends on
  maxRetries?: number    // default 0
  retryDelayMs?: number  // default 1000
  retryBackoff?: number  // default 2
}
```

#### `getStatus(): OrchestratorStatus`

Returns current status including active tasks, queue size, and running agents.

#### `shutdown(): Promise<void>`

Gracefully shut down the orchestrator and release resources.

---

## AgentConfig

```typescript
type AgentConfig = {
  name: string
  model?: string
  provider?: string
  baseURL?: string
  apiKey?: string
  systemPrompt?: string
  tools?: Array<string | ToolDefinition>
  outputSchema?: ZodSchema  // Zod schema for structured output
  maxTokens?: number
  temperature?: number
}
```

### Built-in Tool Names (string references)

| Name | Description |
|------|-------------|
| `'bash'` | Execute shell commands |
| `'file_read'` | Read file contents |
| `'file_write'` | Write to files |
| `'file_edit'` | Edit sections of files |
| `'grep'` | Pattern search in files |

---

## TeamConfig

```typescript
type TeamConfig = {
  name: string
  agents: AgentConfig[]
  sharedMemory?: boolean   // default false — enable inter-agent memory
  coordinator?: AgentConfig // custom coordinator config (optional)
}
```

---

## Task

```typescript
type Task = {
  id: string
  title: string
  description: string
  assignee: string
  dependsOn: string[]
  status: 'pending' | 'running' | 'completed' | 'failed' | 'blocked'
  result?: string
  error?: string
  maxRetries: number
  retryDelayMs: number
  retryBackoff: number
  attempts: number
}
```

---

## Result Types

### AgentResult

```typescript
type AgentResult = {
  output: string
  structured?: unknown      // parsed Zod output if schema provided
  tokenUsage: TokenUsage
  toolResults?: ToolResult[]
}
```

### TeamResult

```typescript
type TeamResult = {
  agentResults: Map<string, AgentResult>
  totalTokenUsage: TokenUsage
  tasks: Task[]
}
```

### TokenUsage

```typescript
type TokenUsage = {
  inputTokens: number
  outputTokens: number
  cacheReadTokens?: number
  cacheWriteTokens?: number
}
```

---

## defineTool

```typescript
function defineTool<T>(config: {
  name: string
  description: string
  schema: ZodSchema<T>
  execute: (input: T, context: ToolUseContext) => Promise<string>
}): ToolDefinition
```

---

## ToolUseContext

```typescript
type ToolUseContext = {
  toolUseId: string
  agentName: string
  signal?: AbortSignal
}
```

---

## OrchestratorEvent

```typescript
type OrchestratorEvent = {
  type: 'agent_start' | 'agent_end' | 'task_start' | 'task_complete'
       | 'task_retry' | 'task_failed' | 'coordinator_start'
       | 'coordinator_end' | 'error'
  agent?: string
  task?: string
  data?: unknown
  timestamp: number
}
```

---

## TraceEvent

```typescript
type TraceEvent = {
  type: 'llm_request' | 'llm_response' | 'tool_call' | 'tool_result'
       | 'memory_read' | 'memory_write'
  agent: string
  data: unknown
  timestamp: number
}
```

---

## LLM Provider Configuration

| Provider | `provider` value | `baseURL` | API Key Env Var |
|----------|-----------------|-----------|-----------------|
| Anthropic | `'anthropic'` | (default) | `ANTHROPIC_API_KEY` |
| OpenAI | `'openai'` | (default) | `OPENAI_API_KEY` |
| Ollama | `'openai'` | `http://localhost:11434/v1` | — |
| vLLM | `'openai'` | `http://localhost:8000/v1` | — |
| LM Studio | `'openai'` | `http://localhost:1234/v1` | — |
| Grok | `'openai'` | `https://api.x.ai/v1` | `XAI_API_KEY` |
| GitHub Copilot | `'openai'` | `https://models.inference.ai.azure.com` | `GITHUB_TOKEN` |

---

## Retry Mechanism

Exponential backoff with capped delay:

```
delay = min(retryDelayMs × retryBackoff^(attempt-1), 60000ms)
```

Default: 0 retries. Configure per-task via `maxRetries`, `retryDelayMs`, `retryBackoff`.

---

## Internal Architecture

```
OpenMultiAgent
├── Team (container for agents)
├── TaskQueue (dependency-aware priority queue)
├── Scheduler (task-to-agent assignment)
├── AgentPool (agent instance lifecycle)
├── MessageBus (inter-agent messaging)
├── MemoryStore (shared key-value memory)
└── Agent (single agent executor with tool loop)
```

The coordinator pattern in `runTeam()`:
1. **Decomposition**: Coordinator receives goal + agent roster → outputs JSON task specs
2. **Parsing**: Framework parses task specs, resolves assignees, builds dependency graph
3. **Execution**: Tasks execute in topological order, respecting `maxConcurrency`
4. **Synthesis**: Coordinator receives all task outputs → produces final answer
