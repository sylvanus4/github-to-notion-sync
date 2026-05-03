---
name: game-studio-qa-plan
description: >-
  Generate a comprehensive test matrix for game QA covering solvability, UI,
  sharing, persistence, and cross-browser. Use when the user asks to 'create
  QA plan', 'test matrix', 'game-qa-plan', 'game testing plan', '게임 QA 계획',
  '게임 테스트 계획', '테스트 매트릭스'. Do NOT use for balance verification (use
  game-studio-balance-check). Do NOT use for simulated playtesting (use
  game-studio-playtest-report). Do NOT use for dev story decomposition (use
  game-studio-dev-story).
---

# Game QA Plan — Test Matrix Generator

Generate a comprehensive test matrix covering puzzle solvability, UI interactions, sharing features, data persistence, and cross-browser compatibility. Produces test cases with expected results and severity classifications.

Use when the user asks to "create QA plan", "test matrix", "game-qa-plan", "game testing plan", "게임 QA 계획", or wants structured quality assurance planning for a game. Do NOT use for balance verification (use balance-check) or simulated playtesting (use playtest-report).

## Test Categories

### 1. Puzzle Solvability (Critical)
- Every generated puzzle has exactly one solution
- Minimum clue count is sufficient to identify the innocent suspect
- No puzzle requires guessing (always deducible)
- Clue text is unambiguous and non-contradictory
- Edge case: all clues revealed still points to one answer

### 2. Game State Machine (Critical)
- State transitions: idle → playing → solved/failed
- Cannot reveal clues after game is solved
- Cannot mark suspects after game is solved
- Game resets correctly for a new day
- Back/forward navigation doesn't break state

### 3. Daily Puzzle System (High)
- Same seed produces same puzzle for all users on the same day
- Puzzle changes at UTC midnight
- Previous day's puzzle is no longer playable (or moves to archive)
- Timezone edge cases: user crosses midnight during play

### 4. UI Interactions (High)
- Suspect grid: tap to mark/unmark each suspect
- Clue panel: reveal clues sequentially (no skip)
- Deduction board: visual state matches game state
- Share card: generates correct emoji grid
- Stats modal: displays accurate statistics
- Responsive: playable on 320px-1920px viewport widths

### 5. Data Persistence (Medium)
- Game progress survives page refresh
- Stats persist across sessions
- Streak counter increments correctly
- localStorage corruption doesn't crash the app
- First-time user sees tutorial/onboarding state

### 6. Sharing (Medium)
- Share text copies to clipboard
- Emoji grid accurately represents the player's solve path
- No spoilers in shared content
- Share works on mobile browsers

### 7. Accessibility (Medium)
- Keyboard navigation through all interactive elements
- Screen reader announces game state changes
- Color is not the only indicator (shape/icon backup)
- Focus management during modals
- Reduced motion preference respected

### 8. Performance (Low)
- Initial load < 2 seconds on 3G
- No layout shifts after content loads
- Smooth animations at 60fps
- Bundle size < 200KB gzipped

## Workflow

### Step 1: Inventory Features
List all features from the GDD and dev stories.

### Step 2: Generate Test Cases
For each feature, write test cases with:
- **ID** (e.g., `PUZZLE-001`)
- **Category** and **severity** (Critical/High/Medium/Low)
- **Precondition**
- **Steps**
- **Expected Result**
- **Edge Cases**

### Step 3: Create Test Matrix
Produce a summary table:
| ID | Category | Severity | Description | Status |

### Step 4: Define Automation Candidates
Flag test cases suitable for automated testing vs. manual-only.

### Step 5: Regression Checklist
Create a minimal regression checklist for pre-release validation.

## Output
A structured markdown document with:
1. Test matrix summary table
2. Detailed test cases per category
3. Automation recommendation list
4. Regression checklist
