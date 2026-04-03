#!/usr/bin/env node
/**
 * Upload pages from MCP-shaped JSON:
 * { "parent": { "page_id": "uuid" }, "pages": [ { "properties": { "title": "..." }, "icon": "📄", "content": "..." } ] }
 *
 * Usage:
 *   NOTION_TOKEN=xxx node upload-mcp-pages.mjs <json-path> [--from N]
 *
 * --from N: skip first N pages (0-based; use 1 to skip first child already uploaded).
 */
import { Client } from "@notionhq/client";
import { markdownToBlocks } from "@tryfabric/martian";
import fs from "fs";

const NOTION_TOKEN = process.env.NOTION_TOKEN;
if (!NOTION_TOKEN) {
  console.error("NOTION_TOKEN is required.");
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

/** Notion API rejects link rich_text with fragment-only or relative URLs. */
function sanitizeMarkdownLinks(md) {
  return md
    .replace(/\[([^\]]+)\]\(#[^)]*\)/g, "$1")
    .replace(/\[([^\]]+)\]\((?!https?:\/\/|mailto:)[^)]*\)/g, "$1");
}

function mdToBlocks(md) {
  md = sanitizeMarkdownLinks(md);
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

async function createPage(parentId, title, content, icon = null) {
  const blocks = mdToBlocks(content);
  const cleanParent = parentId.replace(/-/g, "");
  const props = {
    parent: { page_id: cleanParent },
    properties: {
      title: [{ text: { content: title } }],
    },
    children: blocks.slice(0, 100),
  };
  if (icon && icon !== "none") {
    props.icon = { type: "emoji", emoji: icon };
  }
  const page = await notion.pages.create(props);
  if (blocks.length > 100) {
    await appendBlocks(page.id, blocks.slice(100));
  }
  return page;
}

async function main() {
  const args = process.argv.slice(2);
  let fromIdx = 0;
  const paths = [];
  for (let i = 0; i < args.length; i++) {
    if (args[i] === "--from" && args[i + 1]) {
      fromIdx = parseInt(args[i + 1], 10);
      i++;
    } else if (!args[i].startsWith("--")) {
      paths.push(args[i]);
    }
  }
  const jsonPath = paths[0];
  if (!jsonPath) {
    console.error("Usage: node upload-mcp-pages.mjs <json-path> [--from N]");
    process.exit(1);
  }

  const data = JSON.parse(fs.readFileSync(jsonPath, "utf-8"));
  const parentId = data.parent.page_id;
  const pages = data.pages.slice(fromIdx);

  const out = [];
  for (const p of pages) {
    const title = p.properties.title;
    const icon = p.icon ?? null;
    const content = p.content ?? "";
    const page = await createPage(parentId, title, content, icon);
    out.push({ title, url: page.url, id: page.id });
    console.log("OK:", title, "→", page.url);
  }
  console.log(JSON.stringify({ created: out.length, pages: out }, null, 0));
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
