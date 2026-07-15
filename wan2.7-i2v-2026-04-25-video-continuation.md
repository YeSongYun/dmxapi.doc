# wan2.7-i2v-2026-04-25 视频续写 API 使用文档

`wan2.7-i2v-2026-04-25` 是通义万相 2.7 系列的图生视频模型，通过 `/v1/responses` 端点以「提交任务 + 轮询查询」两步异步方式调用。本文档演示视频续写用法：传入一段 2~10 秒的 mp4/mov 首段视频（first_clip），模型在保持画面主体与风格连贯的前提下续写后续内容，输出总时长由 duration 参数控制（上限 15 秒）——例如输入 3 秒视频、duration=15 时续写生成 12 秒，最终输出 15 秒完整视频。还支持 first_clip+last_frame 组合，让续写内容收束到指定尾帧。输入视频支持公网 URL 或 OSS 临时 URL、文件不超过 100MB，适合短视频扩展、剧情延续、片段补全等场景。

## 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 提交任务 | POST | `https://www.dmxapi.cn/v1/responses` |
| 获取结果 | POST | `https://www.dmxapi.cn/v1/responses` |



:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。如果怀疑密钥已泄露，请立即前往 DMXAPI 官网重新生成。
:::

## 模型名称

- `wan2.7-i2v-2026-04-25`

## 视频续写 示例代码

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
api_key = "sk-******************************************"

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
    # 【model】(string, 必填) 调用的模型名称
    "model": "wan2.7-i2v-2026-04-25",

    # 【input】(object, 必填) 输入的基本信息，如提示词等
    "input": {
        # 【prompt】(string, 可选) 文本提示词，用来描述生成视频中期望包含的元素和视觉特点
        # 支持中英文，长度不超过 5000 个字符，每个汉字/字母占一个字符，超过部分会自动截断
        "prompt": "一个女孩对镜自拍，自拍结束后背着书包出门",

        # 【media】(array, 必填) 媒体素材列表，用于指定视频生成所需的参考素材（图像、音频和视频）
        # 数组的每个元素为一个媒体对象，包含 type 与 url 字段
        # 视频续写仅支持以下素材组合，非法组合将报错:
        #   - 首段视频续写: first_clip
        #   - 首段视频+尾帧续写: first_clip + last_frame
        # 每种 type 在 media 数组中最多出现一次
        "media": [
            {
                # 【media[].type】(string, 必填) 媒体素材类型，此处为 "first_clip"(首视频片段)
                "type": "first_clip",
                # 【media[].url】(string, 必填) 视频文件的 URL，模型将基于该视频内容进行续写生成
                # 续写时长的上限由 duration 参数控制
                # (例如: 当 duration=15 时，输入视频 3 秒，则模型续写生成 12 秒，
                #  最终输出视频总时长 15 秒，按 15 秒计费)
                # 视频限制:
                #   - 格式: mp4、mov
                #   - 时长: 2~10s
                #   - 分辨率: 宽和高的范围为 [240, 4096] 像素
                #   - 宽高比: 1:8 ~ 8:1
                #   - 文件大小: 不超过 100MB
                # 支持公网 URL (HTTP/HTTPS) 或 OSS 临时 URL
                "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/hfugmr/wan-r2v-role1.mp4"
            },
            {
                # 【media[].type】(string, 必填) 媒体素材类型，此处为 "last_frame"(尾帧)
                "type": "last_frame",
                # 【media[].url】(string, 必填) 视频文件的 URL，模型将基于该视频内容进行续写生成
                # 续写时长的上限由 duration 参数控制
                # (例如: 当 duration=15 时，输入视频 3 秒，则模型续写生成 12 秒，
                #  最终输出视频总时长 15 秒，按 15 秒计费)
                # 视频限制:
                #   - 格式: png、jpg、jpeg
                #   - 分辨率: 宽和高的范围为 [240, 4096] 像素
                #   - 宽高比: 1:8 ~ 8:1
                #   - 文件大小: 不超过 100MB
                # 支持公网 URL (HTTP/HTTPS)
                "url": "https://example.com/last_frame.jpg"
            }
        ]
    },

    # 【parameters】(object, 可选) 视频处理参数，如设置视频分辨率、设置视频时长、开启 prompt 智能改写、添加水印等
    "parameters": {
        # 【resolution】(string, 可选) 生成视频的分辨率档位，用于控制视频的清晰度（总像素）
        # 可选值: "720P" / "1080P"(默认值)
        # 模型根据选择的分辨率档位，自动缩放至相近总像素，视频宽高比尽量与输入素材（首帧或首段视频）保持一致
        # 注意: resolution 直接影响费用，请在调用前确认模型价格
        "resolution": "720P",

        # 【duration】(integer, 可选) 生成视频的时长，单位为秒
        # 取值范围: [2, 15] 之间的整数，默认值为 5
        # 视频续写场景下，duration 为输出视频总时长（含输入片段），续写部分 = duration - 输入视频时长
        # 注意: duration 直接影响费用，按秒计费，请在调用前确认模型价格
        "duration": 10,

        # 【prompt_extend】(boolean, 可选) 是否开启 prompt 智能改写，开启后使用大模型对输入 prompt 进行智能改写
        # 对于较短的 prompt 生成效果提升明显，但会增加耗时
        # 可选值: True(默认值，开启智能改写) / False(不开启智能改写)
        "prompt_extend": True,

        # 【watermark】(boolean, 可选) 是否添加水印标识，水印位于视频右下角，文案固定为"AI生成"
        # 可选值: False(默认值，不添加水印) / True(添加水印)
        "watermark": True,

        # 【seed】(integer, 可选) 随机数种子，取值范围为 [0, 2147483647]
        # 未指定时，系统自动生成随机种子；若需提升生成结果的可复现性，建议固定 seed 值
        # 由于模型生成具有概率性，即使使用相同 seed，也不能保证每次生成结果完全一致
        "seed": 43
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
  "request_id": "28d1d8fb-589c-9e48-b0ed-b92854c9114b",
  "output": [
    {
      "type": "message",
      "content": [
        {
          "type": "output_text",
          "text": "{\"task_id\":\"764fa58b-d1ce-4f8b-a060-fd45aa5f44d6\",\"task_status\":\"PENDING\"}"
        }
      ]
    }
  ],
  "usage": {
    "input_tokens": 0,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 60000,
    "output_tokens_details": {
      "reasoning_tokens": 0
    },
    "total_tokens": 60000
  }
}
```

## 获取生成视频 示例代码

```python
"""
╔═══════════════════════════════════════════════════════════════╗
║                  DMXAPI 自研接口                               ║
╚═══════════════════════════════════════════════════════════════╝

📝 功能说明:
   本脚本通过任务 ID 查询视频生成任务的状态与结果
   任务状态: PENDING(排队中) / RUNNING(处理中) / SUCCEEDED(成功)
             FAILED(失败) / CANCELED(已取消) / UNKNOWN(任务不存在或状态未知)

═══════════════════════════════════════════════════════════════
"""

import requests
import json

# ═══════════════════════════════════════════════════════════════
# 🔑 步骤1: 配置 API 连接信息
# ═══════════════════════════════════════════════════════════════

# 🌐 DMXAPI 服务端点地址
url = "https://www.dmxapi.cn/v1/responses"

# 🔐 DMXAPI 密钥 (请替换为您自己的密钥)
# 获取方式: 登录 DMXAPI 官网 -> 个人中心 -> API 密钥管理
api_key = "sk-******************************************"

# ═══════════════════════════════════════════════════════════════
# 📋 步骤2: 配置请求头
# ═══════════════════════════════════════════════════════════════

headers = {
    "Content-Type": "application/json",      # 指定请求体为 JSON 格式
    "Authorization": f"{api_key}",    # token 认证方式
}

# ═══════════════════════════════════════════════════════════════
# 💬 步骤3: 配置请求参数
# ═══════════════════════════════════════════════════════════════

payload = {

    "model": "wan2.7-get",
    "input": "764fa58b-d1ce-4f8b-a060-fd45aa5f44d6"

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

## 返回示例

```json
{
  "request_id": "dee9a316-dd33-9af2-8461-9d712be7f8bb",
  "output": [
    {
      "type": "message",
      "content": [
        {
          "type": "output_text",
          "text": "{\"task_id\":\"764fa58b-d1ce-4f8b-a060-fd45aa5f44d6\",\"task_status\":\"SUCCEEDED\",\"submit_time\":\"2026-07-14 16:50:13.115\",\"scheduled_time\":\"2026-07-14 16:50:13.151\",\"end_time\":\"2026-07-14 16:51:12.797\",\"orig_prompt\":\"一个女孩对镜自拍，自拍结束后背着书包出门\",\"video_url\":\"https://dashscope-a717.oss-accelerate.aliyuncs.com/1d/4e/20260714/fa14b052/24663984-metadata_user_2611ebd846db4ea1_watermark.mp4?Expires=1784105471&OSSAccessKeyId=LTAI5tJjG6wsHad1Sf7iezX4&Signature=xpnjgpTPVGtsqmTVVoYkqAD3phU%3D\"}"
        }
      ]
    }
  ],
  "usage": {
    "input_tokens": 0,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 0,
    "output_tokens_details": {
      "reasoning_tokens": 0
    },
    "total_tokens": 0
  }
}
```

<p align="center">
  <small>© 2026 DMXAPI wan2.7-i2v-2026-04-25 视频续写</small>
</p>
