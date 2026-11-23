---
name: pull-request-writing
description: Prepare, validate, commit, push, and publish a GitHub Pull Request for approved Doc-Sync implementation changes. Use when the PR Writer workflow is explicitly started.
---

# Pull Request Writing and Publishing Skill

## Objective

Publish a Pull Request for approved implementation changes and report only verified results.

## 1. Review the Evidence

Read the available project artifacts:

- `docs/requirements.md`
- `docs/architecture.md`
- `docs/design-review.md`
- `docs/impl-plan.md`
- `docs/code-review.md`
- `docs/test-report.md`

Inspect the actual code changes, tests, and changelog. Identify the selected task and confirm its requirement traceability.

## 2. Check Readiness

Confirm that:

- The implementation is complete and matches the approved task.
- Code review is complete, with no unresolved Critical or High findings.
- Testing evidence is available.
- Test limitations are documented.

Stop and report the reason if required evidence is missing, code review requires changes, or tests failed or are blocked. A draft PR after failed or blocked testing requires explicit user authorization.

Tests passed with limitations may proceed if the limitations are documented.

## 3. Inspect the Repository

Use local Git to check the repository root, branch, remotes, default branch, working-tree status, and relevant changes. Inspect the diff before proceeding.

Include only approved implementation files. Do not discard, overwrite, or silently stage unrelated user changes.

If local Git or `gh` is unavailable, use available GitHub MCP tools for supported remote operations. MCP cannot verify uncommitted local changes or replace local staging, committing, or pushing. If local changes need publishing and local Git is unavailable, stop before creating the PR.

## 4. Prepare the Branch

Reuse the current branch if it is an appropriate feature branch.

If the current branch is the default branch, create a descriptive feature branch for the selected task. Do not overwrite an existing branch.

Example: `feat/TASK-001-document-change-detection`

## 5. Prepare PR Documentation

Create or update `docs/pull-request.md` with these sections:

- **Summary** — exactly 2–3 sentences
- **Changes Made**
- **Test Evidence** — actual commands, results, and evidence
- **Known Limitations**
- **Reviewer Checklist**
- **Changelog**

Keep the document consistent with the code and verified test results.

## 6. Commit and Push

Stage only approved implementation files and `docs/pull-request.md`. Review the staged diff before committing.

Use a meaningful commit message. Do not stage everything blindly, include secrets or unrelated changes, rewrite previous commits without authorization, or force-push.

Push the feature branch to the configured remote and verify the result. If authentication or permissions fail, report the error and stop.

## 7. Create the Pull Request

Use GitHub CLI or available GitHub MCP tools.

Before creating the PR, verify the repository, source and target branches, and that the expected commit is on the remote. Check whether a suitable PR already exists.

Create the PR with:

- A title that describes the implementation
- A body containing all six sections from `docs/pull-request.md`
- The feature branch as the source
- The default branch as the target, unless the user specified another target

If a PR already exists, report it or update it only when its relationship to this implementation is clear.

Do not merge the PR.

## 8. Verify Publication

Verify the remote branch, expected commit, PR title and body, and PR URL.

Update `docs/pull-request.md` with the actual PR URL and publication details. If the update requires another commit, commit and push it, then verify the result.

## 9. Report the Result

Return:

- Repository and branches
- Commit hash and message
- Push result
- PR creation result and URL
- Documentation file
- Test and review status
- Any errors or limitations

Report only verified results.

## Safety Boundaries

This explicitly started workflow authorizes staging approved changes, committing, pushing, and creating a PR.

It does not authorize merging the PR, force-pushing, deleting branches, discarding user changes, including unrelated files, or bypassing review and testing gates.