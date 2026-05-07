# Pi Agent 配置 DMXAPI 教程

Pi 是一款轻量、可扩展的命令行 Coding Agent（CLI），运行在终端中，提供交互式聊天界面、Skills 技能体系、以及多模型供应商接入能力。Pi 通过本地 `models.json` 配置文件管理模型，天然兼容 OpenAI Chat Completions 协议，因此可以直接接入 **DMXAPI**，一个 Key 调用 GPT、Claude、Gemini、Qwen、Doubao 等全球主流大模型。

本文档将带你完成 **Node.js 环境准备 → 安装 Pi CLI → 配置 DMXAPI → 选择模型并使用** 的完整接入流程。


## 一、环境准备

Pi CLI 通过 npm 安装，因此需要先安装 **Node.js**（安装后会自带 `npm` 包管理器）。已安装的用户可跳过本节。

::: tip 推荐版本
建议使用 **Node.js v18 LTS 及以上**版本，版本过低请重装最新 LTS 版本。
:::

### 1. 检查是否已安装

打开终端，运行：

```bash
node -v
npm -v
```

如果能正常输出版本号（示例如下），说明已安装，可直接跳到「[二、安装 Pi CLI](#install-pi-cli)」：

```text
v22.14.0
10.9.2
```

如果提示 `node: command not found` 或 `'node' 不是内部或外部命令`，按下面对应系统进行安装。

### 2. 安装 Node.js

请按你的操作系统选择对应方式安装。

#### 🪟 Windows 安装

1. 访问 Node.js 官网：[https://nodejs.org/](https://nodejs.org/)
2. 下载 **LTS（长期支持版）** 安装包
3. 双击安装包，一路点击「Next」完成安装（保持默认选项即可）
4. 安装完成后，**重新打开终端**，运行 `node -v` 验证

#### 🍎 macOS 安装

**方式一：使用 Homebrew 安装（推荐）**

```bash
brew install node
```

如果还没装过 Homebrew，先粘贴下面这条命令安装 Homebrew：

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

**方式二：官网下载安装包**

访问 [https://nodejs.org/](https://nodejs.org/) 下载 macOS 安装包，双击安装。

#### 🐧 Linux 安装（Ubuntu / Debian）

```bash
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo bash -
sudo apt-get install -y nodejs
```

### 3. 验证安装

**重新打开终端**，运行下面命令确认安装成功：

```bash
node -v
npm -v
```

能看到版本号即表示环境准备完成。


## 二、安装 Pi CLI {#install-pi-cli}

打开终端（Windows 下 Command Prompt、PowerShell、Terminal 均可），运行以下命令全局安装 Pi ：

```bash
npm install -g @mariozechner/pi-coding-agent
```

![pi](img\pi01.png)

安装完成后，运行下面命令验证是否安装成功：

```bash
pi --version
```

![pi](img\pi02.png)

在终端中输入 `pi` 并回车，即可进入 Pi 的交互式界面：

```bash
pi
```

![pi](img\pi03.png)





## 三、配置 DMXAPI

Pi 通过用户目录下的 `models.json` 文件管理模型供应商。下面演示如何在该文件中配置 DMXAPI。

### 1. 创建 `models.json` 配置文件

**Windows：**

1. 打开文件资源管理器（任意一个文件夹窗口）
2. 在顶部路径地址栏中输入以下路径并回车：

   ```text
   C:\Users\你的电脑用户名\.pi\agent\
   ```

   ::: tip
   `.pi` 默认是隐藏文件夹，直接在地址栏输入路径是最快的进入方式。
   :::

3. 在该文件夹下新建一个文本文档，并重命名为 `models.json`（**请确保去掉了 `.txt` 后缀**）

![pi](img\pi04.png)

**macOS / Linux：**

```bash
mkdir -p ~/.pi/agent
touch ~/.pi/agent/models.json
```

### 2. 填入 DMXAPI 配置内容

用编辑器打开 `models.json`，粘贴以下内容（可按需增删模型）：

```json
{
  "providers": {
    "dmxapi": {
      "name": "DMX API",
      "baseUrl": "https://www.dmxapi.cn/v1",
      "apiKey": "sk-**************************************",
      "api": "openai-completions",
      "models": [
        {
          "id": "gpt-5.5",
          "name": "gpt-5.5",
          "input": ["text", "image"],
          "contextWindow": 1000000,
          "maxTokens": 128000
        },
        {
          "id": "gpt-5.2",
          "name": "gpt-5.2",
          "input": ["text", "image"],
          "contextWindow": 400000,
          "maxTokens": 128000
        },
        {
          "id": "claude-opus-4-7",
          "name": "claude-opus-4-7",
          "input": ["text", "image"],
          "contextWindow": 1000000,
          "maxTokens": 128000
        }
      ]
    }
  }
}
```
::: tip 模型字段说明
- `id`：调用时使用的模型名称，必须与 DMXAPI 平台支持的模型 ID 完全一致。
- `name`：在 Pi 界面中显示的名称，可自定义。
- `input`：模型支持的输入类型，纯文本模型填 `["text"]`，多模态模型填 `["text", "image"]`。
- `contextWindow` / `maxTokens`：上下文长度与单次最大输出长度，可参考 [DMXAPI 模型价格页](https://www.dmxapi.cn/rmb)。
:::

---

## 四、选择模型并开始使用

返回 Pi CLI 界面，输入命令：

```text
/model
```

即可看到刚刚配置的模型列表，使用方向键选择目标模型后回车确认。

![pi](img\pi05.png)

切换完成后，模型会显示在界面底部右下角，此时即可直接输入问题与模型对话。

![pi](img\pi06.png)



<p align="center">
  <small>© 2026 Pi Agent 配置 DMXAPI</small>
</p>
