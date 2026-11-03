---
description: MOSS API 接入指南，按语音转文字、音色生成、文字转语音三个分类介绍七种调用方式及 Python 示例。
---

# MOSS API 文档

MOSS API 通过 DMXAPI 提供语音转文字、音色创建与生成、文字转语音能力。本文档按使用场景分为三个部分，共七篇使用指南，每篇包含接口地址、模型说明、请求参数、可运行的 Python 示例及返回说明。

## 1. 语音转文字

将音频或视频转换为文字，根据输入来源选择对应的调用方式。

| 顺序 | 使用指南 | 适用场景 |
|---|---|---|
| 1 | [音频 URL 转文字](./moss-audio-url-to-text.md) | 已有服务端可直接访问的公网音频或视频链接 |
| 2 | [本地音频转文字](./moss-local-audio-to-text.md) | 直接提交本地文件并获得转写结果 |
| 3 | [上传文件并使用 file_id 转文字](./moss-file-id-to-text.md) | 先上传取得文件标识，再用 `file_id` 转写或重复引用文件 |

普通转写使用 `moss-transcribe-1.0`。启用说话人分离、非空热词列表，或选择 `diarized_json` 输出时，使用 `moss-transcribe-diarize-pro`。

## 2. 音色生成

先获得可复用的 `voice_id`，再用于单人朗读或多人对话。

| 顺序 | 使用指南 | 输入与结果 |
|---|---|---|
| 1 | [创建音色](./moss-create-voice.md) | 上传参考录音，创建可复用音色；无需填写 `model` |
| 2 | [音色生成](./moss-voice-generation.md) | 用文字描述声音并生成试听音频；设置 `create_voice=true` 时同时创建可复用音色 |

创建音色的参考录音支持 WAV、MP3、M4A、FLAC，大小不超过 10 MB、时长不超过 30 秒。通过文字描述生成音色时，使用 `moss-voice-generator-1.0`。

## 3. 文字转语音

使用已有的 `voice_id` 将文本合成为音频。示例以 JSON 获取音频 URL，并提供下载到本地的代码。

| 顺序 | 使用指南 | 适用场景与模型 |
|---|---|---|
| 1 | [单人朗读](./moss-single-speaker-tts.md) | 使用一个音色朗读文本；支持 `moss-tts-1.5-flash`、`moss-tts-1.0-pro` |
| 2 | [多人对话](./moss-multi-speaker-tts.md) | 为说话人分别配置音色，按文本分段顺序合成对话；使用 `moss-ttsd-1.0` |

单人 Flash 模型支持 `language` 参数和 `[pause 0.1s]` 至 `[pause 10.0s]` 的停顿标记。切换至 Pro 时，需删除该参数并移除停顿标记。

## 接入准备

1. 在 DMXAPI 获取 [API Key](/lingpai)，并将各篇示例中的 `YOUR_DMXAPI_API_KEY` 替换为实际密钥。
2. 安装 Python 依赖：

   ```bash
   python -m pip install requests
   ```

3. 按所选指南填写音频 URL、本地文件路径或音色标识，保存 Python 代码后运行。

各接口统一使用 `Authorization: Bearer <API_KEY>` 鉴权，均同步返回各自的结果，无需轮询任务状态。文件上传返回的是文件标识，需要继续调用转写接口才能获得文字。

## 接口速查

下表路径均以 `https://www.dmxapi.cn` 为前缀，请求方式均为 `POST`。

| 功能 | 接口路径 | 请求体 |
|---|---|---|
| 音频 URL / file_id 转文字 | `/moss-speech/v1/audio/transcriptions` | `application/json` |
| 本地音频转文字 | `/moss-speech/v1/audio/transcriptions` | `multipart/form-data` |
| 上传文件 | `/moss-speech/v1/files` | `multipart/form-data` |
| 创建音色 | `/moss-speech/v1/audio/voices` | `multipart/form-data` |
| 音色生成与试听 | `/moss-speech/v1/audio/voice/generations` | `application/json` |
| 单人朗读 | `/moss-speech/v1/audio/speech` | `application/json` |
| 多人对话 | `/moss-speakers/v1/audio/speech` | `application/json` |

::: tip 调用前核对
- 多人对话的路径前缀是 `moss-speakers`，其余接口使用 `moss-speech`。请复制各篇文档中的完整接口地址。
- `file_id` 标识转写文件，`voice_id` 标识合成音色；请分别填入对应的请求字段。
- 转写请求中的 `file`、`url`、`audio_url`、`file_id` 四种输入互斥，每次只提交一种。
- 上传文件时由 `requests` 自动生成 multipart 的 `Content-Type` 与 boundary。
:::

## 返回与计费说明

转写接口可返回 JSON 或纯文本；音色与语音合成示例会读取音色标识或音频地址。各篇文档中的返回示例均为字段示意，占位 ID 和音频链接不能直接用于请求。响应字段以接口实际返回为准，示例中的参数取值不代表服务端默认值。

各项功能的价格与计费规则以 [DMXAPI 模型价格](https://www.dmxapi.cn/rmb) 为准。示例中的 `timeout` / `request_timeout` 是客户端等待时间，不表示音频时长上限。

<p align="center">
  <small>© 2026 DMXAPI MOSS API</small>
</p>
