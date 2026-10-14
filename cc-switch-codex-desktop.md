# CC Switch 配置 Codex 桌面端教程

CC-Switch 是一款面向开发者的多供应商配置切换工具，可在 Claude Code、Codex 等多种客户端之间一键切换不同的 API 厂商与模型。本文介绍如何使用 CC Switch 将 **Codex 桌面端** 接入 DMXAPI。

本教程包含三个专题，按您要使用的模型类型选择其中一个进行配置即可：

- **DMXAPI(gpt原生支持)**：使用 GPT 系列原生模型（Responses API 直连）
- **DMXAPI(codex专区配置)**：使用 codex 专区模型（`-cdx` 后缀，如 `gpt-6.1-sol-cdx`）
- **DMXAPI(国产模型配置)**：使用国产模型（如 `deepseek-v4.1-flash`、`glm-5.3`），通过 Chat Completions 协议接入

## 环境准备

在开始之前，请先完成以下准备：

- - 安装 **Codex 桌面端**：前往 [Codex 官网下载页](https://chatgpt.com/zh-Hans-CN/download/) 下载并安装。
- 下载 **CC Switch** 工具：前往 [CC Switch 官网](https://ccswitch.io/zh/) 下载并安装。
- 准备一个 DMXAPI 令牌（API Key），可在 [DMXAPI 控制台](https://www.dmxapi.cn/keys) 的「API 令牌」页获取。

## 前置步骤

三个专题的前两步操作相同，先完成以下准备操作。

### 步骤 1：选择 Codex 并添加供应商

打开 CC Switch，按截图中的编号操作：

- ① 点击左侧的 **Codex** 选项卡
- ② 点击右上角橙色 **「添加供应商」** 按钮

![cc_switch_codex_desktop](img/cc-switch-codex-desktop1.png)

### 步骤 2：选择预设供应商 DMXAPI

进入「添加新供应商」页面，按编号操作：

- ① 在搜索栏中搜索 **DMXAPI**
- ② 点击选择 **DMXAPI** 预设

![cc_switch_codex_desktop](img/cc-switch-codex-desktop2.png)

## DMXAPI(gpt原生支持)

本专题适用于直接使用 **GPT 系列原生模型**（如 `gpt-6.1-sol`），上游走 Responses API 直连，无需模型映射。

### 步骤 1：填写供应商信息

在供应商配置表单中按编号依次操作：

- ① **API Key**：填入您的 DMXAPI 令牌
- ② **名称**：自定义供应商名称，例如 `DMXAPI`（名称仅用于区分不同配置）
- ③ **API 请求地址**：检查为 `https://www.dmxapi.cn/v1`
- ④ **默认模型**：建议修改为 `gpt-6.1-sol`
- ⑤ 确认无误后点击右下角的 **「保存」** 完成配置

![cc_switch_codex_desktop](img/cc-switch-codex-desktop3.png)

### 步骤 2：启用供应商

回到主界面，在 `DMXAPI` 供应商卡片上：

- ① 点击 **「启用」**

启用后重启 Codex 桌面端使配置生效。

![cc_switch_codex_desktop](img/cc-switch-codex-desktop4.png)

### 步骤 3：开始使用

重启 Codex 桌面端后：

- ① 在对话框中输入消息，如 `HI`
- ② 点击右下角的 **「模型」** 下拉框，选择 `6.1 Sol`、`6 Astra` 等模型
- ③ 点击 **「发送」**

![cc_switch_codex_desktop](img/cc-switch-codex-desktop5.png)

### 步骤 4：验证模型响应

模型正常回复后，即可正常使用。恭喜你完成配置！

![cc_switch_codex_desktop](img/cc-switch-codex-desktop6.png)

## DMXAPI(codex专区配置)

本专题适用于使用 **codex 专区模型**（`-cdx` 后缀，如 `gpt-6.1-sol-cdx`），需要在「模型列表」中添加专区模型。

### 步骤 1：创建带模型限制的令牌

登录 DMXAPI 官网，进入 **工作台 → 令牌** 页面，创建 API 密钥：

- ① **名称**：自定义令牌名称，例如 `DMXAPI-CDX`
- ② 打开 **高级设置**，在 **模型限制** 中加上您要使用的 `-cdx` 模型，例如 `gpt-6.1-sol-cdx`（令牌仅能使用选定的模型，防止误调用其他模型）
- ③ 最后点击 **「保存更改」**

![cc_switch_codex_desktop](img/cc-switch-codex-desktop7.png)

### 步骤 2：填写供应商信息

回到 CC Switch，参考前置步骤再次点击 **「添加供应商」** 并选择 DMXAPI 预设，在配置表单中按编号依次操作：

- ① **API Key**：填入上一步创建的 DMXAPI 令牌
- ② **名称**：自定义供应商名称，例如 `DMXAPI-CDX`
- ③ **API 请求地址**：检查为 `https://www.dmxapi.cn/v1`
- ④ 点击 **「获取模型列表」** 检验模型连通性

![cc_switch_codex_desktop](img/cc-switch-codex-desktop8.png)

### 步骤 3：添加并配置模型

在「模型列表」区按编号依次操作：

- ① 如果令牌进行了上一步的模型限制，可以直接点击 **「选择模型」** 一键添加并进行配置
- ② 也可以点击 **「手动添加」** 逐条添加模型
- ③ 配置 codex 专区您使用的模型：在 **菜单显示名 / 实际请求模型** 中输入专区模型名称（如 `gpt-6.1-sol-cdx`），并填入对应的 **上下文窗口**（如 `872000`）
- ④ 确认无误后点击右下角的 **「添加」**

![cc_switch_codex_desktop](img/cc-switch-codex-desktop9.png)

### 步骤 4：配置思考等级和上下文窗口

点击模型行的 **「思考等级」** 下拉框，配置模型支持的思考等级和上下文窗口：

- 勾选模型支持的思考等级（如 `low`、`medium`、`high`、`xhigh`、`max`、`ultra`）
- 在下方 **「默认等级」** 中选择默认的思考等级

::: warning 注意
请先确认所选模型是否支持对应的思考等级（low/high/max 等思考深度控制），再进行开启。
:::

![cc_switch_codex_desktop](img/cc-switch-codex-desktop10.png)

### 步骤 5：启用供应商

回到主界面：

- ① 点击 `DMXAPI-CDX` 供应商卡片上的 **「启用」** 按钮切换启用（启用后显示「使用中」）

启用后重启 Codex 桌面端使配置生效。

![cc_switch_codex_desktop](img/cc-switch-codex-desktop11.png)

### 步骤 6：开始使用

重启后即可正常对话使用：

- ① 在对话框中输入消息，如 `HI`
- ② 在模型下拉框中选择配置的模型，如 `6.1 Sol Cdx`
- ③ 点击 **「发送」**

![cc_switch_codex_desktop](img/cc-switch-codex-desktop12.png)

模型正常回复后，即可正常使用。

![cc_switch_codex_desktop](img/cc-switch-codex-desktop13.png)

## DMXAPI(国产模型配置)

本专题适用于使用 **国产模型**（如 `deepseek-v4.1-flash`、`glm-5.3`），上游走 **Chat Completions** 协议，需要开启 CC Switch 的本地路由才能转换为 Codex 可用的格式。

### 步骤 1：创建带模型限制的令牌

登录 DMXAPI 官网，进入 **工作台 → 令牌** 页面，创建 API 密钥：

- ① **名称**：自定义令牌名称，例如 `DMXAPI-国产模型`
- ② 打开 **高级设置**，在 **模型限制** 中选择您要配置的模型，例如 `deepseek-v4.1-flash`、`glm-5.3`、`kimi-k3` 等
- ③ 最后点击 **「保存更改」**

![cc_switch_codex_desktop](img/cc-switch-codex-desktop14.png)

### 步骤 2：填写供应商信息

回到 CC Switch，参考前置步骤再次点击 **「添加供应商」** 并选择 DMXAPI 预设，在配置表单中按编号依次操作：

- ① **API Key**：填入上一步创建的 DMXAPI 令牌
- ② **名称**：自定义供应商名称，例如 `DMXAPI-国产模型`
- ③ **API 请求地址**：检查为 `https://www.dmxapi.cn/v1`

然后在 **「模型列表」** 区配置您使用的模型（可通过 **「选择模型」** 一键配置或 **「手动添加」**），为每个模型填入 **菜单显示名 / 实际请求模型**、**上下文窗口**（如 `1000000`）和 **思考等级**。

![cc_switch_codex_desktop](img/cc-switch-codex-desktop15.png)

### 步骤 3：设置上游格式并保存

继续在表单中向下操作：

- ① 如果配置了模型限制，可以点击 **「选择模型」** 一键配置
- ② 也可以点击 **「手动添加」** 手动添加配置
- ③ 检查模型配置是否正确
- ④ 展开 **「高级选项」**，**上游格式**选择 **Chat Completions（需转换）**
- ⑤ 确认无误后点击右下角的 **「添加」**

::: warning 注意
直连模式下用不了 Chat Completions 格式，切到 **路由** 或 **聚合** 后才能用这张卡。
:::

![cc_switch_codex_desktop](img/cc-switch-codex-desktop16.png)

### 步骤 4：开启本地路由并启用供应商

回到主界面：

- ① 点击 `DMXAPI-国产模型` 供应商卡片上的 **「启用」** 按钮切换启用（卡片带「需要路由」标签）

![cc_switch_codex_desktop](img/cc-switch-codex-desktop17.png)

弹出「需要路由」提示后：

- ① 选择 **「开始路由并使用它」**，开启本地路由并切换到该配置

![cc_switch_codex_desktop](img/cc-switch-codex-desktop18.png)

### 步骤 5：开始使用

重启 Codex 桌面端后：

- ① 在对话框中输入消息，如 `hi`
- ② 在模型下拉框中选择配置的模型，如 `deepseek-v4.1-flash`
- ③ 点击 **「发送」**

![cc_switch_codex_desktop](img/cc-switch-codex-desktop19.png)

模型正常回复后，即可正常使用。恭喜你完成配置！

![cc_switch_codex_desktop](img/cc-switch-codex-desktop20.png)

<p align="center">
  <small>© 2026 DMXAPI CC Switch 配置 Codex 桌面端教程</small>
</p>
