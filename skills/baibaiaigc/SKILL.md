---
name: baibaiAIGC
description: 对中文或英文技术、学术文本进行降 AIGC 改写。中文模式严格按两轮顺序使用 prompts/baibaiaigc1.md、prompts/baibaiaigc2.md；英文模式只执行一轮，使用 prompts/baibaiaigc-en.md。每次调用只执行一轮改写，并依据记录衔接后续轮次。
user-invocable: true
---

# baibaiAIGC

这是本仓库中用于分发的标准 skill 入口。安装或引用本 skill 时，应指向当前目录，而不是仓库根目录。

本 skill 面向中文或英文论文、摘要、课程作业和技术文档的降 AIGC 改写。目标是降低模板化、机械化和常见 AI 写作痕迹，让表达更自然，同时保持原意、事实、术语和结构稳定。

## 适用范围

当用户有以下需求时，应触发本 skill：

- 降 AIGC
- 论文去 AI 味
- 人性化改写论文或技术文档
- 按多个提示词顺序改写同一篇文本
- 多轮降低论文 AI 痕迹

## 轮次规则

- 中文模式固定执行两轮，但每次调用本 skill 只执行其中一轮。
- 中文模式顺序固定为：`prompts/baibaiaigc1.md` -> `prompts/baibaiaigc2.md`。
- 英文模式只执行一轮，固定使用 `prompts/baibaiaigc-en.md`。
- 上一轮输出必须作为下一轮输入，不能跳轮、逆序，也不能把多轮规则合并到一次调用里。
- 本 skill 当前不使用第 3 轮。

## 对话 skill 模式

对话触发时，默认且必须优先走对话 skill 模式，而不是脚本 API 模式。

- 先读取降 AIGC 记录，判断当前文档应该进入哪一轮。
- 若当前文档没有记录，中文默认进入第 1 轮，英文默认执行唯一一轮。
- 读取对应 prompt 后，对输入文本按原段落优先切分；单段超过 850 字时，再按完整句子的自然断句继续切分。
- 每个处理块默认最多 850 字，逐块改写后必须按原段落结构还原。
- 本轮结束后，写出中间结果和 manifest，并基于 `references/checklist.md` 做本轮评分。
- 如果用户还要继续下一轮，必须提醒用户新开一个对话窗口再次触发本 skill。

当仓库中存在 `scripts/skill_round_helper.py` 和 `scripts/aigc_round_service.py` 时，优先复用它们来完成轮次判定、输入准备、分块处理、输出落盘和记录更新。

## 脚本 API 模式

脚本 API 模式只在用户明确要求命令行、批处理或脚本自动调用模型时才进入。它不是本 skill 的默认入口。

- 当用户明确要求运行 `scripts/run_aigc_round.py` 时，允许进入脚本 API 模式讨论。
- 脚本 API 模式需要模型配置，例如 `api_key`、`model` 和 `base_url`。
- 如果脚本模式缺少 API 配置，正确的处理是报错或显式使用 `--dry-run` 做切块与 prompt 校验。
- 不得把“脚本模式缺少 API 配置”解释成“对话 skill 模式也无法使用”。

## 记录与文件约定

- 记录文件默认位于工作区 `finish/aigc_records.json`。
- 中间结果默认位于 `finish/intermediate/`。
- 第 1 轮输出示例：`finish/intermediate/原文件名_round1.txt`
- 第 2 轮输出示例：`finish/intermediate/原文件名_round2.txt`
- manifest 示例：`finish/intermediate/原文件名_round1_manifest.json`

记录至少应保留：

- 文档标识
- 已执行轮次
- 每轮对应的 prompt 路径
- 每轮输入与输出路径
- manifest 路径

## 约束

- 不得新增事实、数据、案例、文献、引文或实验结论。
- 必须保留原文的专业术语、逻辑关系、编号结构、段落结构和关键结论。
- 单轮内部也不允许将整篇论文一次性整体改写，必须先分块再处理。
- 除非用户明确要求脚本模式，否则不要向用户索取 API key、模型名或 base URL。
- 只输出改写正文，不输出说明性或对话式包装语。

更具体的使用约束见 [references/usage.md](references/usage.md)，评分规则见 [references/checklist.md](references/checklist.md)。
