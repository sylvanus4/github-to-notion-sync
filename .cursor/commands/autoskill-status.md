## AutoSkill Status

Show skill evolution statistics: skills created, merged, discarded, version history, and pipeline health metrics.

### Usage

```bash
/autoskill-status                    # show summary statistics
/autoskill-status --detail           # show full version history
/autoskill-status --skill <name>     # show evolution history for a specific skill
```

### What it does

1. Reads evolution state from `.cursor/hooks/state/autoskill-evolution.json`
2. Displays summary statistics:
   - Total evolution runs
   - Skills created, merged, discarded
   - Last processed timestamp
   - Extraction rate and acceptance rate
3. With `--detail`: shows full version history for all evolved skills
4. With `--skill`: shows evolution timeline for a specific skill

### Output Format

```
📊 AutoSkill Evolution Status
═══════════════════════════════
Last Run:        2026-03-14 10:00
Total Runs:      42
Processed:       156 transcripts

Skills Created:  12
Skills Merged:   28 (avg version: v0.1.4)
Skills Discarded: 15

Extraction Rate: 0.32 (candidates/transcripts)
Acceptance Rate: 0.73 (accepted/candidates)
Merge Ratio:     0.70 (merged/accepted)
```

### Skill

This command reads `.cursor/hooks/state/autoskill-evolution.json` directly. No dedicated skill file needed — the data is self-explanatory.
