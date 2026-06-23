# paiwo-v5.6-itv2 首尾帧生视频 API 文档
paiwo视频模型 可根据视频内容智能生成完整的声音体系，包括环境音效、背景音乐与角色台词，并支持指定音色，实现真正的“音画同步生成”。同时，它还能自动设计推拉、摇移、切换及景别变化等镜头语言，让生成的 10 秒视频具备节奏与呼吸感，呈现更完整的叙事段落，而非单调的动图。



::: warning
使用首尾帧生视频API前，请先完成图片上传API的调用，获取图片的img_id,
本模型请使用 `paiwo-picture` 上传。  
 [图片上传文档](https://doc.dmxapi.cn/paiwo_image_upload.html)
:::
## 接口地址

```
https://www.dmxapi.cn/v1/responses
```

## 模型名称
`paiwo-v5.6-itv2`



## 生成视频 示例代码
```python
import requests
import json

# ═══════════════════════════════════════════════════════════════
# 🔑 步骤1: 配置 API 连接信息
# ═══════════════════════════════════════════════════════════════

# 🌐 DMXAPI 服务端点地址
url = "https://www.dmxapi.cn/v1/responses"

# 🔐 DMXAPI 密钥 (请替换为您自己的密钥)
# 获取方式: 登录 DMXAPI 官网 -> 个人中心 -> API 密钥管理
api_key = "sk-***************************************"

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

    "input": "一只小奶猫在跟大人玩耍", # 输入的文字内容，2048 Characters 以内
    "model": "paiwo-v5.6-itv2",
    "duration": 5, # 视频时长：5s/8s/10s (1080p 无法使用 10s)
    "quality": "540p", # 视频质量："360p","540p","720p","1080p"
    "motion_mode": "normal",# 运动模式："normal","fast". "fast" 不支持 8s, "v5" 不支持此字段
    "seed": 937433858, #可传随机数 0 - 2147483647
    "first_frame_img": 177602101,# 上传图片后获取的img_id
    "last_frame_img": 177602101, #上传图片后获取的img_id
    "generate_audio_switch": True,#生成音频开关：只能v5.5与v5.6使用
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
  "ErrCode": 0,
  "ErrMsg": "success",
  "Resp": {
    "video_id": 385193132999855,
    "credits": 80
  },
  "usage": {
    "total_tokens": 240000,
    "input_tokens": 0,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 240000,
    "output_tokens_details": {
      "reasoning_tokens": 0
    }
  }
}
```


## 获取生成视频 示例代码

```python
import requests
import json

# ═══════════════════════════════════════════════════════════════
# 🔑 步骤1: 配置 API 连接信息
# ═══════════════════════════════════════════════════════════════

# 🌐 DMXAPI 服务端点地址
url = "https://www.dmxapi.cn/v1/responses"

# 🔐 DMXAPI 密钥 (请替换为您自己的密钥)
# 获取方式: 登录 DMXAPI 官网 -> 个人中心 -> API 密钥管理
api_key = "sk-***************************************"

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
    "model": "paiwo-get", 
    "input": "385193132999855",# 输入请求代码返回的视频ID
  
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
  "ErrCode": 0,
  "ErrMsg": "Success",
  "Resp": {
  "Resp": {
    "id": 385193132999855,
    "prompt": "一只小奶猫在跟大人玩耍",
    "negative_prompt": "",
    "id": 385193132999855,
    "prompt": "一只小奶猫在跟大人玩耍",
    "negative_prompt": "",
    "url": "https://media.pixverseai.cn/pixverse%2Fmp4%2Fmedia%2Fweb%2Fori%2F0161f18a-5410-4e7a-aef2-63429c7c74a1_seed937433858.mp4",
    "status": 5,
    "prompt": "一只小奶猫在跟大人玩耍",
    "negative_prompt": "",
    "url": "https://media.pixverseai.cn/pixverse%2Fmp4%2Fmedia%2Fweb%2Fori%2F0161f18a-5410-4e7a-aef2-63429c7c74a1_seed937433858.mp4",
    "status": 5,
    "url": "https://media.pixverseai.cn/pixverse%2Fmp4%2Fmedia%2Fweb%2Fori%2F0161f18a-5410-4e7a-aef2-63429c7c74a1_seed937433858.mp4",
    "status": 5,
    "status": 5,
    "seed": 937433858,
    "seed": 937433858,
    "create_time": "2026-02-04T11:35:38Z",
    "modify_time": "2026-02-04T11:35:39Z",
    "outputWidth": 0,
    "outputWidth": 0,
    "outputHeight": 0,
    "has_audio": false,
    "credits": 80
  }
}
```


<p align="center">
  <small>© 2026 DMXAPI paiwo-v5.6-itv2</small>
</p>