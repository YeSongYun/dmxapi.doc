# PixVerse-C1 首尾帧生视频 API 使用文档

PixVerse-C1 首尾帧生视频接口通过同时提供首帧与尾帧两张参考图，基于 DMXAPI 的 `/v1/responses` 端点实现两步异步视频生成：提交任务拿到 `video_id`，再通过查询模型换取最终视频 URL。支持 1~15 秒任意时长、360p/540p/720p/1080p 四档画质，并提供音频开关、音效生成、对口型等扩展能力，可让两张图片之间以 AI 补全的方式平滑过渡成一段完整视频。

:::warning
使用本 API 前，请先完成前置依赖文档中的调用以获取必要的参数值。

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

## 首尾帧生视频 示例代码

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
    # 【model】(string, 必填) 模型名称
    # 本接口固定使用 PixVerse-C1 模型
    "model": "PixVerse-C1",

    # 【input】(string, 必填) 提示词文本, 2048 Characters 以内
    # 描述首尾帧之间的动作/场景演变过程, 用于引导 AI 补全中间帧
    "input": "可爱的小猫在海边愉快的玩耍",

    # 【first_frame_img】(integer, 必填) 首帧图片 ID
    # 来源于「上传图片」接口返回的 img_id, 用于指定视频的第一帧画面
    "first_frame_img": 177602101,

    # 【last_frame_img】(integer, 必填) 尾帧图片 ID
    # 来源于「上传图片」接口返回的 img_id, 用于指定视频的最后一帧画面
    "last_frame_img": 177602101,

    # 【duration】(integer, 必填) 视频生成时长, 单位秒
    # 取值范围: 1~15 任意整数
    "duration": 5,

    # 【quality】(string, 必填) 视频分辨率档位
    # 可选值: "360p" / "540p" / "720p" / "1080p"
    "quality": "540p",

    # 【generate_audio_switch】(boolean, 可选) 音频生成开关
    # true: 生成带音频的视频; false: 生成静音视频
    "generate_audio_switch": True,

    # 【seed】(integer, 可选) 随机种子
    # 取值范围: 0 ~ 2147483647, 相同种子可复现相近结果, 0 表示自动分配
    "seed": 0,

    # 【motion_mode】(string, 可选) 运镜/动作模式
    # 可选值: "normal"(常规模式)
    "motion_mode": "normal",
}

# ═══════════════════════════════════════════════════════════════
# 步骤4: 发送请求并输出结果
# ═══════════════════════════════════════════════════════════════

# 发送 POST 请求到 API 服务器
response = requests.post(url, headers=headers, json=payload)

# 格式化输出 JSON 响应
# - indent=2: 缩进 2 空格, 便于阅读
# - ensure_ascii=False: 正确显示中文字符
print(json.dumps(response.json(), indent=2, ensure_ascii=False))
```

## 返回示例

```json
{
  "ErrCode": 0,
  "ErrMsg": "success",
  "Resp": {
    "video_id": 397959966880294,
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

> `Resp.video_id` 即为本次任务 ID，需在「获取结果」步骤中作为 `input` 传入。

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
    "Content-Type": "application/json",
    "Authorization": f"{api_key}",
}

# ═══════════════════════════════════════════════════════════════
# 步骤3: 配置请求参数
# ═══════════════════════════════════════════════════════════════

payload = {
    # 【model】(string, 必填) 查询模型固定为 paiwo-get
    "model": "paiwo-get",

    # 【input】(string, 必填) 提交任务返回的 video_id, 以字符串形式传入
    "input": "398402303529744",
}

# ═══════════════════════════════════════════════════════════════
# 步骤4: 发送请求并输出结果
# ═══════════════════════════════════════════════════════════════
# 注意: 实测状态码语义
#   status == 5  : 生成中 (此时 url 字段可能已出现, 但文件未就绪, 下载会 404)
#   status == 1  : 完成, url 可直接下载
#   status == 7/8: 失败 / 审核失败
# 因此轮询判据应为 "status == 1 且 url 非空", 不能仅检查 url 是否存在

response = requests.post(url, headers=headers, json=payload)
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

<p align="center">
  <small>© 2026 DMXAPI PixVerse-C1 首尾帧生视频</small>
</p>
