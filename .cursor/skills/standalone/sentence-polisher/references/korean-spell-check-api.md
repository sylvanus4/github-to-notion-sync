---
name: korean-spell-check-api
description: "바른한글 (구 부산대 맞춤법/문법 검사기) API reference for sentence-polisher Step 3.5."
---
# Korean Spell-Check API Reference

## Overview

바른한글 API (successor of 부산대 맞춤법/문법 검사기) provides Korean spell and grammar checking based on 국립국어원 (National Institute of Korean Language) rules. This reference documents the API surface used by `sentence-polisher` Step 3.5.

## Endpoint

```
POST https://lab-api.bsm.klnet.kr/v1/check
Content-Type: application/x-www-form-urlencoded
```

## Request

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `text` | string | Yes | Korean text to check (max 1500 characters per request) |

## Response

JSON array of correction objects:

```json
[
  {
    "original": "틀린 표현",
    "suggestion": "올바른 표현",
    "reason": "교정 사유 (국립국어원 규칙 기반)"
  }
]
```

## Chunking Strategy

Long texts must be split before sending:

1. Split at sentence boundaries (`.`, `!`, `?`, `\n`)
2. Each chunk must not exceed 1500 characters
3. If a single sentence exceeds 1500 characters, split at clause boundaries (`,`, `;`)
4. Preserve sentence integrity across chunks

## Rate Limiting

- **Mandatory 1-second pause** between consecutive API calls
- Keep overall call frequency low (non-commercial use)

## Integration with sentence-polisher

### When to invoke

- After Step 3 (Error Scan), before Step 4 (Auto-fix)
- Only in Korean mode or Bilingual mode
- Skippable: if the API is unavailable, the LLM-based checks from Step 3 serve as fallback

### Merging results

API corrections are merged into the Error Scan results under:

```
Korean-specific > 맞춤법 검사기
```

Each correction maps to the Change Summary format:

```
"original" -> "suggestion" -- [Korean-specific/맞춤법검사기: reason]
```

### Graceful degradation

| Condition | Action |
|-----------|--------|
| API returns HTTP error (4xx/5xx) | Skip silently, log reason |
| API timeout (>5 seconds) | Skip silently, log reason |
| Network unreachable | Skip silently, log reason |
| Empty response | Treat as "no errors found" |

Do NOT block the pipeline on API failures. LLM-based Korean checks from Step 3 provide baseline coverage.

## Usage Policy

- **Non-commercial use only**
- Do not cache or redistribute API results
- Do not call in tight loops or batch thousands of requests
- Attribute corrections to 바른한글 / 국립국어원 when presenting results

## Error Categories Covered

The API checks against 국립국어원 standard rules:

| Category | Examples |
|----------|----------|
| 맞춤법 (Spelling) | 되/돼, 웬/왠, 로서/로써 |
| 띄어쓰기 (Spacing) | 한 동안/한동안, 할 수 있다/할수있다 |
| 문법 (Grammar) | 이/가, 을/를 particle misuse |
| 표준어 (Standard language) | 짜장면 -> 자장면 (pre-2014), dialect normalization |
| 외래어 표기 (Loanword orthography) | 컨텐츠 -> 콘텐츠, 악세사리 -> 액세서리 |

## Prerequisites

- Python 3.10+ with `urllib.request` (stdlib, no external deps)
- Network access to `lab-api.bsm.klnet.kr`

## Example Call (Python)

```python
import urllib.request
import urllib.parse
import json
import time

def check_korean_spelling(text: str) -> list[dict]:
    url = "https://lab-api.bsm.klnet.kr/v1/check"
    data = urllib.parse.urlencode({"text": text}).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")

    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception:
        return []

def check_with_chunking(full_text: str, max_chunk: int = 1500) -> list[dict]:
    import re
    sentences = re.split(r'(?<=[.!?\n])\s*', full_text)
    chunks, current = [], ""

    for s in sentences:
        if len(current) + len(s) > max_chunk:
            if current:
                chunks.append(current)
            current = s
        else:
            current += s
    if current:
        chunks.append(current)

    results = []
    for chunk in chunks:
        results.extend(check_korean_spelling(chunk))
        time.sleep(1)
    return results
```

## Source

Adapted from `modu-ai/cowork-plugins` `moai-content/skills/korean-spell-check/SKILL.md`, tailored for integration as a sub-step within the `sentence-polisher` pipeline.
