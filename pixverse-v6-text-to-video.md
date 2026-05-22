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

url = "https://www.dmxapi.cn/v1/responses"
api_key = "sk-**************************************"  # 填你的 key

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}",  # 标准是带 Bearer 前缀
}

video_id = 404136280092976

payload = {
    "model": "paiwo-get",
    "input": str(video_id),  # 必须是字符串，且用变量值不要写字面量
}

max_retries = 60  # 最长轮询 5 分钟
for i in range(max_retries):
    response = requests.post(url, headers=headers, json=payload)

    print("=" * 60)
    print(f"[第 {i+1} 次] HTTP Status: {response.status_code}")
    print(f"Response Headers: {dict(response.headers)}")
    print(f"Raw Body:\n{response.text}")
    print("=" * 60)

    try:
        result = response.json()
    except Exception as e:
        print(f"JSON 解析失败: {e}")
        break

    if "error" in result:
        print(f"接口返回错误，停止轮询: {result['error']}")
        break

    video_url = result.get("video_url") or (result.get("Resp") or {}).get("url")
    if video_url:
        print(f"视频链接: {video_url}")
        break

    time.sleep(5)
else:
    print("轮询超时，未获取到视频链接")
```

## 返回示例

```json
============================================================
[第 1 次] HTTP Status: 200
Response Headers: {'Server': 'nginx', 'Date': 'Fri, 22 May 2026 13:03:27 GMT', 'Content-Type': 'application/json; charset=utf-8', 'Content-Length': '431', 'Connection': 'keep-alive', 'X-Rixapi-Request-Id': '20260522210326751646573zOace2dW', 'Strict-Transport-Security': 'max-age=31536000'}
Raw Body:
{"ErrCode":0,"ErrMsg":"Success","Resp":{"id":404137115562463,"prompt":"可爱的小猫在海边愉快的玩耍","negative_prompt":"","url":"https://media.pixverseai.cn/pixverse%2Fmp4%2Fmedia%2Fweb%2Fori%2F5242b6ba-0b25-4f87-956f-3c08cfc85a1c_seed413618676.mp4","status":1,"seed":413618676,"create_time":"2026-05-22T13:02:10Z","modify_time":"2026-05-22T13:02:27Z","outputWidth":640,"outputHeight":360,"has_audio":true,"credits":7}}

============================================================
视频链接: https://media.pixverseai.cn/pixverse%2Fmp4%2Fmedia%2Fweb%2Fori%2F5242b6ba-0b25-4f87-956f-3c08cfc85a1c_seed413618676.mp4
```

<p align="center">
  <small>© 2026 DMXAPI PixVerse-V6 文生视频</small>
</p>
