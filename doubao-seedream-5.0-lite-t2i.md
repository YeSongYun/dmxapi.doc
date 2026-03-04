# doubao-seedream-5.0-lite 文生图 API 文档

通过文字描述生成高质量图片，支持最高 3K 分辨率、联网搜索增强和自定义输出格式。

:::tip doubao-seedream-5.0-lite 与其他版本的差异
- **联网搜索（`tools`）**：仅 5.0-lite 支持，可根据提示词自主判断是否搜索互联网内容（如商品、天气等），提升图片时效性
- **输出格式（`output_format`）**：仅 5.0-lite 支持指定输出为 `png` 或 `jpeg`，4.5/4.0 固定输出 jpeg
- **最高分辨率**：5.0-lite 最高支持 3K（3072px），4.5/4.0 最高支持 4K；若需 4K 分辨率请选用 4.5/4.0 版本
:::

## 请求地址

```
https://www.dmxapi.cn/v1/responses
```

## 模型名称

```
doubao-seedream-5.0-lite
```

## 示例代码

::: code-group

```python [非流式]
import requests
import json

# ═══════════════════════════════════════════════════════════════
# 🔑 步骤1: 配置 API 连接信息
# ═══════════════════════════════════════════════════════════════

# 🌐 DMXAPI 服务端点地址
url = "https://www.dmxapi.cn/v1/responses"

# 🔐 DMXAPI 密钥 (请替换为您自己的密钥)
# 获取方式: 登录 DMXAPI 官网 -> 个人中心 -> API 密钥管理
api_key = "sk-****************************************"

# ═══════════════════════════════════════════════════════════════
# 📋 步骤2: 配置请求头
# ═══════════════════════════════════════════════════════════════

headers = {
    "Content-Type": "application/json",      # 指定请求体为 JSON 格式
    "Authorization": f"{api_key}",           # token 认证方式
}

# ═══════════════════════════════════════════════════════════════
# 💬 步骤3: 配置请求参数
# ═══════════════════════════════════════════════════════════════

payload = {
    "model": "doubao-seedream-5.0-lite",
    # 【input】用于生成图像的提示词，支持中英文
    # 建议不超过 300 汉字或 600 英文单词，字数过多信息容易分散，模型可能因此忽略细节
    "input": "生成5张科技感满满宇宙飞船",
    # 【size】指定生成图像的尺寸信息，支持以下两种方式，不可混用：
    #   方式 1 | 指定分辨率关键词，在 prompt 中用自然语言描述宽高比/形状/用途，模型判断具体大小
    #     可选值：`2K`、`3K`
    #   方式 2 | 指定宽高像素值，默认 2048x2048，需同时满足：
    #     总像素取值范围：[2560x1440=3686400, 3072x3072x1.1025=10404496]
    #     宽高比取值范围：[1/16, 16]
    #     说明：总像素是对单张图宽度和高度的像素乘积限制，而不是对宽度或高度的单独值进行限制
    #       有效示例 `3750x1250`：总像素 3750x1250=4687500 符合 [3686400, 10404496]，
    #                             宽高比 3750/1250=3 符合 [1/16, 16]，故有效
    #       无效示例 `1500x1500`：总像素 1500x1500=2250000 未达到 3686400 最低要求，
    #                             虽宽高比 1 符合范围，但未同时满足两项限制，故无效
    #   推荐宽高像素值：
    #     2K | 1:1=2048x2048  4:3=2304x1728  3:4=1728x2304  16:9=2848x1600
    #         | 9:16=1600x2848  3:2=2496x1664  2:3=1664x2496  21:9=3136x1344
    #     3K | 1:1=3072x3072  4:3=3456x2592  3:4=2592x3456  16:9=4096x2304
    #         | 9:16=2304x4096  3:2=3744x2496  2:3=2496x3744  21:9=4704x2016
    "size": "2K",
    # 【sequential_image_generation】控制是否开启组图功能，默认 disabled
    #   auto：自动判断模式，模型根据提示词自主判断是否返回组图及图片数量
    #   disabled：关闭组图功能，模型只会生成一张图
    "sequential_image_generation": "auto",
    "sequential_image_generation_options": {
        # 【max_images】指定本次请求最多可生成的图片数量，取值范围 [1, 15]，默认 15
        # 注意：输入的参考图数量 + 最终生成的图片数量 ≤ 15
        "max_images": 15
    },
    # 【tools】配置模型调用的工具，仅 doubao-seedream-5.0-lite 支持
    "tools": [{
        # 【type】指定工具类型
        # web_search：联网搜索，开启后模型根据提示词自主判断是否搜索互联网内容
        # 可提升生成图片的时效性，但会增加一定时延
        # 实际搜索次数可通过字段 usage.tool_usage.web_search 查询，如果为 0 表示未搜索
        "type": "web_search"
    }],
    # 【stream】控制是否开启流式输出模式，默认 false，仅 doubao-seedream-5.0-lite/4.5/4.0 支持
    #   false：非流式输出模式，等待所有图片全部生成结束后再一次性返回所有信息
    #   true：流式输出模式，即时返回每张图片输出的结果，在生成单图和组图的场景下均生效
    "stream": False,
    # 【output_format】指定生成图像的文件格式，默认 jpeg，仅 doubao-seedream-5.0-lite 支持自定义设置
    #   可选值：png、jpeg
    "output_format": "png",
    # 【response_format】指定生成图像的返回格式，默认 url
    #   url：返回图片下载链接，链接在图片生成后 24 小时内有效，请及时下载
    #   b64_json：以 Base64 编码字符串的 JSON 格式返回图像数据
    "response_format": "url",
    # 【watermark】是否在生成图片中添加水印，默认 true
    #   false：不添加水印
    #   true：在图片右下角添加"AI生成"字样的水印标识
    "watermark": False,
    "optimize_prompt_options": {
        # 【mode】提示词优化模式，默认 standard
        #   standard：标准模式，生成内容质量更高，耗时较长
        #   fast：快速模式，耗时更短，质量一般；doubao-seedream-5.0-lite 不支持
        "mode": "standard"
    }
}

# ═══════════════════════════════════════════════════════════════
# 📤 步骤4: 发送请求并输出结果
# ═══════════════════════════════════════════════════════════════

# 发送 POST 请求到 API 服务器
response = requests.post(url, headers=headers, json=payload)

# 格式化输出 JSON 响应
# - indent=2: 缩进 2 空格，便于阅读
# - ensure_ascii=False: 正确显示中文字符
print(json.dumps(response.json(), indent=2, ensure_ascii=False))
```

```python [流式]
import requests
import json

# ═══════════════════════════════════════════════════════════════
# 🔑 步骤1: 配置 API 连接信息
# ═══════════════════════════════════════════════════════════════

# 🌐 DMXAPI 服务端点地址
url = "https://www.dmxapi.cn/v1/responses"

# 🔐 DMXAPI 密钥 (请替换为您自己的密钥)
# 获取方式: 登录 DMXAPI 官网 -> 个人中心 -> API 密钥管理
api_key = "sk-****************************************"

# ═══════════════════════════════════════════════════════════════
# 📋 步骤2: 配置请求头
# ═══════════════════════════════════════════════════════════════

headers = {
    "Content-Type": "application/json",      # 指定请求体为 JSON 格式
    "Authorization": f"{api_key}",           # token 认证方式
}

# ═══════════════════════════════════════════════════════════════
# 💬 步骤3: 配置请求参数
# ═══════════════════════════════════════════════════════════════

payload = {
    "model": "doubao-seedream-5.0-lite",
    # 【input】用于生成图像的提示词，支持中英文
    # 建议不超过 300 汉字或 600 英文单词，字数过多信息容易分散，模型可能因此忽略细节
    "input": "生成5张科技感满满宇宙飞船",
    # 【size】指定生成图像的尺寸信息，支持以下两种方式，不可混用：
    #   方式 1 | 指定分辨率关键词，在 prompt 中用自然语言描述宽高比/形状/用途，模型判断具体大小
    #     可选值：`2K`、`3K`
    #   方式 2 | 指定宽高像素值，默认 2048x2048，需同时满足：
    #     总像素取值范围：[2560x1440=3686400, 3072x3072x1.1025=10404496]
    #     宽高比取值范围：[1/16, 16]
    #     说明：总像素是对单张图宽度和高度的像素乘积限制，而不是对宽度或高度的单独值进行限制
    #       有效示例 `3750x1250`：总像素 3750x1250=4687500 符合 [3686400, 10404496]，
    #                             宽高比 3750/1250=3 符合 [1/16, 16]，故有效
    #       无效示例 `1500x1500`：总像素 1500x1500=2250000 未达到 3686400 最低要求，
    #                             虽宽高比 1 符合范围，但未同时满足两项限制，故无效
    #   推荐宽高像素值：
    #     2K | 1:1=2048x2048  4:3=2304x1728  3:4=1728x2304  16:9=2848x1600
    #         | 9:16=1600x2848  3:2=2496x1664  2:3=1664x2496  21:9=3136x1344
    #     3K | 1:1=3072x3072  4:3=3456x2592  3:4=2592x3456  16:9=4096x2304
    #         | 9:16=2304x4096  3:2=3744x2496  2:3=2496x3744  21:9=4704x2016
    "size": "2K",
    # 【sequential_image_generation】控制是否开启组图功能，默认 disabled
    #   auto：自动判断模式，模型根据提示词自主判断是否返回组图及图片数量
    #   disabled：关闭组图功能，模型只会生成一张图
    "sequential_image_generation": "auto",
    "sequential_image_generation_options": {
        # 【max_images】指定本次请求最多可生成的图片数量，取值范围 [1, 15]，默认 15
        # 注意：输入的参考图数量 + 最终生成的图片数量 ≤ 15
        "max_images": 15
    },
    # 【tools】配置模型调用的工具，仅 doubao-seedream-5.0-lite 支持
    "tools": [{
        # 【type】指定工具类型
        # web_search：联网搜索，开启后模型根据提示词自主判断是否搜索互联网内容
        # 可提升生成图片的时效性，但会增加一定时延
        # 实际搜索次数可通过字段 usage.tool_usage.web_search 查询，如果为 0 表示未搜索
        "type": "web_search"
    }],
    # 【stream】控制是否开启流式输出模式，默认 false，仅 doubao-seedream-5.0-lite/4.5/4.0 支持
    #   false：非流式输出模式，等待所有图片全部生成结束后再一次性返回所有信息
    #   true：流式输出模式，即时返回每张图片输出的结果，在生成单图和组图的场景下均生效
    "stream": True,
    # 【output_format】指定生成图像的文件格式，默认 jpeg，仅 doubao-seedream-5.0-lite 支持自定义设置
    #   可选值：png、jpeg
    "output_format": "png",
    # 【response_format】指定生成图像的返回格式，默认 url
    #   url：返回图片下载链接，链接在图片生成后 24 小时内有效，请及时下载
    #   b64_json：以 Base64 编码字符串的 JSON 格式返回图像数据
    "response_format": "url",
    # 【watermark】是否在生成图片中添加水印，默认 true
    #   false：不添加水印
    #   true：在图片右下角添加"AI生成"字样的水印标识
    "watermark": False,
    "optimize_prompt_options": {
        # 【mode】提示词优化模式，默认 standard
        #   standard：标准模式，生成内容质量更高，耗时较长
        #   fast：快速模式，耗时更短，质量一般；doubao-seedream-5.0-lite 不支持
        "mode": "standard"
    }
}

# ═══════════════════════════════════════════════════════════════
# 📤 步骤4: 发送请求并输出结果
# ═══════════════════════════════════════════════════════════════

# 发送 POST 请求到 API 服务器（stream=True 开启流式传输）
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

:::

## 返回示例

::: code-group

```json [非流式]
{
  "background": false,
  "completed_at": 1772426414,
  "created_at": 1772426414,
  "error": null,
  "id": "resp_8d4f166d227246228dda783119c86455",
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
          "text": "![Image 1](https://ark-acg-cn-beijing.tos-cn-beijing.volces.com/...)\n![Image 2](https://ark-acg-cn-beijing.tos-cn-beijing.volces.com/...)\n![Image 3](https://ark-acg-cn-beijing.tos-cn-beijing.volces.com/...)\n![Image 4](https://ark-acg-cn-beijing.tos-cn-beijing.volces.com/...)\n![Image 5](https://ark-acg-cn-beijing.tos-cn-beijing.volces.com/...)",
          "type": "output_text"
        }
      ],
      "id": "msg_ec3f52d7ae79466c99702ca49577aea2",
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

```text [流式]
200
event: response.output_text.delta
{"content_index":0,"delta":"![Image 1](https://ark-acg-cn-beijing.tos-cn-beijing.volces.com/doubao-seedream-5-0/02177246206533281a9193ce9f89e3456d252c7b9d01d03b8ca0e_0.png?X-Tos-Algorithm=TOS4-HMAC-SHA256&X-Tos-Expires=86400&X-Tos-Signature=dbf25a09...&X-Tos-SignedHeaders=host)","item_id":"msg_0ad09f964a3e4a2786d27d589160049b","logprobs":[],"output_index":0,"sequence_number":4,"type":"response.output_text.delta"}
event: response.output_text.delta
{"content_index":0,"delta":"![Image 2](https://ark-acg-cn-beijing.tos-cn-beijing.volces.com/doubao-seedream-5-0/02177246206533281a9193ce9f89e3456d252c7b9d01d03b8ca0e_2.png?X-Tos-Algorithm=TOS4-HMAC-SHA256&X-Tos-Expires=86400&X-Tos-Signature=152b2c3e...&X-Tos-SignedHeaders=host)","item_id":"msg_0ad09f964a3e4a2786d27d589160049b","logprobs":[],"output_index":0,"sequence_number":5,"type":"response.output_text.delta"}
event: response.output_text.delta
{"content_index":0,"delta":"![Image 3](https://ark-acg-cn-beijing.tos-cn-beijing.volces.com/doubao-seedream-5-0/02177246206533281a9193ce9f89e3456d252c7b9d01d03b8ca0e_4.png?X-Tos-Algorithm=TOS4-HMAC-SHA256&X-Tos-Expires=86400&X-Tos-Signature=a2d0bb5b...&X-Tos-SignedHeaders=host)","item_id":"msg_0ad09f964a3e4a2786d27d589160049b","logprobs":[],"output_index":0,"sequence_number":6,"type":"response.output_text.delta"}
event: response.output_text.delta
{"content_index":0,"delta":"![Image 4](https://ark-acg-cn-beijing.tos-cn-beijing.volces.com/doubao-seedream-5-0/02177246206533281a9193ce9f89e3456d252c7b9d01d03b8ca0e_3.png?X-Tos-Algorithm=TOS4-HMAC-SHA256&X-Tos-Expires=86400&X-Tos-Signature=6c1c6841...&X-Tos-SignedHeaders=host)","item_id":"msg_0ad09f964a3e4a2786d27d589160049b","logprobs":[],"output_index":0,"sequence_number":7,"type":"response.output_text.delta"}
event: response.output_text.delta
{"content_index":0,"delta":"![Image 5](https://ark-acg-cn-beijing.tos-cn-beijing.volces.com/doubao-seedream-5-0/02177246206533281a9193ce9f89e3456d252c7b9d01d03b8ca0e_1.png?X-Tos-Algorithm=TOS4-HMAC-SHA256&X-Tos-Expires=86400&X-Tos-Signature=38a045eb...&X-Tos-SignedHeaders=host)","item_id":"msg_0ad09f964a3e4a2786d27d589160049b","logprobs":[],"output_index":0,"sequence_number":8,"type":"response.output_text.delta"}
event: response.completed
{"status": "completed", "usage": {"input_tokens": 0, "input_tokens_details": {"cached_tokens": 0}, "output_tokens": 11000, "output_tokens_details": {"reasoning_tokens": 0}, "total_tokens": 11000}}
```

:::
