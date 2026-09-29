# Cherry Studio 移动端手动配置
本文介绍如何在 Cherry Studio 移动端直接填写 DMXAPI 的 API 密钥完成配置，无需连接桌面端。如果您已经在桌面端配置好 DMXAPI，也可以参考 [Cherry Studio 移动端同步桌面端配置](/cherry-studio-mobile-sync) 直接同步。

::: tip 开始前准备
请先在 DMXAPI 官网获取 API 令牌，获取方法可参考 [Cherry Studio 快速开始](/cherry-studio-fast-start) 中的「获取 DMXAPI 令牌」。
:::

## 快速开始
### 第一步 同意隐私与数据
打开 Cherry Studio 移动端，在 **隐私与数据** 弹窗中点击 **同意并继续**。
<img src="./img/cherry-studio-mobile-manual-config1.png" alt="" width="355">

### 第二步 连接服务商
在欢迎页点击 **连接服务商**。
<img src="./img/cherry-studio-mobile-manual-config2.png" alt="" width="355">

### 第三步 选择 DMXAPI
1. 在搜索框中输入 `dmxapi`  
2. 选择 **DMXAPI**
<img src="./img/cherry-studio-mobile-manual-config3.png" alt="" width="355">

### 第四步 添加密钥
点击 **添加密钥**。服务地址已自动填写，如需修改，可打开 **高级设置**。
<img src="./img/cherry-studio-mobile-manual-config4.png" alt="" width="355">

### 第五步 填写 API Key
1. 填入 DMXAPI 的 API Key  
2. 填写备注（可选），例如 `DMXAPI`  
3. 点击 **添加密钥**
<img src="./img/cherry-studio-mobile-manual-config5.png" alt="" width="355">

### 第六步 启用密钥并保存
1. 确认密钥右侧的开关已开启（绿色），未开启时点击开启  
2. 点击 **保存并继续**
<img src="./img/cherry-studio-mobile-manual-config6.png" alt="" width="355">

### 第七步 搜索模型
在 **选择聊天模型** 页面，通过顶部搜索框搜索模型。
<img src="./img/cherry-studio-mobile-manual-config7.png" alt="" width="355">

### 第八步 选择模型并开始聊天
1. 输入完整模型名称，例如 `deepseek-v4.1-flash`  
2. 选择模型  
3. 点击 **开始聊天**

开始前会检查连接，可能产生少量费用。
<img src="./img/cherry-studio-mobile-manual-config8.png" alt="" width="355">

### 第九步 输入问题
在底部输入框输入文本开始对话，例如「你好」。
<img src="./img/cherry-studio-mobile-manual-config9.png" alt="" width="355">

### 第十步 查看回复
可以看到模型的回复，说明配置成功。
<img src="./img/cherry-studio-mobile-manual-config10.png" alt="" width="355">

## 更新模型列表
### 第一步 进入设置
点击聊天页左上角的侧边栏图标打开菜单，然后点击菜单底部的头像。
<img src="./img/cherry-studio-mobile-manual-config11.png" alt="" width="355">

### 第二步 进入模型服务
点击 **模型服务**，这里用来添加模型服务商。
<img src="./img/cherry-studio-mobile-manual-config12.png" alt="" width="355">

### 第三步 更新模型列表
在 **模型服务** 列表中点击 **DMXAPI**，进入服务商页面后：
1. 切换到 **模型** 标签  
2. 点击右上角的刷新图标更新模型列表
<img src="./img/cherry-studio-mobile-manual-config13.png" alt="" width="355">

### 第四步 同步模型
1. 点击 **全选**，也可以按需勾选  
2. 点击右上角的 **更新**
<img src="./img/cherry-studio-mobile-manual-config14.png" alt="" width="355">

## 进阶配置：选择模型格式
通过新建自定义服务商并填写多个协议端点，可以为不同模型切换调用协议（OpenAI Chat、Anthropic、OpenAI Responses、Gemini）。

### 第一步 新增模型服务商
按上文「更新模型列表」的第一、二步进入 **模型服务** 页面，然后：
1. 点击右上角的 **···**  
2. 选择 **新增模型服务商**
<img src="./img/cherry-studio-mobile-manual-config15.png" alt="" width="355">

### 第二步 创建自定义服务商
在 **自定义服务商** 右侧点击 **创建**。
<img src="./img/cherry-studio-mobile-manual-config16.png" alt="" width="355">

### 第三步 填写服务商信息
1. 填写提供商名称，例如 `DMXAPI-CN`  
2. 点击 **添加密钥**，在弹出的窗口中填写 API Key（见下一步）  
3. 在 **OpenAI Chat** 和 **Anthropic** 端点的输入框中填写 `https://www.dmxapi.cn`
<img src="./img/cherry-studio-mobile-manual-config17.png" alt="" width="355">

### 第四步 填写 API Key
1. 填入 DMXAPI 的 API Key  
2. 填写备注（可选），例如 `DMXAPI`  
3. 点击 **添加密钥**
<img src="./img/cherry-studio-mobile-manual-config18.png" alt="" width="355">

### 第五步 填写全部端点
1. 展开 **更多端点**，将 **OpenAI Chat**、**Anthropic**、**OpenAI Responses**、**Gemini** 四个端点的输入框都填写为 `https://www.dmxapi.cn`  
2. 点击 **保存并继续**
<img src="./img/cherry-studio-mobile-manual-config19.png" alt="" width="355">

### 第六步 同步模型
在 **同步模型** 页面选择要添加的模型，有两种方式：
- 点击 **全选** 添加全部模型，然后点击右上角的 **完成配置**
- 在搜索框中搜索，只添加需要的模型（见下一步）
<img src="./img/cherry-studio-mobile-manual-config20.png" alt="" width="355">

### 第七步 精准添加模型（可选）
1. 在搜索框中输入模型名称，例如 `deepseek-v4.1-flash`  
2. 勾选模型  
3. 点击 **完成配置**
<img src="./img/cherry-studio-mobile-manual-config21.png" alt="" width="355">

### 第八步 进入刚配置的服务商
在 **模型服务** 页面点击刚配置的服务商，例如 **DMXAPI-CN**。
<img src="./img/cherry-studio-mobile-manual-config22.png" alt="" width="355">

### 第九步 找到模型格式设置
1. 切换到 **模型** 标签  
2. 点击模型右侧的 **默认 · OpenAI Chat**
<img src="./img/cherry-studio-mobile-manual-config23.png" alt="" width="355">

### 第十步 选择模型格式
在 **调用协议** 中选择需要的模型格式：**OpenAI Chat**、**Anthropic**、**OpenAI Responses** 或 **Gemini**。默认为「跟随服务商默认」。
<img src="./img/cherry-studio-mobile-manual-config24.png" alt="" width="355">

::: tip 如何选择模型格式
不同系列的模型适用的格式，可参考 [Cherry Studio 对话模型格式切换](/cherry-studio-model-format)。
:::

<p align="center">
  <small>© 2026 DMXAPI Cherry Studio 移动端手动配置</small>
</p>
