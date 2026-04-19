#!/usr/bin/env node
'use strict';

/**
 * beforeSubmitPrompt hook: Secret detection in prompts.
 *
 * Scans for API keys, tokens, private keys, and PII patterns.
 * Warns but does not block (exit 0) to avoid false positives.
 */

const { readStdin } = require('./lib/utils');
const { isHookEnabled } = require('./lib/hook-flags');

const SECRET_PATTERNS = [
  { pattern: /sk-[a-zA-Z0-9]{20,}/, label: 'OpenAI API key' },
  { pattern: /ghp_[a-zA-Z0-9]{36,}/, label: 'GitHub PAT' },
  { pattern: /ghs_[a-zA-Z0-9]{36,}/, label: 'GitHub App token' },
  { pattern: /AKIA[A-Z0-9]{16}/, label: 'AWS access key' },
  { pattern: /xox[bpsa]-[a-zA-Z0-9-]+/, label: 'Slack token' },
  { pattern: /-----BEGIN (RSA |EC )?PRIVATE KEY-----/, label: 'Private key' },
  { pattern: /AIza[0-9A-Za-z_-]{35}/, label: 'Google API key' },
  { pattern: /eyJ[a-zA-Z0-9_-]{10,}\.[a-zA-Z0-9_-]{10,}\./, label: 'JWT token' },
];

const PII_PATTERNS = [
  { pattern: /\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b/, label: 'email address' },
  { pattern: /\b\d{3}-\d{2}-\d{4}\b/, label: 'SSN pattern' },
];

readStdin().then(raw => {
  try {
    const input = JSON.parse(raw || '{}');
    const prompt = String(input.prompt || input.content || input.message || '');

    if (!prompt || !isHookEnabled('pre:prompt:secret-scan', ['minimal', 'standard', 'strict'])) {
      process.stdout.write(raw);
      return;
    }

    let found = false;
    for (const { pattern, label } of SECRET_PATTERNS) {
      if (pattern.test(prompt)) {
        if (!found) {
          console.error('[Hook] WARNING: Potential secrets detected in prompt!');
          found = true;
        }
        console.error(`[Hook]   - ${label}`);
      }
    }

    if (isHookEnabled('pre:prompt:pii-scan', ['standard', 'strict'])) {
      for (const { pattern, label } of PII_PATTERNS) {
        if (pattern.test(prompt)) {
          if (!found) {
            console.error('[Hook] WARNING: Sensitive data detected in prompt!');
            found = true;
          }
          console.error(`[Hook]   - ${label}`);
        }
      }
    }

    if (found) {
      console.error('[Hook] Remove secrets/PII before submitting. Use environment variables instead.');
    }
  } catch {
    // pass through
  }

  process.stdout.write(raw);
}).catch(() => process.exit(0));
