# CC Switch 配置 OpenCode 教程

CC-Switch 是一款面向开发者的多供应商配置切换工具，可在 Claude Code、Codex、OpenCode 等多种客户端之间一键切换不同的 API 厂商与模型。本文介绍如何使用 CC Switch 将 **OpenCode（CLI）** 接入 DMXAPI。

## 环境准备

在开始之前，请先完成以下准备：

- 下载 **CC Switch** 工具：前往 [CC Switch 官网](https://ccswitch.io/zh/) 下载并安装。
- 准备一个 DMXAPI 令牌（API Key），可在 [DMXAPI 控制台](https://www.dmxapi.cn/keys) 的「API 令牌」页获取。
- 已安装 OpenCode CLI，如未安装可参考 [opencode 的安装和配置教程](/opencode)。

## 检查更新

在正式配置前，请先确认 OpenCode 为最新版本，避免因版本过旧导致配置不生效。

### 步骤 1：打开安装与升级

打开 CC Switch，按截图中的编号操作：

- ① 点击右上角的 **「...」** 按钮
- ② 在弹出的菜单中点击 **「安装与升级」**

![cc_switch_opencode](img/claude-code-cli-cc-switch1.png)

![cc_switch_opencode](img/claude-code-cli-cc-switch2.png)

### 步骤 2：检查更新

进入「应用」页面：

- ① 点击右上角的 **「检查更新」**，查看对应配置软件（OpenCode）是否是最新版本，如有新版本请先升级再继续配置

![cc_switch_opencode](img/claude-code-cli-cc-switch3.png)

## 配置 OpenCode

### 步骤 1：选择 OpenCode 并添加供应商

打开 CC Switch 主界面：

- ① 点击左侧的 **OpenCode** 选项卡
- ② 点击右上角橙色 **「添加供应商」** 按钮

![cc_switch_opencode](img/opencode-cc-switch1.png)

### 步骤 2：选择预设供应商 DMXAPI

进入「添加供应商」页面，按编号操作：

- ① 在搜索栏中搜索 **DMXAPI**
- ② 选择 **DMXAPI** 预设

![cc_switch_opencode](img/opencode-cc-switch2.png)

### 步骤 3：填写供应商信息

在配置表单中按编号依次操作：

- ① **供应商标识**：自定义标识符，如 `dmxapi-chat`（配置文件中的唯一标识符，只能使用小写字母、数字和连字符）
- ② **名称**：自定义供应商名称，如 `DMXAPI-chat`
- ③ **接口格式**：选择 **OpenAI Compatible**
- ④ **API Key**：填入您的 DMXAPI 令牌
- ⑤ **Base URL**：检查是否为 `https://www.dmxapi.cn/v1`

::: tip 提示
- 选择 DMXAPI 预设后，**Base URL** 已预设为 `https://www.dmxapi.cn/v1`，无需修改，注意不要以斜杠结尾。
- **接口格式**保持 **OpenAI Compatible** 即可，DMXAPI 模型广场中的对话模型均可通过该格式接入。
:::

![cc_switch_opencode](img/opencode-cc-switch3.png)

### 步骤 4：添加模型

在「模型配置」区点击 **「选择模型」**，打开模型选择弹窗：

![cc_switch_opencode](img/opencode-cc-switch4.png)

在弹窗中按编号依次操作：

- ① 在搜索栏中搜索您要使用的模型，如 `glm-5.3-flash`
- ② 勾选要使用的模型（可重复搜索勾选多个模型，也可以点击 **「手动添加」** 逐条添加）
- ③ 点击右下角的 **「应用」**

![cc_switch_opencode](img/opencode-cc-switch5.png)

### 步骤 5：预览模型并保存

回到配置表单，按编号依次操作：

- ① 预览已添加的模型（模型 ID 与显示名称）
- ② 确认无误后点击右下角的 **「添加」** 保存

![cc_switch_opencode](img/opencode-cc-switch6.png)

### 步骤 6：启用供应商

回到 OpenCode 供应商主界面，在「可添加」区的 DMXAPI 供应商卡片上：

- ① 点击 **「+」** 按钮，将 DMXAPI 配置添加到「已添加」列表，即启用该配置

启用后，恭喜你完成配置！接下来启动 OpenCode 验证效果。

![cc_switch_opencode](img/opencode-cc-switch7.png)

## 启动演示

### 1、打开终端，输入 opencode 启动

![cc_switch_opencode](img/opencode-cc-switch8.png)
> 打开终端，输入 `opencode` 后回车启动 OpenCode。

### 2、输入 /model 切换模型

![cc_switch_opencode](img/opencode-cc-switch9.png)
> 在输入框中输入 `/model`，回车打开模型选择列表。

### 3、选择 DMXAPI 中配置的模型

![cc_switch_opencode](img/opencode-cc-switch10.png)
> 在模型列表的 **DMXAPI** 分组下，选择您刚才配置的模型（如 `glm-5.3-flash`）。

### 4、确认模型并输入对话

![cc_switch_opencode](img/opencode-cc-switch11.png)
> ① 查看底部状态栏，确认当前模型已切换为 DMXAPI 配置的模型（如 `glm-5.3-flash  DMXAPI`）
> ② 在对话框中输入"hi"，回车发送

### 5、模型响应成功，可以开始使用了

![cc_switch_opencode](img/opencode-cc-switch12.png)

<p align="center">
  <small>© 2026 DMXAPI CC Switch 配置 OpenCode 教程</small>
</p>
