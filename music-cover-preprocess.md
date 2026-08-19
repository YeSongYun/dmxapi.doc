# music-cover 翻唱前处理 API 使用文档

基于 MiniMax music-cover 模型的翻唱前处理接口，通过 `/v1/responses` 端点调用。该接口对参考音频做预处理，提取音频特征、自动识别并格式化歌词、分析歌曲结构（intro / verse / chorus / bridge / outro / inst / silence 及其起止时间戳），返回一个有效期 24 小时的 `cover_feature_id`。配合「music-cover 音乐生成」接口即可完成**两步翻唱流程**——先预处理拿到特征 ID 与歌词，按需修改歌词后再生成翻唱版本，适合需要自定义歌词、复用同一首参考音频多次生成的场景。
## 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 翻唱前处理 | POST | `https://www.dmxapi.cn/v1/responses` |



:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。如果怀疑密钥已泄露，请立即前往 DMXAPI 官网重新生成。
:::

## 模型名称

- `music-cover`

## 翻唱前处理 示例代码

```python
import base64
import binascii
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
    # 【model】(string, 必填) 调用的模型名称，必须为 "music-cover"
    "model": "music-cover",

    # 【input】(object, 必填) 输入信息
    "input": {
        # 【audio_url】(string, 条件必填) 参考音频的 URL 地址
        # audio_url 和 audio_base64 必须且只能提供其中一个
        # 参考音频要求:
        #   - 时长: 6 秒至 6 分钟
        #   - 大小: 最大 50MB
        #   - 格式: 支持常见音频格式(mp3、wav、flac 等)
        "audio_url": "https://music.163.com/song/media/outer/url?id=1330348068.mp3"

        # 【audio_base64】(string, 条件必填) Base64 编码的参考音频
        # 与 audio_url 二选一，音频要求同上
        # 使用本地音频文件时，下方"步骤4"会自动完成转换并切换到该字段
    }
}

# ===============================================================
# 步骤4: 媒体输入处理（严格按每个参数自己的接口契约）
# ===============================================================
# 本段代码用于把音频入参统一规整成接口能接受的形式，支持两种写法：
#   - 公网 URL       : 以 http:// 或 https:// 开头，原样透传，仍写入 audio_url 字段
#   - 本地文件路径   : 自动读取文件、转为裸 Base64（不带 data: 头），并改写入 audio_base64 字段
# 注意本接口的音频契约与图片不同：不接受 Data URI，本地文件编码为**裸 Base64**。
# 由于 audio_url 与 audio_base64 互斥，转换后必须删除另一个字段，这一步由下方代码自动完成。
# 若您只使用公网音频 URL，本段可以整体删除，不影响调用。
#
# - payload["input"]["audio_url"]（音频）
#   限制：时长 6 秒至 6 分钟
#   限制：大小最大 50MB
#   限制：支持常见音频格式(mp3、wav、flac 等)

# 媒体契约表：描述该字段允许哪些输入形式、本地文件如何编码、支持哪些格式
_MEDIA_RULES = {
    "rule_1": {
        "allow_url": True,               # 允许公网 URL
        "allow_data_uri": False,         # 不允许 Data URI
        "allow_raw_base64": True,        # 允许裸 Base64
        "allow_local_file": True,        # 允许本地文件路径
        "local_encoding": "raw_base64",  # 本地文件编码为裸 Base64
        # 本地文件允许的扩展名（音频无需 MIME 头，故值为空）
        "file_formats": {
            ".mp3": "",
            ".wav": "",
            ".m4a": "",
            ".aac": "",
            ".ogg": "",
            ".flac": "",
        },
        "data_types": [],
    },
}

def _resolve_media(value: str, rule: dict, field: str) -> tuple:
    """把媒体入参规整为接口可接受的形式，返回 (值, 形式)。形式为 url / data_uri / raw_base64。"""
    if not isinstance(value, str) or not value:
        raise ValueError(f"{field} 必须是非空字符串")

    # 情况一: 公网 URL，直接透传
    if value.startswith(("http://", "https://")):
        if rule["allow_url"]:
            return value, "url"
        raise ValueError(f"{field} 不接受 URL")

    # 情况二: Data URI（本接口不接受，保留分支以便统一错误提示）
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

    # 情况三: 本地文件路径，读取后按契约编码为裸 Base64
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

    # 情况四: 已经是裸 Base64 字符串
    if rule["allow_raw_base64"]:
        try:
            base64.b64decode(value, validate=True)
            return value, "raw_base64"
        except (binascii.Error, ValueError):
            pass

    raise ValueError(f"{field} 不符合接口媒体契约")

# 解析音频入参，并按解析结果写入互斥字段之一：URL -> audio_url，裸 Base64 -> audio_base64
_media_value_1, _media_form_1 = _resolve_media(payload["input"]["audio_url"], _MEDIA_RULES["rule_1"], "payload[\"input\"][\"audio_url\"]")
payload["input"].pop("audio_url", None)
payload["input"].pop("audio_base64", None)
_media_targets_1 = {"url": "audio_url", "raw_base64": "audio_base64"}
payload["input"][_media_targets_1[_media_form_1]] = _media_value_1

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
  "cover_feature_id": "c39f4e87d52f6b48a5837f60d84f2a38",
  "formatted_lyrics": "[Intro 1]\n\n[Intro 2]\n\n[Verse 1]\n这一路上走走停停穿著少年漂流的\n痕迹迈出车站的前一刻竟有些\n犹豫不禁笑著听伤情却仍\n无可避免而整夜的天依旧那么暖换坠进了\n\n[Pre-chorus 1]\n从前从前初识这世间万般流\n连看著天边似的眼前也甘愿赴汤蹈火去投胎一\n\n[Pre-chorus 2]\n如今走过这世间万般流连翻过\n岁月不动的脸措不及防闯入你的笑\n\n[Chorus 1]\n我曾面对白云世界之大也沉溺于其\n中梦话不得挣扎不做挣扎不惧\n\n[Chorus 2]\n笑话我曾将青春翻涌成她也\n曾指尖弹出盛夏心之所动且就随\n缘去吧逆著光行走任风\n\n[Inst 1]\n\n[Verse 2]\n短短的路走走停停也有了几分的\n距离不知抚摸的是故事还是段心\n情也许期待的不过是与时间\n为敌再次看到你微两千公里笑\n\n[Pre-chorus 3]\n得很甜蜜从前初识这世间万般流\n连看著天边似在眼前也甘愿赴汤蹈火去\n投胎一遍如今走过这世间\n\n[Pre-chorus 4]\n万般流连翻过岁月不动的脸措不及\n防闯入你的笑颜\n\n[Chorus 3]\n我曾难自拔于世界之大也沉\n溺于其中梦话不得挣扎不做挣扎不\n惧笑话我曾将青春翻涌成她\n也曾指尖弹出盛夏心之所动且就随缘去吧\n\n[Inst 2]\n\n[Inst 3]\n\n[Chorus 4]\n晚风吹起你鬓间的白发抚平回忆\n留下的疤你的眼中明暗交杂一\n\n[Chorus 5]\n笑生花暮色遮住你爬山的步\n伐走进窗口藏起的花花中的你低著头说\n\n[Chorus 6]\n我仍甘在于世界之大也沉醉于爱\n是情话不胜挣扎不做挣扎不惧\n\n[Chorus 7]\n笑话我终将青春还给了她也\n曾指尖弹出的盛夏心之所动就随风去\n啦以爱之名你还愿意吗\n\n[Outro 1]\n\n[Outro 2]\n\n[Outro 3]\n\n[Silence]",
  "audio_duration": 325.8681179138322,
  "trace_id": "06d1d8de449f241e47368d77092caab3",
  "structure_result": "{\"num_segments\":22,\"segments\":[{\"end\":13.441,\"label\":\"intro\",\"start\":0},{\"end\":25.921,\"label\":\"intro\",\"start\":13.441},{\"end\":49.922,\"label\":\"verse\",\"start\":25.921},{\"end\":64.083,\"label\":\"pre-chorus\",\"start\":49.922},{\"end\":76.323,\"label\":\"pre-chorus\",\"start\":64.083},{\"end\":90.124,\"label\":\"chorus\",\"start\":76.323},{\"end\":105.964,\"label\":\"chorus\",\"start\":90.124},{\"end\":118.685,\"label\":\"inst\",\"start\":105.964},{\"end\":142.686,\"label\":\"verse\",\"start\":118.685},{\"end\":156.726,\"label\":\"pre-chorus\",\"start\":142.686},{\"end\":169.087,\"label\":\"pre-chorus\",\"start\":156.726},{\"end\":193.808,\"label\":\"chorus\",\"start\":169.087},{\"end\":208.328,\"label\":\"inst\",\"start\":193.808},{\"end\":220.329,\"label\":\"inst\",\"start\":208.328},{\"end\":232.809,\"label\":\"chorus\",\"start\":220.329},{\"end\":245.89,\"label\":\"chorus\",\"start\":232.809},{\"end\":259.57,\"label\":\"chorus\",\"start\":245.89},{\"end\":277.091,\"label\":\"chorus\",\"start\":259.57},{\"end\":289.692,\"label\":\"outro\",\"start\":277.091},{\"end\":302.652,\"label\":\"outro\",\"start\":289.692},{\"end\":321.613,\"label\":\"outro\",\"start\":302.652},{\"end\":325.813,\"label\":\"silence\",\"start\":321.613}]}",
  "base_resp": {
    "status_code": 0,
    "status_msg": "success"
  }
}
```

主要返回字段说明：

- `cover_feature_id`：预处理后的音频特征唯一标识，**有效期 24 小时**。将此 ID 传入「music-cover 音乐生成」接口的 `cover_feature_id` 参数即可进行两步翻唱。相同音频内容会返回相同的 `cover_feature_id`（基于 MD5 去重）。
- `formatted_lyrics`：通过 ASR 从参考音频中提取并格式化的歌词，包含 `[Verse]`、`[Chorus]`、`[Bridge]` 等段落标签。您可以修改这些歌词后传入音乐生成接口。
- `structure_result`：JSON 字符串，包含歌曲结构分析结果，含段落类型（`intro`、`verse`、`chorus`、`bridge`、`outro`、`inst`、`silence`）及其起止时间戳（秒）。
- `audio_duration`：参考音频的时长（秒）。
- `trace_id`：请求追踪 ID。

<p align="center">
  <small>© 2026 DMXAPI music-cover 翻唱前处理</small>
</p>
