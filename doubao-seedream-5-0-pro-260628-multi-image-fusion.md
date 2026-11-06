# doubao-seedream-5-0-pro-260628 多图融合 API 使用文档

基于字节跳动豆包 Doubao Seedream 5.0 Pro 模型的多图融合接口，通过 `/v1/responses` 端点同步调用，根据多张参考图片（2~10 张）与文本提示词融合生成单张图片，可将不同图片中的人物、服装、场景等元素自然组合到同一画面（如为图 1 的人物换上图 2 的服装）。参考图以数组形式传入，支持 URL 或 Base64 编码，兼容 jpeg、png、webp、bmp、tiff、gif、heic、heif 共 8 种格式，单张大小最高 30MB；输出尺寸支持 `1K`/`1.5K`/`2K` 分辨率档位与精确宽高像素值两种控制方式，输出格式可选 `png`/`jpeg`。

## 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 图像生成 | POST | `https://www.dmxapi.cn/v1/responses` |



:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。如果怀疑密钥已泄露，请立即前往 DMXAPI 官网重新生成。
:::

## 模型名称

- `doubao-seedream-5-0-pro-260628`

## 多图融合 示例代码

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
    "model": "doubao-seedream-5-0-pro-260628",

    # 【input】(string, 必填) 用于生成图像的提示词，支持中英文
    # 建议不超过 300 个汉字或 600 个英文单词；字数过多信息容易分散，
    # 模型可能因此忽略细节，只关注重点，造成图片缺失部分元素
    "input": "将图1的服装换为图2的服装",

    # 【image】(array, 可选) 输入的多张参考图片列表，支持 URL 或 Base64 编码
    # 多图融合场景根据多张参考图片(2-10 张)+文本提示词生成单张图片，
    # 最多支持传入 10 张参考图
    # 图片 URL: 请确保图片 URL 可被访问
    # Base64 编码: 请遵循格式 data:image/<图片格式>;base64,<Base64编码>，
    #   注意 <图片格式> 需小写，如 data:image/png;base64,<base64_image>
    # 每张图片要求:
    #   - 图片格式: jpeg、png、webp、bmp、tiff、gif、heic、heif
    #   - 宽高比（宽/高）范围: [1/16, 16]，宽高长度（px）> 14
    #   - 大小: 不超过 30MB
    #   - 总像素: 不超过 6000x6000=36000000 px（对单张图宽高像素乘积的限制，
    #     而非对宽度或高度的单独限制）
    "image": [
      "https://ark-project.tos-cn-beijing.volces.com/doc_image/seedream4_imagesToimage_1.png",
      "https://ark-project.tos-cn-beijing.volces.com/doc_image/seedream4_5_imagesToimage_2.png"
    ],

    # 【size】(string, 可选) 指定生成图像的尺寸信息，默认值 2K
    # 支持以下两种方式，不可混用:
    #   - 指定宽高像素值（宽x高）: 总像素取值范围 [1280x720(921600), 2048x2048x1.1025(4624220)]，
    #     宽高比取值范围 [1/16, 16]，需同时满足（有效示例: "2048x1024"）
    #   - 指定分辨率档位: 可选值 "1K" / "1.5K" / "2K"，并在提示词中用自然语言描述图片宽高比、
    #     图片形状或图片用途，最终由模型判断生成图片的大小
    #     （如 2K 档位: 1:1 对应 2048x2048、16:9 对应 2816x1584）
    "size": "2K",

    # 【optimize_prompt_options】(object, 可选) 提示词优化配置，默认值 {"mode": "standard"}
    # mode 可选值:
    #   - "standard": 标准模式，生成内容的质量更高，耗时较长
    #   - "fast": 快速模式，生成耗时更短，效果略低于标准模式（对生成时延敏感的业务推荐使用）
    "optimize_prompt_options": {"mode": "standard"},

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
    "watermark": False
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
  "model": "doubao-seedream-5-0-pro-260628",
  "created": 1793892845,
  "data": [
    {
      "url": "https://ark-acg-cn-beijing.tos-cn-beijing.volces.com/doubao-seedream-5-0-pro/5955e66a651ae14ee6ab17801382bcdb6c77fa180018298397120/Image/2112844032/021793892810081af77c6bdcb28310871ba6ee41ea156a66e5595.png?X-Tos-Algorithm=TOS4-HMAC-SHA256&X-Tos-Credential=AKLTYWJkZTExNjA1ZDUyNDc3YzhjNTM5OGIyNjBhNDcyOTQ%2F20261105%2Fcn-beijing%2Ftos%2Frequest&X-Tos-Date=20261105T153405Z&X-Tos-Expires=86400&X-Tos-Signature=ead0263efd947d44178c8a3c27810befed7d1e6312ef4f2a6afe804e5cc92776&X-Tos-SignedHeaders=host",
      "size": "2048x2048",
      "output_format": "png",
      "background": "opaque"
    }
  ],
  "usage": {
    "total_tokens": 6200,
    "input_tokens": 0,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 6200,
    "output_tokens_details": {
      "reasoning_tokens": 0
    },
    "cost": "¥0.62"
  }
}
```

<p align="center">
  <small>© 2026 DMXAPI doubao-seedream-5-0-pro-260628 多图融合</small>
</p>
