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
  3.  목차 / 발표 순서 (agenda with section highlights)

섹션 2: 핵심 요약 (2-3 슬라이드)
  4.  주요 발견 사항 — 핵심 지표 카드 (keyMetricSlide)
  5.  평가 점수 테이블 (참신성, 건전성, 실험, 명확성, 영향력)
  6.  추천 요약 — 핵심 인용 (highlightSlide)

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
  muted: "6B7280",
  lightText: "FFFFFF",
  success: "16A34A",
  warning: "CA8A04",
  danger: "DC2626",
  cardBg: "FFFFFF",
};

// --- Layout: Standard 16:9 (10" x 5.625") ---
pres.layout = "LAYOUT_16x9";
const W = 10;      // slide width
const H = 5.625;   // slide height

// --- Slide counter for footer ---
let slideNum = 0;

// ============================================================
//  SLIDE FOOTER — adds slide number to every content slide
// ============================================================

function addFooter(slide) {
  slideNum++;
  slide.addText(slideNum.toString(), {
    x: W - 0.6, y: H - 0.4, w: 0.4, h: 0.3,
    fontSize: 9, fontFace: "Arial", color: THEME.muted, align: "right",
  });
}

// ============================================================
//  SLIDE HELPERS
// ============================================================

/**
 * Title slide — dark background, large centered title + subtitle.
 */
function titleSlide(title, subtitle) {
  const slide = pres.addSlide();
  slide.background = { color: THEME.dark };

  // Accent bar at bottom
  slide.addShape(pres.ShapeType.rect, {
    x: 0, y: H - 0.12, w: W, h: 0.12,
    fill: { color: THEME.accent },
  });

  slide.addText(title, {
    x: 0.8, y: 1.4, w: W - 1.6, h: 1.6,
    fontSize: 36, fontFace: "Arial", color: THEME.lightText,
    bold: true, align: "center", valign: "middle",
    shrinkText: true,
  });

  slide.addText(subtitle, {
    x: 0.8, y: 3.2, w: W - 1.6, h: 0.8,
    fontSize: 16, fontFace: "Arial", color: THEME.secondary,
    align: "center",
  });

  return slide;
}

/**
 * Section divider — colored background, centered section name.
 */
function sectionDivider(sectionTitle, sectionNumber) {
  const slide = pres.addSlide();
  slide.background = { color: THEME.primary };

  // Accent strip
  slide.addShape(pres.ShapeType.rect, {
    x: 0, y: 0, w: 0.12, h: H,
    fill: { color: THEME.accent },
  });

  if (sectionNumber) {
    slide.addText(sectionNumber, {
      x: 0.5, y: 1.2, w: W - 1.0, h: 0.8,
      fontSize: 48, fontFace: "Arial", color: THEME.accent,
      bold: true, align: "center",
    });
  }

  slide.addText(sectionTitle, {
    x: 0.5, y: sectionNumber ? 2.2 : 1.8, w: W - 1.0, h: 1.5,
    fontSize: 32, fontFace: "Arial", color: THEME.lightText,
    bold: true, align: "center", valign: "middle",
  });

  return slide;
}

/**
 * Content slide — accent strip left, title top, bullets body.
 * Max 5 bullets per slide. If more, split across slides.
 */
function contentSlide(title, bullets) {
  const slide = pres.addSlide();
  slide.background = { color: THEME.light };

  // Left accent strip
  slide.addShape(pres.ShapeType.rect, {
    x: 0, y: 0, w: 0.12, h: H,
    fill: { color: THEME.accent },
  });

  // Title
  slide.addText(title, {
    x: 0.5, y: 0.3, w: W - 1.0, h: 0.7,
    fontSize: 28, fontFace: "Arial", color: THEME.primary, bold: true,
  });

  // Divider under title
  slide.addShape(pres.ShapeType.rect, {
    x: 0.5, y: 1.05, w: 1.5, h: 0.03,
    fill: { color: THEME.accent },
  });

  // Bullet content
  if (Array.isArray(bullets)) {
    slide.addText(
      bullets.map(b => ({
        text: b,
        options: { bullet: { code: "2022" }, breakLine: true, fontSize: 18, lineSpacingMultiple: 1.4 },
      })),
      {
        x: 0.5, y: 1.3, w: W - 1.0, h: H - 1.9,
        fontSize: 18, fontFace: "Arial", color: THEME.text, valign: "top",
      }
    );
  } else {
    slide.addText(bullets, {
      x: 0.5, y: 1.3, w: W - 1.0, h: H - 1.9,
      fontSize: 18, fontFace: "Arial", color: THEME.text, valign: "top",
    });
  }

  addFooter(slide);
  return slide;
}

/**
 * Two-column slide — side-by-side content (e.g., strengths vs weaknesses).
 */
function twoColumnSlide(title, leftTitle, leftBullets, rightTitle, rightBullets) {
  const slide = pres.addSlide();
  slide.background = { color: THEME.light };

  // Left accent strip
  slide.addShape(pres.ShapeType.rect, {
    x: 0, y: 0, w: 0.12, h: H,
    fill: { color: THEME.accent },
  });

  // Title
  slide.addText(title, {
    x: 0.5, y: 0.3, w: W - 1.0, h: 0.7,
    fontSize: 28, fontFace: "Arial", color: THEME.primary, bold: true,
  });

  slide.addShape(pres.ShapeType.rect, {
    x: 0.5, y: 1.05, w: 1.5, h: 0.03,
    fill: { color: THEME.accent },
  });

  const colW = (W - 1.2) / 2;

  // Left column header
  slide.addText(leftTitle, {
    x: 0.5, y: 1.2, w: colW, h: 0.45,
    fontSize: 20, fontFace: "Arial", color: THEME.primary, bold: true,
  });
  slide.addText(
    leftBullets.map(b => ({
      text: b, options: { bullet: { code: "2022" }, breakLine: true, fontSize: 16, lineSpacingMultiple: 1.3 },
    })),
    { x: 0.5, y: 1.7, w: colW, h: H - 2.3, fontSize: 16, fontFace: "Arial", color: THEME.text, valign: "top" }
  );

  // Right column header
  slide.addText(rightTitle, {
    x: 0.5 + colW + 0.2, y: 1.2, w: colW, h: 0.45,
    fontSize: 20, fontFace: "Arial", color: THEME.accent, bold: true,
  });
  slide.addText(
    rightBullets.map(b => ({
      text: b, options: { bullet: { code: "2022" }, breakLine: true, fontSize: 16, lineSpacingMultiple: 1.3 },
    })),
    { x: 0.5 + colW + 0.2, y: 1.7, w: colW, h: H - 2.3, fontSize: 16, fontFace: "Arial", color: THEME.text, valign: "top" }
  );

  addFooter(slide);
  return slide;
}

/**
 * Table slide — styled data table with header row.
 */
function tableSlide(title, headers, rows) {
  const slide = pres.addSlide();
  slide.background = { color: THEME.light };

  // Left accent strip
  slide.addShape(pres.ShapeType.rect, {
    x: 0, y: 0, w: 0.12, h: H,
    fill: { color: THEME.accent },
  });

  // Title
  slide.addText(title, {
    x: 0.5, y: 0.3, w: W - 1.0, h: 0.7,
    fontSize: 28, fontFace: "Arial", color: THEME.primary, bold: true,
  });

  slide.addShape(pres.ShapeType.rect, {
    x: 0.5, y: 1.05, w: 1.5, h: 0.03,
    fill: { color: THEME.accent },
  });

  const tableW = W - 1.0;
  const tableData = [
    headers.map(h => ({
      text: h,
      options: { bold: true, color: THEME.lightText, fontSize: 14, fill: { color: THEME.primary } },
    })),
    ...rows.map((row, idx) => row.map(cell => ({
      text: cell,
      options: { fontSize: 13, fill: { color: idx % 2 === 0 ? THEME.light : THEME.cardBg } },
    }))),
  ];

  slide.addTable(tableData, {
    x: 0.5, y: 1.3, w: tableW,
    border: { pt: 0.5, color: THEME.primary },
    colW: Array(headers.length).fill(tableW / headers.length),
    color: THEME.text,
    fontSize: 13,
    fontFace: "Arial",
    margin: [4, 6, 4, 6],
  });

  addFooter(slide);
  return slide;
}

/**
 * Key metric slide — 3-4 large numbers displayed as cards.
 * Each metric: { value: "42%", label: "정확도 향상", color?: "16A34A" }
 */
function keyMetricSlide(title, metrics) {
  const slide = pres.addSlide();
  slide.background = { color: THEME.light };

  // Left accent strip
  slide.addShape(pres.ShapeType.rect, {
    x: 0, y: 0, w: 0.12, h: H,
    fill: { color: THEME.accent },
  });

  slide.addText(title, {
    x: 0.5, y: 0.3, w: W - 1.0, h: 0.7,
    fontSize: 28, fontFace: "Arial", color: THEME.primary, bold: true,
  });

  slide.addShape(pres.ShapeType.rect, {
    x: 0.5, y: 1.05, w: 1.5, h: 0.03,
    fill: { color: THEME.accent },
  });

  const count = metrics.length;
  const gap = 0.3;
  const totalGaps = gap * (count - 1);
  const availW = W - 1.0 - totalGaps;
  const cardW = availW / count;
  const cardH = 2.8;
  const startY = 1.5;

  metrics.forEach((m, i) => {
    const x = 0.5 + i * (cardW + gap);
    const metricColor = m.color || THEME.primary;

    // Card background
    slide.addShape(pres.ShapeType.roundRect, {
      x, y: startY, w: cardW, h: cardH,
      fill: { color: THEME.cardBg },
      shadow: { type: "outer", blur: 4, offset: 2, color: "D0D5DD", opacity: 0.3 },
      rectRadius: 0.1,
    });

    // Top accent line on card
    slide.addShape(pres.ShapeType.rect, {
      x: x + 0.1, y: startY, w: cardW - 0.2, h: 0.05,
      fill: { color: metricColor },
    });

    // Metric value
    slide.addText(m.value, {
      x, y: startY + 0.4, w: cardW, h: 1.2,
      fontSize: 40, fontFace: "Arial", color: metricColor,
      bold: true, align: "center", valign: "middle",
    });

    // Metric label
    slide.addText(m.label, {
      x, y: startY + 1.6, w: cardW, h: 0.8,
      fontSize: 14, fontFace: "Arial", color: THEME.muted,
      align: "center", valign: "top",
    });
  });

  addFooter(slide);
  return slide;
}

/**
 * Highlight/quote slide — large centered quote with source attribution.
 */
function highlightSlide(title, quote, source) {
  const slide = pres.addSlide();
  slide.background = { color: THEME.dark };

  slide.addText(title, {
    x: 0.5, y: 0.3, w: W - 1.0, h: 0.6,
    fontSize: 20, fontFace: "Arial", color: THEME.secondary, bold: true,
  });

  // Quote mark
  slide.addText("\u201C", {
    x: 0.8, y: 1.0, w: 1.0, h: 1.0,
    fontSize: 72, fontFace: "Georgia", color: THEME.accent, bold: true,
  });

  // Quote text
  slide.addText(quote, {
    x: 1.0, y: 1.6, w: W - 2.0, h: 2.2,
    fontSize: 22, fontFace: "Arial", color: THEME.lightText,
    italic: true, align: "center", valign: "middle",
    lineSpacingMultiple: 1.4,
  });

  // Source
  if (source) {
    slide.addText(`\u2014 ${source}`, {
      x: 1.0, y: 4.0, w: W - 2.0, h: 0.5,
      fontSize: 14, fontFace: "Arial", color: THEME.muted, align: "center",
    });
  }

  // Bottom accent bar
  slide.addShape(pres.ShapeType.rect, {
    x: 0, y: H - 0.08, w: W, h: 0.08,
    fill: { color: THEME.accent },
  });

  return slide;
}

/**
 * Icon bullet slide — bullets with colored circle markers.
 * items: [{ icon: "01", text: "설명 텍스트" }, ...]
 */
function iconBulletSlide(title, items) {
  const slide = pres.addSlide();
  slide.background = { color: THEME.light };

  // Left accent strip
  slide.addShape(pres.ShapeType.rect, {
    x: 0, y: 0, w: 0.12, h: H,
    fill: { color: THEME.accent },
  });

  slide.addText(title, {
    x: 0.5, y: 0.3, w: W - 1.0, h: 0.7,
    fontSize: 28, fontFace: "Arial", color: THEME.primary, bold: true,
  });

  slide.addShape(pres.ShapeType.rect, {
    x: 0.5, y: 1.05, w: 1.5, h: 0.03,
    fill: { color: THEME.accent },
  });

  const startY = 1.3;
  const rowH = 0.7;

  items.forEach((item, i) => {
    const y = startY + i * rowH;

    // Circle with number
    slide.addShape(pres.ShapeType.ellipse, {
      x: 0.6, y: y + 0.08, w: 0.45, h: 0.45,
      fill: { color: THEME.primary },
    });
    slide.addText(item.icon || (i + 1).toString(), {
      x: 0.6, y: y + 0.08, w: 0.45, h: 0.45,
      fontSize: 14, fontFace: "Arial", color: THEME.lightText,
      bold: true, align: "center", valign: "middle",
    });

    // Text
    slide.addText(item.text, {
      x: 1.2, y: y, w: W - 1.8, h: rowH,
      fontSize: 18, fontFace: "Arial", color: THEME.text, valign: "middle",
    });
  });

  addFooter(slide);
  return slide;
}

/**
 * Comparison slide — side-by-side cards for comparing two approaches.
 */
function comparisonSlide(title, left, right) {
  const slide = pres.addSlide();
  slide.background = { color: THEME.light };

  // Left accent strip
  slide.addShape(pres.ShapeType.rect, {
    x: 0, y: 0, w: 0.12, h: H,
    fill: { color: THEME.accent },
  });

  slide.addText(title, {
    x: 0.5, y: 0.3, w: W - 1.0, h: 0.7,
    fontSize: 28, fontFace: "Arial", color: THEME.primary, bold: true,
  });

  slide.addShape(pres.ShapeType.rect, {
    x: 0.5, y: 1.05, w: 1.5, h: 0.03,
    fill: { color: THEME.accent },
  });

  const cardW = (W - 1.4) / 2;
  const cardH = H - 1.7;

  // Left card
  slide.addShape(pres.ShapeType.roundRect, {
    x: 0.5, y: 1.3, w: cardW, h: cardH,
    fill: { color: THEME.cardBg },
    shadow: { type: "outer", blur: 3, offset: 1, color: "D0D5DD", opacity: 0.3 },
    rectRadius: 0.08,
  });
  slide.addShape(pres.ShapeType.rect, {
    x: 0.5, y: 1.3, w: cardW, h: 0.05,
    fill: { color: THEME.primary },
  });
  slide.addText(left.title, {
    x: 0.7, y: 1.45, w: cardW - 0.4, h: 0.5,
    fontSize: 20, fontFace: "Arial", color: THEME.primary, bold: true,
  });
  slide.addText(
    left.items.map(b => ({
      text: b, options: { bullet: { code: "2022" }, breakLine: true, fontSize: 16, lineSpacingMultiple: 1.3 },
    })),
    { x: 0.7, y: 2.0, w: cardW - 0.4, h: cardH - 1.0, fontSize: 16, fontFace: "Arial", color: THEME.text, valign: "top" }
  );

  // Right card
  const rx = 0.5 + cardW + 0.4;
  slide.addShape(pres.ShapeType.roundRect, {
    x: rx, y: 1.3, w: cardW, h: cardH,
    fill: { color: THEME.cardBg },
    shadow: { type: "outer", blur: 3, offset: 1, color: "D0D5DD", opacity: 0.3 },
    rectRadius: 0.08,
  });
  slide.addShape(pres.ShapeType.rect, {
    x: rx, y: 1.3, w: cardW, h: 0.05,
    fill: { color: THEME.accent },
  });
  slide.addText(right.title, {
    x: rx + 0.2, y: 1.45, w: cardW - 0.4, h: 0.5,
    fontSize: 20, fontFace: "Arial", color: THEME.accent, bold: true,
  });
  slide.addText(
    right.items.map(b => ({
      text: b, options: { bullet: { code: "2022" }, breakLine: true, fontSize: 16, lineSpacingMultiple: 1.3 },
    })),
    { x: rx + 0.2, y: 2.0, w: cardW - 0.4, h: cardH - 1.0, fontSize: 16, fontFace: "Arial", color: THEME.text, valign: "top" }
  );

  addFooter(slide);
  return slide;
}

/**
 * Agenda slide — visual table of contents with highlighted active section.
 * sections: ["핵심 요약", "논문 리뷰", "PM 분석", ...]
 * activeIndex: 0-based index of highlighted section (-1 for overview)
 */
function agendaSlide(sections, activeIndex) {
  const slide = pres.addSlide();
  slide.background = { color: THEME.light };

  slide.addText("발표 순서", {
    x: 0.5, y: 0.3, w: W - 1.0, h: 0.7,
    fontSize: 28, fontFace: "Arial", color: THEME.primary, bold: true,
  });

  slide.addShape(pres.ShapeType.rect, {
    x: 0.5, y: 1.05, w: 1.5, h: 0.03,
    fill: { color: THEME.accent },
  });

  const startY = 1.3;
  const itemH = 0.6;

  sections.forEach((s, i) => {
    const isActive = i === activeIndex;
    const y = startY + i * itemH;

    // Number circle
    slide.addShape(pres.ShapeType.ellipse, {
      x: 0.6, y: y + 0.08, w: 0.4, h: 0.4,
      fill: { color: isActive ? THEME.accent : THEME.primary },
    });
    slide.addText((i + 1).toString(), {
      x: 0.6, y: y + 0.08, w: 0.4, h: 0.4,
      fontSize: 14, fontFace: "Arial", color: THEME.lightText,
      bold: true, align: "center", valign: "middle",
    });

    // Section name
    slide.addText(s, {
      x: 1.2, y: y, w: W - 2.0, h: itemH,
      fontSize: isActive ? 20 : 18,
      fontFace: "Arial",
      color: isActive ? THEME.primary : THEME.muted,
      bold: isActive,
      valign: "middle",
    });
  });

  addFooter(slide);
  return slide;
}

// ============================================================
//  BUILD SLIDES
// ============================================================

// Section 1: Opening
titleSlide(PAPER_TITLE, `${AUTHORS}\n${DATE} | 논문 리뷰 및 분석`);

// ... build paper overview slide using contentSlide()

const AGENDA_SECTIONS = [
  "핵심 요약", "논문 리뷰", "PM 전략 분석",
  "시장 조사", "제품 발견", "GTM 분석",
  "통계 검토", "실행 계획",
];
agendaSlide(AGENDA_SECTIONS, -1);

// ... build remaining slides using the helpers above,
// mapping content from review and perspective markdown files.
//
// Use the Slide Content Mapping table below to pick the right
// helper for each section.

// Section 5: Closing
const closingSlide = pres.addSlide();
closingSlide.background = { color: THEME.dark };
closingSlide.addShape(pres.ShapeType.rect, {
  x: 0, y: H - 0.08, w: W, h: 0.08,
  fill: { color: THEME.accent },
});
closingSlide.addText("감사합니다", {
  x: 0.8, y: 1.8, w: W - 1.6, h: 1.5,
  fontSize: 40, fontFace: "Arial", color: THEME.lightText,
  bold: true, align: "center",
});
closingSlide.addText(`분석일: ${DATE}  |  ThakiCloud Research`, {
  x: 0.8, y: 3.5, w: W - 1.6, h: 0.6,
  fontSize: 14, fontFace: "Arial", color: THEME.secondary,
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
| 주요 발견 수치 (성능, 비용 등) | 핵심 지표 카드 | `keyMetricSlide()` |
| 논문 정보 + 한줄 요약 | 콘텐츠 슬라이드 | `contentSlide()` |
| 문제 정의와 배경 | 콘텐츠 슬라이드 | `contentSlide()` |
| 핵심 아이디어 / 방법론 | 콘텐츠 슬라이드 (필요시 2장) | `contentSlide()` |
| 주요 기여점 | 번호 아이콘 슬라이드 | `iconBulletSlide()` |
| 실험 설정 | 테이블 슬라이드 | `tableSlide()` |
| 주요 결과 | 테이블 슬라이드 | `tableSlide()` |
| Ablation Study | 테이블 슬라이드 | `tableSlide()` |
| 강점 vs 약점 | 비교 슬라이드 | `comparisonSlide()` |
| 핵심 인용/발견 | 하이라이트 슬라이드 | `highlightSlide()` |
| 종합 평가 | 테이블 슬라이드 (점수) | `tableSlide()` |

### 관점 분석 → 슬라이드

| 관점 | 슬라이드 1 | 슬라이드 2 | 슬라이드 3 |
|------|-----------|-----------|-----------|
| PM 전략 | SWOT (비교) `comparisonSlide()` | 가치 제안 `contentSlide()` | 린 캔버스 `tableSlide()` |
| 시장 조사 | TAM/SAM/SOM `keyMetricSlide()` | 경쟁 구도 `tableSlide()` | 사용자 페르소나 `contentSlide()` |
| 제품 발견 | 가정 목록 `tableSlide()` | 기회 솔루션 트리 `iconBulletSlide()` | 실험 설계 `contentSlide()` |
| GTM | 전략 개요 `contentSlide()` | ICP `contentSlide()` | 비치헤드 세그먼트 `contentSlide()` |
| 통계 검토 | 엄밀성 평가 `contentSlide()` | 재현성 점수 `tableSlide()` | — |
| 실행 계획 | 미니 PRD `contentSlide()` | 포지셔닝 `highlightSlide()` | 북극성 지표 `keyMetricSlide()` |

## Content Density Rules (MANDATORY)

These rules prevent the "small text in vast empty space" problem:

1. **Max 5 bullets per slide** — if more than 5, split into multiple slides
   with "(1/2)", "(2/2)" suffixes on the title
2. **Each bullet max 2 lines** — rewrite verbose bullets into concise statements
3. **Table max 6 data rows per slide** — use `autoPage: true` for overflow
4. **No text-only slides** — every content slide must have at least one visual
   element (accent strip, metric card, colored header, or icon)
5. **Font size minimums**: body text 16pt, titles 28pt, table cells 13pt
6. **Vary layouts**: never use the same helper for more than 3 consecutive slides

## Design Guidelines

- Use 16:9 standard layout (10 x 5.625 inches) — NOT widescreen LAYOUT_WIDE
- Dark backgrounds for title/divider/highlight slides, light for content
- Left accent strip (0.12" wide) on all content slides for visual continuity
- Short accent underline (1.5" wide) below content slide titles
- Slide numbers on all content slides (bottom-right)
- Each perspective section starts with a `sectionDivider()` slide
- Use `keyMetricSlide()` for any slide with 3-4 numeric data points
- Use `highlightSlide()` for impactful one-line findings or quotes
- Use `comparisonSlide()` instead of `twoColumnSlide()` when comparing pros/cons
- Use `iconBulletSlide()` for ordered lists of key points (contributions, steps)

## Helper Quick Reference

| Helper | Best For | Visual Style |
|--------|----------|-------------|
| `titleSlide()` | Opening slide | Dark bg, centered, accent bar |
| `sectionDivider()` | Section transitions | Colored bg, section number |
| `contentSlide()` | General bullets | Light bg, accent strip, 18pt |
| `twoColumnSlide()` | Side-by-side lists | Light bg, two text areas |
| `tableSlide()` | Tabular data | Light bg, styled table, 13pt |
| `keyMetricSlide()` | 3-4 big numbers | Rounded cards with shadows |
| `highlightSlide()` | Key quote/finding | Dark bg, large italic text |
| `iconBulletSlide()` | Numbered key points | Circle icons with text |
| `comparisonSlide()` | A vs B comparison | Two rounded cards |
| `agendaSlide()` | Table of contents | Numbered list, highlight |

## Key Constraints

- Layout: `LAYOUT_16x9` (10 x 5.625 inches) — do NOT use LAYOUT_WIDE
- Install PptxGenJS: `npm install -g pptxgenjs`
- Use `writeFile()` for output, not `write()`
- Hex colors without `#` prefix (e.g., `"1E2761"` not `"#1E2761"`)
- Do NOT reuse shadow objects — create fresh objects per call
- Do NOT use `ROUNDED_RECTANGLE` with accent overlay — use `roundRect`
- Do NOT use `headerRow`, `autoPage`, or `autoPageRepeatHeader` in table options — apply fill per-cell instead
- Each slide must have visual variety — avoid repeating the same layout
- Content slides must use 18pt body text minimum
- Table cells must use 13pt minimum
- `shrinkText: true` on title slides to prevent overflow
