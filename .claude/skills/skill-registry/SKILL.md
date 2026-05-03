---
name: skill-registry
description: >-
  Design a database-backed skill registry with CRUD operations, multi-file
  support, workspace scoping, and external import from GitHub/ClawHub/SkillHub
  sources. Use when designing platform-level skill management systems,
  building skill CRUD APIs for multi-user agent platforms, implementing skill
  import from GitHub repos or skill marketplaces, planning skill sharing and
  discovery across workspaces, designing skill versioning and compatibility
  checking, or reviewing skill management code. Do NOT use for creating
  individual SKILL.md files manually (use create-skill), auditing local skill
  quality (use skill-optimizer), autonomous skill prompt optimization (use
  skill-autoimprove), session transcript mining (use autoskill-evolve), skill
  execution or routing at runtime (use sefo-orchestrator), or cross-repo
  .cursor/ asset sync (use cursor-sync). Korean triggers: '스킬 레지스트리', '스킬 관리
  시스템', '스킬 CRUD', '스킬 임포트', '스킬 마켓플레이스'.
disable-model-invocation: true
---

# Skill Registry

Guide the design and implementation of a centralized, database-backed skill
registry that elevates skills from local filesystem artifacts to platform-managed
resources with versioning, workspace scoping, and external import capabilities.

## Architecture Overview

```
┌─────────────────────────────────────────────────┐
│                  Web UI / CLI                    │
│  ┌────────────────────────────────────────────┐  │
│  │ Browse │ Search │ Install │ Import │ Author │  │
│  └────────────────────────────────────────────┘  │
└─────────────────┬───────────────────────────────┘
                  │ REST API
                  ▼
┌─────────────────────────────────────────────────┐
│              Skill API Service                   │
│  ┌──────────────┬──────────────┬─────────────┐  │
│  │ CRUD Handler │ Import Engine│ Validator    │  │
│  └──────────────┴──────────────┴─────────────┘  │
│  ┌──────────────┬──────────────┬─────────────┐  │
│  │ Search Index │ ACL Checker  │ Event Pub    │  │
│  └──────────────┴──────────────┴─────────────┘  │
└─────────────────┬───────────────────────────────┘
                  │
    ┌─────────────┼─────────────┐
    ▼             ▼             ▼
┌────────┐  ┌──────────┐  ┌──────────────┐
│Postgres│  │  NATS    │  │ External     │
│ skills │  │  events  │  │ Sources      │
│ + files│  │          │  │ GitHub/Hub   │
└────────┘  └──────────┘  └──────────────┘
```

## 1. Skill Data Model

A skill is a named, versioned, workspace-scoped resource containing one or more
files (primary SKILL.md + optional supporting files).

### Database Schema

```sql
CREATE TABLE skills (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    description TEXT NOT NULL DEFAULT '',
    content TEXT NOT NULL DEFAULT '',
    config JSONB DEFAULT '{}',
    source TEXT,                    -- 'local', 'github', 'clawhub', 'skillhub'
    source_url TEXT,                -- original import URL
    source_version TEXT,            -- version/sha at time of import
    created_by UUID REFERENCES users(id) ON DELETE SET NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE(workspace_id, name)
);

CREATE TABLE skill_files (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    skill_id UUID NOT NULL REFERENCES skills(id) ON DELETE CASCADE,
    path TEXT NOT NULL,
    content TEXT NOT NULL DEFAULT '',
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE(skill_id, path)
);

CREATE INDEX idx_skills_workspace ON skills(workspace_id);
CREATE INDEX idx_skills_source ON skills(source) WHERE source IS NOT NULL;
CREATE INDEX idx_skill_files_skill ON skill_files(skill_id);
```

### Key design decisions

- `workspace_id` scopes all skills — no global skills (prevents supply-chain risk)
- `name` is unique per workspace — duplicates blocked at DB level
- `content` holds the primary SKILL.md content
- `config` stores structured metadata (tags, triggers, version, dependencies)
- `source` + `source_url` + `source_version` track provenance for imported skills
- `skill_files` supports multi-file skills (e.g., helper scripts, templates, examples)

## 2. CRUD API

### Create Skill

```
POST /api/workspaces/{workspaceId}/skills

Request:
{
  "name": "agent-daemon-protocol",
  "description": "Daemon-server communication protocol for agent platforms",
  "content": "---\nname: agent-daemon-protocol\n...",
  "config": {
    "tags": ["agent", "daemon", "protocol", "infrastructure"],
    "version": "1.0.0",
    "triggers": ["daemon registration", "heartbeat"]
  },
  "files": [
    {
      "path": "examples/register-request.json",
      "content": "{ \"workspace_id\": \"...\", ... }"
    }
  ]
}

Response: 201 Created
{
  "id": "uuid",
  "workspace_id": "uuid",
  "name": "agent-daemon-protocol",
  ...
}
```

### Read Skill

```
GET /api/workspaces/{workspaceId}/skills/{skillId}
GET /api/workspaces/{workspaceId}/skills/{skillId}/files

Response: 200 OK (includes files array)
```

### List Skills

```
GET /api/workspaces/{workspaceId}/skills?search=daemon&tags=agent,infra

Response: 200 OK
{
  "skills": [...],
  "total": 42,
  "page": 1,
  "page_size": 20
}
```

### Update Skill

```
PUT /api/workspaces/{workspaceId}/skills/{skillId}

Request:
{
  "description": "Updated description",
  "content": "...",
  "config": { ... },
  "files": [
    { "path": "examples/register-request.json", "content": "..." }
  ]
}
```

**Design constraints:**
- Updates use a database transaction wrapping skill + files
- File updates are replace-all (delete existing files, insert new set)
- `updated_at` timestamp is always refreshed
- Publish an event on NATS for skill-change subscribers

### Delete Skill

```
DELETE /api/workspaces/{workspaceId}/skills/{skillId}

Response: 204 No Content
```

## 3. File Path Validation

Multi-file skills support arbitrary file paths, but must prevent path traversal
and dangerous patterns.

```go
func validateFilePath(path string) error {
    if path == "" {
        return errors.New("file path cannot be empty")
    }
    if strings.Contains(path, "..") {
        return errors.New("path traversal (..) not allowed")
    }
    if filepath.IsAbs(path) {
        return errors.New("absolute paths not allowed")
    }
    if strings.ContainsAny(path, "\x00") {
        return errors.New("null bytes not allowed in paths")
    }
    clean := filepath.Clean(path)
    if clean != path {
        return errors.New("path must be in canonical form")
    }
    return nil
}
```

**Blocked patterns:**
- `../../../etc/passwd` — path traversal
- `/usr/local/bin/evil` — absolute paths
- `foo\x00bar` — null byte injection
- `./foo/../bar` — non-canonical paths

## 4. External Import

Import skills from external sources into the workspace registry.

### Import from GitHub Repository

```
POST /api/workspaces/{workspaceId}/skills/import

Request:
{
  "source": "github",
  "url": "https://github.com/org/repo",
  "path": ".cursor/skills/infra/agent-daemon-protocol",
  "ref": "main"
}

Import pipeline:
1. Validate URL format and accessibility
2. Fetch SKILL.md from {url}/tree/{ref}/{path}/SKILL.md
3. Scan for additional files in the directory
4. Parse SKILL.md frontmatter for metadata
5. Check for name collision in workspace
6. Create skill with source='github', source_url, source_version=commit SHA
7. Store all files in skill_files table
```

### Import from Skill Hub / Registry

```
POST /api/workspaces/{workspaceId}/skills/import

Request:
{
  "source": "skillhub",
  "skill_id": "published-skill-uuid",
  "version": "1.2.0"
}
```

### Update Check

```
GET /api/workspaces/{workspaceId}/skills/{skillId}/updates

Response:
{
  "has_update": true,
  "current_version": "1.0.0",
  "latest_version": "1.2.0",
  "changelog": "Added support for..."
}
```

**Design constraints:**
- Imported skills are copies, not links — they don't auto-update
- `source_version` records the state at import time
- Update check compares against current source
- User must explicitly pull updates (no silent changes)

## 5. Skill Search & Discovery

### Full-text Search

```sql
-- PostgreSQL full-text search on skill name + description + content
CREATE INDEX idx_skills_search ON skills USING gin(
    to_tsvector('english', name || ' ' || description || ' ' || content)
);

SELECT * FROM skills
WHERE workspace_id = $1
  AND to_tsvector('english', name || ' ' || description || ' ' || content)
      @@ plainto_tsquery('english', $2)
ORDER BY ts_rank(...) DESC;
```

### Tag-based Filtering

```sql
SELECT * FROM skills
WHERE workspace_id = $1
  AND config->'tags' ?| array['agent', 'infrastructure']
ORDER BY name;
```

## 6. Workspace Scoping & Access Control

- All skills belong to exactly one workspace
- Workspace members can view all skills in their workspace
- Create/update/delete requires workspace `admin` or `member` role
- Skills are NOT visible across workspaces (isolation by design)
- For skill sharing: use export/import, not cross-workspace references

## 7. Skill-to-Agent Binding

Agents reference skills they can use. This enables skill routing at runtime.

```sql
CREATE TABLE agent_skills (
    agent_id UUID NOT NULL REFERENCES agents(id) ON DELETE CASCADE,
    skill_id UUID NOT NULL REFERENCES skills(id) ON DELETE CASCADE,
    PRIMARY KEY (agent_id, skill_id)
);
```

When an agent is configured, selected skills are bound via this join table.
The agent daemon receives skill content as part of the task claim response.

## Integration with ThakiCloud Agent Cloud

This pattern maps to the following Agent Cloud roadmap items:
- **Phase 0**: Skill CRUD as part of API Server foundation
- **Phase 1**: Skill Marketplace (import from external sources)
- **Phase 2**: Skill Router uses registry for routing decisions
- **Phase 3**: Web Agent Studio skill browser and editor

Adapt for existing infrastructure:
- Skills API runs within the existing Go/Fiber backend
- PostgreSQL schema integrates with existing migration pipeline
- NATS events for skill changes feed into existing event infrastructure
- Existing 700+ local .cursor/skills/ files can be bulk-imported as seed data
- SEFO orchestrator can query the registry instead of scanning filesystem

## Migration from Local Skills

To bootstrap the registry from existing local skills:

```
1. Scan .cursor/skills/**/**/SKILL.md recursively
2. Parse frontmatter (name, description, tags, version)
3. Collect sibling files as skill_files
4. Insert into skills + skill_files tables
5. Set source='local', source_url=relative path
6. Verify count matches filesystem count
```

Estimated seed: ~700 skills from the current project.

## Examples

### Creating a skill via API

```
POST /api/v1/workspaces/{ws_id}/skills
{
  "name": "deploy-checklist",
  "description": "Pre-deploy checklist with rollback steps",
  "tags": ["devops", "deploy"],
  "files": [
    { "path": "SKILL.md", "content": "---\nname: deploy-checklist\n..." },
    { "path": "references/rollback-steps.md", "content": "## Rollback\n..." }
  ]
}
→ 201 { "id": "skill_abc123", "version": 1, "created_at": "..." }
```

### Importing from GitHub

```
POST /api/v1/workspaces/{ws_id}/skills/import
{
  "source_type": "github",
  "source_url": "https://github.com/org/repo",
  "path": ".cursor/skills/deploy-checklist"
}
→ Server clones sparse checkout → parses SKILL.md frontmatter
→ Creates skill record with source_type=github, source_url, source_ref (SHA)
→ 201 { "id": "skill_def456", "source_ref": "abc1234", ... }
```

### Agent task claiming with skills

```
Daemon claims task → response includes:
{
  "task_id": "...",
  "agent_skills": [
    { "name": "deploy-checklist", "content": "---\nname: deploy-checklist\n..." },
    { "name": "rollback-guide",   "content": "..." }
  ]
}
Daemon injects skills into agent CLI --skills flag
```

## Error Handling

| Error | Cause | Recovery |
|-------|-------|----------|
| 409 on create | Skill with same name exists in workspace | Return existing skill ID; suggest update instead |
| 400 on file path | Path traversal (`../`) or null bytes detected | Reject entire request; do not partial-create |
| 404 on import | GitHub repo or path not found | Return source URL in error; suggest checking path |
| 422 on import | SKILL.md missing or invalid frontmatter | Return parse error details; require valid frontmatter |
| 500 on bulk import | Transaction failure mid-import | Rollback entire batch; return count of processed/failed |
| Stale import | Source repo updated after import | update-check endpoint returns `has_updates: true` |

## Gotchas

- Skill names MUST be unique per workspace — use `(workspace_id, name)` unique constraint, not global uniqueness
- File path validation must reject `..`, absolute paths, and null bytes BEFORE any I/O — path traversal is a critical vulnerability
- Multi-file skill updates MUST be atomic — delete-all-then-insert inside a single transaction; partial updates corrupt skill state
- Full-text search needs a GIN index on `tsvector` — without it, `ts_rank` queries on 700+ skills will be unusably slow
- Import `source_ref` MUST store the exact Git SHA, not branch names — branches move, SHAs don't
- NATS events on skill CRUD are critical for cache invalidation — stale skill content in agent sessions causes subtle misbehavior
- Bulk import from local `.cursor/skills/` must handle skills with no frontmatter gracefully — log and skip, don't fail the batch

## Checklist

- [ ] Design and migrate `skills` + `skill_files` database schema
- [ ] Implement CRUD API handlers with workspace scoping
- [ ] Build file path validation (prevent traversal, null bytes)
- [ ] Create transactional skill update (atomic skill + files replace)
- [ ] Implement full-text search with PostgreSQL GIN index
- [ ] Build tag-based filtering with JSONB operators
- [ ] Design import pipeline for GitHub repositories
- [ ] Design import pipeline for skill hub/registry
- [ ] Implement update-check endpoint for imported skills
- [ ] Build agent-skill binding (join table + claim response injection)
- [ ] Create bulk import script for local .cursor/skills/ migration
- [ ] Publish NATS events on skill create/update/delete
- [ ] Add access control checks (workspace member/admin roles)
- [ ] Write API tests for CRUD + import + search flows
- [ ] Build UI for skill browsing, search, and import
