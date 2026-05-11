# PixVerse-V6 文生视频 API 使用文档

PixVerse-V6 是 PixVerse 最新一代视频生成模型，支持通过文字描述直接生成高质量视频。采用两步异步模式：先提交生成任务获取 video_id，再通过 video_id 轮询获取最终视频链接。V6 版本支持 1~15 秒任意时长、8 种画幅比例（含超宽屏 21:9）、多镜头自动切换、AI 音频合成及智能提示词优化，最高输出 1080p 画质。

## 模型名称

- `PixVerse-V6`

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

# 步骤1: 配置 API 连接信息

# DMXAPI 服务端点地址
url = "https://www.dmxapi.cn/v1/responses"

# DMXAPI 密钥 (请替换为您自己的密钥)
# 获取方式: 登录 DMXAPI 官网 -> 个人中心 -> API 密钥管理
api_key = "sk-******************************************"

# 步骤2: 配置请求头

headers = {
    "Content-Type": "application/json",      # 指定请求体为 JSON 格式
    "Authorization": f"{api_key}",           # token 认证方式
}

# 步骤3: 配置请求参数

payload = {
    # 【model】(string, 必填) 模型名称
    "model": "PixVerse-V6",
    # 【input】(string, 必填) 视频生成提示词
    # 描述想要生成的视频内容，5000 字符以内
    "input": "可爱的小猫在海边愉快的玩耍",
    # 【duration】(integer, 必填) 视频生成时长（秒）
    # 可选值: 1~15 秒
    "duration": 5,
    # 【quality】(string, 必填) 视频输出画质
    # 可选值: "360p" / "540p" / "720p" / "1080p"
    "quality": "360p",
    # 【aspect_ratio】(string, 必填) 视频画幅比例
    #  "16:9" / "9:16" / "4:3" / "3:4" / "1:1" / "2:3" / "3:2" / "21:9"
    "aspect_ratio": "16:9",
    # 【generate_audio_switch】(boolean, 可选) 音频生成开关
    # true: 开启音频生成，false: 关闭音频生成
    "generate_audio_switch": True,
    # 【seed】(integer, 可选) 随机种子
    # 取值范围: 0 - 2147483647，固定种子可复现相同生成结果
    "seed": 0,
    # 【negative_prompt】(string, 可选) 负向提示词
    "negative_prompt": "",
    # 【motion_mode】(string, 可选) 运动模式
    # 可选值: "normal"(标准运动) / "fast"(快速运动)
    # 注意: "fast" 不支持 8s 时长
    "motion_mode": "normal",
    # 【template_id】(integer, 可选) 模板（特效）ID
    # 使用前需先在平台激活对应模板
    "template_id": 0,
    # 【generate_multi_clip_switch】(boolean, 可选) 多镜头控制开关
    # 支持 v5.6/v6，true: 多镜头模式，false: 单镜头模式
    "generate_multi_clip_switch": True,
    # 【thinking_type】(string, 可选) 提示词优化模式
    # 可选值: "enabled"(开启) / "disabled"(关闭) / "auto"(由模型自动决定，默认)
    "thinking_type": "auto",
}
# 步骤4: 发送请求并输出结果
response = requests.post(url, headers=headers, json=payload)
result = response.json()
print(json.dumps(result, indent=2, ensure_ascii=False))
# 提取任务 ID，用于第二步查询视频结果
video_id = result.get("video_id")
print(f"任务 ID: {video_id}")
```

## 返回示例

```json
{
  "video_id": 401769244895246,
  "credits": 45,
  "usage": {
    "total_tokens": 135000,
    "input_tokens": 0,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 135000,
    "output_tokens_details": {
      "reasoning_tokens": 0
    }
  }
}
```

## 获取结果 示例代码

```python
import requests
import json
import time
# DMXAPI 服务端点地址
url = "https://www.dmxapi.cn/v1/responses"
# DMXAPI 密钥 (请替换为您自己的密钥)
api_key = "sk-******************************************"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"{api_key}",
}
# 替换为第一步返回的 video_id
video_id = 401769244895246
payload = {
    # 【model】(string, 必填) 查询模型名称，固定为 PixVerse-V6-get
    "model": "paiwo-get",

    # 【input】(integer, 必填) 视频任务 ID
    # 填入第一步返回的 video_id 值
    "input": video_id,
}
# 轮询获取视频生成结果
while True:
    response = requests.post(url, headers=headers, json=payload)
    result = response.json()
    print(json.dumps(result, indent=2, ensure_ascii=False))
    # 提取视频链接
    video_url = result.get("video_url")
    if video_url:
        print(f"视频链接: {video_url}")
        break
    # 等待 5 秒后重试
    time.sleep(5)
```

## 返回示例

```json
{
  "video_url": "https://cdn.pixverse.ai/video/xxxxxx.mp4",
  "video_id": 401769244895246,
  "status": "succeeded",
  "usage": {
    "total_tokens": 135000,
    "input_tokens": 0,
    "output_tokens": 135000
  }
}
```

<p align="center">
  <small>© 2026 DMXAPI PixVerse-V6 文生视频</small>
</p>
