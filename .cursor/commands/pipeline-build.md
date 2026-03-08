## Pipeline Build

Build automated data pipelines using existing Python scripts, GitHub Actions, and cron schedules without writing new code.

### Usage

```
/pipeline-build                           # Interactive: describe what you want to automate
/pipeline-build github <description>      # Generate a GitHub Actions workflow
/pipeline-build makefile <description>    # Add a Makefile target
/pipeline-build script <description>      # Create a shell script pipeline
/pipeline-build command <description>     # Create a Cursor command pipeline
/pipeline-build list                      # List all existing pipelines
```

### Workflow

1. **Define requirements** — What triggers, which scripts, what outputs
2. **Choose format** — GitHub Actions, Makefile, shell script, or Cursor command
3. **Build** — Generate the pipeline definition
4. **Validate** — Dry run each stage, check dependencies and secrets
5. **Document** — Add to pipeline inventory

### Execution

Read and follow the `pipeline-builder` skill (`.cursor/skills/pipeline-builder/SKILL.md`) for templates, formats, and validation steps.

### Examples

Weekly data refresh workflow:
```
/pipeline-build github "refresh all stock data every Monday"
```

Local analysis Makefile target:
```
/pipeline-build makefile "run analysis and generate report"
```

Multi-stage shell script:
```
/pipeline-build script "download CSVs, import, sync, analyze"
```
