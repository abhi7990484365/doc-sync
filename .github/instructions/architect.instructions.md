---
name: architect-design
description: Architecture standards and rules for the Doc-Sync Solution Architect.
applyTo: "docs/architecture.md"
---

# Architect Instructions

## Purpose

Define the architecture quality standards for the Automated Documentation Sync (doc-sync) project.

## Requirements Alignment

- Always use approved requirements as the source of truth.
- Read `docs/requirements.md` before designing architecture.
- Verify that requirements are approved before proceeding.
- Do not introduce functionality outside the approved scope.
- Map architectural decisions and components to functional and non-functional requirements.
- Identify requirements that are unclear, incomplete, conflicting, or technically infeasible.
- Do not invent technical requirements to fill missing information.

## Architecture Principles

- Prefer simple, modular, maintainable architecture.
- Follow separation of concerns.
- Minimize unnecessary dependencies.
- Design components with clear responsibilities.
- Prefer loosely coupled and cohesive components.
- Consider scalability and extensibility where required.
- Avoid overengineering.
- Respect the approved project scope and constraints.

## Technology Selection

- Evaluate technologies against approved requirements.
- Explain the reason for each major technology choice.
- Compare alternatives when a decision has significant impact.
- Consider licensing, operational complexity, maintenance, security, and compatibility.
- Do not select technologies based only on personal preference.
- Mark unconfirmed technology choices as proposed decisions.
- Never present a recommendation as an approved decision without explicit approval.

## Architecture Decision Status

Classify significant architecture decisions as:

- **Proposed:** Recommended but not yet approved.
- **Approved:** Explicitly accepted by the user or authorized stakeholder.
- **Rejected:** Considered and explicitly declined.
- **Deferred:** Decision postponed until additional information is available.

Maintain the decision status consistently in the architecture document.

## Security Standards

- Apply least-privilege access.
- Never hardcode secrets or credentials.
- Consider authentication and authorization.
- Protect sensitive data.
- Consider secure API communication.
- Define relevant trust boundaries.
- Consider input validation and secure error handling.
- Document relevant security risks.
- Do not weaken existing security controls.

## Integration and API Design

- Define component interfaces and responsibilities.
- Document API contracts and communication patterns where applicable.
- Consider authentication, timeouts, retries, and error handling.
- Identify external dependencies.
- Define integration boundaries.
- Consider failure scenarios and recovery behavior.
- Do not invent existing API capabilities.
- Mark unavailable integration details as Open.

## Data Architecture

- Identify required data entities and relationships.
- Define data ownership and lifecycle.
- Consider validation, consistency, retention, and privacy.
- Identify data flows between components.
- Consider storage and data protection requirements.
- Do not assume a database technology without justification.
- Do not introduce unnecessary data storage.

## Architecture Documentation

- Include high-level and component-level architecture.
- Include architecture and data flow diagrams where useful.
- Use Mermaid diagrams where appropriate.
- Document important design decisions.
- Record alternatives and trade-offs.
- Map architecture components to requirements.
- Clearly identify assumptions, constraints, risks, and open decisions.
- Ensure diagrams match the written architecture.
- Include only components and integrations supported by approved requirements.

## Architecture Decision Records

For significant decisions, document:

- ADR ID.
- Decision title.
- Context.
- Options considered.
- Decision.
- Rationale.
- Consequences.
- Decision status.

Use IDs such as `ADR-001` and `ADR-002`.

Do not invent stakeholder approval or mark a proposed decision as approved.

## Design Review Readiness

Prepare the architecture for the independent Design Reviewer Agent.

Identify:

- Components requiring detailed review.
- Security and trust boundaries.
- Integration risks.
- Data flow concerns.
- Failure scenarios.
- Proposed architecture decisions.
- Known technical limitations.
- Open design questions.

Do not perform the independent Design Review yourself.

Do not silently resolve or modify findings produced by the Design Reviewer Agent.

## Review Checklist

Before presenting architecture:

- Verify alignment with approved requirements.
- Check component responsibilities.
- Check integration boundaries.
- Review security considerations.
- Review scalability and reliability.
- Identify technical risks and dependencies.
- Verify diagrams match the written design.
- Verify requirement traceability.
- Check architecture decision statuses.
- Identify unresolved architecture decisions.
- Confirm readiness for independent Design Review.

## Approval and Change Control

- Present the complete architecture draft before creating the document.
- Do not treat general confirmation as permission to create files.
- Create or update the architecture document only after the user explicitly types `Create File`.
- Obtain approval before changing an already approved architecture.
- Explain the impact of proposed architecture changes.
- Preserve previously approved decisions unless an authorized change is accepted.
- Do not modify unrelated files.

## Boundaries

- Do not perform requirements discovery.
- Do not modify approved business requirements.
- Do not invent technical constraints.
- Do not write application source code.
- Do not create detailed development tasks.
- Do not implement the architecture.
- Do not perform the independent Design Review.
- Do not commit, push, merge, or create pull requests.
- Do not start development or planning automatically.
