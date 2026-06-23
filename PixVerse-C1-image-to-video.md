# PixVerse-C1 图生视频 API 使用文档

PixVerse-C1 是拍我AI（PaiVideo）推出的新一代图生视频模型。基于上传的参考图像和文字提示，可生成 1~15 秒任意时长的高质量视频，支持最高 1080p 画质输出，内置 5 种艺术风格预设（动漫、3D 动画、日常、赛博朋克、漫画），并可选择开启同步音频生成。适用于社交媒体内容创作、广告营销、产品演示等多种图像驱动型视频生成场景。

:::warning
使用本 API 前，请先完成前置依赖文档中的调用以获取必要的参数值。
本模型请使用 `pixverse-picture` 上传。

[前置依赖文档](https://doc.dmxapi.cn/paiwo_image_upload.html)
:::

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
    # 【model】(string, 必需) 模型名称
    # 本文档对应模型: "PixVerse-C1"
    "model": "PixVerse-C1",

    # 【input】(string, 必需) 文本提示词（对应官方文档中的 prompt 字段）
    # 描述希望生成视频的内容画面
    # 长度限制: 2048 Characters 以内
    "input": "可爱的小猫在海边愉快的玩耍",

    # 【img_id】(integer, 必需) 上传图片后获取的图片 ID
    # 通过前置依赖"拍我图片上传 API"调用后返回的 img_id
    "img_id": 177602101,

    # 【style】(string, 可选) 视频风格预设，如非必要可不传
    # 可选值: "anime"(动漫) / "3d_animation"(3D 动画) / "day"(日常) /
    #         "cyberpunk"(赛博朋克) / "comic"(漫画)
    "style": "3d_animation",

    # 【duration】(integer, 必需) 视频生成时长（单位: 秒）
    # 取值范围: 1~15 秒
    "duration": 5,

    # 【quality】(string, 必需) 视频画质
    # 可选值: "360p" / "540p" / "720p" / "1080p"
    "quality": "540p",

    # 【generate_audio_switch】(boolean, 可选) 控制音频开关
    # true: Audio on (开启音频生成)
    # false: Audio off (关闭音频生成)
    "generate_audio_switch": True,

    # 【seed】(integer, 可选) 随机数种子
    # 取值范围: 0 - 2147483647
    # 相同 seed 在相同参数下可复现生成结果
    "seed": 0,

    # 【negative_prompt】(string, 可选) 负向提示词
    # 描述不希望出现在视频中的元素
    # 长度限制: 2048 Characters 以内
    "negative_prompt": "string",

    # 【motion_mode】(string, 可选) 运动模式
    # 可选值: "normal"(标准模式)
    "motion_mode": "normal",

    # 【template_id】(integer, 可选) 模板(特效) ID
    # 使用前需先激活对应模板
    # 0 表示不使用模板
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
    "video_id": 397959847631781,
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

> 返回示例中的 `Resp.video_id` 即为任务 ID，用于下一步"获取结果"查询。

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
    # 【model】(string, 必需) 固定使用查询模型
    "model": "paiwo-get",

    # 【input】(string, 必需) 上一步提交任务返回的 video_id
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

> 返回结果中 `Resp.url` 即为生成的视频下载地址，`status` 字段表示任务状态。

<p align="center">
  <small>© 2026 DMXAPI PixVerse-C1 图生视频</small>
</p>
