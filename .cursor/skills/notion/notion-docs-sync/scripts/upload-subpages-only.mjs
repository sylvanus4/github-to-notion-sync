#!/usr/bin/env node
/**
 * Create sub-pages only under an existing parent (for when parent was already created via MCP).
 * Usage: NOTION_TOKEN=xxx node upload-subpages-only.mjs <mcp-args-json> <parent-page-id>
 * mcp-args-json has: { parent: { page_id }, pages: [{ properties: { title }, content }] }
 */
import { Client } from "@notionhq/client";
import { markdownToBlocks } from "@tryfabric/martian";
import fs from "fs";

const NOTION_TOKEN = process.env.NOTION_TOKEN;
if (!NOTION_TOKEN) {
  console.error("NOTION_TOKEN required");
  process.exit(1);
}

const [jsonPath, parentId] = process.argv.slice(2);
if (!jsonPath || !parentId) {
  console.error("Usage: NOTION_TOKEN=xxx node upload-subpages-only.mjs <mcp-args-json> <parent-page-id>");
  process.exit(1);
}

const notion = new Client({ auth: NOTION_TOKEN, notionVersion: "2022-06-28" });

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

async function appendBlocks(pageId, blocks) {
  for (let i = 0; i < blocks.length; i += 100) {
    await notion.blocks.children.append({
      block_id: pageId,
      children: blocks.slice(i, i + 100),
    });
  }
}

async function createPage(parent, title, content) {
  const blocks = mdToBlocks(content);
  const page = await notion.pages.create({
    parent: { page_id: parent.replace(/-/g, "") },
    properties: { title: [{ text: { content: title } }] },
    children: blocks.slice(0, 100),
  });
  if (blocks.length > 100) await appendBlocks(page.id, blocks.slice(100));
  return page;
}

async function main() {
  const args = JSON.parse(fs.readFileSync(jsonPath, "utf-8"));
  const cleanParentId = parentId.replace(/-/g, "");
  for (const p of args.pages) {
    const title = p.properties.title;
    const content = p.content || "";
    const page = await createPage(cleanParentId, title, content);
    console.log("Created:", title, "→", page.url);
  }
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
