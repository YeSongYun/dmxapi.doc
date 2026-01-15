# Openai Responses 接口图片分析 API 文档

本 API 支持文本和图像的多模态输入，可用于图像内容描述等场景。

## 请求地址

```
https://www.dmxapi.cn/v1/responses
```

## Python 调用示例

```python
"""
================================================================
DMX API 多模态图片识别示例
================================================================
功能说明：
    本脚本演示如何使用 DMX API 的 responses 接口进行图片内容识别。
    支持通过 URL 方式传入图片，让 AI 模型分析并描述图片内容。

作者：DMX API 团队
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
    "Authorization": f"{API_KEY}"          # 携带 API 密钥进行身份验证
}

# ========================================
# 构建请求体
# ========================================
payload = {
    "model": "gpt-5-mini",                          # 指定使用的 AI 模型
    "input": [                                    # 输入消息数组
        {
            "role": "user",                       # 消息角色：用户
            "content": [                          # 多模态内容数组
                {
                    "type": "input_text",         # 内容类型：文本
                    "text": "描述这张图片中的内容"  # 用户的文本提示
                },
                {
                    "type": "input_image",        # 内容类型：图片
                    "image_url": "https://doc.dmxapi.cn/example.jpg"  # 图片 URL 地址
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
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    
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

成功响应将返回 JSON 格式数据，包含模型生成的描述内容。

```json
✅ 请求成功!
============================================================
API 返回结果：
============================================================
{
    "id": "resp_0c3b7023f672732800690dd29dad188193b19186da03efc2c6",
    "object": "response",
    "model": "gpt-5-mini-2025-08-07",
    "usage": {
        "total_tokens": 1473,
        "input_tokens": 935,
        "input_tokens_details": {
            "cached_tokens": 0
        },
        "output_tokens": 538,
        "output_tokens_details": {
            "reasoning_tokens": 192
        }
    },
    "created_at": 1762513567,
    "status": "completed",
    "background": false,
    "content_filters": null,
    "error": null,
    "incomplete_details": null,
    "instructions": null,
    "max_output_tokens": null,
    "max_tool_calls": null,
    "output": [
        {
            "id": "rs_0c3b7023f672732800690dd2a26558819393b160a7957f6676",
            "type": "reasoning",
            "summary": []
        },
        {
            "id": "msg_0c3b7023f672732800690dd2a5bd80819399ed4b2013fa37f7",
            "type": "message",
            "status": "completed",
            "content": [
                {
                    "type": "output_text",
                    "annotations": [],
                    "logprobs": [],
                    "text": "这是一张台式计算器的近拍照片，主要内容和细节包括：\n\n- 品牌与型号：左上角有“Canon”标志，型号写作 WS‑1212H（显示器右上角还有“12”字样，表示12位数显示）。\n- 计算器外观：浅灰/白色机身，顶部有一块较大 的液晶显示屏，显示区下方有两个滑动开关（用于小数位和舍入设置）。\n- 按键布局：标准数字键盘（0–9），左下有红色的开机/清除键（ON/CA 和 C/CE），有“00”和小数点键；上排有 MU、GT、CM、RM、M±、M＝等记忆/功能键；右侧有加、减、乘、除、 等号、百分号、开方符号等运算键。\n- 颜色与材质：按键多为灰色系，功能键和数字键色调稍有区分，机身为塑料材质。\n- 周围环境：计算器放在带有蓝色、黄色花纹的大布或鼠标垫上，右上角有一块浅绿色毛巾，左上角可见一段黑色线缆和一个 USB 接头以及一个浅色小包/收纳袋的一角。\n\n整体画面为俯视拍摄，焦点在计算器正面按键和显示屏区域，光线均匀，有少量反光。"
                }
            ],
            "role": "assistant"
        }
    ],
    "parallel_tool_calls": true,
    "previous_response_id": null,
    "prompt_cache_key": null,
    "reasoning": {
        "effort": "medium",
        "summary": null
    },
    "safety_identifier": null,
    "service_tier": "default",
    "store": true,
    "temperature": 1.0,
    "text": {
        "format": {
            "type": "text"
        },
        "verbosity": "medium"
    },
    "tool_choice": "auto",
    "tools": [],
    "top_logprobs": 0,
    "top_p": 1.0,
    "truncation": "disabled",
    "user": null,
    "metadata": {}
}
```

<p align="center">
  <small>© 2025 DMXAPI Openai 网络图片分析</small>
</p>