# wan2.7-r2v-2026-06-12 多主体参考(图像+视频+音色) API 使用文档

`wan2.7-r2v-2026-06-12` 是通义万相 2.7 系列的参考生视频模型，通过 `/v1/responses` 端点以「提交任务 + 轮询查询」两步异步方式调用。支持在一次请求中混合传入参考图像与参考视频（合计最多 5 个）作为角色、道具、场景的视觉参考，并可为图像/视频中的主体角色额外指定 1~10 秒的 wav/mp3 音色参考（reference_voice），提示词中通过"图1、视频1"这类标识精确指代各素材。本文档演示 4 张参考图 + 1 段参考视频 + 2 条音色参考的多主体协同场景，生成最高 1080P 的有声视频（时长上限：参考素材含视频时 10 秒、纯图像参考时 15 秒），适合多角色对话短剧、商品情景展示、虚拟角色互动等创作场景。

## 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 提交任务 | POST | `https://www.dmxapi.cn/v1/responses` |
| 获取结果 | POST | `https://www.dmxapi.cn/v1/responses` |



:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。如果怀疑密钥已泄露，请立即前往 DMXAPI 官网重新生成。
:::

## 模型名称

- `wan2.7-r2v-2026-06-12`

## 多主体参考(图像+视频+音色) 示例代码

```python
import base64
import os

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
    # 【model】(string, 必填) 调用的模型名称
    "model": "wan2.7-r2v-2026-06-12",

    # 【input】(object, 必填) 输入的基本信息，如提示词等
    "input": {
        # 【prompt】(string, 必填) 文本提示词，用来描述生成视频中期望包含的元素和视觉特点
        # 支持中英文，每个汉字、字母、标点占一个字符，不超过 5000 个字符，超过部分会自动截断
        # 参考指代: 中文提示词中参考图片用"图1、图2"标识指代，参考视频用"视频1、视频2"标识指代
        #           (英文提示词写为"Image 1"、"Video 1"，字母和数字之间有空格，首字母大写)
        # 顺序与 media 数组顺序一致，图和视频分别计数（即同时存在图1、视频1）:
        #   第 1 个 reference_image 对应图1，第 2 个对应图2，以此类推
        #   第 1 个 reference_video 对应视频1，第 2 个对应视频2，以此类推
        # 画面描述支持两种写法: 直接使用标识指代（如"图1在图2里玩耍"），
        # 或结合主体与场景补充说明（如"图1的猫在图2的房间里玩耍"）
        "prompt": "视频1抱着图3，在图4的椅子上弹奏一支舒缓的乡村民谣，并说道：“今天的阳光真好。”图1手中拿着图2，路过视频1，把手中的图2放到视频1旁边的桌子上，并说道：“真好听，能不能再唱一遍”。 ",

        # 【negative_prompt】(string, 可选) 反向提示词，用来描述不希望在视频画面中出现的内容，可以对视频画面进行限制
        # 支持中英文，长度不超过 500 个字符，超过部分会自动截断
        "negative_prompt": "汽车",

        # 【media】(array, 必填) 媒体素材数组，素材包括图像、视频和音频
        # 支持图像/视频输入作为视觉参考，图像支持多视图，常见参考角色、道具、场景等
        # 数组中每个元素为一个媒体对象，包含 type 与 url 字段
        # 素材限制:
        #   - 首帧图像最多传入 1 张
        #   - 参考图像和参考视频至少传入 1 个，参考图像 + 参考视频 ≤ 5
        #   - 参考素材为主体角色时，仅包含单一角色
        "media": [
            {
                # 【media[].type】(string, 必填) 媒体素材类型
                # 可选值: "reference_image"(参考图像，提供主体角色和场景参考)
                #         / "reference_video"(参考视频，提供主体角色和音色参考，不推荐传入空镜视频)
                #         / "first_frame"(首帧图像，基于首帧生成视频)
                "type": "reference_image",
                # 【media[].url】(string, 必填) 媒体素材 URL，每个值可指向一张图像或一段视频
                # 参考图像限制:
                #   - 格式: JPEG、JPG、PNG（不支持透明通道）、BMP、WEBP
                #   - 分辨率: 宽度和高度范围为 [240, 8000] 像素
                #   - 宽高比: 1:8 ~ 8:1
                #   - 文件大小: 不超过 20MB
                # 支持公网 URL (HTTP/HTTPS)、OSS 临时 URL 或 Base64 编码
                # (数据格式 data:{MIME_type};base64,{base64_data})
                "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260408/sjuytr/wan-r2v-object-girl.jpg",
                # 【media[].reference_voice】(string, 可选) 音频 URL，用于指定参考素材（图像/视频）中主体角色的音色
                # 与 reference_image 或 reference_video 搭配使用；该音频仅参考音色，与说话内容无关
                # 建议参考音频语种与提示词语种保持一致，匹配效果更佳
                # 音频限制: 格式 wav/mp3；时长 1~10s；文件大小不超过 15MB
                # 支持公网 URL (HTTP/HTTPS)、OSS 临时 URL
                "reference_voice": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260408/gbqewz/wan-r2v-girl-voice.mp3"
            },
            {
                # 参考视频: 视频内容建议包含主体（人物/动物/物体），仅包含一个角色
                # 若视频有声音，也可以参考音色
                # 参考视频限制:
                #   - 格式: mp4、mov
                #   - 时长: 1~30s
                #   - 分辨率: 宽度和高度范围为 [240, 4096] 像素
                #   - 宽高比: 1:8 ~ 8:1
                #   - 文件大小: 不超过 100MB 
                # 支持公网 URL (HTTP/HTTPS)、OSS 临时 URL
                "type": "reference_video",
                "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/qigswt/wan-r2v-role2.mp4",
                # 音频生效逻辑:
                #   - 默认行为: 若 reference_video 本身包含音频，但未指定 reference_voice，默认使用视频原声
                #   - 优先级: 若同时传入 reference_video(含音频)和 reference_voice，
                #             则优先使用 reference_voice 的音色，覆盖视频原声
                "reference_voice": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260408/isllrq/wan-r2v-boy-voice.mp3"
            },
            {
                "type": "reference_image",
                "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/rtjeqf/wan-r2v-object3.png"
            },
            {
                "type": "reference_image",
                "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/qpzxps/wan-r2v-object4.png"
            },
            {
                "type": "reference_image",
                "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/wfjikw/wan-r2v-backgroud5.png"
            }
        ]
    },

    # 【parameters】(object, 可选) 视频处理参数，如设置视频分辨率
    "parameters": {
        # 【resolution】(string, 可选) 生成视频的分辨率档位，用于控制视频的清晰度（总像素）
        # 可选值: "720P" / "1080P"(默认值)
        # 注意: resolution 直接影响费用，请在调用前确认模型价格
        "resolution": "720P",

        # 【ratio】(string, 可选) 生成视频的宽高比
        # 可选值: "16:9"(默认值) / "9:16" / "1:1" / "4:3" / "3:4"
        # 生效逻辑:
        #   - 未传入首帧图像: 按指定的 ratio 参数生成视频
        #   - 已传入首帧图像: 自动忽略 ratio 参数，以首帧图像的宽高比生成近似比例的视频
        "ratio": "16:9",

        # 【duration】(integer, 可选) 生成视频的时长，单位为秒，默认值为 5
        # 取值范围:
        #   - 当参考素材中包含视频时: [2, 10] 之间的整数
        #   - 当参考素材中不包含视频时: [2, 15] 之间的整数
        # 注意: duration 直接影响费用，请在调用前确认模型价格
        "duration": 10,

        # 【prompt_extend】(boolean, 可选) 是否开启 prompt 智能改写，开启后使用大模型对输入 prompt 进行智能改写
        # 对于较短的 prompt 生成效果提升明显，但会增加耗时
        # 可选值: True(默认值，开启智能改写) / False(不开启智能改写)
        "prompt_extend": False,

        # 【watermark】(boolean, 可选) 是否添加水印标识，水印位于视频右下角，文案固定为"AI生成"
        # 可选值: False(默认值，不添加水印) / True(添加水印)
        "watermark": True,

        # 【seed】(integer, 可选) 随机数种子，取值范围为 [0, 2147483647]
        # 未指定时，系统自动生成随机种子；若需提升生成结果的可复现性，建议固定 seed 值
        # 由于模型生成具有概率性，即使使用相同 seed，也不能保证每次生成结果完全一致
        "seed": 23
    }
}

# ===============================================================
# 步骤4: 媒体输入处理
# ===============================================================
# - 公网 URL (http/https): 原样传入
# - 本地文件路径: 自动读取并转为 data:{MIME_type};base64,{base64_data}

_MIME_MAP = {
    ".bmp": "image/bmp",
    ".gif": "image/gif",
    ".jpeg": "image/jpeg",
    ".jpg": "image/jpeg",
    ".png": "image/png",
    ".webp": "image/webp",
}

def _file_to_data_uri(path: str) -> str:
    ext = os.path.splitext(path)[1].lower()
    mime = _MIME_MAP.get(ext)
    if mime is None:
        raise ValueError(f"不支持的文件格式 {ext}: {path}")
    with open(path, "rb") as f:
        data = base64.b64encode(f.read()).decode("ascii")
    return f"data:{mime};base64,{data}"

def resolve_media(path_or_url: str) -> str:
    """公网 URL 原样返回; 本地文件转 base64 data URI; 其他一律报错。"""
    if path_or_url.startswith(("http://", "https://")):
        return path_or_url
    if path_or_url.startswith("data:"):
        return path_or_url
    if os.path.isfile(path_or_url):
        return _file_to_data_uri(path_or_url)
    raise ValueError(f"无法识别的输入（不是公网 URL，本地文件也不存在）: {path_or_url}")

# 图片：可填公网 URL 或本地文件路径（如 r"C:\文件\示例.bmp"）
payload["input"]["media"][0]["url"] = resolve_media(payload["input"]["media"][0]["url"])
payload["input"]["media"][2]["url"] = resolve_media(payload["input"]["media"][2]["url"])
payload["input"]["media"][3]["url"] = resolve_media(payload["input"]["media"][3]["url"])
payload["input"]["media"][4]["url"] = resolve_media(payload["input"]["media"][4]["url"])

# ===============================================================
# 步骤5: 发送请求并输出结果
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
  "request_id": "c7ae2022-430c-9d40-aac6-d17c1b62de7a",
  "output": [
    {
      "type": "message",
      "content": [
        {
          "type": "output_text",
          "text": "{\"task_id\":\"4aef21e1-248f-4fcd-96c2-082850462800\",\"task_status\":\"PENDING\"}"
        }
      ]
    }
  ],
  "usage": {
    "input_tokens": 0,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 60000,
    "output_tokens_details": {
      "reasoning_tokens": 0
    },
    "total_tokens": 60000
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
   本脚本通过任务 ID 查询视频生成任务的状态与结果
   任务状态: PENDING(排队中) / RUNNING(处理中) / SUCCEEDED(成功)
             FAILED(失败) / CANCELED(已取消) / UNKNOWN(任务不存在或状态未知)

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

    "model": "wan2.7-get",
    "input": "4aef21e1-248f-4fcd-96c2-082850462800"

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
  "request_id": "d4f02c3a-d0e3-9f70-af8a-f499feabb855",
  "output": [
    {
      "type": "message",
      "content": [
        {
          "type": "output_text",
          "text": "{\"task_id\":\"4aef21e1-248f-4fcd-96c2-082850462800\",\"task_status\":\"RUNNING\",\"submit_time\":\"2026-07-14 16:52:38.329\",\"scheduled_time\":\"2026-07-14 16:52:38.369\"}"
        }
      ]
    }
  ],
  "usage": {
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
  <small>© 2026 DMXAPI wan2.7-r2v-2026-06-12 多主体参考(图像+视频+音色)</small>
</p>
