---
description: Analyze approved Doc-Sync requirements, design and validate the technical architecture, and create an approved architecture document.
agent: architect
---

Workflow artifact directory: ${input:workflowDir:Optional workflow artifact directory; leave blank to use docs/}

# Objective

Create a complete, technically feasible, secure, maintainable, and traceable architecture document for the Automated Documentation Sync (doc-sync) project.

# Configuration References

Before starting:

1. Follow `.github/copilot-instructions.md`.
2. Read `.github/instructions/architect.instructions.md`.
3. Follow `.github/skills/architecture-design/SKILL.md`.
4. Follow the responsibilities and boundaries in `.github/agents/architect.agent.md`.

The Architect Agent owns the architecture analysis. The Skill defines the reusable architecture procedure. This Prompt starts the workflow and supplies task-specific inputs.

# Workflow

## Step 1: Obtain Approved Requirements

Read:

`docs/requirements.md`

If the file is unavailable, ask the user to complete the Analyst phase first.

Verify that the requirements have been approved. If approval cannot be established, ask the user to confirm before proceeding.

Read relevant existing project documentation when available.

Do not assume that a draft requirements document is approved.

## Step 2: Understand Requirements

Identify:

- Business objectives.
- Functional requirements.
- Non-functional requirements.
- Business rules.
- Scope and constraints.
- External integrations.
- Security requirements.
- Dependencies and risks.

Summarize the architecture problem and identify the major architecture drivers.

Ask the user for clarification if critical technical requirements are missing.

Do not invent technical requirements to fill gaps.

## Step 3: Define High-Level Architecture

Identify:

- System boundaries.
- Major components.
- Component responsibilities.
- External systems.
- Communication patterns.
- Integration points.
- Trust boundaries.

Consider relevant Doc-Sync capabilities such as:

- GitHub integration.
- Code change detection.
- Documentation impact analysis.
- Documentation parsing.
- Suggested documentation generation.
- Documentation validation.
- Human approval.
- Documentation synchronization.
- Audit logging and reporting.

Treat these as candidate components and validate them against approved requirements.

Do not include a candidate component simply because it appears in this list.

## Step 4: Design Technical Components

For each required component, define:

- Component name.
- Purpose and responsibilities.
- Inputs and outputs.
- Interfaces.
- Dependencies.
- Communication mechanisms.
- Error handling.
- Related requirement IDs.

Avoid unnecessary coupling and duplicate responsibilities.

Clearly identify component boundaries.

## Step 5: Design Integrations and Data

Document applicable areas:

- External API integrations.
- Authentication mechanisms.
- API communication.
- Data entities and relationships.
- Data ownership and lifecycle.
- Storage requirements.
- Validation and error handling.
- Retry and timeout considerations.

Do not invent external API capabilities or database requirements.

Mark missing integration or data decisions as Open.

## Step 6: Evaluate Technology Choices

For major technology decisions:

1. Identify the technical requirement.
2. Evaluate suitable alternatives.
3. Compare advantages and disadvantages.
4. Consider security, compatibility, cost, and maintenance.
5. Recommend an appropriate option.
6. Explain the rationale.

Classify each significant decision as one of:

- Proposed.
- Approved.
- Rejected.
- Deferred.

Do not describe a recommendation as an approved decision without explicit approval.

## Step 7: Design Security and Reliability

Evaluate applicable areas:

- Authentication and authorization.
- Secret management.
- Least-privilege access.
- Secure communication.
- Input validation.
- Logging and auditability.
- Error handling.
- Recovery mechanisms.
- Performance and scalability.

Do not invent measurable targets.

Identify requirements that need further clarification.

## Step 8: Prepare Architecture Diagrams

Create relevant diagrams using Mermaid where appropriate:

- System context diagram.
- High-level architecture diagram.
- Component diagram.
- Data flow diagram.
- Sequence diagram.
- Deployment diagram when deployment requirements are known.

Ensure diagrams are consistent with the architecture description.

Do not include unsupported components or integrations in diagrams.

## Step 9: Document Architecture Decisions

Create ADRs for significant decisions.

Use IDs:

`ADR-001`, `ADR-002`, etc.

Include:

- Context.
- Options considered.
- Decision.
- Rationale.
- Consequences.
- Decision status.

Clearly distinguish proposed decisions from approved decisions.

Do not invent stakeholder approval.

## Step 10: Validate Architecture

Verify:

- Requirements alignment.
- Component responsibilities.
- Integration boundaries.
- Security considerations.
- Scalability and reliability.
- Maintainability.
- Technical feasibility.
- Diagram consistency.
- Requirement traceability.
- Technical risks and open decisions.

Check that:

- Every in-scope requirement has an architectural response.
- Every major component has a clear responsibility.
- External integrations have defined boundaries.
- Unresolved technical decisions are visible.
- No unapproved functionality has been introduced.

Present any gaps and unresolved decisions.

## Step 11: Prepare for Design Review

Before finalizing the architecture draft, prepare it for the next SDLC phase: Design Review.

Include:

- Architecture components requiring review.
- Security and trust boundaries.
- Integration risks.
- Failure scenarios.
- Data flow concerns.
- Proposed architecture decisions.
- Known technical limitations.
- Open design questions.

Do not perform the independent Design Review yourself.

The Design Reviewer Agent will independently evaluate the architecture in the next phase.

## Step 12: Present Architecture Draft

Present the complete architecture document for user review.

Include:

1. Architecture Overview.
2. Architecture Goals and Principles.
3. Architecture Drivers.
4. System Context.
5. High-Level Architecture.
6. Component Architecture.
7. Component Responsibilities.
8. Integration Architecture.
9. API Design Overview, when applicable.
10. Data Architecture, when applicable.
11. Security Architecture.
12. Error Handling and Reliability.
13. Scalability and Performance.
14. Deployment Architecture, when known.
15. Architecture Decision Records.
16. Requirement Traceability Matrix.
17. Technical Risks and Dependencies.
18. Assumptions and Constraints.
19. Open Architecture Decisions.
20. Design Review Preparation Notes.

Clearly identify proposed decisions and unresolved items.

Do not create or modify files during this phase.

## Step 13: Obtain Explicit Approval

Ask the user to review the complete architecture draft.

The exact file-creation approval command is:

`Create File`

Rules:

- Do not treat "looks good", "approved", or "continue" as permission to create files.
- If the user requests changes, revise the draft and present it again.
- Do not create or modify files until the exact command is received.

## Step 14: Create architecture.md

Only after receiving `Create File`:

- Use the supplied workflow artifact directory if provided.
- Otherwise create `docs/architecture.md`.
- Do not create duplicate architecture documents.
- Preserve traceability to approved requirements.
- Clearly label proposed decisions and unresolved items.
- Follow the Architect instructions and Architecture Design Skill.
- Do not write application source code.
- Do not modify unrelated files.

## Step 15: Completion Report

After successful file creation:

1. State the exact file path.
2. Summarize the architecture.
3. List proposed and approved decisions.
4. List unresolved technical decisions.
5. Identify technical risks and dependencies.
6. Confirm whether the document was successfully created.
7. Confirm that the architecture is ready for independent Design Review, or list blockers.
8. Remind the user to review and commit it.

Do not commit, push, merge, or create a pull request.

Do not start development or planning automatically.

Wait for separate user approval before moving to the next SDLC phase.

# Boundaries

- Do not perform requirements discovery.
- Do not change approved business requirements.
- Do not invent technical constraints.
- Do not write application source code.
- Do not create implementation tasks.
- Do not perform the independent Design Review.
- Do not modify unrelated files.
- Do not bypass human approval.
- Do not start the next SDLC phase automatically.

Prioritize technical feasibility, simplicity, security, maintainability, and requirements traceability.