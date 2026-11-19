const fs = require("node:fs");

function deny(reason) {
  process.stdout.write(JSON.stringify({
    permissionDecision: "deny",
    permissionDecisionReason: reason
  }));
}

try {
  const raw = fs.readFileSync(0, "utf8");

  if (!raw.trim()) {
    throw new Error("Hook received empty input.");
  }

  const event = JSON.parse(raw);

  if (typeof event.toolName !== "string") {
    throw new Error(
      "Expected toolName. Received: " + Object.keys(event).join(", ")
    );
  }

  const toolName = event.toolName.toLowerCase();

  // Inspect terminal tools only.
  if (!/terminal|bash|shell|command|powershell/.test(toolName)) {
    process.stdout.write("{}");
    process.exit(0);
  }

  const args = JSON.stringify(event.toolArgs || {});

  const blockedRules = [
    {
      pattern: /git\s+push[^"]*--force(?:-with-lease)?/i,
      reason: "Force push is blocked by Doc-Sync."
    },
    {
      pattern: /git\s+merge/i,
      reason: "Git merge is blocked by Doc-Sync."
    },
    {
      pattern: /git\s+reset[^"]*--hard/i,
      reason: "Destructive git reset is blocked."
    },
    {
      pattern: /git\s+branch[^"]*-D(?:\s|$)/i,
      reason: "Force branch deletion is blocked."
    },
    {
      pattern: /git\s+add\s+(?:\.|-A|--all)(?:\s|$)/i,
      reason: "Blind staging is blocked. Stage individual files."
    }
  ];

  for (const rule of blockedRules) {
    if (rule.pattern.test(args)) {
      deny(rule.reason);
      process.exit(0);
    }
  }

  // No decision: Copilot continues with normal permission handling.
  process.stdout.write("{}");

} catch (error) {
  console.error("DOC-SYNC HOOK ERROR:", error.message);

  deny("Git safety hook failed. Check its input and configuration.");
}
