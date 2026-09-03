# Cherry Studio 对话模型格式切换
Cherry Studio 支持为同一服务商下的不同模型分别设置对话协议（OpenAI、OpenAI Responses、Anthropic、Gemini）。  

## 基础配置
### 第一步 添加服务商
打开 Cherry Studio 设置，进入 **模型服务**，点击底部的 **添加服务商**。
![](img/cherry-studio-new1.png)
### 第二步 选择头像
1. 点击 **内置头像**  
2. 搜索 **DMXAPI**  
3. 选择 DMXAPI 头像
![](img/cherry-studio-new2.png)
### 第三步 填写提供商信息
1. 填写提供商名称，例如 `DMXAPI-CN`  
2. 填写您的 DMXAPI 令牌  
3. 在端点设置的 OpenAI 一栏填入 API 地址，根据您注册的站点选择：
   - cn 站：`https://www.dmxapi.cn`
![](img/cherry-studio-new3.png)
### 第四步 填写其他协议端点
向下滚动，在 **Anthropic**、**OpenAI Responses**、**Gemini** 三栏中填入与上一步相同的 API 地址，随后点击 **添加**。
![](img/cherry-studio-new4.png)
### 第五步 启用服务商并获取模型列表

![](img/cherry-studio-new5.png)
### 第六步 添加模型
点击 **添加全部模型**，也可以按需单独添加。
![](img/cherry-studio-new6.png)

## 配置 Anthropic 格式模型
Claude 系列模型以及所有以 `-cc` 结尾的模型都需要切换到 Anthropic 格式。
### 第一步 搜索 Claude 模型
1. 在模型搜索框中输入要配置的 Claude 模型，例如 `claude-opus-5`  
2. 点击模型右侧的 **设置** 图标
![](img/cherry-studio-new13.png)
### 第二步 切换为 Anthropic 协议
1. 模型用途选择 **对话**  
2. 对话协议选择 **Anthropic**
![](img/cherry-studio-new14.png)
### 第三步 配置 -cc 结尾的模型
以 `-cc` 结尾的模型同样是 Anthropic 格式。  
1. 搜索要修改的模型，例如 `qwen3.8-max-cc`  
2. 点击模型右侧的 **设置** 图标
![](img/cherry-studio-new7.png)
### 第四步 切换协议
在对话协议中切换为 **Anthropic**。
![](img/cherry-studio-new8.png)

## 配置 OpenAI-Response 格式模型
GPT 系列模型建议使用 OpenAI Responses 格式。
### 第一步 搜索 GPT 模型
1. 在模型搜索框中输入对应的模型，例如 `gpt-5.6-sol`  
2. 点击模型右侧的 **设置** 图标
![](img/cherry-studio-new9.png)
### 第二步 切换为 OpenAI Responses 协议
1. 模型用途选择 **对话**  
2. 对话协议选择 **OpenAI Responses**
![](img/cherry-studio-new10.png)

## 配置 Gemini 格式模型
Gemini 系列模型需要切换到 Gemini 格式。
### 第一步 搜索 Gemini 模型
1. 在模型搜索框中输入对应的 Gemini 模型，例如 `gemini-3.8-flash`  
2. 点击模型右侧的 **设置** 图标
![](img/cherry-studio-new11.png)
### 第二步 切换为 Gemini 协议
1. 模型用途选择 **对话**  
2. 对话协议切换为 **Gemini**
![](img/cherry-studio-new12.png)

<p align="center">
  <small>© 2026 DMXAPI Cherry Studio 对话模型格式切换</small>
</p>
