# Somark 文档解析 API 文档
Somark，专为LLM而生的新一代智能文档解析模型，以卓越的准确性、闪电般的处理速度和极具竞争力的成本，将形态各异的文档——无论是PDF、Word、表格还是扫描图像——精准转化为LLM可直接理解与高效利用的纯净、结构化数据。我们致力于打通非结构化信息与智能模型之间的关键桥梁，让知识提取更简单，让AI的潜能充分释放。

## 📡 接口地址

```
https://www.dmxapi.cn/v1/responses
```

## 📝 支持的参数

支持类型：pdf、png、jpg、jpeg、bmp、tiff、jp2、dib、ppm、pgm、pbm、gif、heic、heif、webp、xpm、tga、dds、xbm。




## 💻 文档解析 示例代码
这里我们以PDF 解析为例。
```python
"""
╔═══════════════════════════════════════════════════════════════╗
║                  DMXAPI 自研接口 (文件上传版)                   ║
╚═══════════════════════════════════════════════════════════════╝

📝 功能说明:
   本脚本演示如何使用 requests 库调用 DMXAPI 的自研接口
   支持文件上传功能

═══════════════════════════════════════════════════════════════
"""
import requests
import json
import base64

# ═══════════════════════════════════════════════════════════════
# 🔑 步骤1: 配置 API 连接信息
# ═══════════════════════════════════════════════════════════════

# 🌐 DMXAPI 服务端点地址
url = "https://www.dmxapi.cn/v1/responses"

# 🔐 DMXAPI 密钥 (请替换为您自己的密钥)
# 获取方式: 登录 DMXAPI 官网 -> 个人中心 -> API 密钥管理
api_key = "sk-*****************************"

# ═══════════════════════════════════════════════════════════════
# 📁 步骤2: 配置文件路径
# ═══════════════════════════════════════════════════════════════

# 📄 要上传的文件路径 (请替换为实际文件路径)
file_path = "a.pdf"

# ═══════════════════════════════════════════════════════════════
# 📋 步骤3: 配置请求头
# ═══════════════════════════════════════════════════════════════

# 注意: 使用 JSON 方式发送数据，需要设置 Content-Type
headers = {
    "Authorization": f"{api_key}",    # token 认证方式
    "Content-Type": "application/json"
}

# ═══════════════════════════════════════════════════════════════
# 💬 步骤4: 配置请求参数
# ═══════════════════════════════════════════════════════════════

data = {
    "model": "somark",
    "input": "json"
}

# ═══════════════════════════════════════════════════════════════
# 📤 步骤5: 读取文件并发送请求
# ═══════════════════════════════════════════════════════════════

# 读取文件内容并转换为 base64 编码
with open(file_path, "rb") as f:
    file_content = f.read()
    file_base64 = base64.b64encode(file_content).decode("utf-8")

# 将 base64 编码的文件内容添加到请求数据中
data["file"] = file_base64

# 使用 JSON 方式发送 POST 请求
response = requests.post(url, headers=headers, json=data)

# 格式化输出 JSON 响应
# - indent=2: 缩进 2 空格，便于阅读
# - ensure_ascii=False: 正确显示中文字符
print(json.dumps(response.json(), indent=2, ensure_ascii=False))

```

## 📤 返回示例

```json
{
  "code": 0,
  "message": "ok",
  "data": {
    "task_id": "cff0add043204a7894c1884d82b836ed",
    "result": {
      "file_name": "260122125536496_93_debaca64c51d4e0d8cf3472e47b2e385.pdf",
      "imgs": [],
      "outputs": {
        "json": {
          "pages": [
            {
              "blocks": [
                {
                  "bbox": [
                    186,
                    153,
                    233,
                    180
                  ],
                  "captions": [],
                  "content": "你好",
                  "display": true,
                  "format": "text",
                  "idx": 1,
                  "img_url": "",
                  "type": "text"
                }
              ],
              "merge_content_from_pre_page": false,
              "page_num": 0,
              "page_size": {
                "h": 1754,
                "w": 1241
              }
            }
          ]
        }
      }
    },
    "error": null,
    "metadata": {
      "page_num": 1,
      "file_type": ".pdf"
    }
  },
  "usage": {
    "total_tokens": 1000,
    "input_tokens": 0,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 1000,
    "output_tokens_details": {
      "reasoning_tokens": 0
    }
  }
}
```



## ⚠️ 注意事项

- 请妥善保管您的 API Key,不要泄露给他人
- 流式输出适合需要实时展示响应内容的场景
- 确保网络连接稳定以获得最佳的流式体验

<p align="center">
  <small>© 2026 DMXAPI somark 文档解析</small>
</p>