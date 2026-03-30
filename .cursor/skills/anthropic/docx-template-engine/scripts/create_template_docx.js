#!/usr/bin/env node
/**
 * Create ThakiCloud report DOCX template with placeholder markers.
 * Uses the globally installed `docx` npm package.
 */

const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  HeadingLevel, AlignmentType, WidthType, BorderStyle,
  Header, Footer, PageNumber, NumberFormat,
  Bookmark, ShadingType
} = require("docx");
const fs = require("fs");
const path = require("path");

const THAKI_BLUE = "1A56DB";
const THAKI_DARK = "1E293B";
const CONTENT_WIDTH = 9360;

function createCoverPage() {
  return [
    new Paragraph({ spacing: { before: 4000 } }),
    new Paragraph({
      children: [
        new Bookmark({ id: "COVER_TITLE", children: [
          new TextRun({ text: "{{COVER_TITLE}}", bold: true, size: 56, color: THAKI_BLUE, font: "Arial" })
        ]})
      ],
      alignment: AlignmentType.CENTER,
    }),
    new Paragraph({ spacing: { before: 400 } }),
    new Paragraph({
      children: [
        new Bookmark({ id: "COVER_SUBTITLE", children: [
          new TextRun({ text: "{{COVER_SUBTITLE}}", size: 28, color: THAKI_DARK, font: "Arial" })
        ]})
      ],
      alignment: AlignmentType.CENTER,
    }),
    new Paragraph({ spacing: { before: 2000 } }),
    new Paragraph({
      children: [
        new TextRun({ text: "ThakiCloud", bold: true, size: 24, color: THAKI_BLUE, font: "Arial" }),
      ],
      alignment: AlignmentType.CENTER,
    }),
    new Paragraph({
      children: [
        new TextRun({ text: "Confidential", italics: true, size: 20, color: "6B7280", font: "Arial" }),
      ],
      alignment: AlignmentType.CENTER,
    }),
    new Paragraph({ pageBreakBefore: true }),
  ];
}

function createExecSummary() {
  return [
    new Paragraph({
      text: "Executive Summary",
      heading: HeadingLevel.HEADING_1,
      spacing: { before: 200, after: 200 },
    }),
    new Paragraph({
      children: [
        new Bookmark({ id: "EXEC_SUMMARY", children: [
          new TextRun({ text: "{{EXEC_SUMMARY}}", size: 22, color: THAKI_DARK, font: "Arial" })
        ]})
      ],
      spacing: { after: 200 },
    }),
    new Paragraph({ pageBreakBefore: true }),
  ];
}

function createSection(num, title) {
  return [
    new Paragraph({
      text: title,
      heading: HeadingLevel.HEADING_1,
      spacing: { before: 200, after: 200 },
    }),
    new Paragraph({
      children: [
        new Bookmark({ id: `SECTION_${num}_BODY`, children: [
          new TextRun({ text: `{{SECTION_${num}_BODY}}`, size: 22, color: THAKI_DARK, font: "Arial" })
        ]})
      ],
      spacing: { after: 200 },
    }),
  ];
}

function createRisksTable() {
  const headerRow = new TableRow({
    tableHeader: true,
    children: ["Risk", "Impact", "Mitigation"].map(text =>
      new TableCell({
        children: [new Paragraph({
          children: [new TextRun({ text, bold: true, size: 20, color: "FFFFFF", font: "Arial" })],
        })],
        width: { size: Math.floor(CONTENT_WIDTH / 3), type: WidthType.DXA },
        shading: { type: ShadingType.SOLID, color: THAKI_BLUE },
      })
    ),
  });

  const placeholderRow = new TableRow({
    children: ["{{RISK_1}}", "{{IMPACT_1}}", "{{MITIGATION_1}}"].map(text =>
      new TableCell({
        children: [new Paragraph({
          children: [new TextRun({ text, size: 20, color: THAKI_DARK, font: "Arial" })],
        })],
        width: { size: Math.floor(CONTENT_WIDTH / 3), type: WidthType.DXA },
      })
    ),
  });

  return [
    new Paragraph({
      text: "Risk Assessment",
      heading: HeadingLevel.HEADING_1,
      spacing: { before: 200, after: 200 },
    }),
    new Paragraph({
      children: [new Bookmark({ id: "RISKS_TABLE", children: [
        new TextRun({ text: "" })
      ]})],
    }),
    new Table({
      rows: [headerRow, placeholderRow],
      width: { size: CONTENT_WIDTH, type: WidthType.DXA },
    }),
    new Paragraph({ pageBreakBefore: true }),
  ];
}

function createAppendix() {
  return [
    new Paragraph({
      text: "Appendix",
      heading: HeadingLevel.HEADING_1,
      spacing: { before: 200, after: 200 },
    }),
    new Paragraph({
      children: [
        new Bookmark({ id: "APPENDIX", children: [
          new TextRun({ text: "{{APPENDIX}}", size: 22, color: THAKI_DARK, font: "Arial" })
        ]})
      ],
      spacing: { after: 200 },
    }),
  ];
}

async function main() {
  const outputPath = process.argv[2] || "thaki-report-v1.docx";

  const doc = new Document({
    styles: {
      default: {
        document: {
          run: { size: 22, color: THAKI_DARK, font: "Arial" },
        },
        heading1: {
          run: { size: 32, bold: true, color: THAKI_BLUE, font: "Arial" },
          paragraph: { spacing: { before: 240, after: 120 } },
        },
        heading2: {
          run: { size: 26, bold: true, color: THAKI_DARK, font: "Arial" },
          paragraph: { spacing: { before: 200, after: 100 } },
        },
        heading3: {
          run: { size: 24, bold: true, color: THAKI_DARK, font: "Arial" },
          paragraph: { spacing: { before: 160, after: 80 } },
        },
      },
    },
    sections: [{
      headers: {
        default: new Header({
          children: [new Paragraph({
            children: [
              new TextRun({ text: "ThakiCloud", bold: true, size: 18, color: THAKI_BLUE, font: "Arial" }),
              new TextRun({ text: "  |  Confidential", size: 16, color: "9CA3AF", font: "Arial" }),
            ],
            alignment: AlignmentType.RIGHT,
          })],
        }),
      },
      footers: {
        default: new Footer({
          children: [new Paragraph({
            children: [
              new TextRun({ text: "© 2026 ThakiCloud  |  Page ", size: 16, color: "9CA3AF", font: "Arial" }),
              new TextRun({ children: [PageNumber.CURRENT], size: 16, color: "9CA3AF", font: "Arial" }),
            ],
            alignment: AlignmentType.CENTER,
          })],
        }),
      },
      children: [
        ...createCoverPage(),
        ...createExecSummary(),
        ...createSection(1, "Background"),
        ...createSection(2, "Proposed Solution"),
        ...createRisksTable(),
        ...createAppendix(),
      ],
    }],
  });

  const buffer = await Packer.toBuffer(doc);
  fs.writeFileSync(outputPath, buffer);
  console.log(`Template created: ${outputPath}`);
  console.log(`Slots: COVER_TITLE, COVER_SUBTITLE, EXEC_SUMMARY, SECTION_1_BODY, SECTION_2_BODY, RISKS_TABLE, APPENDIX`);
}

main().catch(err => { console.error(err); process.exit(1); });
