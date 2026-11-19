# DOC-001 — Document Version Tracker

**Status:** Approved by the user; clarifications confirmed 2026-11-19  
**Source:** User-provided story  
**Target:** `docs/requirements.md`

## User Story

> As a user, I want the system to maintain document version history whenever I
> update a document, so that I can identify previous versions and know when a
> document was modified.

## Business Objectives and Scope

Users need to create documents, track content updates and their timestamps, and
view version history.

### In Scope

- Document creation with a title and content.
- Initial version 1.
- Version increments on content updates.
- Recording update timestamps in IST.
- Newest-first version history.
- Rejecting empty content with a validation message.
- Rejecting empty or whitespace-only titles.

### Out of Scope

- Authentication.
- Sharing.
- Attachments.
- Document comparison.
- Restoration.

## Stakeholders and Actors

- **User:** Creates documents, updates content, and views history.

## Functional Requirements

| ID | Requirement | Actor / precondition | Acceptance |
|---|---|---|---|
| FR-001 | The system must allow a user to create a document with a title and content. | User; none identified | AC-001, AC-006 |
| FR-002 | The system must assign version `1` when a document is created. | User; document is saved | AC-001 |
| FR-003 | When a user updates a document's content, the system must increment its version number by one. | User; document exists | AC-002, AC-007 |
| FR-004 | The system must record the date and time of every accepted content update in IST. | User; update is saved | AC-003 |
| FR-005 | The system must allow users to view a document's version history in newest-first order. | User; history exists | AC-004 |
| FR-006 | The system must reject document creation or updates when content is empty and display a validation message. | User; content is submitted | AC-005 |

**Priority:** Not provided for all requirements.

## Non-Functional Requirements

No additional non-functional requirements or measurable performance,
reliability, security, or availability targets were provided. These are
**Not Found**.

## Business Rules

- A new document starts at version 1.
- An accepted content update increments the version by one.
- An update containing the current content is a no-op and does not create a version or timestamp.
- Update timestamps use IST.
- Version history is shown newest-first.
- Empty content is rejected with a validation message.
- Version 1 has a creation timestamp in IST, shown in its history entry.
- Prior content snapshots are retained, but history entries display only the version number and timestamp.
- Titles are immutable after creation; title-only updates are not supported.
- Empty or whitespace-only titles are rejected.
- Whitespace-only content is rejected as empty. Other content is stored without trimming.

## Acceptance Criteria

### AC-001 — Create a document

**Maps to:** FR-001, FR-002

- Given a user creates a document with a title and content,
- When the document is saved,
- Then the system creates it with version `1` and records its creation time in IST.

### AC-002 — Update a document

**Maps to:** FR-003

- Given a document already exists,
- When a user updates its content,
- Then the system increments its version number by one.
- If the submitted content is identical to the current content, the system treats the request as a no-op and does not increment the version.

### AC-003 — Record modification time

**Maps to:** FR-004

- Given a user updates a document,
- When the update is saved,
- Then the system records the modification date and time in IST.

### AC-004 — View version history

**Maps to:** FR-005

- Given a document has been updated multiple times,
- When a user views its version history,
- Then the system displays the available versions in newest-first order.

### AC-005 — Validate empty content

**Maps to:** FR-006

- Given a user is creating or updating a document,
- When the content is empty or contains only whitespace,
- Then the system rejects the operation with the message `Content must not be empty.`

### AC-006 — Validate title

**Maps to:** FR-001

- Given a user is creating a document,
- When the title is empty or contains only whitespace,
- Then the system rejects the operation with the message `Title must not be empty.`

### AC-007 — Ignore unchanged content

**Maps to:** FR-003

- Given a document already exists,
- When a user submits content identical to its current content,
- Then the system leaves the version and modification timestamp unchanged.

## End-to-End Business Workflow

1. The user submits a title and content to create a document.
2. The system rejects an empty or whitespace-only title or content with the corresponding validation message; otherwise, it saves version 1 and records its creation time in IST.
3. The user submits a content update.
4. The system rejects empty or whitespace-only content with a validation message; treats identical content as a no-op; otherwise, it increments the version and records the update timestamp in IST.
5. The user views history, which is ordered newest-first and shows each version number and timestamp.

## Assumptions and Constraints

- No assumptions are confirmed.
- No programming language is mandated. API delivery and JSON persistence were
  selected as technical directions in the Architecture phase.
- Validation messages are `Content must not be empty.` and
  `Title must not be empty.`
- Timestamps are displayed as ISO 8601 values with the IST offset `+05:30`.
- The user approved the clarifications recorded below on 2026-11-19.

## Clarification Log

| ID | Question | Status |
|---|---|---|
| CL-001 | Should history retain and display prior version content, or show only version details such as number and timestamp? | Resolved: retain prior content snapshots; history displays only version number and timestamp. |
| CL-002 | Should version 1's creation time be recorded and shown in history? | Resolved: record and show version 1's creation time in IST. |
| CL-003 | Should a title-only change increment the version and record a timestamp? | Resolved: titles are immutable; title-only updates are unsupported. |
| CL-004 | Should an empty or whitespace-only title be rejected? | Resolved: reject both with `Title must not be empty.` |
| CL-005 | Does whitespace-only content count as empty? | Resolved: reject it as empty; preserve submitted whitespace in all other content. |
| CL-006 | What exact validation-message wording and timestamp display format are required? | Resolved: use the exact messages above and ISO 8601 timestamps with `+05:30`. |

## Open Items

- No business clarifications remain open.
- Performance, availability, capacity, and reliability targets were not provided.

## Negative and Edge Scenarios

- Empty content must be rejected with a validation message (AC-005).
- Whitespace-only content and titles are rejected (AC-005, AC-006).
- Title changes after creation are unsupported (CL-003).
- Version 1 has a creation timestamp; prior content is retained but not exposed through history (CL-001, CL-002).

## Dependencies and Risks

- No external dependencies were provided.
- Retained snapshots and whole-file JSON persistence can increase storage size;
  no capacity or retention target was supplied.

## Requirement Traceability

| Story | Requirement | Acceptance criterion | Test scenario |
|---|---|---|---|
| DOC-001 | FR-001, FR-002 | AC-001 | TC-001: Create a document and verify version 1 and creation timestamp |
| DOC-001 | FR-001 | AC-006 | TC-006: Submit an empty or whitespace-only title and verify rejection |
| DOC-001 | FR-003 | AC-002 | TC-002: Update changed content and verify the version increments |
| DOC-001 | FR-003 | AC-007 | TC-007: Submit unchanged content and verify version and timestamp remain unchanged |
| DOC-001 | FR-004 | AC-003 | TC-003: Update content and verify the timestamp uses IST |
| DOC-001 | FR-005 | AC-004 | TC-004: View history and verify newest-first ordering |
| DOC-001 | FR-006 | AC-005 | TC-005: Submit empty content and verify rejection and message |

These are proposed test scenarios only; no tests have been implemented or run.
