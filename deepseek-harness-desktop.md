# DeepSeek Harness 桌面端的安装和配置教程

DeepSeek Harness 是 DeepSeek 官方推出的全新 AI Agent 桌面客户端，主打「组装无限可能，共探智能上限」。它内置工作区、插件、Agent 预设等能力，支持通过自定义模型 API 接入中转站或自部署服务，兼容 **OpenAI Chat Completions**、**OpenAI Responses**、**Anthropic Messages** 三种主流 API 协议。

本教程以 Windows 系统为例，演示如何在 DeepSeek Harness 桌面端中接入 DMXAPI。

## 一、下载与安装

### 1. 进入官网下载客户端

打开 DeepSeek 官方下载页面，根据您的电脑系统选择对应的安装包进行下载。

DeepSeek Harness 桌面端下载地址：

```
https://www.deepseek.com/download/
```

### 2. 下载完成后进行安装

下载完成后，双击安装包按提示完成安装，安装完成后打开 DeepSeek Harness。

## 二、启动并跳过官方 Key 配置

### 1. 选择「添加 API Key」

在欢迎界面点击 **添加 API Key**。

![deepseek-harness](img/deepseek-harness-desktop1.png)

### 2. 点击「稍后配置」

此处填写的是 DeepSeek 官方密钥，我们暂不填写，直接点击 **稍后配置**，后续使用自定义模型 API 接入 DMXAPI。

![deepseek-harness](img/deepseek-harness-desktop2.png)

## 三、添加 DMXAPI 模型提供商

DeepSeek Harness 支持自定义模型 API，下面分别演示 **Chat Completions**、**Responses**、**Anthropic Messages** 三种协议的接入方式，您可按需选择其中一种或全部配置。

### 1. 打开设置，进入「模型」

进入主界面后，点击左下角的 **··· 更多**。

![deepseek-harness](img/deepseek-harness-desktop3.png)

### 2. 点击「添加模型提供商」

1. 在设置左侧菜单点击 **模型**
2. 点击下方的 **+ 添加模型提供商**

![deepseek-harness](img/deepseek-harness-desktop4.png)

## 1. 配置 Chat Completions 协议供应商

在添加提供商界面选择 **自定义模型 API**，依次填写：

1. **Provider ID**：以小写字母开头的标识，例如 `dmxapi-chat`
2. **显示名称**：自定义显示名称，例如 `dmxapi-chat`
3. **API 地址**（需带 `/v1`）：`https://www.dmxapi.cn/v1`
4. **API 协议**：选择 **OpenAI Chat Completions**

![deepseek-harness](img/deepseek-harness-desktop5.png)

### 1. 填写密钥并获取模型

1. **API 密钥**：填写您的 DMXAPI 密钥
2. 点击 **获取可用模型**，可拉取 DMXAPI 的可用模型列表进行勾选（见下一步）；也可以点击 **+ 添加模型** 手动填写模型
3. 模型添加完成后，点击 **创建提供商**

![deepseek-harness](img/deepseek-harness-desktop6.png)

### 2. 勾选要添加的模型

1. 在弹出的模型列表中，先点击 **取消全选**（可前往 [DMXAPI 模型广场](https://www.dmxapi.cn/rmb) 查看您需要的模型名称）
2. 勾选完成后点击 **添加所选**

![deepseek-harness](img/deepseek-harness-desktop7.png)

### 3. 搜索模型并添加

1. 在搜索框中输入完整模型名称，例如 `deepseek-v4.1-flash`
2. 勾选该模型
3. 点击 **添加所选**

![deepseek-harness](img/deepseek-harness-desktop8.png)

### 4. 配置模型参数并创建

1. **上下文窗口 / 最大输出 token 数**：按模型本身的能力填写（可在模型广场查看），例如 `1000000` 和 `128000`
2. **输入类型**：默认勾选文本，**图片** 需要确认模型支持图片输入后再勾选
3. 点击 **创建提供商**

![deepseek-harness](img/deepseek-harness-desktop9.png)

### 5. 选择模型开始使用

新建会话，在聊天框右下角的模型选择处，选择 **dmxapi-chat** 下刚配置好的模型（如 `deepseek-v4.1-flash`）。

![deepseek-harness](img/deepseek-harness-desktop10.png)

在输入框中发送内容，模型正常回复即表示配置成功，可以正常使用了。

![deepseek-harness](img/deepseek-harness-desktop11.png)

## 2.（可选）配置 Responses 协议供应商

如需 Responses 协议，再次点击 **+ 添加模型提供商**，选择 **自定义模型 API**，依次填写：

1. **Provider ID**：例如 `dmxapi-responses`
2. **显示名称**：例如 `dmxapi-responses`
3. **API 地址**（需带 `/v1`）：`https://www.dmxapi.cn/v1`
4. **API 协议**：选择 **OpenAI Responses**

![deepseek-harness](img/deepseek-harness-desktop12.png)

### 1. 填写密钥并获取模型

1. **API 密钥**：填写您的 DMXAPI 密钥
2. 点击 **获取可用模型** 拉取模型列表（或点击 **+ 添加模型** 手动配置）
3. 点击 **创建提供商**

![deepseek-harness](img/deepseek-harness-desktop13.png)

### 2. 取消全选

在弹出的模型列表中，先点击 **取消全选**，再按需搜索勾选。

![deepseek-harness](img/deepseek-harness-desktop14.png)

### 3. 搜索模型并添加

1. 在搜索框中输入完整模型名称，例如 `gpt-6-luna`
2. 勾选该模型
3. 点击 **添加所选**

![deepseek-harness](img/deepseek-harness-desktop15.png)

### 4. 配置模型参数并保存

1. **上下文窗口 / 最大输出 token 数**：按模型本身的能力填写，例如 `1M` 和 `128K`
2. **输入类型**：确认模型支持图片输入后再勾选 **图片**
3. 点击 **保存**

![deepseek-harness](img/deepseek-harness-desktop16.png)

## 3.（可选）配置 Anthropic Messages 协议供应商

如需 Anthropic 协议，再次点击 **+ 添加模型提供商**，选择 **自定义模型 API**，依次填写：

1. **Provider ID**：例如 `dmxapi-messages`
2. **显示名称**：例如 `dmxapi-messages`
3. **API 地址**（Anthropic 协议 **不需要** 带 `/v1`）：`https://www.dmxapi.cn`
4. **API 协议**：选择 **Anthropic Messages**

![deepseek-harness](img/deepseek-harness-desktop17.png)

### 1. 填写密钥并获取模型

1. **API 密钥**：填写您的 DMXAPI 密钥
2. 点击 **获取可用模型** 拉取模型列表（或点击 **+ 添加模型** 手动配置）
3. 点击 **创建提供商**

![deepseek-harness](img/deepseek-harness-desktop18.png)

### 2. 取消全选

在弹出的模型列表中，先点击 **取消全选**，再按需搜索勾选。

![deepseek-harness](img/deepseek-harness-desktop19.png)

### 3. 搜索模型并添加

1. 在搜索框中输入完整模型名称，例如 `claude-sonnet-5-5`
2. 勾选该模型
3. 点击 **添加所选**

![deepseek-harness](img/deepseek-harness-desktop20.png)

### 4. 配置模型参数并创建

1. **上下文窗口 / 最大输出 token 数**：按模型本身的能力填写，例如 `1000000` 和 `128000`
2. **输入类型**：确认模型支持图片输入后再勾选 **图片**
3. 点击 **创建提供商**

![deepseek-harness](img/deepseek-harness-desktop21.png)

## 四、选择模型开始使用

三种协议都配置完成后，在聊天框右下角的模型选择处即可看到 **dmxapi-chat**、**dmxapi-responses**、**dmxapi-messages** 三个供应商，任选其下配置好的模型即可开始使用。

![deepseek-harness](img/deepseek-harness-desktop22.png)

可以开始用起来啦！！！！

---
<p align="center">
  <small>© 2026 DMXAPI DeepSeek Harness 桌面端的安装及配置</small>
</p>
