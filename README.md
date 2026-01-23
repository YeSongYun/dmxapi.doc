# DMXAPI 文档

DMXAPI 大模型API聚合平台的官方文档站点。

**在线访问**：[doc.dmxapi.cn](https://doc.dmxapi.cn)

## 快速开始

### 环境要求

- Node.js 18+

### 安装依赖

```bash
npm install
```

### 本地开发

```bash
npm run docs:dev
```

访问 `http://localhost:5173` 查看文档站点。

### 生产构建

```bash
npm run docs:build
```

构建产物输出到 `.vitepress/dist` 目录。

### 预览构建结果

```bash
npm run docs:preview
```

## 项目结构

```
cn.doc/
├── .vitepress/
│   ├── config.mts          # VitePress 配置文件
│   ├── theme/              # 主题配置
│   └── dist/               # 构建输出目录
├── img/                    # 文档图片资源
├── public/                 # 静态资源
├── index.md                # 首页
└── *.md                    # 文档页面
```

## 文档内容

### 平台接口

- 余额查询、令牌管理、模型列表
- 模型统计、日志查询、消耗明细

### API 调用指南

- **OpenAI 格式**：文本对话、流式输出、图片分析、函数调用、TTS/STT
- **Gemini 格式**：文本、PDF/视频/音频分析、联网搜索
- **Claude 格式**：文本对话、图片分析、函数调用、缓存

### 多模态模型

- **绘图**：OpenAI DALL-E、豆包梦想、Gemini、Flux、百度
- **视频**：MiniMax 海螺、Sora2、Vidu、Kling
- **音频**：TTS、STT (Whisper、GPT-4o)
- **音乐**：Suno、MiniMax-music

### 第三方应用集成

Claude Code、Cherry Studio、Dify、Coze、ChatBox、VSCode Cline、Cursor 等

## 许可证

Copyright © DMXAPI
