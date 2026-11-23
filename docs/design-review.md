# Independent Re-Review — DOC-001 Revised Architecture

## 1. Review Information

- **Review ID:** DOC-001-DR-R3
- **Prior review:** DOC-001-DR-R2
- **Outcome:** Approved with Conditions
- **Requirements status:** Approved by the user; CL-001–CL-006 were resolved by user-approved dispositions on 2026-11-19.
- **Architecture status:** Approved with Conditions after R3; user-approved dispositions for the conditions were recorded on 2026-11-19.
- **Scope:** Independent re-review; no files or architecture changes performed.

The outcome above records the independent R3 review and is not changed by the later stakeholder dispositions in section 19. Those dispositions are not a new independent review; implementation verification remains pending.

## 2. Review Scope and Sources

Reviewed requirements FR-001–FR-006 and AC-001–AC-005, the revised architecture, the prior design review, and relevant project context.

Source documents:

- `docs/requirements.md`
- `docs/architecture.md`
- `docs/design-review.md` (prior review)
- `.github/instructions/design-reviewer.instructions.md`
- `.github/skills/design-review/SKILL.md`
- Relevant project documentation and repository files

The existing project is a repository-scanning CLI. `requirements.txt` declares FastAPI but not Uvicorn, and no `src/doc_sync_api.py` or equivalent API module exists.

## 3. Architecture Summary

The revised architecture proposes:

- A local FastAPI REST API at `/api/v1`.
- JSON persistence with a schema version and document snapshots.
- Required `expected_version` optimistic updates.
- No-op behavior for unchanged content.
- Timezone-aware IST timestamps.
- Explicit store initialization with a marker.
- Fail-closed startup and operation for missing, unmarked, or corrupt stores.
- A lifetime exclusive OS lock and an in-process mutation mutex.
- One-worker Uvicorn execution bound to `127.0.0.1`.
- Same-directory temporary-file writes and store replacement.

The existing repository-scanning capability remains separate.

## 4. Requirement Coverage Matrix After Stakeholder Dispositions

This matrix reflects the decisions recorded after R3 and is not a new independent assessment.

| Requirement | Coverage | Evidence | Assessment |
|---|---|---|---|
| FR-001 / AC-001, AC-006 | Fully Addressed | `POST /api/v1/documents`, JSON repository | Creation and title validation are specified. |
| FR-002 / AC-001 | Fully Addressed | Document service and `current_version: 1` | Initial version 1 is explicit. |
| FR-003 / AC-002, AC-007 | Fully Addressed | `PUT /api/v1/documents/{id}/content` | Changed content increments once; stale versions conflict; identical content is a no-op. Titles are immutable. |
| FR-004 / AC-003 | Fully Addressed | IST timestamp provider | Content updates receive timestamps; version 1 records creation time; display uses ISO 8601 with `+05:30`. |
| FR-005 / AC-004 | Fully Addressed | History endpoint with descending version order | History shows version number and timestamp; prior content snapshots are retained but not exposed. |
| FR-006 / AC-005 | Fully Addressed | Validation and `422 VALIDATION_ERROR` | Empty and whitespace-only content are rejected with the confirmed message. |

## 5. Carry-Forward Finding Disposition

The original finding descriptions and open statuses in sections 5–6 record the state at the R3 review. Later stakeholder dispositions are recorded in section 19 and do not change the independent review outcome.

### DR-001 — Delivery interface

- **Severity:** Previously High
- **Disposition:** Resolved at interface-direction level.
- **Evidence:** Architecture sections 4 and 7; the user explicitly approved API delivery.
- **Residual issues:** Endpoint semantics and status mappings are addressed by DR-008; runtime details are addressed by DR-013.

### DR-002 — Persistence and atomic updates

- **Severity:** Previously High
- **Disposition:** Resolved with acknowledged limitations.
- **Evidence:** Architecture sections 5–6 describe JSON, explicit initialization, whole-file replacement, locking, and fail-closed behavior.
- **Residual issues at R3:** Marker details, lock identity, and storage failure mappings were recorded in DR-017–DR-019; their later dispositions are in section 19.

### Other carry-forward findings

- **DR-003 — IST semantics:** Medium, Open; carried forward as DR-014.
- **DR-004 — History content and title-only changes:** Medium, Open; carried forward as DR-009 and CL-003.
- **DR-005 — Title and whitespace validation:** Medium, Open; carried forward as DR-014.
- **DR-006 — Storage/state failures:** Medium, Open; carried forward as DR-010 and DR-019.
- **DR-007 — Approval status-label inconsistency:** Medium, Open; carried forward as DR-015.

## 6. Architecture Findings

### DR-008 — API contract and precedence

- **Severity:** High
- **Type:** Integration Gap
- **Related requirements:** FR-001, FR-003, FR-005, FR-006
- **Architecture section:** 4
- **Description:** The prior contract ambiguity is substantially resolved.
- **Evidence:** The revision specifies malformed JSON, shape/type/extra-field validation, missing-document precedence, required `expected_version`, stale-version conflicts, unchanged-content no-op semantics, and empty-string handling.
- **Impact:** The remaining validation and wording clarifications were later resolved by stakeholder approval.
- **Recommended action:** Preserve these mappings in implementation and testing.
- **Status:** Resolved; CL-005 and CL-006 were subsequently resolved by stakeholder approval.

### DR-010 — Missing store, initialization, and durability

- **Severity:** High
- **Type:** Reliability Risk
- **Related requirements:** FR-001–FR-005
- **Architecture section:** 5
- **Description:** The revised architecture addresses missing and deleted store state by requiring explicit marked initialization and failing closed.
- **Evidence:** Normal startup never creates an absent store; marker/store mismatches fail startup; corrupt state is not recreated; both-deletion behavior is acknowledged.
- **Impact:** External deletion or storage failure can still lose history, but the design no longer silently resets or accepts an empty store.
- **Recommended action:** Backup and recovery are deferred; no automatic backup or pruning is provided.
- **Status:** Resolved with acknowledged limitation.

### DR-011 — Single-process ownership

- **Severity:** High
- **Type:** Reliability Risk
- **Related requirements:** FR-002, FR-003
- **Architecture section:** 6
- **Description:** The design bounds operation with an OS lock and single-worker deployment.
- **Evidence:** Lifetime exclusive lock, in-process mutex, one Uvicorn worker, canonical-store lock derivation, and unsupported non-cooperating writers are explicit.
- **Impact:** Co-operating processes can be constrained; aliases and non-cooperating writers remain platform limitations.
- **Recommended action:** Enforce one local worker and document unsupported shared/network storage.
- **Status:** Resolved within the proposed single-process scope.

### DR-013 — ASGI runtime

- **Severity:** High
- **Type:** Technical Feasibility
- **Related requirements:** FR-001–FR-006
- **Architecture section:** 6
- **Description:** The architecture identifies a FastAPI/Uvicorn target and startup command.
- **Evidence:** The target command is documented, but Uvicorn is undeclared and `src.doc_sync_api:app` is absent.
- **Impact:** The design is not currently runnable, but the architecture no longer implies the module exists.
- **Recommended action:** Add the runtime dependency and entry point only as part of approved implementation work.
- **Status:** Resolved as an implementation-state limitation.

### DR-017 — Initialization marker lifecycle

- **Severity:** Medium
- **Type:** Data Design Gap
- **Related requirements:** FR-001–FR-005
- **Architecture sections:** 5, ADR-008
- **Description:** The R3 design left marker content and invalid-marker behavior unspecified.
- **Evidence:** The approved architecture requires a versioned marker and fails closed for missing, mismatched, corrupt, or unsupported state.
- **Impact:** An interrupted initialization may leave unusable state that requires explicit operator action; it will not silently be adopted or reset.
- **Recommended action:** Implement the versioned marker and mismatch checks; verify interrupted initialization fails closed.
- **Status:** Resolved by stakeholder decision to use a versioned marker and fail closed for corrupt or unsupported marker state; implementation verification pending.

### DR-018 — Lock identity and canonicalization

- **Severity:** Medium
- **Type:** Reliability Risk
- **Related requirements:** FR-002, FR-003
- **Architecture section:** 6
- **Description:** The approved design restricts storage to local filesystems and derives lock identity from the canonical configured store path; platform-specific path behavior still needs verification.
- **Evidence:** The architecture excludes shared/network storage and requires canonical-path locking, while documenting platform path aliases as a limitation.
- **Impact:** Platform aliases may still cause cooperating processes to identify the same store differently if canonicalization is incomplete.
- **Recommended action:** Use local filesystems only and derive lock identity from the canonical configured store path; test platform path handling.
- **Status:** Accepted by stakeholder disposition; platform-specific implementation verification pending.

### DR-019 — JSON and replacement failure status mappings

- **Severity:** Medium
- **Type:** Integration Gap
- **Related requirements:** FR-001–FR-006
- **Architecture section:** 4
- **Description:** Missing/corrupt stores map to 503, while write and replacement failures are described generally.
- **Evidence:** Temporary-file creation, write, flush, replacement, and directory-sync failures are not individually mapped to API outcomes.
- **Impact:** API behavior and client recovery treatment could vary for storage I/O failures.
- **Recommended action:** Map storage read/write/replacement failures to 503 and unexpected internal failures to 500, preserving the generic error-envelope rule.
- **Status:** Resolved by stakeholder disposition; implementation verification pending.

### DR-020 — Unchanged-content no-op

- **Severity:** Low
- **Type:** Open Question
- **Related requirements:** FR-003 / AC-002
- **Architecture section:** 4
- **Description:** Identical-content submissions are proposed as no-ops rather than version increments.
- **Evidence:** The architecture explicitly marks this as a technical proposal rather than a change to FR-003.
- **Impact:** If “user updates content” means any update request, semantics may require stakeholder clarification.
- **Recommended action:** Record unchanged-content behavior as an accepted edge rule or ask the stakeholder; do not rewrite FR-003 without approval.
- **Status:** Resolved by stakeholder approval: identical-content submissions are no-ops.

### DR-009 — History snapshots and prior-content semantics

- **Severity:** Medium
- **Type:** Data Design Gap
- **Related requirements:** FR-003, FR-005
- **Architecture sections:** 5, ADR-004
- **Description:** Content snapshots are proposed while history visibility remains unresolved under CL-001.
- **Evidence:** The architecture stores snapshots but proposes metadata-only history.
- **Impact:** Storage growth and privacy exposure may differ from stakeholder intent.
- **Recommended action:** Retain prior content snapshots but expose only version numbers and timestamps in history.
- **Status:** Resolved by stakeholder approval; implementation verification pending.

### DR-014 — Timestamp and whitespace clarifications

- **Severity:** Medium
- **Type:** Open Question
- **Related requirements:** FR-004, FR-006
- **Architecture sections:** 4, ADR-003
- **Description:** CL-002, CL-005, and CL-006 remain unresolved.
- **Evidence:** IST serialization is proposed, version 1 timestamp is open, whitespace-only content is unresolved, and exact wording is open.
- **Impact:** Tests may differ on edge inputs and presentation.
- **Recommended action:** Resolve or formally exclude these clarifications.
- **Status:** Resolved by stakeholder approval of the version 1 timestamp, whitespace rules, validation messages, and timestamp format.

### DR-015 — Approval and draft labels

- **Severity:** Medium
- **Type:** Documentation Inconsistency
- **Related requirements:** FR-001–FR-006
- **Architecture sections:** Document headers
- **Description:** Source documents retain Draft labels despite workflow approvals.
- **Evidence:** `docs/requirements.md` says “Draft for review,” and `docs/architecture.md` says the revised architecture is not yet approved despite the user's approval.
- **Impact:** Review gates and audit history may be ambiguous.
- **Recommended action:** Update labels only under separate authorization.
- **Status:** Resolved by updating document status labels to reflect recorded approvals and the R3 outcome.

### DR-016 — Diagram and failure-path completeness

- **Severity:** Low
- **Type:** Maintainability Concern
- **Related requirements:** FR-001–FR-006
- **Architecture sections:** 2, 6
- **Description:** Diagrams cover components and lock ownership but omit error paths and replacement stages.
- **Evidence:** Missing-store, corrupt-store, lock-failure, temporary-file write, replacement, and 503/500 paths are not shown.
- **Impact:** Operational behavior is less visually auditable.
- **Recommended action:** Show lock, store, write, replacement, and API error paths in the architecture component diagram.
- **Status:** Resolved in the updated architecture diagram; implementation behavior remains to be verified.

## 7. Component Architecture Assessment

- **HTTP/API:** The approved contract specifies deterministic success and error behavior.
- **Validation:** Empty and whitespace-only title/content behavior and messages are confirmed.
- **Document service:** Version increment, existence, and conflict responsibilities are clear.
- **Timestamp provider:** IST timestamps, including version 1 creation time, use ISO 8601 with `+05:30`.
- **Repository:** Candidate-state validation and replacement are described.
- **Initialization:** Explicit initialization, versioned marker, and fail-closed handling are specified.
- **Lock ownership:** One cooperating process is supported on local filesystems using the canonical store path.
- **Existing CLI:** Remains separate and independent.

## 8. Integration Architecture Assessment

No external integration is required by DOC-001. The architecture introduces only a local HTTP API and JSON filesystem dependency.

FastAPI/Uvicorn, loopback binding, status/error mappings, and store lifecycle are approved. Client retry/timeout behavior and external-writer protection are not provided; no requirement requires retries or external integrations.

## 9. Data Architecture Assessment

- JSON is approved.
- JSON snapshot storage is inspectable and local.
- The entire store is rewritten per mutation.
- There are no database transactions, cross-process locks, or backup mechanism.
- Missing, corrupt, mismatched, and unsupported store/marker behavior fails closed.
- The store path is configured with `DOC_SYNC_STORE_PATH`; file permissions rely on the operating-system account.
- Backup and recovery are deferred; snapshots are retained without automatic pruning.

The architecture does not provide content encryption at rest, but no encryption requirement was supplied.

## 10. Security Assessment

- Authentication and authorization remain out of scope.
- Loopback binding is the approved deployment scope.
- Loopback does not authenticate local callers.
- Error responses avoid content, paths, stack traces, and secrets.
- Document content is stored in plaintext JSON.
- Store permissions rely on the execution environment.

Remote or multi-user deployment requires a separate security decision.

## 11. Reliability and Performance Assessment

### Reliability

- Write failures fail closed.
- Corrupt state is not silently discarded.
- Mutations serialize within one process.
- Replacement and crash guarantees are explicitly limited.
- Explicit initialization prevents silent recreation.
- External deletion and deletion of both store and marker can leave unrecoverable state without backup.

### Performance

- No performance or capacity targets exist.
- Whole-file rewrites and snapshot growth are documented limitations.
- No quantitative performance finding is supportable.

## 12. Diagram and ADR Assessment

- ADR-001–ADR-008 record the approved interface, persistence, runtime, timestamp, history, locking, binding, and initialization decisions.
- The context and component diagrams are internally consistent.
- The updated component diagram shows lock, initialization, store, write/replacement, and API error paths.
- ADR-008 correctly states that marker/store deletion cannot trigger automatic recovery.
- Backup/recovery is explicitly deferred, and implementation verification remains pending.

## 13. Risks and Dependencies

| Risk | Finding | Severity |
|---|---|---|
| Marker lifecycle must be implemented and verified consistently | DR-017 | Medium |
| Platform path canonicalization must be tested | DR-018 | Medium |
| Approved storage error mappings must be verified | DR-019 | Medium |
| Snapshot retention increases storage and privacy exposure | DR-009 | Medium |
| Validation and timestamp behavior must match the confirmed rules | DR-014 | Medium |
| No automated backup or recovery is provided | DR-010 | Medium |
| Diagram changes are documented; implementation paths remain to verify | DR-016 | Low |
| Approved unchanged-content no-op semantics must be tested | DR-020 | Low |

## 14. Recommendations

1. Implement and verify the approved marker, local-filesystem lock, and storage-error behavior.
2. Keep loopback-only exposure unless a separate security decision is made.
3. Implement and verify Uvicorn and the API entry point only in the implementation phase.
4. Preserve the documented backup/recovery limitation unless separately scoped.

## 15. Review Outcome

**Approved with Conditions**

- No unresolved Critical findings remain.
- DR-008, DR-010, DR-011, and DR-013 are resolved or resolved within their explicitly documented limitations.
- Stakeholder decisions dispositioned the CL items and R3 conditions DR-009, DR-014–DR-020; implementation verification remains pending.
- The outcome remains **Approved with Conditions** as recorded at R3; the conditions are now documented for implementation rather than treated as unresolved design questions.

## 16. Deferred Operational Items

- Automated backup and recovery are deferred; no automatic backup or pruning is provided.
- Platform-specific canonical path behavior and filesystem durability require implementation testing.
- The exact command interface for explicit store initialization is an implementation detail.
- Uvicorn dependency pinning and the API entry point remain implementation tasks.
- No performance, availability, capacity, or recovery-time targets were provided.

## 17. Required Follow-up

1. Implement and verify the stakeholder-approved dispositions recorded in the architecture.
2. Preserve the deferred backup/recovery limitation unless separately scoped.
3. Re-review is required if a substantive architecture change is made; this report does not claim an independent review of the stakeholder dispositions.

## 18. Handoff

- **Timing:** Handoff state at the conclusion of the R3 review.
- **Outcome:** Approved with Conditions.
- **Critical findings:** None.
- **Unresolved High findings:** None after R3 disposition.
- **Dispositioned Medium findings:** DR-009, DR-014, DR-015, DR-017, DR-018, DR-019; implementation verification remains pending.
- **Dispositioned Low findings:** DR-016 and DR-020.
- **Deferred limitation:** Backup and recovery.
- **Next party:** Orchestrator may hand off the approved plan for a user-selected implementation task.

## 19. Post-R3 Stakeholder Dispositions — 2026-11-19

The user accepted the proposed defaults and authorized the associated document updates:

| Item | Disposition |
|---|---|
| CL-001–CL-006 | Resolved in `docs/requirements.md`: retain snapshots but expose metadata only; timestamp version 1 at creation; titles immutable; reject empty/whitespace-only titles and content; use the confirmed messages and ISO 8601 `+05:30` timestamps. |
| API/runtime | FastAPI/Uvicorn, one worker, loopback binding, REST routes, request semantics, and JSON error contract are approved. |
| DR-017 | Use a versioned marker; fail closed for missing, mismatched, corrupt, or unsupported state. |
| DR-018 | Support local filesystems only and derive the lock from the canonical configured store path. |
| DR-019 | Map storage read/write/replacement failures to `503`; map unexpected internal failures to `500`. |
| DR-020 | Identical-content updates are no-ops. |
| DR-015 | Requirements and plan labels reflect approval; architecture remains labeled Approved with Conditions per R3. |
| DR-016 | Architecture diagram now depicts lock, initialization, store, write/replacement, and API error paths. |
| Backup/recovery | Deferred; no automatic backup, restore, or pruning is provided. |

These are stakeholder dispositions, not a new independent design review. Implementation and platform-specific verification remain outstanding.

## 20. R4 Independent Bounded Re-review — 2026-11-20

### Review boundary

This dated addendum records an independent, bounded re-review of the latest TASK-005 store-path policy amendment only. It does not replace or supersede R3, does not claim R4 replaced R3, and does not represent a new architecture approval beyond the existing user decision.

- **Review ID:** DOC-001-DR-R4
- **Prior independent outcome:** DOC-001-DR-R3 — **Approved with Conditions**
- **R4 outcome:** **Approved with Conditions**
- **Scope:** Architecture §5/§11 and the TASK-005 store-path amendment
- **Sources:** `docs/architecture.md`, `docs/impl-plan.md`, and the existing R3 content in this report
- **Current implementation status:** TASK-005 is In Progress; implementation and test execution are not yet verified.

The R3 outcome remains **Approved with Conditions**. R4 assesses the amended store-path policy for this specific scope and records a condition for implementation verification.

### DR-021 — TASK-005 store-path verification gap

- **Severity:** Medium
- **Type:** Documentation Inconsistency
- **Related requirement IDs:** No new requirement IDs are introduced.
- **Architecture section/component:** Architecture §5, Architecture §11, ADR-009, and implementation plan TASK-005
- **Description:** Architecture §5 and ADR-009 require startup rejection for unset, non-absolute, missing/non-file, and detectable UNC/remote store paths. They also require careful disclosure that unknown mounted network filesystems are unsupported by the approved local-only scope but may not be detectable. The implementation-plan TASK-005 completion and verification text did not explicitly require those checks or the corresponding regression tests.
- **Evidence:** Architecture §5 states the TASK-005 policy B and identifies the five startup rejection cases plus the unknown-mounted-network limitation. Architecture §11 requires TASK-005 startup rejection for those cases without claiming detection of unknown mounts. In `docs/impl-plan.md`, TASK-005 defines startup and entry-point work but its completion criteria and verification approach do not explicitly list the store-path checks or their regression tests.
- **Impact:** The implementation could satisfy the documented runtime/entry-point work while omitting an approved store-path rejection rule or failing to protect it with regression coverage. It could also accidentally represent unknown mounted network storage as detected.
- **Recommended action:** Add explicit TASK-005 completion and verification requirements for startup rejection of unset, non-absolute, missing/non-file, and detectable UNC/remote paths, and add regression tests for these cases plus the unsupported unknown-mounted-network limitation.
- **Status:** Open; condition must be tracked.

### Re-review assessment

- Policy B is coherent and preserves the approved local-filesystem-only supported scope.
- The amendment introduces no new independent security or runtime flaw within the bounded scope.
- Unknown mounted network filesystems remain an accepted operational limitation: they are unsupported and may not be detectable; implementation must not claim that they were detected.
- The R4 condition must be tracked until implementation explicitly adds and verifies the required checks and regression tests.
- Implementation verification remains pending.
- This re-review modified no source code or tests.
- This addendum does not modify `docs/architecture.md` or `docs/impl-plan.md`, and it does not claim a new architecture approval beyond the existing user decision.
