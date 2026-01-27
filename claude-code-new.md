# Claude Code（推荐）
DMXAPI研发的一键配置 Anthropic Claude Code CLI 环境变量的跨平台工具。

## 功能特性

    - 交互式配置 API 地址和认证令牌
    - 自动验证 API 连接有效性
    - 配置默认模型设置
    - 支持 Windows / Linux / macOS
    - 环境变量自动持久化

## 配置工具的下载仓库地址

::: tip 提示
通过下面的仓库地址，下载claude code 的配置工具
:::
cnb开源仓库地址：

https://cnb.cool/dmxapi/dmxapi_claude_code

github仓库地址：

https://github.com/YeSongYun/dmxapi-claude-code


:::warning 注意
编程插件tokens消耗量很大，请注意tokens消耗
:::

## 环境准备
在开始之前，请先安装并验证以下基础环境：

- Node.js（含 `npm`），推荐 `v18+`：<https://nodejs.org/>
- Git（建议 `v2.40+`）：<https://git-scm.com/>

验证安装是否成功：

```bash
node -v
npm -v
git --version
```

## 使用方法
使用之前，请先根据自己的操作系统情况 ，添加执行权限（Windows用户可以直接双击打开）
:::warning 注意
claude code 只能配置模型广场中claude code 专区的后缀为-cc的模型，其他的不可用
:::
### Windows
```
.\dmxapi-claude-code.exe
```

### Linux
```
# 添加执行权限
chmod +x dmxapi-claude-code-linux-amd64

# 运行
./dmxapi-claude-code-linux-amd64

```

### macOS
```
# 添加执行权限

chmod +x dmxapi-claude-code-macos-arm64


# 运行（首次可能需要在"系统设置 > 隐私与安全性"中允许）

./dmxapi-claude-code-macos-arm64
```


## 第一步：安装 Claude Code

```bash
# windows 建议在 管理员权限PowerShell 里使用
npm install -g @anthropic-ai/claude-code
# 查看版本 验证安装成功
claude --version
```

## 第二步：使用 DMXAPI 开发的插件配置 claude code

### 1、复制cnb仓库地址，在浏览器中打开。
![claude-code](img\1-20-8.png)

### 2、点击最新版插件链接，跳转到下载界面
![claude-code](img\1-20-9.png)

### 3、根据自己的操作系统，选择合适的插件，复制下载链接
![claude-code](img\1-20-10.png)

### 4、在浏览器中打开下载链接，下载插件
![claude-code](img\1-20-11.png)

### 5、下载完成
![claude-code](img\1-20-13.png)

### 6、安装之前，添加运行权限（Windows可以直接双击使用）
![claude-code](img\1-20-14.png)

### 7、进入配置界面
![claude-code](img\1-20-15.png)

### 8、填写url
![claude-code](img\1-20-16.png)

### 9、选择更新配置
![claude-code](img\1-20-17.png)

### 10、填写自己的key
![claude-code](img\1-20-18.png)

### 11、声明
因为之前配置过一次，所以会留存一些模型名称,用户下载claude code 第一次配置不会出现这部分内容，直接从默认模型开始配置。
![claude-code](img\1-20-19.png)

### 12、配置模型
:::tip 注意
claude code 只能配置模型广场中claude code 专区的后缀为-cc的模型，其他的不可用
:::
![claude-code](img\1-20-20.png)

### 13、配置成功，按回车退出配置界面
![claude-code](img\1-20-21.png)

### 14、重新打开一个终端，输出claude ，打开claude code
![claude-code](img\1-20-22.png)

### 15、选择Yes，proceed

这一步之前有的用户会出现背景颜色的确认，根据自己喜欢的风格选择后就到这一步了。
![claude-code](img\1-20-23.png)

### 16、在对话框中输入“你好”，回车
![claude-code](img\1-20-24.png)

### 17、模型响应成功，可以开始使用了。
![claude-code](img\1-20-25.png)






## Claude Code 疑难杂症汇总

### 🌈✨powershell 无法启动claude

这是 PowerShell 的“脚本执行策略”在阻止你运行 claude.ps1，不是 Claude 本身出问题。
运行下面代码即可
```bash
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```


---

<p align="center">
  <small>© 2025 DMXAPI Cladue Code</small>
</p>