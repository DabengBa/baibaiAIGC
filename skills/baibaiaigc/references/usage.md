# 使用说明

## 适用范围

本目录是 `baibaiAIGC` 的标准 skill 分发入口，适用于：

- 中文论文去 AI 味
- 多轮降低 AIGC 痕迹
- 对长文档进行分段改写并保留原有结构
- 英文技术或学术文本的单轮自然化改写

本目录只定义 skill 的分发与使用边界，不负责介绍 web、app 或产品安装流程。

## 轮次规则

- 中文模式固定为两轮顺序执行：
  - `prompts/baibaiaigc1.md`
  - `prompts/baibaiaigc2.md`
- 英文模式只执行一轮：
  - `prompts/baibaiaigc-en.md`
- 每次调用 skill 只执行当前应执行的一轮。
- 上一轮输出必须作为下一轮输入。
- 当前项目不使用第 3 轮。

## 对话 skill 模式

当用户在聊天中直接提出“降 AIGC”“降 ai”“去 AI 味”“继续下一轮”等请求时，默认进入对话 skill 模式。

对话 skill 模式应遵循以下流程：

1. 读取 `finish/aigc_records.json`。
2. 判断当前文档应执行的轮次。
3. 读取本轮 prompt。
4. 读取输入文本或从 `.docx` 提取中间 `.txt`。
5. 按原段落优先、850 字上限进行分块。
6. 逐块改写并按原段落结构还原。
7. 写出本轮输出与 manifest。
8. 按 `references/checklist.md` 做本轮评分。
9. 更新记录并提醒用户如需下一轮需新开对话。

对话 skill 模式下：

- 不应要求用户额外提供 `BAIBAIAIGC_API_KEY`、`BAIBAIAIGC_MODEL`、`BAIBAIAIGC_BASE_URL`。
- 不应默认把用户切换到命令行或脚本方案。

## 脚本 API 模式

脚本 API 模式仅在用户明确要求使用命令行、脚本或批处理时进入。

- 入口脚本是仓库根目录下的 `scripts/run_aigc_round.py`。
- 该模式需要模型配置，例如 `api_key`、`model` 和 `base_url`。
- 如果缺少 API 配置，脚本默认不会自动改写；只有显式使用 `--dry-run` 时，才只执行切块与 prompt 校验。
- 脚本模式不可反向否定对话 skill 模式的可用性。

## 输入与输出约定

- 原始输入通常位于仓库根目录 `origin/`。
- 记录文件位于 `finish/aigc_records.json`。
- 中间输出位于 `finish/intermediate/`。
- `.docx` 输入可先提取为中间 `.txt`，再执行当前轮改写。
- 每轮输出应保留文档来源和轮次信息，例如：
  - `finish/intermediate/原文件名_round1.txt`
  - `finish/intermediate/原文件名_round2.txt`

## 约束与禁用行为

- 不新增数据、文献、案例、结论。
- 不破坏原文术语、编号和段落结构。
- 单轮内部必须分段处理，不能整篇一次性改写。
- 不得将两轮提示词合并为一次调用。
- 不得在默认回复中先给安装流程、前端说明、桌面应用说明或产品营销内容。
- 除非用户明确要求脚本方案，否则不要主动输出环境变量设置命令或 API 调用示例。
