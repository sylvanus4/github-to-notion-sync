#!/usr/bin/env node

/**
 * Fat Skills / Fat Code / Thin Harness — afterFileEdit static guard.
 *
 * Runs on every Write to a SKILL.md file. Checks:
 *   1. Inline executable code density (threshold: 20 lines)
 *   2. Inline data-block size (JSON/YAML/SQL >50 lines)
 *   3. Harness body line count (threshold: 250 lines)
 *
 * Non-blocking: surfaces warnings via additional_context so the agent
 * can self-correct, but never prevents the edit.
 */

import { readFileSync } from "node:fs";
import { resolve } from "node:path";

const CODE_FENCE_LANG =
  /^```(?:python|py|javascript|js|typescript|ts|go|bash|sh|shell|ruby|rust|java|csharp|c\+\+|cpp|swift|kotlin|sql)\b/i;
const DATA_FENCE =
  /^```(?:json|yaml|yml|toml|xml|sql|graphql|hcl)\b/i;
const FRONTMATTER_DELIM = /^---\s*$/;
const LAZY_DELEGATION =
  /based on (?:your|the) findings?,?\s*(?:implement|execute|build|create|do)/i;

function collectInput() {
  return new Promise((res) => {
    let buf = "";
    process.stdin.setEncoding("utf8");
    process.stdin.on("data", (chunk) => (buf += chunk));
    process.stdin.on("end", () => res(buf));
  });
}

function isSkillFile(filePath) {
  return filePath.endsWith("/SKILL.md") || filePath === "SKILL.md";
}

function isHarness(filePath) {
  return (
    filePath.includes("/harness/") || filePath.includes("/workflow/harness")
  );
}

function stripFrontmatter(lines) {
  if (lines.length === 0) return lines;
  if (!FRONTMATTER_DELIM.test(lines[0])) return lines;
  for (let i = 1; i < lines.length; i++) {
    if (FRONTMATTER_DELIM.test(lines[i])) return lines.slice(i + 1);
  }
  return lines;
}

function analyze(content, filePath) {
  const warnings = [];
  const lines = content.split("\n");
  const body = stripFrontmatter(lines);

  let codeLines = 0;
  let dataBlockLines = 0;
  let inCode = false;
  let inData = false;
  let currentBlockLines = 0;
  let lazyDelegationHits = [];

  for (let i = 0; i < body.length; i++) {
    const line = body[i];

    if (inCode || inData) {
      currentBlockLines++;
      if (/^```\s*$/.test(line)) {
        if (inCode) codeLines += currentBlockLines;
        if (inData) dataBlockLines += currentBlockLines;
        inCode = false;
        inData = false;
        currentBlockLines = 0;
      }
      continue;
    }

    if (CODE_FENCE_LANG.test(line)) {
      inCode = true;
      currentBlockLines = 0;
      continue;
    }
    if (DATA_FENCE.test(line)) {
      inData = true;
      currentBlockLines = 0;
      continue;
    }

    if (LAZY_DELEGATION.test(line)) {
      lazyDelegationHits.push(i + 1);
    }
  }

  if (codeLines > 20) {
    warnings.push(
      `⚠️ Fat/Thin: ${codeLines} inline code lines detected (threshold: 20). Extract to scripts/.`
    );
  }

  if (dataBlockLines > 50) {
    warnings.push(
      `⚠️ Fat/Thin: ${dataBlockLines} inline data-block lines (JSON/YAML/SQL) detected (threshold: 50). Extract to code files.`
    );
  }

  if (isHarness(filePath)) {
    if (body.length >= 250) {
      warnings.push(
        `⚠️ Fat/Thin: Harness body is ${body.length} lines (threshold: <250). Consider extracting domain logic to dedicated skills.`
      );
    }
    if (lazyDelegationHits.length > 0) {
      warnings.push(
        `⚠️ Fat/Thin: Lazy delegation detected at line(s) ${lazyDelegationHits.join(", ")}. Synthesize before dispatch (Pattern 4).`
      );
    }
  }

  return warnings;
}

async function main() {
  try {
    const raw = await collectInput();
    if (!raw.trim()) process.exit(0);

    const input = JSON.parse(raw);
    const filePath = input.path || input.filePath || "";

    if (!isSkillFile(filePath)) process.exit(0);

    let content;
    try {
      content = readFileSync(resolve(filePath), "utf8");
    } catch {
      process.exit(0);
    }

    const warnings = analyze(content, filePath);

    if (warnings.length > 0) {
      const msg = [
        "**Fat/Thin Guard** detected potential violations:",
        ...warnings,
        "",
        "Ref: `.cursor/rules/fat-thin-principle.mdc`",
      ].join("\n");

      console.log(JSON.stringify({ additional_context: msg }));
    }
  } catch {
    process.exit(0);
  }
}

main();
