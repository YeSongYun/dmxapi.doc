# 豆包 doubao-seedream-5.0-lite 文生图 API 使用文档

基于字节跳动豆包最新 Seedream 5.0 Lite 图像创作模型的文生图接口，支持普通请求与流式输出两种调用方式。具备跨模态理解与推理能力，首次引入联网实时检索功能，通过 Search Agent 整合全网信息辅助生图。支持组图模式批量生成最多 15 张内容关联的图片，内置提示词优化功能（标准模式），可输出 PNG、JPEG 格式，支持 2K/4K 分辨率及多种常用宽高比（1:1、4:3、16:9、21:9 等），并可控制水印添加。


## 🚀 请求地址

```
https://www.dmxapi.cn/v1/responses
```

:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。如果怀疑密钥已泄露，请立即前往 DMXAPI 官网重新生成。
:::

## 🐬 模型名称

- `doubao-seedream-5.0-lite`

## 🌸 文生图（非流式）示例代码

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
    "Authorization": f"{api_key}",    # token 认证方式
}

# ═══════════════════════════════════════════════════════════════
# 步骤3: 配置请求参数
# ═══════════════════════════════════════════════════════════════

payload = {
    # 【model】(string, 必填) 模型名称
    # 指定使用的图像生成模型的 Model ID 或推理接入点（Endpoint ID）
    # 稳定版模型标识为 doubao-seedream-5.0-lite
    "model": "doubao-seedream-5.0-lite",

    # 【input】(string, 必填) 图像生成提示词
    # 用于描述想要生成的图像内容，支持中英文输入
    # 建议不超过 300 个汉字或 600 个英文单词，字数过多信息容易分散，模型可能忽略细节
    # 对应官方 API 的 prompt 参数
    "input": "生成5张科技感满满宇宙飞船",

    # 【size】(string, 可选) 生成图片的尺寸，支持两种指定方式（不可混用）：
    #   方式 1 - 指定分辨率等级，由模型根据 prompt 内容自动判断宽高比:
    #     可选值: "2K" / "4K"
    #   方式 2 - 指定具体宽高像素值，如 "2048x2048"、"2304x1728" 等:
    #     默认值: 2048x2048
    #     总像素取值范围: [2560×1440=3686400, 4096×4096=16777216]
    #     宽高比取值范围: [1/16, 16]
    # 推荐宽高像素值:
    #   2K: 1:1→2048x2048 | 4:3→2304x1728 | 3:4→1728x2304 | 16:9→2848x1600 | 9:16→1600x2848 | 3:2→2496x1664 | 2:3→1664x2496 | 21:9→3136x1344
    #   4K: 1:1→4096x4096 | 4:3→4704x3520 | 3:4→3520x4704 | 16:9→5504x3040 | 9:16→3040x5504 | 3:2→4992x3328 | 2:3→3328x4992 | 21:9→6240x2656
    "size": "2K",

    # 【sequential_image_generation】(string, 可选) 组图生成模式，默认值为 "disabled"
    # 组图：基于输入内容，生成一组内容关联的图片
    # 可选值:
    #   "auto"(自动判断模式，模型根据提示词自主判断是否返回组图及图片数量)
    #   "disabled"(关闭组图功能，仅生成单张图片)
    "sequential_image_generation": "auto",

    # 【sequential_image_generation_options】(object, 可选) 组图功能的配置
    # 仅当 sequential_image_generation 为 "auto" 时生效
    "sequential_image_generation_options": {
        # 【max_images】(integer, 可选) 最多可生成的图片数量，默认值为 15
        # 取值范围: [1, 15]
        # 注意: 输入的参考图数量 + 最终生成的图片数量 ≤ 15 张
        "max_images": 15
    },

    # 【tools】(array of object, 可选) 配置模型要调用的工具
    # 仅 doubao-seedream-5.0-lite 支持该参数
    # 开启联网搜索后，模型会根据提示词自主判断是否搜索互联网内容（如商品、天气等），
    # 提升生成图片的时效性，但会增加一定的时延
    # 实际搜索次数可通过响应字段 usage.tool_usage.web_search 查询
    "tools": [{
        # 【type】(string) 指定使用的工具类型
        # 可选值: "web_search"(联网搜索功能)
        "type": "web_search"
    }],

    # 【stream】(boolean, 可选) 是否启用流式输出模式，默认值为 false
    # false: 非流式输出，等待所有图片全部生成结束后一次性返回
    # true: 流式输出，即时返回每张图片的结果，生成单图和组图场景均生效
    "stream": False,

    # 【output_format】(string, 可选) 输出图片的文件格式，默认值为 "jpeg"
    # 仅 doubao-seedream-5.0-lite 支持该参数
    # 可选值: "png" / "jpeg"
    "output_format": "png",

    # 【response_format】(string, 可选) 响应中图片的返回形式，默认值为 "url"
    # 可选值:
    #   "url"(返回图片下载链接，链接在生成后 24 小时内有效，请及时下载)
    #   "b64_json"(以 Base64 编码字符串的 JSON 格式返回图像数据)
    "response_format": "url",

    # 【watermark】(boolean, 可选) 是否在生成的图片中添加水印，默认值为 true
    # false: 不添加水印
    # true: 在图片右下角添加 "AI生成" 字样的水印标识
    "watermark": False,

    # 【optimize_prompt_options】(object, 可选) 提示词优化功能的配置
    # 启用后模型会自动优化输入的提示词，提升生成图片的质量
    "optimize_prompt_options": {
        # 【mode】(string, 可选) 优化模式，默认值为 "standard"
        # 可选值:
        #   "standard"(标准模式，生成内容质量更高，耗时较长)
        #   "fast"(快速模式，耗时更短，质量一般；doubao-seedream-5.0-lite 当前不支持)
        #   "disabled"(关闭提示词优化)
        "mode": "standard"
    }
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

## 🎀 返回示例

```json
{
  "background": false,
  "completed_at": 1772286264,
  "created_at": 1772286264,
  "error": null,
  "id": "resp_85ed57ffea104de7af72f6615412311f",
  "incomplete_details": null,
  "instructions": null,
  "max_output_tokens": 128000,
  "max_tool_calls": null,
  "metadata": {},
  "model": "doubao-seedream-5.0-lite",
  "object": "response",
  "output": [
    {
      "content": [
        {
          "annotations": [],
          "logprobs": [],
          "text": "![Image 1](https://...图片URL...)\n![Image 2](https://...图片URL...)\n![Image 3](https://...图片URL...)\n![Image 4](https://...图片URL...)\n![Image 5](https://...图片URL...)",
          "type": "output_text"
        }
      ],
      "id": "msg_b45dd253bed64755afba724004c8f17a",
      "role": "assistant",
      "status": "completed",
      "type": "message"
    }
  ],
  "parallel_tool_calls": true,
  "previous_response_id": null,
  "reasoning": {
    "effort": "none",
    "summary": null
  },
  "service_tier": "default",
  "status": "completed",
  "store": true,
  "temperature": 1,
  "text": {
    "format": {
      "type": "text"
    },
    "verbosity": "medium"
  },
  "tool_choice": "auto",
  "tools": [],
  "top_p": 1,
  "truncation": "disabled",
  "usage": {
    "input_tokens": 0,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 11000,
    "output_tokens_details": {
      "reasoning_tokens": 0
    },
    "total_tokens": 11000
  },
  "user": null
}
```

## 🌊 文生图（流式）示例代码

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
    "Authorization": f"{api_key}",    # token 认证方式
}

# ═══════════════════════════════════════════════════════════════
# 步骤3: 配置请求参数
# ═══════════════════════════════════════════════════════════════

payload = {
    # 【model】(string, 必填) 模型名称
    # 指定使用的图像生成模型的 Model ID 或推理接入点（Endpoint ID）
    # 稳定版模型标识为 doubao-seedream-5.0-lite
    "model": "doubao-seedream-5.0-lite",

    # 【input】(string, 必填) 图像生成提示词
    # 用于描述想要生成的图像内容，支持中英文输入
    # 建议不超过 300 个汉字或 600 个英文单词，字数过多信息容易分散，模型可能忽略细节
    # 对应官方 API 的 prompt 参数
    "input": "生成5张科技感满满宇宙飞船",

    # 【size】(string, 可选) 生成图片的尺寸，支持两种指定方式（不可混用）：
    #   方式 1 - 指定分辨率等级: "2K" / "4K"
    #   方式 2 - 指定具体宽高像素值，如 "2048x2048"
    #     默认值: 2048x2048
    #     总像素取值范围: [2560×1440=3686400, 4096×4096=16777216]
    #     宽高比取值范围: [1/16, 16]
    "size": "2K",

    # 【sequential_image_generation】(string, 可选) 组图生成模式，默认值为 "disabled"
    # 可选值: "auto"(自动判断是否生成组图) / "disabled"(仅生成单张)
    "sequential_image_generation": "auto",

    # 【sequential_image_generation_options】(object, 可选) 组图功能配置
    # 仅当 sequential_image_generation 为 "auto" 时生效
    "sequential_image_generation_options": {
        # 【max_images】(integer, 可选) 最多可生成的图片数量，默认值为 15
        # 取值范围: [1, 15]，输入参考图数量 + 生成图片数量 ≤ 15
        "max_images": 15
    },

    # 【tools】(array of object, 可选) 配置模型要调用的工具
    # 仅 doubao-seedream-5.0-lite 支持，开启后模型可联网检索实时信息辅助生图
    "tools": [{
        # 【type】(string) 工具类型
        # 可选值: "web_search"(联网搜索)
        "type": "web_search"
    }],

    # 【stream】(boolean, 可选) 是否启用流式输出模式，默认值为 false
    # true: 流式输出，每张图片生成后即时以 SSE 事件流返回，无需等待全部完成
    "stream": True,

    # 【output_format】(string, 可选) 输出图片的文件格式，默认值为 "jpeg"
    # 仅 doubao-seedream-5.0-lite 支持
    # 可选值: "png" / "jpeg"
    "output_format": "png",

    # 【response_format】(string, 可选) 图片返回形式，默认值为 "url"
    # 可选值: "url"(图片链接，24 小时有效) / "b64_json"(Base64 编码数据)
    "response_format": "url",

    # 【watermark】(boolean, 可选) 是否添加水印，默认值为 true
    # true: 右下角添加 "AI生成" 水印 / false: 不添加
    "watermark": False,

    # 【optimize_prompt_options】(object, 可选) 提示词优化配置
    "optimize_prompt_options": {
        # 【mode】(string, 可选) 优化模式，默认值为 "standard"
        # 可选值: "standard"(质量更高，耗时较长) / "disabled"(关闭优化)
        # 注意: doubao-seedream-5.0-lite 当前不支持 "fast" 模式
        "mode": "standard"
    }
}

# ═══════════════════════════════════════════════════════════════
# 步骤4: 发送请求并输出结果
# ═══════════════════════════════════════════════════════════════

# 发送 POST 请求到 API 服务器（启用流式传输）
response = requests.post(url, headers=headers, json=payload, stream=True)

print(response.status_code)

# 流式读取响应，只保留关键信息
current_event = None
for line in response.iter_lines():
    if line:
        line = line.decode('utf-8')

        # 记录事件类型
        if line.startswith('event: '):
            current_event = line[7:]
            continue

        # 处理数据行
        if line.startswith('data: '):
            data_str = line[6:]
        else:
            data_str = line

        # 只输出图片生成事件和完成事件
        if current_event == 'response.output_text.delta':
            print(f"event: {current_event}")
            print(data_str)
        elif current_event == 'response.completed':
            try:
                data = json.loads(data_str)
                usage = data.get('response', {}).get('usage', {})
                print(f"event: {current_event}")
                print(json.dumps({
                    "status": "completed",
                    "usage": usage
                }, ensure_ascii=False))
            except:
                print(data_str)
        elif data_str == '[DONE]':
            print('[DONE]')
```

## 🎠 返回示例

```json
200
event: response.output_text.delta
{"content_index":0,"delta":"![Image 1](https://...图片URL...)","item_id":"msg_02562ef307dd4f8c878139cb3f76fba0","logprobs":[],"output_index":0,"sequence_number":4,"type":"response.output_text.delta"}
event: response.output_text.delta
{"content_index":0,"delta":"![Image 2](https://...图片URL...)","item_id":"msg_02562ef307dd4f8c878139cb3f76fba0","logprobs":[],"output_index":0,"sequence_number":5,"type":"response.output_text.delta"}
event: response.output_text.delta
{"content_index":0,"delta":"![Image 3](https://...图片URL...)","item_id":"msg_02562ef307dd4f8c878139cb3f76fba0","logprobs":[],"output_index":0,"sequence_number":6,"type":"response.output_text.delta"}
event: response.output_text.delta
{"content_index":0,"delta":"![Image 4](https://...图片URL...)","item_id":"msg_02562ef307dd4f8c878139cb3f76fba0","logprobs":[],"output_index":0,"sequence_number":7,"type":"response.output_text.delta"}
event: response.output_text.delta
{"content_index":0,"delta":"![Image 5](https://...图片URL...)","item_id":"msg_02562ef307dd4f8c878139cb3f76fba0","logprobs":[],"output_index":0,"sequence_number":8,"type":"response.output_text.delta"}
event: response.completed
{"status": "completed", "usage": {"input_tokens": 0, "input_tokens_details": {"cached_tokens": 0}, "output_tokens": 11000, "output_tokens_details": {"reasoning_tokens": 0}, "total_tokens": 11000}}
```

<p align="center">
  <small>© 2026 DMXAPI 豆包 doubao-seedream-5.0-lite 文生图</small>
</p>
