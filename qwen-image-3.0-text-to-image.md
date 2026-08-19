# qwen-image-3.0 文生图 API 使用文档

基于千问图像生成与编辑 3.0 标准模型的文生图（T2I）接口，通过 `/v1/responses` 端点同步调用，一次请求即可拿到图像结果。该模型兼顾生成质量与响应速度，擅长复杂文本渲染与图文混合排版；支持单次输出 1~6 张图，输出分辨率总像素在 512×512 至 2048×2048 之间、宽高比 1:8 至 8:1 自由设置（不指定 `size` 时由模型根据提示词自动推荐分辨率），并提供提示词智能改写（DPE / APE）与思考模式两档质量增强开关，适合海报设计、电商配图、创意插画等场景。

> 上游官方文档：<https://help.aliyun.com/zh/model-studio/qwen-image-generation-and-editing-api-reference>

## 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 生成图像 | POST | `https://www.dmxapi.cn/v1/responses` |



:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。如果怀疑密钥已泄露，请立即前往 DMXAPI 官网重新生成。
:::

## 模型名称

- `qwen-image-3.0`

## 文生图 示例代码

```python
import requests
import json

# ===============================================================
# 步骤1: 配置 API 连接信息
# ===============================================================

# DMXAPI 服务端点地址
url = "https://www.dmxapi.cn/v1/responses"

# DMXAPI 密钥 (请替换为您自己的密钥)
# 获取方式: 登录 DMXAPI 官网 -> 个人中心 -> API 密钥管理
api_key = "sk-***********************************************"

# ===============================================================
# 步骤2: 配置请求头
# ===============================================================

headers = {
    "Content-Type": "application/json",      # 指定请求体为 JSON 格式
    "Authorization": f"{api_key}",           # token 认证方式
}

# ===============================================================
# 步骤3: 配置请求参数
# ===============================================================

payload = {
    # 【input】(object, 必填) 输入信息
    "input": {
        # 【messages】(array[object], 必填) 请求内容数组
        # 当前仅支持单轮对话，数组内有且只有一个元素
        "messages": [
            {
                # 【content】(array[object], 必填) 消息内容数组
                # 文生图(T2I)场景: 仅包含一个 {"text": "..."} 对象
                "content": [
                    {
                        # 【text】(string, 必填) 正向提示词
                        # 用于描述您期望生成的图像内容、风格和构图，支持中英文
                        # 推荐不超过 4500 Token
                        # 注意: 仅支持传入一个 text，不传或传入多个将报错
                        "text": "一张全家福"
                    }
                ],

                # 【role】(string, 必填) 消息发送者角色，必须设置为 "user"
                "role": "user"
            }
        ]
    },

    # 【model】(string, 必填) 调用的模型名称
    "model": "qwen-image-3.0",

    # 【parameters】(object, 可选) 控制图像生成的附加参数
    "parameters": {
        # 【enable_thinking】(bool, 可选) 是否开启思考模式，默认值 True
        # 开启时模型将增强推理能力以提升出图质量，但会增加生成耗时
        # 仅在 prompt_extend=True 时生效
        # 适用于 Direct T2I、Direct I2I 和 Agent T2I，I2I Agent 暂不支持
        "enable_thinking": True,

        # 【n】(integer, 可选) 输出图像的数量，支持输出 1~6 张图片，默认值 1
        "n": 1,

        # 【prompt_extend】(bool, 可选) 是否开启提示词智能改写，默认值 True (建议开启)
        # 开启后模型会按照 prompt_extend_mode 指定的方式优化正向提示词
        # 对描述较简单的提示词效果提升明显
        "prompt_extend": True,

        # 【prompt_extend_mode】(string, 可选) 提示词改写方式，默认值 "direct"
        # 可选值:
        #   - "direct" 直接提示词增强(DPE)，适用于大多数场景，T2I 和 I2I 均支持
        #   - "agent"  智能体提示词增强(APE)，提供更精细的改写效果
        #              仅支持文生图(T2I)，图生图(I2I)场景传入 agent 将返回 400 错误
        "prompt_extend_mode": "direct",

        # 【watermark】(bool, 可选) 是否添加水印，默认值 False
        "watermark": False,

        # ---------------------------------------------------------------
        # 以下为可选参数，按需取消注释后使用
        # ---------------------------------------------------------------

        # 【size】(string, 可选) 设置输出图像的分辨率，格式为 宽*高，例如 "1024*1024"
        # 未指定时由模型根据提示词自动推荐分辨率
        # 文生图(T2I): 像素面积范围 512*512 至 2048*2048，宽高比限制 1:8 至 8:1
        # "size": "1024*1024",

        # 【negative_prompt】(string, 可选) 反向提示词
        # 用来描述不希望在画面中看到的内容，可以对画面进行限制
        # "negative_prompt": "低分辨率，低画质，肢体畸形，手指畸形",

        # 【seed】(integer, 可选) 随机数种子，取值范围 [0, 2147483647]
        # 未传入时服务会随机选择种子，固定种子可使生成结果相对稳定
        # "seed": 42,
    }
}


# ===============================================================
# 步骤4: 发送请求并输出结果
# ===============================================================

# 发送 POST 请求到 API 服务器
response = requests.post(url, headers=headers, json=payload)

# 格式化输出 JSON 响应
# - indent=2: 缩进 2 空格，便于阅读
# - ensure_ascii=False: 正确显示中文字符
print(json.dumps(response.json(), indent=2, ensure_ascii=False))
```

## 返回示例

```json
{
  "output": {
    "choices": [
      {
        "finish_reason": "stop",
        "message": {
          "content": [
            {
              "image": "https://dashscope-a717.oss-accelerate.aliyuncs.com/1d/8c/20260817/daadc68a/3c5761be-2e87-94cd-bb3f-ed8251ad7f51_qwen_image3_serving_output_0.png?Expires=1787053188&OSSAccessKeyId=LTAI5tPxpiCM2hjmWrFXrym1&Signature=ndcGk7CHo0rlRg%2BVhrGiXTldzYA%3D",
              "type": "image"
            }
          ],
          "role": "assistant"
        }
      }
    ],
    "rewrite_status": "success"
  },
  "usage": {
    "input_image_count": 0,
    "input_image_type": "qima_input_2k",
    "output_height": 2048,
    "output_image_count": 1,
    "output_image_type": "qima_output_2k",
    "output_width": 2048
  },
  "request_id": "3c5761be-2e87-94cd-bb3f-ed8251ad7f51"
}
```

主要返回字段说明：

- `output.choices[].message.content[].image`：生成图像的 URL，图像格式为 PNG。**链接有效期为 24 小时**，请及时下载并保存图像。
- `output.rewrite_status`：提示词改写状态，具体取值由请求是否开启改写以及改写执行结果决定。
- `output.choices[].finish_reason`：任务停止原因，自然停止时为 `stop`。
- `usage.output_width` / `usage.output_height`：最终输出图片的宽度和高度（像素）。
- `usage.input_image_count`：请求中输入图片的数量，文生图（T2I）时为 `0`。
- `usage.output_image_count`：实际返回的输出图片数量。
- `usage.input_image_type` / `usage.output_image_type`：计量档位，按输出分辨率像素面积判断，面积 ≤ 2,250,000 为 `qima_input_1k` / `qima_output_1k`，面积 > 2,250,000 为 `qima_input_2k` / `qima_output_2k`。
- `request_id`：请求唯一标识，可用于请求明细溯源和问题排查。

<p align="center">
  <small>© 2026 DMXAPI qwen-image-3.0 文生图</small>
</p>
