# qwen-image-edit-plus-20260226 图片编辑 API文档
千问-图像编辑模型支持多图输入和多图输出，可精确修改图内文字、增删或移动物体、改变主体动作、迁移图片风格及增强画面细节。


## 请求地址

```
https://www.dmxapi.cn/v1/responses
```

## 模型名称

- `qwen-image-edit-plus-20260226`

## 示例代码

```python
import requests
import json

# ═══════════════════════════════════════════════════════════════
# 🔑 步骤1: 配置 API 连接信息
# ═══════════════════════════════════════════════════════════════

# 🌐 DMXAPI 服务端点地址
url = "https://www.dmxapi.cn/v1/responses"

# 🔐 DMXAPI 密钥 (请替换为您自己的密钥)
# 获取方式: 登录 DMXAPI 官网 -> 个人中心 -> API 密钥管理
api_key = "sk-*********************************************"

# ═══════════════════════════════════════════════════════════════
# 📋 步骤2: 配置请求头
# ═══════════════════════════════════════════════════════════════

headers = {
    "Content-Type": "application/json",      # 指定请求体为 JSON 格式
    "Authorization": f"{api_key}",    # token 认证方式
}

# ═══════════════════════════════════════════════════════════════
# 💬 步骤3: 配置请求参数
# ═══════════════════════════════════════════════════════════════

payload = {

    # 【model】模型名称。
    "model": "qwen-image-edit-plus-20260226",

    "input": {
        # 【messages】请求内容数组。当前仅支持单轮对话，因此数组内有且只有一个对象，该对象包含 role 和 content 两个属性。
        "messages": [
            {
                # 【role】消息发送者角色，必须设置为 user。
                "role": "user",
                # 【content】消息内容，包含 1-3 张图像，格式为 {"image": "..."}；以及单个编辑指令，格式为 {"text": "..."}。
                "content": [
                    {
                        # 【image】输入图像的 URL 或 Base64 编码数据。支持传入 1-3 张图像。
                        # 多图输入时，按照数组顺序定义图像顺序，输出图像的比例以最后一张为准。
                        # 图像格式：JPG、JPEG、PNG、BMP、TIFF、WEBP 和 GIF。输出图像为 PNG 格式，对于 GIF 动图，仅处理其第一帧。
                        # 图像分辨率：为获得最佳效果，建议图像的宽和高均在 384 像素至 3072 像素之间。分辨率过低可能导致生成效果模糊，过高则会增加处理时长。
                        # 图像大小：不超过 10MB。
                        # 支持的输入格式
                        #   公网URL：
                        #     支持 HTTP 和 HTTPS 协议。
                        #     示例值：https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/fpakfo/image36.webp。
                        #   临时URL：
                        #     支持OSS协议，必须通过上传文件获取临时 URL。具体见：https://help.aliyun.com/zh/model-studio/get-temporary-file-url?spm=a2c4g.11186623.0.0.66427604IEGWS0
                        #     示例值：oss://dashscope-instant/xxx/2024-07-18/xxx/cat.png。
                        #   传入 Base64 编码图像后的字符串
                        #     示例值：data:image/jpeg;base64,GDU7MtCZz...（示例已截断，仅做演示）
                        #     Base64 编码规范请参见通过Base64编码传入图片。
                        "image": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/fpakfo/image36.webp"
                    },
                    {
                        # 【text】正向提示词，用于描述期望生成的图像内容、风格和构图。
                        # 支持中英文，长度不超过 800 个字符，每个汉字、字母、数字或符号计为一个字符，超过部分会自动截断。
                        # 注意：仅支持传入一个 text，不传或传入多个将报错。
                        "text": "生成一张符合深度图的图像，遵循以下描述：一辆红色的破旧的自行车停在一条泥泞的小路上，背景是茂密的原始森林"
                    }
                ]
            }
        ]
    },
    "parameters": {

        # 【n】输出图像的数量，默认值为 1。
        # 可选择输出 1-6 张图片。
        "n": 2,

        # 【negative_prompt】反向提示词，用来描述不希望在画面中看到的内容，可以对画面进行限制。
        # 支持中英文，长度上限 500 个字符，每个汉字、字母、数字或符号计为一个字符，超过部分会自动截断。
        # 示例值：低分辨率、错误、最差质量、低质量、残缺、多余的手指、比例不良等。
        "negative_prompt": " ",

        # 【prompt_extend】是否开启提示词智能改写，默认值为 true。
        # 开启后，模型会优化正向提示词（text），对描述较简单的提示词效果提升明显。
        # 支持模型：qwen-image-edit-max、qwen-image-edit-plus 系列模型。
        "prompt_extend": False,

        # 【watermark】是否在图像右下角添加 "Qwen-Image" 水印。默认值为 false。
        "watermark": False,

        # 【size】设置输出图像的分辨率，格式为 宽*高，例如 "1024*1536"。
        # 宽和高的取值范围均为 [512, 2048] 像素。
        # 指定 size 参数，系统会以 size 指定的宽高为目标，将实际输出图像的宽高调整为最接近的 16 的倍数。
        # 若不设置，输出图像将保持与输入图像相似的宽高比，总像素数接近 1024*1024。
        # 常见比例推荐分辨率
        #     1:1: 1024*1024、1536*1536
        #     2:3: 768*1152、1024*1536
        #     3:2: 1152*768、1536*1024
        #     3:4: 960*1280、1080*1440
        #     4:3: 1280*960、1440*1080
        #     9:16: 720*1280、1080*1920
        #     16:9: 1280*720、1920*1080
        #     21:9: 1344*576、2048*872
        "size": "1536*1024",

        # 【seed】随机数种子，取值范围 [0, 2147483647]。
        # 使用相同的 seed 参数值可使生成内容保持相对稳定。若不提供，算法将自动使用随机数种子。
        # 注意：模型生成过程具有概率性，即使使用相同的 seed，也不能保证每次生成结果完全一致。
        "seed": 100
    }
}


# ═══════════════════════════════════════════════════════════════
# 📤 步骤4: 发送请求并输出结果
# ═══════════════════════════════════════════════════════════════

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
  "output": [
    {
      "type": "message",
      "content": [
        {
          "type": "image",
          "text": "https://dashscope-result-hz.oss-cn-hangzhou.aliyuncs.com/7d/e8/20260227/45af8005/fc63bad6-0457-4aec-9606-550dfaf2c19c100.png?Expires=1772772014&OSSAccessKeyId=LTAI5tKPD3TMqf2Lna1fASuh&Signature=bBI93DG%2BZLln9mekMZfWdZqbiU0%3D"
        },
        {
          "type": "image",
          "text": "https://dashscope-result-hz.oss-cn-hangzhou.aliyuncs.com/7d/15/20260227/45af8005/3f886c12-99b0-4561-84c1-8a180d53ba06101.png?Expires=1772772014&OSSAccessKeyId=LTAI5tKPD3TMqf2Lna1fASuh&Signature=peLfsXioNLkbFapdMxQyZNGdAGs%3D"
        }
      ]
    }
  ],
  "usage": {
    "total_tokens": 4000,
    "input_tokens": 0,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 4000,
    "output_tokens_details": {
      "reasoning_tokens": 0
    }
  },
  "request_id": "254ad179-8197-4605-8128-118d43e51afa"
}
```

<p align="center">
  <small>© 2026 DMXAPI qwen-image-edit-plus-20260226 图片编辑</small>
</p>
