# wan3.0-video 文生视频 API 使用文档

基于通义万相 3.0 视频生成模型的文生视频接口，通过 `/v1/responses` 端点以异步任务方式调用。仅凭一段最长 20000 字符的文本提示词即可直接生成带原生音频的视频，支持 480P / 720P / 1080P 三档分辨率、2~30 秒自定义时长（传 `-1` 进入智能时长模式由模型自行推荐）、6 种宽高比与自适应比例，并内置 prompt 智能改写，适合广告创意、短视频内容、概念演示等从零开始的视频创作场景。

## 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 提交任务 | POST | `https://www.dmxapi.cn/v1/responses` |
| 获取结果 | POST | `https://www.dmxapi.cn/v1/responses` |


:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。如果怀疑密钥已泄露，请立即前往 DMXAPI 官网重新生成。
:::

## 模型名称

- `wan3.0-video`

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
    # 【input】(object, 必填) 输入的基本信息
    # prompt 和 media 必填其一
    "input": {
        # 【prompt】(string, 条件必选) 文本提示词，用来描述期望生成的视频内容
        # 和 media 必填其一
        # 支持中英文，每个汉字/字母占一个字符，不超过 20000 个字符，超过部分会自动截断
        # 在全能参考模式下，prompt 中可以用"图1""视频1""音频1"等指代 media 数组中
        # 对应顺序的媒体素材
        "prompt": "一只小猫在月光下的屋顶上奔跑，城市的霓虹灯在远处闪烁，电影级画质，流畅运镜。"
    },

    # 【model】(string, 必填) 调用的模型名称
    # wan3.0-video：标准版
    "model": "wan3.0-video",

    # 【parameters】(object, 可选) 视频处理参数
    "parameters": {
        # 【duration】(integer, 可选) 生成视频的时长，单位为秒
        # 默认值为 5
        #   - 无视频输入时: 取值范围为 [2, 30] 的整数
        #   - 传 -1 时: 智能时长模式，模型根据输入的 prompt、内容和富媒体自动推荐合适时长生成
        "duration": 5,
        # 【prompt_extend】(boolean, 可选) 是否开启 prompt 智能改写
        # 开启后使用大模型对输入 prompt 进行智能改写
        # 对于较短的 prompt 生成效果提升明显，但会增加耗时
        # 可选值: True(默认值，开启智能改写) / False(不开启智能改写)
        "prompt_extend": True,
        # 【ratio】(string, 可选) 生成视频的宽高比
        # 可选值:
        #   - "adaptive"(默认值，自适应长宽比，根据输入媒体比例和意图自动推荐合适的长宽比)
        #   - "16:9" / "4:3" / "1:1" / "3:4" / "9:16"
        "ratio": "adaptive",
        # 【resolution】(string, 可选) 生成视频的分辨率档位
        # 默认值为 1080P
        # 可选值: "1080P" / "720P" / "480P"
        "resolution": "480P",
        # 【audio】(boolean, 可选) 输出视频是否包含音频
        # 可选值:
        #   - True(默认值，输出视频包含声音)
        #   - False(输出视频不包含音轨)
        # 开关声音价格相同
        "audio": True,
        # 【seed】(integer, 可选) 随机种子，用于复现生成结果
        # 取值范围: [0, 2147483647]
        "seed": 0,
        # 【watermark】(boolean, 可选) 是否添加水印标识
        # 可选值: False(默认值，不添加水印) / True(添加水印)
        "watermark": False
    },
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
          "text": "e47a17af-3089-452a-9115-984647090120"
        }
      ]
    }
  ],
  "provider_metadata": {
    "task_id": "e47a17af-3089-452a-9115-984647090120",
    "task_status": "PENDING"
  },
  "request_id": "2c9b6ccd-88e4-9228-8d92-15b9c2551457",
  "usage": {
    "input_tokens": 0,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 15000,
    "output_tokens_details": {
      "reasoning_tokens": 0
    },
    "total_tokens": 15000
  }
}
```

返回中的 `task_id`（即 `output` 数组内的任务 ID 文本）用于第二步查询生成结果，`task_status` 为 `PENDING` 表示任务已排队等待处理。

## 获取生成视频 示例代码

```python
"""
╔═══════════════════════════════════════════════════════════════╗
║                  DMXAPI 自研接口                               ║
╚═══════════════════════════════════════════════════════════════╝

📝 功能说明:
   本脚本演示如何使用 requests 库调用 DMXAPI 的自研接口

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
api_key = "sk-***********************************************"

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

    "model": "wan3.0-get",
    "input": "e47a17af-3089-452a-9115-984647090120"

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
  "output": [
    {
      "type": "message",
      "content": [
        {
          "type": "output_text",
          "text": "https://dashscope-a717.oss-accelerate.aliyuncs.com/1d/50/20260828/e4b11e52/e47a17af-3089-452a-9115-984647090120.mp4?Expires=1787975571&OSSAccessKeyId=LTAI5tPxpiCM2hjmWrFXrym1&Signature=CP7ELkaB4hgdVt%2Fi88GNv39%2BeOE%3D"
        }
      ]
    }
  ],
  "request_id": "b7005146-9683-9897-b4dc-2ff2476dd8fa",
  "usage": {
    "SR": 480,
    "duration": 5,
    "fps": 30,
    "input_tokens": 0,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "input_video_duration": 0,
    "output_tokens": 0,
    "output_tokens_details": {
      "reasoning_tokens": 0
    },
    "output_video_duration": 5,
    "ratio": "16:9",
    "total_tokens": 0,
    "video_count": 1
  }
}
```

<p align="center">
  <small>© 2026 DMXAPI wan3.0-video 文生视频</small>
</p>
