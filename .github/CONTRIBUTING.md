# Contributing

How work moves from issue to merged pull request. Code rules:
[`docs/engineering-guide.md`](../docs/engineering-guide.md). Rules for coding agents:
[`AGENTS.md`](../AGENTS.md).

## Issues and branches
- Open each task with the [Task template](ISSUE_TEMPLATE/task.md); give it a Type
  (Task/Bug/Feature), labels `type:*` + `service:*`, and add it to `<project-board>`
- Branch: `<PROJECT>-<issue>` (e.g. `PROJ-123`)
- Commits: the first is the branch name; then `fix review: <summary>` for review
  fixes and `fix: <summary>` for anything you found yourself

## Pull requests
- **1 PR = 1 subtask** — never mix a bug fix, a feature and a refactor
- At most ~400 lines of diff; split larger work
- Title = issue title; body links the issue with `Closes #<issue>`; same labels as the
  issue; Assignee = author, Reviewer = lead
- Fill out the [PR template](pull_request_template.md); its Self-Verification list is
  the definition of done
- Never merge your own PR

## CI
Three required jobs run on every PR (`.github/workflows/ci.yml`):

| Job | Checks |
|---|---|
| `lint` | ruff, pyrefly on every service |
| `test` | pytest with coverage ≥ 80% for changed services (all services when root config or `uv.lock` changes) |
| `secret-scan` | gitleaks over the PR's commits |

New services are picked up automatically. Never bypass CI or hooks (`--no-verify`).

## Reviewing
1. Run `/code-review <PR_NUMBER>`.
2. Check that CI is green and every Self-Verification item in the PR is ticked with
   real evidence; for UI changes, ask for screenshots.
3. Approve or request changes with specific comments, then squash-merge:
   ```bash
   gh pr review <PR_NUMBER> --approve
   gh pr merge <PR_NUMBER> --squash --delete-branch
   ```
