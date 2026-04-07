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


## 第一步：下载安装配置工具

配置工具开源仓库地址：

- cnb：https://cnb.cool/dmxapi/dmxapi_claude_code
- GitHub：https://github.com/YeSongYun/dmxapi-claude-code

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
若以上命令执行失败，请参阅文末「方式二：手动下载」进行手动安装。
:::


## 第二步：运行配置

#### 1、进入配置界面的模式选择
![claude-code](img\1-20-19.png)
> 这里我们第一次配置，选择第一项    

![claude-code](img\1-20-15.png)

#### 2、填写Base URL
![claude-code](img\1-20-16.png)

#### 3、填写正确的key
![claude-code](img\1-20-17.png)

#### 4、配置模型并保存退出
![claude-code](img\1-20-18.png)
:::tip 注意
claude code 只能配置模型广场中claude code 专区的后缀为-cc的模型，其他的不可用
:::

#### 5、重新打开一个终端，输出claude ，打开claude code
![claude-code](img\1-20-22.png)

#### 6、选择Yes，proceed

这一步之前有的用户会出现背景颜色的确认，根据自己喜欢的风格选择后就到这一步了。
![claude-code](img\1-20-23.png)

#### 7、在对话框中输入”你好”，回车
![claude-code](img\1-20-24.png)

#### 8、模型响应成功，可以开始使用了。
![claude-code](img\1-20-25.png)




## 📦 方式二：手动下载

> 适用于快速安装脚本无法运行的情况。

#### 1、复制cnb仓库地址，在浏览器中打开。
![claude-code](img\1-20-8.png)

#### 2、点击最新版插件链接，跳转到下载界面
![claude-code](img\1-20-9.png)

#### 3、根据自己的操作系统，选择合适的插件
![claude-code](img\1-20-10.png)

#### 4、下载完成
windows用户下载完成后可以直接点击运行，开始配置，可以直接跳到第二步，其他操作系统用户需要先给文件添加运行权限，然后再运行。
![claude-code](img\1-20-13.png)

#### 5、安装之前，添加运行权限（Windows可以直接双击使用）
![claude-code](img\1-20-14.png)

---

<p align="center">
  <small>© 2026 DMXAPI Cladue Code</small>
</p>