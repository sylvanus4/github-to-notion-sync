#!/usr/bin/env node
/**
 * Upload hardware-spec JSON parts to Notion:
 * - Part 1: replace body on existing page (clear blocks + append)
 * - Parts 2–N: create child pages under parent
 *
 * Usage (from this directory, after npm install):
 *   NOTION_TOKEN=... node upload-hw-spec-parts.mjs <path-to-notion_page_0.json> <parentPageId> <part1ExistingPageId>
 *
 * Example:
 *   node upload-hw-spec-parts.mjs /tmp/notion-upload-BuQwFx/notion_page_0.json 3359eddc34e6814c8db0fd99cf5bb138 3359eddc-34e6-81a3-a8b9-f33df1398f5f
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
const ICON = "📄";

async function appendBlocks(pageId, blocks) {
  for (let i = 0; i < blocks.length; i += 100) {
    await notion.blocks.children.append({
      block_id: pageId,
      children: blocks.slice(i, i + 100),
    });
  }
}

/** Remove all direct child blocks (best-effort; skip failures for locked/synced blocks). */
async function clearPageBlocks(pageId) {
  const cleanId = pageId.replace(/-/g, "");
  let cursor = undefined;
  let deleted = 0;
  do {
    const res = await notion.blocks.children.list({
      block_id: cleanId,
      start_cursor: cursor,
      page_size: 100,
    });
    for (const block of res.results) {
      try {
        await notion.blocks.delete({ block_id: block.id });
        deleted += 1;
      } catch {
        // ignore
      }
    }
    cursor = res.has_more ? res.next_cursor : undefined;
  } while (cursor);
  return deleted;
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

async function createChildPage(parentId, title, content) {
  const blocks = mdToBlocks(content);
  const cleanParent = parentId.replace(/-/g, "");
  const page = await notion.pages.create({
    parent: { page_id: cleanParent },
    properties: {
      title: {
        title: [{ type: "text", text: { content: title } }],
      },
    },
    icon: { type: "emoji", emoji: ICON },
    children: blocks.slice(0, 100),
  });
  if (blocks.length > 100) {
    await appendBlocks(page.id, blocks.slice(100));
  }
  return page;
}

async function replacePageBody(pageId, content) {
  const blocks = mdToBlocks(content);
  await clearPageBlocks(pageId);
  await notion.pages.update({
    page_id: pageId.replace(/-/g, ""),
    icon: { type: "emoji", emoji: ICON },
  });
  await appendBlocks(pageId.replace(/-/g, ""), blocks);
}

async function main() {
  const [jsonPath, parentRaw, part1Id] = process.argv.slice(2);
  if (!jsonPath || !parentRaw || !part1Id) {
    console.error(
      "Usage: node upload-hw-spec-parts.mjs <notion_page_0.json> <parentPageId> <part1ExistingPageId>",
    );
    process.exit(1);
  }

  const data = JSON.parse(fs.readFileSync(jsonPath, "utf-8"));
  const parts = data.parts;
  if (!Array.isArray(parts) || parts.length === 0) {
    console.error("Invalid JSON: missing parts[]");
    process.exit(1);
  }

  const out = [];

  // Part 1 — replace existing page body
  const p0 = parts[0];
  const title0 = `Part 1: ${p0.subtitle}`;
  console.error("Replacing Part 1 body:", title0);
  await replacePageBody(part1Id, p0.body);
  out.push({ index: 1, title: title0, id: part1Id.replace(/-/g, ""), url: `https://notion.so/${part1Id.replace(/-/g, "")}` });

  // Parts 2..N — create under parent
  for (let i = 1; i < parts.length; i++) {
    const part = parts[i];
    const title = `Part ${i + 1}: ${part.subtitle}`;
    console.error("Creating", title, `(${part.body?.length ?? 0} chars)`);
    const page = await createChildPage(parentRaw, title, part.body);
    out.push({
      index: i + 1,
      title,
      id: page.id,
      url: page.url ?? `https://notion.so/${page.id.replace(/-/g, "")}`,
    });
  }

  console.log(JSON.stringify({ ok: true, pages: out }, null, 2));
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
