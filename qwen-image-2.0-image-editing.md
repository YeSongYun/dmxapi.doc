# qwen-image-2.0 图片编辑 API 使用文档

qwen-image-2.0 是阿里云通义千问图像生成与编辑加速版模型，兼顾效果与响应速度。支持 1-3 张图像输入、1-6 张图像输出，可精确修改图内文字、增删或移动物体、改变主体动作、迁移图片风格及增强画面细节，具备多图融合能力。支持正向与反向提示词、智能提示词改写（prompt_extend）、自定义输出分辨率（最高 2048×2048 像素）、随机种子控制及可选水印，输出格式为 PNG，生成结果链接有效期 24 小时。

## 🌐 请求地址

```
https://www.dmxapi.cn/v1/responses
```

:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。如果怀疑密钥已泄露，请立即前往 DMXAPI 官网重新生成。
:::

## 🤖 模型名称

- `qwen-image-2.0`

## 📝 图片编辑示例代码

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
    # 指定请求体为 JSON 格式
    "Content-Type": "application/json",
    # token 认证方式
    "Authorization": f"{api_key}",
}

# ═══════════════════════════════════════════════════════════════
# 步骤3: 配置请求参数
# ═══════════════════════════════════════════════════════════════

payload = {
    # 【model】(string, 必填) 模型名称
    "model": "qwen-image-2.0",
    "input": {
        # 【messages】(array, 必填) 请求内容数组
        # 当前仅支持单轮对话，数组内有且只有一个对象
        "messages": [
            {
                # 【role】(string, 必填) 消息发送者角色，必须设置为 "user"
                "role": "user",
                # 【content】(array, 必填) 消息内容，包含 1-3 张图像及单个编辑指令
                # 注意: content 数组中必须包含且仅包含一个 text 对象，否则将报错
                "content": [
                    {
                        # 【image】(string, 必填) 输入图像的 URL 或 Base64 编码数据
                        # 支持传入 1-3 张图像，多图输入时按数组顺序定义图像顺序
                        # 多图输入时，输出图像的宽高比以最后一张图像为准
                        # 支持格式: JPG、JPEG、PNG、BMP、TIFF、WEBP、GIF（GIF 仅处理第一帧）
                        # 建议分辨率: 宽和高均在 384-3072 像素之间，分辨率过低导致效果模糊，过高增加处理时长
                        # 图像大小: 不超过 10MB
                        # 支持公网 URL（HTTP/HTTPS）、OSS 临时 URL 及 Base64 编码字符串
                        "image": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260310/jiydyi/image+%2818%29-2026-03-10-16-39-59.webp"
                    },
                    {
                        # 【text】(string, 必填) 正向提示词，描述期望生成的图像内容、风格和构图
                        # 支持中英文，长度不超过 800 个字符（每个汉字、字母、数字或符号计 1 个字符）
                        # 超出长度上限的部分将自动截断
                        "text": "在画面右下角石板路旁、靠近树干根部的位置，以浅灰墨色手写体题写一首七言绝句，字体为行楷风格，笔触自然流畅、略带飞白，大小适中（约占画面高度1/10），与整体水墨淡雅氛围协调。诗文内容为：\"青石桥畔柳风轻， 素手拈花闭目听。 一水碧痕浮旧梦， 半篙烟雨入空舲。\"诗句横向排列，四句分两行书写（前两句一行，后两句一行），末句\"舲\"字右下角钤一枚朱红小印，印文为\"江南\"二字篆书，尺寸约等于单字高度的1/3。"
                    }
                ]
            }
        ],
        # 【parameters】(object, 可选) 控制图像生成的附加参数
        "parameters": {
            # 【n】(integer, 可选) 输出图像的数量，默认值为 1， 可选 1-6 张
            "n": 1,
            # 【negative_prompt】(string, 可选) 反向提示词，描述不希望在画面中出现的内容
            # 支持中英文，长度上限 500 个字符，超出部分自动截断
            # 示例: "低分辨率、错误、最差质量、低质量、残缺、多余的手指、比例不良"
            "negative_prompt": " ",
            # 【prompt_extend】(bool, 可选) 是否开启提示词智能改写，默认值为 true
            # 开启后模型会优化正向提示词，对描述较简单的提示词效果提升明显
            # 不支持 qwen-image-edit 模型
            "prompt_extend": True,
            # 【watermark】(bool, 可选) 是否在图像右下角添加 "Qwen-Image" 水印，默认值为 false
            "watermark": False,
            # 【size】(string, 可选) 设置输出图像的分辨率，格式为 "宽*高"，例如 "1024*1536"
            # qwen-image-2.0 系列: 图像总像素需在 512*512 至 2048*2048 之间
            # 系统会将实际输出宽高调整为最接近的 16 的倍数，例如设置 1033*1032，输出为 1040*1024
            # 常见比例推荐: 
                          # 1:1: 1024*1024、1536*1536
                          # 2:3: 768*1152、1024*1536
                          # 3:2: 1152*768、1536*1024
                          # 3:4: 960*1280、1080*1440
                          # 4:3: 1280*960、1440*1080
                          # 9:16: 720*1280、1080*1920
                          # 16:9: 1280*720、1920*1080
                          # 21:9: 1344*576、2048*872
            "size": "2048*2048",
            # 【seed】(integer, 可选) 随机数种子，取值范围 [0, 2147483647]
            # 使用相同的 seed 值可使生成内容保持相对稳定，但不能保证完全一致
            # 若不提供，算法将自动使用随机数种子
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

## 📋 返回示例

```json
{
  "output": [
    {
      "type": "message",
      "content": [
        {
          "type": "image",
          "text": "https://dashscope-7c2c.oss-accelerate.aliyuncs.com/7d/e4/20260327/5abe4571/442a1510-da92-4dd1-a012-cd981cf93de0.png?Expires=1775216825&OSSAccessKeyId=LTAI5tPxpiCM2hjmWrFXrym1&Signature=efiprJ3CihmslEppmITPoWeHjGs%3D"
        }
      ]
    }
  ],
  "request_id": "8167a2a7-9d21-49e3-bd82-4084888e3ccf",
  "usage": {
    "total_tokens": 2000,
    "input_tokens": 0,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 2000,
    "output_tokens_details": {
      "reasoning_tokens": 0
    }
  }
}
```

<p align="center">
  <small>© 2026 DMXAPI qwen-image-2.0 图片编辑</small>
</p>
