# wan2.7-image-pro 图片编辑 API 使用文档

万相2.7 image专业版图片编辑接口，通过 `/v1/responses` 端点调用，支持多图参考输入（最多9张），可实现涂鸦喷绘、风格迁移、图像融合等多种创意编辑效果。图像编辑场景下输出分辨率最高支持2K（2048×2048），并提供自定义颜色主题（3-10种颜色）、随机种子固定等精细化控制参数。

## 📡 请求地址

```
https://www.dmxapi.cn/v1/responses
```

:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。如果怀疑密钥已泄露，请立即前往 DMXAPI 官网重新生成。
:::

## 🤖 模型名称

- `wan2.7-image-pro`

## 🎨 图片编辑示例代码

```python
import requests
import json

# 步骤1: 配置 API 连接信息

# DMXAPI 服务端点地址
url = "https://www.dmxapi.cn/v1/responses"

# DMXAPI 密钥 (请替换为您自己的密钥)
api_key = "sk-******************************************"

# 步骤2: 配置请求头

headers = {
    "Content-Type": "application/json",      # 指定请求体为 JSON 格式
    "Authorization": f"{api_key}",           # token 认证方式
}

# 步骤3: 配置请求参数

payload = {
    # 【model】(string, 必选) 模型名称
    "model": "wan2.7-image-pro",
    "input": {
        "messages": [
            {
                # 【role】(string, 必选) 消息角色，固定设置为 "user"，当前仅支持单轮对话
                "role": "user",
                "content": [
                    # 【image】(string, 可选) 输入图像的URL或Base64编码字符串
                    # 格式支持: JPEG、JPG、PNG（不支持透明通道）、BMP、WEBP
                    # 图像分辨率: 宽高均在 [240, 8000] 像素范围内，宽高比范围 [1:8, 8:1]
                    # 文件大小: 不超过 20MB
                    # 数量限制: 可传入 0-9 张图片，多图时按数组顺序定义图像顺序（图1、图2...）
                    # URL格式: 支持 HTTP/HTTPS 公网可访问 URL
                    # Base64格式: data:{MIME_type};base64,{base64_data}
                    {"image": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251229/pjeqdf/car.webp"},
                    {"image": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251229/xsunlm/paint.webp"},
                    # 【text】(string, 可选) 用户输入提示词，支持中英文
                    # 长度不超过 5000 个字符（每个汉字、字母、数字或符号计为一个字符），超过部分自动截断
                    {"text": "把图2的涂鸦喷绘在图1的汽车上"},
                ],
            }
        ]
    },
    "parameters": {
        # 【enable_sequential】(boolean, 可选) 控制生图模式
        # false: 默认值，关闭组图输出模式（普通生图）
        # true: 启用组图输出模式（多图联动生成）
        "enable_sequential": False,
        # 【size】(string, 可选) 输出图片分辨率，支持两种指定方式（不可混用）
        # 方式一（推荐）：指定规格档位
        #   图像编辑场景: "1K"(1024×1024) / "2K"(2048×2048，默认)，不支持4K
        #   文生图场景(wan2.7-image-pro): 额外支持 "4K"(4096×4096)
        # 方式二：直接指定宽高像素值（如 "1024*768"）
        #   图像编辑场景: 总像素在 [768×768, 2048×2048]，宽高比范围 [1:8, 8:1]
        #   有图片输入时输出宽高比与最后一张输入图像一致
        "size": "2K",
        # 【n】(int, 可选) 生成图像数量
        # 关闭组图模式时: 取值范围 1-4，默认 4
        # 开启组图模式时: 最大生成数量 1-12，默认 12，实际数量由模型决定且不超过 n
        # 注意: n 直接影响费用，费用 = 单价 × 成功生成的图片张数
        "n": 1,
        # 【watermark】(bool, 可选) 是否添加水印标识
        # false: 默认值，不添加水印
        # true: 添加水印，水印位于图片右下角，文案固定为"AI生成"
        "watermark": False,
        # 【seed】(integer, 可选) 随机数种子，取值范围 [0, 2147483647]
        # 使用相同的 seed 可使生成内容保持相对稳定，不提供时算法自动使用随机种子
        # 注意: 模型生成具有概率性，相同 seed 不能保证每次结果完全一致
        "seed": 42,
        # 【color_palette】(array, 可选) 自定义颜色主题
        # 包含颜色(hex)和占比(ratio)的对象数组，需包含 3-10 种颜色，推荐设置 8 种
        # 仅在关闭组图模式(enable_sequential=false)时可用
        "color_palette": [
            {
                # 【hex】(string, 必选) 十六进制(HEX)格式的色值，如 "#FF5733"
                # 【ratio】(string, 必选) 颜色所占百分比，精确到小数点后两位（如 "25.00%"）
                # 注意: 所有 ratio 值相加总和必须为 100.00%
                "hex": "#FF5733", "ratio": "25.00%"
            },
            {"hex": "#33FF57", "ratio": "25.00%"},
            {"hex": "#3357FF", "ratio": "25.00%"},
            {"hex": "#F0E68C", "ratio": "25.00%"},
        ],
    },
}

# 步骤4: 发送请求并输出结果

# 发送 POST 请求到 API 服务器
response = requests.post(url, headers=headers, json=payload)

# 格式化输出 JSON 响应
# - indent=2: 缩进 2 空格，便于阅读
# - ensure_ascii=False: 正确显示中文字符
print(json.dumps(response.json(), indent=2, ensure_ascii=False))
```

## 📄 返回示例

```json
{
  "output": [
    {
      "type": "message",
      "content": [
        {
          "type": "image",
          "text": "https://dashscope-7c2c.oss-accelerate.aliyuncs.com/1d/2a/20260407/24cd1d9a/58556f07-0317-48d4-a902-e8441881fd5c_0.png?Expires=1775662669&OSSAccessKeyId=LTAI5tPxpiCM2hjmWrFXrym1&Signature=%2FWwLujOg%2BEjVhevsVkeobR80Zm4%3D"
        }
      ]
    }
  ],
  "request_id": "6c3e58b0-1547-91a6-9747-6aa1dc22f23b",
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
  }
}
```

<p align="center">
  <small>© 2026 DMXAPI wan2.7-image-pro 图片编辑</small>
</p>
