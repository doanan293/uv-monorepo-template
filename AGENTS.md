# AI Agent Rules

uv workspace monorepo: every `services/<name>/` is an independent package (HTTP API or
background worker) built with Clean Architecture. The services that ship with the
template are samples — follow the rules, not their names.

@docs/engineering-guide.md

## Workflow
- Never run `git commit` or `git push`, and never bypass hooks or CI (`--no-verify`);
  humans commit
- Before saying a task is done, run in the service directory — all must pass:
  ```bash
  uv run ruff check . && uv run ruff format --check .
  uv run pyrefly check --min-severity warn
  uv run pytest --cov=src --cov-fail-under=80
  ```
- Fix lint and type errors in code: no `# noqa`, `# type: ignore`, `# pyrefly: ignore`,
  and no disabled rules
- Never write secrets into files other than `.env`
- After fixing review comments, give a one-line commit message
  `fix review: <summary>` and a PR comment draft with one line per comment:
  `<reviewer comment> → <fix>`
- Writing or changing an LLM prompt: follow `docs/prompting-instruction.md`
- Branches, PRs and reviews: `.github/CONTRIBUTING.md`

## Conversation
- Keep output concise — do not over-explain what the code already makes clear
- When requirements are unclear: ask rather than assume
