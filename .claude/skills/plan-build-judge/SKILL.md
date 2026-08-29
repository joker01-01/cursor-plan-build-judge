---
name: plan-build-judge
description: >-
  Run a Planner → Builder → Judge workflow for complex tasks. First create a
  testable spec, then execute strictly against it, then review using verifiable
  evidence instead of self-reported completion.
disable-model-invocation: true
---

# Plan → Build → Judge

Use this skill for complex tasks that benefit from an explicit three-stage workflow:

1. **Planner** — turn the request into an execution-ready spec
2. **Builder** — implement strictly against that spec
3. **Judge** — accept or reject based on real artifacts and acceptance criteria

## When to use

- Multi-step work
- Ambiguous or incomplete requirements
- Tasks with explicit or implied acceptance criteria
- Cross-file or cross-module changes
- Work that should be specified before implementation
- Scripts, docs, config, analysis, or other deliverables that can be checked

## When not to use

- Simple Q&A
- Tiny one-line edits
- Cases where the user explicitly wants a one-step answer
- Situations where planning overhead clearly costs more than it saves

## Default interaction pattern

Default sequence:

1. Complete **Planner** only
2. Stop and wait for user confirmation or clarification
3. After go-ahead, run **Builder**
4. Then run **Judge**

Treat these as sufficient go-ahead signals after Planner:

- continue / OK / LGTM / go / build
- 继续 / 按这个做 / 开始实现
- Equivalent short approvals

If the user edits part of the spec while approving, treat the edited spec as authoritative and proceed.

If the user explicitly asks to run all stages in one shot, you may do so, but keep the three stage outputs clearly separated.

Do not skip Judge after Builder unless the user explicitly asks to skip review.

## Stage A: Planner

Understand the user request and convert it into an execution-ready specification.

You must output:

- **Objective**
- **Inputs**
- **Outputs**
- **Constraints**
- **Assumptions**
- **Edge cases**
- **Acceptance criteria**
- **Prompt for Builder**

Rules:

- Do not implement the final result in this stage unless the user explicitly asked for a one-step answer or a continuous full run.
- Prefer structured output.
- When ambiguity is low-impact, choose reasonable defaults and state them under Assumptions.
- Only ask the user to confirm high-impact ambiguities that materially change scope, risk, or success criteria.
- Keep the Builder prompt concrete enough that another agent could execute it without re-interpreting the original request.

## Stage B: Builder

Execute strictly according to the Planner spec (including any user edits made during approval).

Rules:

- Do not silently expand or shrink scope.
- Do not ignore constraints.
- If new assumptions are required, state them clearly before or while acting.
- Do not add unrequested features, refactors, or cleanups.
- Produce only the requested deliverable.
- Prefer making the acceptance criteria easy to verify (clear files, commands, outputs).

## Stage C: Judge

Review the Builder result against:

1. the original user request
2. the Planner spec (including approved edits)
3. the acceptance criteria

Rules:

- Do not rewrite the result unless the user explicitly asks for modification.
- Do not rely only on the Builder's self-description or completion claim.
- Prefer actual evidence: files, code diffs, command output, logs, test results, or other verifiable artifacts.
- If evidence is missing, say what could not be verified and treat that as a review gap.

You must output:

- **Verdict**: Pass / Fail
- **Issue list**
- **Severity** for each issue: High / Medium / Low
- **Suggested fixes**
- **Rework needed**: Yes / No

After a Fail verdict, stop. Do not automatically send work back to Builder. Wait for the user to decide whether to rework.

## Evidence standard

Judge evidence should be based on artifacts that exist outside the model's summary, such as:

- repository files and diffs
- terminal output
- test or lint results
- generated documents with inspectable content

A statement like "done" or "all criteria met" is not evidence.

## Relationship to user rules

This skill is the full shareable workflow. A short personal user rule may still remind the agent to use Planner → Builder → Judge on complex tasks. When both are present, follow this skill's detailed stage contracts for the actual run.
