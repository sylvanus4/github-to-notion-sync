# EOD Ship — Managed Project Registry

## Project Table

| Order | Alias | Repo | Path (회사) | Path (집) | Mode |
|-------|-------|------|-------------|-----------|------|
| 1 | `github-to-notion-sync` | `sylvanus4/github-to-notion-sync` | `/Users/hanhyojung/work/thakicloud/github-to-notion-sync` | `/Users/hanhyojung/thaki/github-to-notion-sync` | full |
| 2 | `ai-template` | `thakicloud/ai-template` | `/Users/hanhyojung/work/thakicloud/ai-template` | `/Users/hanhyojung/thaki/ai-template` | full |
| 3 | `ai-model-event-stock-analytics` | `thakicloud/ai-model-event-stock-analytics` | `/Users/hanhyojung/work/thakicloud/ai-model-event-stock-analytics` | `/Users/hanhyojung/thaki/ai-model-event-stock-analytics` | full |
| 4 | `research` | `thakicloud/research` | `/Users/hanhyojung/work/thakicloud/research` | `/Users/hanhyojung/thaki/research` | full |
| 5 | `ai-platform-strategy` | `thakicloud/ai-platform-strategy` | `/Users/hanhyojung/work/thakicloud/ai-platform-strategy` | `/Users/hanhyojung/thaki/ai-platform-strategy` | full |

**Path resolution**: Each project has two possible paths (회사/집). At runtime, try `Path (회사)` first, then `Path (집)`. Use the first path that exists as a directory. If neither exists, skip the project with a warning.

## Mode Definitions

- **full**: `commit → push → issue → PR → merge` (standard release-ship pipeline)
- **tmp-only**: `commit → push → issue → report` (works exclusively on `tmp` branch, no PRs or cross-branch merges)

## Slack Configuration

| Key | Value |
|-----|-------|
| Channel | `#효정-할일` |
| Channel ID | `C0AA8NT4T8T` |
| Post type | Consolidated EOD summary |

## Managing Projects

### Adding a new project

1. Add a row to the Project Table above
2. Ensure the project directory exists and is a git repo
3. Set `Mode` to `full` or `tmp-only` based on the repo's branching strategy
4. Run `/eod-ship --targets <alias> --dry-run` to verify

### Removing a project

1. Remove the row from the Project Table
2. The project is no longer processed during `/eod-ship`
