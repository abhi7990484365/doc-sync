---
name: requirements-discovery
description: Turn requirements from the configured Jira or Confluence page into clear, testable requirements and acceptance criteria.
---

# Requirements Discovery

## Purpose

Help the team understand what the business needs and how to test it.

Use the requirement and project context provided. Do not guess missing details.

## Inputs

The Orchestrator fetches the requirement from the configured Jira or Confluence page path and passes the content and source path to the Analyst.

If the source cannot be accessed or important information is missing, ask for clarification. Do not invent requirements or hardcode a project-specific source path in this skill.

## Workflow

### 1. Understand the requirement

Summarize:
- Who needs the capability.
- What they need to do.
- Why it matters.

Ask the user to confirm or correct the summary.

### 2. Clarify gaps

Ask focused questions about unclear behavior, scope, data, users, permissions, and errors. Ask up to five questions at a time.

Keep a short log of questions, answers, and unresolved items.

### 3. Write requirements

Use stable IDs:
- Functional requirements: `FR-001`
- Non-functional requirements: `NFR-001`

Keep each requirement clear and testable. Include its purpose, relevant user or role, expected behavior, and acceptance criteria.

Mark information as **Confirmed**, **Assumption**, **Not Found**, or **Open**. Do not turn assumptions into confirmed requirements.

### 4. Define acceptance criteria

Use Given-When-Then format and IDs such as `AC-001`.

For each requirement, consider:
- Normal and negative scenarios.
- Boundary values and edge cases.
- User roles and permissions.
- Validation and external-service failures.

Include only relevant cases. If expected behavior is unclear, ask instead of guessing.

Link each criterion to its requirement. Do not claim tests have been implemented or executed.

### 5. Review and create the document

Check that requirements match the source, are testable, and identify unresolved questions.

Present the requirements for approval. Create the file only after the user gives the agreed command:

`Create File`

Use the artifact path provided by the Orchestrator. If none is provided, use `docs/requirements.md`.

Include the user story and source, scope, requirements, acceptance criteria, assumptions, open items, and traceability.

Do not modify unrelated files or commit or push changes.

## Boundaries

- Preserve the business intent.
- Do not invent requirements or measurable targets.
- Do not design architecture, create implementation tasks, or write application code.
- Do not start architecture design without separate approval.