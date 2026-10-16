# doubao-seedance-2-5-260628 首尾帧生视频 API 使用文档

基于 Doubao Seedance 2.5 的首尾帧生视频接口，通过 `/v1/responses` 端点以异步任务方式调用：同时传入首帧与尾帧 2 张图片（`role` 分别设为 `first_frame` 与 `last_frame`），模型自动补全两帧之间的运动过程与转场，并按提示词生成同步音效。相比全模态参考生视频，本任务能严格保障成片的起止画面与指定图片一致；首尾帧图片可以相同，宽高比不一致时以首帧为准、尾帧自动居中裁剪适配，输出宽高比亦随首帧图片自动确定（仅支持 `adaptive`）。图片支持公网 URL、Base64 编码、素材 ID 三种传入方式，单张不超过 30 MB，适合定格动画、产品形态变换、创意转场等需要精确控制起止画面的场景。

## 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 提交任务 | POST | `https://www.dmxapi.cn/v1/responses` |
| 获取结果 | POST | `https://www.dmxapi.cn/v1/responses` |



:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。如果怀疑密钥已泄露，请立即前往 DMXAPI 官网重新生成。
:::

:::warning 异步任务，请妥善保存任务 ID
本模型为**异步任务**接口：提交任务后不会直接返回视频，只返回一个任务 ID（响应中的 `id` 字段），需再用查询模型 `seedance-2-5-get` 凭该 ID 换取最终视频地址。请在提交成功后立即将任务 ID 落库或写入日志妥善保存——一旦丢失将无法找回，本次生成结果也无法再取回，但费用已产生。
:::

## 模型名称

- `doubao-seedance-2-5-260628`

## 首尾帧生视频 示例代码

```python
import requests
import json
import base64
import binascii
import os

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
# 步骤3: 配置图片来源（选择一种即可）
# ===============================================================

# 【方式一】网络图片 URL（支持 HTTP / HTTPS 协议）
# image_source = "https://img.shetu66.com/2023/07/14/1689320796087949.png"

# 【方式二】本地图片路径（代码自动转换为 Data URL）
image_source = "C:/path/input_image.png"

# 【方式三】素材 ID
# image_source = "asset://<ASSET_ID>"

# ===============================================================
# 步骤4: 配置请求参数
# ===============================================================

payload = {
    # 【model】(string, 必填) 调用的模型名称
    "model": "doubao-seedance-2-5-260628",

    # 【input】(object, 必填) 输入信息
    "input": {
        # 【content】(object[], 必填) 输入内容列表
        # 输入给模型生成视频的信息，本示例传入 1 段文本提示词 + 首帧、尾帧共 2 张图片
        "content": [
            {
                # 【text】(string, 必填) 文本提示词
                # 输入给模型的文本提示词，描述期望生成的视频
                # 语言支持: 中英文，额外支持西班牙语、印度尼西亚语、葡萄牙语、日语、马来语、
                #           泰语、阿拉伯语、越南语、韩语
                # 字数建议: 中文提示词不超过 500 字，英文提示词不超过 1000 词
                #           字数过多易导致信息分散，模型可能忽略细节、仅关注重点，
                #           进而造成视频缺失部分元素
                "text": "图1中小狗跳到图二小狗身上，对着镜头说\"茄子\"，360度环绕运镜",

                # 【type】(string, 必填) 内容类型
                # 输入内容的类型，此处固定为 text
                "type": "text"
            },
            {
                # 【image_url】(object, 必填) 图片对象
                # 输入给模型的图片对象
                "image_url": {
                    # 【url】(string, 必填) 图片来源
                    # 支持图片 URL、图片 Base64 编码、素材 ID 三种形式:
                    #   - 图片 URL: 填入图片的公网 URL
                    #   - Base64 编码: 遵循格式 data:image/<图片格式>;base64,<Base64 编码>
                    #                  注意 <图片格式> 需小写，如 data:image/png;base64,{base64_image}
                    #   - 素材 ID: 遵循格式 asset://<ASSET_ID>，可从素材 & 虚拟人像库获取
                    # 传入单张图片要求:
                    #   - 格式: jpeg、png、webp、bmp、tiff、gif，额外支持 heic、heif
                    #   - 宽高比(宽/高): [0.4, 2.5]
                    #   - 宽高长度(px): [300, 6000]
                    #   - 大小: 单张图片小于 30 MB，请求体大小不超过 64 MB
                    #           大文件请勿使用 Base64 编码
                    #   - 数量: 图生视频-首尾帧 2 张
                    "url": image_source
                },

                # 【role】(string, 可选) 角色/用途
                # 图片的位置或用途。图生视频-首尾帧需要传入 2 个 image_url 对象，且 role 必填
                # 首帧图片对应的 role 为 first_frame
                # 注意: 图生视频-首帧、图生视频-首尾帧、全模态参考生视频为 3 种互斥场景，不可混用
                "role": "first_frame",

                # 【type】(string, 必填) 内容类型
                # 输入内容的类型，此处固定为 image_url
                "type": "image_url"
            },
            {
                # 【image_url】(object, 必填) 图片对象
                # 输入给模型的图片对象
                "image_url": {
                    # 【url】(string, 必填) 图片来源
                    # 支持图片 URL、图片 Base64 编码、素材 ID 三种形式:
                    #   - 图片 URL: 填入图片的公网 URL
                    #   - Base64 编码: 遵循格式 data:image/<图片格式>;base64,<Base64 编码>
                    #                  注意 <图片格式> 需小写，如 data:image/png;base64,{base64_image}
                    #   - 素材 ID: 遵循格式 asset://<ASSET_ID>，可从素材 & 虚拟人像库获取
                    # 传入单张图片要求:
                    #   - 格式: jpeg、png、webp、bmp、tiff、gif，额外支持 heic、heif
                    #   - 宽高比(宽/高): [0.4, 2.5]
                    #   - 宽高长度(px): [300, 6000]
                    #   - 大小: 单张图片小于 30 MB，请求体大小不超过 64 MB
                    #           大文件请勿使用 Base64 编码
                    #   - 数量: 图生视频-首尾帧 2 张
                    "url": "https://img.sucaijishi.com/uploadfile/2023/0301/20230301120626930.png?imageMogr2/format/jpg/blur/1x0/quality/60"
                },

                # 【role】(string, 可选) 角色/用途
                # 图片的位置或用途。尾帧图片对应的 role 为 last_frame
                # 说明: 传入的首尾帧图片可相同；首尾帧图片的宽高比不一致时，以首帧图片为主，
                #       尾帧图片会自动裁剪适配
                "role": "last_frame",

                # 【type】(string, 必填) 内容类型
                # 输入内容的类型，此处固定为 image_url
                "type": "image_url"
            }
        ],

        # 【duration】(integer, 可选) 视频时长
        # 生成视频时长（单位：秒），默认值 -1
        # 取值范围: [4, 30]；或设置为 -1（智能选择，模型在有效取值范围内自主选择合适的整数秒时长）
        # 说明: 查询任务接口返回的 duration = 实际总帧数 / 24（向下取整），为整数秒约数
        "duration": 5,

        # 【generate_audio】(boolean, 可选) 生成有声视频
        # 控制生成的视频是否包含与画面同步的声音，默认值 true
        # 可选值:
        #   - True(模型输出的视频包含同步音频，会基于文本提示词与视觉内容自动生成
        #          匹配的人声、音效及背景音乐)
        #   - False(模型输出的视频为无声视频)
        # 建议将对话部分置于双引号内以优化音频生成效果
        # 注意: 生成的有声视频均为单声道，和传入的音频声道数无关
        "generate_audio": True,

        # 【ratio】(string, 可选) 视频宽高比
        # 生成视频的宽高比例，默认值 adaptive
        # 可选值: "16:9" / "4:3" / "1:1" / "3:4" / "9:16" / "21:9"
        #         "adaptive"(根据任务类型和输入内容自动适配宽高比)
        # 注意: 首帧 / 首尾帧生视频任务仅支持配置为 adaptive，不支持指定具体宽高比
        "ratio": "adaptive",
    }
}

# 媒体处理逻辑（无需修改）

_MEDIA_RULES = {
    "rule_1": {
        "allow_url": True,
        "allow_data_uri": True,
        "allow_raw_base64": False,
        "allow_asset": True,
        "allow_local_file": True,
        "local_encoding": "data_uri",
        "file_formats": {
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".png": "image/png",
            ".bmp": "image/bmp",
            ".webp": "image/webp",
            ".gif": "image/gif",
            ".heic": "image/heic",
            ".heif": "image/heif",
        },
        "data_types": ["image/bmp", "image/gif", "image/heic", "image/heif", "image/jpeg", "image/png", "image/webp"],
    },
}

def _resolve_media(value: str, rule: dict, field: str) -> tuple:
    if not isinstance(value, str) or not value:
        raise ValueError(f"{field} 必须是非空字符串")
    if value.startswith(("http://", "https://")):
        if rule["allow_url"]:
            return value, "url"
        raise ValueError(f"{field} 不接受 URL")
    if value.startswith("data:"):
        if not rule["allow_data_uri"]:
            raise ValueError(f"{field} 不接受 Data URI")
        header, sep, encoded = value.partition(",")
        expected = {f"data:{media_type};base64" for media_type in rule["data_types"]}
        if not sep or header not in expected or not encoded:
            raise ValueError(f"{field} 的 Data URI 头无效；允许: {sorted(expected)}")
        try:
            base64.b64decode(encoded, validate=True)
        except (binascii.Error, ValueError):
            raise ValueError(f"{field} 的 Data URI 正文不是合法 Base64")
        return value, "data_uri"
    if value.lower().startswith("asset://"):
        if rule["allow_asset"] and len(value) > len("asset://"):
            return value, "asset"
        raise ValueError(f"{field} 不接受素材 ID，或素材 ID 为空")
    if os.path.isfile(value):
        if not rule["allow_local_file"]:
            raise ValueError(f"{field} 不接受本地文件")
        ext = os.path.splitext(value)[1].lower()
        if ext not in rule["file_formats"]:
            raise ValueError(f"{field} 不支持本地文件格式 {ext}；允许: {sorted(rule['file_formats'])}")
        with open(value, "rb") as f:
            encoded = base64.b64encode(f.read()).decode("ascii")
        if rule["local_encoding"] == "raw_base64":
            return encoded, "raw_base64"
        media_type = rule["file_formats"][ext]
        return f"data:{media_type};base64,{encoded}", "data_uri"
    if rule["allow_raw_base64"]:
        try:
            base64.b64decode(value, validate=True)
            return value, "raw_base64"
        except (binascii.Error, ValueError):
            pass
    raise ValueError(f"{field} 不符合接口媒体契约")

payload["input"]["content"][1]["image_url"]["url"] = _resolve_media(payload["input"]["content"][1]["image_url"]["url"], _MEDIA_RULES["rule_1"], "payload[\"input\"][\"content\"][1][\"image_url\"][\"url\"]")[0]

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
  "output": [
    {
      "type": "message",
      "content": [
        {
          "type": "output_text",
          "text": "Task ID: task_8nwIq3EjxPoq7htirFxF7y7jK95Akef0"
        }
      ]
    }
  ],
  "usage": {
    "input_tokens": 0,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 108000,
    "output_tokens_details": {
      "reasoning_tokens": 0
    },
    "total_tokens": 108000
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
   本脚本演示如何使用 requests 库查询视频生成任务并获取生成视频链接

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

    # 【model】(string, 必填) 查询视频生成任务使用的模型名称（官方文档未明确说明）
    "model": "seedance-2-5-get",

    # 【input】(string, 必填) 提交任务时返回的任务 ID
    # 视频生成任务 ID 仅保存 7 天（从 created_at 时间戳开始计算），超时后将自动清除
    # 创建视频生成任务为异步接口，获取 ID 后需通过本接口查询任务状态，
    # 任务成功后会输出生成视频的链接
    "input": "task_8nwIq3EjxPoq7htirFxF7y7jK95Akef0"

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
  "created_at": 1787313204,
  "duration": 5,
  "execution_expires_after": 172800,
  "framespersecond": 24,
  "generate_audio": true,
  "id": "task_8nwIq3EjxPoq7htirFxF7y7jK95Akef0",
  "model": "doubao-seedance-2-5-260628",
  "output": [
    {
      "type": "message",
      "content": [
        {
          "type": "output_text",
          "text": "https://ark-acg-cn-bejing.tos-cn-beijing.volces.com/doubao-seedance-2-5/5284b7e74fa5421a9d0168d285cb301e.mp4?X-Tos-Algorithm=TOS4-HMAC-SHA256&X-Tos-Credential=YOUR_ACCESS_KEY_ID%2F20260821%2Fcn-beijing%2Ftos%2Frequest&X-Tos-Date=20260821T115520Z&X-Tos-Expires=86399&X-Tos-Signature=c3d4e5f60718293a4b5c6d7e8f90a1b2c3d4e5f60718293a4b5c6d7e8f90a1b2&X-Tos-SignedHeaders=host"
        }
      ]
    }
  ],
  "ratio": "392:587",
  "resolution": "720p",
  "seed": 68649,
  "service_tier": "default",
  "status": "succeeded",
  "updated_at": 1787313312,
  "usage": {
    "completion_tokens": 108760,
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
  <small>© 2026 DMXAPI doubao-seedance-2-5-260628 首尾帧生视频</small>
</p>