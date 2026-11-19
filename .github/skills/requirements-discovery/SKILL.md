---
name: requirements-discovery
description: Elicit, clarify, analyze, validate, and document business and software requirements for the Automated Documentation Sync (doc-sync) project. Use when analyzing user stories, asking stakeholder questions, defining functional and non-functional requirements, writing acceptance criteria, maintaining a clarification log, or creating requirements.md.
---

# Requirements Discovery

## Purpose

Turn stakeholder-provided user stories into clear, complete, testable, and traceable requirements.

This skill defines the reusable requirements process. The Analyst Agent defines the role, tools, and authority boundaries. The requirements prompt starts the workflow.

## When to Use

Use when a user story or business requirement needs analysis, clarification, refinement, acceptance criteria, traceability, or a requirements document.

Do not use this skill to design technical architecture, create implementation plans, or write application code.

## Inputs

Use user-provided pasted text, attached documents, JIRA issues, Confluence pages, and relevant existing project requirements.

Retrieve external source content only through configured tools. If a source cannot be accessed, explain the limitation and ask the user to provide its content. Never claim to have read inaccessible material.

## Workflow

### 1. Obtain and verify the source

1. Check whether the user provided a story.
2. If not, ask for the story and its source.
3. Retrieve JIRA or Confluence content using configured tools when available.
4. Preserve the original story wording and source reference.
5. Do not add details absent from the source.

### 2. Summarize the story

Summarize in exactly three concise lines:
1. Who needs the capability.
2. What they need to do.
3. Why they need it or the expected outcome.

Ask the user to confirm or correct the summary before continuing.

### 3. Ask clarification questions

Identify missing, ambiguous, conflicting, or unverifiable information.

Ask no more than five questions per batch. Group relevant questions under:
- Business scope and objectives.
- Users and stakeholders.
- Inputs, outputs, and data.
- Functional behavior and business rules.
- Error handling and recovery.
- Security, privacy, and permissions.
- Performance, reliability, and availability.
- Constraints, dependencies, and integrations.

For each question, explain why the answer matters. Offer possible answers only as examples, allow custom answers, and wait for the user's response before asking the next batch. Do not repeat questions already answered.

Maintain a clarification log containing the question, user's answer, and confirmed or unresolved status.

### 4. Separate confirmed facts from unknowns

Classify information as:
- **Confirmed:** explicitly provided or approved by the user.
- **Assumption:** provisional interpretation requiring confirmation.
- **Not Found:** absent from available sources and not supplied by the user.
- **Open:** a decision that remains unresolved.

Never convert assumptions or Not Found items into confirmed requirements. Do not invent numeric performance, availability, capacity, or retention targets.

### 5. Derive requirements

#### Functional requirements

Assign stable IDs: `FR-001`, `FR-002`, and so on.

Each requirement should include:
- ID and title.
- Clear, testable requirement statement.
- Business justification.
- Actor.
- Preconditions.
- Expected behavior and outcome.
- Priority, if supplied or agreed.
- Acceptance criteria.

Use one principal behavior per requirement where practical. Avoid vague terms unless they are defined measurably.

#### Non-functional requirements

Assign stable IDs: `NFR-001`, `NFR-002`, and so on.

Consider relevant attributes:
- Security and access control.
- Privacy and data handling.
- Performance.
- Reliability and recovery.
- Scalability.
- Maintainability.
- Usability and accessibility.
- Observability and auditability.

Include measurable targets only when supplied or approved. Otherwise record them as `Not Found` and add them to Open Items.

#### Business rules and scope

Capture business rules separately from implementation choices. Clearly distinguish in-scope, out-of-scope, and deferred items. Do not expand scope without confirmation.

### 6. Define acceptance criteria

Write criteria in Given-When-Then form. Cover relevant happy paths, negative behavior, boundaries, edge cases, validation failures, authorization, and external-service failures.

Assign stable IDs such as `AC-001`. Map each criterion to at least one requirement. Do not define expected behavior for an unresolved business rule; record it as an open question.

### 7. Maintain traceability

Create the relationship:

`User Story -> Requirement -> Acceptance Criterion -> Test Scenario`

Use stable IDs:
- User story: `US-001` where needed.
- Functional requirement: `FR-001`.
- Non-functional requirement: `NFR-001`.
- Acceptance criterion: `AC-001`.
- Test scenario: `TC-001`.

Identify requirements without acceptance criteria, criteria without a parent requirement, and requirements that cannot yet be tested. Do not claim test cases have been implemented or executed during requirements discovery.

### 8. Review requirements quality

Check:
1. Completeness.
2. Clarity.
3. Consistency.
4. Testability.
5. Traceability.
6. Scope control.
7. Source fidelity.
8. Visibility of assumptions and unknowns.

Report issues; do not silently change stakeholder decisions.

### 9. Obtain explicit approval

Present the consolidated requirements, including story summary, scope, functional and non-functional requirements, business rules, acceptance criteria, clarification log, assumptions, constraints, risks, dependencies, open items, and traceability matrix.

Create a file only after the user gives the exact approval command required by the active requirements prompt and Analyst Agent. For this project, the agreed command is:

`Create File`

Do not treat "looks good", "continue", or other general confirmations as permission to write files.

### 10. Create the requirements document

After receiving `Create File`:
1. Use the workflow artifact directory supplied by the prompt or orchestrator.
2. If no directory is supplied, use `docs/requirements.md`.
3. Do not create multiple competing requirements documents.
4. Preserve the original story and source reference.
5. Clearly label unknowns.
6. Do not write application code or modify unrelated files.
7. Do not commit or push changes.

The document should contain:
1. Document Information.
2. User Story and Source.
3. Business Overview and Objectives.
4. Goal and Scope.
5. Stakeholders and User Roles.
6. Functional Requirements.
7. Non-Functional Requirements.
8. Business Rules.
9. End-to-End Business Workflow.
10. Acceptance Criteria.
11. Assumptions and Constraints.
12. Clarification Log.
13. Negative Scenarios and Edge Cases.
14. Dependencies and Risks.
15. Open Items.
16. Requirement Traceability Matrix.

### 11. Report completion

State the exact file path, summarize the contents, list unresolved Not Found items, and confirm whether the file was successfully written. Remind the user to review and commit it. Do not start architecture design without separate approval.

## Rules and Boundaries

- Be accurate, neutral, and concise.
- Use plain language and testable statements.
- Preserve original business intent.
- Never invent requirements, stakeholder answers, source content, or measurable targets.
- Do not design architecture or select implementation technologies.
- Do not create implementation tasks or source code.
- Do not modify unrelated files.
- Do not commit, push, merge, or create a pull request.
- Respect the Analyst Agent's tool permissions and human approval boundaries.