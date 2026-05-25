---
type: project-source-of-truth
project: "{{project_name}}"
scenario: "{{scenario}}"
phase: "{{phase}}"
stable_artifact: "{{stable_artifact}}"
last_updated: "{{YYYY-MM-DD}}"
purpose: "{{project_name}} 项目的入口与唯一 Source of Truth — 任何 Agent 启动该项目工作前必读"
---

# {{project_name}} · AGENTS.md（Source of Truth）

> 任何 Agent 启动相关任务前 **必读本文件**。这是项目唯一事实源。
> **绝不**先动手起草 / 写文件 / 给建议 —— 先把本文件 + §7 指定的必读项读完。

---

## 1. 项目定位

<!-- Fill: product description, target model/platform, core constraint, current phase -->

- **产品**：{{product_description}}
- **生成模型**：{{target_model}}
- **运行环境**：{{runtime_environment}}
- **核心瓶颈**：{{core_constraint}}
- **当前阶段**：{{current_phase}}
- **当前最新产物 / 迭代基线**：{{stable_artifact}}

---

## 2. 三层架构

{{target_model}} 生成页面时，接收三层独立的上下文。**每层各管一摊，边界即红线**：

| 层 | 谁维护 | 管什么 | 位置 |
|---|---|---|---|
| **System Prompt** | 产品方 | 数据契约 + 工程执行：数据结构声明、SDK 导入规则、sandbox 禁令 | `{{system_prompt_path}}` |
| **Design Prompt** | 本项目核心产物 | 视觉风格 + 页面布局：颜色 / 字体 / 间距 / 材质 / 动效 / Section archetype / 构图 / 组件清单 | `{{design_prompt_folder}}` |
| **running-env** | 运行时基建 | `:root` OKLCH token 声明、data hook 实现、mock 数据 fallback | `{{running_env_path}}` |

**为什么必须分清**：弱模型三层若声明冲突，会随机挑一个执行 → attention drift → 生成质量崩。**三层职责不可交叉**就是 §5 的三条红线。

---

## 3. Design Prompt（当前版本）

### 内部结构（行数 + frontmatter + §1–§N）

<!-- Fill structure table matching actual sections -->

| 节 | 内容 |
|---|---|
| frontmatter | `style_name` / `scenario` / `description` |
| §1 Brand & Style | Mood + Proposition |
| §2 Colors | OKLCH token block + color rules |
| §3 Typography | 字体栈 + weight + 字号表 |
| §4 Spacing & Layout | 基准 + container + density |
| §5 Material | 表面 + 圆角 + panel discipline |
| §6 Motion | EASE + 动效表 + AnimateNumber + reduced-motion |
| §7 Iconography | lucide-react stroke |
| §8 Accessibility & Mobile | WCAG 2.2 AA + 断点 |
| §9 Do's and Don'ts | 视觉 + 动效负例 |
| §10 Pattern Overview | Scenario Mindset + Scope + Atmosphere |
| §11 Section Archetype Library | Archetype + Treatment + Dominant Move |
| §12 Composition | Rhythm + Rules |
| §13 Section Anatomy | Hero + Non-Hero slot mapping |
| §14+ | {{additional_sections}} |

---

## 4. 文件组织

```
{{project_root}}/
├── AGENTS.md                          ← 本文件（唯一 SoT）
├── Round-Log.md                       ← 迭代流水账
├── scenarios/
│   └── {{scenario}}/
│       ├── prompt-template.md         ← 注入模板（不动）
│       ├── PATTERN.md                 ← PATTERN 层（可插拔，无色值）
│       ├── component-spec.md          ← 组件清单
│       └── slot-examples/
│           └── {{style}.slot.json     ← 风格 Slot
└── scripts/                           ← inject.py 等工具脚本
```

---

## 5. 三条红线（Layer Separation）

**红线 #1 · 工程层分离**
Design Prompt 禁止声明任何 System Prompt 已定义的事项 — 数据类型（String/Number）、hook DSL 结构、Aggregation enum 名称、sandbox 禁令、npm install 限制。System Prompt 管工程，Design Prompt 管视觉。

**红线 #2 · 禁角色定义**
Design Prompt 禁止出现"你是一个..."/"Act as..."/"你的任务是生成..."等角色定义句。Design Prompt 是纯声明式风格规范，不是 Instruction Prompt。

**红线 #3 · 禁数据格式声明**
Design Prompt 禁止声明 `row[fld].value` 类型、`useBaseData` 返回结构、`records[0].fields` 访问模式。这些属于 System Prompt 数据契约层。

<!-- Scenario-specific red lines for {{scenario}} — add below -->

**红线 #4 · {{scenario}} 特定红线**
{{scenario_specific_redlines}}

---

## 6. 流程纪律

### 每轮迭代

1. 读 Round-Log.md 最新状态 → 确认当前基线版本
2. 读 AGENTS.md §5 红线 → 不可违反
3. 执行任务（draft / patch / review）
4. verify 通过 → 更新 Round-Log.md
5. 更新 AGENTS.md `stable_artifact` + `last_updated`

### Cowork Agent 职责

- **Cowork（Opus）**：架构决策 / 红线把关 / 验收 / Round-Log 维护
- **Builder（Sonnet CLI）**：执行 patch / inject / render / 验证行数

### 任何 patch 落地前必 verify

- `python3 scripts/inject.py --slot <slot> --template <template> --out <out>`
- 检查输出行数 ≤ 620（Design Prompt），unrendered_tokens = 0
- `verify-three-way-sync.py` 二方 / 三方 ornament sync check

---

## 7. 必读项（Agent 启动时）

<!-- Fill all paths that must be read before any work begins -->

1. `{{system_prompt_path}}` — 数据契约 + 工程执行规则
2. `{{design_prompt_current}}` — 当前 Design Prompt 基线
3. `Round-Log.md` — 迭代历史 + 当前版本快照
4. `scenarios/{{scenario}}/PATTERN.md` — PATTERN 层
5. `{{additional_required_reads}}`

---

## 8. 已知约束 / 已解问题

<!-- Running list of constraints and their resolutions -->

| 约束 | 状态 | 解法 |
|------|------|------|
| {{constraint_1}} | {{resolved|open}} | {{resolution_or_workaround}} |
