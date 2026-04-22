# wan2.7-image 图片编辑 API 使用文档

万相 2.7 图片编辑接口，通过 `/v1/responses` 端点调用，支持将文字指令、参考图（最多 9 张）组合输入，实现涂鸦喷绘、风格迁移、局部修改等多类图像编辑任务。输出分辨率支持 1K（1024²）和 2K（2048²），可自定义颜色主题（3–10 种）、随机种子及水印开关，同一 seed 可使结果相对稳定，适合需要批量生产且风格一致的图像编辑场景。

## 🌐 请求地址

```
https://www.dmxapi.cn/v1/responses
```

:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。如果怀疑密钥已泄露，请立即前往 DMXAPI 官网重新生成。
:::

## 🤖 模型名称

- `wan2.7-image`

## 🖼️ 图片编辑示例代码

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
        # 仅支持单轮对话，即传入一组 role、content，不支持多轮
        "messages": [
            {
                # 【role】(string, 必选) 消息角色，固定为 "user"
                "role": "user",
                # 【content】(array, 必选) 消息内容数组，按顺序传入图像和文本
                "content": [
                    # 【image】(string) 输入图像的公网 URL 或 Base64 编码字符串
                    # 支持格式: JPEG、JPG、PNG（不支持透明通道）、BMP、WEBP
                    # 分辨率: 宽高范围 [240, 8000] 像素，宽高比 [1:8, 8:1]
                    # 文件大小: 不超过 20MB；单次最多传入 0-9 张图片
                    # 多图时按数组顺序定义图像编号（图1、图2…）
                    {"image": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251229/pjeqdf/car.webp"},
                    {"image": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251229/xsunlm/paint.webp"},
                    # 【text】(string) 用户输入提示词
                    # 支持中英文，长度不超过 5000 字符，超过部分自动截断
                    {"text": "把图2的涂鸦喷绘在图1的汽车上"},
                ],
            }
        ]
    },

    # 【parameters】(object, 可选) 模型参数配置
    "parameters": {
        # 【enable_sequential】(boolean, 可选) 控制生图模式
        # false（默认）: 普通生成模式
        # true: 启用组图输出模式（n 最大支持 12，且 color_palette 不可用）
        "enable_sequential": False,

        # 【size】(string, 可选) 输出图片分辨率
        # 图像编辑场景仅支持 1K(1024*1024) 和 2K(2048*2048，默认)，不支持 4K
        # 有图片输入时，输出宽高比与输入图像（多图取最后一张）一致并缩放到选定分辨率
        # 也可直接指定像素值（如 "1024*768"），总像素范围 [768*768, 2048*2048]，宽高比 [1:8, 8:1]
        "size": "2K",

        # 【n】(int, 可选) 生成图像数量
        # 关闭组图模式: 取值范围 1-4，默认为 4
        # 开启组图模式: 取值范围 1-12，默认为 12（实际数量由模型决定且不超过 n）
        # 注意: n 直接影响费用，费用 = 单价 × 成功生成的图片张数
        "n": 1,

        # 【watermark】(bool, 可选) 是否添加水印
        # false（默认）: 不添加水印
        # true: 在图片右下角添加"AI生成"水印
        "watermark": False,

        # 【seed】(integer, 可选) 随机数种子
        # 取值范围: [0, 2147483647]
        # 使用相同的 seed 可使生成内容保持相对稳定，但不保证每次完全一致
        # 不提供时，算法自动使用随机数种子
        "seed": 42,

        # 【color_palette】(array, 可选) 自定义颜色主题
        # 需包含 3-10 种颜色（推荐 8 种），仅在 enable_sequential=false 时可用
        # 所有 ratio 值相加总和必须等于 100.00%
        "color_palette": [
            {
                # 【hex】(string, 必选) 十六进制（HEX）格式的色值，如 "#FF5733"
                # 【ratio】(string, 必选) 颜色所占百分比，需精确到小数点后两位
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
          "text": "https://dashscope-7c2c.oss-accelerate.aliyuncs.com/1d/2b/20260407/7423dd75/ea00aed3-b731-4285-95c8-5b8be08fbb13_0.png?Expires=1775663576&OSSAccessKeyId=LTAI5tPxpiCM2hjmWrFXrym1&Signature=jR1ALqMfl5TH%2Bh%2BGsEwCz0J3yx0%3D"
        }
      ]
    }
  ],
  "request_id": "cad51be3-6838-986c-b1ab-e40d0e19d694",
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
  <small>© 2026 DMXAPI wan2.7-image 图片编辑</small>
</p>
