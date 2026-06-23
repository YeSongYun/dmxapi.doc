# PixVerse-C1 参考生视频 API 使用文档

PixVerse-C1 参考生视频是拍我 AI 推出的多主体（多参考）视频生成能力，通过 DMXAPI 聚合接口即可调用。支持同时传入 1–3 张主体或背景参考图，并使用 `@ref_name` 语法在提示词中精确引用对应角色或场景，实现主体一致性的生成效果。支持 `720p` 画质与 `2:3/3:2/21:9` 等 C1 专属画幅，最长可生成 5 秒视频，并可通过 `generate_audio_switch` 开启配套音频。
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

## 参考生视频 示例代码

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
api_key = "sk-**************************************"

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
    # 【image_references】(array[object], 必填) 图像引用数组，用于声明视频中的主体与背景
    # 对 C1 系列最多支持 1-3 个引用对象；每个对象包含 type / img_id / ref_name 三个必填字段
    # 子属性说明:
    #   type     (string, 必填) 引用类型，仅接受: "subject"(主体) / "background"(背景)
    #   img_id   (integer, 必填) 图片 ID，需先通过"上传图片"前置接口取得
    #   ref_name (string, 必填) 图片自定义名称，用于在 input/prompt 中通过 @ref_name 引用
    "image_references": [
        {
            "type": "subject",
            "img_id": 182641012,
            "ref_name": "dog",
        },
        {
            "type": "background",
            "img_id": 182641035,
            "ref_name": "sea",
        },
    ],

    # 【input】(string, 必填) 文本提示词，使用 @ref_name 精确描述场景
    # 规则 1: @ref_name 后必须有空格，例如 "@dog plays"
    # 规则 2: 提示词中引用的名称必须与 image_references 中的 ref_name 完全一致
    "input": "@dog plays at @sea",

    # 【model】(string, 必填) 模型名称，本接口固定使用 PixVerse-C1
    "model": "PixVerse-C1",

    # 【duration】(integer, 必填) 视频生成时长，单位为秒
    # PixVerse-C1 支持的时长为 5 秒
    "duration": 5,

    # 【quality】(string, 必填) 视频画质
    # 可选值: "360p" / "540p" / "720p" / "1080p"
    "quality": "720p",

    # 【aspect_ratio】(string, 必填) 视频画幅比
    # 基础支持: "16:9" / "9:16" / "4:3" / "3:4" / "1:1"/"2:3" / "3:2" / "21:9"
    "aspect_ratio": "2:3",

    # 【seed】(integer, 可选) 随机种子，用于控制生成结果的可复现性；相同种子+参数可生成近似结果
    "seed": 123456789,

    # 【generate_audio_switch】(boolean, 可选) 音频生成开关，仅支持 v5.6 与 C1
    # true: 生成带音频的视频 / false: 仅生成无音轨的视频
    "generate_audio_switch": True,
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

> `Resp.video_id` 即为后续查询视频结果的任务 ID。

```json
{
  "ErrCode": 0,
  "ErrMsg": "Success",
  "Resp": {
    "video_id": 397959606526648,
    "credits": 65
  },
  "usage": {
    "total_tokens": 195000,
    "input_tokens": 0,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 195000,
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

# ═══════════════════════════════════════════════════════════════
# 步骤1: 配置 API 连接信息
# ═══════════════════════════════════════════════════════════════

# DMXAPI 服务端点地址
url = "https://www.dmxapi.cn/v1/responses"

# DMXAPI 密钥 (请替换为您自己的密钥)
# 获取方式: 登录 DMXAPI 官网 -> 个人中心 -> API 密钥管理
api_key = "sk-**************************************"

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
    # 【model】(string, 必填) 查询模型名，固定为 "paiwo-get"
    "model": "paiwo-get",

    # 【input】(string, 必填) 传入提交任务接口返回的 video_id（任务 ID）
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

<p align="center">
  <small>© 2026 DMXAPI PixVerse-C1 参考生视频</small>
</p>
