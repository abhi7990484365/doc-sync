
const fs = require("node:fs");
const path = require("node:path");
const { spawnSync } = require("node:child_process");

function output(context) {
  process.stdout.write(JSON.stringify({
    additionalContext: context
  }));
}

function readEvent() {
  return JSON.parse(fs.readFileSync(0, "utf8"));
}

function findFilePath(value) {
  const preferredKeys = [
    "filePath",
    "file_path",
    "path",
    "targetFile",
    "target_file",
    "filename",
    "file"
  ];

  if (!value || typeof value !== "object") {
    return null;
  }

  for (const key of preferredKeys) {
    const candidate = value[key];

    if (typeof candidate === "string" && candidate.trim()) {
      return candidate;
    }
  }

  for (const child of Object.values(value)) {
    if (child && typeof child === "object") {
      const result = findFilePath(child);
      if (result) return result;
    }
  }

  return null;
}

function runNodeCheck(filePath, cwd) {
  return spawnSync(process.execPath, ["--check", filePath], {
    cwd,
    encoding: "utf8",
    timeout: 15000,
    windowsHide: true
  });
}

function runPythonCheck(filePath, cwd) {
  const source = fs.readFileSync(filePath, "utf8");

  const result = spawnSync(
    "python",
    [
      "-c",
      "import ast,sys; ast.parse(sys.stdin.read(), filename=sys.argv[1])",
      filePath
    ],
    {
      cwd,
      input: source,
      encoding: "utf8",
      timeout: 15000,
      windowsHide: true
    }
  );

  return result;
}

function validateJson(filePath) {
  JSON.parse(fs.readFileSync(filePath, "utf8"));
}

function validateMarkdown(filePath) {
  const content = fs.readFileSync(filePath, "utf8");
  const issues = [];

  if (/[ \t]+$/m.test(content)) {
    issues.push("Trailing whitespace detected.");
  }

  const fenceCount = (content.match(/^```/gm) || []).length;

  if (fenceCount % 2 !== 0) {
    issues.push("Unclosed Markdown code fence detected.");
  }

  return issues;
}

function main() {
  const event = readEvent();

  const toolName = event.toolName || event.tool_name || "";
  const toolResult = event.toolResult || event.tool_result || {};

  if (!/^(edit|create)$/i.test(toolName)) {
    output("Doc-Sync validation skipped: not a file edit or creation tool.");
    return;
  }

  const resultType =
    toolResult.resultType || toolResult.result_type || "success";

  if (resultType !== "success") {
    output("Doc-Sync validation skipped because the file operation did not succeed.");
    return;
  }

  const args = event.toolArgs || event.tool_input || {};
  const cwd = event.cwd || process.cwd();
  const relativePath = findFilePath(args);

  if (!relativePath) {
    output(
      "Doc-Sync validation could not identify the changed file path. " +
      "Please inspect the changed file and run its relevant checks manually."
    );
    return;
  }

  const absolutePath = path.resolve(cwd, relativePath);
  const relativeToWorkspace = path.relative(cwd, absolutePath);

  if (
    relativeToWorkspace.startsWith("..") ||
    path.isAbsolute(relativeToWorkspace)
  ) {
    output("Doc-Sync validation skipped: the file is outside the workspace.");
    return;
  }

  if (!fs.existsSync(absolutePath) || !fs.statSync(absolutePath).isFile()) {
    output("Doc-Sync validation skipped: the changed file could not be found.");
    return;
  }

  const extension = path.extname(absolutePath).toLowerCase();
  const failures = [];
  const messages = [];

  try {
    if ([".js", ".cjs", ".mjs"].includes(extension)) {
      const result = runNodeCheck(absolutePath, cwd);

      if (result.error || result.status !== 0) {
        failures.push(result.stderr || result.error?.message || "Node syntax check failed.");
      } else {
        messages.push("JavaScript syntax check passed.");
      }
    } else if (extension === ".py") {
      const result = runPythonCheck(absolutePath, cwd);

      if (result.error || result.status !== 0) {
        failures.push(result.stderr || result.error?.message || "Python syntax check failed.");
      } else {
        messages.push("Python syntax check passed.");
      }
    } else if (extension === ".json") {
      validateJson(absolutePath);
      messages.push("JSON syntax check passed.");
    } else if (extension === ".md") {
      const issues = validateMarkdown(absolutePath);

      if (issues.length) {
        failures.push(...issues);
      } else {
        messages.push("Basic Markdown checks passed.");
      }
    } else {
      messages.push(
        `No automatic syntax check is configured for ${extension || "this file type"}.`
      );
    }
  } catch (error) {
    failures.push(error.message);
  }

  const report = [
    `Doc-Sync validation: ${path.relative(cwd, absolutePath)}`,
    ...messages.map(item => `PASS: ${item}`),
    ...failures.map(item => `CHECK REQUIRED: ${item}`),
    "This validation is a lightweight check, not a replacement for the Tester phase."
  ].join("\n");

  output(report);
}

try {
  main();
} catch (error) {
  output(
    `Doc-Sync validation hook encountered an error: ${error.message}. ` +
    "Run the relevant validation manually."
  );
}
