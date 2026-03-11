# PPTX Slide Mapping Instructions

**Language rule**: All slide text, section titles, bullet content, table headers,
and labels MUST be written in Korean. English is only allowed for proper nouns
and technical terminology that has no standard Korean equivalent.

Generate the PowerPoint presentation using PptxGenJS from scratch following
the `anthropic-pptx` skill patterns.

## Slide Structure (~25-35 slides)

```
섹션 1: 오프닝 (3 슬라이드)
  1.  제목 슬라이드
  2.  논문 개요 (제목, 저자, 게재처, 한줄 요약)
  3.  목차 / 발표 순서

섹션 2: 핵심 요약 (2-3 슬라이드)
  4.  주요 발견 사항 요약 (핵심 포인트)
  5.  평가 점수 테이블 (참신성, 건전성, 실험, 명확성, 영향력)
  6.  추천 요약

섹션 3: 논문 리뷰 하이라이트 (5-8 슬라이드)
  7.  문제 정의 및 동기
  8.  핵심 방법론 — 아키텍처 설명
  9.  주요 기여점 (번호 목록)
  10. 실험 설정 (데이터셋, 베이스라인, 평가 지표)
  11. 주요 결과 테이블
  12. Ablation Study 하이라이트
  13. 강점 vs 약점 (2열 레이아웃)
  14. 재현성 평가

섹션 4: PM/연구 관점 분석 (관점당 2-3 슬라이드, ~12-18 총)
  15-17. PM 전략 (SWOT, 가치 제안, 린 캔버스)
  18-20. 시장 조사 (TAM/SAM/SOM, 경쟁 지도, 페르소나)
  21-23. 제품 발견 (가정 테이블, OST, 실험 설계)
  24-26. GTM (전략 개요, ICP, 비치헤드)
  27-28. 통계 검토 (방법론 엄밀성, 재현성 점수)
  29-31. 실행 계획 (미니 PRD, 포지셔닝, 북극성 지표)

섹션 5: 마무리 (2-3 슬라이드)
  32. 핵심 시사점 (3-5개 포인트)
  33. 후속 과제 및 액션 아이템
  34. 참고 문헌 및 리소스
```

## Script Template

Write a Node.js script to `/tmp/paper-review-pptx.js` and execute it.

```javascript
const pptxgen = require("pptxgenjs");
const fs = require("fs");

const pres = new pptxgen();

// --- Configuration ---
const PAPER_TITLE = "{paper_title}";
const AUTHORS = "{authors}";
const DATE = "{date}";
const OUTPUT_PATH = "{output_path}";

// --- Theme ---
// Pick a palette that matches the paper's domain:
// - AI/ML papers: Midnight Executive or Ocean Gradient
// - Systems papers: Charcoal Minimal or Teal Trust
// - Biomedical: Forest & Moss or Sage Calm
const THEME = {
  primary: "1E2761",
  secondary: "CADCFC",
  accent: "E8913A",
  dark: "0D1B2A",
  light: "F7F9FC",
  text: "1A1A1A",
  lightText: "FFFFFF",
};

pres.defineLayout({ name: "WIDE", width: 13.33, height: 7.5 });
pres.layout = "WIDE";

// --- Slide Helpers ---

function titleSlide(title, subtitle) {
  const slide = pres.addSlide();
  slide.background = { color: THEME.dark };
  slide.addText(title, {
    x: 0.8, y: 2.0, w: 11.7, h: 1.5,
    fontSize: 36, fontFace: "Arial", color: THEME.lightText,
    bold: true, align: "center",
  });
  slide.addText(subtitle, {
    x: 0.8, y: 3.8, w: 11.7, h: 0.8,
    fontSize: 18, fontFace: "Arial", color: THEME.secondary,
    align: "center",
  });
  return slide;
}

function sectionDivider(sectionTitle) {
  const slide = pres.addSlide();
  slide.background = { color: THEME.primary };
  slide.addText(sectionTitle, {
    x: 0.8, y: 2.5, w: 11.7, h: 2.0,
    fontSize: 32, fontFace: "Arial", color: THEME.lightText,
    bold: true, align: "center",
  });
  return slide;
}

function contentSlide(title, bullets, opts = {}) {
  const slide = pres.addSlide();
  slide.background = { color: THEME.light };

  // Title bar
  slide.addShape(pres.ShapeType.rect, {
    x: 0, y: 0, w: 13.33, h: 1.0,
    fill: { color: THEME.primary },
  });
  slide.addText(title, {
    x: 0.5, y: 0.15, w: 12.3, h: 0.7,
    fontSize: 22, fontFace: "Arial", color: THEME.lightText, bold: true,
  });

  // Body content
  const bodyOpts = {
    x: 0.8, y: 1.3, w: 11.7, h: 5.5,
    fontSize: 16, fontFace: "Arial", color: THEME.text,
    valign: "top",
    ...opts,
  };

  if (Array.isArray(bullets)) {
    slide.addText(
      bullets.map(b => ({
        text: b,
        options: { bullet: true, breakLine: true, fontSize: 16 },
      })),
      bodyOpts
    );
  } else {
    slide.addText(bullets, bodyOpts);
  }

  return slide;
}

function twoColumnSlide(title, leftTitle, leftBullets, rightTitle, rightBullets) {
  const slide = pres.addSlide();
  slide.background = { color: THEME.light };

  slide.addShape(pres.ShapeType.rect, {
    x: 0, y: 0, w: 13.33, h: 1.0,
    fill: { color: THEME.primary },
  });
  slide.addText(title, {
    x: 0.5, y: 0.15, w: 12.3, h: 0.7,
    fontSize: 22, fontFace: "Arial", color: THEME.lightText, bold: true,
  });

  // Left column
  slide.addText(leftTitle, {
    x: 0.5, y: 1.2, w: 5.8, h: 0.5,
    fontSize: 18, fontFace: "Arial", color: THEME.primary, bold: true,
  });
  slide.addText(
    leftBullets.map(b => ({
      text: b, options: { bullet: true, breakLine: true, fontSize: 14 },
    })),
    { x: 0.5, y: 1.8, w: 5.8, h: 5.0, fontSize: 14, fontFace: "Arial", color: THEME.text, valign: "top" }
  );

  // Right column
  slide.addText(rightTitle, {
    x: 6.8, y: 1.2, w: 5.8, h: 0.5,
    fontSize: 18, fontFace: "Arial", color: THEME.accent, bold: true,
  });
  slide.addText(
    rightBullets.map(b => ({
      text: b, options: { bullet: true, breakLine: true, fontSize: 14 },
    })),
    { x: 6.8, y: 1.8, w: 5.8, h: 5.0, fontSize: 14, fontFace: "Arial", color: THEME.text, valign: "top" }
  );

  return slide;
}

function tableSlide(title, headers, rows) {
  const slide = pres.addSlide();
  slide.background = { color: THEME.light };

  slide.addShape(pres.ShapeType.rect, {
    x: 0, y: 0, w: 13.33, h: 1.0,
    fill: { color: THEME.primary },
  });
  slide.addText(title, {
    x: 0.5, y: 0.15, w: 12.3, h: 0.7,
    fontSize: 22, fontFace: "Arial", color: THEME.lightText, bold: true,
  });

  const tableData = [
    headers.map(h => ({ text: h, options: { bold: true, color: THEME.lightText, fontSize: 12 } })),
    ...rows.map(row => row.map(cell => ({ text: cell, options: { fontSize: 11 } }))),
  ];

  slide.addTable(tableData, {
    x: 0.5, y: 1.3, w: 12.3,
    border: { pt: 0.5, color: THEME.primary },
    colW: Array(headers.length).fill(12.3 / headers.length),
    rowH: Array(rows.length + 1).fill(0.4),
    autoPage: false,
    color: THEME.text,
    fontSize: 11,
    fontFace: "Arial",
    fill: { color: THEME.light },
    headerRow: { fill: { color: THEME.primary } },
  });

  return slide;
}

// --- Build Slides ---
// (Content is populated from the review and perspective markdowns)

// Section 1: Opening
titleSlide(PAPER_TITLE, `${AUTHORS}\n${DATE} | 논문 리뷰 및 분석`);

// ... build remaining slides using the helpers above,
// mapping content from review and perspective markdown files.

// Section 5: Closing
const closingSlide = pres.addSlide();
closingSlide.background = { color: THEME.dark };
closingSlide.addText("감사합니다", {
  x: 0.8, y: 2.5, w: 11.7, h: 2.0,
  fontSize: 40, fontFace: "Arial", color: THEME.lightText,
  bold: true, align: "center",
});
closingSlide.addText(`분석일: ${DATE}`, {
  x: 0.8, y: 4.5, w: 11.7, h: 0.8,
  fontSize: 16, fontFace: "Arial", color: THEME.secondary,
  align: "center",
});

// --- Save ---
pres.writeFile({ fileName: OUTPUT_PATH }).then(() => {
  console.log(`Presentation saved to ${OUTPUT_PATH}`);
});
```

## Slide Content Mapping

Map each section's content from the review/perspective markdown files to slides:

### 논문 리뷰 → 슬라이드

| 리뷰 섹션 | 슬라이드 유형 | 헬퍼 |
|-----------|-------------|------|
| 논문 정보 + 한줄 요약 | 콘텐츠 슬라이드 | `contentSlide()` |
| 문제 정의와 배경 | 콘텐츠 슬라이드 | `contentSlide()` |
| 핵심 아이디어 / 방법론 | 콘텐츠 슬라이드 (필요시 2장) | `contentSlide()` |
| 주요 기여점 | 번호 목록 슬라이드 | `contentSlide()` |
| 실험 설정 | 테이블 슬라이드 | `tableSlide()` |
| 주요 결과 | 테이블 슬라이드 | `tableSlide()` |
| Ablation Study | 테이블 슬라이드 | `tableSlide()` |
| 강점 vs 약점 | 2열 슬라이드 | `twoColumnSlide()` |
| 종합 평가 | 테이블 슬라이드 (점수) | `tableSlide()` |

### 관점 분석 → 슬라이드

| 관점 | 슬라이드 1 | 슬라이드 2 | 슬라이드 3 |
|------|-----------|-----------|-----------|
| PM 전략 | SWOT (2열) | 가치 제안 | 린 캔버스 |
| 시장 조사 | TAM/SAM/SOM | 경쟁 구도 (테이블) | 사용자 페르소나 |
| 제품 발견 | 가정 목록 (테이블) | 기회 솔루션 트리 | 실험 설계 |
| GTM | 전략 개요 | ICP | 비치헤드 세그먼트 |
| 통계 검토 | 엄밀성 평가 | 재현성 점수 (테이블) | - |
| 실행 계획 | 미니 PRD | 포지셔닝 | 북극성 지표 |

## Design Guidelines

- Use widescreen (13.33 x 7.5 inches)
- Dark backgrounds for divider slides, light backgrounds for content
- Consistent color bar at top of content slides
- No more than 6-8 bullet points per slide
- Tables: max 5-6 columns for readability
- Use bold/color for emphasis, not underlines
- Include slide numbers on content slides
- Each perspective section starts with a section divider slide
- Vary slide layouts: content, two-column, table, divider

## Key Constraints

- Install PptxGenJS: `npm install -g pptxgenjs`
- Use `writeFile()` for output, not `write()`
- Text alignment uses `margin: 0` for precision when needed
- Each slide should have visual variety — avoid repeating the same layout
- Content slides have a colored title bar at the top
- Limit text per slide: prefer concise bullet points over paragraphs
