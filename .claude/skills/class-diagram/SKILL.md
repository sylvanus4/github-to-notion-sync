---
name: class-diagram
description: >-
  Create class diagrams, interface hierarchies, and object relationship
  diagrams using Mermaid classDiagram syntax and PlantUML UML syntax. Supports
  classes, interfaces, abstract classes, enums, inheritance, composition,
  aggregation, association, dependency, generics, and annotations. Use when
  the user asks to "create class diagram", "UML class diagram", "object
  model", "domain model", "entity relationships", "type hierarchy", "interface
  diagram", "클래스 다이어그램", "UML 클래스", "도메인 모델", "객체 관계", "타입 계층", "인터페이스 다이어그램",
  or needs to visualize class structures, inheritance trees, or type
  relationships. Do NOT use for database ER diagrams with cardinality only
  (use Mermaid erDiagram directly). Do NOT use for state transitions (use
  state-diagram skill). Do NOT use for process flows (use flowchart or
  workflow-diagram skill). Do NOT use for architecture layers (use
  architecture-diagram skill). Do NOT use for deployment topology (use
  deployment-diagram skill).
disable-model-invocation: true
---

# Class Diagram Generator

**Quick Start:** Define classes with attributes/methods -> Add relationships (inheritance, composition, association) -> Apply styling and notes.

## Mermaid classDiagram (Preferred for Simple/Medium Complexity)

### Critical Rules

#### Rule 1: Mermaid Code Fence
Always output inside ` ```mermaid ` fenced code blocks using `classDiagram`.

#### Rule 2: Class Definition
```
class ClassName {
    +publicAttr : Type
    -privateAttr : Type
    #protectedAttr : Type
    ~packageAttr : Type
    +publicMethod(param: Type) ReturnType
    -privateMethod() void
    #protectedMethod()* ReturnType
    +abstractMethod()* void
    +staticMethod()$ ReturnType
}
```

Visibility prefixes:
| Prefix | Visibility |
|---|---|
| `+` | public |
| `-` | private |
| `#` | protected |
| `~` | package/internal |

Method modifiers:
| Suffix | Meaning |
|---|---|
| `*` | abstract |
| `$` | static |

#### Rule 3: Relationships
| Relationship | Syntax | Meaning |
|---|---|---|
| Inheritance | `Parent <\|-- Child` | Child extends Parent |
| Realization | `Interface <\|.. Implementation` | Implements interface |
| Composition | `Whole *-- Part` | Part cannot exist without Whole |
| Aggregation | `Container o-- Item` | Item can exist independently |
| Association | `ClassA --> ClassB` | Uses / references |
| Dependency | `ClassA ..> ClassB` | Depends on |
| Link (solid) | `ClassA -- ClassB` | Bidirectional association |

#### Rule 4: Cardinality
```
ClassA "1" --> "0..*" ClassB : contains
```

#### Rule 5: Annotations
```
class MyInterface {
    <<interface>>
}

class MyAbstract {
    <<abstract>>
}

class MyEnum {
    <<enumeration>>
    VALUE_A
    VALUE_B
}

class MyService {
    <<service>>
}
```

#### Rule 6: Generics
```
class List~T~ {
    +add(item: T) void
    +get(index: int) T
}
```

#### Rule 7: Namespace (Grouping)
```
namespace DomainLayer {
    class User
    class Order
}
```

### Template: E-Commerce Domain Model (Mermaid)

```mermaid
classDiagram
    class User {
        <<abstract>>
        -id: UUID
        -email: String
        -createdAt: DateTime
        +getDisplayName() String*
        +validateEmail()$ boolean
    }

    class Customer {
        -shippingAddresses: List~Address~
        -loyaltyPoints: int
        +getDisplayName() String
        +placeOrder(cart: Cart) Order
    }

    class Admin {
        -role: AdminRole
        -permissions: Set~Permission~
        +getDisplayName() String
        +manageUsers() void
    }

    class AdminRole {
        <<enumeration>>
        SUPER_ADMIN
        CONTENT_MANAGER
        SUPPORT_AGENT
    }

    class Order {
        -id: UUID
        -status: OrderStatus
        -totalAmount: Money
        -items: List~OrderItem~
        +calculateTotal() Money
        +cancel() void
        +ship(tracking: String) void
    }

    class OrderItem {
        -product: Product
        -quantity: int
        -unitPrice: Money
        +getSubtotal() Money
    }

    class Product {
        -id: UUID
        -name: String
        -price: Money
        -stock: int
        +isAvailable() boolean
        +reserve(qty: int) void
    }

    class OrderStatus {
        <<enumeration>>
        PENDING
        CONFIRMED
        SHIPPED
        DELIVERED
        CANCELLED
    }

    class Money {
        <<value object>>
        -amount: BigDecimal
        -currency: Currency
        +add(other: Money) Money
        +multiply(factor: int) Money
    }

    User <|-- Customer
    User <|-- Admin
    Admin --> AdminRole
    Customer "1" --> "0..*" Order : places
    Order *-- "1..*" OrderItem : contains
    OrderItem --> Product : references
    Order --> OrderStatus
    Order --> Money : totalAmount
    OrderItem --> Money : unitPrice
    Product --> Money : price
```

### Template: Repository Pattern (Mermaid)

```mermaid
classDiagram
    class Repository~T~ {
        <<interface>>
        +findById(id: ID) T
        +findAll() List~T~
        +save(entity: T) T
        +delete(id: ID) void
    }

    class UserRepository {
        <<interface>>
        +findByEmail(email: String) User
        +findByRole(role: Role) List~User~
    }

    class JpaUserRepository {
        -entityManager: EntityManager
        +findById(id: ID) User
        +findAll() List~User~
        +save(entity: User) User
        +delete(id: ID) void
        +findByEmail(email: String) User
        +findByRole(role: Role) List~User~
    }

    class UserService {
        -userRepository: UserRepository
        -passwordEncoder: PasswordEncoder
        +register(dto: RegisterDTO) User
        +authenticate(email: String, password: String) AuthToken
    }

    class PasswordEncoder {
        <<interface>>
        +encode(raw: String) String
        +matches(raw: String, encoded: String) boolean
    }

    class BCryptPasswordEncoder {
        -strength: int
        +encode(raw: String) String
        +matches(raw: String, encoded: String) boolean
    }

    Repository~T~ <|-- UserRepository
    UserRepository <|.. JpaUserRepository
    UserService --> UserRepository : depends
    UserService --> PasswordEncoder : depends
    PasswordEncoder <|.. BCryptPasswordEncoder
```

## PlantUML (Preferred for Complex/Large Diagrams)

### When to Use PlantUML Over Mermaid
- Diagrams with 15+ classes
- Need for `skinparam` fine-tuning
- Package/namespace grouping with nesting
- Note blocks and constraints
- Stereotypes beyond `<<interface>>`

### Template: Layered Architecture Classes (PlantUML)

```plantuml
@startuml
skinparam classAttributeIconSize 0
skinparam backgroundColor white

package "Presentation Layer" #LightBlue {
    class UserController {
        -userService: UserService
        +getUser(id: UUID): ResponseEntity
        +createUser(dto: CreateUserDTO): ResponseEntity
        +updateUser(id: UUID, dto: UpdateUserDTO): ResponseEntity
    }
}

package "Application Layer" #LightGreen {
    interface UserService <<interface>> {
        +findById(id: UUID): UserDTO
        +create(dto: CreateUserDTO): UserDTO
        +update(id: UUID, dto: UpdateUserDTO): UserDTO
    }

    class UserServiceImpl {
        -userRepository: UserRepository
        -eventPublisher: EventPublisher
        +findById(id: UUID): UserDTO
        +create(dto: CreateUserDTO): UserDTO
        +update(id: UUID, dto: UpdateUserDTO): UserDTO
    }
}

package "Domain Layer" #LightYellow {
    class User <<Entity>> {
        -id: UUID
        -email: Email
        -name: Name
        -status: UserStatus
        +activate(): void
        +deactivate(): void
    }

    class Email <<Value Object>> {
        -value: String
        +validate(): boolean
    }

    enum UserStatus {
        ACTIVE
        INACTIVE
        SUSPENDED
    }

    interface UserRepository <<interface>> {
        +findById(id: UUID): Optional<User>
        +save(user: User): User
    }
}

package "Infrastructure Layer" #MistyRose {
    class JpaUserRepository {
        -entityManager: EntityManager
        +findById(id: UUID): Optional<User>
        +save(user: User): User
    }
}

UserController --> UserService
UserService <|.. UserServiceImpl
UserServiceImpl --> UserRepository
UserRepository <|.. JpaUserRepository
User --> Email
User --> UserStatus
UserServiceImpl --> User : creates/reads
@enduml
```

## Best Practices

1. **Group by layer or module** -- use `namespace` (Mermaid) or `package` (PlantUML) to organize
2. **Show visibility** -- always prefix attributes and methods with `+`, `-`, `#`, `~`
3. **Distinguish relationships** -- composition (`*--`) vs aggregation (`o--`) vs association (`-->`)
4. **Add cardinality** -- `"1"` to `"0..*"` on association ends
5. **Use annotations** -- `<<interface>>`, `<<abstract>>`, `<<enumeration>>`, `<<value object>>`
6. **Name relationships** -- label association arrows with role names
7. **Keep it focused** -- one diagram per bounded context or module; 8-15 classes per diagram
8. **Output format** -- ` ```mermaid ` for Mermaid, ` ```plantuml ` for PlantUML
