---
name: kr-ecommerce-guide
description: |
  Korean e-commerce operations guide covering Naver Smartstore, Coupang, product detail page creation,
  Korean SEO (Naver C-Rank, D.I.A.+), SNS content for Korean channels, campaign planning,
  performance reporting (GA4, Naver Ads, Meta Ads, Kakao Moment), and target customer messaging.
  Consolidates Korean-specific e-commerce knowledge from product listing to post-purchase CRM.
  Use when the user asks to "상세페이지 만들어줘", "스마트스토어 최적화", "쿠팡 상품 등록",
  "네이버 SEO", "C-Rank 개선", "이커머스 캠페인", "상품 상세 페이지", "한국 이커머스",
  "Korean e-commerce", "Smartstore optimization", "Coupang listing", "kr-ecommerce-guide",
  "product detail page", "네이버 쇼핑 노출", "쿠팡 로켓그로스", "SNS 마케팅 콘텐츠",
  "퍼포먼스 리포트", "타겟 스크립트", "채널별 KPI", "ROAS 분석", "네이버 광고 분석",
  "고객 여정 맵", "CRM 전략", "인플루언서 전략", "그로스해킹",
  or any Korean e-commerce operations, listing optimization, or marketing task.
  Do NOT use for non-Korean e-commerce platforms (use general marketing skills).
  Do NOT use for China-specific platforms like Taobao, Douyin, Xiaohongshu (use china-* marketing skills).
  Do NOT use for stock/financial analysis (use trading skills).
  Do NOT use for general brand identity without e-commerce context (use kwp-brand-voice skills).
user-invocable: true
version: 1.0.0
---

# Korean E-Commerce Guide (kr-ecommerce-guide)

Korean e-commerce operations from product listing to performance optimization.
Covers the two dominant Korean platforms (Naver Smartstore, Coupang) plus Korean-specific
SEO, SNS content, campaign planning, and performance reporting.

> Source: Adapted from modu-ai/cowork-plugins moai-marketing (campaign-planner, seo-audit,
> sns-content, target-script, performance-report) + project-native marketing skills.

---

## Modes

### Mode 1: Product Detail Page (상세페이지)

Build conversion-optimized product detail pages for Korean e-commerce platforms.

**Trigger**: "상세페이지 만들어줘", "product detail page", "쿠팡 상세페이지", "스마트스토어 상품 등록"

**Input required**:
- Product name, price, key features
- Target platform (Smartstore / Coupang / both)
- Target audience (optional)
- Images or image descriptions (optional)

**Output**: HTML or React code following the structure in `references/product-detail-page.md`

**Page structure**:
1. Header + breadcrumb navigation
2. Image gallery (main + thumbnails, zoom support)
3. Product info (name, price, rating, stock, shipping)
4. Detailed description with benefit-focused copy
5. Feature comparison table
6. Social proof (reviews, testimonials, purchase count)
7. FAQ / Q&A section
8. Related product recommendations
9. Purchase CTA (sticky on mobile)

**Platform-specific rules**:

| Element | Naver Smartstore | Coupang |
|---------|-----------------|---------|
| Image size | 1000x1000px min, 860px width for detail | 850x850px, white background |
| Title | 50 chars max, keyword-front-loaded | 100 chars, category keyword required |
| Detail format | Long-scroll image-heavy HTML | Structured A+ content sections |
| Mobile | Mandatory responsive, AMP optional | Coupang app-first layout |
| SEO | Naver Shopping tag optimization | Coupang search algorithm |

---

### Mode 2: Korean SEO Audit (네이버/구글 SEO)

Comprehensive SEO analysis for Korean search engines with platform-specific metrics.

**Trigger**: "SEO 감사해줘", "네이버 상위 노출", "C-Rank 개선", "키워드 분석"

**Procedure**:

1. **Naver SEO Analysis**
   - C-Rank (Creator Rank): authority score based on content consistency, engagement, expertise
   - D.I.A.+ (Deep Intent Analysis): content quality scoring for search intent matching
   - Naver Shopping SEO: product tag optimization, category relevance, review velocity
   - Blog SEO: keyword density, multimedia ratio, internal linking, posting frequency

2. **Google SEO Analysis**
   - Core Web Vitals (LCP, CLS, INP)
   - E-E-A-T signals (Experience, Expertise, Authoritativeness, Trustworthiness)
   - Mobile-first indexing compliance
   - Structured data (JSON-LD for Product, FAQ, Review)

3. **GEO (Generative Engine Optimization)**
   - AI search citation optimization (ChatGPT, Gemini, Perplexity)
   - Authoritative source positioning
   - Structured answer formatting

**Output**: Severity-ranked audit report with fix priorities.
See `references/korean-seo-guide.md` for detailed C-Rank/D.I.A.+ optimization strategies.

---

### Mode 3: SNS Content Creation (채널별 콘텐츠)

Generate Korean-market-optimized content for major social/content channels.

**Trigger**: "SNS 콘텐츠 만들어줘", "인스타 게시물", "네이버 블로그 글", "유튜브 스크립트"

**Supported channels**:

| Channel | Format | Tone | Key metric |
|---------|--------|------|------------|
| Instagram | Carousel 10장, Reels 15-60s | 감성적·비주얼 중심 | 저장수, 공유수 |
| YouTube | Shorts 60s, Long 10-15min | 정보 전달형 | 시청 지속율 |
| Naver Blog | 2000-3000자 + 이미지 15장+ | 전문적·신뢰감 | C-Rank, 검색 유입 |
| Kakao Channel | 카드뉴스, 알림톡 | 친근한·실용적 | 클릭율, 전환율 |
| TikTok | 15-60s vertical | 트렌디·재미 | 완시율, 공유수 |

**Content creation rules**:
- Korean honorific level: 해요체 (polite informal) for most channels
- Hashtag strategy: Korean + English mixed, 15-30 per post for Instagram
- Emoji usage: moderate, platform-appropriate
- CTA placement: end of content with urgency trigger

---

### Mode 4: Campaign Planning (캠페인 기획)

Plan and execute Korean e-commerce marketing campaigns.

**Trigger**: "캠페인 기획해줘", "A/B 테스트", "인플루언서 전략", "그로스해킹"

**Sub-modes**:

**4a. Campaign Strategy**
- Objective setting (awareness / consideration / conversion)
- Budget allocation across Korean channels
- Timeline with Korean holiday calendar (설날, 추석, 빼빼로데이, 블랙프라이데이 etc.)
- A/B test design with statistical significance calculation

**4b. Influencer Strategy**
- Korean influencer tier classification (mega/macro/micro/nano)
- Platform-specific influencer discovery (YouTube, Instagram, Naver Blog)
- Contract template with KPI-based payment structure
- Content collaboration guidelines

**4c. CRM & Customer Journey**
- Korean customer journey mapping (discovery via Naver → comparison → purchase → review)
- Post-purchase engagement (Kakao Channel follow-up, review incentives)
- Loyalty program design
- Churn prevention triggers

**4d. Growth Hacking**
- Viral loop design for Korean platforms
- Referral program mechanics
- Community-driven growth (Naver Cafe, Kakao Open Chat)

---

### Mode 5: Performance Report (성과 보고서)

Generate marketing performance reports from Korean ad platform data.

**Trigger**: "성과 보고서 만들어줘", "ROAS 분석", "채널별 KPI", "광고비 분석"

**Supported data sources**:

| Platform | Key metrics | Korean-specific notes |
|----------|-------------|----------------------|
| GA4 | Sessions, CVR, Revenue | UTM Korean naming convention |
| Naver Ads | Powerlink CTR, Shopping Ads ROAS | C-Rank impact on CPC |
| Meta Ads | CPM, CPA, ROAS | Korean audience targeting |
| Kakao Moment | Display reach, Message open rate | Kakao Talk integration metrics |
| Google Ads | Search impression share, CPC | Korean keyword competition |

**Report structure**:
1. Executive Summary (경영진용 1-page)
2. Channel-by-channel deep dive with trend arrows
3. Budget efficiency analysis (채널별 ROAS 비교)
4. Audience insight (demographics, device, time-of-day)
5. Competitor benchmark (estimated)
6. Next period action plan with specific KPI targets

---

### Mode 6: Target Messaging Script (타겟 스크립트)

Generate customer-targeted messaging scripts through a 5-stage pipeline.

**Trigger**: "타겟 스크립트", "고객 맞춤 메시지", "buyer persona 카피", "채널별 스크립트"

**Pipeline**:
1. **Target Audience Analysis**: Demographics, psychographics, buying behavior
2. **Pain Point Extraction**: Top 3-5 customer pain points with evidence
3. **Core Message Generation**: Value proposition + emotional hook + rational proof
4. **Channel Adaptation**: Rewrite for email / SNS / web / ads with format rules
5. **A/B Test Proposal**: 2-3 variants per channel with hypothesis

---

## Integration Points

| Task | Primary skill | This skill adds |
|------|--------------|-----------------|
| General SEO | marketing-seo-ops | Naver C-Rank, D.I.A.+, Shopping SEO |
| Content creation | kwp-marketing-content-creation | Korean channel-specific formats |
| Campaign planning | kwp-marketing-campaign-planning | Korean holiday calendar, Naver/Kakao channels |
| Performance analytics | kwp-marketing-performance-analytics | Naver Ads, Kakao Moment data |
| Brand voice | kwp-brand-voice | Korean honorific level adaptation |
| Product copy | content-repurposing-engine | Smartstore/Coupang detail page format |

## Output Formats

- **Markdown**: Default for all modes
- **HTML/React**: Mode 1 (product detail pages)
- **DOCX**: Mode 5 (performance reports) via anthropic-docx
- **Notion**: Any mode via md-to-notion

## References

- `references/product-detail-page.md` -- Product detail page structure and platform rules
- `references/korean-seo-guide.md` -- Naver C-Rank, D.I.A.+, Shopping SEO optimization

---
*kr-ecommerce-guide v1.0.0 | Source: modu-ai/cowork-plugins moai-marketing + project skills*
