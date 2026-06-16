# ZCode 的安装和配置教程

ZCode 是一款面向开发者的 AI Agent 编程桌面客户端，主打"简单、迅捷、氛围十足"的编程体验。它内置任务管理、代码预览、技能、MCP 服务器、插件管理等能力，并支持自定义模型供应商，可灵活接入 Chat Completions、Responses、Anthropic Messages 三种主流 API 格式。

-  ✈️ 开箱即用：提供 Windows / macOS 桌面客户端，下载安装即可使用。
-  🚀 任务与工作区管理：支持多任务、多工作区，方便管理不同项目。
-  🚗 自定义供应商：可完全自定义 API 端点与模型，灵活接入第三方服务。
-  🚢 多格式兼容：同时支持 Anthropic Messages、Chat Completions、Responses 三种 API 格式。
-  🌈 丰富生态：内置技能、MCP 服务器、插件管理与索引库等能力。

本教程以 Windows 系统为例，演示如何在 ZCode 中接入 DMXAPI。

## 一、下载与安装

### 1. 进入官网下载客户端

打开 ZCode 官网，根据您的电脑系统选择对应的安装包进行下载。

ZCode 官网下载地址：

```
https://zcode.z.ai/cn
```

![zcode](img\Zcode1.png)

### 2. 下载完成后进行安装

下载完成后，双击安装包（如 `ZCode-3.0.1-win-x64.exe`）进行安装。

![zcode](img\Zcode2.png)

## 二、启动并跳过登录

### 3. 选择"使用 API key"

安装完成后打开 ZCode，在欢迎界面点击 **使用 API key**。

![zcode](img\Zcode3.png)

### 4. 点击"暂时跳过"

在登录界面无需填写官方 API Key，直接点击 **暂时跳过**，后续我们使用自定义供应商接入 DMXAPI。

![zcode](img\Zcode4.png)

## 三、添加 DMXAPI 模型供应商

ZCode 支持自定义供应商，下面分别演示 **Chat Completions**、**Responses**、**Anthropic Messages** 三种格式的接入方式，您可按需选择其中一种或全部配置。

### 5. 进入"模型设置"，点击"添加供应商"

在左侧菜单进入 **模型设置**，在自定义供应商区域点击 **+ 添加供应商**。

![zcode](img\Zcode5.png)

### 6. 了解三种 API 格式

ZCode 的"API 格式"提供三种选项，分别对应 DMXAPI 的三种接入格式：

1. **Anthropic Messages（/v1/messages）** —— Anthropic 格式
2. **Chat Completions（/chat/completions）** —— Chat Completions 格式
3. **Responses（/responses）** —— Responses 格式

![zcode](img\Zcode6.png)

### 7. 配置 Chat Completions 格式供应商

在添加供应商界面依次填写：

- **名称**：自定义供应商名称，例如 `DMXAPI-Chat`
- **Base URL**（Chat / Responses 格式需带 `/v1`）：
  - cn 站：`https://www.dmxapi.cn/v1`
  - com 站：`https://www.dmxapi.com/v1`
  - ssvip 站：`https://ssvip.dmxapi.com/v1`
- **API Key**：填写您的 DMXAPI 密钥
- **API 格式**：选择 **Chat Completions（/chat/completions）**

![zcode](img\Zcode7.png)

### 8. 点击"添加模型"

填写完基本信息后，点击 **+ 添加模型**，准备录入要使用的模型。

![zcode](img\Zcode8.png)

### 9. 查询模型名称与上下文

可在 DMXAPI 的模型广场查看 **模型名称** 与对应的 **上下文** 长度，复制需要使用的模型名称。

![zcode](img\Zcode9.png)

### 10. 填写模型 ID 与上下文窗口

在"编辑模型配置"弹窗中：

1. **模型 ID**：填写模型名称，例如 `deepseek-v4-pro-guan`
2. **上下文窗口**：设置上下文长度（不要超过模型本身的上下文限制），例如 `1000000`

填写完成后点击 **保存**。

![zcode](img\Zcode10.png)

### 11. 完成 Chat 供应商配置

确认名称、Base URL、API Key、API 格式与模型列表无误后，点击 **添加供应商** 完成保存。

![zcode](img\Zcode11.png)

### 12.（可选）配置 Responses 格式供应商

如需 Responses 格式，再次 **添加供应商**，按下图配置：

- **名称**：例如 `DMXAPI-Responses`
- **Base URL**（需带 `/v1`）：
  - cn 站：`https://www.dmxapi.cn/v1`
  - com 站：`https://www.dmxapi.com/v1`
  - ssvip 站：`https://ssvip.dmxapi.com/v1`
- **API Key**：填写您的 DMXAPI 密钥
- **API 格式**：选择 **Responses（/responses）**
- **模型列表**：添加模型，例如 `gpt-5.5`

填写完成后点击 **添加供应商**。

![zcode](img\Zcode12.png)

### 13.（可选）配置 Anthropic 格式供应商

如需 Anthropic 格式，再次 **添加供应商**，按下图配置：

- **名称**：例如 `DMXAPI-Anthropic`
- **Base URL**（Anthropic 格式 **不需要** 带 `/v1`）：
  - cn 站：`https://www.dmxapi.cn`
  - com 站：`https://www.dmxapi.com`
  - ssvip 站：`https://ssvip.dmxapi.com`
- **API Key**：填写您的 DMXAPI 密钥
- **API 格式**：选择 **Anthropic Messages（/v1/messages）**
- **模型列表**：添加模型，例如 `kimi-k2.7-code-cc`

填写完成后点击 **添加供应商**。

![zcode](img\Zcode13.png)

### 14. 完成三种格式配置

完成后即可在自定义供应商列表中看到 **DMXAPI-Chat**、**DMXAPI-Responses**、**DMXAPI-Anthropic** 三个供应商，恭喜您已完成三个格式的配置，现在可以使用模型了！

![zcode](img\Zcode14.png)

## 四、选择模型开始使用

### 15. 在聊天中选择模型

新建任务，在聊天框右下角的模型选择处，即可随意选择您想用的模型（DMXAPI-Chat / DMXAPI-Responses / DMXAPI-Anthropic 下的模型）进行使用。

![zcode](img\Zcode15.png)

可以开始用起来啦！！！！

---
<p align="center">
  <small>© 2026 DMXAPI ZCode 的安装及配置</small>
</p>
