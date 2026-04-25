#!/usr/bin/env node

/**
 * Post-Task Asset Extractor — postToolUse session-aware nudge hook.
 *
 * Runs after every tool use. Maintains lightweight session state in a
 * temp file, tracking tool call volume, unique tool diversity, and
 * error-like patterns. When thresholds are crossed (informed by
 * hermes-inline-learning.mdc and post-task-reflection.mdc), injects
 * additional_context reminding the agent to evaluate the session for
 * reusable asset extraction (skills, memory entries, patterns).
 *
 * Thresholds:
 *   - 8+ tool calls → first nudge (skill extraction evaluation)
 *   - 3+ unique tool types → multi-step workflow detected
 *   - 20+ tool calls → second nudge (comprehensive reflection)
 *
 * Non-blocking: only surfaces reminders via additional_context.
 * Resets state after 2 hours of inactivity (session boundary heuristic).
 */

import { readFileSync, writeFileSync, existsSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";

const STATE_FILE = join(tmpdir(), "cursor-asset-extractor-state.json");
const SESSION_TTL_MS = 2 * 60 * 60 * 1000; // 2 hours
const NUDGE_THRESHOLD_1 = 8;
const NUDGE_THRESHOLD_2 = 20;
const DIVERSITY_THRESHOLD = 3;
const COOLDOWN_CALLS = 10;

function collectInput() {
  return new Promise((res) => {
    let buf = "";
    process.stdin.setEncoding("utf8");
    process.stdin.on("data", (chunk) => (buf += chunk));
    process.stdin.on("end", () => res(buf));
  });
}

function freshState() {
  return {
    toolCallCount: 0,
    uniqueTools: [],
    errorPatternCount: 0,
    lastNudgeAt: 0,
    nudgeCount: 0,
    startedAt: Date.now(),
    lastActivityAt: Date.now(),
  };
}

function loadState() {
  try {
    if (!existsSync(STATE_FILE)) return freshState();
    const data = JSON.parse(readFileSync(STATE_FILE, "utf8"));
    if (Date.now() - data.lastActivityAt > SESSION_TTL_MS) return freshState();
    return data;
  } catch {
    return freshState();
  }
}

function saveState(state) {
  try {
    state.lastActivityAt = Date.now();
    writeFileSync(STATE_FILE, JSON.stringify(state), "utf8");
  } catch {
    // silently fail — nudging is best-effort
  }
}

function detectErrorPattern(input) {
  const resultStr = JSON.stringify(input).toLowerCase();
  const patterns = ["error:", "failed", "exception", "traceback", "enoent", "permission denied"];
  return patterns.some((p) => resultStr.includes(p));
}

function extractToolName(input) {
  return input.tool_name || input.toolName || input.name || "unknown";
}

function buildNudge(state) {
  const parts = ["**📋 Post-Task Asset Extractor** — session checkpoint:"];

  parts.push(
    `Session stats: ${state.toolCallCount} tool calls, ${state.uniqueTools.length} unique tools, ${state.errorPatternCount} error-like patterns.`
  );

  if (state.toolCallCount >= NUDGE_THRESHOLD_2) {
    parts.push(
      "",
      "🔴 **Comprehensive reflection recommended.** This session has substantial work.",
      "Before wrapping up, consider the 5-step post-task reflection protocol:",
      "1. **Outcome Assessment** — Did the task succeed? Any unexpected findings?",
      "2. **Pattern Detection** — Was this a multi-step workflow worth reusing?",
      "3. **Memory Update** — Any facts, preferences, or decisions to persist?",
      "4. **Skill Candidate Evaluation** — Apply the 3-gate filter: Not Googleable? Codebase-specific? Required real debugging effort?",
      "5. **Lesson Capture** — Record in `tasks/lessons.md` if applicable.",
      "",
      "Skills to consider: `post-task-skill-evaluator`, `omc-learner`, `autoskill-extractor`.",
      "Ref: `.cursor/rules/post-task-reflection.mdc`, `.cursor/rules/hermes-inline-learning.mdc`"
    );
  } else if (state.toolCallCount >= NUDGE_THRESHOLD_1) {
    parts.push(
      "",
      "🟡 **Asset extraction checkpoint reached** (8+ tool calls).",
      "When this task completes, evaluate whether the workflow is worth capturing:",
      "- Reusable multi-step pattern? → Consider `cursor-skill-factory` or `omc-learner`",
      "- New fact or decision? → Update `MEMORY.md` or invoke `memkraft-ingest`",
      "- Hard-won debugging insight? → Capture as instinct via `ecc-continuous-learning`",
      "",
      "Ref: `.cursor/rules/hermes-inline-learning.mdc`"
    );
  }

  if (state.errorPatternCount >= 2) {
    parts.push(
      "",
      `⚡ Error recovery detected (${state.errorPatternCount} error-like patterns). Error recovery workflows are high-value skill candidates.`
    );
  }

  return parts.join("\n");
}

function shouldNudge(state) {
  if (state.toolCallCount < NUDGE_THRESHOLD_1) return false;
  if (state.uniqueTools.length < DIVERSITY_THRESHOLD) return false;
  if (state.nudgeCount > 0 && state.toolCallCount - state.lastNudgeAt < COOLDOWN_CALLS) return false;

  if (state.nudgeCount === 0 && state.toolCallCount >= NUDGE_THRESHOLD_1) return true;
  if (state.nudgeCount === 1 && state.toolCallCount >= NUDGE_THRESHOLD_2) return true;
  if (state.errorPatternCount >= 2 && state.nudgeCount < 2) return true;

  return false;
}

async function main() {
  try {
    const raw = await collectInput();
    if (!raw.trim()) process.exit(0);

    let input;
    try {
      input = JSON.parse(raw);
    } catch {
      process.exit(0);
    }

    const state = loadState();
    state.toolCallCount++;

    const toolName = extractToolName(input);
    if (!state.uniqueTools.includes(toolName)) {
      state.uniqueTools.push(toolName);
    }

    if (detectErrorPattern(input)) {
      state.errorPatternCount++;
    }

    if (shouldNudge(state)) {
      const msg = buildNudge(state);
      state.lastNudgeAt = state.toolCallCount;
      state.nudgeCount++;
      saveState(state);
      console.log(JSON.stringify({ additional_context: msg }));
    } else {
      saveState(state);
    }
  } catch {
    process.exit(0);
  }
}

main();
