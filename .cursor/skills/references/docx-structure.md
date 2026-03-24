# DOCX Assembly Instructions

**Language rule**: All document text, headings, labels, and section titles MUST
be written in Korean. English is only allowed for proper nouns and technical
terminology that has no standard Korean equivalent.

Generate the consolidated Word document using Node.js `docx` package following
the `anthropic-docx` skill patterns.

## Document Structure

```
1. 표지 (Cover Page) — accent bar, 논문 제목, 저자, 분석일
2. 목차
3. 핵심 요약 (2-3 pages, 구체적 수치 포함)
4. 논문 리뷰 (Phase 2 전체 출력)
5. PM 전략 분석
6. 시장 조사 분석
7. 제품 발견 분석
8. GTM 분석
9. 통계/방법론 검토
10. 실행 계획
11. 부록
```

## Script Template

Write a Node.js script to `/tmp/paper-review-docx.js` and execute it.

```javascript
const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  Header, Footer, AlignmentType, LevelFormat,
  TableOfContents, HeadingLevel, BorderStyle, WidthType, ShadingType,
  PageBreak, PageNumber, TabStopType, TabStopPosition
} = require("docx");

// --- Configuration ---
const PAPER_TITLE = "{paper_title}";
const AUTHORS = "{authors}";
const DATE = "{date}";
const OUTPUT_PATH = "{output_path}";

// --- Color Palette ---
const COLORS = {
  primary: "1E3A5F",
  secondary: "2C5F8A",
  accent: "E8913A",
  lightBg: "F0F4F8",
  lightBg2: "F8FAFC",
  darkText: "1A1A1A",
  mutedText: "555555",
  lightText: "FFFFFF",
  border: "D0D5DD",
  headerBg: "1E3A5F",
  success: "16A34A",
  warning: "CA8A04",
  danger: "DC2626",
  calloutBg: "EFF6FF",
  calloutBorder: "2C5F8A",
  codeBg: "F9F2F4",
  codeText: "C7254E",
};

// --- DXA Constants ---
const PAGE_WIDTH = 12240;
const PAGE_HEIGHT = 15840;
const MARGIN = 1440;
const CONTENT_WIDTH = PAGE_WIDTH - (MARGIN * 2); // 9360

// --- Border Presets ---
const thinBorder = { style: BorderStyle.SINGLE, size: 1, color: COLORS.border };
const borders = { top: thinBorder, bottom: thinBorder, left: thinBorder, right: thinBorder };
const noBorder = { style: BorderStyle.NONE, size: 0, color: "FFFFFF" };
const noBorders = { top: noBorder, bottom: noBorder, left: noBorder, right: noBorder };
const accentLeftBorder = { style: BorderStyle.SINGLE, size: 6, color: COLORS.accent };

// ============================================================
//  MARKDOWN INLINE PARSER
//  Converts **bold**, *italic*, `code` within a single line
//  into an array of properly styled TextRun objects.
// ============================================================

function parseInlineMarkdown(text) {
  const runs = [];
  // Match: **bold**, *italic*, `code`, or plain text
  const regex = /(\*\*(.+?)\*\*|\*(.+?)\*|`(.+?)`|([^*`]+))/g;
  let match;
  while ((match = regex.exec(text)) !== null) {
    if (match[2]) {
      // **bold**
      runs.push(new TextRun({
        text: match[2], bold: true, font: "Arial", size: 22,
      }));
    } else if (match[3]) {
      // *italic*
      runs.push(new TextRun({
        text: match[3], italics: true, font: "Arial", size: 22,
      }));
    } else if (match[4]) {
      // `inline code`
      runs.push(new TextRun({
        text: match[4], font: "Consolas", size: 20,
        color: COLORS.codeText,
        shading: { fill: COLORS.codeBg, type: ShadingType.CLEAR },
      }));
    } else if (match[5]) {
      // plain text
      runs.push(new TextRun({
        text: match[5], font: "Arial", size: 22,
      }));
    }
  }
  if (runs.length === 0) {
    runs.push(new TextRun({ text: text || "", font: "Arial", size: 22 }));
  }
  return runs;
}

// ============================================================
//  BASIC ELEMENT HELPERS
// ============================================================

function heading(level, text) {
  return new Paragraph({
    heading: level,
    children: [new TextRun({ text, font: "Arial" })],
  });
}

function bodyParagraph(text) {
  return new Paragraph({
    spacing: { after: 120, line: 276 },
    children: parseInlineMarkdown(text),
  });
}

function bulletItem(text, level = 0, reference = "bullets") {
  return new Paragraph({
    numbering: { reference, level },
    spacing: { after: 60, line: 276 },
    children: parseInlineMarkdown(text),
  });
}

function numberedItem(text, level = 0) {
  return new Paragraph({
    numbering: { reference: "numbers", level },
    spacing: { after: 60, line: 276 },
    children: parseInlineMarkdown(text),
  });
}

function blockquote(text) {
  return new Paragraph({
    spacing: { after: 120, line: 276 },
    indent: { left: 480 },
    border: { left: { style: BorderStyle.SINGLE, size: 4, color: COLORS.secondary, space: 8 } },
    children: [new TextRun({
      text, font: "Arial", size: 22, italics: true, color: COLORS.mutedText,
    })],
  });
}

function pageBreak() {
  return new Paragraph({ children: [new PageBreak()] });
}

// ============================================================
//  VISUAL DESIGN HELPERS
// ============================================================

/**
 * Colored callout box with accent left border and tinted background.
 * Use for key insights, important findings, or recommendations.
 */
function calloutBox(title, bodyLines, accentColor = COLORS.accent) {
  const children = [];
  if (title) {
    children.push(new Paragraph({
      spacing: { after: 80 },
      children: [new TextRun({
        text: title, font: "Arial", size: 22, bold: true, color: accentColor,
      })],
    }));
  }
  bodyLines.forEach(line => {
    children.push(new Paragraph({
      spacing: { after: 60 },
      children: parseInlineMarkdown(line),
    }));
  });

  const bgFill = accentColor === COLORS.accent ? "FEF3E2"
               : accentColor === COLORS.secondary ? COLORS.calloutBg
               : accentColor === COLORS.success ? "F0FDF4"
               : accentColor === COLORS.danger ? "FEF2F2"
               : COLORS.lightBg;

  return new Table({
    width: { size: CONTENT_WIDTH, type: WidthType.DXA },
    columnWidths: [CONTENT_WIDTH],
    rows: [new TableRow({
      children: [new TableCell({
        width: { size: CONTENT_WIDTH, type: WidthType.DXA },
        borders: {
          top: noBorder, bottom: noBorder, right: noBorder,
          left: { style: BorderStyle.SINGLE, size: 8, color: accentColor },
        },
        shading: { fill: bgFill, type: ShadingType.CLEAR },
        margins: { top: 120, bottom: 120, left: 200, right: 200 },
        children,
      })],
    })],
  });
}

/**
 * Key findings panel — numbered items with accent highlight.
 */
function keyFindingPanel(title, items) {
  const children = [
    new Paragraph({
      spacing: { after: 120 },
      children: [new TextRun({
        text: title, font: "Arial", size: 26, bold: true, color: COLORS.primary,
      })],
    }),
  ];
  items.forEach((item, i) => {
    children.push(new Paragraph({
      spacing: { after: 80, line: 276 },
      children: [
        new TextRun({
          text: `${i + 1}. `, font: "Arial", size: 22, bold: true, color: COLORS.accent,
        }),
        ...parseInlineMarkdown(item),
      ],
    }));
  });
  return new Table({
    width: { size: CONTENT_WIDTH, type: WidthType.DXA },
    columnWidths: [CONTENT_WIDTH],
    rows: [new TableRow({
      children: [new TableCell({
        width: { size: CONTENT_WIDTH, type: WidthType.DXA },
        borders: {
          top: { style: BorderStyle.SINGLE, size: 2, color: COLORS.primary },
          bottom: { style: BorderStyle.SINGLE, size: 2, color: COLORS.primary },
          left: noBorder, right: noBorder,
        },
        shading: { fill: COLORS.lightBg, type: ShadingType.CLEAR },
        margins: { top: 160, bottom: 160, left: 200, right: 200 },
        children,
      })],
    })],
  });
}

/**
 * Section divider — page break + styled section heading with decorative
 * bottom border line.
 */
function sectionDivider(title) {
  return [
    pageBreak(),
    new Paragraph({
      spacing: { after: 200 },
      border: { bottom: { style: BorderStyle.SINGLE, size: 3, color: COLORS.accent, space: 8 } },
      children: [new TextRun({
        text: title, font: "Arial", size: 36, bold: true, color: COLORS.primary,
      })],
    }),
  ];
}

/**
 * Score table with conditional color coding.
 * Each row: [criteria, score(string), notes]
 * Score colors: 4-5 → green, 3 → yellow, 1-2 → red
 */
function scoreTable(title, rows) {
  function scoreColor(scoreStr) {
    const n = parseFloat(scoreStr);
    if (n >= 4) return COLORS.success;
    if (n >= 3) return COLORS.warning;
    return COLORS.danger;
  }

  const colWidths = [3600, 1400, 4360];
  const headerRow = new TableRow({
    children: ["평가 기준", "점수", "비고"].map((h, i) => new TableCell({
      borders,
      width: { size: colWidths[i], type: WidthType.DXA },
      shading: { fill: COLORS.headerBg, type: ShadingType.CLEAR },
      margins: { top: 80, bottom: 80, left: 120, right: 120 },
      children: [new Paragraph({
        children: [new TextRun({ text: h, bold: true, color: COLORS.lightText, font: "Arial", size: 20 })],
      })],
    })),
  });

  const dataRows = rows.map((row, rowIdx) => new TableRow({
    children: row.map((cell, colIdx) => {
      const isScore = colIdx === 1;
      const textColor = isScore ? scoreColor(cell) : COLORS.darkText;
      return new TableCell({
        borders,
        width: { size: colWidths[colIdx], type: WidthType.DXA },
        shading: {
          fill: rowIdx % 2 === 0 ? COLORS.lightBg2 : "FFFFFF",
          type: ShadingType.CLEAR,
        },
        margins: { top: 80, bottom: 80, left: 120, right: 120 },
        children: [new Paragraph({
          children: [new TextRun({
            text: cell, font: "Arial", size: 20,
            bold: isScore, color: textColor,
          })],
        })],
      });
    }),
  }));

  const elements = [];
  if (title) {
    elements.push(new Paragraph({
      spacing: { before: 200, after: 120 },
      children: [new TextRun({ text: title, font: "Arial", size: 26, bold: true, color: COLORS.primary })],
    }));
  }
  elements.push(new Table({
    width: { size: CONTENT_WIDTH, type: WidthType.DXA },
    columnWidths: colWidths,
    rows: [headerRow, ...dataRows],
  }));
  return elements;
}

// ============================================================
//  TABLE HELPER (enhanced with alternating rows + padding)
// ============================================================

function markdownTableToDocx(headers, rows) {
  const colCount = headers.length;
  const colWidth = Math.floor(CONTENT_WIDTH / colCount);

  const headerRow = new TableRow({
    children: headers.map(h => new TableCell({
      borders,
      width: { size: colWidth, type: WidthType.DXA },
      shading: { fill: COLORS.headerBg, type: ShadingType.CLEAR },
      margins: { top: 100, bottom: 100, left: 150, right: 150 },
      children: [new Paragraph({
        children: [new TextRun({ text: h, bold: true, color: COLORS.lightText, font: "Arial", size: 20 })],
      })],
    })),
  });

  const dataRows = rows.map((row, rowIdx) => new TableRow({
    children: row.map(cell => new TableCell({
      borders,
      width: { size: colWidth, type: WidthType.DXA },
      shading: {
        fill: rowIdx % 2 === 0 ? COLORS.lightBg2 : "FFFFFF",
        type: ShadingType.CLEAR,
      },
      margins: { top: 100, bottom: 100, left: 150, right: 150 },
      children: [new Paragraph({
        children: parseInlineMarkdown(cell),
      })],
    })),
  }));

  return new Table({
    width: { size: CONTENT_WIDTH, type: WidthType.DXA },
    columnWidths: Array(colCount).fill(colWidth),
    rows: [headerRow, ...dataRows],
  });
}

// ============================================================
//  FULL MARKDOWN BLOCK PARSER
//  Converts an entire markdown string into an array of docx
//  elements (Paragraph, Table, etc.). Handles headings, lists,
//  blockquotes, tables, horizontal rules, and inline formatting.
// ============================================================

function convertMarkdownToDocx(markdownText) {
  const lines = markdownText.split("\n");
  const elements = [];
  let i = 0;

  while (i < lines.length) {
    const line = lines[i];
    const trimmed = line.trim();

    // Skip empty lines
    if (trimmed === "") { i++; continue; }

    // --- Horizontal rule → page break ---
    if (/^-{3,}$/.test(trimmed) || /^\*{3,}$/.test(trimmed)) {
      elements.push(pageBreak());
      i++;
      continue;
    }

    // --- Headings ---
    const headingMatch = trimmed.match(/^(#{1,3})\s+(.+)/);
    if (headingMatch) {
      const level = headingMatch[1].length;
      const headingLevel = level === 1 ? HeadingLevel.HEADING_1
                         : level === 2 ? HeadingLevel.HEADING_2
                         : HeadingLevel.HEADING_3;
      elements.push(heading(headingLevel, headingMatch[2]));
      i++;
      continue;
    }

    // --- Blockquote ---
    if (trimmed.startsWith("> ")) {
      const quoteText = trimmed.replace(/^>\s*/, "");
      elements.push(blockquote(quoteText));
      i++;
      continue;
    }

    // --- Unordered list ---
    if (/^[-*]\s+/.test(trimmed)) {
      const itemText = trimmed.replace(/^[-*]\s+/, "");
      elements.push(bulletItem(itemText));
      i++;
      continue;
    }

    // --- Ordered list ---
    const orderedMatch = trimmed.match(/^(\d+)\.\s+(.+)/);
    if (orderedMatch) {
      elements.push(numberedItem(orderedMatch[2]));
      i++;
      continue;
    }

    // --- Pipe table ---
    if (trimmed.startsWith("|") && trimmed.endsWith("|")) {
      const tableLines = [];
      while (i < lines.length && lines[i].trim().startsWith("|") && lines[i].trim().endsWith("|")) {
        tableLines.push(lines[i].trim());
        i++;
      }
      // Parse: first row = headers, second row = separator (skip), rest = data
      if (tableLines.length >= 2) {
        const parseRow = (row) =>
          row.split("|").filter((_, idx, arr) => idx > 0 && idx < arr.length - 1)
             .map(cell => cell.trim());
        const headers = parseRow(tableLines[0]);
        const dataRows = tableLines.slice(2).map(parseRow);
        elements.push(new Paragraph({ spacing: { before: 120 } }));
        elements.push(markdownTableToDocx(headers, dataRows));
        elements.push(new Paragraph({ spacing: { after: 120 } }));
      }
      continue;
    }

    // --- Regular paragraph (with inline formatting) ---
    elements.push(bodyParagraph(trimmed));
    i++;
  }

  return elements;
}

// ============================================================
//  PAGE PROPERTIES (reusable)
// ============================================================

const pageProps = {
  page: {
    size: { width: PAGE_WIDTH, height: PAGE_HEIGHT },
    margin: { top: MARGIN, right: MARGIN, bottom: MARGIN, left: MARGIN },
  },
};

const defaultHeader = new Header({
  children: [
    new Paragraph({
      border: { bottom: { style: BorderStyle.SINGLE, size: 1, color: COLORS.border, space: 4 } },
      children: [
        new TextRun({ text: PAPER_TITLE, font: "Arial", size: 16, color: COLORS.mutedText, italics: true }),
      ],
    }),
  ],
});

const defaultFooter = new Footer({
  children: [
    new Paragraph({
      alignment: AlignmentType.CENTER,
      children: [
        new TextRun({ children: [PageNumber.CURRENT], font: "Arial", size: 18, color: COLORS.mutedText }),
      ],
    }),
  ],
});

// ============================================================
//  CONTENT SECTIONS — read markdown files and convert
// ============================================================

// Read all markdown source files
const reviewMd = fs.readFileSync("{review_md_path}", "utf-8");
const pmStrategyMd = fs.readFileSync("{pm_strategy_md_path}", "utf-8");
const marketResearchMd = fs.readFileSync("{market_research_md_path}", "utf-8");
const discoveryMd = fs.readFileSync("{discovery_md_path}", "utf-8");
const gtmMd = fs.readFileSync("{gtm_md_path}", "utf-8");
const statisticsMd = fs.readFileSync("{statistics_md_path}", "utf-8");
const executionMd = fs.readFileSync("{execution_md_path}", "utf-8");

// ============================================================
//  BUILD DOCUMENT
// ============================================================

const doc = new Document({
  styles: {
    default: {
      document: {
        run: { font: "Arial", size: 22, color: COLORS.darkText },
        paragraph: { spacing: { line: 276 } },
      },
    },
    paragraphStyles: [
      {
        id: "Heading1", name: "Heading 1",
        basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 36, bold: true, font: "Arial", color: COLORS.primary },
        paragraph: { spacing: { before: 360, after: 240 }, outlineLevel: 0 },
      },
      {
        id: "Heading2", name: "Heading 2",
        basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 30, bold: true, font: "Arial", color: COLORS.secondary },
        paragraph: { spacing: { before: 280, after: 180 }, outlineLevel: 1 },
      },
      {
        id: "Heading3", name: "Heading 3",
        basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 26, bold: true, font: "Arial", color: COLORS.darkText },
        paragraph: { spacing: { before: 200, after: 120 }, outlineLevel: 2 },
      },
    ],
  },
  numbering: {
    config: [
      {
        reference: "bullets",
        levels: [
          {
            level: 0, format: LevelFormat.BULLET, text: "\u2022",
            alignment: AlignmentType.LEFT,
            style: { paragraph: { indent: { left: 720, hanging: 360 } } },
          },
          {
            level: 1, format: LevelFormat.BULLET, text: "\u25E6",
            alignment: AlignmentType.LEFT,
            style: { paragraph: { indent: { left: 1440, hanging: 360 } } },
          },
        ],
      },
      {
        reference: "numbers",
        levels: [
          {
            level: 0, format: LevelFormat.DECIMAL, text: "%1.",
            alignment: AlignmentType.LEFT,
            style: { paragraph: { indent: { left: 720, hanging: 360 } } },
          },
          {
            level: 1, format: LevelFormat.LOWER_LETTER, text: "%2)",
            alignment: AlignmentType.LEFT,
            style: { paragraph: { indent: { left: 1440, hanging: 360 } } },
          },
        ],
      },
    ],
  },
  sections: [
    // =========================
    //  COVER PAGE
    // =========================
    {
      properties: { ...pageProps },
      children: [
        // Accent bar at top (via borderless table)
        new Table({
          width: { size: CONTENT_WIDTH, type: WidthType.DXA },
          columnWidths: [CONTENT_WIDTH],
          rows: [new TableRow({
            height: { value: 200, rule: "exact" },
            children: [new TableCell({
              width: { size: CONTENT_WIDTH, type: WidthType.DXA },
              borders: noBorders,
              shading: { fill: COLORS.accent, type: ShadingType.CLEAR },
              children: [new Paragraph({ children: [] })],
            })],
          })],
        }),

        new Paragraph({ spacing: { before: 2400 } }),

        // Document type label
        new Paragraph({
          alignment: AlignmentType.CENTER,
          spacing: { after: 400 },
          children: [new TextRun({
            text: "논문 리뷰 및 분석 보고서",
            font: "Arial", size: 28, color: COLORS.mutedText,
            allCaps: true,
          })],
        }),

        // Paper title
        new Paragraph({
          alignment: AlignmentType.CENTER,
          spacing: { after: 300 },
          children: [new TextRun({
            text: PAPER_TITLE,
            font: "Arial", size: 48, bold: true, color: COLORS.primary,
          })],
        }),

        // Divider line
        new Table({
          width: { size: 3000, type: WidthType.DXA },
          columnWidths: [3000],
          rows: [new TableRow({
            height: { value: 30, rule: "exact" },
            children: [new TableCell({
              width: { size: 3000, type: WidthType.DXA },
              borders: noBorders,
              shading: { fill: COLORS.accent, type: ShadingType.CLEAR },
              children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [] })],
            })],
          })],
        }),

        new Paragraph({ spacing: { after: 600 } }),

        // Authors
        new Paragraph({
          alignment: AlignmentType.CENTER,
          spacing: { after: 200 },
          children: [new TextRun({
            text: AUTHORS,
            font: "Arial", size: 24, color: COLORS.darkText,
          })],
        }),

        // Date
        new Paragraph({
          alignment: AlignmentType.CENTER,
          spacing: { after: 200 },
          children: [new TextRun({
            text: `분석일: ${DATE}`,
            font: "Arial", size: 22, color: COLORS.mutedText, italics: true,
          })],
        }),

        // Organization
        new Paragraph({
          alignment: AlignmentType.CENTER,
          spacing: { before: 600 },
          children: [new TextRun({
            text: "ThakiCloud Research",
            font: "Arial", size: 20, color: COLORS.secondary,
          })],
        }),
      ],
    },

    // =========================
    //  TABLE OF CONTENTS + CONTENT
    // =========================
    {
      properties: { ...pageProps },
      headers: { default: defaultHeader },
      footers: { default: defaultFooter },
      children: [
        heading(HeadingLevel.HEADING_1, "목차"),
        new TableOfContents("목차", {
          hyperlink: true,
          headingStyleRange: "1-3",
        }),
        pageBreak(),

        // --- 핵심 요약 (Executive Summary) ---
        // The agent synthesizes key findings from ALL perspectives
        // into a 2-3 page executive summary. Use calloutBox() and
        // keyFindingPanel() for visual emphasis.
        //
        // Example:
        //   ...sectionDivider("핵심 요약"),
        //   keyFindingPanel("주요 발견 사항", [
        //     "발견 1: 구체적 수치 포함",
        //     "발견 2: 구체적 수치 포함",
        //   ]),
        //   calloutBox("핵심 인사이트", ["인사이트 내용"], COLORS.accent),

        // --- 논문 리뷰 ---
        ...sectionDivider("논문 리뷰"),
        ...convertMarkdownToDocx(reviewMd),

        // --- PM 전략 분석 ---
        ...sectionDivider("PM 전략 분석"),
        ...convertMarkdownToDocx(pmStrategyMd),

        // --- 시장 조사 분석 ---
        ...sectionDivider("시장 조사 분석"),
        ...convertMarkdownToDocx(marketResearchMd),

        // --- 제품 발견 분석 ---
        ...sectionDivider("제품 발견 분석"),
        ...convertMarkdownToDocx(discoveryMd),

        // --- GTM 분석 ---
        ...sectionDivider("GTM 분석"),
        ...convertMarkdownToDocx(gtmMd),

        // --- 통계/방법론 검토 ---
        ...sectionDivider("통계 및 방법론 검토"),
        ...convertMarkdownToDocx(statisticsMd),

        // --- 실행 계획 ---
        ...sectionDivider("실행 계획"),
        ...convertMarkdownToDocx(executionMd),

        // --- 부록 ---
        ...sectionDivider("부록"),
        bodyParagraph("논문 메타데이터, 분석에 사용된 도구 및 프레임워크 목록을 여기에 포함합니다."),
      ],
    },
  ],
});

Packer.toBuffer(doc).then((buffer) => {
  fs.writeFileSync(OUTPUT_PATH, buffer);
  console.log(`Document saved to ${OUTPUT_PATH}`);
});
```

## How the Agent Should Use This Template

1. **Replace placeholders**: Fill `{paper_title}`, `{authors}`, `{date}`,
   `{output_path}`, and all `{*_md_path}` variables with actual values.

2. **Executive Summary**: Before the review section, the agent should manually
   compose a 2-3 page executive summary using `calloutBox()`,
   `keyFindingPanel()`, and `bodyParagraph()` to highlight the most important
   findings across all perspectives. This section is NOT auto-generated from
   markdown — the agent writes it directly using the helpers.

3. **convertMarkdownToDocx()**: Use this function to convert each perspective's
   markdown file into docx elements. It handles:
   - `# / ## / ###` headings → proper heading levels (included in TOC)
   - `- / *` unordered lists → bulleted lists with `LevelFormat.BULLET`
   - `1. 2. 3.` ordered lists → numbered lists with `LevelFormat.DECIMAL`
   - `> blockquote` → indented italic with left border
   - `| pipe | tables |` → styled tables with alternating row colors
   - `---` → page breaks between major sections
   - `**bold**`, `*italic*`, `` `code` `` → proper TextRun formatting

4. **Visual emphasis**: Use `calloutBox()` for key insights within the
   executive summary, `scoreTable()` for the evaluation score grid, and
   `keyFindingPanel()` for numbered findings.

## Markdown-to-DOCX Conversion Reference

| Markdown | DOCX Element | Function |
|----------|-------------|----------|
| `# Heading` | Heading 1 (in TOC) | `heading(HeadingLevel.HEADING_1, text)` |
| `## Heading` | Heading 2 (in TOC) | `heading(HeadingLevel.HEADING_2, text)` |
| `### Heading` | Heading 3 (in TOC) | `heading(HeadingLevel.HEADING_3, text)` |
| `- bullet` | Bulleted list | `bulletItem(text)` |
| `1. item` | Numbered list | `numberedItem(text)` |
| `> quote` | Indented italic + left border | `blockquote(text)` |
| `**bold**` inside text | Bold TextRun | via `parseInlineMarkdown()` |
| `*italic*` inside text | Italic TextRun | via `parseInlineMarkdown()` |
| `` `code` `` inside text | Monospace + tinted bg | via `parseInlineMarkdown()` |
| `\| table \|` | Table with alt-row colors | `markdownTableToDocx()` |
| `---` | Page break | `pageBreak()` |

## Visual Design Helpers Reference

| Helper | Purpose | When to Use |
|--------|---------|-------------|
| `calloutBox(title, lines, color)` | Accent-bordered box with tinted background | Key insights, warnings, recommendations |
| `keyFindingPanel(title, items)` | Numbered panel with top/bottom borders | Executive summary findings |
| `sectionDivider(title)` | Page break + decorated heading | Between major document sections |
| `scoreTable(title, rows)` | Color-coded score grid | Evaluation scores (green/yellow/red) |
| `markdownTableToDocx(headers, rows)` | Styled table with alternating rows | Any tabular data from markdown |

## Validation

After generating the document, always validate:

```bash
python .cursor/skills/anthropic-docx/scripts/office/validate.py output.docx
```

## Key Constraints

- Page size: US Letter (12240 x 15840 DXA)
- Margins: 1 inch all around (1440 DXA)
- Content width: 9360 DXA
- Default font: Arial 11pt (size: 22 in half-points)
- Line spacing: 1.15 (line: 276 in 240ths)
- Never use unicode bullets — use `LevelFormat.BULLET`
- Never use `\n` inside TextRun — use separate Paragraphs
- Tables: always set both `columnWidths` and cell `width` with `WidthType.DXA`
- Use `ShadingType.CLEAR` (not SOLID) for cell shading
- Cell margins use `margins` property (not `margin`)
- Alternating row colors: even rows `F8FAFC`, odd rows `FFFFFF`
