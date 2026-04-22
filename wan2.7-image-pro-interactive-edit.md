# wan2.7-image-pro 交互式编辑 API 使用文档

万相 wan2.7-image-pro 交互式编辑接口基于万相 2.7 多模态大模型，通过 `/v1/responses` 端点调用，支持将指定图片中的元素自然融合到另一张图片的指定区域。借助 `bbox_list` 参数框选目标区域，实现精准的跨图像元素迁移与场景光线融合，支持最高 2K（2048×2048）分辨率输出，生成数量最多 4 张（组图模式最多 12 张），并可通过 `color_palette`（3-10 种颜色）和 `seed` 参数进一步控制色彩风格与生成一致性。

## 🔗 请求地址

```
https://www.dmxapi.cn/v1/responses
```

:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。如果怀疑密钥已泄露，请立即前往 DMXAPI 官网重新生成。
:::

## 🤖 模型名称

- `wan2.7-image-pro`

## 🖼️ 交互式编辑示例代码

```python
import requests
import json

# 步骤1: 配置 API 连接信息

# DMXAPI 服务端点地址
url = "https://www.dmxapi.cn/v1/responses"

# DMXAPI 密钥 (请替换为您自己的密钥)
# 获取方式: 登录 DMXAPI 官网 -> 个人中心 -> API 密钥管理
api_key = "sk-******************************************"

# 步骤2: 配置请求头

headers = {
    "Content-Type": "application/json",      # 指定请求体为 JSON 格式
    "Authorization": f"{api_key}",           # token 认证方式
}

# 步骤3: 配置请求参数

payload = {
    # 【model】(string, 必填) 模型名称
    "model": "wan2.7-image-pro",
    "input": {
        # 【messages】(array, 必填) 请求内容数组，当前仅支持单轮对话
        # 即传入一组 role、content 参数，不支持多轮对话
        "messages": [
            {
                # 【role】(string, 必填) 消息角色，固定设置为 "user"
                "role": "user",
                "content": [
                    # 【image】(string, 可选) 输入图像的 URL 或 Base64 编码字符串
                    # 支持格式: JPEG、JPG、PNG（不支持透明通道）、BMP、WEBP
                    # 分辨率限制: 宽高范围均为 [240, 8000] 像素，宽高比范围 [1:8, 8:1]
                    # 文件大小: 不超过 20MB
                    # 图像数量: 可传入 0-9 张图片
                    # 多图时按 content 数组顺序定义图像序号（图1、图2...）
                    # 支持公网可访问 URL（HTTP/HTTPS）或 Base64 字符串（data:{MIME};base64,...）
                    {"image": "https://img.alicdn.com/imgextra/i3/O1CN0157XGE51l6iL9441yX_!!6000000004770-49-tps-1104-1472.webp"},
                    {"image": "https://img.alicdn.com/imgextra/i3/O1CN01SfG4J41UYn9WNt4X1_!!6000000002530-49-tps-1696-960.webp"},
                    # 【text】(string, 可选) 用户输入提示词
                    # 支持中英文，长度不超过 5000 个字符（每个汉字/字母/数字/符号各计 1 个字符）
                    # 超过 5000 字符部分会自动截断
                    {"text": "把图1的闹钟放在图2的框选的位置，保持场景和光线融合自然"},
                ],
            }
        ]
    },
    "parameters": {
        # 【bbox_list】(List[List[List[int]]], 可选) 交互式编辑框选区域
        # 列表长度必须与输入图片数量一致；若某张图片无需编辑，在对应位置传入空列表 []
        # 坐标格式: [x1, y1, x2, y2]（左上角 x, 左上角 y, 右下角 x, 右下角 y）
        # 使用原图绝对像素坐标，图像左上角为坐标原点 (0, 0)
        # 单张图片最多支持 2 个边界框
        # 示例: [[], [[989,515,1138,681]]] 表示图1无框选，图2有一个框选区域
        "bbox_list": [[], [[989, 515, 1138, 681]]],

        # 【enable_sequential】(boolean, 可选) 控制生图模式
        # false: 默认值，关闭组图模式；n 取值范围 1-4，默认 4
        # true: 启用组图输出模式；n 取值范围 1-12，默认 12（实际数量由模型决定，不超过 n）
        "enable_sequential": False,

        # 【size】(string, 可选) 输出图片分辨率
        # 交互式编辑场景仅支持 1K 和 2K，不支持 4K
        # "1K": 总像素 1024*1024
        # "2K": 总像素 2048*2048（默认值）
        # 当有图片输入时，输出宽高比与最后一张输入图像一致，并缩放至选定分辨率
        # 也可指定宽高像素值，其他场景总像素在 [768*768, 2048*2048] 之间，宽高比 [1:8, 8:1]
        "size": "2K",

        # 【n】(int, 可选) 生成图像数量，直接影响费用（费用 = 单价 × 成功生成张数）
        # 关闭组图模式时: 取值范围 1-4，默认 4
        # 开启组图模式时: 取值范围 1-12，默认 12（实际数量由模型决定，不超过 n）
        "n": 1,

        # 【watermark】(bool, 可选) 是否添加水印标识
        # false: 默认值，不添加水印
        # true: 在图片右下角添加固定文案"AI生成"水印
        "watermark": False,

        # 【seed】(integer, 可选) 随机数种子
        # 取值范围: [0, 2147483647]
        # 使用相同 seed 可使生成结果保持相对稳定（因模型具有概率性，不能保证完全一致）
        # 若不提供，算法将自动使用随机数种子
        "seed": 42,

        # 【color_palette】(array, 可选) 自定义颜色主题
        # 需包含 3-10 种颜色，推荐设置 8 种；仅在 enable_sequential=false 时可用
        # 每个颜色对象包含以下必填属性:
        #   hex (string, 必填): 十六进制 HEX 格式色值，如 "#FF5733"
        #   ratio (string, 必填): 颜色占比，需精确到小数点后两位（如 "25.00%"）
        # 所有 ratio 值相加总和必须恰好为 100.00%
        "color_palette": [
            {"hex": "#FF5733", "ratio": "25.00%"},
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
          "text": "https://dashscope-7c2c.oss-accelerate.aliyuncs.com/1d/87/20260407/24cd1d9a/02f6ef3b-78e6-4649-9168-b96603080d7f_0.png?Expires=1775662754&OSSAccessKeyId=LTAI5tPxpiCM2hjmWrFXrym1&Signature=pzxJv0B9eHtLMXjfwJXR0Q6o9Dc%3D"
        }
      ]
    }
  ],
  "request_id": "dd2207a6-866c-9fc7-8077-1bc3622bb840",
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
  <small>© 2026 DMXAPI wan2.7-image-pro 交互式编辑</small>
</p>
