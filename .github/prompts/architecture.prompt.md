---
description: Propose the high-level architecture from requirements.md.
agent: architect
---

Workflow artifact directory: ${input:workflowDir:optional workflow artifact directory; leave blank to use docs/}

Read `requirements.md` from the supplied workflow artifact directory, or
`docs/requirements.md` if no directory was supplied. Propose a high-level
architecture.

Ask me up to 5 clarifying questions first if anything affects the design,
then create `architecture.md` in the supplied workflow artifact directory, or
`docs/architecture.md` if no directory was supplied. Use this structure:

# Architecture
## 1. Overview  (what the system does, in 3-4 lines)
## 2. Components  (name, responsibility, inputs, outputs for each)
## 3. Component Diagram  (Mermaid)
## 4. Data Flow  (step by step, plus a Mermaid sequence or flow diagram)
## 5. Technology Choices  (choice, reason, alternative considered)
## 6. Requirement Traceability  (table: requirement ID -> component)
## 7. Error Handling and Security  (API failures, missing data, secrets)
## 8. Risks and Open Questions

Keep it simple. No code. Write the file to disk when done.