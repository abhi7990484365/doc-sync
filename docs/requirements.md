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
