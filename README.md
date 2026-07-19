# Cursor Plan-Build-Judge

A reusable Cursor skill for complex tasks.  
一个可复用的 Cursor Skill，用于复杂任务。

It applies a three-stage workflow / 采用三阶段工作流：

- **Planner** — turn a vague request into a clear, testable spec  
  **规划** — 把模糊需求变成清晰、可验收的规格
- **Builder** — implement strictly against that spec  
  **执行** — 严格按规格实现
- **Judge** — review with real evidence against the request, spec, and acceptance criteria  
  **验收** — 对照原始需求、规格与验收标准，基于真实证据审查

## Why this exists / 为什么需要它

AI often fails in three ways / AI 常在三件事上失手：

1. It starts implementing too early / 还没澄清需求就直接开写
2. It silently changes scope while building / 实现时偷偷改范围
3. It judges its own work from summaries instead of evidence / 审查时只根据自己刚写的摘要打分

This skill reduces those failures with / 这个 Skill 用三点降低这些失败：

- **spec-first** / **先规格化**
- **bounded execution** / **执行不越界**
- **evidence-based review** / **验收看证据**

## Skill locations / Skill 位置

```text
.cursor/skills/plan-build-judge/SKILL.md      # English / 英文
.cursor/skills/plan-build-judge-zh/SKILL.md   # Chinese / 中文
```

## What it does / 它做什么

### Planner / 规划

Outputs / 输出：

- Objective / 目标
- Inputs / 输入
- Outputs / 输出
- Constraints / 约束
- Assumptions / 假设
- Edge cases / 边界情况
- Acceptance criteria / 验收标准
- Prompt for Builder / 给 Builder 的执行提示

By default, the workflow **stops after Planner** and waits for confirmation.  
默认在 **Planner 之后停住**，等待确认。

### Builder / 执行

- follows the approved spec strictly / 严格按已确认规格执行
- avoids scope creep / 避免范围蔓延
- states new assumptions clearly / 新假设必须说清楚

### Judge / 验收

- checks actual artifacts, not self-reported completion / 检查实际产物，而不是只看「已完成」自述
- returns Pass / Fail, issues, severity, and fix suggestions / 输出：通过/不通过、问题、严重程度、修改建议
- does **not** auto-rework after Fail; waits for the user / **不通过后不自动返工**，等待用户决定

## When to use / 何时使用

Use for / 适合：

- coding tasks / 编码任务
- scripts / 脚本
- documentation generation / 文档生成
- structured analysis / 结构化分析
- configuration changes / 配置修改
- any complex task with checkable outputs / 任何有可检查产物的复杂任务

## When not to use / 何时不要使用

Do not use for / 不适合：

- simple Q&A / 简单问答
- tiny edits / 极小改动
- one-shot answers where planning overhead is unnecessary / 规划成本明显高于收益的一步直出场景

## Installation / 安装

Copy either skill folder into your Cursor project or personal skills directory:  
把对应 Skill 目录复制到 Cursor 项目或个人 skills 目录：

**Project / 项目级**

```text
your-project/
  .cursor/skills/plan-build-judge/
  # or / 或
  .cursor/skills/plan-build-judge-zh/
```

**Personal / 个人级（所有项目可用）**

```text
~/.cursor/skills/plan-build-judge/
# Windows:
C:\Users\<you>\.cursor\skills\plan-build-judge\
```

Then invoke it manually as a Cursor skill (for example via `/plan-build-judge` or `/plan-build-judge-zh`).  
然后在 Cursor 里手动调用（例如 `/plan-build-judge` 或 `/plan-build-judge-zh`）。

This skill sets `disable-model-invocation: true`, so the model will not auto-select it. That is intentional for a heavyweight workflow.  
本 Skill 设置了 `disable-model-invocation: true`，模型不会自动选用。这对重流程 Skill 是有意为之。

### Manual install / 手动安装

```bash
git clone https://github.com/joker01-01/cursor-plan-build-judge.git
```

Then copy one skill folder into your workspace or personal Cursor skills directory.  
然后把其中一个 skill 文件夹复制到工作区或个人 Cursor skills 目录。

## Example walkthrough / 示例走读

Task (intentionally vague) / 任务（故意模糊）：

> Make this API more secure.  
> 把这个 API 变得更安全。

### 1) Planner (stops here by default) / Planner（默认先停在这里）

Example spec shape / 规格示例：

- **Objective / 目标**: Reduce common abuse and credential-exposure risks on the existing HTTP API without a full security rewrite  
  在不做全面安全重写的前提下，降低现有 HTTP API 的常见滥用与凭据暴露风险
- **Inputs / 输入**: Current API routes/handlers, auth middleware (if any), config/env usage  
  当前 API 路由/处理逻辑、鉴权中间件（如有）、配置/环境变量用法
- **Outputs / 输出**: Minimal code/config changes plus a short note of what was and was not hardened  
  最小代码/配置改动，并简要说明加固了什么、没做什么
- **Constraints / 约束**: No new major dependencies unless required; do not redesign the API surface; keep existing happy-path behavior  
  除非必要不引入大型新依赖；不重做 API 表面；保持现有主路径行为
- **Assumptions / 假设** (defaults chosen because the request was vague / 因需求模糊而主动给定的默认):
  - Focus on authn/authz gaps, secrets in code/config, and basic rate limiting on sensitive endpoints  
    聚焦鉴权缺口、代码/配置中的秘密信息、敏感接口的基础限流
  - Out of scope: WAF, infra hardening, pentest, full OWASP program  
    不做 WAF、基建加固、渗透测试或完整 OWASP 专项
- **Edge cases / 边界情况**: Missing auth middleware; local-only dev routes; endpoints that must stay public  
  缺少鉴权中间件；仅本地开发路由；必须保持公开的接口
- **Acceptance criteria / 验收标准**:
  1. Sensitive endpoints require authentication unless explicitly marked public / 敏感接口默认需要认证，除非明确标记为公开
  2. No secrets hardcoded in source / 源码中无硬编码秘密
  3. Login/auth-sensitive route has rate limiting with a documented limit / 登录/鉴权相关路由有限流，并写明限额
  4. Unauthenticated access to protected routes fails with the existing error style / 未认证访问受保护路由时，错误风格与现有一致
- **Prompt for Builder / 给 Builder 的执行提示**: Implement only the items above; do not refactor unrelated code.  
  只实现以上条目，不要重构无关代码。

User go-ahead examples / 用户放行示例: `LGTM`, `继续`, `按这个做`.

### 2) Builder / 执行

Implements only the approved security scope. Does not "also clean up" unrelated files.  
只实现已确认的安全范围，不「顺便」清理无关文件。

### 3) Judge / 验收

Reviews with evidence, for example / 基于证据审查，例如：

- diff shows auth checks and rate-limit wiring on the agreed routes / diff 显示约定路由上的鉴权与限流改动
- secret scan / file inspection shows no hardcoded credentials / 文件检查确认无硬编码凭据
- a request/repro note or test output shows protected routes reject anonymous access / 请求复现说明或测试输出显示受保护路由会拒绝匿名访问

Possible Judge result / 可能的 Judge 结果：

- **Verdict / 结论**: Fail / 不通过
- **Issue / 问题**: Rate limiting was added globally instead of only on sensitive routes / 限流被加到了全局，而不是只加在敏感路由
- **Severity / 严重程度**: High / 高
- **Rework needed / 是否需要返工**: Yes / 是

The workflow stops there until the user asks for changes.  
然后停住，等用户决定是否修改。

## Relationship to Cursor User Rules / 与 Cursor User Rule 的关系

You can keep a short personal rule that reminds the agent to use Planner → Builder → Judge on complex tasks.  
你可以保留一条简短的个人 Rule，提醒模型在复杂任务时走「规划 → 执行 → 验收」。

Use / 建议分工：

- a **short user rule** for default reminders / **短 Rule**：默认提醒
- this **skill** as the full stage contract when you explicitly invoke it / **本 Skill**：显式调用时的完整阶段约定

## Files / 文件

- `.cursor/skills/plan-build-judge/SKILL.md`
- `.cursor/skills/plan-build-judge-zh/SKILL.md`
- `README.md`
- `LICENSE`

## License / 许可

MIT
