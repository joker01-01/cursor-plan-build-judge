# Repository Purpose

This repository publishes the same Planner → Builder → Judge workflow for
Cursor and Claude Code.

The workflow converts an ambiguous request into a testable specification,
requires explicit approval before implementation, keeps execution inside the
approved scope, and reviews the result from repository evidence.

## Supported Skill Layouts

- Cursor English: `.cursor/skills/plan-build-judge/SKILL.md`
- Cursor Chinese: `.cursor/skills/plan-build-judge-zh/SKILL.md`
- Claude Code English: `.claude/skills/plan-build-judge/SKILL.md`
- Claude Code Chinese: `.claude/skills/plan-build-judge-zh/SKILL.md`

The Cursor and Claude Code copies for the same language must remain identical.
The compatibility check in `scripts/validate_skills.py` enforces that rule.

## Required Workflow Semantics

- Preserve the Planner → human approval → Builder → Judge sequence.
- Planner must stop for explicit approval by default.
- Builder must not silently expand or reduce the approved scope.
- Judge must use inspectable artifacts such as files, diffs, logs, commands,
  or test output instead of trusting a completion claim.
- A Fail verdict must return control to the user rather than starting an
  automatic self-repair loop.
- Keep `disable-model-invocation: true`; this workflow must be invoked
  intentionally by the user.

## Change Rules

- Update both platform copies in the same change.
- Keep English and Chinese versions behaviorally equivalent.
- Update `README.md` when installation, invocation, or supported platforms
  change.
- Avoid unrelated refactors or feature additions.
- Do not weaken approval, evidence, permission, or stop conditions.

## Validation Before Completion

Run:

```bash
python scripts/validate_skills.py
```

Then report:

- changed files;
- validation output;
- any behavior difference or remaining limitation.

Do not describe `CLAUDE.md` as an enforcement or security boundary. It provides
persistent project instructions; hard action blocking belongs in permissions or
hooks.
