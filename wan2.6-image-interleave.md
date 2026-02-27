# wan2.6-image 图文混排 API文档
wan2.6图文混排模式，支持根据文本描述生成图文并茂的内容，或进行纯文本生成图像（文生图）。可输入0~1张参考图像，输出包含文本和图像的混合内容；支持多种主流图像格式（JPEG、PNG、BMP、WEBP），输出分辨率最高可达1280×1280，并提供反向提示词等精细化控制参数。


## 请求地址

```
https://www.dmxapi.cn/v1/responses
```

## 模型名称

- `wan2.6-image`

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
api_key = "sk-************************************"

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
    "model": "wan2.6-image",
    "input": {
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        # 正向提示词用于描述您期望生成的图像内容、风格和构图。
                        # 支持中英文，长度不超过2000个字符，每个汉字、字母、数字或符号计为一个字符，超过部分会自动截断。
                        # 注意：content数组中，必须且只能包含一个含 text 字段的对象。
                        "text": "生成一张春天的风景画，包含樱花树和小溪"
                    }
                    # 图文混排模式下可输入0~1张图像（可选）。
                    # 如需传入参考图像，在content数组中添加一个image对象即可：
                    # {
                    #     "image": "https://cdn.wanx.aliyuncs.com/tmp/pressure/umbrella1.png"
                    # }
                    #
                    # 图像限制：
                    #     图像格式：JPEG、JPG、PNG（不支持透明通道）、BMP、WEBP。
                    #     图像分辨率：图像的宽高范围均为[384, 5000]像素。
                    #     文件大小：不超过10MB。
                    # 支持的输入格式：
                    # 使用公网可访问URL
                    #     支持 HTTP 或 HTTPS 协议。
                    #     示例值：http://wanx.alicdn.com/material/xxx.jpeg。
                    # 传入 Base64 编码图像后的字符串
                    #     格式：data:{MIME_type};base64,{base64_data}
                    #     示例：data:image/jpeg;base64,GDU7MtCZzEbTbmRZ...（仅示意，实际需传入完整字符串）
                    #     Base64 编码规范请参见图像传入方式。链接如下:https://help.aliyun.com/zh/model-studio/wan-image-edit-2-5?spm=a2c4g.11186623.0.0.f7815b1dvRcn2Q#8db0e2215frua
                ]
            }
        ]
    },


        # 输出图像尺寸的规则
        # 方式一：指定 size 参数：系统会以 size 指定的宽高为目标，将实际输出图像的宽高调整为不大于指定值的、最大的16的倍数。
        # 方式二：未指定 size：输出图像由 总像素上限 和 宽高比规则 共同决定。
        #     总像素规则：图文混排模式下：
        #         若输入图像总像素 ≤ 1280*1280，输出总像素与输入一致；
        #         若输入图像总像素 > 1280*1280，输出总像素固定为 1280*1280。
        #     宽高比规则（近似）：
        #         单图输入：输出宽高比与输入图像一致；
        #         无图输入：由模型自动决定。
    "parameters": {

        "watermark": False, # 是否添加水印标识，水印位于图片右下角，文案固定为“AI生成”。

        # [n]:图文混排模式下此参数默认为1，且必须固定为1。若设置为其他值，接口将报错。
        # 如需控制生成图像的数量上限，请使用 max_images 参数。
        "n": 1,

        # [enable_interleave]:控制生图模式：
        # true：表示启用图文混排输出模式（仅支持传入一张图像或不传图像）。
        #     用途：根据文本描述生成图文并茂的内容，或进行纯文本生成图像（文生图）。
        #     输入：可以不提供图像（文生图），或提供最多1张参考图像。
        #     输出：生成包含文本和图像的混合内容。
        "enable_interleave": True,

        # 输出图像的分辨率，格式为宽*高。
        # wan2.6-image：总像素在 [768*768, 1280*1280] （即589824 至 1638400像素）之间，且宽高比范围为 [1:4, 4:1]。例如，1024*1536符合要求。
        # 常见比例推荐的分辨率
        #     1:1：1280*1280 或 1024*1024
        #     2:3：800*1200
        #     3:2：1200*800
        #     3:4：960*1280
        #     4:3：1280*960
        #     9:16：720*1280
        #     16:9：1280*720
        #     21:9：1344*576
        "size": "1280*1280",

        # 反向提示词，用于描述不希望在图像中出现的内容，对画面进行限制。
        # 支持中英文，长度不超过500个字符，超出部分将自动截断。
        "negative_prompt": "",

        # [max_images]:仅在图文混排模式（即 enable_interleave=true）下生效。
        # 作用：指定模型在单次回复中生成图像的最大数量。
        # 取值范围：1～5，默认值为 5。
        # 注意：该参数仅代表"数量上限"。实际生成的图像数量由模型推理决定，可能会少于设定值（例如：设置为 5，模型可能根据内容仅生成 3 张）。
        "max_images": 3,

        

        # [seed]随机数种子，取值范围[0,2147483647]。
        # 使用相同的seed参数值可使生成内容保持相对稳定。若不提供，算法将自动使用随机数种子。
        # 注意：模型生成过程具有概率性，即使使用相同的seed，也不能保证每次生成结果完全一致。
        "seed": 100,
    }
    # [stream]:图文混排模式下必须设置为 true（流式输出）。
    "stream": True
}

# ═══════════════════════════════════════════════════════════════
# 📤 步骤4: 发送请求并解析流式响应
# ═══════════════════════════════════════════════════════════════

# 发送 POST 请求到 API 服务器（流式模式）
response = requests.post(url, headers=headers, json=payload, stream=True)

# 逐行解析流式响应（SSE 格式）
for line in response.iter_lines():
    if line:
        decoded_line = line.decode("utf-8")
        if decoded_line.startswith("data:"):
            data_str = decoded_line[len("data:"):].strip()
            if data_str == "[DONE]":
                print("\n[流式输出完成]")
                break
            try:
                data = json.loads(data_str)
                print(json.dumps(data, indent=2, ensure_ascii=False))
            except json.JSONDecodeError:
                pass
```


## 返回示例
图文混排模式采用流式输出（SSE），响应会逐块返回，每块包含文本或图像内容。以下为单个数据块示例：
```json
{
  "output": [
    {
      "type": "message",
      "content": [
        {
          "type": "text",
          "text": "春天的景色令人心旷神怡。"
        }
      ]
    }
  ],
  "usage": {
    "total_tokens": 0,
    "input_tokens": 0,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 0,
    "output_tokens_details": {
      "reasoning_tokens": 0
    }
  },
  "request_id": "example-request-id"
}
```

<p align="center">
  <small>© 2026 DMXAPI wan2.6-image 图文混排</small>
</p>
