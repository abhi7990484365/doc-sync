# Requirements

## 1. User Story

As a developer on a project team, I want a command-line tool that scans a
repository and generates `docs/PROJECT_DOC.md`, so that our documentation
always matches the code and does not go stale.

The tool is named `doc-sync`. It accepts a local repository folder or a GitHub
repository identified as `owner/name`. A GitHub Action runs it on pushes to
`main` and commits the generated document only when it changes.

## 2. Goal and Scope

In scope:
- Generate and update `docs/PROJECT_DOC.md` from local repositories and
  GitHub repositories.
- Generate the seven required documentation sections in the specified order.
- Report invalid inputs and GitHub API failures clearly with a non-zero exit.
- Run the generator from a GitHub Action on pushes to `main`.
- Add automated tests for normal, empty, missing, and failure cases.

Out of scope:
- Generating API reference documentation from source comments.
- Supporting repository hosts other than GitHub.
- A web interface.

## 3. Functional Requirements

- FR-1: The CLI shall accept a local repository directory as input.
- FR-2: The CLI shall accept a GitHub repository in `owner/name` form. Unless
  an output path is supplied, GitHub mode shall write
  `docs/PROJECT_DOC.md` under the current working directory.
- FR-3: The CLI shall create or update `docs/PROJECT_DOC.md` with these
  sections, in this exact order: Name, Description, Languages, Dependencies,
  Entry Points, How to Run, Last Commit.
- FR-4: Description shall come from the first non-empty paragraph in a
  supported README file. It shall not infer a description from the repository
  name or unrelated metadata.
- FR-5: Dependencies shall be read from `requirements.txt` only.
- FR-6: Entry Points shall include recognized common script entry points
  (including `main.py` and `app.py`) and declared packaging entry points.
- FR-7: Any required value that cannot be found shall be written exactly as
  `Not Found`.
- FR-8: An empty local repository shall produce the document with every
  section value set to `Not Found` and shall not crash.
- FR-9: Missing or invalid local paths and nonexistent GitHub repositories
  shall produce a clear error and a non-zero exit code.
- FR-10: GitHub API failures, timeouts, and rate limits shall be reported
  clearly and shall not crash or hang.
- FR-11: The GitHub token, when required, shall be read only from an
  environment variable. Credentials shall not be written to files.
- FR-12: Secrets, tokens, passwords, and absolute local paths shall not appear
  in the generated document, logs, or error messages.
- FR-13: Given unchanged repository content and commit metadata, repeated
  runs shall produce identical output.
- FR-14: The GitHub Action shall run on every push to `main` and commit the
  generated document only when it has changed.

## 4. Non-Functional Requirements

- NFR-1: The tool shall run from the command line on Python 3.11.
- NFR-2: A local scan of a typical repository with fewer than 1,000 files
  shall complete in under 10 seconds.
- NFR-3: The implementation shall use automated tests, including edge cases.
- NFR-4: The tool shall use standard-library functionality where practical
  and avoid adding unnecessary dependencies.

## 5. Acceptance Criteria

- AC1: Given a local repository with a README, `requirements.txt`, and a main
  script, the tool creates `docs/PROJECT_DOC.md` with all seven sections
  populated from available data.
- AC2: Any value that cannot be found is written exactly as `Not Found`; the
  tool does not guess or invent values.
- AC3: An empty repository produces a document where every section value is
  `Not Found` and the command exits without crashing.
- AC4: A missing or invalid path, or a GitHub repository that does not exist,
  produces a clear error and a non-zero exit code.
- AC5: GitHub API failures, timeouts, and rate limits are reported clearly
  without crashing or hanging.
- AC6: Secrets, tokens, and passwords do not appear in the generated
  document, logs, or error messages. The GitHub token is read only from an
  environment variable.
- AC7: Running the tool twice against an unchanged repository produces
  identical output.
- AC8: The GitHub Action runs on pushes to `main` and commits the document
  only when it has changed.

## 6. Clarification Log

- Description source: first non-empty README paragraph.
- Entry point detection: common script files plus declared packaging entry
  points.
- Dependency source: `requirements.txt` only.

## 7. Agent Orchestrator Requirements

### 7.1 User Story

As a project user, I want an orchestrator that accepts a user story and
requirement as input and passes each agent's output to the next agent, so that
the project workflow can run through its existing agents without manually
re-entering their outputs.

### 7.2 Goal and Scope

In scope:
- Add a Copilot workflow that coordinates the existing project agents.
- Pass named artifacts between stages in this order: analyst, architect,
  design reviewer, planner, developer, code reviewer, and tester.
- Run all implementation-plan tasks in dependency order, one task at a time.
- Preserve the existing human approval requirements.
- Stop and report when a stage fails or its required output is missing.

Out of scope:
- Changing the behavior of the `doc-sync` CLI or generated project document.
- Replacing or duplicating the responsibilities of the existing agents.
- Running stages without the required user approvals.

### 7.3 Functional Requirements

- FR-15: The orchestrator shall accept user-provided user story and
  requirement text as workflow inputs.
- FR-16: The orchestrator shall run the existing agents in this order:
  analyst, architect, design reviewer, planner, developer, code reviewer,
  and tester.
- FR-17: The orchestrator shall pass the named outputs from each completed
  stage to the next relevant stage, including `requirements.md`,
  `architecture.md`, `design-review.md`, `impl-plan.md`, implementation
  changes, `code-review.md`, and `verification-report.md`.
- FR-18: The planner shall receive the requirements, architecture, and design
  review outputs before creating the implementation plan.
- FR-19: The orchestrator shall process every implementation-plan task in
  dependency order, invoking the developer for one task at a time and
  confirming its blockers are complete before starting it.
- FR-20: The orchestrator shall obtain user approval before each stage writes
  or changes files, before each implementation task begins, and before
  committing, pushing, or creating/updating a pull request.
- FR-21: The orchestrator shall run the code reviewer after all implementation
  tasks are complete, the tester after code review, and the PR stage only
  after verification succeeds.
- FR-22: If an agent fails or does not produce a required output, the
  orchestrator shall stop before starting dependent stages and report which
  stage and output are missing.
- FR-23: The tester shall verify the completed work against the requirements
  and save its results in the workflow artifact directory.
- FR-24: Each workflow run shall store all named artifacts in a unique,
  sanitized `docs/workflows/<workflow-id>/` directory without overwriting
  project-level documentation or artifacts from another run.
- FR-25: After successful verification and user approval, the orchestrator
  shall commit only the workflow's approved changes, push the current
  non-base branch, and create a pull request to `main` or update an existing
  open pull request for the same head and base.
- FR-26: The PR stage shall create a workflow-specific PR description with
  Summary, Changes Made, Test Evidence, Known Limitations, and Reviewer
  Checklist sections, based only on repository changes and actual verification
  results.
- FR-27: The PR stage shall stop without committing, pushing, or creating a
  pull request if the worktree contains unapproved changes, the current branch
  is the base branch, required GitHub authentication or remote information is
  unavailable, or verification failed. It shall never merge a pull request.

### 7.4 Non-Functional Requirements

- NFR-5: The workflow shall use the repository's existing Copilot agents and
  named artifacts rather than duplicating agent responsibilities.
- NFR-6: Artifact handoffs shall be sequential and preserve the source output
  so downstream stages can use it without manual re-entry.
- NFR-7: The workflow shall follow the repository's security rules and shall
  not expose secrets in prompts, artifacts, logs, or generated output.

### 7.5 Acceptance Criteria

- AC9: Given user story and requirement text, the workflow provides both to
  the analyst stage.
- AC10: Each stage receives the required named artifacts from preceding
  stages, and no dependent stage starts before its inputs exist.
- AC11: All implementation-plan tasks are processed in dependency order, one
  task at a time, with user approval before each task.
- AC12: The workflow pauses for required file-write approvals and does not
  bypass them.
- AC13: A failed stage or missing output stops downstream execution and
  reports the failure and stage.
- AC14: On successful completion, code review and verification have run, and
  the verification report is available.
- AC15: Each run stores its artifacts in a unique, sanitized workflow
  directory and does not overwrite project-level documentation or another
  run's outputs.
- AC16: After successful verification and explicit approval, the workflow
  commits only approved workflow changes and pushes the non-base branch.
- AC17: The workflow creates a pull request to `main`, or updates an existing
  open pull request for the same head and base, with all five required
  description sections and factual test evidence.
- AC18: The workflow does not publish on failed verification, include
  unapproved work, push the base branch, or merge a pull request.

### 7.6 Clarification Log

- Initial inputs: user story and requirement text.
- Agent sequence: analyst, architect, planner, developer, and tester, with
  design review before planning and code review before verification.
- Implementation scope: all plan tasks, processed one at a time.
- Approval policy: preserve the existing user approval gates.
- Handoff format: named artifacts, including requirements and architecture
  documents.
- Artifact location: each run has a unique, sanitized directory under
  `docs/workflows/`.
- Publication: retain explicit approval before commit, push, and PR
  creation/update; default PR base is `main`; never merge automatically.
