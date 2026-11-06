# doubao-seedream-5-0-flash-260915 文生图 API 使用文档

基于字节跳动豆包 Doubao Seedream 5.0 Flash 模型的文生图接口，通过 `/v1/responses` 端点同步调用，根据输入的文本提示词直接生成单张图片。尺寸控制支持 `1K`/`1.5K`/`2K` 分辨率档位与精确宽高像素值（总像素范围 921600~4624220、宽高比范围 [1/16, 16]）两种方式，输出格式可选 `png`/`jpeg`，返回方式支持图片 URL（24 小时内有效）或 Base64 编码。提示词支持中英文，建议不超过 300 个汉字或 600 个英文单词，适合人像摄影、海报设计、艺术创作等高质量图像生成场景。

## 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 图像生成 | POST | `https://www.dmxapi.cn/v1/responses` |



:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。如果怀疑密钥已泄露，请立即前往 DMXAPI 官网重新生成。
:::

## 模型名称

- `doubao-seedream-5-0-flash-260915`

## 文生图 示例代码

```python
import requests
import json

# ===============================================================
# 步骤1: 配置 API 连接信息
# ===============================================================

# DMXAPI 服务端点地址
url = "https://www.dmxapi.cn/v1/responses"

# DMXAPI 密钥 (请替换为您自己的密钥)
# 获取方式: 登录 DMXAPI 官网 -> 个人中心 -> API 密钥管理
api_key = "sk-***********************************************"

# ===============================================================
# 步骤2: 配置请求头
# ===============================================================

headers = {
    "Content-Type": "application/json",      # 指定请求体为 JSON 格式
    "Authorization": f"{api_key}",           # token 认证方式
}

# ===============================================================
# 步骤3: 配置请求参数
# ===============================================================

payload = {
    # 【model】(string, 必填) 您需要调用的模型 ID（Model ID）
    "model": "doubao-seedream-5-0-flash-260915",

    # 【input】(string, 必填) 用于生成图像的提示词，支持中英文
    # 建议不超过 300 个汉字或 600 个英文单词；字数过多信息容易分散，
    # 模型可能因此忽略细节，只关注重点，造成图片缺失部分元素
    "input": "充满活力的特写编辑肖像，模特眼神犀利，头戴雕塑感帽子，色彩拼接丰富，眼部焦点锐利，景深较浅，具有Vogue杂志封面的美学风格，采用中画幅拍摄，工作室灯光效果强烈。",

    # 【size】(string, 可选) 指定生成图像的尺寸信息，默认值 2K
    # 支持以下两种方式，不可混用:
    #   - 指定宽高像素值（宽x高）: 总像素取值范围 [1280x720(921600), 2048x2048x1.1025(4624220)]，
    #     宽高比取值范围 [1/16, 16]，需同时满足（有效示例: "2048x1024"）
    #   - 指定分辨率档位: 可选值 "1K" / "1.5K" / "2K"，并在提示词中用自然语言描述图片宽高比、
    #     图片形状或图片用途，最终由模型判断生成图片的大小
    #     （如 1K 档位: 1:1 对应 1024x1024、16:9 对应 1424x800）
    "size": "1K",

    # 【output_format】(string, 可选) 指定生成图像的文件格式，默认值 jpeg
    # 可选值: "png" / "jpeg"
    "output_format": "png",

    # 【response_format】(string, 可选) 指定生成图像的返回格式，默认值 url
    # 可选值:
    #   - "url": 返回图片下载链接，链接在图片生成后 24 小时内有效，请及时下载图片
    #   - "b64_json": 以 Base64 编码字符串的 JSON 格式返回图像数据
    "response_format": "url",

    # 【watermark】(boolean, 可选) 是否在生成的图片中添加水印，默认值 true
    # 可选值: true(在图片右下角添加"AI生成"字样的水印标识) / false(不添加水印)
    "watermark": False,
}


# ===============================================================
# 步骤4: 发送请求并输出结果
# ===============================================================

# 发送 POST 请求到 API 服务器
response = requests.post(url, headers=headers, json=payload)

# 格式化输出 JSON 响应
# - indent=2: 缩进 2 空格，便于阅读
# - ensure_ascii=False: 正确显示中文字符
print(json.dumps(response.json(), indent=2, ensure_ascii=False))
```

## 返回示例

```json
{
  "model": "doubao-seedream-5-0-flash-260915",
  "created": 1793954426,
  "data": [
    {
      "url": "https://ark-acg-cn-beijing.tos-cn-beijing.volces.com/doubao-seedream-5-0-flash/2f4203fc3846eb75b826fb1abda622f072adfd008314459397120/Image/2112844032/021793954413800dfda270f226adba1bf628b57be6483cf3024f2.png?X-Tos-Algorithm=TOS4-HMAC-SHA256&X-Tos-Credential=AKLTYWJkZTExNjA1ZDUyNDc3YzhjNTM5OGIyNjBhNDcyOTQ%2F20261106%2Fcn-beijing%2Ftos%2Frequest&X-Tos-Date=20261106T084026Z&X-Tos-Expires=86400&X-Tos-Signature=be731501f2e7728fa0744609f02e1cac7a0ebb04e7e3788959d7ae49f2fb2c6e&X-Tos-SignedHeaders=host",
      "size": "832x1248",
      "output_format": "png",
      "background": "opaque"
    }
  ],
  "usage": {
    "total_tokens": 1200,
    "input_tokens": 0,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 1200,
    "output_tokens_details": {
      "reasoning_tokens": 0
    },
    "cost": "¥0.12"
  }
}
```

<p align="center">
  <small>© 2026 DMXAPI doubao-seedream-5-0-flash-260915 文生图</small>
</p>
