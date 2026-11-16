---
name: doc-sync-format
description: Required structure and rules for the generated docs/PROJECT_DOC.md. Use when writing the renderer or testing its output.
---

# PROJECT_DOC.md format
Sections, in order: Name, Description, Languages, Dependencies,
Entry Points, How to Run, Last Commit.

# Rules
- Each section is always present.
- A value that cannot be found is exactly `Not Found`.
- No secrets, tokens, or absolute local paths in the output.
- Output must be deterministic: the same repo gives the same document.