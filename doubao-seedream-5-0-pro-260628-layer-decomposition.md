# doubao-seedream-5-0-pro-260628 图层拆分 API 使用文档

基于字节跳动豆包 Doubao Seedream 5.0 Pro 模型的图层拆分接口，通过 `/v1/responses` 端点同步调用，将单张图片中的主体、背景、文字等内容自动拆解为 1 张底图与最多 16 个可独立编辑的透明图层，适用于海报、封面、设计稿等图片的二次编辑。提示词可选：不传时模型自动识别并拆分图片中的所有主要元素，传入时可通过 `<bbox>` 坐标或自然语言指定需要拆分的元素。待拆分图片支持 URL 或 Base64 编码传入，仅支持 png、jpeg 格式；输出底图格式可选 `png`/`jpeg`，各图层固定为带透明通道的 png，并返回每个图层的叠放顺序、边界框坐标、名称与描述。

## 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 图层拆分 | POST | `https://www.dmxapi.cn/v1/responses` |



:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。如果怀疑密钥已泄露，请立即前往 DMXAPI 官网重新生成。
:::

## 模型名称

- `doubao-seedream-5-0-pro-260628`

## 图层拆分 示例代码

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

    # 【input】(string, 可选) 用于指定图层拆分意图的提示词，支持中英文
    # 不传时: 模型自动识别图片中的所有主要元素，并拆分为独立图层
    # 传入时: 模型按提示词意图识别并拆分指定元素，可使用 <bbox>x1 y1 x2 y2</bbox>
    #   标注元素位置（坐标为 0-1000 的归一化坐标，原点为图片左上角）
    # 注意: 若提示词要求的拆分数量超过上限（16 个图层），可能导致部分图层信息丢失
    "input": "将图片进行精确的图层分离，需分离的文字坐标为<bbox>180 64 812 198</bbox>、<bbox>757 210 939 280</bbox>、<bbox>63 212 320 282</bbox>、<bbox>178 714 826 810</bbox>、<bbox>814 819 949 894</bbox>、<bbox>326 824 698 930</bbox>；鹦鹉的坐标为<bbox>347 305 642 997</bbox>",

    # 【image】(string, 必填) 待拆分的图片，支持 URL 或 Base64 编码，仅支持传入 1 张
    # 图片 URL: 请确保图片 URL 可被访问
    # Base64 编码: 请遵循格式 data:image/<图片格式>;base64,<Base64编码>，
    #   注意 <图片格式> 需小写，如 data:image/png;base64,<base64_image>
    # 传入图片要求:
    #   - 图片格式: png、jpeg
    #   - 宽高比（宽/高）范围: [1/16, 16]
    #   - 大小: 不超过 30MB
    #   - 总像素: [512x512=262144, 6000x6000=36000000] px（对宽高像素乘积的限制，
    #     而非对宽度或高度的单独限制）
    "image": "https://arkdocs.tos-cn-beijing.volces.com/images/image-generation/seedream_50_pro_layer_input.png",

    # 【layer_decomposition】(boolean, 必填) 图层拆分开关，图层拆分时须设为 true
    # 开启后模型将输入图拆解为 1 张底图和最多 16 个图层，每个图层为带透明通道的 png 图片
    # 任一图层生成失败时整体请求报错，不支持部分成功
    "layer_decomposition": True,

    # 【size】(string, 可选) 指定输出图片的分辨率档位，默认值 auto
    # 仅支持指定分辨率档位，不支持指定宽高像素值
    # 可选值: "1K" / "1.5K" / "2K" / "auto"（根据输入图的尺寸和宽高比进行输出）
    #   - 底图: 分辨率和 size 指定的档位一致，宽高比和原图一致
    #   - 各图层: 分辨率和 size 指定的档位接近，宽高比和该图层在原图中的宽高比一致
    "size": "2K",

    # 【output_format】(string, 可选) 指定输出底图的文件格式，默认值 jpeg
    # 可选值: "png" / "jpeg"
    # 注意: 该参数仅对底图生效，各图层固定输出为带透明通道的 png
    "output_format": "jpeg",

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

`data` 按叠放顺序返回，第 1 项为底图，其余为拆分出的图层。图层拆分按输出图片张数计费，底图与每个图层均单独计费。

| 字段 | 说明 |
|------|------|
| `z_index` | 图层叠放顺序，底图固定为 `0`，图层从 `1` 开始递增，数值越大越靠上层 |
| `bounding_box.absolute` | 图层在输出底图中的像素坐标 `[left, top, right, bottom]`，将图层还原到输出底图时建议优先使用 |
| `bounding_box.normalized` | 同一位置的 0-1000 归一化坐标，可用于将图层还原到任意尺寸的画布中 |
| `name` / `description` | 模型自动生成的图层名称与内容描述 |
| `background` | 底图为 `opaque`（不透明），图层为 `transparent`（透明） |

```json
{
  "model": "doubao-seedream-5-0-pro-260628",
  "created": 1793883210,
  "data": [
    {
      "url": "https://ark-acg-cn-beijing.tos-cn-beijing.volces.com/doubao-seedream-5-0-pro/a3f9de0634...ed9f3a_base.jpeg?X-Tos-Algorithm=TOS4-HMAC-SHA256...",
      "size": "2048x2048",
      "output_format": "jpeg",
      "z_index": 0,
      "background": "opaque"
    },
    {
      "url": "https://ark-acg-cn-beijing.tos-cn-beijing.volces.com/doubao-seedream-5-0-pro/a3f9de0634...ed9f3a_layer_1.png?X-Tos-Algorithm=TOS4-HMAC-SHA256...",
      "size": "821x2037",
      "output_format": "png",
      "z_index": 1,
      "bounding_box": {
        "absolute": [731, 627, 1300, 2040],
        "normalized": [357, 306, 635, 996]
      },
      "name": "彩色金刚鹦鹉",
      "description": "提取栖息在树枝上的红蓝色金刚鹦鹉本体，只提取鹦鹉本身，不包含背景树枝和雨林环境",
      "background": "transparent"
    },
    {
      "url": "https://ark-acg-cn-beijing.tos-cn-beijing.volces.com/doubao-seedream-5-0-pro/a3f9de0634...ed9f3a_layer_2.png?X-Tos-Algorithm=TOS4-HMAC-SHA256...",
      "size": "1790x364",
      "output_format": "png",
      "z_index": 2,
      "bounding_box": {
        "absolute": [138, 451, 632, 551],
        "normalized": [67, 220, 309, 269]
      },
      "name": "左上标语文字",
      "description": "提取白色的EXPORE THE WILD, INSPIRE THE SOUL.文字，只提取该文字本体，不包含其他背景内容",
      "background": "transparent"
    },
    {
      "url": "https://ark-acg-cn-beijing.tos-cn-beijing.volces.com/doubao-seedream-5-0-pro/a3f9de0634...ed9f3a_layer_3.png?X-Tos-Algorithm=TOS4-HMAC-SHA256...",
      "size": "1366x448",
      "output_format": "png",
      "z_index": 3,
      "bounding_box": {
        "absolute": [1566, 447, 1912, 560],
        "normalized": [765, 218, 934, 273]
      },
      "name": "右上刊号文字",
      "description": "提取白色的VOL.01 SUMMER 2026文字，只提取该文字本体，不包含其他背景内容",
      "background": "transparent"
    },
    {
      "url": "https://ark-acg-cn-beijing.tos-cn-beijing.volces.com/doubao-seedream-5-0-pro/a3f9de0634...ed9f3a_layer_4.png?X-Tos-Algorithm=TOS4-HMAC-SHA256...",
      "size": "1980x551",
      "output_format": "png",
      "z_index": 4,
      "bounding_box": {
        "absolute": [705, 1713, 1350, 1893],
        "normalized": [344, 836, 659, 924]
      },
      "name": "底部三行说明文字",
      "description": "提取白色的FLY BEYOND LIMITS、TROPICAL SPLENDOR、RANFOREST ADVENTURES三行文字，只提取该文字本体，不包含其他背景内容",
      "background": "transparent"
    },
    {
      "url": "https://ark-acg-cn-beijing.tos-cn-beijing.volces.com/doubao-seedream-5-0-pro/a3f9de0634...ed9f3a_layer_5.png?X-Tos-Algorithm=TOS4-HMAC-SHA256...",
      "size": "2447x507",
      "output_format": "png",
      "z_index": 5,
      "bounding_box": {
        "absolute": [384, 120, 1653, 383],
        "normalized": [188, 59, 807, 187]
      },
      "name": "Seedream大标题文字",
      "description": "提取黄色的Seedream文字，只提取该文字本体，不包含其他背景内容",
      "background": "transparent"
    },
    {
      "url": "https://ark-acg-cn-beijing.tos-cn-beijing.volces.com/doubao-seedream-5-0-pro/a3f9de0634...ed9f3a_layer_6.png?X-Tos-Algorithm=TOS4-HMAC-SHA256...",
      "size": "2544x329",
      "output_format": "png",
      "z_index": 6,
      "bounding_box": {
        "absolute": [364, 1481, 1685, 1652],
        "normalized": [178, 723, 823, 807]
      },
      "name": "WILD BEAUTY大标题文字",
      "description": "提取黄色的WILD BEAUTY文字，只提取该文字本体，不包含其他背景内容",
      "background": "transparent"
    },
    {
      "url": "https://ark-acg-cn-beijing.tos-cn-beijing.volces.com/doubao-seedream-5-0-pro/a3f9de0634...ed9f3a_layer_7.png?X-Tos-Algorithm=TOS4-HMAC-SHA256...",
      "size": "1179x655",
      "output_format": "png",
      "z_index": 7,
      "bounding_box": {
        "absolute": [1679, 1686, 1947, 1834],
        "normalized": [820, 823, 951, 896]
      },
      "name": "右下NATURE INSIDE标识文字",
      "description": "提取椭圆标识内的白色NATURE INSIDE文字，只提取该标识和文字本体，不包含其他背景内容",
      "background": "transparent"
    }
  ],
  "usage": {
    "total_tokens": 13500,
    "input_tokens": 0,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 13500,
    "output_tokens_details": {
      "reasoning_tokens": 0
    }
  }
}
```

<p align="center">
  <small>© 2026 DMXAPI doubao-seedream-5-0-pro-260628 图层拆分</small>
</p>
