---
name: game-studio-start
description: >-
  Scaffold a new browser game project with React + Vite + TypeScript +
  Tailwind CSS + Zustand. Use when the user asks to 'start a new game',
  'scaffold game project', 'game-start', 'initialize game', '게임 프로젝트 생성', '게임
  시작', '새 게임 만들기'. Do NOT use for existing projects that already have a
  package.json and game structure. Do NOT use for ideation (use
  game-studio-brainstorm). Do NOT use for GDD authoring (use
  game-studio-design-system).
disable-model-invocation: true
---

# Game Start — Project Scaffolding

Scaffold a new browser game project with React + Vite + TypeScript + Tailwind CSS + Zustand. Creates the full directory structure, installs dependencies, and generates boilerplate files for the game engine and UI layers.

Use when the user asks to "start a new game", "scaffold game project", "game-start", "initialize game", "게임 프로젝트 생성", or wants to set up a fresh game project from scratch. Do NOT use for existing projects that already have a `package.json` and game structure.

## Workflow

### Step 1: Confirm Project Parameters
Ask the user for (or use defaults):
- **Project name** (default: `alibi-network`)
- **Game type** (default: `daily-puzzle`)
- **Grid size** (default: `3x3`)

### Step 2: Scaffold with Vite
```bash
npm create vite@latest <project-name> -- --template react-ts
cd <project-name>
npm install
```

### Step 3: Install Game Dependencies
```bash
npm install zustand lucide-react
npm install -D tailwindcss @tailwindcss/vite
```

### Step 4: Configure Tailwind
Update `vite.config.ts` to include the Tailwind plugin.
Create `src/index.css` with `@import "tailwindcss"`.

### Step 5: Create Directory Structure
```
src/
  components/
    Game/           # SuspectGrid, CluePanel, DeductionBoard, ShareCard, StatsModal
    Layout/         # Header, Footer
  hooks/            # useDaily, useGameState, useStats
  lib/              # puzzleEngine, clueGenerator, seedRandom, shareFormatter
  data/             # suspects, puzzleBank
  types/            # game.ts (TypeScript interfaces)
```

### Step 6: Generate Type Definitions
Create `src/types/game.ts` with the core interfaces:
- `Puzzle` (id, suspects, innocentIndex, clues, minCluesNeeded)
- `Suspect` (name, role, trait, gridPosition)
- `Clue` (text, type, eliminates)
- `GameState` (puzzle, markedSuspects, revealedClues, gameStatus, score)

### Step 7: Generate Boilerplate Files
Create minimal placeholder files for:
- `src/lib/seedRandom.ts` — mulberry32 PRNG stub
- `src/lib/puzzleEngine.ts` — puzzle generation stub
- `src/hooks/useGameState.ts` — Zustand store stub
- `src/App.tsx` — basic game layout shell

### Step 8: Verify Build
```bash
npm run dev
```
Confirm the dev server starts without errors.

## Output Checklist
- [ ] Vite project builds and serves
- [ ] Tailwind CSS processes utility classes
- [ ] Zustand store initializes
- [ ] Type definitions compile without errors
- [ ] Directory structure matches the architecture spec
