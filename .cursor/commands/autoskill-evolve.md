## AutoSkill Evolve

Run the full skill evolution pipeline: extract reusable skill candidates from agent transcripts, judge each against existing skills, and apply add/merge/discard decisions.

### Usage

```bash
/autoskill-evolve
/autoskill-evolve --scope recent      # default: 5 most recent unprocessed transcripts
/autoskill-evolve --scope all         # all unprocessed transcripts
/autoskill-evolve --scope session <uuid>  # specific session
/autoskill-evolve --dry-run           # preview without changes
/autoskill-evolve --auto-optimize     # run skill-optimizer on results
/autoskill-evolve --slack             # post summary to Slack
/autoskill-evolve --hint "coding conventions"  # guide extraction focus
```

### What it does

1. Selects transcripts based on scope (incremental watermark tracking)
2. Runs `autoskill-extractor` on each transcript (max 2 candidates per transcript)
3. Runs `autoskill-judge` on each candidate (add/merge/discard decision)
4. For `add`: creates new SKILL.md in `.cursor/skills/`
5. For `merge`: runs `autoskill-merger` to update existing skill with version bump
6. Generates evolution report in `outputs/autoskill-reports/`
7. Updates state in `.cursor/hooks/state/autoskill-evolution.json`

### Skill

Read and follow `.cursor/skills/autoskill-evolve/SKILL.md`
