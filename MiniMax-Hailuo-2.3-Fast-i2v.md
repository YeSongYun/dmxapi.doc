# MiniMax 海螺 MiniMax-Hailuo-2.3-Fast 图生视频 API 使用文档

MiniMax-Hailuo-2.3-Fast 是海螺视频生成系列的高速版模型，支持以图片作为起始帧生成高质量视频。该模型在保持出色画面质量的同时显著提升生成速度，支持 768P 和 1080P 两档分辨率，最长可生成 10 秒视频，并提供 15 种运镜指令实现精确的镜头控制，适合需要快速迭代的创意工作流。

## 接口地址

| 功能 | 请求方式 | URL |
|------|---------|-----|
| 提交任务 | POST | `https://www.dmxapi.cn/v1/responses` |
| 查询任务 | POST | `https://www.dmxapi.cn/v1/responses` |
| 下载视频 | POST | `https://www.dmxapi.cn/v1/responses` |

## 支持的模型

| 模型名称 | 说明 |
|---------|------|
| `MiniMax-Hailuo-2.3-Fast` | 海螺 2.3 高速版图生视频模型 |

:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。
:::


## 图生视频 示例代码

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
    # 【input】(string, 可选) 视频的文本描述，最大 2000 字符
    # 支持使用 "[指令]" 语法进行运镜控制
    # 支持 15 种运镜指令:
    #   左右移: [左移], [右移]
    #   左右摇: [左摇], [右摇]
    #   推拉: [推进], [拉远]
    #   升降: [上升], [下降]
    #   上下摇: [上摇], [下摇]
    #   变焦: [变焦推近], [变焦拉远]
    #   其他: [晃动], [跟随], [固定]
    # 组合运镜: 同一组 [] 内多个指令同时生效，如 [左摇,上升]，建议不超过 3 个
    # 顺序运镜: 前后出现的指令依次生效，如 "...[推进], 然后...[拉远]"
    "input": "A mouse runs toward the camera, smiling and blinking.",

    # 【first_frame_image】(string, 必填) 将指定图片作为视频的起始帧
    # 支持公网 URL 或 Base64 编码的 Data URL (data:image/jpeg;base64,...)
    # 图片要求:
    #   格式: JPG, JPEG, PNG, WebP
    #   体积: 小于 20MB
    #   尺寸: 短边像素大于 300px，长宽比在 2:5 和 5:2 之间
    "first_frame_image": "https://cdn.hailuoai.com/prod/2024-09-18-16/user/multi_chat_file/9c0b5c14-ee88-4a5b-b503-4f626f018639.jpeg",

    # 【model】(enum<string>, 必填) 模型名称
    "model": "MiniMax-Hailuo-2.3-Fast",

    # 【prompt_optimizer】(boolean, 可选) 是否自动优化 prompt
    # 默认值为 true，设为 false 可进行更精确的控制
    "prompt_optimizer": True,

    # 【fast_pretreatment】(boolean, 可选) 是否缩短 prompt_optimizer 的优化耗时
    # 默认值为 false
    "fast_pretreatment": False,

    # 【duration】(integer, 可选) 视频时长（秒），默认值为 6
    # MiniMax-Hailuo-2.3-Fast 可用值:
    #   768P 分辨率: 6 或 10
    #   1080P 分辨率: 6
    "duration": 6,

    # 【resolution】(enum<string>, 可选) 视频分辨率
    # MiniMax-Hailuo-2.3-Fast 可用值:
    #   6 秒视频: "768P"(默认), "1080P"
    #   10 秒视频: "768P"(默认)
    "resolution": "1080P",

    # 【aigc_watermark】(boolean, 可选) 是否在生成的视频中添加水印
    # 默认值为 false
    "aigc_watermark": False
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
  "task_id": "418221057708420",
  "base_resp": {
    "status_code": 0,
    "status_msg": "success"
  },
  "usage": {
    "total_tokens": 23100,
    "input_tokens": 0,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 23100,
    "output_tokens_details": {
      "reasoning_tokens": 0
    }
  }
}
```

## 查询视频生成状态 示例代码

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
    # 【model】(string, 必填) 查询任务专用模型标识
    "model": "MiniMax-Hailuo-query",

    # 【input】(object, 必填) 查询参数
    "input": {
        # 【task_id】(string, 必填) 提交任务时返回的任务 ID
        "task_id": "418221057708420"
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

## 返回示例

```json
{
  "base_resp": {
    "status_code": 0,
    "status_msg": "success"
  },
  "file_id": "418201399554182",
  "status": "Success",
  "task_id": "418197520085420",
  "usage": {
    "total_tokens": 0,
    "input_tokens": 0,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 0,
    "output_tokens_details": {
      "reasoning_tokens": 0
    }
  },
  "video_height": 1080,
  "video_width": 1920
}
```


## 下载视频 示例代码

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
    # 【model】(string, 必填) 下载视频专用模型标识
    "model": "MiniMax-Hailuo-get",

    # 【input】(object, 必填) 下载参数
    "input": {
        # 【file_id】(string, 必填) 查询任务时返回的文件 ID
        "file_id": "418201399554182"
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

## 返回示例

```json
{
  "base_resp": {
    "status_code": 0,
    "status_msg": "success"
  },
  "file": {
    "file_id": 418201399554182,
    "bytes": 0,
    "created_at": 1783658254,
    "filename": "output_aigc.mp4",
    "purpose": "video_generation",
    "download_url": "https://public-cdn-video-data-algeng.oss-cn-wulanchabu.aliyuncs.com/..."
  },
  "usage": {
    "total_tokens": 0,
    "input_tokens": 0,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 0,
    "output_tokens_details": {
      "reasoning_tokens": 0
    }
  }
}
```


## 完整工作流程

1. **提交任务** → 调用 `/v1/responses`（model: `MiniMax-Hailuo-2.3-Fast`），获得 `task_id`
2. **轮询查询** → 定期调用 `/v1/responses`（model: `MiniMax-Hailuo-query`），等待 `status: "Success"`，获得 `file_id`
3. **下载视频** → 调用 `/v1/responses`（model: `MiniMax-Hailuo-get`），获取 `download_url` 并下载视频文件

<p align="center">
  <small>&copy; 2026 DMXAPI MiniMax 海螺 视频生成</small>
</p>
