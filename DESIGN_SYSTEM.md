# 3-Theme Design System · v1.1

## 1. 不可协商的三轨范式

| 轨道 | 常驻身份 | 不变 | 每月可变 |
| --- | --- | --- | --- |
| **Dark / Obsidian** | Linear 式精密暗色 | 深色背景、表面、文字、边框、基础字体、布局、组件行为 | accent、onAccent、accentSoft、secondary、decorative |
| **Light / Porcelain** | Apple 式柔和浅色 | 浅色背景、表面、文字、边框、基础字体、布局、组件行为 | accent、onAccent、accentSoft、secondary、decorative |
| **Trend / Atelier** | 当月时尚策展 | 组件语义、信息架构、交互、排版层级、状态含义 | 背景、表面、文字、边框、主辅色、材质、视觉气氛 |

**解释**：Classic 是固定骨架 + 月度点缀，不允许因潮流把 Dark 改成浅色或把 Light 改成高饱和全屏色。Trend 可以改变整体观感，但不允许改按钮的功能、导航逻辑、风险语义或组件 API。

## 2. 三层 Token

1. **Core**（themes/core.json）：共用 spacing/radius/typography、经典主题不可变的 foundations、按深浅模式对应的 success/warning/danger。所有新项目必须继承。
2. **Monthly Classic**（themes/dark.json / light.json）：各五个可变色彩 Token。经典主题必须只更新这些值及 edition 元数据。
3. **Monthly Trend**（themes/trend.json）：完整语义色 + 控制在可实现范围的材质定义。所有项目映射到同一语义接口。

统一消费接口（伪代码）：

~~~js
const resolved = theme.kind === "classic"
  ? { ...core.foundations[theme.mode], ...theme.tokens, ...core.status[theme.mode] }
  : { ...theme.tokens, ...core.status[theme.mode] };
~~~

颜色不直接写在业务组件里；组件只用 resolved.background / surface / text / accent 等语义字段。保留各平台原生可访问性、动态字号与减少动态效果设置。

## 3. 视觉使用规则

- 4pt 精度、8pt 优先节奏；卡片圆角默认 16px；层级靠留白、排版、适度边框，而不是大面积发光特效。
- 标题和信息结构稳定；经典主题不跟随每月潮流改变形状、导航或字体层级。
- 明暗模式各自的语义状态色由 Core 统一约束；风险/危险不能由纯装饰色替代，状态还应有文本、图标或其它辅助表达。
- 默认检查普通文本与背景对比度不低于 **4.5:1**，大型文字最低 3:1；本仓库对主要 Token 组合统一使用 4.5:1 的更严格检查。渐变和真实截图仍需人工检测。
- Trend 的纹理、毛玻璃、模糊等只能作为可选增强；不能成为交互必需条件，也不能明显增加性能或阅读负担。

## 4. 每月发布规程

1. **研究**：收集 Pantone Color of the Year、Pantone Fashion Color Trend Report、时装周和可信设计趋势来源，记录事件/发布日期与 URL。Pantone **没有被假定存在官方每月色板**。
2. **策展**：提出 3 套候选方向，每个有名称、视觉情绪、5–8 个主要色值与选色理由，明确原创调色与官方色号区别。
3. **定稿**：选一套贯穿三轨的灵感；更新 dark/light 的五个点缀 Token；为 trend 重新配色并记录来源。
4. **快照**：当月版本写入 archives/YYYY-MM.json，旧归档不可覆盖；保留整月回溯能力。
5. **验证**：运行 python3 scripts/validate_themes.py，输出统一页面/组件的深色、浅色、潮流三主题截图。检查文字、焦点、数据图表、风险状态、暗色/浅色可读性。
6. **发布**：PR 记录本月与上月变化、设计灵感来源、三轨截图及验收结论；人工审核后合并，应用侧自行选择何时更新。

## 5. AI 工程交付边界

- Agent 先读取本文件、Core 和当前三份主题 JSON，再开始修改 UI。
- 禁止硬编码随机 HEX；禁止因主题切换增加重复组件；禁止自创第四套正式主题。
- 不能把 shadcn/ui、Magic UI、Motion 等 Web 技术假设为 iOS/Android 通用方案；先遵循目标项目的技术栈与组件层。
- 月度策展只交付规范和资产，不自动修改业务仓库、推送生产配置或发布应用。

## 6. 版本约定

- 系统结构/不可变契约改动 → 设计系统版本升级，单独 PR。
- 常规月度换色 → 仅更新 edition、经典 monthly tokens、Trend tokens/材质与 archives 快照，不重新定义 Core。
- 2026-11 为原创演示初版；之后的官方趋势引用必须在月度报告中逐条核实。

