---
applyTo: "src/**/*.py,tests/**/*.py"
---
- Use type hints and a one-line docstring on every public function.
- One job per function; names must explain what they do.
- Put shared logic in one helper. Never copy-paste.
- Missing data returns the string "Not Found". Never guess.
- Catch API errors, timeouts, missing files, and empty repos; return a clear message.
- Never print or log tokens or secrets. Read credentials from environment variables.
- Every function gets tests: happy path, Not Found, missing field, empty repo, API failure.