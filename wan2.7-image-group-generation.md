# wan2.7-image 组图生成 API 使用文档

万相 2.7 image 组图生成接口，基于 `/v1/responses` 端点调用，通过设置 `enable_sequential: true` 启用组图输出模式，支持一次请求生成最多 12 张风格连贯的系列图像，输出分辨率最高 2K（2048×2048）。两个可用模型中，`wan2.7-image-pro` 额外支持 4K 输出（仅文生图、非组图模式），`wan2.7-image` 生成速度更快。组图模式下，角色/场景连贯性由模型自动保障，适合四季组图、故事序列、风格系列等场景。

## 🌐 请求地址

```
https://www.dmxapi.cn/v1/responses
```

:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。如果怀疑密钥已泄露，请立即前往 DMXAPI 官网重新生成。
:::

## 🤖 模型名称
- `wan2.7-image`

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
    # 【Content-Type】(string, 必选) 请求内容类型，固定值
    "Content-Type": "application/json",
    # 【Authorization】(string, 必选) 身份认证，直接传入 API Key（不加 Bearer 前缀）
    "Authorization": f"{api_key}",
}

# 步骤3: 配置请求参数

payload = {
    # 【model】(string, 必选) 模型名称
    "model": "wan2.7-image",

    # 【input】(object, 必选) 输入的基本信息
    "input": {
        # 【messages】(array, 必选) 请求内容数组
        # 仅支持单轮对话，传入一组 role/content，不支持多轮对话
        "messages": [
            {
                # 【role】(string, 必选) 消息角色，固定设置为 "user"
                "role": "user",
                # 【content】(array, 必选) 消息内容数组
                "content": [
                    # 【text】(string) 文本提示词，描述要生成的组图内容
                    # 建议在提示词中明确说明每张图的场景及角色一致性要求
                    {"text": "电影感组图，记录同一只流浪橘猫，特征必须前后一致。第一张：春天，橘猫穿梭在盛开的樱花树下；第二张：夏天，橘猫在老街的树荫下乘凉避暑；第三张：秋天，橘猫踩在满地的金色落叶上；第四张：冬天，橘猫在雪地上走留下足迹。"},
                ],
            }
        ]
    },

    # 【parameters】(object, 可选) 模型参数配置
    "parameters": {
        # 【enable_sequential】(boolean, 可选) 控制生图模式
        # false: 默认值，普通多图生成模式
        # true: 启用组图输出模式（角色/场景保持连贯性）
        "enable_sequential": True,

        # 【n】(int, 可选) 图像数量
        # 重要: n 直接影响费用，费用 = 单价 × 成功生成的图片张数
        # 关闭组图模式时: 取值范围 1-4，默认为 4，代表生成图像数量
        # 开启组图模式时: 取值范围 1-12，默认为 12，代表最大生成图像数量（实际数量由模型决定且不超过 n）
        "n": 4,

        # 【size】(string, 可选) 输出图片分辨率，两种方式不可混用
        # 方式一（推荐）- 指定规格关键字:
        #   wan2.7-image:     "1K"(1024*1024) / "2K"(2048*2048, 默认)，不支持4K
        # 方式二 - 指定宽高像素值（如 "1024*1024"）:
        #   组图及其他场景: 总像素 [768*768, 2048*2048]，宽高比范围 [1:8, 8:1]
        # 有图片输入时，输出宽高比与输入图像一致并缩放到选定分辨率
        "size": "2K",

        # 【watermark】(bool, 可选) 是否添加水印标识
        # 水印位于图片右下角，文案固定为"AI生成"
        # false: 默认值，不添加水印
        # true: 添加水印
        "watermark": True,

        # 【seed】(integer, 可选) 随机数种子，取值范围 [0, 2147483647]
        # 使用相同的 seed 值可使生成内容保持相对稳定
        # 若不提供，算法将自动使用随机数种子
        # 注意: 模型生成过程具有概率性，相同 seed 不能保证结果完全一致
        "seed": 22,
    },
}

# 步骤4: 发送请求并输出结果

response = requests.post(url, headers=headers, json=payload)

# 格式化输出 JSON 响应
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
          "text": "https://dashscope-7c2c.oss-accelerate.aliyuncs.com/1d/b7/20260408/ea4c8ef9/f0366367-f320-4c1d-b6f6-d2f27b4c5b58_0.png?Expires=1775664011&OSSAccessKeyId=LTAI5tPxpiCM2hjmWrFXrym1&Signature=F6RRCjiKXSUCdaIskzldJnCNFs4%3D"
        },
        {
          "type": "image",
          "text": "https://dashscope-7c2c.oss-accelerate.aliyuncs.com/1d/e1/20260408/ea4c8ef9/f0366367-f320-4c1d-b6f6-d2f27b4c5b58_1.png?Expires=1775664011&OSSAccessKeyId=LTAI5tPxpiCM2hjmWrFXrym1&Signature=xV2VEYWZEOzfoiKJ8Ttss68oGkI%3D"
        },
        {
          "type": "image",
          "text": "https://dashscope-7c2c.oss-accelerate.aliyuncs.com/1d/2f/20260408/ea4c8ef9/f0366367-f320-4c1d-b6f6-d2f27b4c5b58_2.png?Expires=1775664011&OSSAccessKeyId=LTAI5tPxpiCM2hjmWrFXrym1&Signature=shgv%2Bdlf%2FoNMQwTC01daqUJhExI%3D"
        },
        {
          "type": "image",
          "text": "https://dashscope-7c2c.oss-accelerate.aliyuncs.com/1d/5e/20260408/ea4c8ef9/f0366367-f320-4c1d-b6f6-d2f27b4c5b58_3.png?Expires=1775664011&OSSAccessKeyId=LTAI5tPxpiCM2hjmWrFXrym1&Signature=TBTgareRLYTOyzr8YxKyK78r%2BsQ%3D"
        }
      ]
    }
  ],
  "request_id": "39330362-5ad4-99c3-b105-f26db3ed0e3e",
  "usage": {
    "total_tokens": 8000,
    "input_tokens": 0,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 8000,
    "output_tokens_details": {
      "reasoning_tokens": 0
    }
  }
}
```

<p align="center">
  <small>© 2026 DMXAPI wan2.7-image 组图生成</small>
</p>
