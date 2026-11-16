# doubao-seedream-5-5-261028 图层拆分 API 使用文档

基于字节跳动豆包 Doubao Seedream 5.5（`doubao-seedream-5-5-261028`）的图层拆分接口，仍走 `/api/v3/images/generations`，在请求里把 `layer_decomposition` 设为 `true`。模型把单张图片拆成 1 张底图和多个可独立编辑的图层，每个图层是带透明通道的 PNG；Seedream 5.5 最多输出 1 张底图和 99 个图层。只接受 1 张待拆分图，传入多张会报错。图片格式仅 png、jpeg，宽高比 [1/16, 16]，不超过 30MB，总像素 [512x512（262144）, 6000x6000（36M）]。

## 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 图像生成 | POST | `https://www.dmxapi.cn/api/v3/images/generations` |


:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。如果怀疑密钥已泄露，请立即前往 DMXAPI 官网重新生成。
:::

## 模型名称

- `doubao-seedream-5-5-261028`

## 图层拆分 示例代码

```python
import requests
import json

# ===============================================================
# 步骤1: 配置 API 连接信息
# ===============================================================

# DMXAPI 服务端点地址
url = "https://www.dmxapi.cn/api/v3/images/generations"

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
    # 【model】(string, 必填) 调用的模型名称
    "model": "doubao-seedream-5-5-261028",

    # 【prompt】(string, 图层拆分场景可选) 提示词
    # 用于指定图层拆分意图，模型根据提示词意图识别并拆分指定元素
    # 若不传入提示词，模型将自动识别图片中的所有主要元素并拆分为独立图层
    # 语言支持: 中英文，额外支持俄语、阿拉伯语、菲律宾语、泰语、土耳其语、韩语、马来语、
    #           西班牙语、葡萄牙语、印尼语、法语、德语、越南语、日语
    # 字数建议: 中文提示词不超过 300 字，英文提示词不超过 600 词
    # 注意: 若提示词要求的拆分数量超过上限，可能导致部分图层信息丢失
    "prompt": "把标题文字、人物主体和背景分别拆成独立图层",

    # 【image】(string / string[], 图层拆分场景必填) 待拆分图片
    # 输入的图片信息，支持 URL 或 Base64 编码 (请替换为您自己的图片)
    #   - 图片 URL: 请确保图片 URL 可被访问
    #   - Base64 编码: 格式为 data:image/<图片格式>;base64,<Base64 编码>
    #                  注意 <图片格式> 需小写，如 data:image/png;base64,<Base64 编码>
    # 开启图层拆分模式时 image 为必选参数，且仅支持输入单张图片，传入多张报错
    # 单张图片传入要求:
    #   - 图片格式: png、jpeg
    #   - 宽高比: [1/16, 16]
    #   - 大小: 不超过 30MB
    #   - 总像素 (宽x高) 范围: [512x512 (262144), 6000x6000 (36M)]，
    #     是宽度和高度的乘积限制，不是对宽或高的单独限制
    "image": "https://example.com/poster.png",

    # 【layer_decomposition】(boolean, 可选) 图层拆分开关
    # 控制是否开启图层拆分功能，默认值 false；本示例为图层拆分场景，需设为 True
    # 图层拆分会将单张图片的主体、背景、文字等内容自动拆解为 1 张底图和多个可独立编辑的图层，
    # 每个图层为带透明通道的 PNG 图片
    # 可选值:
    #   - True(图层拆分模式，模型将输入图拆解为一张底图和多个图层；
    #          Seedream 5.5 最多输出 1 张底图和 99 个图层)
    #   - False(图片生成模式，不进行图层拆分)
    # 注意: 任一图层生成失败，整体请求报错，不支持部分成功
    # 响应的 data 中将返回每个产出图层的位置和内容信息，包括图层顺序 (z_index)、
    # 边界框信息 (bounding_box)、名称 (name) 和描述 (description)
    "layer_decomposition": True,

    # 【layer_decomposition_options】(object, 可选) 图层拆分配置
    # 图层拆分功能的配置，仅当 layer_decomposition 为 True 时生效
    "layer_decomposition_options": {
        # 【max_images】(integer, 可选) 最大输出图片数
        # 设置本次请求最多生成的图片总数，包含底图和图层，默认值 30
        # 取值范围: [2, 100]
        # 说明: 每次请求将按 max_images 值预扣减 IPM (每分钟图片数限额)，若实际生成图片数量不足则释放多扣额度
        #       当提示词未说明如何拆分或描述不清晰时，模型会结合 max_images 和输入图片的
        #       复杂度合理规划拆分结果；传入的 max_images 值越大，拆分结果通常越细
        "max_images": 30,

        # 【text_recognition】(boolean, 可选) 富文本 OCR 返回开关
        # 控制是否对规整文字图层额外返回富文本 OCR 结果，默认值 false
        # 支持识别文本内容和文本样式 (加粗、斜体、下划线、删除线、阴影和半透明)
        # 可选值:
        #   - True(通过 data[].text_recognition 返回富文本 OCR 结果)
        #   - False(不返回富文本 OCR 结果)
        # 注意: 非文字图层，以及艺术字、手写体等非规整文字图层，不返回 OCR 结果
        "text_recognition": True
    },

    # 【size】(string, 可选) 图像尺寸
    # 图层拆分场景仅支持指定分辨率档位，默认值 auto
    # 可选值: "1K" / "1.5K" / "2K" / "auto"(根据输入图的尺寸和宽高比进行输出)
    # 输出图的分辨率规则:
    #   - 底图: 分辨率和 size 指定的分辨率一致，宽高比和原待拆分图一致
    #   - 各图层: 分辨率和 size 指定的分辨率接近，宽高比和其在原图中的宽高比一致
    # auto 适配规则 (按底图和每个图层的原始尺寸输出，并保持其在原图中的宽高比):
    #   - 原始尺寸在 [1280x720 (921600), 2048x2048x1.1025 (4624220)] 之间: 按原尺寸输出
    #   - 原始尺寸小于 1K: 按 1K 输出
    #   - 原始尺寸大于 2K: 按 2K 输出
    "size": "auto",

    # 【optimize_prompt_options】(object, 可选) 提示词优化配置
    # 提示词优化功能的配置
    "optimize_prompt_options": {
        # 【mode】(string, 可选) 优化模式
        # 设置提示词优化功能使用的模式，默认值 standard
        # 可选值:
        #   - "standard"(标准模式，生成内容的质量更高，耗时较长)
        # Seedream 5.5 仅支持 standard
        "mode": "standard"
    },

    # 【output_format】(string, 可选) 图像格式
    # 指定生成图像的文件格式，默认值 png
    # 可选值: "png" / "jpeg"
    # 注意: 图层拆分场景下，output_format 仅控制底图的输出格式，图层始终以 png 格式输出
    "output_format": "png",

    # 【response_format】(string, 可选) 返回格式
    # 指定生成图像的返回格式，默认值 url
    # 可选值:
    #   - "url"(返回图片下载链接，链接在图片生成后 24 小时内有效，请及时下载图片)
    #   - "b64_json"(以 Base64 编码字符串的 JSON 格式返回图像数据)
    "response_format": "url",

    # 【watermark】(boolean, 可选) 水印开关
    # 是否在生成的图片中添加水印，默认值 true
    # 可选值:
    #   - True(在图片右下角添加「AI 生成」字样的水印标识)
    #   - False(不添加水印)
    "watermark": False

    # 注意: 图层拆分场景不支持传入 background 参数，传入将报错
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
  "created": 1794819367,
  "data": [
    {
      "background": "opaque",
      "output_format": "png",
      "size": "1024x1024",
      "url": "https://ark-acg-cn-beijing.tos-cn-beijing.volces.com/doubao-seedream-5-5/bc371e1aa4280a2dc696cc4256e754d1ae93b3006653918497120/Image/2112844032/0217948193566003b39ea1d457e6524cc696cd2a0824aa1e173cb_base.png?X-Tos-Algorithm=TOS4-HMAC-SHA256&X-Tos-Credential=AKLTYWJkZTExNjA1ZDUyNDc3YzhjNTM5OGIyNjBhNDcyOTQ%2F20261116%2Fcn-beijing%2Ftos%2Frequest&X-Tos-Date=20261116T085605Z&X-Tos-Expires=86400&X-Tos-Signature=9a910e829424d6a2e1223471ec404901a3437f7f815f3ae297e33f560fde7435&X-Tos-SignedHeaders=host",
      "z_index": 0
    },
    {
      "background": "transparent",
      "bounding_box": {
        "absolute": [
          0,
          0,
          1024,
          1024
        ],
        "normalized": [
          0,
          0,
          1000,
          1000
        ]
      },
      "description": "身着液态银色金属质感服饰、带有尖刺状液态金属发型的女性人物主体",
      "name": "身着液态银色金属质感服饰、带有尖刺状液态金属发型的女性人物主体",
      "output_format": "png",
      "size": "1024x1024",
      "url": "https://ark-acg-cn-beijing.tos-cn-beijing.volces.com/doubao-seedream-5-5/bc371e1aa4280a2dc696cc4256e754d1ae93b3006653918497120/Image/2112844032/0217948193566003b39ea1d457e6524cc696cd2a0824aa1e173cb_layer_1.png?X-Tos-Algorithm=TOS4-HMAC-SHA256&X-Tos-Credential=AKLTYWJkZTExNjA1ZDUyNDc3YzhjNTM5OGIyNjBhNDcyOTQ%2F20261116%2Fcn-beijing%2Ftos%2Frequest&X-Tos-Date=20261116T085603Z&X-Tos-Expires=86400&X-Tos-Signature=7934f71918679e6a3332707875e0cc4ed27653938c6f49e4bca0482b5bf50d31&X-Tos-SignedHeaders=host",
      "z_index": 1
    }
  ],
  "model": "doubao-seedream-5-5-261028",
  "usage": {
    "generated_images": 2,
    "input_images": 1,
    "output_tokens": 8192,
    "total_tokens": 8192,
    "cost": "¥0.31"
  }
}
```

<p align="center">
  <small>© 2026 DMXAPI doubao-seedream-5-5-261028 图层拆分</small>
</p>
