# qwen-image-2.0-pro 多图融合 API 使用文档

基于阿里云通义千问 qwen-image-2.0-pro 模型的多图融合接口，支持同时传入 1-3 张参考图像，通过自然语言提示词精确控制融合效果。模型可将不同图像中的主体、风格、场景无缝合并，支持 512×512 至 2048×2048 分辨率输出，内置提示词智能改写功能可自动优化简洁的描述，并通过随机种子参数实现相对可复现的生成结果。

## 🌐 请求地址

```
https://www.dmxapi.cn/v1/responses
```

:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。如果怀疑密钥已泄露，请立即前往 DMXAPI 官网重新生成。
:::

## 🤖 模型名称

- `qwen-image-2.0-pro`

## 💻 多图融合示例代码

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
    "Content-Type": "application/json",
    "Authorization": f"{api_key}",
}

# ═══════════════════════════════════════════════════════════════
# 步骤3: 配置请求参数
# ═══════════════════════════════════════════════════════════════

payload = {
    # 【model】(string, 必填) 模型名称
    "model": "qwen-image-2.0-pro",
    "input": {
        "messages": [
            {
                # 【role】(string, 必填) 消息发送者角色，必须设置为 "user"
                "role": "user",
                "content": [
                    {
                        # 【image】(string, 必填) 输入图像的 URL 或 Base64 编码数据
                        # 支持传入 1-3 张图像，多图输入时按数组顺序定义图像顺序
                        # 输出图像的比例以最后一张图像为准
                        # 支持格式: JPG、JPEG、PNG、BMP、TIFF、WEBP、GIF（动图仅处理第一帧）
                        # 建议分辨率: 宽和高均在 384px 至 3072px 之间，图像大小不超过 10MB
                        # 支持公网 URL（HTTP/HTTPS）、OSS 临时 URL 或 Base64 编码字符串
                        "image": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260310/rdsgaa/image+%2815%29.png"
                    },
                    {
                        # 第二张输入图像（图二），作为多图融合的参考素材
                        "image": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260310/qokhtl/image+%2816%29.png"
                    },
                    {
                        # 【text】(string, 必填) 正向提示词，描述期望生成的图像内容、风格和构图
                        # 支持中英文，长度不超过 800 个字符（汉字、字母、数字或符号各计 1 个字符）
                        # 超出部分会自动截断，内容中可引用"图一"、"图二"等指代具体输入图
                        "text": "使用图一的城市照片作为底图。请勿更改照片中的真实建筑、街道、车辆或人物。保持照片的真实性。三个图二中的卡通形象在建筑物周围，一个趴在建筑物上方，一个从建筑物的右边探出头来，一个坐在建筑物前的空地上。该形象应采用扁平化的图形风格绘制，轮廓清晰，类似于壁画或海报插图。"
                    }
                ]
            }
        ],
        "parameters": {
            # 【n】(integer, 可选) 输出图像的数量
            # 取值范围: 1-6，默认值为 1
            "n": 1,
            # 【negative_prompt】(string, 可选) 反向提示词，描述不希望在画面中出现的内容
            # 支持中英文，长度上限 500 个字符，超出部分自动截断
            # 示例值: 低分辨率、错误、最差质量、低质量、残缺、多余的手指、比例不良等
            "negative_prompt": " ",
            # 【prompt_extend】(bool, 可选) 是否开启提示词智能改写
            # 默认值为 true，开启后模型会自动优化正向提示词，对简单提示词效果提升明显
            "prompt_extend": True,
            # 【watermark】(bool, 可选) 是否在图像右下角添加 "Qwen-Image" 水印
            # 默认值为 false
            "watermark": False,
            # 【size】(string, 可选) 输出图像的分辨率，格式为"宽*高"
            # 图像总像素需在 512*512 至 2048*2048 之间
            # 默认总像素数接近 1024*1024，宽高比与最后一张输入图相近
            # 系统会将指定尺寸调整为最接近的 16 的倍数输出
            # 常见比例推荐: 1:1 → 1024*1024, 16:9 → 1920*1080, 9:16 → 1080*1920
            "size": "2048*2048",
            # 【seed】(integer, 可选) 随机数种子
            # 取值范围: [0, 2147483647]，若不提供则自动使用随机数种子
            # 使用相同 seed 可使生成内容保持相对稳定（不能保证每次结果完全一致）
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
          "text": "https://dashscope-7c2c.oss-accelerate.aliyuncs.com/7d/b6/20260327/f22125ef/55d819a9-750b-48ab-b24e-dcb5af604642.png?Expires=1775216102&OSSAccessKeyId=LTAI5tPxpiCM2hjmWrFXrym1&Signature=Pnm%2BMgXI2pP%2F7CTDyxGE5Ddonlg%3D"
        }
      ]
    }
  ],
  "request_id": "e8a7817d-981d-40a9-a1b9-400a0bc99433",
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
  <small>© 2026 DMXAPI qwen-image-2.0-pro 多图融合</small>
</p>
