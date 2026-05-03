---
name: web-design-guidelines
description: Review UI code for Web Interface Guidelines compliance by fetching rules from Vercel's web-interface-guidelines repository. Use when asked to check a file against web interface best practices or validate HTML/CSS/accessibility standards. Do NOT use for heuristic UX evaluations or detailed accessibility audits (use ux-expert) or building new UIs (use frontend-design).
metadata:
  author: vercel
  version: "1.0.0"
  category: review
  argument-hint: file-or-pattern
---

# Web Interface Guidelines

Review files for compliance with Web Interface Guidelines.

## How It Works

1. Fetch the latest guidelines from the source URL below
2. Read the specified files (or prompt user for files/pattern)
3. Check against all rules in the fetched guidelines
4. Output findings in the terse `file:line` format

## Guidelines Source

Fetch fresh guidelines before each review:

```
https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md
```

Use WebFetch to retrieve the latest rules. The fetched content contains all the rules and output format instructions.

## Usage

When a user provides a file or pattern argument:
1. Fetch guidelines from the source URL above
2. Read the specified files
3. Apply all rules from the fetched guidelines
4. Output findings using the format specified in the guidelines

If no files specified, ask the user which files to review.

## Examples

### Example 1: Review a component file
User says: "Check my Button component against web guidelines"
Actions:
1. Fetch latest guidelines from Vercel's repository
2. Read the specified component file
3. Apply all rules and output findings in `file:line` format
Result: Compliance report with specific violations and line references

### Example 2: Audit multiple files
User says: "Review all components in src/components/ui/"
Actions:
1. Fetch guidelines
2. Read all files matching the pattern
3. Check each file against all rules
Result: Aggregated findings across all reviewed files

## Troubleshooting

### Guidelines fetch fails
Cause: Network issue or GitHub rate limiting
Solution: Retry the WebFetch call; if persistent, use a cached copy of the guidelines

### No files specified
Cause: User didn't provide a file path or pattern
Solution: Ask the user which files or directories to review
