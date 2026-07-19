# Cursor Plan-Build-Judge

A reusable Cursor skill for complex tasks.

It applies a three-stage workflow:

- **Planner** — turn a vague request into a clear, testable spec
- **Builder** — implement strictly against that spec
- **Judge** — review the result against the original request, the spec, and acceptance criteria using real evidence

Chinese README: [README.zh-CN.md](./README.zh-CN.md)

## Why this exists

AI often fails in three ways:

1. It starts implementing too early
2. It silently changes scope while building
3. It judges its own work from summaries instead of evidence

This skill is designed to reduce those failures with:

- **spec-first** planning
- **bounded** execution
- **evidence-based** review

## Skill locations

```text
.cursor/skills/plan-build-judge/SKILL.md      # English
.cursor/skills/plan-build-judge-zh/SKILL.md   # Chinese
```

## What it does

### Planner

Outputs:

- Objective
- Inputs
- Outputs
- Constraints
- Assumptions
- Edge cases
- Acceptance criteria
- Prompt for Builder

By default, the workflow **stops after Planner** and waits for confirmation.

### Builder

- follows the approved spec strictly
- avoids scope creep
- states new assumptions clearly

### Judge

- checks actual artifacts, not just self-reported completion
- returns Pass / Fail, issues, severity, and fix suggestions
- does **not** auto-rework after Fail; it waits for the user

## When to use

Use this skill for:

- coding tasks
- scripts
- documentation generation
- structured analysis
- configuration changes
- any complex task with checkable outputs

## When not to use

Do not use this skill for:

- simple Q&A
- tiny edits
- one-shot answers where planning overhead is unnecessary

## Installation

Copy either skill folder into your Cursor project or personal skills directory:

```text
.cursor/skills/plan-build-judge/
# or
.cursor/skills/plan-build-judge-zh/
```

Then invoke it manually as a Cursor skill.

This skill sets `disable-model-invocation: true`, so the model will not auto-select it. That is intentional for a heavyweight workflow.

### Manual install

Clone or copy this repository, then place the skill folder into your workspace or personal Cursor skills directory.

## Example walkthrough

Task (intentionally vague):

> Make this API more secure.

### 1) Planner (stops here by default)

Example spec shape:

- **Objective**: Reduce common abuse and credential-exposure risks on the existing HTTP API without a full security rewrite
- **Inputs**: Current API routes/handlers, auth middleware (if any), config/env usage
- **Outputs**: Minimal code/config changes plus a short note of what was and was not hardened
- **Constraints**: No new major dependencies unless required; do not redesign the API surface; keep existing happy-path behavior
- **Assumptions** (defaults chosen because the request was vague):
  - Focus on authn/authz gaps, secrets in code/config, and basic rate limiting on sensitive endpoints
  - Out of scope: WAF, infra hardening, pentest, full OWASP program
- **Edge cases**: Missing auth middleware; local-only dev routes; endpoints that must stay public
- **Acceptance criteria**:
  1. Sensitive endpoints require authentication unless explicitly marked public
  2. No secrets hardcoded in source
  3. Login/auth-sensitive route has rate limiting with a documented limit
  4. Unauthenticated access to protected routes fails with the existing error style
- **Prompt for Builder**: Implement only the items above; do not refactor unrelated code.

User go-ahead examples: `LGTM`, `继续`, `按这个做`.

### 2) Builder

Implements only the approved security scope. Does not "also clean up" unrelated files.

### 3) Judge

Reviews with evidence, for example:

- diff shows auth checks and rate-limit wiring on the agreed routes
- secret scan / file inspection shows no hardcoded credentials
- a request/repro note or test output shows protected routes reject anonymous access

Possible Judge result:

- **Verdict**: Fail
- **Issue**: Rate limiting was added globally instead of only on sensitive routes
- **Severity**: High
- **Rework needed**: Yes

The workflow stops there until the user asks for changes.

## Relationship to Cursor User Rules

You can keep a short personal rule that reminds the agent to use Planner → Builder → Judge on complex tasks.

Use:

- a **short user rule** for default reminders
- this **skill** as the full stage contract when you explicitly invoke it

## Files

- `.cursor/skills/plan-build-judge/SKILL.md`
- `.cursor/skills/plan-build-judge-zh/SKILL.md`
- `README.md`
- `README.zh-CN.md`
- `LICENSE`

## License

MIT
