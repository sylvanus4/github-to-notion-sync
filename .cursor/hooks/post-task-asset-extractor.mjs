#!/usr/bin/env node

/**
 * Post-Task Asset Extractor Hook
 *
 * Fires on every postToolUse event. Tracks tool call count per session
 * (scoped by project directory). When the count crosses the configured
 * threshold (default 8), injects additional_context that nudges the
 * agent to run the Mandatory Self-Check Block from
 * hermes-inline-learning.mdc.
 *
 * Session boundary detection: a gap of >30 minutes between consecutive
 * tool calls resets the counter for a fresh session.
 */

import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { createHash } from 'node:crypto';

const THRESHOLD = 8;
const SESSION_GAP_MS = 30 * 60 * 1000;

const projectHash = createHash('md5')
  .update(process.cwd())
  .digest('hex')
  .slice(0, 8);
const STATE_FILE = join(tmpdir(), `cursor-asset-extractor-${projectHash}.json`);

function loadState() {
  try {
    if (existsSync(STATE_FILE)) {
      return JSON.parse(readFileSync(STATE_FILE, 'utf-8'));
    }
  } catch {
    /* corrupt or missing — start fresh */
  }
  return { count: 0, nudged: false, lastToolCall: 0, hasErrors: false };
}

function saveState(state) {
  writeFileSync(STATE_FILE, JSON.stringify(state));
}

let input = '';
try {
  input = readFileSync('/dev/stdin', 'utf-8');
} catch {
  process.stdout.write('{}');
  process.exit(0);
}

let data = {};
try {
  data = JSON.parse(input);
} catch {
  process.stdout.write('{}');
  process.exit(0);
}

const state = loadState();
const now = Date.now();

if (now - state.lastToolCall > SESSION_GAP_MS) {
  state.count = 0;
  state.nudged = false;
  state.hasErrors = false;
}

state.count++;
state.lastToolCall = now;

const output = data.toolOutput ?? data.tool_output ?? '';
const outputStr = typeof output === 'string' ? output : JSON.stringify(output);
if (/\b(error|Error|ERROR|failed|Failed|FAILED|exception|Exception)\b/.test(outputStr)) {
  state.hasErrors = true;
}

if (!state.nudged && state.count >= THRESHOLD) {
  state.nudged = true;
  saveState(state);

  const errorNote = state.hasErrors ? ', error recovery detected' : '';
  const nudge = [
    `[Asset Extraction Nudge] This session has reached ${state.count} tool calls${errorNote}.`,
    'Before marking the task as done, evaluate per hermes-inline-learning.mdc:',
    `1. Non-trivial? (${state.count} tool calls${errorNote})`,
    '2. Reusable pattern not captured by an existing skill?',
    '3. Passes 3-gate filter? (Non-Googleable, Codebase-specific, Hard-won)',
    'If YES to all 3 → invoke autoskill-extractor.',
    'If YES to 1-2 only → capture as memory entry.',
  ].join(' ');

  process.stdout.write(JSON.stringify({ additional_context: nudge }));
} else {
  saveState(state);
  process.stdout.write('{}');
}
