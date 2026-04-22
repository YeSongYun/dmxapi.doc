# wan2.7-image-pro 文生图 API 使用文档

wan2.7-image-pro 是万相2.7图像生成系列中的专业版模型，通过 `/v1/responses` 端点调用，支持文生图、图像编辑、多图参考生成等多种场景。专业版独家支持 4K（4096×4096 像素）超高清输出，相比标准版总像素提升 4 倍，适合高精度商业图像生成需求。内置 `thinking_mode` 增强推理模式可提升出图质量，`color_palette` 参数支持 3-10 种自定义颜色主题，`seed` 参数实现相对稳定的结果复现。

## 🌐 请求地址

```
https://www.dmxapi.cn/v1/responses
```

:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。如果怀疑密钥已泄露，请立即前往 DMXAPI 官网重新生成。
:::

## 🤖 模型名称

- `wan2.7-image-pro`

## 🖼️ 文生图 示例代码

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
    # 【model】(string, 必选) 模型名称
    "model": "wan2.7-image-pro",

    # 【input】(object, 必选) 输入的基本信息
    "input": {
        # 【messages】(array, 必选) 请求内容数组
        # 仅支持单轮对话，即传入一组 role+content 参数，不支持多轮对话
        "messages": [
            {
                # 【role】(string, 必选) 消息的角色，固定设置为 "user"
                "role": "user",
                # 【content】(array, 必选) 消息内容数组
                "content": [
                    # 【text】(string, 可选) 用户输入提示词
                    # 支持中英文，长度不超过 5000 个字符
                    # 每个汉字、字母、数字或符号各计 1 个字符，超出部分自动截断
                    {"text": "一间有着精致窗户的花店，漂亮的木质门，摆放着花朵"}
                ],
            }
        ]
    },

    # 【parameters】(object, 可选) 模型参数配置
    "parameters": {
        # 【enable_sequential】(boolean, 可选) 控制生图模式
        # false：默认值，普通生图模式
        # true：启用组图输出模式（支持最多12张组图）
        # 注意：color_palette 参数仅在 enable_sequential=false 时可用
        "enable_sequential": False,

        # 【size】(string, 可选) 输出图片分辨率，支持两种方式（不可混用）
        # 方式一（推荐）：指定分辨率规格
        #   "1K"（1024*1024）/ "2K"（2048*2048，默认）/ "4K"（4096*4096，仅pro且仅文生图）
        # 方式二：指定宽高像素值，如 "1024*768"
        #   文生图场景：总像素范围 [768*768, 4096*4096]，宽高比范围 [1:8, 8:1]
        #   图像编辑/其他场景：总像素范围 [768*768, 2048*2048]，宽高比范围 [1:8, 8:1]
        # 输出图片实际像素值可能与指定值存在微小差异
        "size": "2K",

        # 【n】(integer, 可选) 生成图像数量，直接影响费用（费用 = 单价 × 成功生成张数）
        # 关闭组图模式（enable_sequential=false）：取值范围 [1, 4]，默认为 4
        # 开启组图模式（enable_sequential=true）：取值范围 [1, 12]，默认为 12
        #   开启组图时实际生成数量由模型决定，不超过 n
        "n": 1,

        # 【watermark】(boolean, 可选) 是否添加水印
        # false：默认值，不添加水印
        # true：在图片右下角添加"AI生成"字样水印
        "watermark": False,

        # 【thinking_mode】(boolean, 可选) 是否开启思考模式，默认为 true
        # 仅在关闭组图模式（enable_sequential=false）且无图片输入时生效
        # true：增强推理能力，提升出图质量，但会增加生成耗时
        # false：关闭思考模式，生成速度更快
        "thinking_mode": True,

        # 【seed】(integer, 可选) 随机数种子，取值范围 [0, 2147483647]
        # 使用相同的 seed 可使生成内容保持相对稳定（注意：不保证每次结果完全一致）
        # 若不提供，算法将自动使用随机数种子
        "seed": 42,

        # 【color_palette】(array, 可选) 自定义颜色主题
        # 包含 3 至 10 种颜色（推荐设置 8 种），所有颜色的 ratio 总和必须精确为 100.00%
        # 仅在关闭组图模式（enable_sequential=false）时可用
        "color_palette": [
            {
                # 【hex】(string, 必选) 十六进制 (HEX) 格式的色值，如 "#FF5733"
                # 【ratio】(string, 必选) 颜色占比，需精确到小数点后两位，如 "25.00%"
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
          "text": "https://dashscope-7c2c.oss-accelerate.aliyuncs.com/1d/2c/20260407/312f092c/c9ed4aa5-9149-4d35-be62-0a7090f20ced_0.png?Expires=1775662540&OSSAccessKeyId=LTAI5tPxpiCM2hjmWrFXrym1&Signature=zRSrAAlCy6qeY1OyfSqe%2FoX4Ox0%3D"
        }
      ]
    }
  ],
  "request_id": "d77fd5ac-0d3b-94c8-82d5-325021417545",
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
  <small>© 2026 DMXAPI wan2.7-image-pro 文生图</small>
</p>
