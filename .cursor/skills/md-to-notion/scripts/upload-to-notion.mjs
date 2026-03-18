#!/usr/bin/env node
/**
 * Upload pre-processed markdown (from convert_tables.py JSON) to Notion.
 * Uses NOTION_TOKEN and @notionhq/client.
 *
 * Usage:
 *   NOTION_TOKEN=xxx node upload-to-notion.mjs <json-path> <parent-page-id>
 *
 * Example:
 *   NOTION_TOKEN=xxx node upload-to-notion.mjs /tmp/notion_page_0.json 3209eddc34e6801b8921f55d85153730
 */
import { Client } from "@notionhq/client";
import { markdownToBlocks } from "@tryfabric/martian";
import fs from "fs";

const NOTION_TOKEN = process.env.NOTION_TOKEN;
if (!NOTION_TOKEN) {
  console.error("NOTION_TOKEN 환경변수가 필요합니다.");
  process.exit(1);
}

const [jsonPath, parentId] = process.argv.slice(2);
if (!jsonPath || !parentId) {
  console.error("Usage: NOTION_TOKEN=xxx node upload-to-notion.mjs <json-path> <parent-page-id>");
  process.exit(1);
}

const notion = new Client({ auth: NOTION_TOKEN, notionVersion: "2022-06-28" });

async function appendBlocks(pageId, blocks) {
  for (let i = 0; i < blocks.length; i += 100) {
    await notion.blocks.children.append({
      block_id: pageId,
      children: blocks.slice(i, i + 100),
    });
  }
}

function htmlTableToMarkdown(html) {
  const rows = [];
  const trRe = /<tr>([\s\S]*?)<\/tr>/gi;
  let m;
  while ((m = trRe.exec(html)) !== null) {
    const cells = [];
    const tdRe = /<td>([\s\S]*?)<\/td>/gi;
    let cm;
    while ((cm = tdRe.exec(m[1])) !== null) {
      cells.push(cm[1].trim().replace(/<[^>]+>/g, ""));
    }
    if (cells.length) rows.push(cells);
  }
  if (rows.length === 0) return "";
  const header = rows[0].join(" | ");
  const sep = rows[0].map(() => "---").join(" | ");
  const dataRows = rows.slice(1).map((r) => r.join(" | "));
  return `| ${header} |\n| ${sep} |\n` + dataRows.map((r) => `| ${r} |`).join("\n");
}

function mdToBlocks(md) {
  const TABLE_RE = /<table[^>]*>[\s\S]*?<\/table>/gi;
  const parts = [];
  let lastIdx = 0;
  let m;
  while ((m = TABLE_RE.exec(md)) !== null) {
    if (m.index > lastIdx) {
      parts.push({ type: "md", content: md.slice(lastIdx, m.index) });
    }
    parts.push({ type: "table", content: htmlTableToMarkdown(m[0]) });
    lastIdx = m.index + m[0].length;
  }
  if (lastIdx < md.length) parts.push({ type: "md", content: md.slice(lastIdx) });
  const fullMd = parts.map((p) => (p.type === "table" ? p.content : p.content)).join("\n\n");
  return markdownToBlocks(fullMd);
}

async function createPage(parent, title, content, icon = null) {
  const blocks = mdToBlocks(content);
  const props = {
    parent: { page_id: parent },
    properties: {
      title: [{ text: { content: title } }],
    },
    children: blocks.slice(0, 100),
  };
  if (icon) props.icon = { type: "emoji", emoji: icon };
  const page = await notion.pages.create(props);
  if (blocks.length > 100) {
    await appendBlocks(page.id, blocks.slice(100));
  }
  return page;
}

async function main() {
  const data = JSON.parse(fs.readFileSync(jsonPath, "utf-8"));
  const cleanParentId = parentId.replace(/-/g, "");

  if (data.split) {
    const parentContent = `> This document is split into sub-pages due to size.
> Original file: \`${data.filepath}\`

Sub-pages are listed below.`;
    const parentPage = await createPage(
      cleanParentId,
      data.title,
      parentContent,
      "📄"
    );
    console.log("Created parent:", data.title, "→", parentPage.url);

    for (let i = 0; i < data.parts.length; i++) {
      const part = data.parts[i];
      const subTitle = `${i + 1}부: ${part.subtitle}`;
      const subPage = await createPage(parentPage.id, subTitle, part.body);
      console.log("Created sub-page:", subTitle, "→", subPage.url);
    }

    console.log("\nNotion page URL:", parentPage.url);
  } else {
    const page = await createPage(cleanParentId, data.title, data.content, "📄");
    console.log("Created:", data.title, "→", page.url);
  }
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
