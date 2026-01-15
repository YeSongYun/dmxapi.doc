# 关于 Base URL

## 🌐 DMXAPI 站点介绍

DMXAPI 提供三个不同的服务站点：

| 站点 | 域名 | 计价方式 | 折扣 | 说明 |
|------|------|----------|------|------|
| 🌍 **国际站** | `www.dmxapi.com` | 美金计价 | 主流模型 6.8 折 | 打折渠道 |
| 🇨🇳 **国内站** | `www.dmxapi.cn` | 人民币计价 | 主流模型 6.8 折 | 打折渠道 |
| 💎 **SSVIP站** | `ssvip.dmxapi.com` | 美金计价 | 原价无折扣 | 高级服务 |

## 🔑 令牌与域名配套关系

> ⚠️ **重要提醒**：令牌必须与对应的域名配套使用

| 站点类型 | 对应 Base URL |
|----------|---------------|
| COM 站令牌 | `https://www.dmxapi.com` |
| CN 站令牌 | `https://www.dmxapi.cn` |
| SSVIP 站令牌 | `https://ssvip.dmxapi.com` |


## 常用接口(OpenAI格式)

| 功能 | 接口地址 |
| --- | --- |
| 对话 | `https://www.dmxapi.cn/v1/chat/completions` |
| 对话（新） | `https://www.dmxapi.cn/v1/responses` |
| 嵌入（Embedding） | `https://www.dmxapi.cn/v1/embeddings` |
| 图片生成 | `https://www.dmxapi.cn/v1/images/generations` |
| 图片编辑 | `https://www.dmxapi.cn/v1/images/edits` |
| 语音转文字 STT | `https://www.dmxapi.cn/v1/audio/transcriptions` |
| 文字转语音 TTS | `https://www.dmxapi.cn/v1/audio/speech` |

## 常用接口(Gemini格式)

`https://www.dmxapi.cn/v1beta/models/{model}:generateContent`

::: tip Gemini 原生格式说明
- 适用于需要使用 Google Gemini 原生 SDK 或原生 API 格式的场景
- 支持流式响应，在 URL 后使用 `:streamGenerateContent` 替代 `:generateContent`
:::

## 常用接口(Claude格式)

`https://www.dmxapi.cn/v1/messages`

::: tip Claude 原生格式说明
- 适用于需要使用 Anthropic Claude 原生 SDK 或原生 API 格式的场景
- 请求头需设置 `x-api-key` 为你的 DMXAPI 密钥
- 支持 Claude 全系列模型，如 `claude-sonnet-4-20250514`、`claude-opus-4-20250514` 等
:::

## 🔗 完整 Base URL 示例

将域名与接口路径组合，得到完整的 API 地址：

```text
https://www.dmxapi.com/v1/chat/completions
https://www.dmxapi.cn/v1/embeddings
https://ssvip.dmxapi.com/v1/images/generations
```

## ⚙️ 第三方应用配置

在各类第三方应用中，通常使用以下 Base URL：

```text
https://www.dmxapi.com/v1
https://www.dmxapi.cn/v1
https://ssvip.dmxapi.com/v1
```

> 💡 **配置提示**：在 Claude Code 等部分应用中，仅需配置域名即可，无需添加 `/v1` 路径。

---

### 📝 配置小贴士

Base URL 配置通常有三种格式，可以根据应用要求选择：

1. **完整路径**：`https://域名/v1/具体接口`
2. **带 v1**：`https://域名/v1`
3. **仅域名**：`https://域名`

💡 **建议**：如果不确定格式，可以按上述顺序逐一尝试。

---

<p align="center">
  <small>© 2025 DMXAPI Base url</small>
</p>
