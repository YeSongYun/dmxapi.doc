# Claude 思考参数说明

## 📚 快速开始

为了更方便的使用,我们在模型 ID 后缀增加 `-thinking` 和 `-nothinking` 就可以进行思考或者关闭思考了。

- **`-thinking`** - 打开并展示思考过程
- **`-nothinking`** - 关闭思考过程,回复更快,更省 token

---

## 💡 Claude 思考功能详细说明

### 概念介绍

思考功能允许 Claude 在给出最终答案前展示其推理过程。启用该功能需要预留至少 **1,024 个 token** 的预算空间,这些 token 将计入总 token 限制 (`max_tokens`)。

---

## 🎯 支持的模型

- `claude-haiku-4-5-20251001-thinking`
- `claude-opus-4-1-20250805-thinking`
- `claude-opus-4-20250514-thinking`

---

## ⚙️ 更深入的代码思考功能配置

> ⚠️ **注意**: 仅在您确定知道如何使用该功能时才使用以下参数。否则,您应该使用默认值。

### 配置参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `type` | string | ✅ 是 | 模式选择: `enabled`(启用) 或 `disabled`(禁用) |
| `budget_tokens` | integer | ⚠️ 启用时必填 | 分配给推理过程的 token 数量,必须 ≥1024 且 < max_tokens |

### 1️⃣ 启用模式 (-thinking 对应参数)

```json
{
  "type": "enabled",
  "budget_tokens": 2048
}
```

### 2️⃣ 禁用模式

```json
{
  "type": "disabled"
}
```

---

<p align="center">
  <small>© 2025 DMXAPI Claude thinking</small>
</p>