---
name: workflow-diagram
description: Create business process and workflow diagrams using PlantUML with BPMN 2.0 notation (events, gateways, tasks, pools, lanes) and Enterprise Integration Pattern stencils. Supports order processing, approval workflows, ETL pipelines, microservice orchestration, and value stream mapping. Use when the user asks to "create workflow diagram", "BPMN diagram", "business process diagram", "approval workflow", "ETL pipeline diagram", "value stream map", "integration pattern diagram", "워크플로우 다이어그램", "비즈니스 프로세스", "BPMN", "승인 워크플로우", "ETL 파이프라인", "밸류 스트림 맵", or needs to visualize business processes with standardized BPMN notation. Do NOT use for simple sequential flowcharts without business process semantics (use flowchart skill). Do NOT use for state machine transitions (use state-diagram skill). Do NOT use for system architecture layers (use architecture-diagram skill). Do NOT use for cloud deployment topology (use deployment-diagram skill).
---

# Workflow Diagram Generator

**Quick Start:** Choose diagram type (BPMN/EIP/Lean) -> Set direction -> Define pools/lanes -> Add events, gateways, tasks -> Connect with arrows.

## Critical Rules

### Rule 1: PlantUML Code Fence
Always output inside ` ```plantuml ` fenced code blocks with `@startuml` / `@enduml`.

### Rule 2: Direction
Use `left to right direction` for horizontal workflows (most common). Omit for top-to-bottom.

### Rule 3: Stencil Icon Syntax
Use `mxgraph.<library>.<icon>` format inside `<<...>>` stereotypes:
- **BPMN**: `mxgraph.bpmn.start_event`, `mxgraph.bpmn.end_event`, `mxgraph.bpmn.exclusive_gateway`, `mxgraph.bpmn.task`
- **EIP**: `mxgraph.eip.message_channel`, `mxgraph.eip.message_router`, `mxgraph.eip.message_endpoint`
- **Lean**: `mxgraph.lean_mapping.process_box`, `mxgraph.lean_mapping.inventory_box`

### Rule 4: Automatic Colors
Icons defined with `mxgraph.*` stencils receive vendor-appropriate colors automatically; do not set manual colors for stencil icons.

### Rule 5: Container Shapes
| Container | Syntax | Use For |
|---|---|---|
| Pool / Lane | `rectangle "Pool Name"` | Organizational boundaries |
| Subprocess | `package "Sub" { }` | Grouped steps |
| System boundary | `cloud "External" { }` | External integrations |

### Rule 6: Connection Types
| Type | Syntax | Meaning |
|---|---|---|
| Sequence Flow | `-->` | Normal process flow |
| Message Flow | `..>` | Cross-pool communication |
| Association | `--` | Annotation / data object link |

## BPMN Elements

### Events
| Element | Stereotype | Use For |
|---|---|---|
| Start Event | `<<mxgraph.bpmn.start_event>>` | Process start |
| End Event | `<<mxgraph.bpmn.end_event>>` | Process end |
| Timer Event | `<<mxgraph.bpmn.timer_start>>` | Scheduled trigger |
| Message Event | `<<mxgraph.bpmn.message_start>>` | Message trigger |
| Error Event | `<<mxgraph.bpmn.error_end>>` | Error termination |

### Gateways
| Element | Stereotype | Use For |
|---|---|---|
| Exclusive (XOR) | `<<mxgraph.bpmn.exclusive_gateway>>` | One path only |
| Parallel (AND) | `<<mxgraph.bpmn.parallel_gateway>>` | All paths concurrently |
| Inclusive (OR) | `<<mxgraph.bpmn.inclusive_gateway>>` | One or more paths |
| Event-Based | `<<mxgraph.bpmn.event_gateway>>` | Wait for event |

### Tasks
| Element | Stereotype | Use For |
|---|---|---|
| User Task | `<<mxgraph.bpmn.user_task>>` | Human interaction |
| Service Task | `<<mxgraph.bpmn.service_task>>` | Automated service |
| Script Task | `<<mxgraph.bpmn.script_task>>` | Script execution |
| Send Task | `<<mxgraph.bpmn.send_task>>` | Send message |
| Receive Task | `<<mxgraph.bpmn.receive_task>>` | Wait for message |

## Template: Order Processing Workflow

```plantuml
@startuml
left to right direction
skinparam backgroundColor white

rectangle "Order Processing" {
  agent start <<mxgraph.bpmn.start_event>>
  agent receive_order <<mxgraph.bpmn.receive_task>> as "Receive\nOrder"
  agent validate <<mxgraph.bpmn.service_task>> as "Validate\nOrder"
  agent check <<mxgraph.bpmn.exclusive_gateway>> as "Valid?"
  agent process_payment <<mxgraph.bpmn.service_task>> as "Process\nPayment"
  agent fulfill <<mxgraph.bpmn.user_task>> as "Fulfill\nOrder"
  agent notify <<mxgraph.bpmn.send_task>> as "Notify\nCustomer"
  agent end_ok <<mxgraph.bpmn.end_event>> as "Complete"
  agent reject <<mxgraph.bpmn.send_task>> as "Send\nRejection"
  agent end_err <<mxgraph.bpmn.error_end>> as "Rejected"

  start --> receive_order
  receive_order --> validate
  validate --> check
  check --> process_payment : "Yes"
  check --> reject : "No"
  process_payment --> fulfill
  fulfill --> notify
  notify --> end_ok
  reject --> end_err
}
@enduml
```

## Template: Approval Workflow with Parallel Tasks

```plantuml
@startuml
left to right direction
skinparam backgroundColor white

rectangle "Approval Process" {
  agent start <<mxgraph.bpmn.start_event>>
  agent submit <<mxgraph.bpmn.user_task>> as "Submit\nRequest"
  agent fork <<mxgraph.bpmn.parallel_gateway>> as "Fork"
  agent review_mgr <<mxgraph.bpmn.user_task>> as "Manager\nReview"
  agent review_fin <<mxgraph.bpmn.user_task>> as "Finance\nReview"
  agent join <<mxgraph.bpmn.parallel_gateway>> as "Join"
  agent decide <<mxgraph.bpmn.exclusive_gateway>> as "Approved?"
  agent approve <<mxgraph.bpmn.service_task>> as "Process\nApproval"
  agent deny <<mxgraph.bpmn.send_task>> as "Send\nDenial"
  agent end_a <<mxgraph.bpmn.end_event>> as "Done"
  agent end_d <<mxgraph.bpmn.end_event>> as "Denied"

  start --> submit
  submit --> fork
  fork --> review_mgr
  fork --> review_fin
  review_mgr --> join
  review_fin --> join
  join --> decide
  decide --> approve : "Yes"
  decide --> deny : "No"
  approve --> end_a
  deny --> end_d
}
@enduml
```

## Template: Enterprise Integration Pattern (EIP)

```plantuml
@startuml
left to right direction
skinparam backgroundColor white

agent source <<mxgraph.eip.message_endpoint>> as "Source\nSystem"
agent channel <<mxgraph.eip.message_channel>> as "Message\nChannel"
agent router <<mxgraph.eip.message_router>> as "Content\nRouter"
agent transform_a <<mxgraph.eip.message_translator>> as "Transform\nJSON"
agent transform_b <<mxgraph.eip.message_translator>> as "Transform\nXML"
agent target_a <<mxgraph.eip.message_endpoint>> as "Service A"
agent target_b <<mxgraph.eip.message_endpoint>> as "Service B"

source --> channel
channel --> router
router --> transform_a : "type=json"
router --> transform_b : "type=xml"
transform_a --> target_a
transform_b --> target_b
@enduml
```

## Template: Value Stream Map (Lean)

```plantuml
@startuml
left to right direction
skinparam backgroundColor white

agent customer <<mxgraph.lean_mapping.outside_sources>> as "Customer"
agent order <<mxgraph.lean_mapping.process_box>> as "Order Entry\nCT: 5min\nC/O: 0"
agent pick <<mxgraph.lean_mapping.process_box>> as "Pick & Pack\nCT: 15min\nC/O: 2min"
agent ship <<mxgraph.lean_mapping.process_box>> as "Shipping\nCT: 10min\nC/O: 0"
agent inv1 <<mxgraph.lean_mapping.inventory_box>> as "WIP\n50 units"
agent inv2 <<mxgraph.lean_mapping.inventory_box>> as "FG\n20 units"

customer --> order
order --> inv1
inv1 --> pick
pick --> inv2
inv2 --> ship
ship --> customer
@enduml
```

## Best Practices

1. **Use BPMN for business processes** -- standardized notation is universally understood
2. **Use EIP for integration** -- message channels, routers, and translators
3. **Use Lean for manufacturing/ops** -- value stream maps with cycle times and inventory
4. **Pool boundaries** -- separate organizational units into distinct pools
5. **Gateway discipline** -- every fork gateway needs a matching join gateway
6. **Label all edges** -- especially on decision gateways
7. **Output format** -- always output inside ` ```plantuml ` fenced code blocks
