
const fs = require("node:fs");

function readEvent() {
  const input = fs.readFileSync(0, "utf8");

  if (!input.trim()) {
    throw new Error("Missing hook event input.");
  }

  return JSON.parse(input);
}

function collectStrings(value, results = []) {
  if (typeof value === "string") {
    results.push(value);
  } else if (Array.isArray(value)) {
    for (const item of value) {
      collectStrings(item, results);
    }
  } else if (value && typeof value === "object") {
    for (const item of Object.values(value)) {
      collectStrings(item, results);
    }
  }

  return results;
}

function isTerminalTool(toolName) {
  return /terminal|bash|shell|command|powershell/i.test(toolName);
}

function findBlockedOperation(command) {
  const normalized = command
    .replace(/\\\s*\n/g, " ")
    .replace(/\s+/g, " ")
    .trim();

  const blockedRules = [
    {
      pattern: /\bgit\s+push\b[^;&|]*?(--force-with-lease|--force\b|-f\b)/i,
      reason: "Force-pushing is not allowed by the Doc-Sync safety hook."
    },
    {
      pattern: /\bgit\s+push\b[^;&|]*?\b(main|master|refs\/heads\/(main|master))\b/i,
      reason: "Direct pushes to main or master are not allowed."
    },
    {
      pattern: /\bgit\s+merge\b/i,
      reason: "Merging branches requires a separate explicit workflow."
    },
    {
      pattern: /\bgit\s+branch\b[^;&|]*?\s-D\b/i,
      reason: "Force-deleting branches is not allowed."
    },
    {
      pattern: /\bgit\s+reset\b[^;&|]*?--hard\b/i,
      reason: "git reset --hard can discard user changes."
    },
    {
      pattern: /\bgit\s+clean\b[^;&|]*?-[a-z]*f[a-z]*d/i,
      reason: "Destructive git clean operations are not allowed."
    },
    {
      pattern: /\bgit\s+checkout\b[^;&|]*?--\s+(\.|:\s*\/)/i,
      reason: "Discarding tracked changes through git checkout is not allowed."
    },
    {
      pattern: /\bgit\s+restore\b[^;&|]*?(--worktree\b|--staged\b)?\s+(\.|:\s*\/)/i,
      reason: "Restoring the entire working tree or index is not allowed."
    },
    {
      pattern: /\bgit\s+add\s+(-A|--all|\.)\s*(?:$|[;&|])/i,
      reason: "Blindly staging the entire repository is not allowed. Stage approved files individually."
    }
  ];

  for (const rule of blockedRules) {
    if (rule.pattern.test(normalized)) {
      return rule.reason;
    }
  }

  return null;
}

function main() {
  const event = readEvent();

  const toolName = event.toolName;

  if (typeof toolName !== "string") {
    process.stdout.write("{}");
    return;
  }

  if (!isTerminalTool(toolName)) {
    process.stdout.write("{}");
    return;
  }

  const commandValues = collectStrings(event.toolArgs);
  const commandText = commandValues.join("\n");

  const reason = findBlockedOperation(commandText);

  if (reason) {
    process.stdout.write(
      JSON.stringify({
        permissionDecision: "deny",
        permissionDecisionReason: reason
      })
    );
    return;
  }

  process.stdout.write("{}");
}

try {
  main();
} catch (error) {
  // Fail closed if the hook cannot inspect the event safely.
  process.stdout.write(
    JSON.stringify({
      permissionDecision: "deny",
      permissionDecisionReason:
        "Doc-Sync Git safety check could not inspect this tool call. Review the hook input and configuration."
    })
  );
}
