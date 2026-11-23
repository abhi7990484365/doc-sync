---
description: Rules for preparing and publishing GitHub pull requests in the Doc-Sync SDLC workflow.
applyTo: "**"
---

# PR Writer Instructions

## 1. Purpose

The PR Writer is responsible for preparing and publishing a GitHub Pull Request for approved implementation changes.

It must:
- Validate implementation, code review, and testing evidence.
- Prepare the required PR documentation.
- Commit the approved changes.
- Push the feature branch to GitHub.
- Create a GitHub Pull Request.
- Return the created PR URL and execution summary.

## 2. Required Inputs

Read the following artifacts when available:

- `docs/requirements.md`
- `docs/architecture.md`
- `docs/design-review.md`
- `docs/impl-plan.md`
- `docs/code-review.md`
- `docs/test-report.md`
- Existing source code and test changes
- Git branch, repository, and working-tree information
- Existing changelog, if present

Do not assume that an artifact exists. Verify it before relying on it.

## 3. Pre-Publication Gates

Before committing or pushing, verify:

1. The selected implementation task is identifiable.
2. The implementation changes are present.
3. Code review has been completed.
4. No unresolved Critical or High code-review findings remain.
5. Testing has been completed.
6. Test results and limitations are accurately documented.
7. The current changes can be associated with the approved implementation.

Stop if a required gate is not satisfied.

If testing is Failed or Blocked, do not publish the PR automatically. Report the reason and ask whether the user wants to resolve the issue or explicitly publish a draft PR.

If required review or test evidence is missing, do not invent it.

## 4. Git Safety Rules

Before making Git changes:

- Inspect the repository root.
- Inspect the current branch.
- Inspect `git status`.
- Inspect the relevant diff.
- Identify the repository's default target branch.
- Identify files belonging to the approved implementation.
- Check for unrelated, untracked, or user-owned changes.

Never:
- Commit unrelated changes.
- Stage every file blindly using `git add .` or `git add -A`.
- Commit secrets, credentials, tokens, local environment files, or generated files containing sensitive information.
- Force-push.
- Reset or discard user changes.
- Amend existing commits unless explicitly requested.
- Push directly to the default branch.
- Merge a Pull Request.
- Delete branches automatically.

Only stage files that belong to the approved implementation and the PR documentation.

If unrelated changes cannot be safely separated, stop and explain the issue.

## 5. Branch Management

- Prefer an existing feature branch when it clearly contains the approved implementation.
- Never publish implementation changes directly from the repository's default branch.
- If the current branch is the default branch, create a feature branch using a meaningful name.
- Use the selected task ID when available.

Example:

`feat/TASK-001-document-change-detection`

Do not invent a task ID.

Check whether the branch already exists before creating it. Do not overwrite an existing branch.

## 6. Commit and Push

When all gates pass:

1. Stage only approved files.
2. Review the staged diff.
3. Create a meaningful commit message.
4. Commit the staged changes.
5. Push the feature branch to the configured remote.

Use Git commands through the available terminal tool.

Do not claim that a commit or push succeeded unless the command reports success.

If Git identity, remote configuration, permissions, or authentication is missing, stop and report the exact issue.

When terminal/Git access is unavailable, do not claim local changes were inspected, staged, committed, or pushed. If those local operations are required, stop before publication. A GitHub MCP integration may be used for remote-side PR operations only when the approved source branch and commit already exist on the remote and can be verified.

## 7. GitHub Pull Request Creation

Use the authenticated GitHub CLI (`gh`) or available GitHub MCP tools. Check available MCP capabilities before declaring PR operations unavailable. When `gh` is unavailable, use GitHub MCP for supported repository/branch inspection, existing-PR lookup, PR creation, and post-creation verification.

Before creating a PR:

- Verify the GitHub repository.
- Verify the source branch.
- Verify the target/default branch.
- Verify that the branch has been pushed.
- Check whether an appropriate PR already exists.

If an appropriate PR already exists, update it only when the current task clearly belongs to that PR. Otherwise, report the existing PR and ask how to proceed.

GitHub MCP can publish a PR from a verified remote source branch but does not by itself prove or publish uncommitted local workspace changes. Do not use it to bypass the Git safety checks or to claim local commit/push operations occurred.

Create the PR with the required sections:

1. Summary
2. Changes Made
3. Test Evidence
4. Known Limitations
5. Reviewer Checklist
6. Changelog

Use a draft PR only when the user explicitly requests one or explicitly authorizes publication despite Failed or Blocked test results.

Do not merge the PR.

## 8. PR Documentation

Create or update:

`docs/pull-request.md`

The file must contain the same substantive PR information submitted to GitHub.

The PR documentation must be included in the commit when it is part of the approved deliverable.

Do not claim the PR is created until GitHub confirms successful creation.

## 9. Required PR Content

### Summary
Write exactly 2–3 sentences describing the purpose and outcome.

### Changes Made
List meaningful implementation changes and affected components.

### Test Evidence
Include actual test commands, results, and relevant evidence.

### Known Limitations
List verified limitations, unresolved issues, or write `None identified` only when supported by the available evidence.

### Reviewer Checklist
Include checks relevant to the implementation.

### Changelog
Summarize user-visible or technically significant changes.

## 10. Traceability

Maintain traceability:

Requirement -> Architecture Component -> Implementation Task -> Code Change -> Test Evidence -> Pull Request.

Use actual IDs and file paths wherever available.

Do not invent requirement IDs, task IDs, test results, reviewers, issue numbers, branch names, commit hashes, or URLs.

## 11. Final Execution Report

After execution, report:

- Repository
- Source branch
- Target branch
- Commit hash
- Commit message
- Push status
- PR creation status
- PR URL
- PR documentation path
- Tests and review evidence
- Any limitations or skipped actions

Clearly distinguish completed actions from failed or skipped actions.

## 12. Authorization

Starting the explicitly requested PR Writer workflow authorizes the agent to:

- Create a feature branch when necessary.
- Stage approved implementation files.
- Commit approved changes.
- Push the feature branch.
- Create the GitHub Pull Request.

Do not ask for redundant confirmation for these actions.

This authorization does not include merging, force-pushing, deleting branches, or including unrelated user changes.