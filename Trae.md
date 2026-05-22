# Trae 客户端配置方法

Trae 是一款 AI 驱动的编程工作台（IDE / 编码助手），内置 Builder 智能体、对话流、MCP 等功能，支持通过「自定义配置」接入任意 OpenAI 兼容或 Anthropic 兼容的 API 服务。

::: tip
编程类应用 tokens 消耗量较大，请留意 tokens 消耗。
:::

## 第一步 进入模型管理，点击「添加模型」

在 Trae 左侧菜单中选择「模型」进入模型管理页面，点击顶部的「+ 添加模型」按钮。

![trae](./img/trae01.png)

## 第二步 在「自定义配置」中填写模型信息

在「添加模型」弹窗中切换到「自定义配置」标签页。Trae 支持两种 API 格式，您可根据要接入的模型类型任选其一填写（也可分别添加两条配置，分别使用 OpenAI 格式模型与 Claude 系列模型）。

::: tip 通用字段
- **模型 ID**：填入您需要使用的模型名称，可在 DMXAPI 网站顶部的「模型价格」页面查看并复制
- **API 密钥**：填入您的 DMXAPI 密钥
- **自定义请求地址**：**不要以斜杠结尾**，Trae 会根据所选 API 格式自动补全后续路径
:::

### 类型一：OpenAI Chat Completions 格式（适用于 GPT、Qwen、DeepSeek 等模型）

- **API 格式**：选择 `OpenAI Chat Completions 格式`
- **自定义请求地址**（Trae 自动补全 `/chat/completions`）：
  - cn 站：`https://www.dmxapi.cn/v1`
  - com 站：`https://www.dmxapi.com/v1`
  - ssvip 站：`https://ssvip.dmxapi.com/v1`
- **模型 ID** 示例：`gpt-5.5`

![trae](./img/trae02.png)

### 类型二：Anthropic Messages 格式（适用于 Claude 系列模型）

- **API 格式**：选择 `Anthropic Messages 格式`
- **自定义请求地址**（Trae 自动补全 `/v1/messages`）：
  - cn 站：`https://www.dmxapi.cn`
  - com 站：`https://www.dmxapi.com`
  - ssvip 站：`https://ssvip.dmxapi.com`
- **模型 ID** 示例：`claude-opus-4-7`

![trae](./img/trae03.png)

填写完成后点击底部「添加模型」按钮保存。

## 第三步 在对话界面选择配置好的模型

回到对话界面，点击输入框右下角的模型选择下拉框，在底部「自定义模型」分组中即可看到刚刚配置好的模型（如 `claude-opus-4-7`、`gpt-5.5`），点击选中您要使用的模型即可（已选中的模型右侧会显示绿色对勾）。

![trae](./img/trae04.png)

## 第四步 发送消息测试

在 Builder 对话中发送一条测试消息（如 `hi`），收到模型正常回复（如 `Hi! How can I help you today?`）即表示配置成功，可以开始愉快地使用 Trae 进行 AI 编程。

![trae](./img/trae05.png)

<p align="center">
  <small>© 2026 DMXAPI Trae 客户端配置教程</small>
</p>
