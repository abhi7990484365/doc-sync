# DOC-001 Implementation Plan

## 1. Document Information

- **Story:** DOC-001 — Document Version Tracker
- **Requirements:** FR-001–FR-006; AC-001–AC-007
- **Architecture review:** R3 — Approved with Conditions; bounded R4 re-review — Approved with Conditions for the TASK-005 store-path scope
- **Plan status:** Approved by the user on 2026-11-19
- **Approval:** Requirements, architecture, and this plan are approved. R3 conditions and CL-001–CL-006 have recorded stakeholder dispositions. The bounded R4 re-review records DR-021 for TASK-005; R3 remains unchanged, and implementation verification remains pending.

## 2. Planning Overview

The work is organized into four workstreams:

1. Decision and condition gates.
2. Runtime and persistence foundation.
3. Document operations.
4. Contract verification and handoff.

The user requested that remaining R3 conditions be tracked during planning. The user-approved dispositions are now recorded in the source documents. The bounded R4 re-review of the amended TASK-005 store-path policy is also tracked as DR-021, with R3 unchanged and implementation verification pending.

## 3. Source Documents

- `docs/requirements.md` — Approved; FR-001–FR-006, AC-001–AC-007, and resolved CL-001–CL-006.
- `docs/architecture.md` — Approved with Conditions following R3; user-approved API, runtime, persistence, lifecycle, locking, validation, and error decisions recorded.
- `docs/design-review.md` — R3 Approved with Conditions; subsequent stakeholder dispositions recorded without changing the independent review outcome. R4 independent bounded re-review outcome: Approved with Conditions for the TASK-005 store-path scope only; DR-021 implementation verification is pending.
- `.github/instructions/planner.instructions.md`
- `.github/skills/implementation-planning/SKILL.md`
- `README.md`
- `requirements.txt`
- Existing repository structure and source/test locations.

The existing project is a repository-scanning CLI. At planning time, `requirements.txt` contained FastAPI and httpx but not Uvicorn, and no API entry-point module was present. TASK-005 has since added the pinned dependency and entry point; execution and verification remain pending.

## 4. Planning Assumptions and Constraints

- Preserve DOC-001 scope: document creation, content updates, IST timestamps, newest-first history, and empty-content rejection; titles are immutable.
- Do not add authentication, sharing, attachments, comparison, or restoration.
- API and JSON, FastAPI/Uvicorn, REST contract, explicit initialization, versioned marker, local-filesystem locking, no-op semantics, and failure mappings are approved.
- Prior content snapshots are retained but history exposes only version number and timestamp; no automatic pruning is provided.
- `DOC_SYNC_STORE_PATH` must identify an absolute local path; file access relies on OS permissions. Mounted network filesystems that cannot be reliably identified are unsupported by the approved local-only scope but may not be automatically detectable; implementation must not claim stronger detection.
- Backup/recovery is deferred; no automatic backup, restore, or pruning is provided. No performance, availability, capacity, or recovery-time targets were supplied.
- The existing scanner remains separate and unchanged.

## 5. Architecture Summary

The approved architecture uses a local API and JSON persistence. API, document-service, timestamp, repository, and process-ownership responsibilities are separate from the existing scanner.

The approved contract uses REST endpoints and response mappings; FastAPI/Uvicorn; loopback binding; explicit store initialization and a versioned marker; JSON replacement writes; local-filesystem process locking; stale-version handling; and unchanged-content no-op behavior. Implementation must preserve documented durability and backup/recovery limitations.

## 6. Implementation Workstreams

| Workstream | Tasks | Purpose |
|---|---|---|
| Decision and condition gates | TASK-001–TASK-004 | Resolve or explicitly defer business questions and track review conditions. |
| Runtime and persistence | TASK-005–TASK-007 | Establish the confirmed runtime, store lifecycle, and single-process protections. |
| Document operations | TASK-008–TASK-010 | Implement create, content update, and history behaviors. |
| Contract, verification, and documentation | TASK-011–TASK-013 | Implement error handling, verify behavior and scanner independence, and document operation. |

## 7. Prioritized Task List

### TASK-001 — Resolve or formally defer CL-001–CL-006

- **Description:** Obtain and record stakeholder dispositions for history content (CL-001), version 1 timestamp (CL-002), title-only changes (CL-003), empty-title validation (CL-004), whitespace-only content (CL-005), and exact validation-message and timestamp-display formats (CL-006). Record the approved unchanged-content no-op semantics (DR-020).
- **Requirement IDs:** FR-001–FR-006; AC-001–AC-007, as affected by each clarification.
- **Architecture component:** API validation, document service, timestamp provider, JSON document/history model.
- **Dependencies:** None.
- **Priority:** P1 — These decisions gate correct behavior for the requirements and acceptance scenarios they affect.
- **Completion criteria:** Each clarification has an explicit answer or a documented deferral/exclusion approved by the appropriate stakeholder; affected behavior is identified without changing requirements by assumption.
- **Verification approach:** Review the recorded dispositions against affected FRs/ACs and confirm downstream tasks use only the recorded outcomes.
- **Status:** **Completed** — CL-001–CL-006 and the DR-020 no-op decision were confirmed and recorded in the approved artifacts.

### TASK-002 — Confirm proposed API and runtime contract details

- **Description:** Before implementing API-specific behavior, obtain explicit confirmation or disposition for proposed route shapes, request/response schemas, status/error mappings, expected-version behavior, unchanged-content semantics, runtime choice, startup configuration, and loopback exposure. Preserve the approved API direction.
- **Requirement IDs:** FR-001–FR-006; AC-001–AC-007.
- **Architecture component:** HTTP/API layer and application runtime.
- **Dependencies:** None.
- **Priority:** P1 — API behavior and runtime are prerequisites for delivering the approved API direction.
- **Completion criteria:** Implementation-relevant details have explicit approval or documented deferral; no unapproved behavior is included as a contract.
- **Verification approach:** Compare each confirmed detail with the architecture proposal and requirements; identify any required architecture or requirements review before implementation.
- **Status:** **Completed** — API routes, runtime, request semantics, loopback scope, and error contract were confirmed and recorded.

### TASK-003 — Disposition storage and ownership conditions

- **Description:** Resolve or explicitly defer DR-017 (marker format and invalid-marker behavior), DR-018 (lock identity, canonicalization, and filesystem scope), and DR-019 (storage write/replacement failure mappings). Coordinate history snapshot/content disposition with CL-001 and DR-009. Do not silently choose filesystem, marker, or error semantics.
- **Requirement IDs:** FR-001–FR-005; AC-001–AC-004.
- **Architecture component:** JSON repository, store initialization, process ownership, version-history model.
- **Dependencies:** TASK-001 for the CL-001/history decision.
- **Priority:** P1 — These conditions affect persistence safety, concurrency assumptions, and observable failure behavior.
- **Completion criteria:** Each condition has an explicit disposition sufficient to guide implementation, or dependent behavior is explicitly deferred. Unsupported storage or recovery guarantees are not claimed.
- **Verification approach:** Review dispositions against R3 findings and proposed architecture; confirm dependent implementation tasks are gated accordingly.
- **Status:** **Completed** — DR-017–DR-019 and history/storage dispositions were recorded; backup/recovery is explicitly deferred.

### TASK-004 — Track approval-label and diagram follow-ups

- **Description:** Resolve DR-015 by aligning document labels with recorded approvals, and resolve DR-016 by adding the identified failure paths to the architecture diagram, under the user's explicit authorization.
- **Requirement IDs:** None; review/documentation follow-up only, with no added product scope.
- **Architecture component:** Architecture and review documentation.
- **Dependencies:** None.
- **Priority:** P3 — Low-severity documentation concerns do not block core implementation.
- **Completion criteria:** Requirements and plan labels reflect approval, architecture retains the R3 Approved with Conditions status, and the architecture diagram shows the identified failure paths.
- **Verification approach:** Check approval labels and verify that the updated architecture diagram depicts the identified failure paths.
- **Status:** **Completed** — Approval labels were corrected and the architecture diagram includes the identified failure paths.

### TASK-005 — Establish the approved API runtime and application startup

- **Description:** Add a compatible pinned Uvicorn dependency and create the API application entry point and startup lifecycle using the approved runtime and configuration. At startup, fail closed before serving when `DOC_SYNC_STORE_PATH` is unset, relative, missing, not a regular file, or a detectable UNC/remote path. Keep the existing scanner entry point independent. Mounted network filesystems that cannot be reliably identified are unsupported but may not be automatically detected; do not claim stronger detection.
- **Requirement IDs:** FR-001–FR-006.
- **Architecture component:** HTTP/API layer and application runtime.
- **Dependencies:** TASK-002.
- **Priority:** P1 — A runnable application is required to provide the API.
- **Completion criteria:** The approved application entry point starts using `DOC_SYNC_STORE_PATH`; dependencies are pinned; startup fails closed for unset, relative, missing, non-file, and detectable UNC/remote store paths; no store initialization or service acceptance occurs for rejected paths; unknown mounted network filesystems are documented as unsupported and not claimed as detectable; scanner invocation remains unchanged.
- **Verification approach:** Run focused startup/configuration tests for unset, relative, missing, directory/non-file, and detectable UNC/remote paths, confirming fail-closed behavior. Run the scanner regression suite to confirm the existing scanner remains independent and unchanged. Record any platform limitations and do not claim detection of mounted network filesystems that cannot be reliably identified.
- **Status:** **Completed** — The focused command `python -m pytest tests/test_doc_sync_api.py` reported 15 passed and one Starlette/AnyIO deprecation warning in 1.09s; the full command `python -m pytest` reported 15 passed and one warning in 0.93s. Both runs covered startup/configuration checks and scanner regression. Real Windows remote-drive behavior was not exercised against an actual remote drive. TASK-002 is complete.

### TASK-006 — Implement JSON store lifecycle and initialization

- **Description:** Implement the confirmed JSON store representation, `DOC_SYNC_STORE_PATH` configuration, and explicit initialization/fail-closed lifecycle. Handle absent, mismatched, corrupt, and unsupported store state only as approved; do not silently initialize or overwrite data.
- **Requirement IDs:** FR-001–FR-005.
- **Architecture component:** JSON repository and initialization marker.
- **Dependencies:** TASK-002, TASK-003, TASK-005.
- **Priority:** P1 — Persistence is required for document creation, updates, and history.
- **Completion criteria:** Confirmed store schema and initialization rules are implemented; invalid or unavailable state fails as specified; existing data is not silently discarded or reset.
- **Verification approach:** Unit and integration tests for initialization, valid and invalid state, store/marker mismatch, and persistence across restart.
- **Status:** **Blocked** — Depends on completion of TASK-005.

### TASK-007 — Enforce single-process mutation ownership

- **Description:** Implement the confirmed canonical-path process lock on local filesystems and in-process mutation serialization. Fail before serving if ownership cannot be acquired. Do not claim protection against external or non-cooperating writers.
- **Requirement IDs:** FR-002–FR-003.
- **Architecture component:** Process ownership and document service/repository mutation path.
- **Dependencies:** TASK-003, TASK-006.
- **Priority:** P1 — Concurrent writes could violate version consistency under the approved single-process design.
- **Completion criteria:** The approved ownership mechanism is held for the service lifetime; a second cooperating process cannot serve against the same supported store; mutations are serialized as specified.
- **Verification approach:** Platform-appropriate tests for lock acquisition, contention, release, and concurrent mutation behavior on the supported local filesystem.
- **Status:** **Blocked** — Depends on TASK-006.

### TASK-008 — Implement document creation and content validation

- **Description:** Implement confirmed creation behavior: accept title and content, persist a new document at version 1 with its creation timestamp, and reject empty or whitespace-only titles/content with the approved messages.
- **Requirement IDs:** FR-001, FR-002, FR-006; AC-001, AC-005, AC-006.
- **Architecture component:** API validation, document service, JSON repository.
- **Dependencies:** TASK-001, TASK-002, TASK-006, TASK-007.
- **Priority:** P1 — Creation and empty-content rejection are required functionality.
- **Completion criteria:** A valid create follows the confirmed API contract and persists version 1; empty content is rejected without modifying the store; title and whitespace behavior matches recorded decisions.
- **Verification approach:** API and service tests for valid creation, version 1, empty content, and decided title/whitespace cases.
- **Status:** **Blocked** — Depends on the runtime, store lifecycle, and ownership tasks above.

### TASK-009 — Implement content updates, versioning, and IST timestamps

- **Description:** Implement accepted content updates, version increments, and timezone-aware IST timestamps. Apply the approved stale-version and unchanged-content behavior. Do not add title-update behavior without an approved scope change.
- **Requirement IDs:** FR-003, FR-004, FR-006; AC-002, AC-003, AC-005, AC-007.
- **Architecture component:** API layer, document service, timestamp provider, JSON repository.
- **Dependencies:** TASK-001, TASK-002, TASK-006, TASK-007.
- **Priority:** P1 — Versioning and timestamps are central DOC-001 requirements.
- **Completion criteria:** Each accepted content change increments the version once and records the confirmed IST timestamp; invalid content does not mutate state; version 1 timestamp, no-op, stale-update, and title-only cases follow explicit decisions.
- **Verification approach:** Service/API tests for changed content, version increments, timestamp timezone/serialization, invalid content, and all decided edge cases.
- **Status:** **Blocked** — Depends on the store lifecycle and ownership tasks above.

### TASK-010 — Implement newest-first version history

- **Description:** Implement the confirmed history response and ordering. Retain prior content snapshots but expose only version numbers and timestamps.
- **Requirement IDs:** FR-005; AC-004.
- **Architecture component:** History API, document service, JSON history model.
- **Dependencies:** TASK-001, TASK-003, TASK-006, TASK-009.
- **Priority:** P1 — Viewing newest-first history is an explicit requirement.
- **Completion criteria:** Available versions are returned newest-first, and included history fields match recorded CL-001/CL-002 decisions.
- **Verification approach:** API tests with multiple versions; verify order, returned fields, and initial-version timestamp behavior against recorded decisions.
- **Status:** **Blocked** — Depends on the history and persistence implementation tasks above.

### TASK-011 — Implement API error serialization and storage-failure behavior

- **Description:** Implement the confirmed API error envelope, validation and conflict behavior, and deterministic mappings for storage read/write/replacement failures. Avoid returning content, filesystem paths, stack traces, or secrets.
- **Requirement IDs:** FR-001–FR-006; AC-001–AC-007.
- **Architecture component:** HTTP/API layer and JSON repository error boundary.
- **Dependencies:** TASK-002, TASK-003, TASK-008, TASK-009, TASK-010.
- **Priority:** P1 — Clear validation and failure behavior is required for a safe, testable API.
- **Completion criteria:** Malformed JSON maps to 400; invalid requests to 422; missing documents to 404; stale versions to 409; storage failures to 503; and unexpected failures to 500. Errors do not expose sensitive details.
- **Verification approach:** API tests for malformed and invalid requests, missing documents, approved conflicts, unavailable/corrupt stores, and write/replacement failures.
- **Status:** **Blocked** — Depends on document operations and persistence implementation.

### TASK-012 — Verify integrated behavior and scanner independence

- **Description:** Add and run unit, API, and integration tests for confirmed DOC-001 behavior and failure cases. Include regression coverage demonstrating that the existing repository scanner remains independent and unchanged.
- **Requirement IDs:** FR-001–FR-006; AC-001–AC-007.
- **Architecture component:** API, service, timestamp provider, JSON repository, process ownership, and scanner boundary.
- **Dependencies:** TASK-005–TASK-011.
- **Priority:** P1 — Verification demonstrates requirement coverage and protects the existing capability.
- **Completion criteria:** Tests cover acceptance criteria and decided edge cases; scanner tests continue to pass; no DOC-001 task is reported complete without verification.
- **Verification approach:** Run the project test suite and DOC-001 API/integration tests; record results and limitations.
- **Status:** **Blocked** — Depends on implementation tasks and their decision gates.

### TASK-013 — Document approved operation and limitations

- **Description:** Update appropriate project documentation with approved API startup/usage, store initialization and configuration, supported storage/locking scope, and known limitations. Keep scanner usage intact. Document only approved behavior.
- **Requirement IDs:** FR-001–FR-006; AC-001–AC-007.
- **Architecture component:** API/runtime and persistence operational documentation.
- **Dependencies:** TASK-005–TASK-012.
- **Priority:** P2 — Documentation follows implementation and verification.
- **Completion criteria:** Documentation matches verified behavior, explains approved limitations and startup, and preserves existing scanner instructions.
- **Verification approach:** Review documented commands and behavior against the implemented API; verify existing scanner documentation remains accurate.
- **Status:** **Blocked** — Depends on verified implementation and approved operational details.

## 8. Task Dependencies

```text
TASK-001 ─┬─> TASK-008 ─┐
          ├─> TASK-009 ─┼─> TASK-010 ─┐
          └─> TASK-010  │             │
TASK-002 ─> TASK-005 ─> TASK-006 ─> TASK-007
    │             │          │          │
    └─────────────┴──────────┴──────────┴─> TASK-008 / TASK-009
TASK-003 ───────────────> TASK-006 / TASK-007 / TASK-010
TASK-002 + TASK-003 + TASK-008–TASK-010 ─> TASK-011
TASK-005–TASK-011 ─> TASK-012 ─> TASK-013
```

TASK-004 is independent and does not block product implementation. All dependency references point to defined task IDs; no circular dependencies are planned.

## 9. Requirement Traceability Matrix

| Requirement / acceptance | Architecture component | Tasks | Verification |
|---|---|---|---|
| FR-001 / AC-001, AC-006 — Create with title and content; validate title | API validation, document service, JSON repository | TASK-001, TASK-002, TASK-006, TASK-008, TASK-011, TASK-012 | Create API, persistence, and invalid-title tests |
| FR-002 / AC-001 — Initial version 1 | Document service, JSON model | TASK-001, TASK-006, TASK-008, TASK-012 | Creation response and persisted-state tests |
| FR-003 / AC-002, AC-007 — Increment changed content; no-op unchanged content | API, document service, repository, mutation ownership | TASK-001, TASK-002, TASK-006, TASK-007, TASK-009, TASK-012 | Update/version, no-op, and concurrency tests |
| FR-004 / AC-003 — Record accepted update time in IST | Timestamp provider, version entry | TASK-001, TASK-009, TASK-012 | Timezone-aware timestamp tests |
| FR-005 / AC-004 — Newest-first history | History API, service, JSON model | TASK-001, TASK-003, TASK-006, TASK-009, TASK-010, TASK-012 | Multi-version ordering and field tests |
| FR-006 / AC-005 — Reject empty content with message | Request validation and API error handling | TASK-001, TASK-002, TASK-008, TASK-009, TASK-011, TASK-012 | Create/update rejection and response tests |

| Dispositioned item | Confirmed behavior | Tracking tasks |
|---|---|---|
| CL-001 | Retain snapshots; expose only version number and timestamp | TASK-001, TASK-003, TASK-010 |
| CL-002 | Record and show version 1 creation time in IST | TASK-001, TASK-009, TASK-010 |
| CL-003 | Titles are immutable; no title-only update operation | TASK-001, TASK-009 |
| CL-004 | Reject empty or whitespace-only titles | TASK-001, TASK-008 |
| CL-005 | Reject whitespace-only content; preserve other submitted content | TASK-001, TASK-008, TASK-009 |
| CL-006 | Exact validation messages; ISO 8601 timestamps with `+05:30` | TASK-001, TASK-008, TASK-009, TASK-011 |
| DR-017–DR-019 | Versioned fail-closed marker; local canonical-path lock; storage errors 503 and unexpected errors 500 | TASK-003, TASK-006, TASK-007, TASK-011 |
| DR-009, DR-014, DR-020 | Snapshot visibility, timestamp/validation rules, and no-op semantics confirmed | TASK-001–TASK-003, TASK-008–TASK-010 |
| DR-015, DR-016 | Approval labels corrected; failure paths added to architecture diagram | TASK-004 |
| DR-021 | TASK-005 must implement and verify fail-closed startup store-path checks; unknown mounted network filesystems remain unsupported and may be undetectable | TASK-005, TASK-012 |

No in-scope requirement is excluded. Backup and recovery are deferred, with no automatic backup, restore, or pruning.

## 10. Completion Criteria

Implementation planning will be ready for implementation handoff when:

- Decision and condition gates are recorded; implementation tasks remain blocked by their actual dependencies.
- Approved API and JSON directions and confirmed technical details are followed.
- FR-001–FR-006 and AC-001–AC-007 are implemented and verified according to confirmed behavior.
- Error and persistence failures have deterministic, approved handling.
- The existing scanner remains separate and its regression tests pass.
- Documentation reflects verified behavior and does not present unresolved decisions as settled.

## 11. Verification Strategy

- **Unit tests:** Validation, version transitions, timestamp handling, serialization, and repository behavior.
- **API tests:** Confirmed routes, request/response shapes, acceptance scenarios, and error mappings.
- **TASK-005 startup tests:** Focused coverage for unset, relative, missing, non-file, and detectable UNC/remote `DOC_SYNC_STORE_PATH` values, plus confirmation that startup is fail-closed and no store or service state is accepted. Scanner regression is required separately.
- **Persistence/integration tests:** Initialization and failure states, restart persistence, and history ordering.
- **Concurrency/platform tests:** Only for the approved lock and filesystem scope; do not claim guarantees beyond tested conditions.
- **Regression tests:** Existing scanner tests and invocation remain unaffected.
- **Documentation review:** Commands and operational descriptions match verified behavior.
- No performance or durability target is asserted because none was supplied.

## 12. Risks and Blockers

| Item | Impact | Tracking |
|---|---|---|
| Runtime implementation not yet verified | Uvicorn dependency and API entry point have been added; startup and regression evidence is pending | TASK-005, TASK-012 |
| JSON whole-file writes and local storage | Durability, size, and external-writer limitations remain | TASK-006, TASK-007 |
| Backup/recovery deferred | Data loss may be unrecoverable; no automatic backup, restore, or pruning | TASK-006, TASK-013 |
| Platform path and replacement behavior | Canonicalization and crash guarantees require platform testing | TASK-006, TASK-007, TASK-012 |
| DR-021 — TASK-005 store-path verification gap | The bounded R4 plan gate is addressed through explicit TASK-005 completion and verification requirements, but implementation and executed tests remain pending; unknown mounted network filesystems may not be detectable | TASK-005, TASK-012 |

There are no unresolved Critical or High design findings per R3. R3 remains Approved with Conditions. DR-021 is the bounded R4 medium-severity condition for TASK-005 scope and is addressed as a plan gate, but implementation verification remains pending. Stakeholder dispositions for the medium/low conditions are recorded.

## 13. Deferred Items and Implementation Details

1. Backup and recovery remain deferred; no automatic backup, restore, or pruning is provided.
2. The exact command interface for explicit store initialization is an implementation detail.
3. Runtime and platform-specific startup verification remain implementation work.
4. No performance, availability, capacity, or recovery-time targets were provided.

## 14. Implementation Sequence

1. Decision and condition gates TASK-001–TASK-004 are complete.
2. Complete implementation and verification for the user-selected TASK-005 runtime/startup task.
3. Implement approved JSON lifecycle (TASK-006), then process ownership (TASK-007).
4. Implement creation/validation and content updates (TASK-008, TASK-009).
5. Implement history (TASK-010) and API error behavior (TASK-011).
6. Run integrated and scanner regression tests (TASK-012).
7. Document only verified, approved behavior (TASK-013).

A task must not advance through an unresolved gate that affects its behavior.

## 15. Handoff Notes

This plan contains **13 tasks**: P1 decision gates and core work, P2 documentation, and P3 review follow-up. TASK-001–TASK-005 are complete. The focused and full pytest runs each reported 15 passed and one non-failing Starlette/AnyIO deprecation warning; the test module covers startup/configuration checks and scanner regression. TASK-006–TASK-013 remain blocked by implementation dependencies. Document creation, update, and history tasks have not started.

TASK-005 is complete. No later implementation task has started.
