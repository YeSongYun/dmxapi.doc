# qwen-image-edit-max-2026-01-16 多图融合 API文档
千问-图像编辑模型支持多图输入和多图输出，可精确修改图内文字、增删或移动物体、改变主体动作、迁移图片风格及增强画面细节。


## 接口地址

```
https://www.dmxapi.cn/v1/responses
```

## 模型名称

- `qwen-image-edit-max-2026-01-16`

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
    "model": "qwen-image-edit-max-2026-01-16",
    "input": {
        "messages": [
            {
                "role": "user",
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
                        "image": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/thtclx/input1.png"
                    },
                    {
                        "image": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/iclsnx/input2.png"
                    },
                    {
                        "image": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/gborgw/input3.png"
                    },
                    {
                        "text": "图1中的女生穿着图2中的黑色裙子按图3的姿势坐下"
                    }
                ]
            }
        ]
    },
    "parameters": {
        # 【n】输出图像的数量，默认值为 1。
        # 可选择输出 1-6 张图片。
        "n": 1,

        # 【negative_prompt】反向提示词，用来描述不希望在画面中看到的内容，可以对画面进行限制。
        # 支持中英文，长度上限 500 个字符，每个汉字、字母、数字或符号计为一个字符，超过部分会自动截断。
        # 示例值：低分辨率、错误、最差质量、低质量、残缺、多余的手指、比例不良等。
        "negative_prompt": " ",

        # 【prompt_extend】是否开启提示词智能改写，默认值为 true。
        # 开启后，模型会优化正向提示词，对描述较简单的提示词效果提升明显。
        # 支持模型：qwen-image-edit-max、qwen-image-edit-plus 系列模型。
        "prompt_extend": True,

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
        "seed": 0
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
          "text": "https://dashscope-result-sh.oss-cn-shanghai.aliyuncs.com/7d/92/20260228/f3c4f0bb/3a94bd1a-fbcb-41fb-9055-997215f53687-1.png?Expires=1772850254&OSSAccessKeyId=LTAI5tKPD3TMqf2Lna1fASuh&Signature=21Tov0xt92VwPv2C5spgwENDDgk%3D"
        }
      ]
    }
  ],
  "usage": {
    "total_tokens": 5000,
    "input_tokens": 0,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 5000,
    "output_tokens_details": {
      "reasoning_tokens": 0
    }
  },
  "request_id": "b4480bd7-2ad0-422c-b4ce-8157fc895719"
}
```

<p align="center">
  <small>© 2026 DMXAPI qwen-image-edit-max-2026-01-16 多图融合</small>
</p>
