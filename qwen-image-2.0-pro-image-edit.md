# qwen-image-2.0-pro 图片编辑 API 使用文档

qwen-image-2.0-pro 是千问图像生成与编辑 Pro 系列模型，专为高精度图像编辑场景设计。支持单图编辑与多图融合，可精确修改画面中的文字内容、增删或移动物体、改变主体动作、迁移图片风格及增强画面细节，具备更强的文字渲染、真实质感和语义遵循能力。输入支持最多 3 张图像，输出支持 1-6 张图像，分辨率总像素范围 512×512 至 2048×2048，图像格式为 PNG。

## 🌐 请求地址

```
https://www.dmxapi.cn/v1/responses
```

:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。如果怀疑密钥已泄露，请立即前往 DMXAPI 官网重新生成。
:::

## 🤖 模型名称

- `qwen-image-2.0-pro`

## 🖼️ 图片编辑 示例代码

```python
import requests
import json

# ═══════════════════════════════════════════════════════════════
# 步骤1: 配置 API 连接信息
# ═══════════════════════════════════════════════════════════════

# DMXAPI 服务端点地址
url = "https://www.dmxapi.cn/v1/responses"

# DMXAPI 密钥 (请替换为您自己的密钥)
# 获取方式: 登录 DMXAPI 官网 -> 个人中心 -> API 密钥管理
api_key = "sk-******************************************"

# ═══════════════════════════════════════════════════════════════
# 步骤2: 配置请求头
# ═══════════════════════════════════════════════════════════════

headers = {
    "Content-Type": "application/json",  # 指定请求体为 JSON 格式
    "Authorization": f"{api_key}",       # token 认证方式
}

# ═══════════════════════════════════════════════════════════════
# 步骤3: 配置请求参数
# ═══════════════════════════════════════════════════════════════

payload = {
    # 【model】(string, 必选) 模型名称
    "model": "qwen-image-2.0-pro",
    "input": {
        "messages": [
            {
                # 【role】(string, 必选) 消息发送者角色，必须设置为 "user"
                "role": "user",
                "content": [
                    {
                        # 【image】(string, 必选) 输入图像的 URL 或 Base64 编码数据
                        # 支持传入 1-3 张图像，多图时按数组顺序定义图像顺序
                        # 多图输入时，输出图像比例以最后一张图为准
                        # 图像格式：JPG、JPEG、PNG、BMP、TIFF、WEBP、GIF（GIF 仅处理第一帧）
                        # 建议分辨率：宽高均在 384-3072 像素之间
                        # 图像大小：不超过 10MB
                        "image": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260310/jiydyi/image+%2818%29-2026-03-10-16-39-59.webp"
                    },
                    {
                        # 【text】(string, 必选) 正向提示词，描述期望生成的图像内容、风格和构图
                        # 支持中英文，长度不超过 800 个字符，超过部分自动截断
                        # content 数组中必须包含且仅包含一个 text 对象，否则将报错
                        "text": "在画面右下角石板路旁、靠近树干根部的位置，以浅灰墨色手写体题写一首七言绝句，字体为行楷风格，笔触自然流畅、略带飞白，大小适中（约占画面高度1/10），与整体水墨淡雅氛围协调。诗文内容为：\"青石桥畔柳风轻， 素手拈花闭目听。 一水碧痕浮旧梦， 半篙烟雨入空舲。\"诗句横向排列，四句分两行书写（前两句一行，后两句一行），末句\"舲\"字右下角钤一枚朱红小印，印文为\"江南\"二字篆书，尺寸约等于单字高度的1/3。"
                    }
                ]
            }
        ],
        "parameters": {
            # 【n】(integer, 可选) 输出图像数量，默认值为 1,可选 1-6 张
            "n": 1,
            # 【negative_prompt】(string, 可选) 反向提示词，描述不希望在画面中出现的内容
            # 支持中英文，长度上限 500 个字符，超过部分自动截断
            # 示例值："低分辨率、错误、最差质量、低质量、残缺、多余的手指、比例不良"
            "negative_prompt": " ",
            # 【prompt_extend】(bool, 可选) 是否开启提示词智能改写，默认值为 true
            # 开启后模型会优化正向提示词，对描述较简单的提示词效果提升明显
            "prompt_extend": True,
            # 【watermark】(bool, 可选) 是否在图像右下角添加 "Qwen-Image" 水印，默认值为 false
            "watermark": False,
            # 【size】(string, 可选) 输出图像分辨率，格式为 "宽*高"，例如 "1024*1536"
            # qwen-image-2.0 系列：总像素需在 512*512 至 2048*2048 之间
            # 系统将实际输出宽高调整为最接近的 16 的倍数（如设置 1033*1032，输出为 1040*1024）
            # 常见比例推荐：1:1(1024*1024) / 2:3(1024*1536) / 3:2(1536*1024) /
            #               9:16(1080*1920) / 16:9(1920*1080)
            "size": "2048*2048",
            # 【seed】(integer, 可选) 随机数种子，取值范围 [0, 2147483647]
            # 使用相同 seed 可使生成内容保持相对稳定，但因模型生成具有概率性，不能保证完全一致
            # 不提供时算法自动使用随机数种子
            "seed": 30
        }
    },
}

# ═══════════════════════════════════════════════════════════════
# 步骤4: 发送请求并输出结果
# ═══════════════════════════════════════════════════════════════

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
          "text": "https://dashscope-7c2c.oss-accelerate.aliyuncs.com/7d/d5/20260327/f22125ef/855a33b2-29fd-4e3b-bce6-a924d939e950.png?Expires=1775216954&OSSAccessKeyId=LTAI5tPxpiCM2hjmWrFXrym1&Signature=iy%2FIyShxENANM0%2BEehitKPSCb1E%3D"
        }
      ]
    }
  ],
  "request_id": "d0721527-9aa2-4853-84a2-f2cfc3993c1a",
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
  <small>© 2026 DMXAPI qwen-image-2.0-pro 图片编辑</small>
</p>
