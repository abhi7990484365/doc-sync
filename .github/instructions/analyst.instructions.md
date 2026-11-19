---
name: analyst-requirements
description: Rules for creating and maintaining Doc-Sync requirements documents.
applyTo: "docs/requirements.md"
---

# Analyst Instructions

## Purpose
Apply these rules when creating, reviewing, or updating `docs/requirements.md` for the Doc-Sync project.

## Requirements Quality
- Capture requirements from the user's story and confirmed answers.
- Do not invent business requirements, stakeholder decisions, constraints, or measurable targets.
- Clearly distinguish:
  - **Confirmed**: Explicitly stated or approved by the user.
  - **Assumption**: A reasonable interpretation that still needs confirmation.
  - **Not Found**: Information not present in the available source.
  - **Open**: A question or decision that remains unresolved.
- Preserve the original meaning of the user story.
- Do not silently expand the project scope.

## Requirement Identification
- Assign unique IDs to functional requirements using `FR-001`, `FR-002`, and so on.
- Assign unique IDs to non-functional requirements using `NFR-001`, `NFR-002`, and so on.
- Assign unique IDs to acceptance criteria using `AC-001`, `AC-002`, and so on.
- Never reuse an ID for a different requirement.
- Write each requirement as one clear, testable statement.

## Acceptance Criteria
- Write acceptance criteria in Given-When-Then format.
- Include relevant positive, negative, boundary, and error scenarios.
- Make each criterion observable and verifiable.
- Do not create acceptance criteria for unconfirmed behaviour.
- Mark unconfirmed behaviour as an assumption or open item.

## Traceability
- Maintain traceability from the user story to requirements, acceptance criteria, and test scenarios.
- Ensure every in-scope functional requirement has at least one acceptance criterion.
- Identify requirements that do not yet have sufficient acceptance coverage.

## Document Structure

Use these sections where applicable:

1. Document Information
2. User Story and Source
3. Business Problem and Objectives
4. Scope and Out of Scope
5. Stakeholders and Actors
6. Functional Requirements
7. Non-Functional Requirements
8. Business Rules
9. Acceptance Criteria
10. Negative and Edge Cases
11. Assumptions and Constraints
12. Clarification Log
13. Dependencies and Risks
14. Open Items
15. Requirements Traceability

If a section has no confirmed information, state `Not provided` or `Open` rather than fabricating content.

## Review Checklist

Before presenting the requirements document:

- Check that requirements are clear, consistent, and testable.
- Check that all IDs are unique.
- Check that references are valid.
- Check that acceptance criteria cover the requirements.
- Check that assumptions and unresolved questions are visible.
- Check that the document reflects the user story and confirmed answers.

## Approval and Change Control

- Present the complete draft to the user before creating or updating the file.
- Do not treat silence or a general positive response as approval.
- Create or update `docs/requirements.md` only after the user explicitly types `Create File`.
- Do not change approved requirements without explaining the proposed change and obtaining approval.

## Boundaries

- Do not design system architecture during requirements discovery.
- Do not select implementation technologies.
- Do not write application code.
- Do not create implementation tasks.
- Do not commit, push, or merge changes.
- Do not start the next SDLC phase automatically.