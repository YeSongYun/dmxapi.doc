# Claude Code 配置教程文档

DMXAPI研发的一键配置 Anthropic Claude Code CLI 环境变量的跨平台工具。

## 功能特性

- 交互式配置 API 地址和认证令牌
- 自动验证 API 连接有效性
- 配置默认模型设置
- 支持 Windows / Linux / macOS
- 环境变量自动持久化

:::warning 注意
请先把.claude 文件夹下的setting.json文件删除
:::

## 环境准备

在开始之前，请确保你的电脑已安装 **Git**（建议 `v2.40+`），Claude Code 需要 Git 来管理代码仓库。

### 检查是否已安装

打开终端，运行以下命令：

```bash
git --version
```

如果能正常输出版本号（如下所示），说明已安装，可以跳过安装步骤：

```text
git version 2.45.0
```

### 安装 Git

如果提示 `git: command not found` 或 `'git' 不是内部或外部命令`，说明尚未安装，请按照你的操作系统选择对应方式安装：

**Windows：**

方式一：命令安装（推荐）

打开 PowerShell，运行：

```powershell
winget install --id Git.Git -e --source winget
```

安装完成后，**重新打开终端**，运行 `git --version` 验证。

方式二：手动下载安装

1. 访问 Git 官网：[https://git-scm.com/downloads/win](https://git-scm.com/downloads/win)
2. 下载 **64-bit Git for Windows Setup** 安装包
3. 双击安装包，一路点击「Next」完成安装（保持默认选项即可）
4. 安装完成后，**重新打开终端**，运行 `git --version` 验证

**macOS：**

方式一：使用 Homebrew 安装（推荐）

```bash
brew install git
```

方式二：在终端运行以下命令，系统会自动提示安装 Xcode 命令行工具（内含 Git）：

```bash
xcode-select --install
```

**Linux（Ubuntu / Debian）：**

```bash
sudo apt-get update
sudo apt-get install -y git
```

安装完成后，运行 `git --version` 确认安装成功。

## 安装 Claude Code

**macOS / Linux / WSL**

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

**Windows**

:::code-group
```powershell [PowerShell（推荐）]
irm https://claude.ai/install.ps1 | iex
```
```cmd [CMD]
winget install Anthropic.ClaudeCode
```
:::

:::tip Windows 用户提示
如果提示 `claude 不是内部或外部命令`，需将安装路径加入 PATH，根据终端**任选其一**运行：

:::code-group
```powershell [PowerShell]
[Environment]::SetEnvironmentVariable("Path", [Environment]::GetEnvironmentVariable("Path", "User") + ";$env:USERPROFILE\.local\bin", "User")
```
```cmd [CMD]
setx Path "%Path%;%USERPROFILE%\.local\bin"
```
:::

执行后**重新打开终端**即可生效。
:::

:::tip PowerShell 无法启动 Claude？
如果 PowerShell 提示脚本执行策略错误，无法运行 claude.ps1，这是 PowerShell 的安全策略在阻止，不是 Claude 本身出问题。运行以下命令解除限制：

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

执行后重新打开终端即可正常使用。
:::

安装完成后验证：

```bash
claude --version
```

## 第一步：下载配置工具

:::warning 注意
编程插件tokens消耗量很大，请注意tokens消耗
:::

### ⚡ 方式一：快速安装（推荐）

直接在终端运行对应命令，自动完成下载与安装。

:::tip 提示
以下命令为一次性安装脚本，运行后脚本不会保留在电脑上。如需再次使用配置工具，请重新运行对应命令，无需提前下载或保存。
:::

**Linux / macOS**

```bash
curl -fsSL https://cnb.cool/dmxapi/dmxapi_claude_code/-/git/raw/main/install.sh | bash
```

**Windows PowerShell**

```powershell
iwr -useb https://cnb.cool/dmxapi/dmxapi_claude_code/-/git/raw/main/install.ps1 | iex
```

**Windows CMD**

```cmd
curl -fsSL https://cnb.cool/dmxapi/dmxapi_claude_code/-/git/raw/main/install.cmd -o "%TEMP%\install.cmd" && call "%TEMP%\install.cmd"
```

:::tip 快速安装失败？
若以上命令执行失败，请参阅下方「方式二：手动下载」进行手动安装。
:::

### 📦 方式二：手动下载

> 适用于快速安装脚本无法运行的情况。
>
> 配置工具开源仓库地址：

- cnb：https://cnb.cool/dmxapi/dmxapi_claude_code


#### 1、打开 cnb 仓库，点击右侧「最新版插件链接」
![claude-code](img/claude-code-new24.png)
> 在仓库右侧 Release 区，点击最新版本（如 DMXAPI Claude Code v1.8.0）进入下载页。

#### 2、根据操作系统选择合适的插件，点击下载
![claude-code](img/claude-code-new25.png)
> 在附件列表中选择对应系统的插件下载，例如 Windows 选 windows-amd64.exe。

#### 3、下载完成
![claude-code](img/claude-code-new26.png)
> 下载完成后即可按下方安装说明运行。

#### 4、按安装说明运行
![claude-code](img/claude-code-new27.png)
> Windows 用户下载完成后可直接双击运行；Linux / macOS 用户需先 `chmod +x` 添加执行权限再运行（macOS 还需 `xattr -cr` 移除隔离标记），运行后即可跳到第二步进行配置。

## 第二步：运行配置

#### 1、进入配置界面，选择配置方式
![claude-code](img/claude-code-new1.png)
> 第一次配置，选择第一项「dmxapi 推荐配置」一键配置即可。

#### 2、确认推荐配置，填入 DMXAPI 令牌
![claude-code](img/claude-code-new2.png)
> 推荐配置已自动填好 Base URL 与各模型，只需粘贴你的 DMXAPI 令牌（Auth Token）后回车。

#### 3、配置完成，查看配置摘要
![claude-code](img/claude-code-new3.png)
> API 连接验证成功、配置保存成功后会显示配置摘要，按回车退出。配置已保存到环境变量，**重新打开终端**后生效。

#### 4、重新打开终端，输入 claude 启动
![claude-code](img/claude-code-new4.png)
> 重新打开终端，输入 `claude` 后回车启动 Claude Code。

#### 5、信任当前文件夹
![claude-code](img/claude-code-new5.png)
> 启动后出现安全提示，选择 `1. Yes, I trust this folder` 回车即可使用 Claude Code。

#### 6、在对话框中输入"你好"，回车
![claude-code](img/claude-code-new6.png)

#### 7、模型响应成功，可以开始使用了
![claude-code](img/claude-code-new7.png)


## 进阶：手动配置

> 如果你想自定义 Base URL、令牌、模型等参数，可在模式选择界面选择「手动配置」，按提示逐项填写。

#### 1、在模式选择界面，选择「手动配置」
![claude-code](img/claude-code-new8.png)
> 选择第二项「手动配置 URL / Token / 模型等」新增一套配置。

#### 2、填写配置名称
![claude-code](img/claude-code-new9.png)
> 为本次配置取一个目录名称，便于后续管理多套配置。

#### 3、填写 Base URL
![claude-code](img/claude-code-new10.png)
> 填入 API 服务器地址：cn 站填写 `https://www.dmxapi.cn`，com 站填写 `https://www.dmxapi.com`，ssvip 站填写 `https://ssvip.dmxapi.com`。

#### 4、填写 Auth Token
![claude-code](img/claude-code-new11.png)
> 粘贴你的 DMXAPI 令牌，获取地址：`https://www.dmxapi.cn/token`。

#### 5、配置模型设置
![claude-code](img/claude-code-new12.png)
> 进入模型配置菜单，用上下键和回车选择要配置的模型项（默认 / Haiku / Sonnet / Opus），配置完成后按 ESC 或输入 q 保存退出。

![claude-code](img/claude-code-new13.png)
> 进入某个模型项后，可从预设列表中选择模型（后缀 -cc 为 claude code 专区模型），也可选择最下方「自定义输入」。

![claude-code](img/claude-code-new14.png)
> 选择「自定义输入」后手动输入模型名称（需在模型广场中能找到该模型）。

#### 6、是否配置 Agent Teams 功能
![claude-code](img/claude-code-new15.png)
> Agent Teams 功能尚不完善，建议选择「否」保持当前值不变。

#### 7、是否配置 VSCode 插件
![claude-code](img/claude-code-new16.png)
> 选择「是」可将你配置的模型同步到 VSCode 插件。

#### 8、自定义 Git 署名
![claude-code](img/claude-code-new17.png)
> 可自定义提交时的 Git 署名，不需要可直接回车采用默认。

#### 9、写入 VSCode settings.json
![claude-code](img/claude-code-new18.png)
> 选择「是」将配置写入 VSCode `settings.json`，完成插件配置。

#### 10、配置完成
![claude-code](img/claude-code-new19.png)
> 出现配置摘要即表示配置完成，按回车结束。配置已保存到环境变量，**重新打开终端**后生效。

## 进阶：管理已有配置

> 已保存的配置会出现在模式选择界面，可随时切换、编辑或删除。

#### 1、在模式选择界面选中已保存的配置
![claude-code](img/claude-code-new20.png)
> 选择你想使用的已保存配置进入管理界面。

#### 2、选择管理操作
![claude-code](img/claude-code-new21.png)
> 可对配置执行：写入 settings.json 并应用到环境变量、编辑配置、删除配置。

#### 3、进入编辑配置
![claude-code](img/claude-code-new22.png)
> 选择「编辑此配置 修改 URL / Token / 模型 / 开关等」进入编辑界面。

#### 4、编辑配置
![claude-code](img/claude-code-new23.png)
> 编辑菜单可分别修改 URL / Token / 模型、effort 思考强度、Agent Teams、VSCode 插件、Git 与 PR 署名等。

---

<p align="center">
  <small>© 2026 DMXAPI Cladue Code</small>
</p>