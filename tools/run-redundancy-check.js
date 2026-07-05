/**
 * run-redundancy-check.js — Find ABPindo rules redundant with EasyList
 *
 * Combines both filter lists, runs ABPVN redundant.js engine (full ABP syntax),
 * reports ABPindo rules covered by EasyList.
 *
 * Usage:
 *   node tools/run-redundancy-check.js                    # auto-download EasyList
 *   node tools/run-redundancy-check.js --easylist path    # use cached
 *
 * Output: src/redundant.txt (one "A is redundant with B" per line)
 * Exit: 1 if redundancies found, 0 otherwise
 */
"use strict";

const fs = require("fs");
const path = require("path");
const https = require("https");
const { Worker } = require("worker_threads");

const EASYLIST_URL = "https://easylist.to/easylist/easylist.txt";
const ENGINE_PATH = path.join(__dirname, "abpvn-redundant.js");
const SRC_DIR = path.resolve(__dirname, "..", "src");
const OUTPUT = path.resolve(__dirname, "..", "src", "redundant.txt");

function download(url, dest) {
  return new Promise((resolve, reject) => {
    const file = fs.createWriteStream(dest);
    https.get(url, { headers: { "User-Agent": "ABPindo-redundancy-check" } }, (res) => {
      if (res.statusCode !== 200) { reject(new Error(`HTTP ${res.statusCode}`)); return; }
      res.pipe(file);
      file.on("finish", () => file.close(resolve));
    }).on("error", reject);
  });
}

function readRules(filepath) {
  const content = fs.readFileSync(filepath, "utf-8");
  const rules = [];
  for (const line of content.split("\n")) {
    const t = line.trim();
    if (!t || t.startsWith("!") || t.startsWith("[") || t.startsWith("#")) continue;
    rules.push(t);
  }
  return rules;
}

function readAllFilters(dir) {
  const files = fs.readdirSync(dir, { recursive: true })
    .filter(f => f.endsWith(".txt") && path.basename(f) !== "redundant.txt")
    .map(f => path.join(dir, f))
    .sort();
  return files.flatMap(fp => readRules(fp));
}

function runEngine(combinedFilters) {
  const engineCode = fs.readFileSync(ENGINE_PATH, "utf-8");
  // Worker: override self to capture postMessage, call startWorker directly
  const workerCode = `
const { parentPort } = require("worker_threads");
// Capture engine output
let engineResult = null;
const self = {
  postMessage: (r) => { engineResult = r; },
  close: () => {},
  addEventListener: () => {}
};
globalThis.self = self;
// Engine code follows
${engineCode}
// Feed data and run
const data = { filters: ${JSON.stringify(combinedFilters)}, modifiers: {} };
// The engine's message listener would call startWorker(e.data)
// Call startWorker directly instead
startWorker(data);
// Send result back
parentPort.postMessage(engineResult);
`;
  return new Promise((resolve, reject) => {
    const worker = new Worker(workerCode, { eval: true });
    worker.on("message", resolve);
    worker.on("error", reject);
    worker.on("exit", (code) => {
      if (code !== 0) reject(new Error(`Worker exit ${code}`));
    });
  });
}

async function main() {
  const args = process.argv.slice(2);
  const elFlag = args.indexOf("--easylist");
  let elPath;

  if (elFlag >= 0 && args[elFlag + 1]) {
    elPath = path.resolve(args[elFlag + 1]);
    if (!fs.existsSync(elPath)) {
      console.error(`Error: ${elPath} not found`); process.exit(1);
    }
  } else {
    elPath = path.join(__dirname, "..", ".easylist_tmp.txt");
    console.log("Downloading EasyList...");
    await download(EASYLIST_URL, elPath);
  }

  console.log("Reading ABPindo filters...");
  const abpindoRules = readAllFilters(SRC_DIR);
  console.log(`  ${abpindoRules.length} ABPindo rules`);

  console.log("Reading EasyList...");
  const elRules = readRules(elPath);
  console.log(`  ${elRules.length} EasyList rules`);
  if (elFlag < 0) fs.unlinkSync(elPath);

  const abpSet = new Set(abpindoRules);
  const elSet = new Set(elRules);

  // Run engine on combined list
  console.log("Running redundancy engine...");
  const result = await runEngine([...abpindoRules, ...elRules].join("\n"));

  if (!result || !result.results) {
    console.log("No engine results"); process.exit(0);
  }

  // Filter: only ABPindo rules covered by EasyList
  const lines = [];
  for (const [red, covering] of Object.entries(result.results)) {
    if (red === covering) continue;
    if (!abpSet.has(red)) continue;
    const isEasyList = elSet.has(covering);
    lines.push({ red, covering, confirmed: elSet.has(covering) });
  }

  // Write report
  const reportLines = lines.map(e => `${e.red} is redundant with ${e.covering}`);
  reportLines.push(""); // trailing newline
  fs.writeFileSync(OUTPUT, reportLines.join("\n"), "utf-8");

  console.log(`\nReport: ${OUTPUT}`);
  console.log(`${lines.length} redundant ABPindo rule(s) found.`);

  const confirmed = lines.filter(l => l.confirmed).length;
  if (confirmed < lines.length)
    console.log(`  ${confirmed} confirmed EasyList, ${lines.length - confirmed} unconfirmed (engine-transformed)`);

  lines.forEach(l => console.log(`  ${l.red}`));
  if (lines.length > 0) process.exit(1);
}

main().catch(err => { console.error(err); process.exit(1); });
