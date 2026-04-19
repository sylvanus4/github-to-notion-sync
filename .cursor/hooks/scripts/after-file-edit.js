#!/usr/bin/env node
'use strict';

/**
 * afterFileEdit hook: Auto-format and lint after file edits.
 *
 * - Python files: run `ruff format` + warn on print() outside tests
 * - TS/TSX/JS/JSX files: run Prettier + warn on console.log
 */

const { execFileSync } = require('child_process');
const path = require('path');
const { readStdin, readFile } = require('./lib/utils');
const { isHookEnabled } = require('./lib/hook-flags');

readStdin().then(raw => {
  try {
    const input = JSON.parse(raw);
    const filePath = input.path || input.file || '';
    if (!filePath) { process.stdout.write(raw); return; }

    if (isHookEnabled('post:edit:format', ['standard', 'strict'])) {
      if (/\.py$/.test(filePath)) {
        formatPython(filePath);
        warnPythonPrint(filePath);
      } else if (/\.(ts|tsx|js|jsx)$/.test(filePath)) {
        formatTypeScript(filePath);
        warnConsoleLog(filePath);
      }
    }

    if (/\.(py|go|ts|tsx|js|jsx)$/.test(filePath)) {
      try {
        execFileSync('code-review-graph', ['update', filePath], {
          stdio: ['pipe', 'pipe', 'pipe'],
          timeout: 5000,
        });
      } catch { /* CRG not installed or failed — non-blocking */ }
    }
  } catch {
    // pass through on error
  }
  process.stdout.write(raw);
}).catch(() => process.exit(0));

function formatPython(filePath) {
  try {
    execFileSync('ruff', ['format', filePath], {
      stdio: ['pipe', 'pipe', 'pipe'],
      timeout: 10000,
    });
  } catch {
    // ruff not installed or failed — non-blocking
  }
}

function formatTypeScript(filePath) {
  const projectRoot = findProjectRoot(path.dirname(path.resolve(filePath)));
  const localPrettier = path.join(projectRoot, 'node_modules', '.bin', 'prettier');
  const fs = require('fs');

  if (fs.existsSync(localPrettier)) {
    try {
      execFileSync(localPrettier, ['--write', path.resolve(filePath)], {
        cwd: projectRoot,
        stdio: ['pipe', 'pipe', 'pipe'],
        timeout: 10000,
      });
    } catch { /* non-blocking */ }
  }
}

function warnConsoleLog(filePath) {
  const content = readFile(filePath);
  if (!content) return;
  const lines = content.split('\n');
  const matches = [];
  lines.forEach((line, idx) => {
    if (/console\.log/.test(line) && !/\/\//.test(line.split('console.log')[0])) {
      matches.push(`  L${idx + 1}: ${line.trim()}`);
    }
  });
  if (matches.length > 0) {
    console.error(`[Hook] console.log found in ${path.basename(filePath)}:`);
    matches.slice(0, 5).forEach(m => console.error(m));
  }
}

function warnPythonPrint(filePath) {
  if (/test[s_]?[/\\]/.test(filePath) || /test_/.test(path.basename(filePath))) return;
  const content = readFile(filePath);
  if (!content) return;
  const lines = content.split('\n');
  const matches = [];
  lines.forEach((line, idx) => {
    if (/^\s*print\(/.test(line)) {
      matches.push(`  L${idx + 1}: ${line.trim()}`);
    }
  });
  if (matches.length > 0) {
    console.error(`[Hook] print() found in ${path.basename(filePath)} (use logging instead):`);
    matches.slice(0, 5).forEach(m => console.error(m));
  }
}

function findProjectRoot(startDir) {
  const fs = require('fs');
  let dir = startDir;
  while (dir !== path.dirname(dir)) {
    if (fs.existsSync(path.join(dir, 'package.json')) || fs.existsSync(path.join(dir, 'pyproject.toml'))) {
      return dir;
    }
    dir = path.dirname(dir);
  }
  return startDir;
}
