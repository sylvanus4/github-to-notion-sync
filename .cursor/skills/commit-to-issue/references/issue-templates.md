# Issue Body Templates

## Standard Feature Issue

```markdown
## 주요 작업 내용

- [x] `ClassName` — Brief description of what it does
- [x] `function_name` — Brief description of what it does

## 관련 파일

- `path/to/file1.py`
- `path/to/file2.py`

## 성공 기준

- Criterion 1
- Criterion 2
- Criterion 3
```

## Infrastructure / Chore Issue

```markdown
## 주요 작업 내용

- [x] Configuration item 1
- [x] Configuration item 2

## 관련 파일

- `Dockerfile`
- `docker-compose.yml`
- `configs/file.yaml`

## 성공 기준

- Build/deploy succeeds
- Configuration loads correctly
```

## Test / Documentation Issue

```markdown
## 주요 작업 내용

- [x] Unit tests for module X (N test files)
- [x] Integration tests for pipeline Y (N test files)
- [x] Documentation for Z

## 관련 파일

- `tests/unit/test_*.py`
- `docs/*.md`

## 성공 기준

- All tests pass
- Documentation covers key modules
```

## Title Convention

Follow CONTRIBUTING.md format: `[TYPE] Summary`

| Type | When to use |
|------|-------------|
| `feat` | New features |
| `enhance` | Improve existing features |
| `refactor` | Code restructure without behavior change |
| `docs` | Documentation only |
| `fix` | Bug fixes |
| `style` | Formatting only |
| `test` | Test code |
| `chore` | Build, config, tooling |

## Grouping Heuristics

When multiple commits touch the same module, group them into a single issue:

1. **By directory**: Files in the same top-level directory = one issue
2. **By domain**: Related functionality across directories = one issue
3. **By commit type**: Same `[TYPE]` prefix with related scope = one issue

Target: 5-15 issues per batch. Fewer than 5 means grouping is too aggressive; more than 15 means splitting is too fine-grained.
