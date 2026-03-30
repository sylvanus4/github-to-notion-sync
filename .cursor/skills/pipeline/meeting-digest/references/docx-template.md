# Meeting Digest DOCX Template

Node.js `docx` code template for generating meeting digest Word documents.
Follows the patterns and constraints from `anthropic-docx` skill.

## Prerequisites

```bash
npm install -g docx
```

Run with:
```bash
NODE_PATH=$(npm root -g) node generate-meeting-docx.js
```

## Document Structure

The meeting digest DOCX combines `summary.md` and `action-items.md` into
a single professional document with this layout:

1. Cover page (meeting title, date, type badge)
2. Table of Contents (auto-generated)
3. 회의 개요 (participants, date, topic)
4. 핵심 논의 사항 (one subsection per discussion point)
5. 주요 결정 사항 (decision table)
6. 미해결 이슈 (open issues table)
7. 액션 아이템 대시보드 (action items table)
8. 다음 단계 (next steps)
9. 부록: PM 분석 (PM analysis appendix, if applicable)

## Code Template

```javascript
const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  Header, Footer, AlignmentType, LevelFormat, HeadingLevel,
  BorderStyle, WidthType, ShadingType, PageBreak, PageNumber,
  TableOfContents
} = require("docx");

// --- Constants ---
const PAGE_WIDTH = 12240;   // US Letter width in DXA
const PAGE_HEIGHT = 15840;  // US Letter height in DXA
const MARGIN = 1440;        // 1 inch in DXA
const CONTENT_WIDTH = PAGE_WIDTH - (MARGIN * 2); // 9360 DXA
const FONT_DEFAULT = "Arial";

// --- Shared styles ---
const border = { style: BorderStyle.SINGLE, size: 1, color: "CCCCCC" };
const borders = { top: border, bottom: border, left: border, right: border };
const cellMargins = { top: 80, bottom: 80, left: 120, right: 120 };

const headerShading = { fill: "2B579A", type: ShadingType.CLEAR };
const headerTextStyle = { bold: true, color: "FFFFFF", font: FONT_DEFAULT, size: 20 };
const bodyTextStyle = { font: FONT_DEFAULT, size: 20 };

// --- Helper functions ---

function createHeaderCell(text, width) {
  return new TableCell({
    borders, width: { size: width, type: WidthType.DXA },
    shading: headerShading, margins: cellMargins,
    children: [new Paragraph({
      children: [new TextRun({ ...headerTextStyle, text })]
    })]
  });
}

function createBodyCell(text, width) {
  return new TableCell({
    borders, width: { size: width, type: WidthType.DXA },
    margins: cellMargins,
    children: [new Paragraph({
      children: [new TextRun({ ...bodyTextStyle, text })]
    })]
  });
}

function createTable(headers, rows, columnWidths) {
  return new Table({
    width: { size: CONTENT_WIDTH, type: WidthType.DXA },
    columnWidths,
    rows: [
      new TableRow({
        children: headers.map((h, i) => createHeaderCell(h, columnWidths[i]))
      }),
      ...rows.map(row =>
        new TableRow({
          children: row.map((cell, i) => createBodyCell(cell, columnWidths[i]))
        })
      )
    ]
  });
}

// --- Build document ---

function buildMeetingDigest({ title, date, meetingType, participants,
  topics, decisions, openIssues, actionItems, nextSteps, pmAnalysis }) {

  const doc = new Document({
    styles: {
      default: {
        document: { run: { font: FONT_DEFAULT, size: 22 } }
      },
      paragraphStyles: [
        {
          id: "Heading1", name: "Heading 1", basedOn: "Normal",
          next: "Normal", quickFormat: true,
          run: { size: 32, bold: true, font: FONT_DEFAULT, color: "2B579A" },
          paragraph: { spacing: { before: 360, after: 200 }, outlineLevel: 0 }
        },
        {
          id: "Heading2", name: "Heading 2", basedOn: "Normal",
          next: "Normal", quickFormat: true,
          run: { size: 28, bold: true, font: FONT_DEFAULT, color: "2B579A" },
          paragraph: { spacing: { before: 240, after: 160 }, outlineLevel: 1 }
        },
        {
          id: "Heading3", name: "Heading 3", basedOn: "Normal",
          next: "Normal", quickFormat: true,
          run: { size: 24, bold: true, font: FONT_DEFAULT },
          paragraph: { spacing: { before: 200, after: 120 }, outlineLevel: 2 }
        }
      ]
    },
    numbering: {
      config: [{
        reference: "bullets",
        levels: [{
          level: 0, format: LevelFormat.BULLET, text: "\u2022",
          alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } }
        }]
      }]
    },
    sections: [
      // --- Section 1: Cover Page ---
      {
        properties: {
          page: {
            size: { width: PAGE_WIDTH, height: PAGE_HEIGHT },
            margin: { top: MARGIN, right: MARGIN, bottom: MARGIN, left: MARGIN }
          }
        },
        children: [
          new Paragraph({ spacing: { before: 4000 } }),
          new Paragraph({
            alignment: AlignmentType.CENTER,
            children: [new TextRun({
              text: "회의 요약 보고서",
              font: FONT_DEFAULT, size: 48, bold: true, color: "2B579A"
            })]
          }),
          new Paragraph({ spacing: { before: 600 },
            alignment: AlignmentType.CENTER,
            children: [new TextRun({
              text: title, font: FONT_DEFAULT, size: 36, color: "333333"
            })]
          }),
          new Paragraph({ spacing: { before: 400 },
            alignment: AlignmentType.CENTER,
            children: [new TextRun({
              text: `${date}  |  ${meetingType}`,
              font: FONT_DEFAULT, size: 24, color: "666666"
            })]
          }),
          new Paragraph({ spacing: { before: 200 },
            alignment: AlignmentType.CENTER,
            children: [new TextRun({
              text: `참석자: ${participants.join(", ")}`,
              font: FONT_DEFAULT, size: 22, color: "666666"
            })]
          })
        ]
      },

      // --- Section 2: TOC + Body ---
      {
        properties: {
          page: {
            size: { width: PAGE_WIDTH, height: PAGE_HEIGHT },
            margin: { top: MARGIN, right: MARGIN, bottom: MARGIN, left: MARGIN }
          }
        },
        headers: {
          default: new Header({
            children: [new Paragraph({
              alignment: AlignmentType.RIGHT,
              children: [new TextRun({
                text: `${title} — ${date}`,
                font: FONT_DEFAULT, size: 16, color: "999999"
              })]
            })]
          })
        },
        footers: {
          default: new Footer({
            children: [new Paragraph({
              alignment: AlignmentType.CENTER,
              children: [new TextRun({ children: [PageNumber.CURRENT],
                font: FONT_DEFAULT, size: 16, color: "999999" })]
            })]
          })
        },
        children: [
          // Table of Contents
          new Paragraph({
            heading: HeadingLevel.HEADING_1,
            children: [new TextRun("목차")]
          }),
          new TableOfContents("Table of Contents", {
            hyperlink: true, headingStyleRange: "1-3"
          }),
          new Paragraph({ children: [new PageBreak()] }),

          // 회의 개요
          new Paragraph({
            heading: HeadingLevel.HEADING_1,
            children: [new TextRun("회의 개요")]
          }),
          // ... populate from summary.md overview section ...

          // 핵심 논의 사항
          new Paragraph({ children: [new PageBreak()] }),
          new Paragraph({
            heading: HeadingLevel.HEADING_1,
            children: [new TextRun("핵심 논의 사항")]
          }),
          // ... one H2 subsection per topic from topics array ...

          // 주요 결정 사항
          new Paragraph({ children: [new PageBreak()] }),
          new Paragraph({
            heading: HeadingLevel.HEADING_1,
            children: [new TextRun("주요 결정 사항")]
          }),
          createTable(
            ["#", "결정 사항", "맥락/근거"],
            decisions.map((d, i) => [String(i + 1), d.decision, d.context]),
            [600, 4380, 4380]
          ),

          // 미해결 이슈
          new Paragraph({ spacing: { before: 400 } }),
          new Paragraph({
            heading: HeadingLevel.HEADING_1,
            children: [new TextRun("미해결 이슈")]
          }),
          createTable(
            ["#", "이슈", "담당자", "예상 해결일"],
            openIssues.map((o, i) => [String(i + 1), o.issue, o.owner, o.dueDate]),
            [600, 4000, 2380, 2380]
          ),

          // 액션 아이템 대시보드
          new Paragraph({ children: [new PageBreak()] }),
          new Paragraph({
            heading: HeadingLevel.HEADING_1,
            children: [new TextRun("액션 아이템 대시보드")]
          }),
          createTable(
            ["#", "액션 아이템", "담당자", "우선순위", "마감일"],
            actionItems.map((a, i) => [
              String(i + 1), a.item, a.owner, a.priority, a.dueDate
            ]),
            [500, 3500, 1800, 1200, 2360]
          ),

          // 다음 단계
          new Paragraph({ spacing: { before: 400 } }),
          new Paragraph({
            heading: HeadingLevel.HEADING_1,
            children: [new TextRun("다음 단계")]
          }),
          // ... populate from nextSteps array as bullet list ...

          // 부록: PM 분석 (conditional)
          ...(pmAnalysis ? [
            new Paragraph({ children: [new PageBreak()] }),
            new Paragraph({
              heading: HeadingLevel.HEADING_1,
              children: [new TextRun("부록: PM 분석")]
            }),
            // ... populate from pmAnalysis content ...
          ] : [])
        ]
      }
    ]
  });

  return doc;
}

// --- Generate and save ---
async function main() {
  // Read and parse the summary.md and action-items.md files
  // to extract structured data (title, participants, topics, etc.)
  const meetingData = {
    title: "MEETING_TITLE",
    date: "YYYY-MM-DD",
    meetingType: "sprint (회고)",
    participants: ["참석자1", "참석자2"],
    topics: [/* { title, content } */],
    decisions: [/* { decision, context } */],
    openIssues: [/* { issue, owner, dueDate } */],
    actionItems: [/* { item, owner, priority, dueDate } */],
    nextSteps: ["Step 1", "Step 2"],
    pmAnalysis: null // or string content
  };

  const doc = buildMeetingDigest(meetingData);
  const buffer = await Packer.toBuffer(doc);
  fs.writeFileSync("output/meetings/YYYY-MM-DD/{slug}/meeting-digest.docx", buffer);
  console.log("DOCX generated successfully.");
}

main().catch(console.error);
```

## Key Rules

1. **Always use `WidthType.DXA`** — never `WidthType.PERCENTAGE`
2. **Table `columnWidths` must sum to `CONTENT_WIDTH`** (9360 for US Letter with 1" margins)
3. **Cell `width` must match its corresponding `columnWidth`**
4. **Use `LevelFormat.BULLET`** — never unicode bullet characters
5. **Run with `NODE_PATH=$(npm root -g)`** for global module resolution
6. **Korean text renders with system fonts** — Arial has Korean glyph fallback on most systems
7. **Validate after generation**: `python scripts/office/validate.py output.docx`

## Content Extraction from Markdown

When building the DOCX, parse the generated `summary.md` and `action-items.md`
to extract structured data. Key sections to extract:

From `summary.md`:
- Title from `# 회의 요약 보고서` heading
- Participants from `참석자` field
- Discussion topics from `## 핵심 논의 사항` subsections
- Decisions from `## 주요 결정 사항` list/table
- Open issues from `## 미해결 이슈` section
- PM analysis from `## 부록: PM 분석` section

From `action-items.md`:
- Action items from the dashboard table
- Priority groupings (긴급, 높음, 보통)
- Owner assignments and due dates
