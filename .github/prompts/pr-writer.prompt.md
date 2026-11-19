---
name: Create and Publish Pull Request
description: Validate the completed Doc-Sync implementation, commit and push approved changes, and create a GitHub Pull Request.
agent: pr-writer
---

# Create and Publish GitHub Pull Request

Start the PR Writer workflow for the approved Doc-Sync implementation.

## Instructions

### Step 1: Read Project Artifacts

Read and validate:

- `docs/requirements.md`
- `docs/architecture.md`
- `docs/design-review.md`
- `docs/impl-plan.md`
- `docs/code-review.md`
- `docs/test-report.md`

Inspect the actual implementation, tests, changelog, and Git repository.

### Step 2: Validate Readiness

Verify:

- Implementation is complete.
- Code review is complete.
- No unresolved Critical or High code-review findings remain.
- Testing is complete.
- Test evidence is available.
- Changes correspond to the approved implementation task.

If a required gate is not satisfied, stop and report the reason.

If tests are Failed or Blocked, ask whether to resolve the issue or explicitly publish a draft PR.

### Step 3: Inspect Git

Identify:

- Repository
- Current branch
- Default branch
- Remote configuration
- Working-tree changes
- Relevant implementation files

Inspect the actual diff.

Exclude unrelated user changes.

### Step 4: Prepare Feature Branch

Reuse the appropriate feature branch if available.

If currently on the default branch, create a descriptive feature branch based on the actual implementation task.

Do not push directly to the default branch.

### Step 5: Generate PR Documentation

Create or update `docs/pull-request.md`.

Include:

1. Summary (2–3 sentences)
2. Changes Made
3. Test Evidence
4. Known Limitations
5. Reviewer Checklist
6. Changelog

### Step 6: Commit and Push

Stage only approved implementation files and PR documentation.

Review the staged changes.

Create a meaningful commit and push the feature branch to the configured remote.

Verify the actual commit and push results.

### Step 7: Create GitHub PR

Use authenticated GitHub CLI (`gh`) or an available GitHub integration.

Verify the repository, source branch, and target branch.

Check for an existing PR before creating a new one.

Create the PR using the required six-section structure.

Do not merge the PR.

### Step 8: Verify and Report

Verify that the PR exists and obtain its actual URL.

Return:

- Repository
- Source branch
- Target branch
- Commit message
- Commit hash
- Push status
- PR creation status
- PR URL
- Code review status
- Test status
- Any limitations or errors

## Execution Rule

The user explicitly starting this prompt authorizes the PR Writer to commit approved changes, push the feature branch, and create the GitHub PR.

Do not ask for redundant confirmation.

Never bypass readiness gates or include unrelated changes.
