"""Secret/PII redaction for Claude Code transcripts.

Used by extract_sft.py / extract_preference.py before any output write.
Pure regex; no external deps.
"""
from __future__ import annotations

import json
import re

# Order matters — longer/more-specific patterns first
PATTERNS: list[tuple[re.Pattern, str]] = [
    # SSH private key blocks (multi-line)
    (re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----.*?-----END [A-Z ]*PRIVATE KEY-----", re.DOTALL),
     "[REDACTED_SSH_PRIVATE_KEY]"),

    # HF tokens
    (re.compile(r"hf_[A-Za-z0-9]{30,}"), "[REDACTED_HF_TOKEN]"),

    # RunPod API keys (rpa_ + 40+)
    (re.compile(r"rpa_[A-Za-z0-9]{40,}"), "[REDACTED_RUNPOD_KEY]"),

    # Anthropic API keys
    (re.compile(r"sk-ant-[A-Za-z0-9_\-]{40,}"), "[REDACTED_ANTHROPIC_KEY]"),

    # Generic OpenAI-style sk-...
    (re.compile(r"\bsk-[A-Za-z0-9]{30,}"), "[REDACTED_API_KEY]"),

    # Stripe-style pk_live_/pk_test_
    (re.compile(r"\bpk_(live|test)_[A-Za-z0-9]{20,}"), "[REDACTED_STRIPE_KEY]"),

    # AWS access keys
    (re.compile(r"\bAKIA[A-Z0-9]{16}\b"), "[REDACTED_AWS_ACCESS_KEY]"),
    (re.compile(r"\bASIA[A-Z0-9]{16}\b"), "[REDACTED_AWS_TEMP_KEY]"),

    # GitHub PATs
    (re.compile(r"\bghp_[A-Za-z0-9]{36,}\b"), "[REDACTED_GITHUB_PAT]"),
    (re.compile(r"\bghs_[A-Za-z0-9]{36,}\b"), "[REDACTED_GITHUB_TOKEN]"),

    # Slack tokens
    (re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{20,}\b"), "[REDACTED_SLACK_TOKEN]"),

    # Bearer / Authorization headers
    (re.compile(r"(?i)(authorization:\s*bearer\s+)[A-Za-z0-9._\-]+"), r"\1[REDACTED_BEARER]"),

    # Email addresses (loose; mask local part)
    (re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"), "[REDACTED_EMAIL]"),

    # SSH ed25519 / rsa public keys (full key blob)
    (re.compile(r"ssh-(ed25519|rsa|dss|ecdsa-sha2-nistp\d+)\s+[A-Za-z0-9+/=]{50,}(\s+[\S]+)?"),
     "[REDACTED_SSH_PUBLIC_KEY]"),

    # Twitter/X cookies (auth_token, ct0)
    (re.compile(r"\bauth_token=[a-f0-9]{40,}"), "auth_token=[REDACTED]"),
    (re.compile(r"\bct0=[a-f0-9]{160,}"), "ct0=[REDACTED]"),

    # JWT (3 dot-separated b64url segments, length-bounded)
    (re.compile(r"\beyJ[A-Za-z0-9_\-]{10,}\.eyJ[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}"),
     "[REDACTED_JWT]"),
]

# Add custom patterns by appending to this list (NOT by editing PATTERNS above —
# keep the canonical list in version control)
EXTRA_PATTERNS: list[tuple[re.Pattern, str]] = []


def redact_text(s: str) -> tuple[str, dict[str, int]]:
    """Apply all patterns to a string. Returns (redacted, hit_counts)."""
    if not s:
        return s, {}
    hits: dict[str, int] = {}
    out = s
    for pat, repl in PATTERNS + EXTRA_PATTERNS:
        # Count before sub
        matches = pat.findall(out)
        if matches:
            hits[repl] = hits.get(repl, 0) + len(matches)
        out = pat.sub(repl, out)
    return out, hits


def redact_obj(obj):
    """Recursively walk a JSON-like structure and redact all strings.
    Returns (redacted_obj, total_hit_counts).
    """
    total: dict[str, int] = {}

    def merge(h):
        for k, v in h.items():
            total[k] = total.get(k, 0) + v

    def walk(o):
        if isinstance(o, str):
            r, h = redact_text(o)
            merge(h)
            return r
        if isinstance(o, dict):
            return {k: walk(v) for k, v in o.items()}
        if isinstance(o, list):
            return [walk(v) for v in o]
        return o

    return walk(obj), total


if __name__ == "__main__":
    # Quick smoke test
    import sys
    test = sys.stdin.read() if not sys.stdin.isatty() else """
    HF_TOKEN=hf_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
    Authorization: Bearer eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0.signature_part
    user@example.com sent ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIabc123def456ghi789jkl test@host
    """
    redacted, hits = redact_text(test)
    print(redacted)
    print(json.dumps(hits, indent=2))
