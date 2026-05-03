---
name: game-studio-playtest-report
description: >-
  Simulate playtesting with 4 Bartle archetypes (Achiever, Explorer,
  Socializer, Casual) and produce a consolidated feedback report. Use when the
  user asks to 'playtest', 'simulate players', 'game-playtest-report', 'player
  feedback', '게임 플레이테스트', '플레이테스트 시뮬레이션', '플레이어 피드백'. Do NOT use for QA test
  cases (use game-studio-qa-plan). Do NOT use for balance verification (use
  game-studio-balance-check). Do NOT use for GDD authoring (use
  game-studio-design-system).
---

# Game Playtest Report — Simulated Player Feedback

Simulate playtesting by walking through the game as 4 distinct player archetypes (Achiever, Explorer, Socializer, Casual). Each archetype plays through a sample puzzle and reports friction points, confusion, delight moments, and suggestions. Produces a consolidated feedback report.

Use when the user asks to "playtest", "simulate players", "game-playtest-report", "player feedback", "게임 플레이테스트", or wants simulated user feedback before real playtesting. Do NOT use for QA test cases (use qa-plan) or balance verification (use balance-check).

## Player Archetypes (Bartle Framework)

### Achiever
- **Goal:** Solve in minimum clues, maintain streak, maximize score
- **Focus:** Optimization, score comparison, efficiency
- **Tests:** Scoring fairness, difficulty ceiling, leaderboard hooks
- **Friction signals:** "Score doesn't reflect my skill", "too easy/hard", "streak lost unfairly"

### Explorer
- **Goal:** Understand the puzzle system, find patterns, try unusual strategies
- **Focus:** Mechanics depth, edge cases, hidden interactions
- **Tests:** Rule clarity, edge case handling, puzzle variety
- **Friction signals:** "Clue was misleading", "I found a loophole", "puzzles feel samey"

### Socializer
- **Goal:** Share results, compare with friends, discuss strategy
- **Focus:** Sharing UX, spoiler-free design, community features
- **Tests:** Share card quality, no-spoiler guarantee, social hooks
- **Friction signals:** "Share card reveals too much", "can't find share button", "no way to discuss"

### Casual
- **Goal:** Quick daily ritual, low stress, satisfying completion
- **Focus:** Onboarding clarity, session length, forgiveness
- **Tests:** Tutorial quality, UI intuitiveness, time-to-first-success
- **Friction signals:** "Don't understand what to do", "took too long", "felt punished for mistakes"

## Workflow

### Step 1: Select Sample Puzzles
Choose 3 puzzles: one easy, one medium, one hard.

### Step 2: Archetype Walkthroughs
For each archetype, simulate a play session:
1. First impression (loading, onboarding)
2. Puzzle interaction (clue reveals, suspect marking, deduction)
3. Resolution (solve or fail, share, stats view)
4. Repeat engagement (would they come back tomorrow?)

Document observations in first-person voice of the archetype.

### Step 3: Friction Log
Create a consolidated friction log:
| # | Archetype | Phase | Observation | Severity | Suggestion |

### Step 4: Delight Moments
List moments that would create positive emotional responses.

### Step 5: Retention Assessment
For each archetype, predict:
- Day 1 return probability
- Day 7 return probability
- Primary retention driver
- Primary churn risk

### Step 6: Prioritized Recommendations
Rank all suggestions by impact × effort, grouped into:
- **Must-fix before launch** (breaks core loop)
- **Should-fix** (hurts retention)
- **Nice-to-have** (polishes experience)

## Output
A structured markdown playtest report with:
1. Per-archetype walkthrough narratives
2. Consolidated friction log table
3. Delight moments list
4. Retention predictions per archetype
5. Prioritized recommendation list
