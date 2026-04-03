#!/usr/bin/env node
/**
 * Upload one entry from output/_notion_h2_upload_plans.json:
 * - Creates parent page under root (unless --existing-parent)
 * - Creates each child page under that parent
 *
 * Usage:
 *   NOTION_TOKEN=xxx node upload-h2-plan.mjs <plans.json> <planIndex> <rootPageId> [--existing-parent <pageId>] [--skip-children N]
 *
 * Example (new parent):
 *   node upload-h2-plan.mjs ../../../output/_notion_h2_upload_plans.json 1 3239eddc34e680e8a7a5d5b5eac18b38
 *
 * Example (parent already created — only children):
 *   node upload-h2-plan.mjs ../../../output/_notion_h2_upload_plans.json 0 3239... --existing-parent 3359eddc-34e6-81b7-b118-c7b5428c1676 --skip-children 1
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

function parseArgs(argv) {
  const out = {
    plansPath: null,
    planIndex: null,
    rootPageId: null,
    existingParent: null,
    skipChildren: 0,
  };
  const rest = [...argv];
  while (rest.length) {
    const a = rest.shift();
    if (a === "--existing-parent" && rest[0]) {
      out.existingParent = rest.shift();
    } else if (a === "--skip-children" && rest[0]) {
      out.skipChildren = parseInt(rest.shift(), 10) || 0;
    } else if (!out.plansPath) {
      out.plansPath = a;
    } else if (out.planIndex === null) {
      out.planIndex = parseInt(a, 10);
    } else if (!out.rootPageId) {
      out.rootPageId = a;
    }
  }
  return out;
}

async function main() {
  const { plansPath, planIndex, rootPageId, existingParent, skipChildren } = parseArgs(process.argv.slice(2));
  if (!plansPath || Number.isNaN(planIndex) || !rootPageId) {
    console.error(
      "Usage: node upload-h2-plan.mjs <plans.json> <planIndex> <rootPageId> [--existing-parent <id>] [--skip-children N]",
    );
    process.exit(1);
  }

  const plans = JSON.parse(fs.readFileSync(plansPath, "utf-8"));
  const item = plans[planIndex];
  if (!item) {
    console.error("Invalid planIndex");
    process.exit(1);
  }

  let parentId = existingParent;
  if (!parentId) {
    const parentPage = await createPage(
      rootPageId,
      item.parent_title,
      item.parent_content,
      item.parent_icon,
    );
    parentId = parentPage.id;
    console.log("Parent:", item.parent_title, "→", parentPage.url);
  } else {
    console.log("Using existing parent:", parentId);
  }

  const children = item.children.slice(skipChildren);
  const created = [];
  for (const ch of children) {
    const title = ch.properties.title;
    const icon = ch.icon ?? "📄";
    const content = ch.content ?? "";
    const page = await createPage(parentId, title, content, icon);
    created.push({ title, url: page.url, id: page.id });
    console.log("Child OK:", title, "→", page.url);
  }
  console.log(JSON.stringify({ parentId, created: created.length, pages: created }, null, 2));
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
