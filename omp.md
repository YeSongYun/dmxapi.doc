# omp 配置 DMXAPI 教程

omp（Oh My Pi）是一款开源的终端 AI 编程智能体（Coding Agent），类似 Claude Code 的开源替代品：内置 32 个工具、LSP 代码智能、DAP 调试器、子智能体、代码审查等能力，支持 40+ 模型供应商，Windows / macOS / Linux 原生运行。官网：[omp.sh](https://omp.sh)。

omp 支持通过 `models.yml` 配置文件接入任意 OpenAI / Anthropic 兼容的第三方 provider，因此可以直接接入 **DMXAPI**，一个密钥调用 GPT、Claude、GLM、DeepSeek、Qwen、Kimi 等数百个主流大模型。

本文档将带你完成 **安装 omp → 创建 models.yml → 填入 DMXAPI 配置 → 选择模型并使用** 的完整接入流程。

:::warning 注意
编程智能体 tokens 消耗量很大，请注意 tokens 消耗。
:::

## 一、安装 omp

按你的操作系统任选一种方式安装：

**macOS / Linux**

```bash
curl -fsSL https://omp.sh/install | sh
```

**macOS（Homebrew）**

```bash
brew install can1357/tap/omp
```

**Windows（PowerShell）**

```powershell
irm https://omp.sh/install.ps1 | iex
```

**Bun（已安装 Bun ≥ 1.3.14 的用户）**

```bash
bun install -g @oh-my-pi/pi-coding-agent
```

安装完成后，**重新打开终端**验证：

```bash
omp --version        # 能输出版本号即安装成功
omp config path      # 查看配置目录（models.yml 就放在这里）
```

:::tip Windows 终端按键提示
Windows Terminal 未实现 Kitty 键盘协议，在 omp 中输入多行文本请用 `Alt+Enter` 换行（代替 `Shift+Enter`）。
:::

## 二、创建 models.yml 配置文件

omp 通过用户目录下的 `models.yml` 文件管理自定义模型供应商：

| 系统 | 路径 |
|---|---|
| Windows | `C:\Users\你的用户名\.omp\agent\models.yml` |
| macOS / Linux | `~/.omp/agent/models.yml` |

**Windows：**

1. 打开文件资源管理器（任意一个文件夹窗口）
2. 在顶部路径地址栏中输入以下路径并回车：

   ```text
   C:\Users\你的电脑用户名\.omp\agent\
   ```

   ::: tip
   `.omp` 默认是隐藏文件夹，直接在地址栏输入路径是最快的进入方式；目录不存在就逐级新建。
   :::

3. 在该文件夹下新建一个文本文档，并重命名为 `models.yml`（**请确保去掉了 `.txt` 后缀**）

**macOS / Linux：**

```bash
mkdir -p ~/.omp/agent
touch ~/.omp/agent/models.yml
```

## 三、填入 DMXAPI 配置内容

用编辑器打开 `models.yml`，粘贴以下内容，把 `apiKey` 换成你自己的 DMXAPI 密钥（获取地址：`https://www.dmxapi.cn/token`），模型可按需增删：

```yaml
# ~/.omp/agent/models.yml
# 模型 id 大小写敏感；如需换密钥只改 apiKey 一行
#
# 本文件演示 omp 支持的三种接口格式（api 字段），各配一个模型：
#   openai-completions -> /v1/chat/completions   （glm-5.2）
#   openai-responses   -> /v1/responses          （gpt-5.6-sol）
#   anthropic-messages -> /v1/messages           （claude-opus-4-8）

providers:                                    # 所有自定义 provider 都放在这个顶级键下
  dmxapi:                                     # provider 的 id，可自定义；在 omp 里选模型时显示为 dmxapi/<模型>
    baseUrl: https://www.dmxapi.cn/v1         # 接入地址，只写到 /v1；omp 会自动追加 /chat/completions 等，切勿多写
    apiKey: sk-在此填入你的DMXAPI密钥          # DMXAPI 后台生成的密钥；也可填环境变量名
    authHeader: true                          # true=以 Authorization: Bearer <key> 方式发送鉴权头（DMXAPI 需要）
    disableStrictTools: true                  # true=关闭工具 strict 校验；走 Anthropic 接口的中转通常必须关，否则被拒
    models:                                   # 该 provider 下的模型列表，每个模型以 "- id:" 起头
      # ===== 格式一：chat/completions（走 /v1/chat/completions）=====
      # 最通用的 OpenAI 格式，国产模型基本都用它
      - id: glm-5.2                           # 模型 id，必须与 DMXAPI 后台完全一致（大小写敏感）
        name: GLM-5.2 (DMXAPI)                # 显示名，随意起，仅用于 /model 列表展示
        api: openai-completions               # 接口格式：openai-completions=OpenAI 的 /v1/chat/completions
        reasoning: true                       # true=推理/思考型模型，允许 omp 发送思考强度参数
        contextWindow: 1000000                # 上下文窗口上限（token）；决定 omp 何时压缩历史，填模型真实上限
        maxTokens: 128000                     # 单次回复的最大输出 token 数

      # ===== 格式二：responses（走 /v1/responses）=====
      # gpt-5.6 系带 tools + reasoning 时必须走这个端点，
      # 否则 chat/completions 会报 400（tools 与 reasoning_effort 不兼容）
      - id: gpt-5.6-sol                       # 模型 id，大小写敏感
        name: gpt-5.6-sol (DMXAPI)            # 显示名
        api: openai-responses                 # 接口格式：openai-responses=OpenAI 的 /v1/responses
        reasoning: true                       # true=推理模型（gpt-5.6 是推理模型，故走 responses）
        input: [text, image]                  # 支持的输入类型：[text]=纯文字，[text, image]=可收图片（多模态）
        contextWindow: 1000000                # 上下文窗口上限（token）
        maxTokens: 128000                     # 单次最大输出 token 数

      # ===== 格式三：messages（走 /v1/messages）=====
      # Anthropic 原生格式，Claude 系用它，omp 对其 thinking/缓存支持最好
      - id: claude-opus-4-8                   # 模型 id，大小写敏感
        name: Claude Opus 4.8 (DMXAPI)        # 显示名
        api: anthropic-messages               # 接口格式：anthropic-messages=Anthropic 的 /v1/messages
        reasoning: true                       # true=启用 Claude 的思考（thinking）能力
        input: [text, image]                  # 支持文字 + 图片输入（Claude 支持看图）
        contextWindow: 1000000                # 上下文窗口上限（token）
        maxTokens: 128000                     # 单次最大输出 token 数
```

保存文件（UTF-8 编码）。**改完必须重启 omp** 才会重新读取。

### 关键字段说明

**provider 级字段：**

| 字段 | 必填 | 说明 |
|---|---|---|
| `baseUrl` | ✅ | 接入地址，**只写到 `/v1`**。国内站 `https://www.dmxapi.cn/v1`，国际站 `https://www.dmxapi.com/v1`。⚠️ 不要写成 `.../v1/chat/completions`，omp 会自动追加，写多了路径会重复报 404 |
| `apiKey` | ✅ | DMXAPI 后台生成的 `sk-` 密钥 |
| `authHeader` | 建议 | `true` 时以 `Authorization: Bearer <key>` 发送鉴权头（DMXAPI 需要） |
| `disableStrictTools` | 建议 | `true`。中转平台走 Anthropic 接口时通常必须关掉 strict 校验，否则请求被拒 |

**model 级字段：**

| 字段 | 必填 | 说明 |
|---|---|---|
| `id` | ✅ | 模型 id，**大小写敏感**，必须与 DMXAPI 模型广场完全一致 |
| `name` | 建议 | 显示名，随意起，仅用于 `/model` 列表展示 |
| `api` | ✅ | 接口格式，见下方「接口格式怎么选」 |
| `reasoning` | 可选 | 推理/思考型模型写 `true` |
| `input` | 可选 | 支持的输入类型：纯文本 `[text]`，多模态 `[text, image]` |
| `contextWindow` | 可选 | 上下文窗口上限（token），可参考 [DMXAPI 模型价格页](https://www.dmxapi.cn/rmb) |
| `maxTokens` | 可选 | 单次回复的最大输出 token 数 |

### 接口格式怎么选

`api` 字段决定该模型走哪种「线路协议」。在 DMXAPI 上：

| 模型 | `api` 该写 | 实际请求路径 |
|---|---|---|
| Claude 系（claude-opus / sonnet / haiku…） | `anthropic-messages` | `/v1/messages` |
| gpt-5.6 系推理模型（带 tools + reasoning） | `openai-responses` | `/v1/responses` |
| 其它（GPT / GLM / DeepSeek / Qwen / Kimi…） | `openai-completions` | `/v1/chat/completions` |

不确定某模型走哪种，可用密钥拉一下模型列表，看它的 `supported_endpoint_types`：

```bash
curl https://www.dmxapi.cn/v1/models -H "Authorization: Bearer sk-你的密钥"
```

- 返回里含 `"anthropic"` → 写 `anthropic-messages`
- 只有 `"openai"` → 写 `openai-completions`

## 四、选择模型并开始使用

#### 1、启动 omp

在任意项目目录下打开终端，输入：

```bash
omp
```

#### 2、跳过首屏登录列表

首屏若出现内置 provider 的登录列表，直接按 `Esc` 跳过——DMXAPI 是自定义 provider，不走内置登录。

#### 3、选择模型

输入 `/model` 回车，在列表中选择 `dmxapi/…` 模型，即可开始对话使用。

也可在终端确认配置是否加载成功：

```bash
omp models find dmxapi    # 列出 dmxapi 下已加载的模型
```

:::tip 一次性提问（不进 TUI）
`omp -p "帮我列出 src 下的 .ts 文件"` 可单次执行一个提问后直接退出，适合脚本调用。
:::

### 设为默认模型（可选）

在 `~/.omp/agent/config.yml`（注意是 **config.yml**，不是 models.yml）里可以把角色指到具体模型：

```yaml
modelRoles:
  default: dmxapi/claude-opus-4-8    # 日常主力
  smol: dmxapi/glm-5.2               # 便宜的小任务（子智能体等）
```

## 常见问题

| 现象 | 原因 | 解决办法 |
|---|---|---|
| `404 Invalid URL (POST /v1/chat/completions/chat/completions)` | `baseUrl` 写成了 `.../v1/chat/completions`，omp 又追加了一次 | `baseUrl` 只写到 `/v1` |
| `/model` 里根本没有 dmxapi | `models.yml` YAML 解析失败，omp 静默回退到内置模型 | 检查 YAML 语法（见下方红线）；跑 `omp models` 看报错 |
| `404` / 模型不存在 | 模型 `id` 拼错或大小写不对 | 照抄 `/v1/models` 返回里的准确 id |
| `401` / 未授权 | 密钥错误或失效 | 检查 `apiKey` 是完整的 `sk-` 串，无多余空格 |
| Claude 模型报 strict 相关错误 | 没关 strict 校验 | provider 级加 `disableStrictTools: true` |
| 某模型报「上下文超限」 | `contextWindow` 填大了 | 把该模型的 `contextWindow` 调小 |

:::warning YAML 书写红线
以下任何一条违反都会导致**整个文件解析失败**、`/model` 里 dmxapi 消失：

1. 冒号后必须有空格：`maxTokens: 128000` ✅，`maxTokens:128000` ❌
2. 只能用半角符号，不能用中文标点（如中文逗号「，」）
3. 缩进用空格，不能用 Tab
4. 每个模型以 `- id:` 起头，一个模型一个条目
5. 文件保存为 UTF-8 编码，改完**重启 omp** 生效
:::

---

<p align="center">
  <small>© 2026 DMXAPI omp</small>
</p>
