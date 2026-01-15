# Claude Code 接入指南 & 详细指令教程

::: tip
编程插件tokens消耗量很大，请注意tokens消耗
:::
在开始之前，请先安装并验证以下基础环境：

- Node.js（含 `npm`），推荐 `v18+`：<https://nodejs.org/>
- Git（建议 `v2.40+`）：<https://git-scm.com/>

验证安装是否成功：

```bash
node -v
npm -v
git --version
```
### cc switch优点

可以切换其他模型！  
图像化配置，无需手动设置环境变量！

## 第一步：安装 Claude Code

```bash
# windows 建议在 管理员权限PowerShell 里使用
npm install -g @anthropic-ai/claude-code
# 查看版本 验证安装成功
claude --version
```

## 第二步：使用cc switch配置claude code

请前往 [cc_switch](/cc_switch) 查看详细配置说明。

### cc switch优点

可以切换其他模型！  
图像化配置，无需手动设置环境变量！

## 第三步：在vs code中配置 claude code
 1、在vs code 中安装claude code插件。
![claude-code](img\cc-switch06.png)

 2、在vs code 中对claude code插件进行设置。
![claude-code](img\cc-switch07.png)
 3、在vs code 中开启claude code插件的相关选项。
![claude-code](img\cc-switch08.png)



## Claude Code 疑难杂症汇总

### 🌈✨powershell 无法启动claude

这是 PowerShell 的“脚本执行策略”在阻止你运行 claude.ps1，不是 Claude 本身出问题。
运行下面代码即可
```bash
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```
### Claude Code 在跳过地区限制的解决方案

claude code 跳过地区限制的解决方案。（mac和Windows用户通用，mac用户比较容易出现这个问题），解决方案为：在cc switch中添加参数【"hasCompletedOnboarding":true】，具体操作如下。

### 1. 点击编辑按钮，开始配置cc switch

![claude-code](img\1-4-1.jpg)

### 2. 点击“编辑通用配置选项”

![claude-code](img\1-7-9.png)

### 3. 添加新的参数

新参数："hasCompletedOnboarding":true

![claude-code](img\1-4-3.jpg)

### 4. 保存配置，然后重启claude code就好啦！！！

### ✈️✨Claude Code 在cc switch中配置key但是没有生效的解决方案
需要配置系统环境变量，具体步骤如下：

### 配置系统环境变量(新方法)
用户可以根据自己的使用情况，选择合适的指令。


Windows PowerShell（推荐）:
```
$wc = New-Object System.Net.WebClient; $wc.Encoding = [System.Text.Encoding]::UTF8; iex $wc.DownloadString('https://doc.dmxapi.cn/0_fenxiang/dmxapi-claude-code.ps1')
```

Windows CMD:
```
powershell -ExecutionPolicy Bypass -c "$wc = New-Object System.Net.WebClient; $wc.Encoding = [System.Text.Encoding]::UTF8; iex $wc.DownloadString('https://doc.dmxapi.cn/0_fenxiang/dmxapi-claude-code.ps1')"
```
macOS / Linux:

```
curl -fsSL https://doc.dmxapi.cn/0_fenxiang/dmxapi-claude-code.sh | sh
```

### 配置系统环境变量(旧方法)

### 1. 在搜索栏中搜索：配置系统环境变量  

![claude-code](img\1.png)

### 2. 进入系统环境变量配置界面

![claude-code](img\2.png)

### 3. 找到变量建立位置

![claude-code](img\3.png)

### 4. 新建系统环境变量

![claude-code](img\4.png)

### 5. 输入变量名和变量值，然后保存
变量名称：ANTHROPIC_AUTH_TOKEN，变量值：sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx（您在DMXAPI申请的访问令牌）

![claude-code](img\5.png)

### 6. 重启Claude Code
重启Claude code以后就可以愉快的使用啦！！！

---

<p align="center">
  <small>© 2025 DMXAPI Cladue Code</small>
</p>