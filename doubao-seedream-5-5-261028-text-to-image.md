# doubao-seedream-5-5-261028 文生图 API 使用文档

基于字节跳动豆包 Doubao Seedream 5.5（`doubao-seedream-5-5-261028`）的文生图接口，通过 `/api/v3/images/generations` 端点同步调用：只提交文本提示词，生成单张图片。该模型不支持组图（不要传 `sequential_image_generation`）、联网搜索和流式输出。


## 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 图像生成 | POST | `https://www.dmxapi.cn/api/v3/images/generations` |


:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。如果怀疑密钥已泄露，请立即前往 DMXAPI 官网重新生成。
:::

## 模型名称

- `doubao-seedream-5-5-261028`

## 文生图 示例代码

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

    # 【prompt】(string, 图片生成场景必填) 提示词
    # 用于描述生成图像的内容，模型根据提示词生成对应图像
    # 语言支持: 中英文，额外支持俄语、阿拉伯语、菲律宾语、泰语、土耳其语、韩语、马来语、
    #           西班牙语、葡萄牙语、印尼语、法语、德语、越南语、日语
    # 字数建议: 中文提示词不超过 300 字，英文提示词不超过 600 词
    #           字数过多信息容易分散，模型可能因此忽略细节、只关注重点，
    #           造成图片缺失部分元素
    "prompt": "一只橘猫趴在窗台上晒太阳，窗外是秋天的银杏树，胶片摄影风格，画面比例 16:9",

    # 【size】(string, 可选) 图像尺寸
    # 指定生成图像的尺寸信息，默认值 2K
    # 支持以下两种方式，不可混用:
    #   - 方式 1(推荐): 指定分辨率档位，并在 prompt 中用自然语言描述图片宽高比、图片形状
    #                   或图片用途，最终由模型判断生成图片的大小
    #                   可选值: "1K" / "1.5K" / "2K"
    #   - 方式 2: 指定宽高像素值，格式 "宽x高"，例如 "2880x1440"
    #             总像素取值范围: [921600, 4624220]，即 1280x720 至 2048x2048x1.1025
    #             宽高比取值范围: [1/16, 16]
    #             需同时满足两项限制；总像素是宽度和高度的乘积限制，不是对宽或高的单独限制
    # 方式 1 时模型实际映射的宽高像素参考值 (仅列常见):
    #   - 1K  : 1:1 1024x1024、4:3 1152x864、3:4 864x1152、16:9 1424x800、9:16 800x1424、
    #           3:2 1248x832、2:3 832x1248、21:9 1568x672
    #   - 1.5K: 1:1 1536x1536、4:3 1792x1344、3:4 1344x1792、16:9 2048x1152、9:16 1152x2048、
    #           3:2 1872x1248、2:3 1248x1872、21:9 2352x1008
    #   - 2K  : 1:1 2048x2048、4:3 2368x1776、3:4 1776x2368、16:9 2816x1584、9:16 1584x2816、
    #           3:2 2496x1664、2:3 1664x2496、21:9 3136x1344
    "size": "2K",

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
    # 注意: 当 output_format 为 jpeg，且 background 为 transparent 时，请求报错
    "output_format": "png",

    # 【background】(string, 可选) 透明通道模式
    # 控制生成图片是否带 Alpha 通道 (透明度通道)，默认值 auto
    # 可选值:
    #   - "auto"(模型根据提示词和 output_format 自动判断；
    #            若设置输出格式为 jpeg，输出图片不带透明通道)
    #   - "transparent"(输出带透明通道的图片，即 RGBA 图；Seedream 5.5 支持文生 RGBA 图片)
    #   - "opaque"(输出不带透明通道的图片，即 RGB 图)
    "background": "auto",

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
  "created": 1794806465,
  "data": [
    {
      "background": "opaque",
      "output_format": "png",
      "size": "2816x1584",
      "url": "https://ark-acg-cn-beijing.tos-cn-beijing.volces.com/doubao-seedream-5-5/378a0728353bae7877c69bc55a42d2a0c3dcd3609054608497120/Image/2112844032/0217948064509063dcd3c0a2d24a55cb96c7787eab3538270a873.png?X-Tos-Algorithm=TOS4-HMAC-SHA256&X-Tos-Credential=AKLTYWJkZTExNjA1ZDUyNDc3YzhjNTM5OGIyNjBhNDcyOTQ%2F20261116%2Fcn-beijing%2Ftos%2Frequest&X-Tos-Date=20261116T052103Z&X-Tos-Expires=86400&X-Tos-Signature=ee73577e0de8baee4f26247196726348719666f3a219ea3d166fccd6f2515dd6&X-Tos-SignedHeaders=host"
    }
  ],
  "model": "doubao-seedream-5-5-261028",
  "usage": {
    "generated_images": 1,
    "input_images": 0,
    "output_tokens": 17424,
    "total_tokens": 17424,
    "cost": "¥0.23"
  }
}
```

<p align="center">
  <small>© 2026 DMXAPI doubao-seedream-5-5-261028 文生图</small>
</p>
