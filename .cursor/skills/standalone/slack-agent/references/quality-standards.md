# Quality Standards

Mandatory quality requirements for Slack agent projects.

## After Every File Modification

1. **Run linting**:
   ```bash
   npm run lint
   ```
   If using ESLint, auto-fix with `npm run lint -- --fix`.

2. **Check for test file**: If `foo.ts` was modified, check if `foo.test.ts` exists. If not and the file exports functions, create one.

## Before Completing Any Task

```bash
npx tsc --noEmit     # TypeScript compilation - must pass
npm run lint         # Linting - no errors
npm test             # All tests must pass
```

Do NOT mark a task complete if any check fails.

## Unit Tests

- **Location**: Co-located `*.test.ts` files or `src/__tests__/`
- **Framework**: Vitest (recommended) or Jest
- **Coverage**: All exported functions must have tests

```typescript
import { describe, it, expect, vi } from "vitest";
import { processCommand } from "./commands";

describe("processCommand", () => {
  it("should handle normal input", () => {
    expect(processCommand("hello")).toBeDefined();
  });

  it("should handle empty input", () => {
    expect(processCommand("")).toBe("Please provide a question.");
  });
});
```

## Mocking Slack Client

```typescript
import { vi } from "vitest";

const mockClient = {
  chat: {
    postMessage: vi.fn().mockResolvedValue({ ok: true }),
  },
  conversations: {
    replies: vi.fn().mockResolvedValue({ messages: [] }),
  },
};
```

## Integration Tests

Required when modifying:
- Bot mention handlers / message handlers
- Slash commands
- Interactive components (buttons, modals)
- Bot responses

Integration tests verify the full flow from Slack event to bot response.

## Vitest Configuration

```typescript
// vitest.config.ts
import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    globals: true,
    environment: "node",
    coverage: {
      provider: "v8",
      reporter: ["text", "json", "html"],
    },
  },
});
```

## ESLint Configuration

```json
{
  "extends": ["eslint:recommended", "plugin:@typescript-eslint/recommended"],
  "parser": "@typescript-eslint/parser",
  "plugins": ["@typescript-eslint"],
  "rules": {
    "@typescript-eslint/no-unused-vars": "error",
    "no-console": ["warn", { "allow": ["error", "warn"] }]
  }
}
```

## TypeScript Configuration

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "Node16",
    "moduleResolution": "Node16",
    "strict": true,
    "outDir": "dist",
    "rootDir": "src",
    "esModuleInterop": true,
    "skipLibCheck": true
  },
  "include": ["src"]
}
```
