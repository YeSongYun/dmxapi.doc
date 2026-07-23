# Openai Responses 接口图片分析 API 文档

本 API 支持文本和图像的多模态输入，可用于图像内容描述等场景。以下示例使用 `gpt-5.6-sol-ssvip` 模型，通过图片 URL（`input_image`）传入待分析的网络图片。

## 请求地址

```
https://www.dmxapi.cn/v1/responses
```

## Python 调用示例

```python
"""
================================================================
DMXAPI 多模态图片识别示例（Responses 接口）
================================================================
功能说明：
    本脚本演示如何使用 DMXAPI 的 responses 接口进行网络图片内容识别。
    支持通过 URL 方式传入图片，让 AI 模型分析并描述图片内容。

作者：DMXAPI 团队
================================================================
"""

import json
import requests

# ========================================
# API 配置信息
# ========================================
# 你的 DMXAPI 密钥（请替换为真实密钥）
API_KEY = "sk-***************************"

# DMXAPI 请求地址
url = "https://www.dmxapi.cn/v1/responses"

# ========================================
# 构建请求头
# ========================================
headers = {
    "Content-Type": "application/json",           # 指定请求内容类型为 JSON
    "Authorization": f"{API_KEY}"                 # 携带 API 密钥进行身份验证
}

# ========================================
# 构建请求体
# ========================================
payload = {
    "model": "gpt-5.6-sol-ssvip",                 # 指定使用的 AI 模型
    "input": [                                    # 输入消息数组
        {
            "role": "user",                       # 消息角色：用户
            "content": [                          # 多模态内容数组
                {
                    "type": "input_text",         # 内容类型：文本
                    "text": "分析这个图片"          # 用户的文本提示
                },
                {
                    "type": "input_image",        # 内容类型：图片
                    "image_url": "https://fenxiang.yesongyun.com/fapiao.png"  # 图片 URL 地址
                },
            ],
        }
    ],
}

# ========================================
# 发送 API 请求并处理响应
# ========================================
try:
    # 发送 POST 请求到 API 服务器
    response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=120)

    # 检查 HTTP 响应状态码，如果出错会抛出异常
    response.raise_for_status()

    # ========================================
    # 输出成功结果
    # ========================================
    print("✅ 请求成功!")
    print("=" * 60)
    print("API 返回结果：")
    print("=" * 60)
    # 格式化输出 JSON 响应结果（保持中文显示）
    print(json.dumps(response.json(), indent=4, ensure_ascii=False))

except requests.exceptions.RequestException as e:
    # 捕获网络请求相关的所有异常（连接错误、超时、HTTP 错误等）
    print(f"❌ 请求失败: {e}")
except ValueError as e:
    # 捕获 JSON 解析错误等值相关的异常
    print(f"❌ 数据解析错误: {e}")
```

## 响应示例

成功响应将返回 JSON 格式数据，`output` 数组中 `type` 为 `message` 的元素里包含模型生成的描述内容（`output_text`）。

```json
✅ 请求成功!
============================================================
API 返回结果：
============================================================
{
    "id": "resp_088a8ead782dc421006a60b2692a1481968cff9d7e9aa96d74",
    "object": "response",
    "created_at": 1784722027,
    "status": "completed",
    "model": "gpt-5.6-sol-ssvip",
    "output": [
        {
            "id": "rs_088a8ead782dc421006a60b26cb5688196922485f444dc0833",
            "type": "reasoning",
            "content": [],
            "summary": []
        },
        {
            "id": "msg_088a8ead782dc421006a60b273a1f881968104ec5af4b2cf18",
            "type": "message",
            "status": "completed",
            "content": [
                {
                    "type": "output_text",
                    "annotations": [],
                    "logprobs": [],
                    "text": "这是一张**电子发票（普通发票）**截图，部分敏感信息已被打码。\n\n### 票面信息\n- **开票日期**：2026年06月01日\n- **发票号码**：以“26312…”开头，后半部分被遮挡\n- **购买方/销售方**：名称及统一社会信用代码大部分被遮挡\n- **项目名称**：`*生产生活服务*技术服务费`\n- **数量**：1\n- **不含税单价**：943.396226415094 元\n- **不含税金额**：943.40 元\n- **税率**：6%\n- **税额**：56.60 元\n- **价税合计**：1000.00 元\n- **大写金额**：壹仟圆整\n- **下载次数**：1\n\n### 金额核对\n计算关系基本正确：\n\n- 943.40 × 6% ≈ 56.60 元\n- 943.40 + 56.60 = 1000.00 元\n\n单价保留了较多小数，但金额栏按人民币规则四舍五入到两位小数，属于常见情况。\n\n### 需要注意\n1. **日期异常风险**：票面日期为2026年06月01日；如果核验时间早于该日期，则属于未来日期，需要重点确认。\n2. 图片中的二维码、完整发票号码和购销双方税号均被遮挡，因此**无法仅凭截图判断真伪**。\n3. 红色监制章及版式看起来符合常见数电票/电子普通发票样式，但版式正常不等于发票真实有效。\n4. 建议使用税务机关的**全国增值税发票查验平台**，输入完整发票号码、开票日期、金额等信息核验，并确认销售方名称、税号及业务内容与实际交易一致。"
                }
            ],
            "role": "assistant"
        }
    ],
    "reasoning": {
        "effort": "medium",
        "summary": null
    },
    "service_tier": "priority",
    "store": true,
    "temperature": 1.0,
    "text": {
        "format": {
            "type": "text"
        },
        "verbosity": "medium"
    },
    "usage": {
        "input_tokens": 520,
        "input_tokens_details": {
            "cached_tokens": 0
        },
        "output_tokens": 956,
        "output_tokens_details": {
            "reasoning_tokens": 516
        },
        "total_tokens": 1476
    },
    "metadata": {}
}
```

## ⚠️ 注意事项

- `image_url` 需为公网可访问的图片直链地址
- 请妥善保管您的 API 密钥，不要将其暴露在公开代码中
- 模型返回内容位于 `output` 数组中 `type` 为 `message` 的元素内，解析时请先过滤 `type == "reasoning"` 的元素
- 图片较大或网络较慢时，建议适当调大 `timeout`

<p align="center">
  <small>© 2025 DMXAPI Openai 网络图片分析</small>
</p>
