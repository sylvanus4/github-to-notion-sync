#!/usr/bin/env node
'use strict';

/**
 * sessionEnd hook: End-of-session cleanup, KB ingest flag, and reminders.
 *
 * - Warns about dirty working directory
 * - Detects substantial session work (commits, file edits) and flags for KB ingest
 * - Suggests memory update if substantial session
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');
const { getProjectRoot } = require('./lib/utils');
const { isHookEnabled } = require('./lib/hook-flags');

function run(cmd, cwd) {
  try {
    return execSync(cmd, { cwd, encoding: 'utf8', timeout: 5000 }).trim();
  } catch { return ''; }
}

function detectSessionWork(root) {
  const today = new Date().toISOString().slice(0, 10);

  const todayCommits = run(
    `git log --since="6 hours ago" --oneline --no-merges 2>/dev/null`,
    root
  );
  const commitCount = todayCommits ? todayCommits.split('\n').filter(Boolean).length : 0;

  const changedFiles = run('git diff --name-only HEAD~5 2>/dev/null', root);
  const fileCount = changedFiles ? changedFiles.split('\n').filter(Boolean).length : 0;

  const outputDirs = [
    `outputs/today/${today}`,
    `outputs/knowledge-daily-aggregator/${today}`,
    `outputs/daily-pm/${today}`,
    `outputs/role-analysis`,
    `outputs/twitter`,
  ];
  let outputCount = 0;
  for (const dir of outputDirs) {
    const fullPath = path.join(root, dir);
    try {
      const files = fs.readdirSync(fullPath);
      outputCount += files.length;
    } catch { /* dir doesn't exist */ }
  }

  return { commitCount, fileCount, outputCount, isSubstantial: commitCount >= 3 || fileCount >= 5 || outputCount >= 3 };
}

function writeKbIngestFlag(root) {
  const today = new Date().toISOString().slice(0, 10);
  const flagDir = path.join(root, 'outputs', 'kb-ingest-flags');
  try {
    fs.mkdirSync(flagDir, { recursive: true });
    const flagFile = path.join(flagDir, `${today}-session.json`);
    const flag = {
      date: today,
      timestamp: new Date().toISOString(),
      source: 'session-end-hook',
      status: 'pending',
    };
    fs.writeFileSync(flagFile, JSON.stringify(flag, null, 2));
    return true;
  } catch { return false; }
}

function runKbHealthCheck(root) {
  const healthScript = path.join(root, 'scripts', 'kb_health_check.py');
  if (!fs.existsSync(healthScript)) return null;

  try {
    const output = execSync(
      `python3 "${healthScript}" --json --days 3`,
      { cwd: root, encoding: 'utf8', timeout: 15000, stdio: ['pipe', 'pipe', 'pipe'] }
    ).trim();
    return JSON.parse(output);
  } catch (e) {
    if (e.stdout) {
      try { return JSON.parse(e.stdout.toString().trim()); } catch { /* fall through */ }
    }
    return null;
  }
}

function autoFixKbGaps(root) {
  const localRouter = path.join(root, 'scripts', 'kb_daily_router.py');
  const results = [];

  if (fs.existsSync(localRouter)) {
    const out = run(`python3 "${localRouter}" 2>&1`, root);
    results.push({ router: 'kb_daily_router', output: (out || '').slice(-200) });
  }

  const researchCandidates = [
    path.join(process.env.HOME || '', 'thaki', 'research'),
    path.join(process.env.HOME || '', 'work', 'thakicloud', 'research'),
  ];
  for (const rr of researchCandidates) {
    const intelRouter = path.join(rr, 'scripts', 'intelligence', 'kb_intel_router.py');
    if (fs.existsSync(intelRouter)) {
      const out = run(`python3 "${intelRouter}" 2>&1`, rr);
      results.push({ router: 'kb_intel_router', output: (out || '').slice(-200) });
      break;
    }
  }

  return results;
}

function writeKbHealthState(root, report, fixResults) {
  const stateDir = path.join(root, '.cursor', 'hooks', 'state');
  try {
    fs.mkdirSync(stateDir, { recursive: true });
    const statePath = path.join(stateDir, 'kb-health-last.json');
    const state = {
      timestamp: new Date().toISOString(),
      gaps_found: 0,
      stale_wikis: 0,
      auto_fixed: fixResults.length > 0,
    };
    if (report) {
      for (const section of ['local', 'research']) {
        const findings = report[section]?.findings || [];
        for (const f of findings) {
          state.gaps_found += f.gap || 0;
          if (f.stale_wiki) state.stale_wikis++;
        }
      }
    }
    fs.writeFileSync(statePath, JSON.stringify(state, null, 2));
  } catch { /* best effort */ }
}

(function main() {
  if (!isHookEnabled('session:end:cleanup', ['standard', 'strict'])) return;

  const root = getProjectRoot();
  const reminders = [];

  const status = run('git status --porcelain', root);
  if (status) {
    const lines = status.split('\n').filter(Boolean);
    reminders.push(`${lines.length} uncommitted file(s) — consider running /domain-commit or /eod-ship`);
  }

  const unpushed = run('git log @{u}..HEAD --oneline 2>/dev/null', root);
  if (unpushed) {
    const commits = unpushed.split('\n').filter(Boolean);
    if (commits.length >= 3) {
      reminders.push(`${commits.length} unpushed commits — consider pushing before ending`);
    }
  }

  const work = detectSessionWork(root);
  if (work.isSubstantial) {
    const flagged = writeKbIngestFlag(root);
    reminders.push(
      `Substantial session detected (${work.commitCount} commits, ${work.fileCount} files, ${work.outputCount} outputs)` +
      (flagged
        ? ' — KB ingest flag written to outputs/kb-ingest-flags/. Run /daily-pm or knowledge-daily-aggregator to process.'
        : ' — consider running knowledge-daily-aggregator to capture session knowledge.')
    );
  }

  const healthReport = runKbHealthCheck(root);
  let fixResults = [];
  if (healthReport) {
    let totalGaps = 0;
    let staleTopics = 0;
    for (const section of ['local', 'research']) {
      const findings = healthReport[section]?.findings || [];
      for (const f of findings) {
        totalGaps += f.gap || 0;
        if (f.stale_wiki) staleTopics++;
      }
    }

    if (totalGaps > 0 || staleTopics > 0) {
      fixResults = autoFixKbGaps(root);
      const fixSummary = fixResults.length > 0
        ? `auto-routed via ${fixResults.map(r => r.router).join(', ')}`
        : 'auto-fix unavailable';
      reminders.push(
        `KB health: ${totalGaps} unrouted output(s), ${staleTopics} stale wiki(s) — ${fixSummary}`
      );
    }

    writeKbHealthState(root, healthReport, fixResults);
  }

  if (reminders.length) {
    console.error('[Session End] Reminders:');
    reminders.forEach(r => console.error(`  - ${r}`));
  }
})();
