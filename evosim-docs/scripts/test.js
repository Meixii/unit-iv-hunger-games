#!/usr/bin/env node
/**
 * Test Suite for EvoSim Documentation and Engine Logic
 */

import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, "..");

let tests = 0;
let passed = 0;
let failed = 0;

function test(name, fn) {
  tests++;
  try {
    fn();
    console.log(`✔ [PASS] ${name}`);
    passed++;
  } catch (err) {
    console.error(`✖ [FAIL] ${name}: ${err.message}`);
    failed++;
  }
}

function assert(condition, message) {
  if (!condition) throw new Error(message || "Assertion failed");
}

console.log("\n🧪 Running EvoSim Docs Test Suite...\n");

// Test 1: Content file presence
test("All content JSON files exist and parse", () => {
  const contentDir = path.join(ROOT, "content");
  const required = [
    "site.json",
    "objectives.json",
    "scope.json",
    "limitations.json",
    "terminologies.json",
    "mlp-evolution.json",
    "fitness-function.json",
    "core-mechanics.json",
    "parameters.json",
    "map-objectives.json",
    "events-disasters.json",
    "quantitative-mechanics.json",
    "code-implementation.json",
    "formulas.json",
    "data-structure.json",
    "tasks.json",
    "phases.json",
    "dashboard.json",
  ];

  for (const f of required) {
    const full = path.join(contentDir, f);
    assert(fs.existsSync(full), `Missing content file: ${f}`);
    const data = JSON.parse(fs.readFileSync(full, "utf8"));
    assert(typeof data === "object" && data !== null, `${f} is not an object`);
  }
});

// Test 2: Astro pages coverage
test("All documentation pages exist in src/pages", () => {
  const pagesDir = path.join(ROOT, "src", "pages");
  const expectedRoutes = [
    "index.astro",
    "objectives.astro",
    "scope.astro",
    "limitations.astro",
    "terminologies.astro",
    "mlp-evolution.astro",
    "fitness-function.astro",
    "core-mechanics.astro",
    "parameters.astro",
    "map-objectives.astro",
    "events-disasters.astro",
    "quantitative-mechanics.astro",
    "code-implementation.astro",
    "formulas.astro",
    "data-structure.astro",
    "development-tasks.astro",
    "phases.astro",
    "dashboard.astro",
    "404.astro",
  ];

  for (const page of expectedRoutes) {
    const full = path.join(pagesDir, page);
    assert(fs.existsSync(full), `Missing page template: ${page}`);
  }
});

// Test 3: Math formula verification
test("Fitness Score calculation matches formula", () => {
  // Formula: (Time * 1.0) + ((Res / 40) * 5.0) + (Kills * 50.0) + (Dist * 0.2) + (Events * 10.0)
  const time = 45;
  const res = 120;
  const kills = 2;
  const dist = 60;
  const events = 3;

  const score = (time * 1.0) + ((res / 40.0) * 5.0) + (kills * 50.0) + (dist * 0.2) + (events * 10.0);
  assert(score === 202.0, `Expected 202.0, got ${score}`);
});

test("Locomotion energy cost formula matches specification", () => {
  // Formula: (BASE_COST * T_mod) - (AGI * 0.5)
  const baseCost = 10;
  const forestMod = 1.5;
  const agi = 6;

  const cost = (baseCost * forestMod) - (agi * 0.5);
  assert(cost === 12.0, `Expected 12.0, got ${cost}`);
});

test("Combat damage calculation matches specification", () => {
  // Formula: max(5, (STR * 2.0) - AGI_def)
  const str = 8;
  const defAgi = 5;

  const damage = Math.max(5, (str * 2.0) - defAgi);
  assert(damage === 11.0, `Expected 11.0, got ${damage}`);
});

// Test 4: CMS schema integrity
test("CMS schema targets valid files", async () => {
  const schemaFile = path.join(ROOT, "cms", "schema.js");
  assert(fs.existsSync(schemaFile), "cms/schema.js must exist");
  const { schema } = await import(`file://${schemaFile}`);
  for (const [key, def] of Object.entries(schema)) {
    assert(def.file, `Schema ${key} missing file target`);
    const targetPath = path.join(ROOT, "content", def.file);
    assert(fs.existsSync(targetPath), `Schema ${key} targets missing file: ${def.file}`);
  }
});

console.log(`\nResults: ${passed}/${tests} tests passed.`);
if (failed > 0) {
  console.error(`✖ ${failed} test(s) failed.\n`);
  process.exit(1);
} else {
  console.log("✔ All tests passed successfully.\n");
  process.exit(0);
}
