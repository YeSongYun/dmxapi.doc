# doubao-seedance-2-0-mini-260615 视频延长 API 使用文档

doubao-seedance-2-0-mini-260615 支持视频延长：输入 1 个待延长的参考视频 + 文本提示词描述后续内容（可选附带参考图片、参考音频），生成 1 个在原视频基础上向后延续的新视频。视频延长属于多模态参考生视频的子场景，模型根据提示词意图自动识别为延长任务。模型支持 480p/720p 分辨率（不支持 1080p 与 4k），视频时长范围 4~15 秒。视频生成采用两步异步模式：先提交任务获取任务 ID，再通过 `seedance-2-0-get` 模型查询并获取视频结果。

## 模型名称

- `doubao-seedance-2-0-mini-260615`

## 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 提交任务 | POST | `https://www.dmxapi.cn/v1/responses` |
| 获取结果 | POST | `https://www.dmxapi.cn/v1/responses` |

:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。
:::

:::warning 异步任务，请妥善保存任务 ID
本模型为**异步任务**接口：提交任务后不会直接返回视频，只返回一个任务 ID（响应中的 `id` 字段），需再用查询模型 `seedance-2-0-get` 凭该 ID 换取最终视频地址。请在提交成功后立即将任务 ID 落库或写入日志妥善保存——一旦丢失将无法找回，本次生成结果也无法再取回，但费用已产生。
:::

## 视频延长 示例代码

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
    "Content-Type": "application/json",
    "Authorization": f"{api_key}",
}

# 步骤3: 配置待延长视频来源（二选一即可）

# 【方式一】网络视频 URL
video_source = "https://ark-project.tos-cn-beijing.volces.com/doc_video/r2v_tea_video1.mp4"

# 【方式二】素材 ID
# video_source = "asset://<VIDEO_ASSET_ID>"

# 步骤4: 配置请求参数

payload = {
    # 【model】(string, 必填) 模型名称，指定使用 doubao-seedance-2-0-mini 模型
    "model": "doubao-seedance-2-0-mini-260615",

    # 【input】(array, 必填) 输入内容数组
    # 视频延长需传入至少 1 个 type=video_url 的对象作为待延长视频，role 为 "reference_video"
    # 文本提示词描述后续要延续的内容，模型据此判定为延长任务
    # 提示词建议中文不超过500字，英文不超过1000词
    # 额外支持西班牙语、印度尼西亚语、葡萄牙语、日语
    "input": [
        {
            "type": "text",
            "text": "接着视频1的最后一个镜头继续，人物转身走向远处的街道，镜头跟随平移，背景灯光逐渐亮起，保持原有的画面风格与运镜节奏",
        },
        {
            # 【video_url.url】视频 URL 或素材 ID（asset://<ASSET_ID>），不支持 Base64
            "type": "video_url",
            "video_url": {
                "url": video_source
            },
            # 【role】(string, 必填) 参考视频固定为 "reference_video"
            "role": "reference_video",
        },
    ],

    # 【ratio】(string, 可选) 视频宽高比，默认值 adaptive
    # 可选值: "16:9" / "4:3" / "1:1" / "3:4" / "9:16" / "21:9" / "adaptive"
    # "adaptive": 由模型根据待延长视频在可选宽高比中自动选择
    "ratio": "adaptive",

    # 【resolution】(string, 可选) 视频分辨率，默认值 720p
    # 可选值: "480p" / "720p"（seedance 2.0 mini 不支持 1080p 和 4k）
    "resolution": "720p",

    # 【duration】(integer, 可选) 视频时长（秒）
    # 取值范围: [4, 15]，或 -1 由模型在有效范围内自主选择合适时长
    # 传 -1 时按 15 秒预扣费，实际时长确定后多退少补
    # 注意: 视频时长与计费相关，请谨慎设置
    "duration": 8,

    # 【generate_audio】(boolean, 可选) 是否生成同步音频（人声/音效/背景音乐），默认值 true
    # true: 模型自动生成与画面匹配的人声、音效及背景音乐
    # false: 输出无声视频
    # 注意: 生成的有声视频均为单声道，与传入音频的声道数无关
    "generate_audio": True,

    # 【seed】(integer, 可选) 随机种子，默认值 -1
    # 取值范围: [-1, 2147483647]；-1 表示使用随机数
    "seed": -1,

    # 【watermark】(boolean, 可选) 是否包含水印，默认值 false
    # true: 生成视频右下角展示「AI 生成」水印
    "watermark": False,

    # 【return_last_frame】(boolean, 可选) 是否返回视频尾帧图像，默认值 false
    # true: 返回尾帧图像（png 格式，宽高与视频一致，无水印）
    # 可将本次的尾帧用于后续任务，实现多段连续视频
    "return_last_frame": False,

    # 【execution_expires_after】(integer, 可选) 任务超时时间（秒）
    # 取值范围: [3600, 259200]，默认 172800（48小时）
    # 从 created_at 开始计算，超时后任务终止并标记为 expired
    "execution_expires_after": 172800,

    # 【callback_url】(string, 可选) 任务状态回调地址
    # 状态说明: queued(排队中) / running(运行中) / succeeded(成功) / failed(失败) / expired(超时)
    "callback_url": "https://www.dmxapi.cn",

    # 【tools】(array, 可选) 工具配置，开启联网搜索
    # web_search: 模型根据提示词自主判断是否搜索互联网内容，可提升视频时效性但增加时延
    "tools": [{"type": "web_search"}],
}

# 步骤5: 发送请求并输出结果

response = requests.post(url, headers=headers, json=payload)
print(json.dumps(response.json(), indent=2, ensure_ascii=False))
```

## 返回示例

```json
{
  "id": "cgt-20260820144736-kn2xf",
  "usage": {
    "total_tokens": 43120,
    "input_tokens": 0,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 43120,
    "output_tokens_details": {
      "reasoning_tokens": 0
    }
  }
}
```

> 返回的 `id` 字段即为任务 ID，用于第二步查询视频生成结果。

## 获取结果 示例代码

```python
import requests
import json

url = "https://www.dmxapi.cn/v1/responses"

# DMXAPI 密钥 (请替换为您自己的密钥)
api_key = "sk-******************************************"

headers = {
    "Content-Type": "application/json",
    # 获取结果接口使用 Bearer 认证方式
    "Authorization": f"Bearer {api_key}",
}

payload = {
    # 【model】(string, 必填) 查询模型，固定为 seedance-2-0-get
    "model": "seedance-2-0-get",

    # 【input】(string, 必填) 第一步提交任务返回的任务 ID
    "input": "cgt-20260820144736-kn2xf"
}

response = requests.post(url, headers=headers, json=payload)
result = response.json()

# 用量与计费：output_tokens 即本次实际扣费依据
print("用量:")
print(json.dumps(result.get("usage", {}), indent=2, ensure_ascii=False))

# 解析任务详情与视频链接
try:
    text = result["output"][0]["content"][0]["text"]
    inner = json.loads(text)

    # 格式化打印任务详情：含实际生成参数（时长/分辨率/宽高比/随机种子/帧率等）
    # text 本身是被转义的 JSON 字符串，直接打印会挤成一行，需先 json.loads 再格式化
    print("\n任务详情:")
    print(json.dumps(inner, indent=2, ensure_ascii=False))

    video_url = inner["content"]["video_url"]
    print(f"\n视频链接: {video_url}")
    last_frame_url = inner["content"].get("last_frame_url")
    if last_frame_url:
        print(f"尾帧图像: {last_frame_url}")
except Exception as e:
    print(f"提取 URL 失败: {e}")
```

## 返回示例

```json
{
  "request_id": "cgt-20260820144736-kn2xf",
  "output": [
    {
      "type": "message",
      "content": [
        {
          "type": "output_text",
          "text": "{\"content\":{\"video_url\":\"https://ark-acg-cn-beijing.tos-cn-beijing.volces.com/doubao-seedance-2-0-mini/02178748456700000000000000000000000ffffac1167b9c45f8.mp4?X-Tos-Algorithm=TOS4-HMAC-SHA256\\u0026X-Tos-Credential=AKLTYWJkZTExNjA1ZDUyNDc3YzhjNTM5OGIyNjBhNDcyOTQ%2F20260820%2Fcn-beijing%2Ftos%2Frequest\\u0026X-Tos-Date=20260820T064736Z\\u0026X-Tos-Expires=86400\\u0026X-Tos-Signature=f60718293a4b5c6d7e8f90a1b2c3d4e5f60718293a4b5c6d7e8f90a1b2c3d4e5\\u0026X-Tos-SignedHeaders=host\"},\"id\":\"cgt-20260820144736-kn2xf\",\"model\":\"doubao-seedance-2-0-mini-260615\",\"status\":\"succeeded\"}"
        }
      ]
    }
  ],
  "usage": {
    "total_tokens": 43120,
    "input_tokens": 0,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 43120,
    "output_tokens_details": {
      "reasoning_tokens": 0
    }
  }
}

视频链接: https://ark-acg-cn-beijing.tos-cn-beijing.volces.com/doubao-seedance-2-0-mini/02178748456700000000000000000000000ffffac1167b9c45f8.mp4?X-Tos-Algorithm=TOS4-HMAC-SHA256&X-Tos-Credential=AKLTYWJkZTExNjA1ZDUyNDc3YzhjNTM5OGIyNjBhNDcyOTQ%2F20260820%2Fcn-beijing%2Ftos%2Frequest&X-Tos-Date=20260820T064736Z&X-Tos-Expires=86400&X-Tos-Signature=f60718293a4b5c6d7e8f90a1b2c3d4e5f60718293a4b5c6d7e8f90a1b2c3d4e5&X-Tos-SignedHeaders=host
```

<p align="center">
  <small>© 2026 DMXAPI doubao-seedance-2-0-mini-260615 视频延长</small>
</p>
