# doc-sync

`doc-sync` scans a local repository or a GitHub repository and generates
`docs/PROJECT_DOC.md` with a deterministic project overview.

## Requirements

- Python 3.11
- Dependencies from `requirements.txt`
- Before changing files, check the current Git branch. If it is `main`, create
  and switch to a new working branch before making any changes.

Install dependencies with:

```shell
python -m pip install -r requirements.txt
```

## Usage

Scan a local repository (the current directory by default):

```shell
python -m src.doc_sync .
```

Scan a GitHub repository using `owner/name`:

```shell
python -m src.doc_sync owner/name
```

GitHub mode writes `docs/PROJECT_DOC.md` under the current working directory.
Set `GITHUB_TOKEN` in the environment to authenticate API requests; public
repositories can be read without a token. You can choose a different output
location with `--output`:

```shell
python -m src.doc_sync owner/name --output docs/PROJECT_DOC.md
```

The generated document contains Name, Description, Languages, Dependencies,
Entry Points, How to Run, and Last Commit sections. Missing values are written
as `Not Found`.

## Agent Workflow

The workspace also provides a Copilot orchestrator for the project SDLC
agents. In VS Code Copilot Chat, select the `orchestrator` agent or use the
`orchestrate` prompt, then provide both a user story and requirement text.

The orchestrator passes approved artifacts through the analyst, architect,
design review, planner, developer, code review, tester, and final PR-writer
stages. It pauses for clarifications and approvals, runs implementation
tasks one at a time, and stops if a stage fails or its required output is
missing. After successful verification, the PR writer can commit approved
changes, push the feature branch, and create a pull request or update an
existing open one, with separate approval before each publication action.
It never merges automatically. Each run stores its artifacts in a unique
directory under `docs/workflows/` without replacing the project-level
documentation.
