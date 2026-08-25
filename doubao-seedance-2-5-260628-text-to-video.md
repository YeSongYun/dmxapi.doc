# doubao-seedance-2-5-260628 文生视频 API 使用文档

基于 Doubao Seedance 2.5 的文生视频接口，通过 `/v1/responses` 端点以异步任务方式调用：仅输入一段文本提示词即可直出带同步音效的视频。模型原生支持有声视频生成，会依据提示词与画面内容自动配上人声、音效与背景音乐；支持 480p / 720p / 1080p 三档分辨率与 16:9、4:3、1:1、3:4、9:16、21:9 六种宽高比（另可用 `adaptive` 由模型自动适配），单次可生成 4~30 秒视频，或设为 `-1` 由模型智能选择时长。提示词除中英文外还额外支持西班牙语、印度尼西亚语、葡萄牙语、日语、马来语、泰语、阿拉伯语、越南语、韩语共 9 个语种，适合广告短片、创意分镜、社交媒体内容等纯文本驱动的视频生产场景。

## 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 提交任务 | POST | `https://www.dmxapi.cn/v1/responses` |
| 获取结果 | POST | `https://www.dmxapi.cn/v1/responses` |



:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。如果怀疑密钥已泄露，请立即前往 DMXAPI 官网重新生成。
:::

:::warning 异步任务，请妥善保存任务 ID
本模型为**异步任务**接口：提交任务后不会直接返回视频，只返回一个任务 ID（响应中的 `id` 字段），需再用查询模型 `seedance-2-5-get` 凭该 ID 换取最终视频地址。请在提交成功后立即将任务 ID 落库或写入日志妥善保存——一旦丢失将无法找回，本次生成结果也无法再取回，但费用已产生。
:::

## 模型名称

- `doubao-seedance-2-5-260628`

## 文生视频 示例代码

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
    # 【input】(object[], 必填) 输入内容列表
    # 输入给模型生成视频的信息，支持文本、图片、视频、音频等多种类型的元素
    # 本示例为纯文本输入
    "input": [
        {
            # 【text】(string, 必填) 文本提示词
            # 输入给模型的文本提示词，描述期望生成的视频
            # 语言支持: 中英文，额外支持西班牙语、印度尼西亚语、葡萄牙语、日语、马来语、
            #           泰语、阿拉伯语、越南语、韩语
            # 字数建议: 中文提示词不超过 500 字，英文提示词不超过 1000 词
            #           字数过多易导致信息分散，模型可能忽略细节、仅关注重点，
            #           进而造成视频缺失部分元素
            "text": "小猫对着镜头打哈欠",

            # 【type】(string, 必填) 内容类型
            # 输入内容的类型，此处固定为 text
            "type": "text"
        }
    ],

    # 【duration】(integer, 可选) 视频时长
    # 生成视频时长（单位：秒），默认值 -1
    # 取值范围: [4, 30]；或设置为 -1（智能选择，模型在有效取值范围内自主选择合适的整数秒时长）
    # 说明: 查询任务接口返回的 duration = 实际总帧数 / 24（向下取整），为整数秒约数
    "duration": 5,

    # 【execution_expires_after】(integer, 可选) 任务超时阈值
    # 指定任务提交后的过期时间（单位：秒），从 created_at 时间戳开始计算，默认值 172800（48 小时）
    # 超过该时间后任务会被自动终止，并标记为 expired 状态
    # 取值范围: [3600, 259200]
    "execution_expires_after": 172800,

    # 【generate_audio】(boolean, 可选) 生成有声视频
    # 控制生成的视频是否包含与画面同步的声音，默认值 true
    # 可选值:
    #   - True(模型输出的视频包含同步音频，会基于文本提示词与视觉内容自动生成
    #          匹配的人声、音效及背景音乐)
    #   - False(模型输出的视频为无声视频)
    # 建议将对话部分置于双引号内以优化音频生成效果
    # 注意: 生成的有声视频均为单声道，和传入的音频声道数无关
    "generate_audio": True,

    # 【model】(string, 必填) 调用的模型名称
    "model": "doubao-seedance-2-5-260628",

    # 【output_format】(string, 可选) 输出格式
    # 输出视频的格式，默认值 mp4
    # 可选值:
    #   - "mp4"(通用格式，兼容性最好，采用标准色彩精度，可在网页、移动端、各类播放器
    #           及分发平台直接播放)
    #   - "mov"(面向专业场景的高色彩精度格式，更好地保持画面色彩与亮度一致性，适用于调色、
    #           抠像、合成等对色彩还原要求高的专业后期加工；推荐在视频编辑、视频延长场景
    #           使用 mov 格式作为输入和输出)
    # 注意: mov 格式采用 H.264 视频编码 + yuv444p 色度采样 + PCM 音频编码，部分播放器可能
    #       不兼容，常见支持的播放器有 IINA(仅 macOS)、VLC、mpv、ffplay
    "output_format": "mp4",

    # 【ratio】(string, 可选) 视频宽高比
    # 生成视频的宽高比例，默认值 adaptive
    # 可选值: "16:9" / "4:3" / "1:1" / "3:4" / "9:16" / "21:9"
    #         "adaptive"(根据任务类型和输入内容自动适配宽高比)
    "ratio": "adaptive",

    # 【resolution】(string, 可选) 视频分辨率
    # 视频分辨率，默认值 720p
    # 可选值: "480p" / "720p" / "1080p"
    # 各宽高比对应的宽高像素值:
    #   - 480p : 16:9 854×480、4:3 752×560、1:1 640×640、3:4 560×752、9:16 480×854、21:9 992×432
    #   - 720p : 16:9 1280×720、4:3 1112×834、1:1 960×960、3:4 834×1112、9:16 720×1280、21:9 1470×630
    #   - 1080p: 16:9 1920×1080、4:3 1664×1248、1:1 1440×1440、3:4 1248×1664、9:16 1080×1920、21:9 2206×946
    # 注意: 1080p 视频采用 10bit 位深与 H.265/HEVC 编码，能保留更丰富的色彩层次与更平滑的渐变
    #       过渡；H.265/HEVC 在少数播放环境中可能不兼容，可使用 VLC、MPV、QuickTime Player 播放
    "resolution": "720p",

    # 【return_last_frame】(boolean, 可选) 返回尾帧
    # 是否返回生成视频的尾帧图像，默认值 false
    # 可选值:
    #   - True(返回尾帧图像，可通过查询视频生成任务接口获取；尾帧图像格式为 png，
    #          宽高像素值与生成的视频保持一致，无水印)
    #   - False(不返回尾帧图像)
    # 使用该参数可实现生成多个连续视频：以上一个生成视频的尾帧作为下一个视频任务的首帧
    "return_last_frame": False,

    # 【watermark】(boolean, 可选) 视频水印
    # 生成视频是否包含水印，默认值 false
    # 可选值:
    #   - True(生成视频右下角会展示「AI 生成」水印)
    #   - False(生成视频不含水印)
    "watermark": False
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
  "output": [
    {
      "type": "message",
      "content": [
        {
          "type": "output_text",
          "text": "Task ID: task_PkucWMByIsMaeyVULkgA6Jqy7LukjBdm"
        }
      ]
    }
  ],
  "usage": {
    "input_tokens": 0,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 108000,
    "output_tokens_details": {
      "reasoning_tokens": 0
    },
    "total_tokens": 108000
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
   本脚本演示如何使用 requests 库查询视频生成任务并获取生成视频链接

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

    # 【model】(string, 必填) 查询视频生成任务使用的模型名称（官方文档未明确说明）
    "model": "seedance-2-5-get",

    # 【input】(string, 必填) 提交任务时返回的任务 ID
    # 视频生成任务 ID 仅保存 7 天（从 created_at 时间戳开始计算），超时后将自动清除
    # 创建视频生成任务为异步接口，获取 ID 后需通过本接口查询任务状态，
    # 任务成功后会输出生成视频的链接
    "input": "task_PkucWMByIsMaeyVULkgA6Jqy7LukjBdm"

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
  "created_at": 1787312176,
  "duration": 5,
  "execution_expires_after": 172800,
  "framespersecond": 24,
  "generate_audio": true,
  "id": "task_PkucWMByIsMaeyVULkgA6Jqy7LukjBdm",
  "model": "doubao-seedance-2-5-260628",
  "output": [
    {
      "type": "message",
      "content": [
        {
          "type": "output_text",
          "text": "https://ark-acg-cn-bejing.tos-cn-beijing.volces.com/doubao-seedance-2-5/772ef640ec344d769378e357b4570b90.mp4?X-Tos-Algorithm=TOS4-HMAC-SHA256&X-Tos-Credential=AKLTNTEwMTIwZTEzYWE0NDcwOWE1Yzk2MzQ0ZjViYTk3OWU%2F20260821%2Fcn-beijing%2Ftos%2Frequest&X-Tos-Date=20260821T113824Z&X-Tos-Expires=86399&X-Tos-Signature=c1700648ba5d8deba28119af1825436b94eb8fc5afee27147ba52c7c2f74a071&X-Tos-SignedHeaders=host"
        }
      ]
    }
  ],
  "ratio": "9:16",
  "resolution": "720p",
  "seed": 64259,
  "service_tier": "default",
  "status": "succeeded",
  "updated_at": 1787312282,
  "usage": {
    "completion_tokens": 108900,
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
  <small>© 2026 DMXAPI doubao-seedance-2-5-260628 文生视频</small>
</p>