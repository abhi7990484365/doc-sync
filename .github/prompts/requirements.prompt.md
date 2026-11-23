---
description: Start the Doc-Sync requirements engineering workflow. Analyze user stories, clarify requirements, validate acceptance criteria, and create an approved requirements document.
agent: analyst
---

Workflow artifact directory: ${input:workflowDir:Optional workflow artifact directory; leave blank to use docs/}

# Objective

Analyze a stakeholder-provided user story and produce a complete, accurate, testable, and traceable requirements document for the Automated Documentation Sync (doc-sync) project.

# Configuration References

Before starting:

1. Follow `.github/copilot-instructions.md` for repository-wide rules.
2. Read `.github/instructions/analyst.instructions.md` for Analyst-specific rules.
3. Follow `.github/skills/requirements-discovery/SKILL.md` for the requirements engineering procedure.
4. Follow the responsibilities and boundaries defined in `.github/agents/analyst.agent.md`.

The Analyst Agent owns the requirements analysis. The Skill defines the reusable procedure. This Prompt starts the workflow and supplies task-specific inputs.

Do not duplicate or contradict the rules in these configuration files.

# Workflow

## Step 1: Obtain the User Story

Accept a user story through:

- Pasted text.
- Attached document.
- JIRA issue ID or link.
- Confluence page ID or link.

If no story is provided, ask the user to provide one and its source.

If a JIRA or Confluence reference is provided:

- Retrieve it using configured Atlassian tools.
- Verify that the source was actually retrieved.
- Preserve the original story and source reference.
- If retrieval fails or tools are unavailable, explain the limitation and request the content manually.
- Never fabricate source information.

## Step 2: Understand the Story

1. Read the complete user story.
2. Identify the business problem, intended outcome, and stakeholders.
3. Summarize your understanding in exactly three concise lines:
   - Who needs the capability.
   - What they need.
   - Why they need it.
4. Ask the user to confirm or correct your understanding.

Do not proceed with an incorrect or unconfirmed interpretation.

## Step 3: Clarify Requirements

Follow the Requirements Discovery Skill.

Ask no more than five clarification questions per batch.

Cover relevant areas:

- Business scope and objectives.
- Users and stakeholders.
- Inputs, outputs, and data.
- Functional behavior and business rules.
- Error handling and recovery.
- Security, privacy, and permissions.
- Performance, reliability, and availability.
- Constraints, dependencies, and integrations.

For every question:

- Explain why the answer matters.
- Provide possible answers only as examples.
- Allow custom answers.
- Wait for the user's response before asking the next batch.
- Do not repeat questions already answered.

Maintain a clarification log.

Classify information as:

- Confirmed.
- Assumption.
- Not Found.
- Open.

Never invent missing business details or measurable targets.

## Step 4: Analyze Requirements

After clarification is complete, prepare the following.

### Functional Requirements

Assign unique IDs:

- FR-001
- FR-002
- FR-003

Each requirement should include:

- Requirement ID and title.
- Clear, testable description.
- Business justification.
- Actor.
- Preconditions.
- Expected behavior.
- Priority, if supplied or agreed.
- Acceptance criteria.

### Non-Functional Requirements

Assign unique IDs:

- NFR-001
- NFR-002
- NFR-003

Consider relevant attributes:

- Security.
- Privacy.
- Performance.
- Reliability.
- Scalability.
- Maintainability.
- Usability.
- Observability.

Do not invent measurable targets. Mark unavailable targets as Not Found and include them in Open Items.

### Business Rules and Scope

Identify:

- Business rules.
- In-scope functionality.
- Out-of-scope functionality.
- Deferred requirements.
- Assumptions.
- Constraints.

Do not expand project scope without user confirmation.

### Requirement Prioritization

Use MoSCoW prioritization when priorities are supplied or agreed:

- Must Have.
- Should Have.
- Could Have.
- Won't Have (this time).

Do not independently make business priority decisions.

### Dependencies and Duplicate Detection

- Identify dependencies between requirements.
- Check existing requirements for duplicate or overlapping functionality when available.
- Highlight conflicting requirements.
- Do not silently merge or remove requirements.

## Step 5: Define Acceptance Criteria and Traceability

Write acceptance criteria using Given-When-Then format.

Assign unique IDs:

- AC-001
- AC-002
- AC-003

Cover relevant:

- Positive scenarios.
- Negative scenarios.
- Boundary conditions.
- Edge cases.
- Validation failures.
- Authorization failures.
- External-service failures.

Maintain the relationship:

`User Story -> Requirement -> Acceptance Criterion -> Test Scenario`

Assign test scenario IDs such as TC-001 and TC-002.

Identify:

- Requirements without acceptance criteria.
- Acceptance criteria without parent requirements.
- Requirements that cannot yet be tested.

Do not claim that test cases have been implemented or executed.

## Step 6: Review Requirements Quality

Before presenting the draft, validate:

1. Completeness.
2. Clarity.
3. Consistency.
4. Testability.
5. Traceability.
6. Scope control.
7. Source accuracy.
8. Requirement uniqueness.
9. Dependency identification.
10. Visibility of assumptions and unknowns.

Highlight unresolved issues instead of silently making decisions.

## Step 7: Present the Requirements Draft and Obtain Approval

Present the complete requirements draft for user review.

Include:

- User story and source.
- Business overview and objectives.
- Scope and out-of-scope items.
- Stakeholders and user roles.
- Functional requirements.
- Non-functional requirements.
- Business rules.
- Requirement priorities.
- Acceptance criteria.
- Negative scenarios and edge cases.
- Assumptions and constraints.
- Clarification log.
- Dependencies and risks.
- Open Items and Not Found items.
- Requirement traceability matrix.

Clearly highlight:

- Confirmed decisions.
- Assumptions.
- Unresolved questions.
- Requirements that are not yet testable.
- Potential conflicts or duplicates.

Do not create or modify files during this phase.

The exact file-creation approval command is:

`Create File`

Rules:

- Do not treat "looks good", "approved", "continue", or general confirmations as permission to create files.
- If the user requests changes, update the draft and present it again.
- Wait for the exact `Create File` command before writing the document.

## Step 8: Create requirements.md

Only after receiving the exact `Create File` command:

1. Use the supplied workflow artifact directory if provided.
2. Otherwise, create `docs/requirements.md`.
3. Do not create multiple competing requirements documents.
4. Preserve the original user story and source reference.
5. Clearly label assumptions, Not Found items, and unresolved decisions.
6. Follow `.github/instructions/analyst.instructions.md`.
7. Follow the document standards in the Requirements Discovery Skill.
8. Do not write application code or modify unrelated files.

Use this document structure:

# Requirements

## 1. Document Information
## 2. User Story and Source
## 3. Business Overview and Objectives
## 4. Goal and Scope
## 5. Stakeholders and User Roles
## 6. Functional Requirements
## 7. Non-Functional Requirements
## 8. Business Rules
## 9. End-to-End Business Workflow
## 10. Requirement Prioritization
## 11. Acceptance Criteria
## 12. Assumptions and Constraints
## 13. Clarification Log
## 14. Negative Scenarios and Edge Cases
## 15. Dependencies and Risks
## 16. Open Items
## 17. Requirement Traceability Matrix

## Step 9: Completion Report

After successful file creation:

1. State the exact file path.
2. Summarize the document contents.
3. List unresolved Not Found items and Open Items.
4. Confirm whether the file was successfully created.
5. Remind the user to review and commit it.

Do not commit, push, merge, or create a pull request.

Do not start architecture design or planning automatically.

Wait for separate user approval before moving to the next SDLC phase.

# Change Impact Analysis

If the user requests changes to an existing approved requirements document:

1. Identify the changed requirements.
2. Identify dependent requirements.
3. Identify affected acceptance criteria.
4. Identify affected test scenarios.
5. Explain potential scope and business impact.
6. Present proposed changes to the user.
7. Obtain approval before modifying the approved document.

Never silently change approved requirements.

# Boundaries

- Do not design technical architecture.
- Do not select implementation technologies.
- Do not write application source code.
- Do not create implementation tasks.
- Do not modify unrelated files.
- Do not commit, push, merge, or create pull requests.
- Do not bypass human approval.
- Do not start the next SDLC phase without separate user approval.

Prioritize accuracy, clarity, testability, and traceability over document length.
