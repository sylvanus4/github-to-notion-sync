#!/usr/bin/env node
'use strict';

/**
 * sessionStart hook: Inject contextual hints at session start.
 *
 * - Reminds about uncommitted changes
 * - Shows current branch
 * - Reminds about project skills
 */

const { execSync } = require('child_process');
const { getProjectRoot } = require('./lib/utils');
const { isHookEnabled } = require('./lib/hook-flags');

function run(cmd, cwd) {
  try {
    return execSync(cmd, { cwd, encoding: 'utf8', timeout: 5000 }).trim();
  } catch { return ''; }
}

(function main() {
  if (!isHookEnabled('session:start:context', ['standard', 'strict'])) return;

  const root = getProjectRoot();
  const hints = [];

  const branch = run('git rev-parse --abbrev-ref HEAD', root);
  if (branch) hints.push(`Branch: ${branch}`);

  const status = run('git status --porcelain', root);
  if (status) {
    const lines = status.split('\n').filter(Boolean);
    hints.push(`Uncommitted changes: ${lines.length} file(s)`);
  }

  const unpushed = run('git log @{u}..HEAD --oneline 2>/dev/null', root);
  if (unpushed) {
    const commits = unpushed.split('\n').filter(Boolean);
    hints.push(`Unpushed commits: ${commits.length}`);
  }

  // CRG graph status
  const fs = require('fs');
  const graphDb = require('path').join(root, '.code-review-graph', 'graph.db');
  if (fs.existsSync(graphDb)) {
    const stats = run('code-review-graph status 2>/dev/null', root);
    if (stats) hints.push(`CRG graph: ${stats.split('\n')[0]}`);
    hints.push('Tip: Prefer CRG MCP tools over manual file scanning for code reviews');
  } else {
    hints.push('CRG graph not built yet — run `code-review-graph build` to enable graph-powered reviews');
  }

  if (hints.length) {
    console.error('[Session Start] Context:');
    hints.forEach(h => console.error(`  - ${h}`));
  }
})();
