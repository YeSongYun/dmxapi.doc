# Doubao 豆包模型思考功能参数说明

## 📖 概念介绍

思考功能(thinking)是豆包模型的一个特性参数，用于控制模型在响应前是否显示思考过程。该功能适用于需要观察模型推理过程的场景。

## ⚙️ 思考参数配置

| 参数值 | 说明 |
|--------|------|
| `enabled` | 强制开启思考过程 |
| `disabled` | 强制关闭思考过程 |
| `auto` | 由模型自动决定是否显示思考过程 |

## 🔌 API 接口

**请求方法**: `POST`

**Base URL**: `https://www.dmxapi.cn/v1/chat/completions`

## 💻 示例代码

```python
import json
import requests

# 配置 API 密钥
api_key = "sk-**************"  # 替换为你的 DMXAPI 令牌
url = "https://www.dmxapi.cn/v1/chat/completions"

# 设置请求头
headers = {
    "Authorization": f"{api_key}",
    "Content-Type": "application/json"
}

# 构造请求数据
data = {
    "model": "doubao-seed-1-6-250615",  # 指定模型版本
    "messages": [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "从1加到10等于多少？"  # 用户提问
                }
            ]
        }
    ],
    "thinking": {"type": "enabled"}  # 开启思考功能，可选: enabled / disabled / auto
}

try:
    # 发送 API 请求
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()  # 检查 HTTP 错误

    # 处理响应结果
    print("请求成功!")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))

except requests.exceptions.RequestException as e:
    # 异常处理
    print(f"请求失败: {e}")
```

## ⚠️ 注意事项

1. 思考功能会增加少量响应时间
2. 对于简单问题建议使用 `disabled` 或 `auto` 模式
3. 复杂推理问题使用 `enabled` 模式可获得更好的可解释性

---

<p align="center">
  <small>© 2025 DMXAPI Doubao thinking</small>
</p>