#!/usr/bin/env node

/**
 * axe-scan.js — Automated accessibility scanner using axe-core + Playwright
 *
 * Scans one or more URLs for WCAG 2.1 AA violations and outputs structured
 * JSON matching the accessibility-audit-report SKILL.md finding format.
 *
 * Prerequisites:
 *   npm install @axe-core/playwright playwright
 *   npx playwright install chromium
 *
 * Usage:
 *   node axe-scan.js <url1> [url2] [url3] ...
 *   node axe-scan.js https://example.com/checkout https://example.com/cart
 *   node axe-scan.js https://example.com --output results.json
 *   node axe-scan.js https://example.com --tags wcag2a,wcag2aa,wcag21aa
 *   node axe-scan.js https://example.com --include ".main-content"
 *   node axe-scan.js https://example.com --wait 5000
 *
 * Options:
 *   --output <file>     Write JSON to file instead of stdout
 *   --tags <tags>        Comma-separated axe rule tags (default: wcag2a,wcag2aa,wcag21aa)
 *   --include <selector> CSS selector to scope the scan (default: entire page)
 *   --wait <ms>          Wait time in ms after page load before scanning (default: 2000)
 *   --viewport <WxH>     Viewport size (default: 1280x720)
 *
 * Output format (per finding):
 *   {
 *     "url": "https://example.com/checkout",
 *     "criterion": "4.1.2 Name, Role, Value",
 *     "severity": "Critical",
 *     "impact": "critical",
 *     "element": "button.submit-btn",
 *     "html": "<button class=\"submit-btn\"></button>",
 *     "description": "Buttons must have discernible text",
 *     "help": "https://dequeuniversity.com/rules/axe/4.9/button-name",
 *     "ruleId": "button-name"
 *   }
 */

const { chromium } = require("playwright");
const AxeBuilder = require("@axe-core/playwright").default;

// --- Argument parsing ---

function parseArgs(argv) {
  const args = argv.slice(2);
  const config = {
    urls: [],
    output: null,
    tags: ["wcag2a", "wcag2aa", "wcag21aa"],
    include: null,
    wait: 2000,
    viewport: { width: 1280, height: 720 },
  };

  for (let i = 0; i < args.length; i++) {
    switch (args[i]) {
      case "--output":
        config.output = args[++i];
        break;
      case "--tags":
        config.tags = args[++i].split(",").map((t) => t.trim());
        break;
      case "--include":
        config.include = args[++i];
        break;
      case "--wait":
        config.wait = parseInt(args[++i], 10);
        break;
      case "--viewport": {
        const [w, h] = args[++i].split("x").map(Number);
        config.viewport = { width: w, height: h };
        break;
      }
      case "--help":
      case "-h":
        printUsage();
        process.exit(0);
        break;
      default:
        if (args[i].startsWith("http")) {
          config.urls.push(args[i]);
        } else {
          console.error(`Unknown argument: ${args[i]}`);
          process.exit(1);
        }
    }
  }

  if (config.urls.length === 0) {
    console.error("Error: At least one URL is required.\n");
    printUsage();
    process.exit(1);
  }

  return config;
}

function printUsage() {
  console.log(`Usage: node axe-scan.js <url1> [url2] [options]

Options:
  --output <file>       Write JSON to file instead of stdout
  --tags <tags>         Comma-separated axe rule tags (default: wcag2a,wcag2aa,wcag21aa)
  --include <selector>  CSS selector to scope the scan
  --wait <ms>           Wait after page load before scanning (default: 2000)
  --viewport <WxH>      Viewport size (default: 1280x720)
  --help                Show this help message`);
}

// --- Severity mapping ---
// axe-core uses: critical, serious, moderate, minor
// SKILL.md audit report uses: Critical, Major, Minor, Best Practice

function mapSeverity(axeImpact) {
  switch (axeImpact) {
    case "critical":
      return "Critical";
    case "serious":
      return "Major";
    case "moderate":
      return "Minor";
    case "minor":
      return "Best Practice";
    default:
      return "Minor";
  }
}

// --- WCAG criterion mapping ---
// Maps axe-core rule tags to human-readable WCAG criterion references

const WCAG_CRITERIA = {
  "wcag111": "1.1.1 Non-text Content",
  "wcag121": "1.2.1 Audio-only and Video-only",
  "wcag122": "1.2.2 Captions (Prerecorded)",
  "wcag123": "1.2.3 Audio Description or Media Alternative",
  "wcag125": "1.2.5 Audio Description (Prerecorded)",
  "wcag131": "1.3.1 Info and Relationships",
  "wcag132": "1.3.2 Meaningful Sequence",
  "wcag133": "1.3.3 Sensory Characteristics",
  "wcag134": "1.3.4 Orientation",
  "wcag135": "1.3.5 Identify Input Purpose",
  "wcag141": "1.4.1 Use of Color",
  "wcag142": "1.4.2 Audio Control",
  "wcag143": "1.4.3 Contrast (Minimum)",
  "wcag144": "1.4.4 Resize Text",
  "wcag145": "1.4.5 Images of Text",
  "wcag1410": "1.4.10 Reflow",
  "wcag1411": "1.4.11 Non-text Contrast",
  "wcag1412": "1.4.12 Text Spacing",
  "wcag1413": "1.4.13 Content on Hover or Focus",
  "wcag211": "2.1.1 Keyboard",
  "wcag212": "2.1.2 No Keyboard Trap",
  "wcag214": "2.1.4 Character Key Shortcuts",
  "wcag221": "2.2.1 Timing Adjustable",
  "wcag222": "2.2.2 Pause, Stop, Hide",
  "wcag231": "2.3.1 Three Flashes or Below",
  "wcag241": "2.4.1 Bypass Blocks",
  "wcag242": "2.4.2 Page Titled",
  "wcag243": "2.4.3 Focus Order",
  "wcag244": "2.4.4 Link Purpose (In Context)",
  "wcag245": "2.4.5 Multiple Ways",
  "wcag246": "2.4.6 Headings and Labels",
  "wcag247": "2.4.7 Focus Visible",
  "wcag251": "2.5.1 Pointer Gestures",
  "wcag252": "2.5.2 Pointer Cancellation",
  "wcag253": "2.5.3 Label in Name",
  "wcag254": "2.5.4 Motion Actuation",
  "wcag311": "3.1.1 Language of Page",
  "wcag312": "3.1.2 Language of Parts",
  "wcag321": "3.2.1 On Focus",
  "wcag322": "3.2.2 On Input",
  "wcag323": "3.2.3 Consistent Navigation",
  "wcag324": "3.2.4 Consistent Identification",
  "wcag331": "3.3.1 Error Identification",
  "wcag332": "3.3.2 Labels or Instructions",
  "wcag333": "3.3.3 Error Suggestion",
  "wcag334": "3.3.4 Error Prevention (Legal, Financial, Data)",
  "wcag411": "4.1.1 Parsing",
  "wcag412": "4.1.2 Name, Role, Value",
  "wcag413": "4.1.3 Status Messages",
};

function extractCriterion(tags) {
  for (const tag of tags) {
    if (WCAG_CRITERIA[tag]) {
      return WCAG_CRITERIA[tag];
    }
  }
  // Fallback: find any tag matching wcag pattern
  const wcagTag = tags.find((t) => /^wcag\d+$/.test(t));
  if (wcagTag) {
    const digits = wcagTag.replace("wcag", "");
    // Convert "143" to "1.4.3"
    if (digits.length === 3) {
      return `${digits[0]}.${digits[1]}.${digits[2]}`;
    } else if (digits.length === 4) {
      return `${digits[0]}.${digits[1]}.${digits.slice(2)}`;
    }
  }
  return "Unknown";
}

// --- Main scan function ---

async function scanUrl(page, url, config) {
  console.error(`Scanning: ${url}`);

  await page.goto(url, { waitUntil: "networkidle", timeout: 30000 });

  if (config.wait > 0) {
    await page.waitForTimeout(config.wait);
  }

  let builder = new AxeBuilder({ page }).withTags(config.tags);

  if (config.include) {
    builder = builder.include(config.include);
  }

  const results = await builder.analyze();

  const findings = [];

  for (const violation of results.violations) {
    const criterion = extractCriterion(violation.tags);

    for (const node of violation.nodes) {
      findings.push({
        url,
        criterion,
        severity: mapSeverity(node.impact || violation.impact),
        impact: node.impact || violation.impact,
        element: node.target.join(" > "),
        html: node.html,
        description: violation.help,
        help: violation.helpUrl,
        ruleId: violation.id,
      });
    }
  }

  console.error(
    `  Found ${findings.length} issues (${results.violations.length} unique rules violated)`
  );
  return findings;
}

async function main() {
  const config = parseArgs(process.argv);

  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    viewport: config.viewport,
  });

  const allFindings = [];

  try {
    const page = await context.newPage();

    for (const url of config.urls) {
      try {
        const findings = await scanUrl(page, url, config);
        allFindings.push(...findings);
      } catch (err) {
        console.error(`  Error scanning ${url}: ${err.message}`);
        allFindings.push({
          url,
          criterion: "N/A",
          severity: "Error",
          impact: "error",
          element: "N/A",
          html: "N/A",
          description: `Scan failed: ${err.message}`,
          help: "",
          ruleId: "scan-error",
        });
      }
    }
  } finally {
    await browser.close();
  }

  // Summary
  const summary = {
    scanDate: new Date().toISOString(),
    urlsScanned: config.urls.length,
    totalFindings: allFindings.filter((f) => f.severity !== "Error").length,
    bySeverity: {
      Critical: allFindings.filter((f) => f.severity === "Critical").length,
      Major: allFindings.filter((f) => f.severity === "Major").length,
      Minor: allFindings.filter((f) => f.severity === "Minor").length,
      "Best Practice": allFindings.filter((f) => f.severity === "Best Practice")
        .length,
    },
    tags: config.tags,
  };

  const output = JSON.stringify({ summary, findings: allFindings }, null, 2);

  if (config.output) {
    const fs = require("fs");
    fs.writeFileSync(config.output, output);
    console.error(`Results written to ${config.output}`);
  } else {
    console.log(output);
  }

  console.error(
    `\nScan complete. ${summary.totalFindings} findings across ${config.urls.length} URL(s).`
  );
  console.error(
    `  Critical: ${summary.bySeverity.Critical}, Major: ${summary.bySeverity.Major}, Minor: ${summary.bySeverity.Minor}, Best Practice: ${summary.bySeverity["Best Practice"]}`
  );
}

main().catch((err) => {
  console.error(`Fatal error: ${err.message}`);
  process.exit(1);
});
