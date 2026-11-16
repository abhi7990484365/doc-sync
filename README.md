# doc-sync

`doc-sync` scans a local repository or a GitHub repository and generates
`docs/PROJECT_DOC.md` with a deterministic project overview.

## Requirements

- Python 3.11
- Dependencies from `requirements.txt`

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
