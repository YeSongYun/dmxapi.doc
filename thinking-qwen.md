# Qwen 关于"思考"功能的参数说明

::: warning 注意
仅在您确定需要使用此功能时再查看本文档
:::

## 推理思考概念介绍

思考功能允许 AI 在生成最终回答前展示其推理过程。通过配置思考参数，可以控制 AI 的思考深度和输出方式。

::: tip 官方文档
[阿里云 - 深度思考功能文档](https://help.aliyun.com/zh/model-studio/deep-thinking?spm=a2c4g.11186623.0.0.78d84823pcyZsz#1dd26768ddaua)
:::

## 推理思考参数

| 参数配置 | 类型 | 说明 |
|---------|------|------|
| `enable_thinking` | 布尔值 | 激活/禁用 Qwen3 模型的逐步推理功能，默认值建议为 `True` |
| `thinking_budget` | 整数 | 限制单次推理过程允许使用的最大 Token 数量（例如 `2048`），防止资源过度消耗 |

## 支持的主流 Qwen 模型

`enable_thinking` 参数开启思考过程，`thinking_budget` 参数设置最大推理过程 Token 数。

::: warning 重要提示
这两个参数对 **QwQ 模型无效**
:::

### 使用示例

```json
extra_body={
    "enable_thinking": true,
    "thinking_budget": 50
}
```

---

<p align="center">
  <small>© 2025 DMXAPI 千问 thinking</small>
</p>