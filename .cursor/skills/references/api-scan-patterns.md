# API Scan Patterns by Framework

How to locate API definitions, schemas, and routing in common backend frameworks.

## NestJS (TypeScript)

| Artifact | File Patterns | Key Decorators/Patterns |
|----------|--------------|------------------------|
| Endpoints | `*.controller.ts` | `@Get()`, `@Post()`, `@Put()`, `@Delete()`, `@Patch()` |
| DTOs | `*.dto.ts`, `dto/` | `class CreateXxxDto`, class-validator decorators |
| Entities | `*.entity.ts`, `entities/` | `@Entity()`, `@Column()`, `@ManyToOne()` |
| Guards | `*.guard.ts` | `@UseGuards()`, `canActivate()` |
| Modules | `*.module.ts` | `@Module({ controllers, providers })` |
| Routes | `app.module.ts`, `main.ts` | `setGlobalPrefix()`, module imports |

## Express (JavaScript/TypeScript)

| Artifact | File Patterns | Key Patterns |
|----------|--------------|-------------|
| Endpoints | `routes/*.ts`, `router/*.ts` | `router.get()`, `router.post()`, `app.use()` |
| Middleware | `middleware/*.ts` | `app.use()`, `router.use()` |
| Validation | `validators/`, `schemas/` | Joi, Zod, express-validator |

## FastAPI (Python)

| Artifact | File Patterns | Key Patterns |
|----------|--------------|-------------|
| Endpoints | `routers/*.py`, `api/*.py` | `@router.get()`, `@app.post()` |
| Schemas | `schemas/*.py`, `models/*.py` | `class XxxSchema(BaseModel)` |
| Dependencies | `deps.py`, `dependencies/` | `Depends()` |

## Spring Boot (Java/Kotlin)

| Artifact | File Patterns | Key Patterns |
|----------|--------------|-------------|
| Endpoints | `*Controller.java` | `@RestController`, `@RequestMapping` |
| DTOs | `*Dto.java`, `*Request.java` | POJO with validation annotations |
| Entities | `*Entity.java` | `@Entity`, `@Table` |

## Django REST Framework (Python)

| Artifact | File Patterns | Key Patterns |
|----------|--------------|-------------|
| Endpoints | `views.py`, `viewsets.py` | `class XxxViewSet(ViewSet)`, `@api_view` |
| Serializers | `serializers.py` | `class XxxSerializer(ModelSerializer)` |
| URLs | `urls.py` | `path()`, `router.register()` |

## General Scan Strategy

1. Check `package.json` / `requirements.txt` / `pom.xml` / `build.gradle` for framework
2. Find the entry point (`main.ts`, `app.py`, `Application.java`)
3. Trace routing configuration to find all registered endpoints
4. For each endpoint, find the handler function and trace to DTOs/schemas
5. Look for middleware/guards/dependencies for auth and validation
