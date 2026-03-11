# DOCX Assembly Instructions

**Language rule**: All document text, headings, labels, and section titles MUST
be written in Korean. English is only allowed for proper nouns and technical
terminology that has no standard Korean equivalent.

Generate the consolidated Word document using Node.js `docx` package following
the `anthropic-docx` skill patterns.

## Document Structure

```
1. 표지 (Cover Page)
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
  darkText: "1A1A1A",
  lightText: "FFFFFF",
  border: "CCCCCC",
  headerBg: "1E3A5F",
};

// --- Reusable Helpers ---
const border = { style: BorderStyle.SINGLE, size: 1, color: COLORS.border };
const borders = { top: border, bottom: border, left: border, right: border };
const noBorder = { style: BorderStyle.NONE, size: 0, color: "FFFFFF" };
const noBorders = { top: noBorder, bottom: noBorder, left: noBorder, right: noBorder };

function heading(level, text) {
  return new Paragraph({
    heading: level,
    children: [new TextRun({ text, font: "Arial" })],
  });
}

function bodyText(text, opts = {}) {
  return new Paragraph({
    spacing: { after: 120 },
    children: [
      new TextRun({
        text,
        font: "Arial",
        size: 22,
        ...opts,
      }),
    ],
  });
}

function bulletItem(text, reference = "bullets") {
  return new Paragraph({
    numbering: { reference, level: 0 },
    children: [new TextRun({ text, font: "Arial", size: 22 })],
  });
}

function sectionBreak() {
  return new Paragraph({
    children: [new PageBreak()],
  });
}

// --- Content Sections ---
// Each section reads from the corresponding markdown file and converts
// the content to docx elements. The conversion follows these rules:
//
// Markdown → DOCX Mapping:
//   # Heading → HeadingLevel.HEADING_1
//   ## Heading → HeadingLevel.HEADING_2
//   ### Heading → HeadingLevel.HEADING_3
//   - bullet → numbered list (bullets reference)
//   1. numbered → numbered list (numbers reference)
//   **bold** → TextRun({ bold: true })
//   | table | → Table with borders
//   paragraph → bodyText()
//   > blockquote → bodyText({ italics: true })
//   --- → page break between major sections

// --- Build Document ---
const doc = new Document({
  styles: {
    default: {
      document: {
        run: { font: "Arial", size: 22, color: COLORS.darkText },
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
        levels: [{
          level: 0, format: LevelFormat.BULLET, text: "\u2022",
          alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } },
        }],
      },
      {
        reference: "numbers",
        levels: [{
          level: 0, format: LevelFormat.DECIMAL, text: "%1.",
          alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } },
        }],
      },
    ],
  },
  sections: [
    // --- Cover Page ---
    {
      properties: {
        page: {
          size: { width: 12240, height: 15840 },
          margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 },
        },
      },
      children: [
        new Paragraph({ spacing: { before: 3600 } }),
        new Paragraph({
          alignment: AlignmentType.CENTER,
          children: [
            new TextRun({
              text: "논문 리뷰 및 분석 보고서",
              font: "Arial", size: 48, bold: true, color: COLORS.primary,
            }),
          ],
        }),
        new Paragraph({ spacing: { after: 600 } }),
        new Paragraph({
          alignment: AlignmentType.CENTER,
          children: [
            new TextRun({
              text: PAPER_TITLE,
              font: "Arial", size: 32, color: COLORS.secondary,
            }),
          ],
        }),
        new Paragraph({ spacing: { after: 400 } }),
        new Paragraph({
          alignment: AlignmentType.CENTER,
          children: [
            new TextRun({
              text: AUTHORS,
              font: "Arial", size: 22, color: COLORS.darkText,
            }),
          ],
        }),
        new Paragraph({ spacing: { after: 200 } }),
        new Paragraph({
          alignment: AlignmentType.CENTER,
          children: [
            new TextRun({
              text: `분석일: ${DATE}`,
              font: "Arial", size: 22, color: COLORS.darkText, italics: true,
            }),
          ],
        }),
      ],
    },

    // --- Table of Contents ---
    {
      properties: {
        page: {
          size: { width: 12240, height: 15840 },
          margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 },
        },
      },
      headers: {
        default: new Header({
          children: [
            new Paragraph({
              children: [
                new TextRun({
                  text: PAPER_TITLE,
                  font: "Arial", size: 16, color: COLORS.border, italics: true,
                }),
              ],
            }),
          ],
        }),
      },
      footers: {
        default: new Footer({
          children: [
            new Paragraph({
              alignment: AlignmentType.CENTER,
              children: [
                new TextRun({ children: [PageNumber.CURRENT], font: "Arial", size: 18 }),
              ],
            }),
          ],
        }),
      },
      children: [
        heading(HeadingLevel.HEADING_1, "목차"),
        new TableOfContents("목차", {
          hyperlink: true,
          headingStyleRange: "1-3",
        }),
        sectionBreak(),

        // --- 콘텐츠 섹션 삽입 ---
        // 각 마크다운 파일을 읽어 docx 요소로 변환:
        //
        // 1. 핵심 요약 (Executive Summary)
        //    - 모든 관점 분석의 주요 발견 사항을 종합
        //    - 최소 2-3 페이지, 구체적 수치와 근거 포함
        //
        // 2. 논문 리뷰 (Phase 2 결과물)
        //    - {paper-id}-review-{DATE}.md 전체 내용 포함
        //
        // 3. PM 전략 분석 — {paper-id}-pm-strategy-{DATE}.md 전체 내용
        // 4. 시장 조사 분석 — {paper-id}-market-research-{DATE}.md 전체 내용
        // 5. 제품 발견 분석 — {paper-id}-discovery-{DATE}.md 전체 내용
        // 6. GTM 분석 — {paper-id}-gtm-{DATE}.md 전체 내용
        // 7. 통계/방법론 검토 — {paper-id}-statistics-{DATE}.md 전체 내용
        // 8. 실행 계획 — {paper-id}-execution-{DATE}.md 전체 내용
        //
        // 9. 부록
        //    - 논문 메타데이터
        //    - 분석에 사용된 도구 및 프레임워크 목록
      ],
    },
  ],
});

Packer.toBuffer(doc).then((buffer) => {
  fs.writeFileSync(OUTPUT_PATH, buffer);
  console.log(`Document saved to ${OUTPUT_PATH}`);
});
```

## Markdown-to-DOCX Conversion Rules

When converting each markdown section to docx elements:

| Markdown | DOCX Element |
|----------|-------------|
| `# Heading` | `heading(HeadingLevel.HEADING_1, text)` |
| `## Heading` | `heading(HeadingLevel.HEADING_2, text)` |
| `### Heading` | `heading(HeadingLevel.HEADING_3, text)` |
| `- bullet item` | `bulletItem(text)` |
| `1. numbered` | numbered list with `numbers` reference |
| `**bold text**` | `TextRun({ text, bold: true })` |
| `*italic text*` | `TextRun({ text, italics: true })` |
| `> blockquote` | `bodyText(text, { italics: true })` |
| Regular paragraph | `bodyText(text)` |
| `---` | `sectionBreak()` |

### Table Conversion

For markdown tables, create `Table` with proper `columnWidths` and cell widths:

```javascript
function markdownTableToDocx(headers, rows) {
  const colCount = headers.length;
  const colWidth = Math.floor(9360 / colCount);

  const headerRow = new TableRow({
    children: headers.map(h => new TableCell({
      borders,
      width: { size: colWidth, type: WidthType.DXA },
      shading: { fill: COLORS.headerBg, type: ShadingType.CLEAR },
      children: [new Paragraph({
        children: [new TextRun({ text: h, bold: true, color: COLORS.lightText, font: "Arial", size: 20 })],
      })],
    })),
  });

  const dataRows = rows.map(row => new TableRow({
    children: row.map(cell => new TableCell({
      borders,
      width: { size: colWidth, type: WidthType.DXA },
      children: [new Paragraph({
        children: [new TextRun({ text: cell, font: "Arial", size: 20 })],
      })],
    })),
  }));

  return new Table({
    width: { size: 9360, type: WidthType.DXA },
    columnWidths: Array(colCount).fill(colWidth),
    rows: [headerRow, ...dataRows],
  });
}
```

## Validation

After generating the document, always validate:

```bash
python .cursor/skills/anthropic-docx/scripts/office/validate.py output.docx
```

If validation fails, unpack → fix XML → repack per the `anthropic-docx` editing workflow.

## Key Constraints

- Page size: US Letter (12240 x 15840 DXA)
- Margins: 1 inch all around (1440 DXA)
- Default font: Arial 11pt (size: 22 in half-points)
- Never use unicode bullets — use `LevelFormat.BULLET`
- Tables: always set both `columnWidths` and cell `width`
- Use `ShadingType.CLEAR` (not SOLID) for cell shading
- No `\n` in TextRun text — use separate Paragraphs
