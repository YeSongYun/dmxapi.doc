# opencode的安装和配置教程
OpenCode 是一款基于 Go 的命令行编程工具（CLI），为开发者提供强大的 AI 协助，帮助编程、除错等工作。该工具提供了直观的终端用户界面（TUI），支持多个大语言模型（LLM）供应商，包括 OpenAI、 Anthropic、Gemini 等，同时也兼容通过 Ollama
等工具运行的本地模型，提供灵活的推理部署选项。

-  ✈️交互式终端界面：利用 Bubble Tea提供顺畅的终端体验。
-  🚀会话管理：可储存和管理多个会话，支持持久化存储。
-  🚗自定义命令：支持自定义命令，可预设多个占位符和参数。
-  🚢集成 LSP：提供代码智能和诊断功能。
-  🌈安装和配置简便：支持多种安装方式，并提供丰富的环境变数配置选项。


## 安装指南

1、OpenCode官方提供提供终端界面、桌面应用程序和 IDE 扩展三种使用方式，安装 CLI 最简单的方法是通过脚本安装：

```
curl -fsSL https://opencode.ai/install | bash

```


2、Windows 系统推荐下载 Node.js，然后通过 NPM 命令安装 OpenCode 官方 CLI 程序。

node.js安装地址：

```
https://nodejs.org/zh-cn/download

```

OpenCode安装命令：

```
npm i -g opencode-ai@latest

```

3、macOS 用户可以通过 Homebrew 安装桌面客户端

```
brew install anomalyco/tap/opencode

```
  


## 配置教程

OpenCode 可通过我司自研的小插件实现快速配置与一键接入，显著降低环境初始化、密钥与参数管理、调用链路对接等集成成本，帮助团队在开发、测试与生产等不同环境中保持一致的接入体验，并便于在多个项目间复用与迁移。插件采用模块化设计，支持按需启用能力、灵活扩展与二次开发，同时提供清晰的配置示例与使用说明，便于快速上手与持续维护。该插件已正式开源，地址如下。

CNB仓库： https://cnb.cool/dmxapi/opencode_dmxapi

github仓库：https://github.com/YeSongYun/OpenCode-DMXAPI

## 配置细化

这里我以Windows系统为例演示

### 1. 输入仓库链接，准备下载插件

仓库下载链接：
https://cnb.cool/dmxapi/opencode_dmxapi

![opencode](img\1-27-1.png)
### 2. 根据您的系统环境选择合适的插件，点击下载 

![opencode](img\1-27-2.png)
### 3. 下载插件

![opencode](img\1-27-3.png)

### 4. 根据您的系统环境选择合适的插件，点击下载 

![opencode](img\1-27-4.png)

### 5. 选择DMXAPI和输入API 密钥
下载成功后双击打开，进入配置界面，然后填写您的url，如下图：

![opencode](img\1-12-3.png)

### 6. 配置key

配置key时要注意跟第三步填写的url对应

![opencode](img\1-12-4.png)

### 7. 根据需求添加模型

![opencode](img\1-12-5.png)

### 8. 配置成功，退出配置界面

![opencode](img\1-12-6.png)

### 9. 在系统终端中使用
在搜索栏中输入cmd，单击回车打开系统终端，输入opencode，回车。

![opencode](img\1-12-7.png)

### 10. 选择想用的模型

在聊天框中输入"/model"，单击回车
![opencode](img\1-12-8.png)

### 9. 选择之前填入的DMXAPI后缀的模型

![opencode](img\1-12-9.png)


### 10. 验证模型的配置情况，开始使用

可以开始用起来啦！！！！
![opencode](img\1-12-10.png)

---
<p align="center">
  <small>© 2025 DMXAPI opencode的安装及配置</small>
</p>