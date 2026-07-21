/**
 * run-redundancy-check.js
 *
 * Checks whether rules from a target filter list are already covered
 * by one or more base filter lists using the ABPVN redundancy engine.
 *
 * Only redundancies originating from the target list are reported.
 *
 * Usage:
 *     node run-redundancy-check.js \
 *       --target src/abpindo.txt \
 *       --base easylist.txt \
 *       --base adguard.txt \
 *       --output src/redundant.txt
 */

"use strict";

const fs = require("fs");
const path = require("path");
const { Worker } = require("worker_threads");

const ENGINE_PATH = path.join(__dirname, "abpvn-redundant.js");
let engineCodeCache = null;

// Lazy initialization without redundant FileSystem access
function getEngineCode() {
  if (!engineCodeCache) {
    try {
      engineCodeCache = fs.readFileSync(ENGINE_PATH, "utf-8");
    } catch (err) {
      throw new Error(`Failed to load engine from ${ENGINE_PATH}: ${err.message}`);
    }
  }
  return engineCodeCache;
}

// --- Helper Functions ---

function printHelp() {
  console.log(`
ABP Redundancy Checker

Usage:
  node tools/run-redundancy-check.js --target <file> --base <file> [options]

Options:
  -t, --target <path>   Target filter file to check for redundancies (Required)
  -b, --base <path>     Base filter file(s) to check against (Can be specified multiple times)
  -o, --output <path>   Output report file path (Default: redundant.txt)
  -h, --help            Show this help message
`);
}

function parseArgs(args) {
  if (args.includes("-h") || args.includes("--help")) {
    printHelp();
    process.exit(0);
  }

  let target = null;
  const baseList = [];
  let output = "redundant.txt";

  for (let i = 0; i < args.length; i++) {
    const flag = args[i];

    if (flag === "--target" || flag === "-t") {
      if (++i >= args.length) {
        throw new Error(`${flag} requires a file path.`);
      }
      target = args[i];
    } else if (flag === "--base" || flag === "-b") {
      if (++i >= args.length) {
        throw new Error(`${flag} requires a file path.`);
      }
      baseList.push(args[i]);
    } else if (flag === "--output" || flag === "-o") {
      if (++i >= args.length) {
        throw new Error(`${flag} requires a file path.`);
      }
      output = args[i];
    } else {
      throw new Error(`Unknown argument: ${flag}`);
    }
  }

  if (!target) {
    throw new Error("Missing required argument: --target (-t)");
  }
  if (baseList.length === 0) {
    throw new Error("Missing required argument: At least one --base (-b) file is required.");
  }

  return { target, baseList, output };
}

function readRules(filepath) {
  const resolvedPath = path.resolve(filepath);
  if (!fs.existsSync(resolvedPath)) {
    throw new Error(`File not found: ${resolvedPath}`);
  }

  const content = fs.readFileSync(resolvedPath, "utf-8");
  const rules = [];

  for (const line of content.split(/\r?\n/)) {
    const t = line.trim();
    if (!t || t.startsWith("!") || t.startsWith("[") || t.startsWith("#")) continue;
    rules.push(t);
  }
  return rules;
}

function runEngine(combinedFilters) {
  const engineCode = getEngineCode();

  const workerCode = `
const { parentPort } = require("worker_threads");
let engineResult = null;
const self = {
  postMessage: (r) => { engineResult = r; },
  close: () => {},
  addEventListener: () => {}
};
globalThis.self = self;

${engineCode}

const data = { filters: ${JSON.stringify(combinedFilters)}, modifiers: {} };
startWorker(data);
parentPort.postMessage(engineResult);
`;

  return new Promise((resolve, reject) => {
    const worker = new Worker(workerCode, { eval: true });

    worker.once("message", resolve);
    worker.once("error", reject);
    worker.once("exit", (code) => {
      if (code !== 0) reject(new Error(`Worker exited with code ${code}`));
    });
  });
}

// --- Main Process ---

async function main() {
  const { target, baseList, output } = parseArgs(process.argv.slice(2));
  const outputPath = path.resolve(output);

  console.log(`Loading target: ${target}`);
  const targetRules = [...new Set(readRules(target))];
  console.log(`  Loaded ${targetRules.length} unique target rules`);

  console.log(`\nLoading base files...`);
  const baseRules = [...new Set(baseList.flatMap(filePath => {
    console.log(`  Loading ${filePath}...`);
    const rules = readRules(filePath);
    console.log(`    Loaded ${rules.length} rules`);
    return rules;
  }))];
  console.log(`  Total unique base rules: ${baseRules.length}`);

  const targetSet = new Set(targetRules);
  const baseSet = new Set(baseRules);

  console.log("\nRunning redundancy engine...");
  const combinedFilters = [...targetRules, ...baseRules].join("\n");
  const result = await runEngine(combinedFilters);

  if (!result || !result.results) {
    console.log("No engine results received.");
    process.exit(0);
  }

  // Filter: target rules that are redundant relative to base rules
  const redundantRules = [];
  for (const [red, covering] of Object.entries(result.results)) {
    if (red === covering) continue;
    if (!targetSet.has(red)) continue;

    redundantRules.push({
      red,
      covering,
      confirmedByExactMatch: baseSet.has(covering)
    });
  }

  // Automatically create output directory if it doesn't exist
  fs.mkdirSync(path.dirname(outputPath), { recursive: true });

  // Format report
  const reportBlocks = redundantRules.map(
    e => `${e.red}\n    redundant with:\n    ${e.covering}`
  );

  // Sort to ensure deterministic output for CI/CD pipelines
  reportBlocks.sort();

  // Write report file
  fs.writeFileSync(
    outputPath,
    reportBlocks.join("\n\n") + (reportBlocks.length ? "\n" : ""),
    "utf-8"
  );

  console.log(`\nReport written to: ${outputPath}`);
  console.log(`${redundantRules.length} redundant rule(s) found.`);

  if (redundantRules.length > 0) {
    const exactMatches = redundantRules.filter(l => l.confirmedByExactMatch).length;
    if (exactMatches < redundantRules.length) {
      console.log(`  Note: ${exactMatches} rules directly match base file, ${redundantRules.length - exactMatches} rules transformed/normalized by engine.`);
    }
    redundantRules.forEach(l => console.log(`  - ${l.red}`));
    process.exit(1);
  }

  process.exit(0);
}

main().catch(err => {
  console.error("\nError:");
  console.error(err instanceof Error ? err.stack : err);
  process.exit(1);
});
