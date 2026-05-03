---
name: state-diagram
description: >-
  Create state machine and statechart diagrams using Mermaid stateDiagram-v2
  syntax. Supports simple states, composite/nested states, forks/joins, choice
  pseudostates, notes, and concurrency. Use when the user asks to "create
  state diagram", "state machine", "statechart", "lifecycle diagram", "status
  transitions", "상태 다이어그램", "상태 머신", "상태 전이", "라이프사이클", or needs to visualize
  object lifecycle, protocol states, or UI state management. Do NOT use for
  sequential process flows without state semantics (use flowchart skill). Do
  NOT use for BPMN business processes (use workflow-diagram skill). Do NOT use
  for class relationships (use class-diagram skill). Do NOT use for
  architecture layers (use architecture-diagram skill).
---

# State Diagram Generator

**Quick Start:** Define states -> Add transitions with triggers -> Add guards/actions -> Wrap with composite states if needed.

## Critical Rules

### Rule 1: Mermaid Code Fence
Always output inside ` ```mermaid ` fenced code blocks using `stateDiagram-v2`.

### Rule 2: Use stateDiagram-v2
Always use `stateDiagram-v2` (not the older `stateDiagram`). v2 supports all advanced features.

### Rule 3: State Naming
- State IDs must NOT contain spaces; use camelCase or PascalCase
- Display labels use `: Label` syntax: `StateId : Display Label`
- Avoid reserved words as state IDs

### Rule 4: Special States
| State | Syntax | Use For |
|---|---|---|
| Initial | `[*]` | Start of lifecycle |
| Final | `[*]` | End of lifecycle (same syntax, context-dependent) |
| Choice | `<<choice>>` | Conditional branching |
| Fork | `<<fork>>` | Parallel split |
| Join | `<<join>>` | Parallel merge |

### Rule 5: Transition Syntax
```
StateA --> StateB : trigger [guard] / action
```
- `trigger` -- event that causes the transition
- `[guard]` -- condition that must be true (optional)
- `/ action` -- side effect executed during transition (optional)

### Rule 6: Composite States
Nest states inside a parent to show hierarchical decomposition:
```
state ParentState {
  [*] --> ChildA
  ChildA --> ChildB
}
```

### Rule 7: Concurrency
Use `--` separator inside a composite state for parallel regions:
```
state ActiveState {
  [*] --> Processing
  --
  [*] --> Monitoring
}
```

## Template: Order Lifecycle

```mermaid
stateDiagram-v2
    [*] --> Draft : create

    Draft --> Submitted : submit
    Draft --> Cancelled : cancel

    Submitted --> UnderReview : assign_reviewer
    Submitted --> Cancelled : cancel

    UnderReview --> Approved : approve
    UnderReview --> Rejected : reject
    UnderReview --> Submitted : request_changes

    Approved --> Processing : start_processing
    Approved --> Cancelled : cancel

    Processing --> Shipped : ship
    Processing --> Cancelled : cancel

    Shipped --> Delivered : confirm_delivery
    Shipped --> Returned : return

    Delivered --> [*]
    Returned --> Processing : reship
    Returned --> Refunded : refund
    Refunded --> [*]
    Cancelled --> [*]
    Rejected --> Draft : revise
```

## Template: Authentication State Machine

```mermaid
stateDiagram-v2
    [*] --> Unauthenticated

    state Unauthenticated {
        [*] --> Idle
        Idle --> Authenticating : login_attempt
        Authenticating --> Idle : auth_failed
    }

    Unauthenticated --> Authenticated : auth_success

    state Authenticated {
        [*] --> Active
        Active --> SessionExpiring : timeout_warning
        SessionExpiring --> Active : user_activity
        SessionExpiring --> SessionExpired : timeout
    }

    Authenticated --> Unauthenticated : logout
    Authenticated --> Unauthenticated : session_expired
    Authenticated --> Locked : too_many_violations

    Locked --> Unauthenticated : admin_unlock
    Locked --> [*] : account_deleted
```

## Template: CI/CD Pipeline States

```mermaid
stateDiagram-v2
    [*] --> Queued : push_event

    Queued --> Building : runner_available

    state Building {
        [*] --> Compile
        Compile --> Test : compile_ok
        Compile --> Failed : compile_error
        Test --> Lint : tests_pass
        Test --> Failed : tests_fail
        Lint --> BuildComplete : lint_pass
        Lint --> Failed : lint_fail
    }

    state Failed {
        [*] --> NotifyOwner
        NotifyOwner --> WaitingFix
    }

    BuildComplete --> Deploying : auto_deploy

    state fork_deploy <<fork>>
    state join_deploy <<join>>

    Deploying --> fork_deploy
    fork_deploy --> DeployStaging
    fork_deploy --> RunE2E
    DeployStaging --> join_deploy
    RunE2E --> join_deploy

    join_deploy --> AwaitApproval : staging_ok

    state decision <<choice>>
    AwaitApproval --> decision : reviewed
    decision --> Production : approved
    decision --> Rollback : rejected

    Production --> [*] : healthy
    Rollback --> Failed : rollback_complete
    Failed --> Queued : retry
```

## Template: Simple UI State (Fetch Operation)

```mermaid
stateDiagram-v2
    [*] --> Idle

    Idle --> Loading : fetch
    Loading --> Success : data_received
    Loading --> Error : request_failed

    Success --> Loading : refresh
    Success --> Idle : reset

    Error --> Loading : retry
    Error --> Idle : dismiss

    Success --> [*] : unmount
    Error --> [*] : unmount
    Idle --> [*] : unmount
```

## Template: Concurrent States (Media Player)

```mermaid
stateDiagram-v2
    [*] --> Off

    Off --> On : power_on
    On --> Off : power_off

    state On {
        [*] --> Playing

        state Playing {
            [*] --> AudioStream
            --
            [*] --> VideoStream
            --
            [*] --> SubtitleTrack
        }

        Playing --> Paused : pause
        Paused --> Playing : resume
        Playing --> Buffering : buffer_underrun
        Buffering --> Playing : buffer_ready
    }
```

## Best Practices

1. **Start with [*]** -- every diagram should have a clear initial state
2. **Name states as nouns/adjectives** -- `Processing`, `Active`, `Locked` (not verbs)
3. **Label transitions as verbs/events** -- `submit`, `approve`, `timeout`
4. **Use composite states** -- group related states to reduce visual clutter
5. **Show error/edge paths** -- include cancelled, failed, and timeout transitions
6. **One responsibility per state** -- if a state does multiple things, decompose it
7. **Guards vs separate states** -- prefer guards `[condition]` for simple checks, separate states for complex logic
8. **Output format** -- always output inside ` ```mermaid ` fenced code blocks
