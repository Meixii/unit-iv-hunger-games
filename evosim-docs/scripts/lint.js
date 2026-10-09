#!/usr/bin/env node
/**
 * Strict Anti-Slop and Code Quality Linter
 * Enforces:
 *   - Zero em dashes (anti-slop) across all UI, markdown, and content files (R-02)
 *   - No empty links or orphan anchors (R-24)
 *   - Content JSON file structural validity
 */

import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, "..");

let errors = 0;
let checkedFiles = 0;

function scanDir(dir, filterExt) {
  if (!fs.existsSync(dir)) return [];
  const files = [];
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  for (const entry of entries) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      if (entry.name !== "node_modules" && entry.name !== ".astro" && entry.name !== "dist" && entry.name !== ".git") {
        files.push(...scanDir(full, filterExt));
      }
    } else if (filterExt.some((ext) => entry.name.endsWith(ext))) {
      files.push(full);
    }
  }
  return files;
}

console.log("\n🧪 Running Anti-Slop & Quality Checks...\n");

// Check 1: No em dashes in content and UI source files
const filesToCheck = [
  ...scanDir(path.join(ROOT, "content"), [".json"]),
  ...scanDir(path.join(ROOT, "src"), [".astro", ".ts", ".css"]),
  path.join(ROOT, "DESIGN.md"),
  path.join(ROOT, "CHANGELOG.md"),
];

const EM_DASH = "\u2014";

for (const file of filesToCheck) {
  if (!fs.existsSync(file)) continue;
  checkedFiles++;
  const content = fs.readFileSync(file, "utf8");
  const rel = path.relative(ROOT, file);

  if (content.includes(EM_DASH)) {
    const lines = content.split("\n");
    lines.forEach((line, i) => {
      if (line.includes(EM_DASH)) {
        console.error(`❌ [R-02 Violation] Em dash found in ${rel}:${i + 1}`);
        console.error(`   ${line.trim()}`);
        errors++;
      }
    });
  }
}

// Check 2: Content JSON files parse validly
const contentDir = path.join(ROOT, "content");
const jsonFiles = scanDir(contentDir, [".json"]);

for (const jf of jsonFiles) {
  const rel = path.relative(ROOT, jf);
  try {
    JSON.parse(fs.readFileSync(jf, "utf8"));
  } catch (err) {
    console.error(`❌ [JSON Syntax Error] ${rel}: ${err.message}`);
    errors++;
  }
}

// Check 3: Verified no dead anchor links "#" in Astro pages
const astroFiles = scanDir(path.join(ROOT, "src"), [".astro"]);
for (const af of astroFiles) {
  const rel = path.relative(ROOT, af);
  const content = fs.readFileSync(af, "utf8");
  if (content.includes('href="#"')) {
    console.error(`❌ [R-26 Violation] Dead link href="#" found in ${rel}`);
    errors++;
  }
}

console.log(`\nChecked ${checkedFiles} files.`);
if (errors === 0) {
  console.log("✔ All Anti-Slop and Quality checks passed perfectly (0 errors).\n");
  process.exit(0);
} else {
  console.error(`\n✖ ${errors} error(s) detected. Fix them before delivery.\n`);
  process.exit(1);
}
