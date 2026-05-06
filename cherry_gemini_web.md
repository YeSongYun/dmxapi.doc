# Cherry Studio 使用 Gemini 模型联网搜索教程

本教程介绍如何在 Cherry Studio 中接入 DMXAPI 的 Gemini文本模型，并启用其原生联网搜索能力。完成配置后，Gemini 会自动判断是否需要检索最新信息，并在回答中附带可点击的引用来源，适用于查询实时新闻、价格行情、最新政策等需要最新数据的场景。

## 第一步 打开设置，添加新的模型提供商

点击 Cherry Studio 右上角「设置」按钮 

![Cherry使用gemini网络搜索教程](img\cherry_gemini_web01.png)

## 第二步 填写提供商信息

在弹窗中填写提供商名称，提供商类型选择 `Gemini` 。

![Cherry使用gemini网络搜索教程](img\cherry_gemini_web02.png)

## 第三步 填写 API 地址和 Key

- **自定义请求地址**：根据您所使用的站点填写
  - cn 站：`https://www.dmxapi.cn`
  - com 站：`https://www.dmxapi.com`
  - ssvip 站：`https://ssvip.dmxapi.com`
- API 密钥：填入您的 DMXAPI 令牌 
- 点击加号手动添加模型 

![Cherry使用gemini网络搜索教程](img\cherry_gemini_web03.png)

## 第四步 在对话窗口选择 Gemini 模型

回到对话界面，点击顶部模型选择器，搜索刚刚手动添加的gemini模型，**注意要选择刚刚添加的 Gemini 格式提供商**（如示例中的 `dmx-gemini`）下的模型，而不是 OpenAI 格式或 Response 格式提供商下的同名模型。只有 Gemini 原生格式才能触发模型内置的联网搜索能力。

![Cherry使用gemini网络搜索教程](img\cherry_gemini_web04.png)

## 第五步 开启「网络搜索」并选择「模型内置」

在输入框下方点击 🌐 网络搜索图标，在弹出的搜索源列表中选择 **「模型内置」**。这会让 Gemini 使用自身的联网搜索功能，由模型自动判断检索时机和关键词，效果优于第三方搜索引擎方案。

![Cherry使用gemini网络搜索教程](img\cherry_gemini_web05.png)

## 第六步 输入问题，查看带引用的搜索结果

直接输入需要最新信息的问题，例如「今日油价」「最近的科技新闻」等。Gemini 会自动联网检索，并在回答末尾给出引用来源（点击可跳转原网页）。

![Cherry使用gemini网络搜索教程](img\cherry_gemini_web06.png)


<p align="center">
  <small>© 2026 Cherry Studio 使用 Gemini 模型联网搜索教程</small>
</p>
