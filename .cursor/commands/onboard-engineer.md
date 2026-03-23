---
description: Generate complete new engineer onboarding package with environment setup, must-read docs, architecture overview, and mentor assignment
argument-hint: "[engineer-name] [team/role]"
---

# /onboard-engineer

## What This Command Does
Generates a comprehensive onboarding package for new engineers joining the Cloud Tech team, including environment setup checklist, essential documentation links, architecture overview, and mentor assignment.

## Required Input
- New engineer's name
- Team/role (optional)

## Execution Steps
1. Read the onboarding-accelerator skill for base template
2. Generate environment setup checklist tailored to ThakiCloud stack (K8s, GPU Operator, Keycloak, ArgoCD)
3. Compile must-read documentation list from docs/ directory
4. Generate architecture overview using visual-explainer
5. Create getting-started guide via docs-tutor-setup
6. Assign mentor from team roster (suggest based on tech area)
7. Create Notion onboarding tracker page
8. Post welcome message to #cloudtech-자동화 Slack channel

## Output
- Notion: Onboarding tracker page with checklist
- Slack: Welcome message with key links
- Google Drive: Compiled document package

## Skills Used
- onboarding-accelerator: Base onboarding template
- docs-tutor-setup: Study materials generation
- local-dev-runner: Environment setup instructions
- codebase-archaeologist: Code ownership overview
- visual-explainer: Architecture diagram
- md-to-notion: Notion page creation

## Example Usage
```
/onboard-engineer 김철수 SRE
```
