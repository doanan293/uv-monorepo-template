<!--
Pull request template.
Rule: delete any section that does not apply.
Source of truth: business = ticket, technical/AC = issue, conventions = AGENTS.md, docs/engineering-guide.md and .github/CONTRIBUTING.md.
A PR is the evidence that the code meets that contract.
-->

## Linked Issues
<!-- Issue/ticket links, so the change can be traced back. -->
- **Issue:** Closes #
- **Ticket:** <!-- delete if the issue is already linked -->

## Summary
<!-- Main changes; one line = one change that matters to the reviewer. -->
-
-

## Type
<!-- Keep one, delete the rest. -->
`Feature` · `Bug Fix` · `Hotfix` · `Refactor` · `Docs` · `Performance` · `Infra` · `Chore`

## Acceptance Criteria
<!-- Map each AC of the issue to its evidence (test / command / file). Do NOT copy the AC text. -->
| AC | Status | Evidence |
|----|--------|----------|
|    | ✅     |          |

## Review Focus
<!-- Where the reviewer should look first: risky spots, trade-offs, points to confirm. -->
-

## Out of Scope
<!-- What this PR deliberately does NOT do. -->
-

## How to Test
<!-- Commands or steps the reviewer (or an agent) can re-run. -->
```bash

```

## Operational Impact
<!-- Keep only the lines this PR touches; delete the section if none. -->
- **Env vars:** new/changed variable + default + added to `.env.example` and `docker-compose.yml`
- **New deps:** package@version + reason
- **Breaking API:** impact + who is affected + docs updated
- **Release with:** PRs/services deployed together + order

## Self-Verification
<!-- This list is the definition of done. Tick = ran it and have the evidence, not a formality. -->
- [ ] CI passes: lint (ruff, pyrefly), test, secret scan
- [ ] `/code-review` run and every finding fixed
- [ ] No hardcoded secrets, keys or tokens
- [ ] Coverage ≥ 80% (or reason for N/A)
- [ ] Clean Architecture layer rules respected
- [ ] AC mapping above checked against the issue
