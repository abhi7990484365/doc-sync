---
name: architecture-design
description: Design and document a technical architecture from approved Doc-Sync requirements.
---

# Architecture Design

## Purpose

Turn approved requirements into a clear, practical architecture for Doc-Sync.

Use this skill for architecture design and documentation. Do not use it for requirements discovery, implementation planning, coding, or independent design review.

## Inputs

Use:
- Approved requirements from `docs/requirements.md`.
- Existing project documentation and architecture.
- Approved technical constraints and decisions.

The Orchestrator provides the requirement source and workflow context. Do not hardcode a project-specific Jira or Confluence path.

If requirements are missing, approval is unclear, or critical details are unresolved, stop and ask for clarification.

## Workflow

### 1. Understand the requirements

Identify the system’s goals, scope, constraints, integrations, and quality needs.

Keep confirmed requirements separate from assumptions and open questions. Do not change approved requirements or invent missing details.

### 2. Design the architecture

Define the system boundaries, main components, responsibilities, interfaces, data flows, and external integrations.

For each major component, explain its purpose, inputs, outputs, and dependencies. Include only components supported by the requirements or a clear technical need.

Consider security, reliability, performance, maintainability, and deployment needs. Do not invent API capabilities, security policies, or measurable targets.

### 3. Evaluate important decisions

Compare suitable options when a decision affects the design. Explain the recommendation and its trade-offs.

Label decisions as **Proposed**, **Approved**, **Rejected**, or **Deferred**. Do not mark a decision approved without explicit approval.

Create an ADR for significant decisions. Keep the format simple: context, options, decision, and rationale.

### 4. Check traceability and risks

Use the original requirement IDs to show:

`Requirement → Architecture Component → Decision`

Identify uncovered requirements, unnecessary components, risks, dependencies, and open decisions. Mark unknown details as open questions instead of guessing.

### 5. Prepare the architecture draft

Include the sections that apply:
- Overview and goals
- System and component architecture
- Integrations and data flow
- Security and reliability
- Technology decisions and trade-offs
- Diagrams, where useful
- Requirement traceability
- Risks, assumptions, and open questions

Use Mermaid when a diagram helps explain the design. Keep diagrams consistent with the written architecture.

Present the draft for approval and independent design review. The Architect must not review or approve its own design.

### 6. Create the document

Create or update the architecture file only after the user explicitly types:

`Create File`

Use the artifact path provided by the Orchestrator. If none is provided, use `docs/architecture.md`.

Do not create duplicate architecture documents, modify unrelated files, write application code, or commit or push changes.

After creating the document, report its path and summarize the design. Hand it to the Design Reviewer and do not start the next phase automatically.

## Boundaries

- Follow approved requirements and preserve their intent.
- Keep the design simple and maintainable.
- Do not invent facts or present proposals as approved decisions.
- Do not create implementation tasks or write application code.
- Do not perform or approve the independent design review.
- Do not commit, push, merge, or create pull requests.
- Do not start development without separate approval.