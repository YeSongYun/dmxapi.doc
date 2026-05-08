# PixVerse-C1 文生视频 API 使用文档

PixVerse-C1 是拍我 AI（PixVerse）最新一代 C1 系列文生视频模型，通过文本提示词驱动生成高质量短视频。相比前代模型，C1 支持 1~15 秒任意时长自由选择、最高 1080p 画质，覆盖 8 种画幅比例（含 21:9 超宽与 2:3/3:2 等竖屏/横屏场景），并内置可开关的 AI 配音（generate_audio_switch）能力。支持 0~2147483647 范围的 seed 随机数控制以复现结果，normal/fast 双运动模式以及特效模板（template_id）扩展，适合营销素材、短视频创意、游戏概念演示等多场景的快速视觉生产。

## 模型名称

- `PixVerse-C1`

## 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 提交任务 | POST | `https://www.dmxapi.cn/v1/responses` |
| 获取结果 | POST | `https://www.dmxapi.cn/v1/responses` |

:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。
:::

## 文生视频 示例代码

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
    # 【model】(string, 必需) 使用的视频生成模型名称
    # 本文档仅演示 PixVerse-C1 模型；模型值由 DMXAPI 侧路由到官方 c1 系列
    "model": "PixVerse-C1",

    # 【input】(string, 必需) 文本提示词（prompt），描述希望生成的视频画面内容
    # 长度限制: 5000 Characters 以内
    "input": "可爱的小猫在海边愉快的玩耍",

    # 【duration】(integer, 必需) 视频生成时长（秒）
    # v3.5/v4/v4.5: 5/8 (v3.5 1080p 无法使用 8)
    # v5: 5/8
    # v5.5/v5.6: 5/8/10 (1080p 无法使用 10)
    # v6/c1: 1~15 任意时长
    "duration": 5,

    # 【quality】(string, 必需) 视频分辨率
    # 可选值: "360p" / "540p" / "720p" / "1080p"
    "quality": "540p",

    # 【aspect_ratio】(string, 必需) 画幅比例
    # 基础提供: "16:9","9:16","4:3","3:4","1:1"
    # v6/c1 扩展支持: "16:9","9:16","4:3","3:4","1:1","2:3","3:2","21:9"
    "aspect_ratio": "16:9",

    # 【generate_audio_switch】(boolean, 可选) 音频开关
    # 支持 v5.5 / v5.6 / v6 / c1
    # true: Audio on (开启音频)
    # false: Audio off (关闭音频)
    "generate_audio_switch": True,

    # 【seed】(integer, 可选) 随机数种子，用于复现生成结果
    # 取值范围: 0 - 2147483647
    "seed": 0,

    # 【negative_prompt】(string, 可选) 负向提示词，用于描述不希望在视频中出现的元素
    # 长度限制: 2048 Characters 以内（根据示例代码推断，官方请求参数文档未单独列出）
    "negative_prompt": "string",

    # 【motion_mode】(string, 可选) 运动模式
    # PixVerse-C1 模型仅支持 "normal"（经实测验证）
    # "fast" 模式仅适用于 v3.5 / v4 / v4.5 模型，C1 传 "fast" 将返回 HTTP 400
    # 错误码: pixverse_c1_400017 "motion_mode:fast is only supported for models v3.5, v4, and v4.5."
    "motion_mode": "normal",

    # 【template_id】(integer, 可选) 模板(特效)ID
    # 使用前需先在平台激活对应模板；传 0 表示不使用特效模板
    "template_id": 0,
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

## 返回示例

```json
{
  "ErrCode": 0,
  "ErrMsg": "success",
  "Resp": {
    "video_id": 397959714188216,
    "credits": 50
  },
  "usage": {
    "total_tokens": 150000,
    "input_tokens": 0,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 150000,
    "output_tokens_details": {
      "reasoning_tokens": 0
    }
  }
}
```

返回的 `Resp.video_id` 即为异步生成任务的 ID，请保存该值并在下一步「获取结果」接口中作为 `input` 传入。

## 获取结果 示例代码

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
    # 【model】(string, 必需) 固定值 "paiwo-get"，表示调用拍我 AI 视频任务查询接口
    "model": "paiwo-get",

    # 【input】(string, 必需) 上一步「提交任务」接口返回的 Resp.video_id
    # 该 ID 用于查询对应视频生成任务的最新状态与结果 URL
    "input": "398402303529744",
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

## 返回示例

```json
{
  "ErrCode": 0,
  "ErrMsg": "Success",
  "Resp": {
    "id": 398402303529744,
    "prompt": "可爱的小猫在海边愉快的玩耍",
    "negative_prompt": "string",
    "url": "https://media.pixverseai.cn/pixverse%2Fmp4%2Fmedia%2Fweb%2Fori%2F5d302b9d-4d96-43d1-9729-ca3502a2af8c_seed1949340905.mp4",
    "status": 1,
    "seed": 1949340905,
    "create_time": "2026-04-20T03:12:09Z",
    "modify_time": "2026-04-20T03:12:43Z",
    "outputWidth": 1024,
    "outputHeight": 576,
    "has_audio": true,
    "credits": 50
  }
}
```

返回的 `Resp.url` 字段即为最终可下载/播放的视频链接。

<p align="center">
  <small>© 2026 DMXAPI PixVerse-C1 文生视频</small>
</p>
