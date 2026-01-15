# Gemini 官方 API 思考功能参数说明

:::tip 核心特点
和 Claude 不同，默认情况下 Gemini 的思考模型会自动决定是否思考，就算不开启适配模型也可以正常使用。
:::

## 📖 推理思考概念介绍

思考功能允许 AI 在生成最终回答前展示其推理过程。通过配置思考参数，可以控制 AI 的思考深度和输出方式。

## ⚙️ 如何开关思考及控制思考预算？

为了更方便的使用，我们直接用模型 ID 后缀增加 `-thinking` 和 `-nothinking` 进行开启和关闭**思考**功能。

| 后缀 | 功能说明 |
|------|---------|
| `-thinking` | 打开并展示思考过程 |
| `-nothinking` | 关闭思考过程，回复更快，更省 token |

## 🤖 支持的 Gemini 模型

```
gemini-2.5-flash-nothinking
gemini-2.5-flash-thinking
gemini-2.5-pro-thinking
```

## ⚠️ 注意事项

- 和 Claude 不同，默认情况下 Gemini 的思考模型会自动决定是否思考
- `gemini-2.5-pro` 默认无法关闭思考和不展示思考过程，`-thinking` 只是让其展示思考过程

---

<p align="center">
  <small>© 2025 DMXAPI Gemini thinking</small>
</p>