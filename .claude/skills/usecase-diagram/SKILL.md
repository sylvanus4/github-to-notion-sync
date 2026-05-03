---
name: usecase-diagram
description: >-
  Create use case diagrams using PlantUML UML syntax. Supports actors
  (primary, secondary, system), use cases, system boundaries, relationships
  (association, include, extend, generalization), and packages. Use when the
  user asks to "create use case diagram", "actor use case", "system boundary
  diagram", "functional requirements diagram", "user interaction diagram",
  "유스케이스 다이어그램", "액터 유스케이스", "시스템 바운더리", "기능 요구사항 다이어그램", "사용자 상호작용", or needs
  to visualize who interacts with a system and what they can do. Do NOT use
  for UI flow or screen navigation (use flowchart skill). Do NOT use for class
  structures (use class-diagram skill). Do NOT use for business process
  workflows (use workflow-diagram skill). Do NOT use for state transitions
  (use state-diagram skill). Do NOT use for deployment topology (use
  deployment-diagram skill).
---

# Use Case Diagram Generator

**Quick Start:** Define actors -> Draw system boundary -> Add use cases -> Connect actors to use cases -> Add include/extend relationships.

## Critical Rules

### Rule 1: PlantUML Code Fence
Always output inside ` ```plantuml ` fenced code blocks with `@startuml` / `@enduml`.

### Rule 2: Direction
Use `left to right direction` for horizontal layouts (recommended when there are many use cases). Omit for vertical (default top-to-bottom).

### Rule 3: Actor Syntax
```
actor "Actor Name" as alias
```
Place primary actors on the left, secondary/supporting actors on the right.

### Rule 4: Use Case Syntax
```
usecase "Use Case Name" as UC1
usecase (Short Name) as UC2
```

### Rule 5: System Boundary
```
rectangle "System Name" {
    usecase "UC1" as uc1
    usecase "UC2" as uc2
}
```
Use `rectangle` (or `package`) to group use cases belonging to the same system or subsystem.

### Rule 6: Relationships
| Relationship | Syntax | Meaning |
|---|---|---|
| Association | `Actor --> UC` | Actor interacts with use case |
| Include | `UC1 ..> UC2 : <<include>>` | UC1 always invokes UC2 |
| Extend | `UC2 ..> UC1 : <<extend>>` | UC2 optionally extends UC1 |
| Generalization (actor) | `ChildActor --\|> ParentActor` | Actor inheritance |
| Generalization (use case) | `SpecificUC --\|> GeneralUC` | Use case inheritance |

### Rule 7: Styling
```
skinparam actorStyle awesome
skinparam backgroundColor white
skinparam usecase {
    BackgroundColor LightYellow
    BorderColor DarkSlateGray
}
```

## Template: E-Commerce Platform

```plantuml
@startuml
left to right direction
skinparam actorStyle awesome
skinparam backgroundColor white

actor "Customer" as customer
actor "Guest" as guest
actor "Admin" as admin
actor "Payment\nGateway" as payment

rectangle "E-Commerce Platform" {
    usecase "Browse Products" as UC1
    usecase "Search Products" as UC2
    usecase "View Product Details" as UC3
    usecase "Add to Cart" as UC4
    usecase "Checkout" as UC5
    usecase "Process Payment" as UC6
    usecase "Track Order" as UC7
    usecase "Leave Review" as UC8
    usecase "Register Account" as UC9
    usecase "Login" as UC10
    usecase "Manage Products" as UC11
    usecase "Manage Orders" as UC12
    usecase "Generate Reports" as UC13
    usecase "Authenticate" as UC14
}

guest --> UC1
guest --> UC2
guest --> UC3
guest --> UC9

customer --> UC1
customer --> UC2
customer --> UC3
customer --> UC4
customer --> UC5
customer --> UC7
customer --> UC8
customer --> UC10

admin --> UC11
admin --> UC12
admin --> UC13
admin --> UC10

UC5 ..> UC6 : <<include>>
UC5 ..> UC14 : <<include>>
UC6 --> payment
UC8 ..> UC14 : <<include>>
UC10 ..> UC14 : <<include>>

guest --|> customer : registers
@enduml
```

## Template: User Authentication System

```plantuml
@startuml
left to right direction
skinparam actorStyle awesome
skinparam backgroundColor white

actor "User" as user
actor "Admin" as admin
actor "OAuth\nProvider" as oauth
actor "Email\nService" as email

rectangle "Authentication System" {
    usecase "Login" as UC1
    usecase "Login with Password" as UC1a
    usecase "Login with OAuth" as UC1b
    usecase "Login with MFA" as UC1c
    usecase "Register" as UC2
    usecase "Reset Password" as UC3
    usecase "Verify Email" as UC4
    usecase "Manage Sessions" as UC5
    usecase "Lock Account" as UC6
    usecase "Audit Login History" as UC7
    usecase "Send Notification" as UC8
    usecase "Validate Credentials" as UC9
}

user --> UC1
user --> UC2
user --> UC3
user --> UC5

admin --> UC6
admin --> UC7

UC1a --|> UC1
UC1b --|> UC1
UC1c --|> UC1

UC1 ..> UC9 : <<include>>
UC1b --> oauth
UC2 ..> UC4 : <<include>>
UC2 ..> UC8 : <<include>>
UC3 ..> UC8 : <<include>>
UC4 --> email
UC8 --> email
UC1c ..> UC1a : <<extend>>
UC6 ..> UC8 : <<include>>
@enduml
```

## Template: CI/CD Pipeline System

```plantuml
@startuml
left to right direction
skinparam actorStyle awesome
skinparam backgroundColor white

actor "Developer" as dev
actor "Tech Lead" as lead
actor "DevOps\nEngineer" as ops
actor "GitHub\nWebhook" as gh
actor "Slack\nBot" as slack

rectangle "CI/CD Pipeline System" {
    package "Build & Test" {
        usecase "Push Code" as UC1
        usecase "Run CI Pipeline" as UC2
        usecase "Run Unit Tests" as UC3
        usecase "Run Integration Tests" as UC4
        usecase "Run Linter" as UC5
        usecase "Build Docker Image" as UC6
    }

    package "Review & Approve" {
        usecase "Create Pull Request" as UC7
        usecase "Review Code" as UC8
        usecase "Approve Merge" as UC9
    }

    package "Deploy" {
        usecase "Deploy to Staging" as UC10
        usecase "Run E2E Tests" as UC11
        usecase "Deploy to Production" as UC12
        usecase "Rollback" as UC13
    }

    package "Monitor" {
        usecase "Monitor Health" as UC14
        usecase "Send Alerts" as UC15
    }
}

dev --> UC1
dev --> UC7
gh --> UC2
lead --> UC8
lead --> UC9
ops --> UC12
ops --> UC13
ops --> UC14

UC2 ..> UC3 : <<include>>
UC2 ..> UC4 : <<include>>
UC2 ..> UC5 : <<include>>
UC2 ..> UC6 : <<include>>
UC9 ..> UC10 : <<include>>
UC10 ..> UC11 : <<include>>
UC12 ..> UC14 : <<include>>
UC13 ..> UC15 : <<include>>
UC15 --> slack
@enduml
```

## Template: SaaS Platform (Multi-Role)

```plantuml
@startuml
left to right direction
skinparam actorStyle awesome
skinparam backgroundColor white

actor "End User" as user
actor "Team Admin" as team_admin
actor "Super Admin" as super_admin
actor "Billing\nSystem" as billing

team_admin --|> user
super_admin --|> team_admin

rectangle "SaaS Platform" {
    usecase "Use Core Features" as UC1
    usecase "Manage Profile" as UC2
    usecase "View Dashboard" as UC3
    usecase "Invite Team Members" as UC4
    usecase "Manage Roles" as UC5
    usecase "Configure Workspace" as UC6
    usecase "Manage Billing" as UC7
    usecase "View Usage Analytics" as UC8
    usecase "Manage Tenants" as UC9
    usecase "System Configuration" as UC10
    usecase "Process Payment" as UC11
}

user --> UC1
user --> UC2
user --> UC3
team_admin --> UC4
team_admin --> UC5
team_admin --> UC6
team_admin --> UC7
team_admin --> UC8
super_admin --> UC9
super_admin --> UC10
UC7 ..> UC11 : <<include>>
UC11 --> billing
@enduml
```

## Best Practices

1. **Identify primary vs secondary actors** -- primary actors initiate; secondary actors respond (payment gateways, email services)
2. **Keep use cases verb-noun** -- "Place Order", "View Report" (not "Order" or "Reports")
3. **Use system boundaries** -- `rectangle` groups show what's inside vs outside the system
4. **`<<include>>` for mandatory sub-steps** -- e.g., Checkout always includes Process Payment
5. **`<<extend>>` for optional behavior** -- e.g., MFA optionally extends Login
6. **Actor generalization for role hierarchies** -- Admin inherits from User
7. **Limit to 7-15 use cases per diagram** -- split subsystems into separate diagrams if needed
8. **Output format** -- always output inside ` ```plantuml ` fenced code blocks
