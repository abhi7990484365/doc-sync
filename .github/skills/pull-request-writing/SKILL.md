---
name: pull-request-writing
description: Prepare, validate, commit, push, and publish a GitHub Pull Request for approved Doc-Sync implementation changes. Use when the PR Writer workflow is explicitly started.
---

# Pull Request Writing and Publishing Skill

## Objective

Complete the final SDLC handoff by converting approved implementation changes into a documented and published GitHub Pull Request.

## Step 1: Collect Project Evidence

Read the available project artifacts:

- `docs/requirements.md`
- `docs/architecture.md`
- `docs/design-review.md`
- `docs/impl-plan.md`
- `docs/code-review.md`
- `docs/test-report.md`

Inspect the actual source changes, tests, and changelog.

Identify the selected task and its requirement traceability.

## Step 2: Validate Readiness

Verify:

- Implementation is complete.
- Code review is complete.
- Critical and High findings are resolved.
- Testing evidence is available.
- Test limitations are documented.
- The changes correspond to the approved task.

### Decision

| Condition | Action |
|---|---|
| All gates pass | Continue |
| Code review has unresolved Critical/High findings | Stop |
| Code review is Changes Required | Stop |
| Test result is Failed | Stop and request direction |
| Test result is Blocked | Stop and request direction |
| Required evidence is missing | Stop and report missing evidence |
| Test result is Passed with Limitations | Continue and document limitations |

A draft PR after Failed or Blocked testing requires explicit user authorization.

## Step 3: Inspect Git Repository

Run appropriate Git commands to identify:

- Repository root
- Current branch
- Configured remotes
- Default branch
- Working-tree status
- Relevant unstaged and staged changes
- Existing commits and branch state

Inspect the diff before proceeding.

Identify approved implementation files and exclude unrelated changes.

Do not discard, overwrite, or silently stage unrelated user changes.

## Step 4: Prepare Branch

If the current branch is already an appropriate feature branch, reuse it.

If the current branch is the default branch:

1. Identify the selected task ID.
2. Create a descriptive feature branch.
3. Confirm the branch is active.
4. Do not overwrite an existing branch.

Example:

`feat/TASK-001-document-change-detection`

## Step 5: Prepare PR Documentation

Create or update `docs/pull-request.md`.

Use this structure:

# Pull Request

## Summary

Write exactly 2–3 sentences.

## Changes Made

Describe the implementation changes.

## Test Evidence

Include actual test commands, outcomes, and evidence.

## Known Limitations

Document verified limitations and unresolved issues.

## Reviewer Checklist

Include relevant review checks.

## Changelog

Summarize important changes.

Ensure the content is consistent with the actual code and verification results.

## Step 6: Stage and Commit

Stage only approved implementation files and `docs/pull-request.md`.

Review the staged diff before committing.

Use a meaningful commit message.

Example:

`feat: implement document change detection`

Do not:
- Stage all repository files blindly.
- Include credentials or secrets.
- Include unrelated changes.
- Rewrite previous commits without authorization.

## Step 7: Push Branch

Push the feature branch to the configured remote.

Verify the push result.

If authentication or permission fails, report the error and stop.

Never force-push.

## Step 8: Create GitHub Pull Request

Use GitHub CLI or an available GitHub integration.

Verify the repository, source branch, target branch, and pushed commit.

Check whether an appropriate PR already exists.

Create the PR with:

- Title describing the implementation.
- Body containing all six required sections.
- Source branch set to the feature branch.
- Target branch set to the repository's default branch unless the user specified another target.

If the PR already exists for this implementation, report it or update it only when the relationship is unambiguous.

Do not merge the PR.

## Step 9: Verify Publication

Verify that:

- The feature branch exists on the remote.
- The expected commit is present.
- The PR exists on GitHub.
- The PR title and body are correct.
- The PR URL is available.

Update `docs/pull-request.md` if needed to include the actual PR URL and publication details. If this requires another commit, commit and push that documentation update.

## Step 10: Return Execution Summary

Return:

- Repository
- Feature branch
- Target branch
- Commit hash
- Commit message
- Push result
- PR creation result
- PR URL
- Documentation file
- Test and review status
- Any errors or limitations

Report only verified results.

## Safety Boundaries

The explicitly started PR workflow authorizes staging approved changes, committing, pushing, and creating the PR.

It does not authorize:

- Merging the PR
- Force-pushing
- Deleting branches
- Discarding user changes
- Including unrelated files
- Bypassing review or testing gates
