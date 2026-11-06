# doubao-seedream-5-0-flash-260915 图生图 API 使用文档

基于字节跳动豆包 Doubao Seedream 5.0 Flash 模型的图生图接口，通过 `/v1/responses` 端点同步调用，根据单张参考图片与文本提示词生成单张图片，可在保持原图主体结构的同时完成材质替换、光影调整、风格转换等精细编辑。参考图支持 URL 或 Base64 编码传入，兼容 jpeg、png、webp、bmp、tiff、gif、heic、heif 共 8 种格式，单张大小最高 30MB；输出尺寸支持 `1K`/`1.5K`/`2K` 分辨率档位与精确宽高像素值两种控制方式，输出格式可选 `png`/`jpeg`；输入带透明通道的图片时，可通过 `background` 参数输出透明背景图片。

## 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 图像生成 | POST | `https://www.dmxapi.cn/v1/responses` |



:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。如果怀疑密钥已泄露，请立即前往 DMXAPI 官网重新生成。
:::

## 模型名称

- `doubao-seedream-5-0-flash-260915`

## 图生图 示例代码

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
    "input": "保持logo的形状和构图不变，将logo改为金属质感，表面带有拉丝金属纹理和高光反射，保留透明背景",

    # 【image】(string, 可选) 输入的参考图片信息，支持 URL 或 Base64 编码
    # 图片 URL: 请确保图片 URL 可被访问
    # Base64 编码: 请遵循格式 data:image/<图片格式>;base64,<Base64编码>，
    #   注意 <图片格式> 需小写，如 data:image/png;base64,<base64_image>
    # 传入图片要求:
    #   - 图片格式: jpeg、png、webp、bmp、tiff、gif、heic、heif
    #   - 宽高比（宽/高）范围: [1/16, 16]，宽高长度（px）> 14
    #   - 大小: 不超过 30MB
    #   - 总像素: 不超过 6000x6000=36000000 px（对宽高像素乘积的限制，
    #     而非对宽度或高度的单独限制）
    "image": "https://registry.npmmirror.com/@lobehub/icons-static-png/2.6.0/files/light/doubao-color.png",

    # 【size】(string, 可选) 指定生成图像的尺寸信息，默认值 2K
    # 支持以下两种方式，不可混用:
    #   - 指定宽高像素值（宽x高）: 总像素取值范围 [1280x720(921600), 2048x2048x1.1025(4624220)]，
    #     宽高比取值范围 [1/16, 16]，需同时满足（有效示例: "2048x1024"）
    #   - 指定分辨率档位: 可选值 "1K" / "1.5K" / "2K"，并在提示词中用自然语言描述图片宽高比、
    #     图片形状或图片用途，最终由模型判断生成图片的大小
    #     （如 2K 档位: 1:1 对应 2048x2048、16:9 对应 2848x1600）
    "size": "2K",

    # 【output_format】(string, 可选) 指定生成图像的文件格式，默认值 jpeg
    # 可选值: "png" / "jpeg"
    "output_format": "png",

    # 【background】(string, 可选) 图片透明通道，默认值 opaque
    # 可选值:
    #   - "opaque": 不透明背景模式，生成常规的实体背景图
    #   - "transparent": 透明背景模式，输出带透明背景的图
    # 使用 "transparent" 时需注意:
    #   - 仅支持输入 1 张带透明通道的图片（如带透明背景的 png），
    #     传入不支持透明通道的格式（如 jpeg）将报错
    #   - 输出图为 png，若同时将 output_format 设为 "jpeg" 将报错
    "background": "transparent",

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
  "model": "doubao-seedream-5-0-flash-260915",
  "created": 1793955322,
  "data": [
    {
      "url": "https://ark-acg-cn-beijing.tos-cn-beijing.volces.com/doubao-seedream-5-0-flash/9acf165fd380ba62c536505d365d82f88c3686773203559397120/Image/2112844032/0217939553023776863c88f28d563d505635c26ab083df561fca9.png?X-Tos-Algorithm=TOS4-HMAC-SHA256&X-Tos-Credential=AKLTYWJkZTExNjA1ZDUyNDc3YzhjNTM5OGIyNjBhNDcyOTQ%2F20261106%2Fcn-beijing%2Ftos%2Frequest&X-Tos-Date=20261106T085520Z&X-Tos-Expires=86400&X-Tos-Signature=db1506b8a88163dbfd092ccd9df268914cd6845ee0600d27a428393a2f75b6da&X-Tos-SignedHeaders=host",
      "size": "2048x2048",
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
  <small>© 2026 DMXAPI doubao-seedream-5-0-flash-260915 图生图</small>
</p>
