---
name: architecture-design
description: Analyze approved Doc-Sync requirements and design, evaluate, validate, and document the technical solution architecture. Use when creating architecture diagrams, defining components, designing integrations, evaluating technology choices, documenting architecture decisions, or preparing architecture.md.
---

# Architecture Design

## Purpose

Convert approved business and software requirements into a clear, maintainable, secure, and scalable technical architecture for the Automated Documentation Sync (Doc-Sync) project.

The Architect Agent defines the role, tools, responsibilities, and decision boundaries.

This skill defines the reusable architecture design procedure.

The Architecture Prompt starts the workflow.

## When to Use

Use this skill when:

- Approved requirements need technical architecture.
- System components and their responsibilities need to be defined.
- API and external integrations need architectural design.
- Data flows and storage requirements need analysis.
- Technology options need evaluation.
- Architecture decisions need documentation.
- An architecture document needs creation or revision.

Do not use this skill to perform requirements discovery, create implementation tasks, or write application code.

## Inputs

Use:

- Approved `docs/requirements.md`.
- Existing project documentation.
- Approved technology constraints.
- Existing architecture documents, if available.
- Stakeholder-approved technical decisions.

If approved requirements are missing, ask the user to complete the requirements phase first.

Never assume that a proposed or unapproved requirements draft is approved.

## Workflow

### 1. Verify Requirements

1. Locate `docs/requirements.md`.
2. Read the complete requirements document.
3. Verify its approval status with the user or workflow evidence.
4. Identify functional and non-functional requirements.
5. Identify scope, constraints, dependencies, and open items.
6. Map requirements to architecture drivers.

Do not proceed if critical requirements are missing or approval cannot be established.

### 2. Identify Architecture Drivers

Identify the requirements that influence architecture decisions, including:

- Security.
- Performance.
- Reliability.
- Scalability.
- Maintainability.
- Availability.
- Integration requirements.
- Deployment constraints.
- Data privacy.

Distinguish confirmed constraints from assumptions and proposed decisions.

### 3. Define High-Level Architecture

Identify:

- System boundaries.
- Major components.
- Component responsibilities.
- External systems.
- Communication patterns.
- Trust boundaries.
- Important integration points.

For Doc-Sync, evaluate relevant components such as:

- GitHub integration.
- Change detection.
- Documentation impact analysis.
- Documentation parsing.
- Documentation update generation.
- Validation.
- Human approval.
- Documentation synchronization.
- Audit logging and reporting.

These are candidate components, not mandatory design decisions. Confirm their necessity against approved requirements.

### 4. Design Component Architecture

For each component, document:

- Component name.
- Purpose.
- Responsibilities.
- Inputs.
- Outputs.
- Dependencies.
- Interfaces.
- Error handling.

Define clear component boundaries and avoid unnecessary coupling.

Every major component must have a clear relationship to at least one approved requirement or documented technical justification.

### 5. Design Integration Architecture

Identify required integrations.

For each integration, document:

- External system.
- Integration purpose.
- Communication mechanism.
- Authentication requirements.
- Data exchanged.
- Error handling.
- Retry and timeout considerations.
- Rate limits and operational constraints, where known.

Do not invent external API capabilities.

Mark unavailable integration details as open questions instead of assuming their behavior.

### 6. Design Data Architecture

Identify:

- Main data entities.
- Relationships.
- Data ownership.
- Data storage requirements.
- Data validation.
- Data lifecycle.
- Retention requirements.
- Sensitive information.
- Audit requirements.

Recommend a storage technology only after evaluating the requirements.

### 7. Evaluate Technology Choices

For major technology decisions:

1. Identify the technical need.
2. List suitable alternatives.
3. Compare advantages and disadvantages.
4. Evaluate security, compatibility, cost, and maintainability.
5. Recommend an option.
6. Document the rationale and trade-offs.

Use the following decision statuses consistently:

- **Proposed:** Recommended but not yet approved.
- **Approved:** Explicitly accepted by the authorized stakeholder.
- **Rejected:** Considered and not selected.
- **Deferred:** Decision postponed until additional information is available.

Do not present proposed technology choices as approved decisions.

### 8. Design Security and Reliability

Evaluate:

- Authentication and authorization.
- Least-privilege access.
- Secret management.
- Secure communication.
- Input validation.
- Logging and auditability.
- Failure handling.
- Retry mechanisms.
- Recovery strategies.
- Availability and scalability.

Identify security trust boundaries and the validation required when data crosses them.

Do not invent security policies or measurable targets.

### 9. Create Architecture Diagrams

Prepare relevant diagrams:

- System context diagram.
- High-level architecture diagram.
- Component diagram.
- Data flow diagram.
- Sequence diagram for important workflows.
- Deployment diagram, when deployment requirements are known.

Use Mermaid where appropriate.

Ensure diagrams match the written architecture.

Do not introduce components or interactions in diagrams that are not explained in the architecture document.

### 10. Document Architecture Decisions

For significant decisions, create Architecture Decision Records (ADRs).

Use IDs:

- ADR-001
- ADR-002
- ADR-003

Each ADR should contain:

- Title.
- Status.
- Context.
- Options considered.
- Decision or recommendation.
- Rationale.
- Consequences.

Use the decision statuses:

- Proposed.
- Approved.
- Rejected.
- Deferred.

Record the rationale and relevant trade-offs. Do not mark a decision Approved without explicit approval.

### 11. Maintain Requirement Traceability

Maintain:

`Requirement -> Architecture Component -> Design Decision`

Identify:

- Requirements without architectural coverage.
- Components without a clear requirement or justification.
- Unresolved architecture decisions.
- Technical constraints that affect implementation.

Use the original requirement IDs from `docs/requirements.md`.

Do not invent requirement IDs or modify approved requirements.

### 12. Identify Risks and Dependencies

Document:

- Technical risks.
- External dependencies.
- Integration risks.
- Security concerns.
- Performance concerns.
- Operational constraints.
- Unresolved technical decisions.

For each significant risk, explain its potential impact and possible mitigation.

Clearly distinguish confirmed risks from risks that depend on unverified assumptions.

### 13. Validate Architecture Quality

Check:

1. Requirements alignment.
2. Completeness.
3. Component boundaries.
4. Integration consistency.
5. Security.
6. Scalability.
7. Reliability.
8. Maintainability.
9. Technical feasibility.
10. Diagram consistency.
11. Requirement traceability.
12. Risks and open decisions.

Report gaps rather than silently making assumptions.

### 14. Prepare for Independent Design Review

Before handing over the architecture:

1. Confirm that the architecture document covers the approved requirements.
2. Verify that architecture diagrams match the written design.
3. Verify component responsibilities and integration boundaries.
4. Check that security and reliability considerations are documented.
5. Identify proposed, approved, rejected, and deferred decisions.
6. List unresolved questions, assumptions, risks, and dependencies.
7. Prepare a summary of areas that require independent review.

The Design Reviewer must independently evaluate the architecture.

The Architect must not perform the independent Design Review or approve its own architecture.

### 15. Obtain Explicit Approval

Present the complete architecture draft to the user.

Include:

- Architecture overview.
- Architecture principles.
- High-level architecture.
- Component responsibilities.
- Integration design.
- Data architecture.
- Security and reliability.
- Technology evaluation.
- Architecture diagrams.
- ADRs.
- Requirement traceability.
- Risks and dependencies.
- Open decisions.
- Design Review Preparation Notes.

Create or modify a file only after the user explicitly types:

`Create File`

General confirmations such as "looks good" or "continue" are not file-creation approval.

### 16. Create Architecture Document

After receiving `Create File`:

1. Use the workflow artifact directory supplied by the prompt or orchestrator.
2. Otherwise use `docs/architecture.md`.
3. Do not create multiple competing architecture documents.
4. Preserve traceability to approved requirements.
5. Clearly label proposed and approved decisions.
6. Include Design Review Preparation Notes.
7. Do not write application source code.
8. Do not modify unrelated files.
9. Do not commit or push changes.

After creating the document, report the file path and summarize the architecture.

Hand over the completed architecture to the Design Reviewer for independent evaluation.

Do not automatically start the next phase.

## Expected Architecture Document

Use these sections:

1. Document Information.
2. Architecture Overview.
3. Architecture Goals and Principles.
4. Architecture Drivers.
5. System Context.
6. High-Level Architecture.
7. Component Architecture.
8. Component Responsibilities.
9. Integration Architecture.
10. API Design Overview.
11. Data Architecture.
12. Security Architecture.
13. Error Handling and Reliability.
14. Scalability and Performance.
15. Deployment Architecture.
16. Architecture Decision Records.
17. Requirement Traceability Matrix.
18. Technical Risks and Dependencies.
19. Assumptions and Constraints.
20. Open Architecture Decisions.
21. Design Review Preparation Notes.

Include only sections relevant to the approved requirements. Where information is unavailable, clearly mark it as an assumption, open question, or not applicable instead of inventing details.

## Rules and Boundaries

- Follow approved requirements.
- Never invent technical constraints or external API capabilities.
- Clearly distinguish proposed decisions from approved decisions.
- Prefer simple and maintainable designs.
- Explain major technology choices.
- Do not change approved business requirements.
- Do not create implementation tasks.
- Do not write application source code.
- Do not perform the independent Design Review.
- Do not approve your own architecture.
- Do not commit, push, merge, or create pull requests.
- Do not start development without separate user approval.