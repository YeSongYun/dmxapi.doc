# DMXAPI 快速开始

## 基本概念

1. **令牌 (Token)**
   - 也称为密钥、key、token
   - 用于身份验证，关联用户会员信息
   - 示例：`sk-sq3LViN553MWvkatNyygDWBIkLnQNFWN58lIPxGI3xebiSBc`（示例 key，已失效）

::: warning
请妥妥保管你的 API 密钥，不要泄露给他人。
:::

2. **Base URL**
   - 中转网址，用于替换官方 API 地址
   - 将以下官方地址替换为 DMXAPI 地址：

| 官方地址 | DMXAPI 地址 |
| --- | --- |
| `https://api.openai.com/v1` | `https://www.dmxapi.cn/v1` |

3. **模型 (Model)**
   - 指的是不同的 AI 模型，如 GPT-5.1、claude-sonnet-4-5-20250929、gemini-3-pro-preview
   - 每个模型有不同的功能和性能
   - 示例：`gpt-5.1`、`claude-sonnet-4-5-20250929`、`gemini-3-pro-preview`

4. **Tokens**
   - Tokens 是 AI 模型处理文本的基本单位，并非字符或单词的直接映射。
   - 中文分词：一个汉字通常编码为 1–2 个 tokens；例如 `你好` ≈ 2–4 tokens
   - 英文分词：常见单词通常为 1 个 token；较长或不常见的单词会被拆分；例如 `hello` = 1 token、`indescribable` ≈ 4 tokens
   - 特殊字符：空格、标点符号等也会占用 tokens；换行符通常计为 1 个 token

::: info
不同模型的分词方式略有差异，上述示例仅供参考。
:::

## 常见问题

<details>
<summary>我注册了，key 在哪？</summary>
注册登录 `www.DMXAPI.cn`，点击顶部「工作台」→「令牌」即可查看。
</details>

<details>
<summary>如何新建令牌 key？</summary>
注册登录，进入「工作台」→「令牌页面」→ 点击「添加令牌」按钮。

<img src="/img/create-key.png" alt="新建令牌" width="560">
</details>

<details>
<summary>如何获取 OpenAI / Claude / Gemini 的 Key？</summary>
Key 就是令牌。注册登录 DMXAPI 后，在左侧「令牌」菜单中点击「添加令牌」，填写一个自定义令牌名称即可。该 key 可用于 GPT 系列、Claude 系列、Gemini 系列模型。
</details>

<details>
<summary>key 为什么不能用？调用 API 没反应？</summary>
多数情况为 Base URL 设置不正确。请将 OpenAI 的 Base URL 改为 `https://www.dmxapi.cn/v1`。
</details>

<details>
<summary>能用 .env 存放 apikey 吗？</summary>
当然可以，请注意同时修改 Base URL。
例如：
```bash
DMXAPI_BASE_URL=https://www.dmxapi.cn/v1
DMXAPI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx
```
</details>

<details>
<summary>单个 key 的并发或 RPM、TPM 有限制吗？</summary>
没有主动限制。DMXAPI 不会限制用户的 RPM/TPM，但模型账号为所有用户共享，使用高峰期可能会出现 `429` 或 `500`。如需高并发方案，可联系客服咨询。
</details>

---

<p align="center">
  <small>© 2025 DMXAPI 快速开始</small>
</p>
