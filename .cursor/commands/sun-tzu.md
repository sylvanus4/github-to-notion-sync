## Sun Tzu Competitive Analyzer

Map any business, career, or trading situation onto Sun Tzu's Art of War principles and prescribe the precise strategic move.

### Usage

```
/sun-tzu {situation}                                  # standalone analysis
/sun-tzu {situation} --competitive                    # overlay on competitive data
/sun-tzu {situation} --trading                        # market-adapted analysis
/sun-tzu {situation} --role-layer                     # concise brief for role-dispatcher
/sun-tzu {situation} --with-first-principles          # strip assumptions first
/sun-tzu {situation} --output scqa                    # format as SCQA narrative
/sun-tzu {situation} --competitive --output scqa      # combine flags
```

### Flags

| Flag | Effect |
|------|--------|
| `--competitive` | Compose with `kwp-*-competitive-analysis` for competitive data enrichment |
| `--trading` | Adapt 5 factors to market structure, sector rotation, and portfolio positioning |
| `--role-layer` | Output concise Strategic Terrain Brief (< 200 words) for executive-briefing pipeline |
| `--with-first-principles` | Run `first-principles-analysis` pre-pass before Sun Tzu analysis |
| `--output scqa` | Format the verdict as Situation-Complication-Question-Answer narrative |

### Workflow

1. **Parse input** — Extract situation description and flags
2. **Mode selection** — Determine operating mode from flags
3. **Optional pre-pass** — Run first-principles-analysis if `--with-first-principles`
4. **Five-Factor Analysis** — Terrain, Enemy, Relative Strength, Information Asymmetry, Timing
5. **Six-Step Strategic Verdict** — Read terrain → Name enemy → Find gap → Prescribe move → Name trap → Governing principle
6. **Persist output** — Save to `outputs/sun-tzu/{date}/` (standalone/competitive/trading) or `outputs/role-analysis/` (role-layer)
7. **Report** — Present analysis with eval gate verification

### Execution

Read and follow the `sun-tzu-analyzer` skill (`.cursor/skills/standalone/sun-tzu-analyzer/SKILL.md`).

### Examples

Business competitive situation:
```
/sun-tzu 우리 SaaS 제품이 대기업 경쟁사의 가격 인하에 직면해 있다
```

Trading / market context:
```
/sun-tzu 반도체 섹터가 과열됐는데 AI 테마주를 계속 들고 있어야 할지 --trading
```

Competitive overlay with SCQA format:
```
/sun-tzu AWS가 우리 핵심 기능을 자체 서비스로 출시했다 --competitive --output scqa
```

Career strategy:
```
/sun-tzu 이직 제안을 받았는데 현재 회사에서 승진 가능성도 있다
```

Role-layer for executive briefing:
```
/sun-tzu New GPU inference service launch --role-layer
```

First principles pre-analysis:
```
/sun-tzu 우리 팀이 마이크로서비스 전환을 추진 중인데 맞는 방향인지 --with-first-principles
```
