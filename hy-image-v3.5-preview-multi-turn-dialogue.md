# hy-image-v3.5-preview 多轮对话 API 使用文档

基于腾讯混元 Hy-Image-3.5-preview 模型的多轮对话式生图/编辑接口，通过 `/v1/images/generations` 端点以 Chat/Messages 协议提交单轮或多轮上下文，同步返回图片结果。第一轮提交文本指令与参考图后，响应中的 `assembled_history`（assistant + tool + assistant 三条已拼接好的回灌消息）随上下文保存为 JSON 文件；第二轮读取该文件，用上一轮生成的图片替换原始参考图，按「第一轮 messages + assembled_history + 本轮新 user 指令」拼接请求，实现多轮连续编辑。`session` 字段用于一致性哈希调度，同一会话落到同一推理实例以提升 KV-cache 命中率；输出最高支持 4096×4096（4K），返回的图片地址为有效期 12 小时的临时签名 URL。

## 🌐 请求地址

```text
https://www.dmxapi.cn/v1/images/generations
```

:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。如果怀疑密钥已泄露，请立即前往 DMXAPI 官网重新生成。
:::

## 模型名称

- `hy-image-v3.5-preview`

## 多轮对话（第一轮）示例代码

```python
import base64
import json
import os
from datetime import datetime
from pathlib import Path

import requests

# ===============================================================
# 步骤1: 配置 API 连接信息
# ===============================================================

# DMXAPI 服务端点地址
url = "https://www.dmxapi.cn/v1/images/generations"

# DMXAPI 密钥 (请替换为您自己的密钥)
# 获取方式: 登录 DMXAPI 官网 -> 个人中心 -> API 密钥管理
api_key = "sk-***********************************************"

# ===============================================================
# 步骤2: 配置请求头
# ===============================================================

headers = {
    "Authorization": f"Bearer {api_key}",    # Bearer token 认证方式
    "Content-Type": "application/json",      # 指定请求体为 JSON 格式
}

# ===============================================================
# 步骤3: 配置请求参数
# ===============================================================

# 参考图来源，可以填写本地图片路径，也可以填写公网图片 URL
image_source = "https://cdn.jsdelivr.net/gh/opencv/opencv/samples/data/fruits.jpg"

payload = {
    # 【model】(string, 必填) 调用的模型名称
    # 取值: hy-image-v3.5-preview
    "model": "hy-image-v3.5-preview",

    # 【session】(string, 可选) 会话 ID
    # 用于推理服务一致性哈希调度：同 session 的多轮请求会落到同一推理实例，
    # 提升 KV-cache 命中率；多轮对话建议整条会话保持同一 session 值
    "session": "demo-session-001",

    # 【messages】(array[object], 必填) 多轮会话内容，时间从旧到新排列
    # 服务端会取数组中最后一个 role=user 的消息作为本轮生图指令，
    # 其余对象作为历史上下文一并透传（用于多轮编辑）
    "messages": [
        {
            # 【role】(string, 必填) 角色
            # 支持 user / assistant / tool；tool 角色仅在
            # 「把上一轮生图结果回灌作为下一轮上下文」时出现
            "role": "user",

            # 【content】(array[object], 可选) 该轮的具体内容
            "content": [
                {
                    # 【type】(string, 必填) 内容类型，text 或 image_url
                    "type": "text",

                    # 【text】(string, 可选) 当 type=text 时使用，表示具体文本
                    "text": "给图中的主体带上圣诞小帽，并将整体色调调整为圣诞色"
                },
                {
                    "type": "image_url",

                    # 【image_url】(object, 可选) 当 type=image_url 时使用
                    # 结构为 {"url": "..."}，支持 http(s) 公网 URL 或
                    # data:image/...;base64,... 形态
                    # 单图大小 ≤ 20MB，图片总数量 ≤ 20 张
                    # （超过时服务端按轮次由远到近自动截断）
                    "image_url": {
                        "url": image_source
                    }
                }
            ]
        }
    ],

    # 【size】(string, 可选) 生成尺寸，格式 ${宽}x${高}
    # 宽、高均为正整数，取值范围 [256, 8192]
    # 宽 × 高（面积）不超过 16777216，即最高支持 4096x4096（4K）
    # 不传或传空串时，由模型基于 prompt 语义与 generate_max_pixels 自主决定尺寸
    "size": "1024x1024",

    # 【seed】(integer, 可选) 生成种子
    # int64 类型，取值范围 [0, 2^63-1]；为 0 或不传时服务端随机分配，负值将被拒绝
    "seed": 0,

    # 【generate_max_pixels】(integer, 可选) 生成图片的目标面积（像素数）
    # 仅在未传 size 时生效，支持 3 个枚举档位:
    #   - 1048576: 1K（1024x1024）
    #   - 2359296: 1.5K（默认档位）
    #   - 4194304: 2K
    # 传入非枚举中间值时按最近面积归档；该参数最高档位为 2K
    "generate_max_pixels": 4194304,

    # 【resize_max_pixels】(integer, 可选) 输入参考图面积上限（像素数）
    # 原图面积不超过阈值时原样透传；超过阈值时按比例等比缩放到接近阈值后再送入模型
    # 不传时默认 1048576（1024x1024）
    "resize_max_pixels": 1048576,

    # 【footnote】(string, 可选) 业务自定义水印内容
    # 最长 16 个字符（按 utf8.RuneCount 计算，不区分中英文），生成在图片右下角
    "footnote": "DMXAPI",

    # 【use_search_tool】(object, 可选) 外部搜索增强开关
    # 结构固定为 {"value": true} 或 {"value": false}，当前默认关闭
    "use_search_tool": {
        "value": False
    }
}

# 本地图片路径的 Base64 转换逻辑（公网 URL 无需转换）

IMAGE_MIME_TYPES = {
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
    ".webp": "image/webp",
    ".bmp": "image/bmp",
    ".gif": "image/gif",
}

MAX_IMAGE_SIZE = 20 * 1024 * 1024


def convert_image(source):
    # 公网 URL 直接传递
    if source.startswith(("http://", "https://")):
        return source

    # 本地文件不存在时抛出错误
    if not os.path.isfile(source):
        raise FileNotFoundError(f"图片不存在：{source}")

    # 检查图片格式
    extension = os.path.splitext(source)[1].lower()
    mime_type = IMAGE_MIME_TYPES.get(extension)

    if mime_type is None:
        raise ValueError(f"不支持的图片格式：{extension}")

    # 检查图片大小
    if os.path.getsize(source) > MAX_IMAGE_SIZE:
        raise ValueError("图片大小不能超过 20MB")

    # 读取本地图片并转换为 Base64 Data URL
    with open(source, "rb") as image_file:
        encoded_image = base64.b64encode(
            image_file.read()
        ).decode("ascii")

    return f"data:{mime_type};base64,{encoded_image}"


# 将参考图统一转换为可传输格式
payload["messages"][0]["content"][1]["image_url"]["url"] = (
    convert_image(
        payload["messages"][0]["content"][1]["image_url"]["url"]
    )
)

# ===============================================================
# 步骤4: 发送请求并输出结果
# ===============================================================

# 发送 POST 请求到 API 服务器
response = requests.post(
    url,
    headers=headers,
    json=payload,
    timeout=300
)

print("HTTP 状态码：", response.status_code)

try:
    result = response.json()
    print(json.dumps(result, indent=2, ensure_ascii=False))
except ValueError:
    result = {}
    print(response.text)

response.raise_for_status()

if result.get("error"):
    raise RuntimeError(
        json.dumps(result["error"], ensure_ascii=False)
    )

# 打印第一轮生成的图片地址（临时签名 URL，有效期 12 小时，请及时下载转存）
if result.get("data"):
    print("\n第一轮图片地址：")
    print(result["data"][0].get("url"))

# assembled_history：服务端拼好的「下一轮回灌消息序列」，
# 结构与请求体 messages 元素完全一致，典型为 3 条对象：
#   1. role=assistant（含 reasoning + tool_calls，描述本轮思考与工具调用）
#   2. role=tool（含工具产出图的中间 URL，tool_call_id 与第 1 条一致）
#   3. role=assistant（只含收尾文本，例如「你请求的图片已完成。」）
# 多轮编辑时直接把该数组原样追加到下一轮 messages 即可
assembled_history = result.get("assembled_history")

if not assembled_history:
    raise RuntimeError("响应中没有 assembled_history")

# 将第一轮上下文保存为 JSON 文件，供第二轮代码读取
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

context_path = Path(__file__).with_name(
    f"hunyuan_round1_{timestamp}.json"
)

with context_path.open("w", encoding="utf-8") as file:
    json.dump(
        {
            "model": payload["model"],
            "session": payload["session"],
            "messages": payload["messages"],
            "assembled_history": assembled_history,
            "latest_image_url": (
                result.get("data", [{}])[0].get("url")
            )
        },
        file,
        ensure_ascii=False,
        indent=2
    )

print(f"\n第一轮上下文已保存：{context_path}")
```

## 返回示例

```json
{
  "created": 1789720599,
  "data": [
    {
      "url": "https://aigc-output-image-file-1326893053.cos.ap-guangzhou.myqcloud.com/xxx/round1.png?..."
    }
  ],
  "request_id": "a1c00d07-041b-4daa-bae0-b7eabf2bc33a",
  "usage": {
    "total_tokens": 20000
  },
  "assembled_history": [
    {
      "role": "assistant",
      "content": [
        { "type": "text", "text": "为了按要求创建图片，我将使用生成工具。" }
      ],
      "reasoning": "用户希望给图中主体戴上圣诞小帽，并将整体色调调整为圣诞色...",
      "tool_calls": [
        {
          "id": "generate@call_0",
          "type": "function",
          "function": {
            "name": "generate",
            "arguments": "{\"recaption\":\"...\"}"
          }
        }
      ]
    },
    {
      "role": "tool",
      "tool_call_id": "generate@call_0",
      "content": [
        {
          "type": "image_url",
          "image_url": {
            "url": "http://hunyuan-image-result-tob-1258344703.cos.ap-guangzhou.myqcloud.com/xxx/round1.png?..."
          }
        }
      ]
    },
    {
      "role": "assistant",
      "content": [
        { "type": "text", "text": "你请求的图片已完成。" }
      ]
    }
  ]
}
```

## 多轮对话（第二轮）示例代码

```python
"""
╔═══════════════════════════════════════════════════════════════╗
║          hy-image-v3.5-preview 多轮对话（第二轮）              ║
╚═══════════════════════════════════════════════════════════════╝

📝 功能说明:
   本脚本演示如何读取第一轮保存的上下文 JSON，拼接多轮 messages
   并发起第二轮编辑请求

═══════════════════════════════════════════════════════════════
"""

import copy
import json
from datetime import datetime
from pathlib import Path

import requests

# ═══════════════════════════════════════════════════════════════
# 🔑 步骤1: 配置 API 连接信息
# ═══════════════════════════════════════════════════════════════

# 🌐 DMXAPI 服务端点地址
url = "https://www.dmxapi.cn/v1/images/generations"

# 🔐 DMXAPI 密钥 (请替换为您自己的密钥)
# 获取方式: 登录 DMXAPI 官网 -> 个人中心 -> API 密钥管理
api_key = "sk-***********************************************"

# ═══════════════════════════════════════════════════════════════
# 📋 步骤2: 配置请求头
# ═══════════════════════════════════════════════════════════════

headers = {
    "Authorization": f"Bearer {api_key}",    # Bearer token 认证方式
    "Content-Type": "application/json",      # 指定请求体为 JSON 格式
}

# ═══════════════════════════════════════════════════════════════
# 💬 步骤3: 读取第一轮上下文并拼接多轮请求参数
# ═══════════════════════════════════════════════════════════════

# 查找第一轮代码保存的上下文 JSON 文件（取最新的一份）
context_files = sorted(
    Path(__file__).parent.glob("hunyuan_round1_*.json")
)

if not context_files:
    raise FileNotFoundError(
        "没有找到第一轮上下文，请先运行第一段代码"
    )

context_path = context_files[-1]

with context_path.open("r", encoding="utf-8") as file:
    context = json.load(file)

print(f"正在读取：{context_path}")


def find_image_url(value):
    # 在嵌套结构中递归查找第一张图片的 URL
    if isinstance(value, dict):
        if value.get("type") == "image_url":
            image = value.get("image_url")

            if isinstance(image, dict):
                image = image.get("url")

            if isinstance(image, str):
                return image

        for item in value.values():
            result = find_image_url(item)

            if result:
                return result

    elif isinstance(value, list):
        for item in value:
            result = find_image_url(item)

            if result:
                return result

    return None


def convert_http_to_https(value):
    # 将历史消息中的 HTTP 地址递归转换为 HTTPS
    if isinstance(value, dict):
        for key, item in value.items():
            if (
                key == "url"
                and isinstance(item, str)
                and item.startswith("http://")
            ):
                value[key] = "https://" + item[7:]
            else:
                convert_http_to_https(item)

    elif isinstance(value, list):
        for item in value:
            convert_http_to_https(item)


original_messages = copy.deepcopy(context["messages"])
assembled_history = copy.deepcopy(
    context["assembled_history"]
)

# 优先使用第一轮生成的最终图片
current_image_url = context.get("latest_image_url")

if not current_image_url:
    current_image_url = find_image_url(assembled_history)

if not current_image_url:
    raise RuntimeError("没有找到上一轮生成的图片地址")

if current_image_url.startswith("http://"):
    current_image_url = "https://" + current_image_url[7:]

# 将历史消息中的 HTTP 地址转换为 HTTPS
convert_http_to_https(assembled_history)

# 用上一轮生成的图片替换原来的本地 Base64 图片
for message in original_messages:
    content = message.get("content", [])

    if not isinstance(content, list):
        continue

    for item in content:
        if item.get("type") != "image_url":
            continue

        image_url = item.get("image_url")

        if isinstance(image_url, dict):
            image_url["url"] = current_image_url
        else:
            item["image_url"] = {
                "url": current_image_url
            }

# 按官方格式拼接多轮 messages：
# 第 N+1 轮请求的 messages = 第 N 轮的 messages（含首条 user）
#   + 第 N 轮响应中的 assembled_history（assistant + tool + assistant 三条）
#   + 本轮新的 user 消息
messages = []

messages.extend(original_messages)
messages.extend(assembled_history)

messages.append({
    "role": "user",
    "content": [
        {
            "type": "text",
            "text": "将图里的主体的圣诞小帽换成牛仔帽，并将整体色调调整为西部牛仔风格",
        }
    ]
})

payload = {
    # 【model】(string, 必填) 调用的模型名称，与第一轮保持一致
    "model": context["model"],

    # 【session】(string, 可选) 会话 ID
    # 与第一轮保持同一 session 值，使多轮请求落到同一推理实例，
    # 提升 KV-cache 命中率
    "session": context["session"],

    # 【messages】(array[object], 必填) 多轮会话内容，时间从旧到新排列
    # 服务端会取数组中最后一个 role=user 的消息作为本轮生图指令，
    # 其余对象（含 assembled_history 回灌的历史）作为上下文一并透传
    "messages": messages
}

# ═══════════════════════════════════════════════════════════════
# 📤 步骤4: 发送请求并输出结果
# ═══════════════════════════════════════════════════════════════

# 发送 POST 请求到 API 服务器
response = requests.post(
    url,
    headers=headers,
    json=payload,
    timeout=300
)

print("HTTP 状态码：", response.status_code)

try:
    result = response.json()
    print(json.dumps(result, indent=2, ensure_ascii=False))
except ValueError:
    result = {}
    print(response.text)

response.raise_for_status()

if result.get("error"):
    raise RuntimeError(
        json.dumps(result["error"], ensure_ascii=False)
    )

if not result.get("data"):
    raise RuntimeError("响应中没有图片数据")

# 打印第二轮生成的图片地址（临时签名 URL，有效期 12 小时，请及时下载转存）
print("\n第二轮图片地址：")
print(result["data"][0].get("url"))

# 将第二轮上下文保存为 JSON 文件，可用于继续第三轮及后续编辑
if result.get("assembled_history"):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    output_path = Path(__file__).with_name(
        f"hunyuan_round2_{timestamp}.json"
    )

    with output_path.open("w", encoding="utf-8") as file:
        json.dump(
            {
                "model": payload["model"],
                "session": payload["session"],
                "messages": payload["messages"],
                "assembled_history": result["assembled_history"],
                "latest_image_url": result["data"][0].get("url")
            },
            file,
            ensure_ascii=False,
            indent=2
        )

    print(f"\n第二轮上下文已保存：{output_path}")
```

## 返回示例

```json
{
  "created": 1789720660,
  "data": [
    {
      "url": "https://aigc-output-image-file-1326893053.cos.ap-guangzhou.myqcloud.com/xxx/round2.png?..."
    }
  ],
  "request_id": "c3e22f29-263d-6fcc-dcg1-d9gdh4de56dc",
  "usage": {
    "total_tokens": 20000
  },
  "assembled_history": [
    {
      "role": "assistant",
      "content": [
        { "type": "text", "text": "为了按要求创建图片，我将使用生成工具。" }
      ],
      "reasoning": "用户希望把圣诞小帽换成牛仔帽，并将整体色调调整为西部牛仔风格...",
      "tool_calls": [
        {
          "id": "generate@call_0",
          "type": "function",
          "function": {
            "name": "generate",
            "arguments": "{\"recaption\":\"...\"}"
          }
        }
      ]
    },
    {
      "role": "tool",
      "tool_call_id": "generate@call_0",
      "content": [
        {
          "type": "image_url",
          "image_url": {
            "url": "http://hunyuan-image-result-tob-1258344703.cos.ap-guangzhou.myqcloud.com/xxx/round2.png?..."
          }
        }
      ]
    },
    {
      "role": "assistant",
      "content": [
        { "type": "text", "text": "你请求的图片已完成。" }
      ]
    }
  ]
}
```

<p align="center">
  <small>© 2026 DMXAPI hy-image-v3.5-preview 多轮对话</small>
</p>
