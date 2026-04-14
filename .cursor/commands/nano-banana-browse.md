## Nano Banana Browse — Prompt Library Explorer

Browse, search, and discover prompts from the 7,600+ curated Nano Banana prompt library.

### Usage

```
# Browse all tiers
/nano-banana-browse

# Browse a specific tier
/nano-banana-browse photography

# Browse a subcategory
/nano-banana-browse creative/anime --limit 10

# Search by keyword
/nano-banana-browse search "sunset portrait"

# Random prompt
/nano-banana-browse random --tier design --count 3

# Show prompt details
/nano-banana-browse show --id 12445

# Library statistics
/nano-banana-browse stats
```

### Workflow

1. **Parse** — Extract subcommand (browse / search / random / stats / show) and arguments
2. **Build command** — Construct `uv run prompt_library.py` command with appropriate flags
3. **Execute** — Run the `prompt_library.py` script via Shell
4. **Present** — Display results formatted for the user

### Output

Prompt details including title, category, tags, and the full prompt text. For structured BananaX prompts, the 7-part YAML is auto-converted to natural language.

### Execution

Read and follow the `nano-banana` skill (`.cursor/skills/standalone/nano-banana/SKILL.md`).
