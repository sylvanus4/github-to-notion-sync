---
name: sleek-design-mobile-apps
description: >-
  Design mobile app screens via the Sleek REST API. Covers high-level requests
  ("design a fitness app") and specific actions ("list my projects", "create a
  new project", "screenshot that screen"). Supports natural language
  descriptions, async/sync modes, automated screenshot delivery, and code
  export for native frameworks. Use when the user asks to "design a mobile
  app", "create app screens", "Sleek project", "mobile UI prototype", "모바일 앱
  디자인", "앱 화면 만들기", "Sleek 프로젝트", "모바일 UI 프로토타입", "앱 디자인", "스크린 디자인",
  "sleek-design-mobile-apps", or wants to interact with their Sleek projects
  for designing, iterating, or exporting mobile app screens. Do NOT use for
  web frontend design (use anthropic-frontend-design). Do NOT use for Figma
  design workflows (use figma-dev-pipeline). Do NOT use for design system
  token management (use tailwind-design-system). Do NOT use for static
  image/poster creation (use anthropic-canvas-design). Do NOT use for video
  generation from designs (use pika-text-to-video). Korean triggers: "모바일 앱
  디자인", "앱 화면", "Sleek", "앱 프로토타입", "스크린 디자인", "모바일 UI".
---

# Designing with Sleek

[sleek.design](https://sleek.design) is an AI-powered mobile app design tool. Interact with it via a REST API at `/api/v1/*` to create projects, describe what you want built in plain language, and get back rendered screens.

**Base URL**: `https://sleek.design`
**Auth**: `Authorization: Bearer $SLEEK_API_KEY` on every `/api/v1/*` request
**Content-Type**: `application/json` (requests and responses)

## Prerequisites

Create API keys at **https://sleek.design/dashboard/api-keys**. The full key value is shown only once at creation -- store it in the `SLEEK_API_KEY` environment variable.

**Required plan**: Pro or higher (API access is gated).

### Key Scopes

| Scope | What it unlocks |
|---|---|
| `projects:read` | List / get projects |
| `projects:write` | Create / delete projects |
| `components:read` | List components in a project |
| `chats:read` | Get chat run status |
| `chats:write` | Send chat messages |
| `screenshots` | Render component screenshots |

Create a key with only the scopes needed for the task.

## Security

- **Single host**: All requests go exclusively to `https://sleek.design`. No data is sent to third parties.
- **HTTPS only**: The API key is transmitted only in the `Authorization` header to Sleek endpoints.
- **Minimal scopes**: Create API keys with only the scopes required. Prefer short-lived or revocable keys.
- **Image URLs**: When using `imageUrls` in chat messages, those URLs are fetched by Sleek's servers. Avoid passing URLs that contain sensitive content.

## Quick Reference -- All Endpoints

| Method | Path | Scope | Description |
|---|---|---|---|
| `GET` | `/api/v1/projects` | `projects:read` | List projects |
| `POST` | `/api/v1/projects` | `projects:write` | Create project |
| `GET` | `/api/v1/projects/:id` | `projects:read` | Get project |
| `DELETE` | `/api/v1/projects/:id` | `projects:write` | Delete project |
| `GET` | `/api/v1/projects/:id/components` | `components:read` | List components |
| `GET` | `/api/v1/projects/:id/components/:componentId` | `components:read` | Get component |
| `POST` | `/api/v1/projects/:id/chat/messages` | `chats:write` | Send chat message |
| `GET` | `/api/v1/projects/:id/chat/runs/:runId` | `chats:read` | Poll run status |
| `POST` | `/api/v1/screenshots` | `screenshots` | Render screenshot |

## Endpoints

### Projects

#### List projects

```http
GET /api/v1/projects?limit=50&offset=0
Authorization: Bearer $SLEEK_API_KEY
```

Response `200`:

```json
{
  "data": [
    {
      "id": "proj_abc",
      "name": "My App",
      "slug": "my-app",
      "createdAt": "2026-01-01T00:00:00Z",
      "updatedAt": "..."
    }
  ],
  "pagination": { "total": 12, "limit": 50, "offset": 0 }
}
```

#### Create project

```http
POST /api/v1/projects
Authorization: Bearer $SLEEK_API_KEY
Content-Type: application/json

{ "name": "My New App" }
```

Response `201` -- same shape as a single project.

#### Get / Delete project

```http
GET    /api/v1/projects/:projectId
DELETE /api/v1/projects/:projectId   -> 204 No Content
```

### Components

#### List components

```http
GET /api/v1/projects/:projectId/components?limit=50&offset=0
Authorization: Bearer $SLEEK_API_KEY
```

Response `200`:

```json
{
  "data": [
    {
      "id": "cmp_xyz",
      "name": "Hero Section",
      "activeVersion": 3,
      "versions": [{ "id": "ver_001", "version": 1, "code": "<!DOCTYPE html>...</html>", "createdAt": "..." }],
      "createdAt": "...",
      "updatedAt": "..."
    }
  ],
  "pagination": { "total": 5, "limit": 50, "offset": 0 }
}
```

#### Get component

Fetches a single component by ID. Use this when you need the code for a specific screen (e.g., after a chat run returns a `componentId` in its operations).

```http
GET /api/v1/projects/:projectId/components/:componentId
Authorization: Bearer $SLEEK_API_KEY
```

### Chat -- Send Message

Describe what you want in `message.text` and the AI creates or modifies screens.

```http
POST /api/v1/projects/:projectId/chat/messages?wait=false
Authorization: Bearer $SLEEK_API_KEY
Content-Type: application/json
idempotency-key: <optional, max 255 chars>

{
  "message": { "text": "Add a pricing section with three tiers" },
  "imageUrls": ["https://example.com/ref.png"],
  "target": { "screenId": "scr_abc" }
}
```

| Field | Required | Notes |
|---|---|---|
| `message.text` | Yes | 1+ chars, trimmed |
| `imageUrls` | No | HTTPS URLs only; included as visual context |
| `target.screenId` | No | Edit a specific screen; omit to let AI decide |
| `?wait=true/false` | No | Sync wait mode (default: false) |
| `idempotency-key` header | No | Replay-safe re-sends |

#### Async response (default, `wait=false`)

Status `202 Accepted`. `result` and `error` are absent until the run reaches a terminal state.

```json
{
  "data": {
    "runId": "run_111",
    "status": "queued",
    "statusUrl": "/api/v1/projects/proj_abc/chat/runs/run_111"
  }
}
```

#### Sync response (`wait=true`)

Blocks up to **300 seconds**. Returns `200` when completed, `202` if timed out.

```json
{
  "data": {
    "runId": "run_111",
    "status": "completed",
    "statusUrl": "...",
    "result": {
      "assistantText": "I added a pricing section with...",
      "operations": [
        { "type": "screen_created", "screenId": "scr_xyz", "screenName": "Pricing", "componentId": "cmp_xyz" },
        { "type": "screen_updated", "screenId": "scr_abc", "componentId": "cmp_abc" },
        { "type": "theme_updated" }
      ]
    }
  }
}
```

### Chat -- Poll Run Status

Use after async send to check progress.

```http
GET /api/v1/projects/:projectId/chat/runs/:runId
Authorization: Bearer $SLEEK_API_KEY
```

**Run status lifecycle**: `queued` -> `running` -> `completed | failed`

When failed, `error` is present:

```json
{
  "data": {
    "runId": "run_111",
    "status": "failed",
    "error": { "code": "execution_failed", "message": "..." }
  }
}
```

### Screenshots

Takes a snapshot of one or more rendered components.

```http
POST /api/v1/screenshots
Authorization: Bearer $SLEEK_API_KEY
Content-Type: application/json

{
  "componentIds": ["cmp_xyz", "cmp_abc"],
  "projectId": "proj_abc",
  "format": "png",
  "scale": 2,
  "gap": 40,
  "padding": 40,
  "background": "transparent"
}
```

| Field | Default | Notes |
|---|---|---|
| `format` | `png` | `png` or `webp` |
| `scale` | `2` | 1-3 (device pixel ratio) |
| `gap` | `40` | Pixels between components |
| `padding` | `40` | Uniform padding on all sides |
| `paddingX/Y` | _(optional)_ | Axis-level override |
| `paddingTop/Right/Bottom/Left` | _(optional)_ | Per-side override |
| `background` | `transparent` | Any CSS color |
| `showDots` | `false` | Overlay a subtle dot grid on the background |

Padding resolves with a cascade: per-side -> axis -> uniform.

Always use `"background": "transparent"` unless the user explicitly requests a specific background color.

Response: raw binary `image/png` or `image/webp` with `Content-Disposition: attachment`.

## Error Shapes

```json
{ "code": "UNAUTHORIZED", "message": "..." }
```

| HTTP | Code | When |
|---|---|---|
| 401 | `UNAUTHORIZED` | Missing/invalid/expired API key |
| 403 | `FORBIDDEN` | Valid key, wrong scope or plan |
| 404 | `NOT_FOUND` | Resource doesn't exist |
| 400 | `BAD_REQUEST` | Validation failure |
| 409 | `CONFLICT` | Another run is active for this project |
| 500 | `INTERNAL_SERVER_ERROR` | Server error |

Chat run-level errors (inside `data.error`):

| Code | Meaning |
|---|---|
| `out_of_credits` | Organization has no credits left |
| `execution_failed` | AI execution error |

## Designing Workflow

### 1. Create a project

Create with `POST /api/v1/projects` if one doesn't exist yet. Each project has its own theme, style, and design system. Create separate projects for different design variations.

### 2. Send a chat message

Describe what to build using `POST /api/v1/projects/:id/chat/messages`. Pass the user's request as-is -- don't add details the user didn't ask for. Sleek produces richer designs when given room to plan.

**Polling**: start at 2s interval, back off to 5s after 10s, give up after 5 minutes.

**Editing a specific screen**: use `target.screenId` (from operations, not `componentId`).

**One run at a time**: only one active run per project. `409 CONFLICT` means wait for the current run. Different projects can run in parallel using async polling.

**Safe retries**: add an `idempotency-key` header for replay-safe re-sends.

### 3. Show the results

After every chat run that produces `screen_created` or `screen_updated` operations, **always take screenshots and show them to the user**. Never silently complete a chat run without delivering the visuals.

- **New screens**: one screenshot per screen + one combined screenshot of all screens.
- **Updated screens**: one screenshot per affected screen.

Save screenshots in the project directory, not a temporary folder.

## Implementing Designs

When the user wants to implement designs in code, **always fetch the component HTML code** -- do not rely on screenshots alone. Use `GET /api/v1/projects/:id/components/:componentId` for each screen.

### HTML prototypes

The component `code` is a complete HTML document -- save it directly to a `.html` file.

### Native frameworks (React Native, SwiftUI, etc.)

- **HTML code** is the implementation reference (structure, layout, styling, colors, spacing, content, image URLs, icon names).
- **Screenshots** are the visual target.

#### Icons

Sleek uses [Iconify](https://iconify.design) icons in `prefix:name` format (e.g., `solar:heart-bold`). Common sets: **Solar**, **Hugeicons**, **Material Symbols**, **MDI**.

Use the exact icons from the HTML code. Fetch SVGs from `https://api.iconify.design/{prefix}/{name}.svg` and embed them. For React Native/Expo, use `react-native-svg`'s `SvgXml` component.

#### Fonts

Extract font family names and weights from Google Fonts `<link>` tags in the HTML `<head>`.

#### Navigation

Update the project's navigation styling and structure to match the designs.

## Pagination

All list endpoints accept `limit` (1-100, default 50) and `offset` (>=0). Response includes `pagination.total`.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Missing `Authorization` header | Add `Authorization: Bearer $SLEEK_API_KEY` to every request |
| Wrong scope | Check key's scopes match the endpoint |
| Sending next message before run completes | Poll until `completed`/`failed` before next send |
| Using `wait=true` on long generations | Blocks 300s max; have a fallback to polling for `202` |
| HTTP URLs in `imageUrls` | Only HTTPS URLs are accepted |
| Assuming `result` is present on `202` | `result` is absent until `completed` |
| Using `screenId` as `componentIds` in screenshots | Use `componentId` from operations for screenshots |
