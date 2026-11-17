---
description: Capture and finalize requirements from a user story.
agent: analyst
---

Workflow artifact directory: ${input:workflowDir:optional workflow artifact directory; leave blank to use docs/}

I will give you a user story (pasted in chat, attached as a Word file,
or as a JIRA/Confluence link/ID).

Follow these steps:

1. If I have not given the story yet, ask me for it and where it comes from.
2. Read the story and summarise it back to me in 3 lines to confirm understanding.
3. Ask clarifying questions, max 5 per round, and wait for my answers.
   Continue until I say "Create File".
4. After I say "Create File", write `requirements.md` in the supplied workflow
   artifact directory. If no directory was supplied, write
   `docs/requirements.md`. Use this structure:

   # Requirements
   ## 1. User Story  (original text, with source)
   ## 2. Goal and Scope  (in scope / out of scope)
   ## 3. Functional Requirements  (FR-1, FR-2, ... each testable)
   ## 4. Non-Functional Requirements  (NFR-1, ... security, reliability, performance, maintainability)
   ## 5. Assumptions and Constraints
   ## 6. Clarification Log  (each question I was asked and my answer)
   ## 7. Open Items  (anything marked "Not Found")

5. Do not write any code in this step.
6. Show me a short summary of the file and remind me to commit it.