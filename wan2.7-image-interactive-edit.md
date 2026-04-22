# wan2.7-image 交互式编辑 API 使用文档

wan2.7-image 交互式编辑接口通过 `/v1/responses` 端点调用，支持将多张输入图像的指定区域（通过 `bbox_list` 框选坐标定义）进行融合编辑，实现跨图元素迁移与自然场景合成。输入最多 9 张图像，通过边界框坐标精准定位编辑区域，输出最高 2K（2048×2048）分辨率图像，并支持颜色主题定制（`color_palette`，3–10 种颜色）和随机种子（`seed`）控制生成稳定性。

## 🖼️ 请求地址

```
https://www.dmxapi.cn/v1/responses
```

:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。如果怀疑密钥已泄露，请立即前往 DMXAPI 官网重新生成。
:::

## 🤖 模型名称

- `wan2.7-image`

## ✏️ 交互式编辑示例代码

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
    "Content-Type": "application/json",      # 指定请求体为 JSON 格式
    "Authorization": f"{api_key}",           # token 认证方式
}

# ═══════════════════════════════════════════════════════════════
# 步骤3: 配置请求参数
# ═══════════════════════════════════════════════════════════════

payload = {
    # 【model】(string, 必选) 模型名称
    "model": "wan2.7-image",

    # 【input】(object, 必选) 输入的基本信息
    "input": {
        # 【messages】(array, 必选) 请求内容数组
        # 当前仅支持单轮对话，即传入一组 role、content 参数，不支持多轮对话
        "messages": [
            {
                # 【role】(string, 必选) 消息的角色，固定设置为 "user"
                "role": "user",
                # 【content】(array, 必选) 消息内容数组
                # 可混合传入 image 和 text 对象，图像数量范围 0-9 张
                # 图像格式支持: JPEG、JPG、PNG（不支持透明通道）、BMP、WEBP
                # 图像分辨率: 宽高范围均为 [240, 8000] 像素，宽高比范围 [1:8, 8:1]
                # 文件大小: 单张不超过 20MB
                # 支持公网可访问 URL 或 Base64 编码字符串（格式: data:{MIME};base64,{data}）
                "content": [
                    {"image": "https://img.alicdn.com/imgextra/i3/O1CN0157XGE51l6iL9441yX_!!6000000004770-49-tps-1104-1472.webp"},
                    {"image": "https://img.alicdn.com/imgextra/i3/O1CN01SfG4J41UYn9WNt4X1_!!6000000002530-49-tps-1696-960.webp"},
                    {"text": "把图1的闹钟放在图2的框选的位置，保持场景和光线融合自然"},
                ],
            }
        ]
    },

    # 【parameters】(object, 可选) 模型参数配置
    "parameters": {
        # 【bbox_list】(List[List[List[int]]], 可选) 交互式编辑框选区域
        # 列表长度必须与输入图片数量一致，若某张图片无需框选则传入空列表 []
        # 坐标格式: [x1, y1, x2, y2]（左上角x, 左上角y, 右下角x, 右下角y）
        # 使用原图绝对像素坐标，左上角坐标为 (0, 0)
        # 限制: 单张图片最多支持 2 个边界框
        # 示例: 图1无框，图2有一个框选区域 (989,515)→(1138,681)
        "bbox_list": [[], [[989, 515, 1138, 681]]],

        # 【enable_sequential】(boolean, 可选) 控制生图模式
        # false: 默认值，关闭组图输出模式
        # true: 启用组图输出模式（开启后 n 的取值范围变为 1-12，默认 12）
        "enable_sequential": False,

        # 【size】(string, 可选) 输出图片分辨率
        # wan2.7-image: 支持 "1K"(1024*1024)、"2K"(2048*2048，默认)，不支持 "4K"
        # 交互式编辑场景仅支持 1K / 2K，不支持 4K
        # 有图片输入时输出宽高比与输入图像（多图时为最后一张）一致，并缩放到选定分辨率
        # 也支持直接指定像素值（总像素在 [768*768, 2048*2048] 之间，宽高比 [1:8, 8:1]）
        "size": "2K",

        # 【n】(int, 可选) 生成图像数量，直接影响费用（费用 = 单价 × 成功生成张数）
        # 关闭组图模式时: 取值范围 1-4，默认为 4
        # 开启组图模式时: 取值范围 1-12，默认为 12，实际数量由模型决定且不超过 n
        "n": 1,

        # 【watermark】(bool, 可选) 是否添加水印标识
        # 水印位于图片右下角，文案固定为"AI生成"
        # false: 默认值，不添加水印
        # true: 添加水印
        "watermark": False,

        # 【seed】(integer, 可选) 随机数种子
        # 取值范围: [0, 2147483647]
        # 使用相同的 seed 值可使生成内容保持相对稳定，但不能保证每次完全一致
        # 若不提供，算法将自动使用随机数种子
        "seed": 42,

        # 【color_palette】(array, 可选) 自定义颜色主题
        # 包含颜色(hex)和占比(ratio)的对象数组，需要包含 3-10 种颜色，推荐设置为 8 种
        # 仅当关闭组图模式（enable_sequential=false）时可用
        # 所有 ratio 值相加总和必须为 100.00%
        "color_palette": [
            {
                # 【hex】(string, 必选) 十六进制(HEX)格式的色值
                # 【ratio】(string, 必选) 颜色所占百分比，精确到小数点后两位，如 "25.00%"
                "hex": "#FF5733", "ratio": "25.00%"
            },
            {"hex": "#33FF57", "ratio": "25.00%"},
            {"hex": "#3357FF", "ratio": "25.00%"},
            {"hex": "#F0E68C", "ratio": "25.00%"},
        ],
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
          "text": "https://dashscope-7c2c.oss-accelerate.aliyuncs.com/1d/0d/20260407/7423dd75/8800e83e-e773-4857-92b4-11c9233cbc61_0.png?Expires=1775663933&OSSAccessKeyId=LTAI5tPxpiCM2hjmWrFXrym1&Signature=%2FKdGm9xoVzPU295MJ0rPs29fsFI%3D"
        }
      ]
    }
  ],
  "request_id": "1835cba1-91a6-9ad6-8f98-a79a8cb4cf6a",
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
  <small>© 2026 DMXAPI wan2.7-image 交互式编辑</small>
</p>
