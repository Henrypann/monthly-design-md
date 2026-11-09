# monthly-design-md

**3-Theme Design System v1.1** — 一套面向 Vibe Coding / AI Agent 开发的、可按月策展的跨项目视觉规范。

> **固定骨架，动态色彩。** Dark / Obsidian 和 Light / Porcelain 的底色、表面、文字、排版及组件长期稳定；两套经典主题的强调色、辅助色、装饰色每月更新；Trend / Atelier 每月推出全新的视觉主题。三套主题始终共享同一交互结构与状态语义。

## 从这里开始

- [设计系统契约](DESIGN_SYSTEM.md)：不随月份改变的规范、主题边界和验收标准
- [Core tokens](themes/core.json)：排版、布局、经典深浅色基础和语义状态
- [Dark / Obsidian](themes/dark.json)：本月深色主题点缀
- [Light / Porcelain](themes/light.json)：本月浅色主题点缀
- [Trend / Atelier](themes/trend.json)：本月完整潮流主题
- [2026-11 快照](archives/2026-11.json)：初始化月度主题归档
- [月度策展 Agent Prompt](prompts/monthly-curator.md)：可交给 Codex、Claude Code 或其他 Agent 执行
- [月度报告模板](templates/monthly-report.md)：每月输出的标准格式

## 快速使用

1. 读取 themes/core.json，并根据主题读取 themes/dark.json、themes/light.json 或 themes/trend.json。
2. 经典主题按「Core foundations[mode] + Core status[mode] + 当月 tokens」合并；Trend 按「Trend tokens + Core status[mode]」合并。
3. 业务 UI 只能引用语义 Token，不能为单个组件随机发明色彩。
4. 每月 1 日策展后先提 PR：仅修改经典主题的 monthly tokens、Trend 全量主题及新增归档，过验收后再合并。

运行纯标准库校验：

~~~bash
python3 scripts/validate_themes.py
~~~

当前 2026-11 配色仅是可工作的**原创起始示例**，不冒充 Pantone 官方趋势结论。每月正式策展必须提供可追溯的趋势来源、日期以及自行选择配色的说明。

## 适用边界

这是视觉规范仓库，不是某个前端框架的组件库。React Native / Expo、Flutter、Web 均可映射相同的语义 Token；不要把 Web 专属 CSS 或动效当作跨端实现标准。

