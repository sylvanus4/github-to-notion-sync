#!/usr/bin/env node
'use strict';

/**
 * beforeShellExecution hook: Command safety gate.
 *
 * - BLOCK: git push --force to main/dev
 * - WARN: dangerous commands (rm -rf /, DROP TABLE)
 * - WARN: git push reminder to review changes
 */

const { readStdin } = require('./lib/utils');
const { isHookEnabled } = require('./lib/hook-flags');

readStdin().then(raw => {
  try {
    const input = JSON.parse(raw || '{}');
    const cmd = String(input.command || input.args?.command || '');

    if (isHookEnabled('pre:bash:force-push-block', ['standard', 'strict'])) {
      if (/\bgit\s+push\s+.*--force\b/.test(cmd) || /\bgit\s+push\s+-f\b/.test(cmd)) {
        if (/\b(main|master|dev)\b/.test(cmd)) {
          console.error('[Hook] BLOCKED: Force push to main/dev is not allowed.');
          console.error('[Hook] Use a feature branch or remove --force.');
          process.exit(2);
        }
      }
    }

    if (isHookEnabled('pre:bash:dangerous-cmd-warn', ['standard', 'strict'])) {
      if (/\brm\s+-rf\s+\/\s*$/.test(cmd) || /\brm\s+-rf\s+\/[^/]/.test(cmd) === false && /\brm\s+-rf\s+\/\s/.test(cmd)) {
        console.error('[Hook] WARNING: Destructive rm -rf detected. Double-check the path.');
      }
      if (/\bDROP\s+(TABLE|DATABASE)\b/i.test(cmd)) {
        console.error('[Hook] WARNING: DROP TABLE/DATABASE detected. Ensure this is intentional.');
      }
    }

    if (isHookEnabled('pre:bash:git-push-reminder', ['strict'])) {
      if (/\bgit\s+push\b/.test(cmd) && !/--force/.test(cmd)) {
        console.error('[Hook] Reminder: Review changes before push — git diff origin/main...HEAD');
      }
    }

    if (isHookEnabled('pre:bash:tmux-suggest', ['standard', 'strict'])) {
      const longRunners = /\b(uvicorn|gunicorn|flask\s+run|npm\s+run\s+dev|next\s+dev|vite|webpack\s+serve|pytest-watch|nodemon|tail\s+-f|make\s+serve|docker\s+compose\s+up)\b/;
      if (longRunners.test(cmd) && !/\btmux\b/.test(cmd)) {
        console.error('[Hook] Tip: This looks like a long-running process. Consider using tmux:');
        console.error('[Hook]   /tmux new devserver "' + cmd.replace(/"/g, '\\"') + '"');
      }
    }
  } catch {
    // noop
  }

  process.stdout.write(raw);
}).catch(() => process.exit(0));
