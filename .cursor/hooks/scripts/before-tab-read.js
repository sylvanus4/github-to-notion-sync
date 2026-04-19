#!/usr/bin/env node
'use strict';

/**
 * beforeTabFileRead hook: Block Tab autocomplete from reading sensitive files.
 *
 * Prevents accidental secret exposure via inline completions.
 * Exit code 2 blocks the read; exit code 0 allows it.
 */

const { readStdin } = require('./lib/utils');

const BLOCKED_PATTERNS = [
  /\.(env|key|pem)$/i,
  /\.env\./i,
  /credentials\.json$/i,
  /client_secret[_\-].*\.json$/i,
  /\.secrets\.baseline$/i,
  /id_rsa$/i,
  /id_ed25519$/i,
  /\.p12$/i,
  /\.pfx$/i,
  /service[_-]?account.*\.json$/i,
];

readStdin().then(raw => {
  try {
    const input = JSON.parse(raw || '{}');
    const filePath = String(input.path || input.file || '');
    if (!filePath) { process.stdout.write(raw); return; }

    for (const pattern of BLOCKED_PATTERNS) {
      if (pattern.test(filePath)) {
        console.error(`[Hook] BLOCKED: Tab cannot read sensitive file: ${filePath}`);
        process.exit(2);
      }
    }
  } catch {
    // pass through
  }

  process.stdout.write(raw);
}).catch(() => process.exit(0));
