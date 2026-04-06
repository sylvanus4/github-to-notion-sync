---
name: brain-full-crew
description: >-
  Install and operate the My-Brain-Is-Full-Crew (8 AI agents + 13 skills) for
  Obsidian vault management — dispatcher-driven orchestration covering knowledge
  capture, inbox triage, email/calendar integration, vault maintenance,
  transcription, and custom agent creation via PARA+Zettelkasten structure.
  Use when the user asks to "install brain crew", "set up Obsidian agents",
  "brain full crew", "vault crew setup", "Obsidian AI agents", "my brain is full",
  "brain-full-crew", "옵시디언 크루 설치", "볼트 에이전트 설치", "옵시디언 AI 팀",
  "브레인 크루", or wants a multi-agent Obsidian vault management system.
  Do NOT use for individual Obsidian CLI operations (use obsidian-files, obsidian-search, etc.).
  Do NOT use for Obsidian-KB bridge without crew context (use obsidian-kb-bridge).
  Do NOT use for general note-taking without Obsidian agent orchestration.
tags:
  - obsidian
  - multi-agent
  - vault-management
  - PARA
  - zettelkasten
  - dispatcher
version: 1.0.0
---

# My Brain Is Full — Crew

Multi-agent Obsidian vault management system: 8 specialized AI agents + 13 skills orchestrated by a dispatcher for complete knowledge lifecycle management.

**Source**: https://github.com/gnekt/My-Brain-Is-Full-Crew

## Prerequisites

- [Claude Code](https://claude.ai/code) with Claude Pro, Max, or Team subscription
- [Obsidian](https://obsidian.md) installed with a vault created
- Git CLI
- (Optional) Google Workspace CLI (`gws`) for email/calendar — see `references/gws-setup.md`
- (Optional) Hey CLI for Hey.com email accounts

## Installation

### Step 1: Clone into Obsidian vault

```bash
cd /path/to/your-obsidian-vault
git clone https://github.com/gnekt/My-Brain-Is-Full-Crew.git
```

### Step 2: Run installer

```bash
cd My-Brain-Is-Full-Crew
bash scripts/launchme.sh
```

The installer copies agents and skills to `.claude/agents/` and `.claude/skills/` inside the vault.

### Step 3: Initialize

Open Claude Code **inside the vault folder** and say: **"Initialize my vault"**

The `/onboarding` skill guides through:
1. Profile setup (name, language, role)
2. Agent activation selection
3. Gmail/Calendar integration (optional)

After onboarding, the Architect creates the full PARA + Zettelkasten structure.

### Updating

```bash
cd /path/to/your-vault/My-Brain-Is-Full-Crew
git pull
bash scripts/updateme.sh
```

## Architecture

### Vault Structure (PARA + Zettelkasten)

```
00-Inbox/          Capture everything here first
01-Projects/       Active projects with deadlines
02-Areas/          Ongoing responsibilities
03-Resources/      Reference material, guides, how-tos
04-Archive/        Completed or historical content
05-People/         Personal CRM
06-Meetings/       Timestamped meeting notes
07-Daily/          Daily notes and journals
MOC/               Maps of Content (thematic indexes)
Templates/         Obsidian note templates
Meta/              Vault config, agent logs, health reports
```

### Dispatcher Routing

```
User message → Dispatcher checks skills first → Skill match? → Invoke skill
                                               → No match?   → Invoke agent → Vault updated
```

Skills handle complex multi-step conversational flows. Agents handle quick single-shot operations. Skills are checked first.

### Agent Chaining

Agents coordinate through `### Suggested next agent` sections in their output. The dispatcher reads this and automatically chains the next agent:

- `/transcribe` finds new project → chains **Architect** to create folder structure
- `/email-triage` finds deadline → chains **Sorter** to file notes
- **Connector** finds orphan notes → chains **Librarian** to investigate
- **Sorter** finds notes for new area → chains **Architect** to build it

## The 8 Agents

| # | Agent | Role | Capability |
|---|-------|------|------------|
| 1 | **Architect** | Vault Structure & Setup | Designs vault, runs onboarding, sets rules |
| 2 | **Scribe** | Text Capture | Transforms messy brain dumps into clean notes |
| 3 | **Sorter** | Inbox Triage | Routes every note to its correct location |
| 4 | **Seeker** | Search & Intelligence | Finds anything, synthesizes answers with citations |
| 5 | **Connector** | Knowledge Graph | Discovers hidden links between notes |
| 6 | **Librarian** | Vault Maintenance | Health checks, deduplication, broken link repair |
| 7 | **Transcriber** | Audio & Meetings | Turns recordings into structured meeting notes |
| 8 | **Postman** | Email & Calendar | Bridges Gmail/Hey.com and Google Calendar with vault |

## The 13 Skills

| Skill | What it does | Source Agent |
|-------|-------------|--------------|
| `/onboarding` | Full vault setup conversation | Architect |
| `/create-agent` | Design a custom agent step by step | Architect |
| `/manage-agent` | Edit, remove, or list custom agents | Architect |
| `/defrag` | Weekly vault defragmentation (5 phases) | Architect |
| `/email-triage` | Scan and prioritize unread emails | Postman |
| `/meeting-prep` | Comprehensive meeting brief | Postman |
| `/weekly-agenda` | Day-by-day week overview | Postman |
| `/deadline-radar` | Unified deadline timeline | Postman |
| `/transcribe` | Process recordings into structured notes | Transcriber |
| `/vault-audit` | Full 7-phase vault audit | Librarian |
| `/deep-clean` | Extended vault cleanup | Librarian |
| `/tag-garden` | Tag analysis and cleanup | Librarian |
| `/inbox-triage` | Process and route inbox notes | Sorter |

## Custom Agent Creation

Say **"create a new agent"** and the Architect walks through a conversation to design one. No code required. Custom agents:
- Coordinate with the core crew
- Get discovered automatically by Claude Code
- Respond in the user's language

## Modes of Operation

### Install Mode
When user asks to install or set up the crew:
1. Verify Obsidian vault path
2. Clone the repository
3. Run `launchme.sh`
4. Guide through onboarding

### Usage Guide Mode
When user asks how to use the crew:
1. Explain dispatcher routing (skills first, then agents)
2. Show example interactions per agent/skill
3. Explain agent chaining behavior

### Troubleshooting Mode
When user reports issues:
1. Check `.claude/agents/` and `.claude/skills/` exist in vault
2. Verify Claude Code is opened inside the vault directory
3. Check `gws` installation for email/calendar features
4. Run `bash scripts/updateme.sh` if agents seem outdated

## Multi-Language Support

The crew responds in whatever language the user writes in. No configuration needed.

```
"Salva questa nota veloce..."          → Italian
"Vérifie mon email..."                 → French
"Was habe ich diese Woche geplant?"    → German
"Check my inbox"                       → English
```

## Recommended Obsidian Plugins

**Essential:** Templater, Dataview, Calendar, Tasks

**Recommended:** QuickAdd, Folder Notes, Tag Wrangler, Natural Language Dates, Periodic Notes, Omnisearch, Linter

## Integration with Existing Obsidian Skills

This skill complements the existing `obsidian-*` skill family:
- Use `obsidian-setup` for CLI installation → then `brain-full-crew` for agent crew setup
- Use `obsidian-files` for direct file CRUD → crew handles this via conversation
- Use `obsidian-search` for CLI vault search → Seeker agent provides semantic search
- Use `obsidian-kb-bridge` for KB pipeline integration → separate from crew operations

## Conservative Defaults

Agents never delete — they always archive. They ask before making big decisions. This is by design for overwhelmed users who need a safety net, not another source of anxiety.
