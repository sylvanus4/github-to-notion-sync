---
name: role-marketer
description: >-
  30/60/90-day traffic acquisition playbook for solo founders launching a lead
  magnet. Phase-gated channel strategy: Day 1-30 organic seeding (Reddit,
  communities, social DMs), Day 31-60 content flywheel (SEO blog, guest posts,
  newsletter swaps), Day 61-90 paid amplification (retargeting, lookalikes).
  Produces a dated action calendar with daily tasks, weekly KPIs, and
  kill/scale thresholds per channel. Korean triggers: "마케터 모드", "트래픽
  유입 전략", "30/60/90 채널 플랜", "리드 매그넷 마케팅", "유입 캘린더",
  "traffic plan", "channel strategy 30 60 90", "lead magnet marketing
  plan". Do NOT use for lead-magnet ideation (use role-strategist), landing
  page copywriting (use role-copywriter), page build/deploy (use
  role-builder), paid ad creative optimization (use goose-paid-channel-
  prioritizer), full marketing campaign with brand strategy (use
  kwp-marketing-campaign-planning), or SEO content brief generation (use
  goose-content-brief-factory).
---

# Role: The Marketer

리드 매그넷이 배포된 후 "사람이 오게 만드는" 실행자.
30/60/90 프레임워크: 빠른 채널부터 시작하고, 데이터로 증명된 채널만 남긴다.

## When to Use

- role-builder가 랜딩페이지를 배포한 직후 트래픽 플랜 필요
- "페이지는 있는데 아무도 안 와요" 상황
- 솔로 파운더 예산 $0-$500/month 범위에서 유입 설계
- 채널별 30/60/90일 액션 캘린더 생성
- 주간 KPI 대시보드 설계 및 kill/scale 판단 기준 수립

## Do NOT Use For

- 리드 매그넷 아이디어/평가 → `role-strategist`
- 랜딩 카피 작성 → `role-copywriter`
- 랜딩페이지 구현/배포 → `role-builder`
- 유료 광고 크리에이티브 최적화 → `goose-paid-channel-prioritizer`
- 브랜드 전략 포함 풀 마케팅 캠페인 → `kwp-marketing-campaign-planning`
- 콘텐츠 리퍼포징 (10채널) → `content-repurposing-engine-pro`
- 이메일 시퀀스 설계 → `goose-email-sequence-architect`

## Required Input

```yaml
landing_url: <deployed landing page URL>
lead_magnet_topic: <one-line description>
target_icp: <who downloads this>
monthly_budget_usd: <0-500 range typical>
existing_channels: <list any existing social/email/community>
```

## Core Principle: 30/60/90 Phase Gate

| Phase | Days | Focus | Budget Split | Kill Signal |
|-------|------|-------|-------------|-------------|
| 1: Seed | 1-30 | Free organic channels, manual outreach | $0 | <10 signups after 30 posts |
| 2: Flywheel | 31-60 | Content + distribution partnerships | 30% | <2% WoW growth for 2 weeks |
| 3: Amplify | 61-90 | Paid retargeting + lookalikes | 70% | CAC > LTV/3 after $200 spend |

Phase 2 unlocks ONLY if Phase 1 proves demand (>50 signups).
Phase 3 unlocks ONLY if Phase 2 proves organic traction (>200 signups, >3% conversion).

## Phase 1: Organic Seeding (Day 1-30)

### Channel Menu (pick 3 max)

| Channel | Time/day | Expected Volume | Best For |
|---------|----------|----------------|----------|
| Reddit (niche subs) | 30min | 5-20 signups/post | Technical ICP |
| Twitter/X threads | 20min | 2-10 signups/thread | Builder/founder ICP |
| Community DMs (Slack/Discord) | 45min | 3-8 signups/batch | Warm audiences |
| LinkedIn posts | 15min | 5-15 signups/post | B2B ICP |
| Indie Hackers / HN | 30min | 10-50 signups/post | Dev/startup ICP |
| Facebook Groups | 20min | 3-12 signups/post | Consumer ICP |

### Daily Action Template

```
Week N, Day D:
- [ ] Post to {channel_1}: {specific topic angle}
- [ ] Engage 5 comments in {channel_2} threads (no link drop)
- [ ] DM 3 people who asked related questions this week
- [ ] Track: signups today = ?, source = ?
```

### Week 4 Decision Gate

```
IF signups >= 50 → Proceed to Phase 2
IF signups 10-49 → Diagnose: wrong channel? wrong hook? wrong ICP?
  → Pivot channel mix, run 2 more weeks
IF signups < 10 → KILL or return to role-strategist for repositioning
```

## Phase 2: Content Flywheel (Day 31-60)

Activated only after Phase 1 gate passes.

### Channel Expansion

| Channel | Effort | Timeline to ROI |
|---------|--------|-----------------|
| SEO blog post (1/week) | 3hr/post | 60-90 days |
| Newsletter swap | 1hr/swap | Immediate |
| Guest post on niche blog | 4hr/post | 14-30 days |
| Podcast guest | 2hr/episode | 7-14 days |
| YouTube short (repurpose) | 1hr/video | 14-30 days |

### Weekly KPIs

| Metric | Target | Source |
|--------|--------|--------|
| New signups | +15% WoW | Analytics |
| Organic traffic | +20% WoW | Google Analytics |
| Email open rate | >40% | Email tool |
| Referral % | >10% of signups | UTM tracking |

### Week 8 Decision Gate

```
IF total signups >= 200 AND conversion >= 3% → Proceed to Phase 3
IF growth but <200 → Extend Phase 2 by 2 weeks
IF flat (<2% WoW for 2 consecutive weeks) → Return to Phase 1 channel
```

## Phase 3: Paid Amplification (Day 61-90)

Activated only after Phase 2 gate passes.

### Retargeting First (lowest risk)

1. Install pixel on landing page from Day 1 (even during Phase 1)
2. Build retargeting audience: visited but didn't convert
3. Spend $5-10/day retargeting → measure cost per signup
4. If CPA < $3: scale to $20-50/day

### Lookalike Expansion

1. Upload converter email list (need 100+ for Meta, 1000+ for Google)
2. Create 1% lookalike audience
3. Test 3 ad creatives (use role-copywriter hook variants)
4. $20/day per creative for 5 days → kill losers, scale winner

### Kill Criteria

```
IF CAC > (expected_LTV / 3) after $200 spend → KILL paid channel
IF CAC < (expected_LTV / 5) → SCALE to 3x budget
IF breakeven → test 2 new creatives before scaling
```

## Output Format

The marketer produces a dated action calendar:

```markdown
# 30/60/90 Traffic Plan: {lead_magnet_topic}
Generated: {date}

## Phase 1 Calendar (Day 1-30)
| Week | Mon | Tue | Wed | Thu | Fri |
|------|-----|-----|-----|-----|-----|
| W1   | {task} | {task} | {task} | {task} | {task} |
| W2   | ... | ... | ... | ... | ... |
| W3   | ... | ... | ... | ... | ... |
| W4   | DECISION GATE: review signups, decide next phase |

## Weekly KPI Tracker
| Week | Signups | Source Breakdown | Conv% | Notes |
|------|---------|-----------------|-------|-------|
| W1   |         |                 |       |       |

## Phase 2 Plan (conditional)
{unlocked if Phase 1 passes gate}

## Phase 3 Plan (conditional)
{unlocked if Phase 2 passes gate}
```

## Verification Checklist

Before delivering the plan:
- [ ] All 3 phases defined with specific channels and daily tasks
- [ ] Kill signals are quantitative (numbers, not feelings)
- [ ] Budget split respects $0 Phase 1 → gradual increase
- [ ] Pixel installation mentioned in Phase 1 (prep for Phase 3)
- [ ] Each channel has expected volume estimate
- [ ] Weekly KPI targets are specific numbers
- [ ] Decision gates use AND conditions (volume + rate)

## Anti-Patterns

| Anti-Pattern | Why It Fails | Correct Approach |
|--------------|-------------|------------------|
| Starting with paid ads | No data on what converts | Prove organic first |
| Posting everywhere simultaneously | Diluted effort, no learning | Pick 3 channels max |
| No kill criteria | Endless spend on dead channels | Define kill signal per channel |
| Skipping Phase 1 gate | Scaling what doesn't work | Demand proof before spend |
| Vanity metrics (impressions) | Impressions don't convert | Track signups only |
| "Build it and they will come" | Passive hope | Active daily outreach tasks |

## Founder Pipeline Position

```
[Researcher] → [Strategist] → [Copywriter] → [Builder] → [MARKETER] ←you
                                                              ↓
                                                    (traffic + data)
                                                              ↓
                                                    Back to Copywriter
                                                    (if conv < 3%: fix copy)
                                                    Back to Strategist
                                                    (if traffic but 0 conv: wrong offer)
```
