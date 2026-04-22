# wan2.7-image-pro 组图生成 API 使用文档

万相 2.7 image 专业版（wan2.7-image-pro）的组图生成接口，通过 `/v1/responses` 端点调用，支持在单次请求中生成多达 12 张主题连贯的系列图像。开启组图模式（`enable_sequential: true`）后，模型会依据同一提示词自动输出前后一致的角色/场景图序列，适合电影感分镜、故事板、四季主题等需要视觉连贯性的批量创作场景。输出分辨率支持 1K 和 2K，图像格式为 PNG，带可选水印标识。

## 🌐 请求地址

```
https://www.dmxapi.cn/v1/responses
```

:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。如果怀疑密钥已泄露，请立即前往 DMXAPI 官网重新生成。
:::

## 🤖 模型名称

- `wan2.7-image-pro`

## 🖼️ 组图生成示例代码

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
    # 【Content-Type】(string, 必填) 请求内容类型，固定为 application/json
    "Content-Type": "application/json",
    # 【Authorization】(string, 必填) API Key 身份认证，直接传入密钥字符串
    "Authorization": f"{api_key}",
}

# 步骤3: 配置请求参数

payload = {
    # 【model】(string, 必填) 模型名称
    "model": "wan2.7-image-pro",

    # 【input】(object, 必填) 输入的基本信息
    "input": {
        # 【messages】(array, 必填) 请求内容数组，仅支持单轮对话（一组 role + content），不支持多轮
        "messages": [
            {
                # 【role】(string, 必填) 消息角色，固定为 "user"
                "role": "user",
                # 【content】(array, 必填) 消息内容数组
                "content": [
                    {
                        # 【text】(string, 可选) 用户输入的提示词
                        # 支持中英文，最长 5000 个字符（每个汉字/字母/数字/符号均计为 1 个字符），超出部分自动截断
                        # 组图模式下，建议在提示词中明确描述各张图的场景及角色一致性要求
                        "text": "电影感组图，记录同一只流浪橘猫，特征必须前后一致。第一张：春天，橘猫穿梭在盛开的樱花树下；第二张：夏天，橘猫在老街的树荫下乘凉避暑；第三张：秋天，橘猫踩在满地的金色落叶上；第四张：冬天，橘猫在雪地上走留下足迹。",
                    },
                    # 【image】(string, 可选) 输入图像的 URL 或 Base64 编码字符串（组图生成场景可选传入参考图）
                    # 支持格式: JPEG、JPG、PNG（不支持透明通道）、BMP、WEBP
                    # 图像限制: 宽高均在 [240, 8000] 像素，宽高比 [1:8, 8:1]，单文件不超过 20MB
                    # 数量限制: 可传入 0-9 张图片；多图时在 content 中依次追加多个 image 对象
                    # URL 示例: {"image": "http://example.com/photo.jpg"}
                    # Base64 示例: {"image": "data:image/jpeg;base64,/9j/4AAQ..."}
                ],
            }
        ]
    },

    # 【parameters】(object, 可选) 模型参数配置
    "parameters": {
        # 【enable_sequential】(boolean, 可选) 控制生图模式
        # false: 默认值，标准生图模式
        # true: 启用组图输出模式，模型将生成主题连贯的系列图像
        # 注意: 开启组图模式时，thinking_mode 和 color_palette 参数不生效
        "enable_sequential": True,

        # 【n】(int, 可选) 生成图像数量
        # 组图模式关闭时: 生成图像数量，取值范围 [1, 4]，默认为 4
        # 组图模式开启时: 最大生成图像数量，取值范围 [1, 12]，默认为 12
        #   实际数量由模型自动决定，不超过 n 的值
        # 注意: n 直接影响费用，费用 = 单价 × 成功生成的图片张数
        "n": 4,

        # 【size】(string, 可选) 输出图像分辨率，支持两种方式（不可混用）
        # 方式一（推荐）- 指定规格:
        #   "1K": 1024×1024 总像素
        #   "2K": 2048×2048 总像素（默认值）
        #   "4K": 4096×4096 总像素（仅文生图且非组图模式可用）
        # 方式二 - 指定宽高像素值（如 "1024*768"）:
        #   组图/图像编辑场景: 总像素 [768×768, 2048×2048]，宽高比 [1:8, 8:1]
        # 注意: 有图片输入时，输出宽高比与输入图像（多图时为最后一张）一致并缩放到目标规格
        "size": "2K",

        # 【watermark】(bool, 可选) 是否添加水印标识
        # false: 默认值，不添加水印
        # true: 在图片右下角添加固定文案 "AI生成" 水印
        "watermark": True,

        # 【seed】(integer, 可选) 随机数种子，取值范围 [0, 2147483647]
        # 使用相同 seed 可使生成内容保持相对稳定；不提供时算法自动使用随机种子
        # 注意: 模型生成具有概率性，相同 seed 不保证每次结果完全一致
        "seed": 22,

        # 【thinking_mode】(boolean, 可选) 是否开启思考模式，默认为 true（开启）
        # 仅在关闭组图模式（enable_sequential=false）且无图片输入时生效
        # true: 模型增强推理能力，提升出图质量，但会增加生成耗时
        # false: 关闭思考模式，生成速度更快
        # 注意: 组图模式下此参数不生效
        # "thinking_mode": True,

        # 【color_palette】(array, 可选) 自定义颜色主题，包含 3-10 种颜色（推荐 8 种）
        # 仅在关闭组图模式（enable_sequential=false）时可用
        # 示例:
        # "color_palette": [
        #     {"hex": "#FF6B6B", "ratio": "30.00%"},
        #     {"hex": "#4ECDC4", "ratio": "40.00%"},
        #     {"hex": "#45B7D1", "ratio": "30.00%"},
        # ]
        # 【hex】(string, 必填) 十六进制（HEX）格式色值，如 "#FF6B6B"
        # 【ratio】(string, 必填) 颜色占比，精确到小数点后两位（如 "25.00%"），所有 ratio 总和必须为 100.00%

        # 【bbox_list】(List[List[List[int]]], 可选) 交互式编辑框选区域（仅图像编辑场景使用）
        # 列表长度必须与输入图片数量一致；无需编辑的图片对应位置传入空列表 []
        # 坐标格式: [x1, y1, x2, y2]（左上角坐标，使用原图绝对像素值）
        # 单张图片最多支持 2 个边界框
        # 示例（3 张图片，第 2 张无框选）:
        # "bbox_list": [[[0, 0, 100, 100]], [], [[10, 10, 50, 50]]]
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

## 📋 返回示例

```json
{
  "output": [
    {
      "type": "message",
      "content": [
        {
          "type": "image",
          "text": "https://dashscope-7c2c.oss-accelerate.aliyuncs.com/1d/e6/20260407/ef3b0431/001193c8-a539-404e-9d30-2e31f60c98fa_0.png?Expires=1775663258&OSSAccessKeyId=LTAI5tPxpiCM2hjmWrFXrym1&Signature=Fj%2BQSEgGq5Qymf8gAVO70wlsTrw%3D"
        },
        {
          "type": "image",
          "text": "https://dashscope-7c2c.oss-accelerate.aliyuncs.com/1d/c8/20260407/ef3b0431/001193c8-a539-404e-9d30-2e31f60c98fa_1.png?Expires=1775663258&OSSAccessKeyId=LTAI5tPxpiCM2hjmWrFXrym1&Signature=2Um5PgvEivXY2TDuhlmA654xLAU%3D"
        },
        {
          "type": "image",
          "text": "https://dashscope-7c2c.oss-accelerate.aliyuncs.com/1d/0a/20260407/ef3b0431/001193c8-a539-404e-9d30-2e31f60c98fa_2.png?Expires=1775663258&OSSAccessKeyId=LTAI5tPxpiCM2hjmWrFXrym1&Signature=7BILTTG5u%2Fy3VpWTmZU3yYnFAFc%3D"
        },
        {
          "type": "image",
          "text": "https://dashscope-7c2c.oss-accelerate.aliyuncs.com/1d/f5/20260407/ef3b0431/001193c8-a539-404e-9d30-2e31f60c98fa_3.png?Expires=1775663258&OSSAccessKeyId=LTAI5tPxpiCM2hjmWrFXrym1&Signature=7NiILD54rcGvvNXzuksMcWVbF2c%3D"
        }
      ]
    }
  ],
  "request_id": "cda24d4e-c190-9dfb-9365-b49ad1b15c33",
  "usage": {
    "total_tokens": 20000,
    "input_tokens": 0,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 20000,
    "output_tokens_details": {
      "reasoning_tokens": 0
    }
  }
}
```


<p align="center">
  <small>© 2026 DMXAPI wan2.7-image-pro 组图生成</small>
</p>
