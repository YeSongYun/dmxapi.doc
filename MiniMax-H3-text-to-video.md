# MiniMax-H3 文生视频 API 使用文档

MiniMax-H3 视频生成 V2 接口，通过多模态 `content` 数组输入（文本 / 图片 / 视频 / 音频）驱动，2K 直出。文生视频场景仅需在数组中提供一个非空文本项，单个 `text` 最多 7000 个字符；支持 768P 与 2K 两档分辨率、4~15 秒整数时长，以及 21:9、16:9、4:3、1:1、3:4、9:16 六种宽高比（文生视频场景下 `ratio` 必填且不可为 `adaptive`）。接口以异步任务方式工作：提交后返回任务 ID，再用查询模型换取最终视频地址。

## 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 提交任务 | POST | `https://www.dmxapi.cn/v1/responses` |
| 获取结果 | POST | `https://www.dmxapi.cn/v1/responses` |



:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。如果怀疑密钥已泄露，请立即前往 DMXAPI 官网重新生成。
:::

:::warning 异步任务，请妥善保存 task_id
本模型为**异步任务**接口：提交任务后不会直接返回视频，只返回一个任务 ID（`task_id`），需再用查询模型 `MiniMax-H3-get` 凭该 ID 换取最终视频地址。请在提交成功后立即将 `task_id` 落库或写入日志妥善保存——一旦丢失将无法找回，本次生成结果也无法再取回，但费用已产生。
:::

## 模型名称

- `MiniMax-H3`

## 文生视频示例代码

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
    # 【model】(enum<string>, 必填) 模型名称
    # 可用值: "MiniMax-H3"
    "model": "MiniMax-H3",

    # 【input】(object[], 必填) 多模态输入内容数组，描述用于生成视频的信息
    # 每个元素通过 type 区分类型("text" / "image_url" / "video_url" / "audio_url")，
    # 并可通过 role 标注用途
    # 每次请求必须包含一个非空 text 项(prompt 必填)，缺失会返回参数错误
    # 文生视频场景: 仅一个 text 元素
    "input": [
        {
            # 【type】(enum<string>, 必填) 输入内容的类型
            # 可用值: "text" / "image_url" / "video_url" / "audio_url"
            "type": "text",

            # 【text】(string, 必填) 文本提示词(prompt)
            # 所有场景都需包含一个非空 text，描述期望生成的视频
            # 按字符数计算长度，单个 text 最多 7000 个字符
            "text": "史诗级太空歌剧院线预告：女舰长独自站在巨大观景窗前，最后一支舰队正在集结并跃迁离去，强光爆闪、舰桥震动，她被留在原地。"
        }
    ],

    # 【resolution】(enum<string>, 必填) 视频分辨率
    # 可用值: "768P" / "2K"
    "resolution": "2K",

    # 【duration】(enum<integer>, 必填) 生成视频时长(秒)，整数
    # 可用值: 4 / 5 / 6 / 7 / 8 / 9 / 10 / 11 / 12 / 13 / 14 / 15
    "duration": 5,

    # 【ratio】(enum<string>, 条件必填) 生成视频的宽高比
    # 文生视频(t2va，输入仅含 text)场景: ratio 必填，且不能为 "adaptive"
    # 本场景可用值: "21:9" / "16:9" / "4:3" / "1:1" / "3:4" / "9:16"
    "ratio": "16:9",

    # 【aigc_watermark】(boolean, 可选) 是否在生成视频中添加 AIGC 标识水印
    # 默认值: false
    "aigc_watermark": False
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
  "task_id": "427019898360251",
  "usage": {
    "total_tokens": 40000,
    "input_tokens": 0,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 40000,
    "output_tokens_details": {
      "reasoning_tokens": 0
    }
  }
}
```

返回中的 `task_id` 即任务 ID，用于后续查询任务状态与结果。**该 ID 仅在本次提交的响应中返回一次，请务必妥善保存**，丢失后无法找回本次任务。

## 获取生成视频 示例代码

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

    "model": "MiniMax-H3-get",
    "input": "427019898360251"

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
  "task": {
    "id": "427019898360251",
    "model": "MiniMax-H3",
    "status": "succeeded",
    "created_at": 1785813179,
    "updated_at": 1785813374,
    "content": {
      "url": "https://your-cdn.example.com/h3-generated-2k-output.mp4"
    },
    "resolution": "2K",
    "duration": 5,
    "usage": {
      "total_seconds": 5,
      "input_seconds": 0,
      "output_seconds": 5,
      "input_image_count": 0
    },
    "ratio": "16:9",
    "task_type": "generation"
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

任务状态 `status` 取值：`queued`（排队中）、`running`（运行中）、`succeeded`（成功）、`failed`（失败）、`cancelled`（已取消）。状态为 `succeeded` 时，`task.content.url` 即为生成视频的下载地址。

<p align="center">
  <small>© 2026 DMXAPI MiniMax-H3 文生视频</small>
</p>
