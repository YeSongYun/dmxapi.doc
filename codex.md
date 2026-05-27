# Openai Codex 安装与配置教程

::: warning 注意
Codex 仅支持配置 **GPT-5 系列** 模型（如 `gpt-5.5`），请勿填写其他系列的模型，否则将无法正常调用。
:::

::: tip 建议
为防止 Codex 在使用过程中调用到非 GPT-5 系列模型，建议前往 DMXAPI 控制台编辑您的令牌，**启用「模型限制」并仅选定 `gpt-5.5`**（或其他 GPT-5 系列模型）。这样即使配置文件被误改，令牌也会拒绝其他模型的请求。
:::

## 创建带模型限制的令牌（推荐）

按照以下步骤创建一个仅允许调用 GPT-5 系列模型的专用令牌，避免 Codex 误调用其他模型造成意外消费。

**1. 进入 API 令牌页面**

登录 [DMXAPI 控制台](https://www.dmxapi.cn/)，进入左侧菜单的「API 令牌」页，点击「添加令牌」按钮。

![点击添加令牌创建新的令牌](/img/codex_shen1.png)

**2. 填写基本信息**

在弹出的「创建新的令牌」对话框中：

- ① 自定义令牌名称（例如 `codex测试`），方便后续识别。
- ② 选择令牌过期时间（如「永不过期」、「一个月」等，按需选择）。
- ③ 令牌渠道分组保持默认的 `default` 即可。

![填写令牌基本信息](/img/codex_shen2.png)

**3. 启用模型限制并提交**

继续在同一对话框中下滑到「安全设置」：

- ① 按需设置令牌额度（不需要可保留默认 `∞`）。
- ② 按需设置令牌次数限制。
- ③ **勾选「启用模型限制」**，在下方搜索并选定 `gpt-5.5`（Codex 仅支持 GPT-5 系列模型）。
- ④ 点击「提交」按钮保存。

![启用模型限制并提交保存](/img/codex_shen3.png)

**4. （可选）为已有令牌补充模型限制**

如果不想新建令牌，也可以在令牌列表中点击已有令牌的编辑按钮，在弹出的「更新令牌信息」对话框中同样勾选「启用模型限制」并选定 `gpt-5.5`，然后点击「提交」保存即可。

![为已有令牌启用模型限制](/img/codex_shen.png)

创建或更新完成后，将该令牌的 Key（`sk-...`）填入下文 Codex 的 `auth.json` 配置中即可。

## Windows 版本教程

### 系统要求
- Windows 10 或 Windows 11
- Node.js 22+
- npm 10+
- 网络连接

### 安装步骤

**前置步骤！！！**
安装 Git Bash，请访问 [Git - Downloads](https://git-scm.com/downloads) 下载对应您电脑系统的版本，之后一直点击“下一步”即可完成安装。

**1. 安装 Node.js**
访问 [Node.js 官网](https://nodejs.org/) 下载并安装最新 LTS 版本。

**2. 安装 codex**
打开命令提示符 (CMD) 或 PowerShell，运行：
```bash
npm install -g @openai/codex
````

**3. 验证安装**
打开命令提示符 (CMD) 或 PowerShell，运行：

```bash
codex --version
```


### 配置 第三方API 方法

**1. 配置文件**

1.  进入当前用户的用户目录下的 `.codex` 文件夹中，例如：`C:\Users\testuser\.codex`。

    **注意**：如果看不到该目录，说明您没有打开 Windows 的“显示隐藏的项目”，请先在文件资源管理器中开启。
    
![Windows 显示隐藏的项目设置](/img/codex_shen4.png)

2.  如果没有 `.codex` 文件夹，请手动创建该文件夹，然后在其中创建 `config.toml` 以及 `auth.json` 两个文件。

![image.png](/img/codex-dir.png)

3.  **填写配置** (需要将 `sk-xxxxxxxxxxxxxxxxxxxx` 替换成您的 DMXAPI 令牌)。

    a. `auth.json` 中的配置：

    ```json
    {"OPENAI_API_KEY": "sk-xxx"}
    ```

    b. `config.toml` 中的配置（直接粘贴下面的内容即可）：
    `model_reasoning_effort` 可选值为 `high`, `medium`, `low`，分别代表模型思考的努力程度（高、中、低）。

    ```toml
    model_provider = "DMX1"
    model = "gpt-5.5"
    model_reasoning_effort = "high"
    disable_response_storage = true
    preferred_auth_method = "apikey"

    [model_providers.DMX1]
    name = "DMX1"
    base_url = "https://www.dmxapi.cn/v1"
    wire_api = "responses"
    ```

### 关闭终端，然后再次启动 codex

#### 进入到您的工程目录：

```bash
cd your-project-folder
```

#### 运行以下命令启动：

```bash
codex
```

#### codex 运行界面：
![image.png](/img/codex.png)

---

## VSCode 插件 codex

以上配置完成后，在 VSCode 扩展商店中搜索并安装 `codex` 即可。

![在 VSCode 扩展商店搜索 codex](/img/codex_shen5.png)

安装完成后会出现在侧边栏。

![安装后出现在侧边栏](/img/codex_shen6.png)

---

## Mac 版本教程

### 系统要求

  - macOS 12 或更高版本
  - Node.js 22+
  - npm 10+
  - 网络连接

### 安装步骤

**1. 安装 codex**
打开终端 (Terminal)，运行（可能需要加 `sudo`）：

```bash
npm install -g @openai/codex
```

验证安装：打开终端 (Terminal)，运行：

```bash
codex --version
```

### 配置 API

**配置文件**

1.  创建目录和文件：

    ```bash
    mkdir -p ~/.codex
    touch ~/.codex/auth.json
    touch ~/.codex/config.toml
    ```

2.  编辑 `auth.json` 文件：

    ```bash
    vi ~/.codex/auth.json
    ```

    按 `i` 进入插入模式，粘贴以下内容（将 `sk-xxx` 替换为您的 DMXAPI 令牌），然后按 `ESC` 键，输入 `:wq` 并回车保存退出。

    ```json
    {"OPENAI_API_KEY": "sk-xxx"}
    ```

3.  编辑 `config.toml` 文件：

    ```bash
    vi ~/.codex/config.toml
    ```

    按 `i` 进入插入模式，粘贴以下内容，然后按 `ESC` 键，输入 `:wq` 并回车保存退出。

    ```toml
    model_provider = "api111"
    model = "gpt-5.5"
    model_reasoning_effort = "high"
    disable_response_storage = true
    preferred_auth_method = "apikey"

    [model_providers.api111]
    name = "api111"
    base_url = "https://www.dmxapi.cn/v1"
    wire_api = "responses"
    ```

### 重启终端，再次启动 codex

进入到您的工程目录：

```bash
cd your-project-folder
```

启动codex：

```bash
codex
```
---

## Linux 版本教程

### 系统要求

  - 主流 Linux 发行版 (Ubuntu 20.04+, Debian 10+, CentOS 7+, etc.)
  - Node.js 22+
  - npm 10+
  - 网络连接

### 安装步骤

**1. 安装 Node.js**

  - **Ubuntu/Debian**
    ```bash
    sudo apt update
    curl -fsSL [https://deb.nodesource.com/setup_lts.x](https://deb.nodesource.com/setup_lts.x) | sudo -E bash -
    sudo apt-get install -y nodejs
    ```
  - **CentOS/RHEL/Fedora**
    ```bash
    # 使用 dnf (Fedora) 或 yum (CentOS/RHEL)
    sudo dnf install nodejs npm
    # 或
    sudo yum install nodejs npm
    ```
  - **Arch Linux**
    ```bash
    sudo pacman -S nodejs npm
    ```

**2. 安装 codex**
打开终端 (Terminal)，运行：

```bash
sudo npm install -g @openai/codex
```

验证安装：打开终端 (Terminal)，运行：

```bash
codex --version
```

### Linux Codex 配置 DMXAPI

**配置文件**

1.  创建目录和文件：
    ```bash
    mkdir -p ~/.codex
    touch ~/.codex/auth.json
    touch ~/.codex/config.toml
    ```
2.  编辑 `auth.json` 文件：
    ```bash
    vi ~/.codex/auth.json
    ```
    按 `i` 进入插入模式，粘贴以下内容（将 `sk-xxx` 替换为您的密钥），然后按 `ESC` 键，输入 `:wq` 并回车保存退出。
    ```json
    {"OPENAI_API_KEY": "sk-xxx"}
    ```
3.  编辑 `config.toml` 文件：
    ```bash
    vi ~/.codex/config.toml
    ```
    按 `i` 进入插入模式，粘贴以下内容，然后按 `ESC` 键，输入 `:wq` 并回车保存退出。
    ```toml
    model_provider = "api111"
    model = "gpt-5.5"
    model_reasoning_effort = "high"
    disable_response_storage = true
    preferred_auth_method = "apikey"

    [model_providers.api111]
    name = "api111"
    base_url = "https://www.dmxapi.cn/v1"
    wire_api = "responses"
    ```

### 启动 codex

**重启终端！重启终端！重启终端！**
然后进入到您的工程目录：

```bash
cd your-project-folder
```

运行以下命令启动：

```bash
codex
```
![image.png](https://api.apifox.com/api/v1/projects/5443236/resources/575125/image-preview)

<p align="center">
  <small>© 2025 DMXAPI Openai C...</small>
</p>