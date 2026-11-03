# Gemini 3.8 Flash 文档实测报告

测试日期：**2026-11-03**。本次使用提供的测试密钥，对“Gemini 请求格式”下的真实 Python 代码进行远程 API 调用。报告和提交文件不包含密钥。

[打开交互式报告：结果筛选、实际回答、耗时与素材](/reports/gemini-3.8-flash-2026-11-03/index.html) · [下载脱敏 JSON 证据](/reports/gemini-3.8-flash-2026-11-03/results.json)

## 结果

| 范围 | 结果 |
| --- | --- |
| Gemini 3.8 Flash 生成与分析 | **23/24 通过** |
| 专用嵌入模型 | **0/7 通过**；当前密钥分组返回 503 / model_not_found |
| Python 语法 | **31 个代码块通过** |
| 生成类示例耗时中位数 | 13.248 秒，含代码执行与远程素材下载 |
| 文档构建 | PASS |

13 篇生成与分析文档统一使用 `gemini-3.8-flash`。向量化文档继续使用 `gemini-embedding-2-preview`，因为 `embedContent` / `batchEmbedContents` 返回数值向量，不能直接替换为生成模型。

## 实际观察与修正

- **搜索 + JSON**：原单次组合请求返回 JSON，但 SDK / REST 都没有返回搜索来源。改为先搜索并确认来源、再整理 JSON；报告记录原失败尝试和最终复测结果。
- **音频**：3 秒 440 Hz 纯音收到 HTTP 200，却被回答为“没有提供音频”，判定失败。最终使用已知内容的合成语音，校验订单号 **427** 和金额 **180**，不把 HTTP 200 当成内容正确。
- **超时**：测试期间 SDK 基础调用、思考等级、图片、多轮和思考总结等出现过超时。报告保留这些历史失败；最终状态取最近一次实际执行结果，不能据此保证长期稳定性。
- **流式思考总结未通过**：首轮曾返回 `thought=True` 摘要，后续一次只返回最终答案、一次读取超时。最终状态为失败，报告保留成功及失败证据；非流式思考总结已通过本次实测。
- **嵌入服务阻塞**：7 个示例均返回 `503 model_not_found`，错误提示 `default` 分组没有 `gemini-embedding-2-preview` 可用渠道。需开通该模型通道后再次验证。
- **输出校验修正**：网络图片和网络视频的装饰边框曾导致校验器误报。对同一次真实调用的完整输出去除行首边框后重新比对，不重新发送请求；修正记录保存在 JSON 的 `output_recheck` 与历史中。
- **输出处理**：修正 SSE 对冒号后空格的假设，并合并视频回复中所有非思考文本，避免签名部分导致答案丢失。

## 测试素材与校验

使用自行生成的素材：红圆 / 蓝方 / 绿三角图片、同画面的 3 秒 MP4、含 Q1=120 / Q2=180 的 PDF，以及已知订单号与金额的语音。网络图片与视频使用更新后示例中的公开地址，分别校验管风琴与 DMXAPI 内容。交互报告提供素材预览、每项断言、响应来源、正文和脱敏输出。

测试直接提取 Markdown 的 Python 代码块，只替换测试密钥和本地媒体路径；保留提示词、模型和请求参数。每条结果记录代码 SHA-256，复测器会使代码、校验器或素材已变更的旧通过结果失效。

环境：Python `3.14.5`；requests `2.34.2`；google-genai `2.19.0`；pydantic `2.13.4`。

## 逐项结果

| 示例 | 文档 | 最终结果 | 耗时 / 秒 |
| --- | --- | --- | --- |
| 文本 · 非流式 | [gemini-chat](/gemini-chat) · 代码块 1 | 通过 | 7.446 |
| 文本 · SSE 流式 | [gemini-chat-stream](/gemini-chat-stream) · 代码块 1 | 通过 | 35.843 |
| PDF 分析 | [gemini-pdf](/gemini-pdf) · 代码块 1 | 通过 | 7.213 |
| 本地视频 | [gemini-video](/gemini-video) · 代码块 1 | 通过 | 8.488 |
| 网络视频 | [gemini-video1](/gemini-video1) · 代码块 1 | 通过 | 21.625 |
| 音频分析 | [gemini-stt](/gemini-stt) · 代码块 1 | 通过 | 6.836 |
| 本地图片 / REST 流式 | [gemini-image](/gemini-image) · 代码块 1 | 通过 | 10.786 |
| 本地图片 / SDK | [gemini-image](/gemini-image) · 代码块 2 | 通过 | 19.688 |
| 网络图片 / REST | [gemini-image1](/gemini-image1) · 代码块 1 | 通过 | 35.893 |
| 网络图片 / SDK | [gemini-image1](/gemini-image1) · 代码块 2 | 通过 | 37.378 |
| JSON 结构化输出 | [gemini-json](/gemini-json) · 代码块 1 | 通过 | 12.708 |
| 多轮对话 / REST | [duolunduihua](/duolunduihua) · 代码块 1 | 通过 | 5.101 |
| 多轮对话 / SDK | [duolunduihua](/duolunduihua) · 代码块 2 | 通过 | 13.788 |
| 联网搜索 | [gemini-internet](/gemini-internet) · 代码块 1 | 通过 | 8.985 |
| 开发者指南 / SDK 基础 | [gemini-3](/gemini-3) · 代码块 1 | 通过 | 4.795 |
| 开发者指南 / REST 基础 | [gemini-3](/gemini-3) · 代码块 2 | 通过 | 27.857 |
| 开发者指南 / SDK 思考等级 | [gemini-3](/gemini-3) · 代码块 3 | 通过 | 2.711 |
| 开发者指南 / REST 思考等级 | [gemini-3](/gemini-3) · 代码块 4 | 通过 | 92.668 |
| 开发者指南 / SDK 图片分辨率 | [gemini-3](/gemini-3) · 代码块 5 | 通过 | 4.757 |
| 开发者指南 / REST 图片分辨率 | [gemini-3](/gemini-3) · 代码块 6 | 通过 | 11.298 |
| 开发者指南 / SDK 搜索 → JSON | [gemini-3](/gemini-3) · 代码块 7 | 通过 | 18.064 |
| 开发者指南 / REST 搜索 → JSON | [gemini-3](/gemini-3) · 代码块 8 | 通过 | 27.816 |
| 思考总结 / 非流式 | [gemini3-thinking-summary](/gemini3-thinking-summary) · 代码块 1 | 通过 | 15.213 |
| 思考总结 / 流式 | [gemini3-thinking-summary](/gemini3-thinking-summary) · 代码块 2 | FAIL | 120.346 |
| 多模态向量 / 文本 | [gemini-embedding-2-preview](/gemini-embedding-2-preview) · 代码块 1 | 阻塞：503 无可用渠道 | 0.207 |
| 多模态向量 / 图片 | [gemini-embedding-2-preview](/gemini-embedding-2-preview) · 代码块 2 | 阻塞：503 无可用渠道 | 0.255 |
| 多模态向量 / 音频 | [gemini-embedding-2-preview](/gemini-embedding-2-preview) · 代码块 3 | 阻塞：503 无可用渠道 | 0.226 |
| 多模态向量 / 视频 | [gemini-embedding-2-preview](/gemini-embedding-2-preview) · 代码块 4 | 阻塞：503 无可用渠道 | 0.203 |
| 多模态向量 / PDF | [gemini-embedding-2-preview](/gemini-embedding-2-preview) · 代码块 5 | 阻塞：503 无可用渠道 | 0.226 |
| 多模态向量 / 多模态组合 | [gemini-embedding-2-preview](/gemini-embedding-2-preview) · 代码块 6 | 阻塞：503 无可用渠道 | 0.234 |
| 多模态向量 / 批量 | [gemini-embedding-2-preview](/gemini-embedding-2-preview) · 代码块 7 | 阻塞：503 无可用渠道 | 0.247 |

## 本地复测

安装 `requests google-genai pydantic pillow`，并确保 `ffmpeg` 在 PATH 中。Windows 使用系统语音合成制作已知内容的语音；其他系统默认使用纯音素材，应另行验证非语音识别结果。

```powershell
pip install -U requests google-genai pydantic pillow
python scripts/verify-gemini-docs.py --prepare
$env:DMXAPI_API_KEY = "填写你自己的密钥"
python scripts/verify-gemini-docs.py
```

只复测部分示例可添加 `--only gemini-stt-1 gemini-3-7`。所有检查通过才返回退出码 0；当前嵌入通道阻塞时，完整测试返回 1。历史结果保存在 `test/gemini-3.8-flash/results.json`，该目录不提交。

生成报告：`python scripts/render-gemini-report.py --date 2026-11-03`。本报告是当前密钥、当前通道的一次功能测试，不是性能基准或稳定性保证。
