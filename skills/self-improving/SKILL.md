---
name: Self-Improving + Proactive Agent
slug: self-improving
version: 1.3.0
homepage: https://clawic.com/skills/self-improving
description: "Self-reflection + Self-criticism + Self-learning + Self-organizing memory + Evolutionary self-improvement. Evaluates work, catches mistakes, analyzes execution traces, auto-evolves skills/prompts, and compounds quality permanently."
changelog: "Evolutionary upgrade: execution trace analysis, GEPA-style skill/prompt evolution, guardrails pipeline, evolution-log tracking, auto-detection of skill blind spots. Inspired by Hermes Agent self-evolution v0.14."
metadata: {"clawdbot":{"emoji":"🧠","requires":{"bins":[]},"os":["linux","darwin","win32"],"configPaths":["~/self-improving/"],"configPaths.optional":["./AGENTS.md","./SOUL.md","./HEARTBEAT.md"]}}
---

## When to Use

User corrects you or points out mistakes. You complete significant work and want to evaluate the outcome. You notice something in your own output that could be better. Knowledge should compound over time without manual maintenance.

## Architecture

Memory lives in `~/self-improving/` with tiered structure. If `~/self-improving/` does not exist, run `setup.md`.
Workspace setup should add the standard self-improving steering to the workspace AGENTS, SOUL, and `HEARTBEAT.md` files, with recurring maintenance routed through `heartbeat-rules.md`.

```
~/self-improving/
├── memory.md          # HOT: ≤100 lines, always loaded
├── index.md           # Topic index with line counts
├── heartbeat-state.md # Heartbeat state: last run, reviewed change, action notes
├── projects/          # Per-project learnings
├── domains/           # Domain-specific (code, writing, comms)
├── archive/           # COLD: decayed patterns
└── corrections.md     # Last 50 corrections log
```

## Quick Reference

| Topic | File |
|-------|------|
| Setup guide | `setup.md` |
| Heartbeat state template | `heartbeat-state.md` |
| Memory template | `memory-template.md` |
| Workspace heartbeat snippet | `HEARTBEAT.md` |
| Heartbeat rules | `heartbeat-rules.md` |
| Learning mechanics | `learning.md` |
| Security boundaries | `boundaries.md` |
| Scaling rules | `scaling.md` |
| Memory operations | `operations.md` |
| Self-reflection log | `reflections.md` |
| OpenClaw HEARTBEAT seed | `openclaw-heartbeat.md` |

## Requirements

- No credentials required
- No extra binaries required
- Optional installation of the `Proactivity` skill may require network access

## Learning Signals

Log automatically when you notice these patterns:

**Corrections** → add to `corrections.md`, evaluate for `memory.md`:
- "No, that's not right..."
- "Actually, it should be..."
- "You're wrong about..."
- "I prefer X, not Y"
- "Remember that I always..."
- "I told you before..."
- "Stop doing X"
- "Why do you keep..."

**Preference signals** → add to `memory.md` if explicit:
- "I like when you..."
- "Always do X for me"
- "Never do Y"
- "My style is..."
- "For [project], use..."

**Pattern candidates** → track, promote after 3x:
- Same instruction repeated 3+ times
- Workflow that works well repeatedly
- User praises specific approach

**Ignore** (don't log):
- One-time instructions ("do X now")
- Context-specific ("in this file...")
- Hypotheticals ("what if...")

## Self-Reflection

After completing significant work, pause and evaluate:

1. **Did it meet expectations?** — Compare outcome vs intent
2. **What could be better?** — Identify improvements for next time
3. **Is this a pattern?** — If yes, log to `corrections.md`

**When to self-reflect:**
- After completing a multi-step task
- After receiving feedback (positive or negative)
- After fixing a bug or mistake
- When you notice your output could be better

**Log format:**
```
CONTEXT: [type of task]
REFLECTION: [what I noticed]
LESSON: [what to do differently]
```

**Example:**
```
CONTEXT: Building Flutter UI
REFLECTION: Spacing looked off, had to redo
LESSON: Check visual spacing before showing user
```

Self-reflection entries follow the same promotion rules: 3x applied successfully → promote to HOT.

## Quick Queries

| User says | Action |
|-----------|--------|
| "What do you know about X?" | Search all tiers for X |
| "What have you learned?" | Show last 10 from `corrections.md` |
| "Show my patterns" | List `memory.md` (HOT) |
| "Show [project] patterns" | Load `projects/{name}.md` |
| "What's in warm storage?" | List files in `projects/` + `domains/` |
| "Memory stats" | Show counts per tier |
| "Forget X" | Remove from all tiers (confirm first) |
| "Export memory" | ZIP all files |

## Memory Stats

On "memory stats" request, report:

```
📊 Self-Improving Memory

HOT (always loaded):
  memory.md: X entries

WARM (load on demand):
  projects/: X files
  domains/: X files

COLD (archived):
  archive/: X files

Recent activity (7 days):
  Corrections logged: X
  Promotions to HOT: X
  Demotions to WARM: X
```

## Common Traps

| Trap | Why It Fails | Better Move |
|------|--------------|-------------|
| Learning from silence | Creates false rules | Wait for explicit correction or repeated evidence |
| Promoting too fast | Pollutes HOT memory | Keep new lessons tentative until repeated |
| Reading every namespace | Wastes context | Load only HOT plus the smallest matching files |
| Compaction by deletion | Loses trust and history | Merge, summarize, or demote instead |

## Core Rules

### 0. Execution Trace Analysis (Evolutionary)

After every significant task, build a lightweight execution trace:

```yaml
trace:
  task: "简短任务描述"
  outcome: "成功|失败|部分成功"
  failure_reason: "失败根因分析"
  correction_signal: "用户纠正内容（如有）"
  quality_score: 0-10
```

**分析规则：**
- 相同错误模式出现 3 次 → 标记为**技能盲区**，触发进化流程
- 用户纠正频率加速 → 标记为**退化信号**，回滚到前一版本
- 成功率持续提升 → 标记为**有效进化**，固化到基线

存储位置：`~/self-improving/traces/`（按日期归档）

### 1. Learn from Corrections and Self-Reflection
- Log when user explicitly corrects you
- Log when you identify improvements in your own work
- Never infer from silence alone
- After 3 identical lessons → ask to confirm as rule

### 2. Tiered Storage
| Tier | Location | Size Limit | Behavior |
|------|----------|------------|----------|
| HOT | memory.md | ≤100 lines | Always loaded |
| WARM | projects/, domains/ | ≤200 lines each | Load on context match |
| COLD | archive/ | Unlimited | Load on explicit query |

### 3. Automatic Promotion/Demotion
- Pattern used 3x in 7 days → promote to HOT
- Pattern unused 30 days → demote to WARM
- Pattern unused 90 days → archive to COLD
- Never delete without asking

### 4. Namespace Isolation
- Project patterns stay in `projects/{name}.md`
- Global preferences in HOT tier (memory.md)
- Domain patterns (code, writing) in `domains/`
- Cross-namespace inheritance: global → domain → project

### 5. Conflict Resolution
When patterns contradict:
1. Most specific wins (project > domain > global)
2. Most recent wins (same level)
3. If ambiguous → ask user

### 6. Compaction
When file exceeds limit:
1. Merge similar corrections into single rule
2. Archive unused patterns
3. Summarize verbose entries
4. Never lose confirmed preferences

### 7. Transparency
- Every action from memory → cite source: "Using X (from projects/foo.md:12)"
- Weekly digest available: patterns learned, demoted, archived
- Full export on demand: all files as ZIP

### 8. Security Boundaries
See `boundaries.md` — never store credentials, health data, third-party info.

### 9. Evolutionary Self-Improvement (GEPA-style)

See `evolution-mechanics.md` for full engine.

**轻量进化流程：**
1. 识别改进目标（高频错误、用户纠正模式、执行效率瓶颈）
2. 生成 2-3 个变异体（AI 重写特定段落）
3. 对每个变体做质量评估（精确性/效率/完整性/一致性/安全性）
4. 选择最优变体，展示变更差异
5. **必须经用户确认后**再写入文件
6. 记录到 `~/self-improving/evolution-log.md`
7. 追踪后续效果 7 天

**触发条件：**
- 同一技能/流程 3 次以上失败
- 用户明确说 "改进这个"
- 手动触发 `/evolve <target>`

**永不进化的内容：**
- 用户明确的个人偏好
- 安全敏感配置
- SOUL.md 核心人格

### 10. Graceful Degradation
If context limit hit:
1. Load only memory.md (HOT)
2. Load relevant namespace on demand
3. Never fail silently — tell user what's not loaded

## Scope

This skill ONLY:
- Learns from user corrections and self-reflection
- Stores preferences in local files (`~/self-improving/`)
- Maintains heartbeat state in `~/self-improving/heartbeat-state.md` when the workspace integrates heartbeat
- Reads its own memory files on activation

This skill NEVER:
- Accesses calendar, email, or contacts
- Makes network requests
- Reads files outside `~/self-improving/`
- Infers preferences from silence or observation
- Deletes or blindly rewrites self-improving memory during heartbeat cleanup
- Modifies its own SKILL.md

## Data Storage

Local state lives in `~/self-improving/`:

- `memory.md` for HOT rules and confirmed preferences
- `corrections.md` for explicit corrections and reusable lessons
- `projects/` and `domains/` for scoped patterns
- `archive/` for decayed or inactive patterns
- `heartbeat-state.md` for recurring maintenance markers

## Related Skills
Install with `clawhub install <slug>` if user confirms:

- `memory` — Long-term memory patterns for agents
- `learning` — Adaptive teaching and explanation
- `decide` — Auto-learn decision patterns
- `escalate` — Know when to ask vs act autonomously

## Feedback

- If useful: `clawhub star self-improving`
- Stay updated: `clawhub sync`
