# paiwo-v5.6-itv 图生视频 API 文档
paiwo视频模型 可根据视频内容智能生成完整的声音体系，包括环境音效、背景音乐与角色台词，并支持指定音色，实现真正的“音画同步生成”。同时，它还能自动设计推拉、摇移、切换及景别变化等镜头语言，让生成的 10 秒视频具备节奏与呼吸感，呈现更完整的叙事段落，而非单调的动图。

::: warning
使用图生视频API前，请先完成图片上传API的调用，获取图片的img_id,
本模型请使用 `paiwo-picture` 上传。  
 [图片上传文档](https://doc.dmxapi.cn/paiwo_image_upload.html)
:::


## 接口地址

```
https://www.dmxapi.cn/v1/responses
```

## 模型名称
`paiwo-v5.6-itv`



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
api_key = "sk-**************************************"

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
    "model": "paiwo-v5.6-itv",
    "input": "在晴朗的海边沙滩上，一位约6–8岁的小女孩穿着浅色夏装和哥哥，赤脚在细沙上一边大笑一边奔跑，与2–3位同龄小伙伴追逐玩耍、击掌嬉戏；镜头后景一只金毛犬兴奋地摇尾巴追赶孩子们，时而加速、时而绕圈，沙粒被脚步扬起。天空湛蓝通透，阳光明亮但柔和，远处海面波光粼粼，浪花轻拍岸边；几只海鸥从画面上方掠过并盘旋，清晰可闻海鸥叫声与海浪声、孩子的笑声、犬吠声。画面风格为真实摄影、电影级质感，色彩自然清新，肤色真实，细节丰富（沙滩纹理、发丝随海风飘动、衣物褶皱、狗毛光泽）。",
    "duration": 10, # 视频持续时间(秒) ：5s/8s/10s (注意1080p 无法使用 10s)
    "img_id": 177602101, #上传图片后获取的img_id
    "motion_mode": "normal", #运动模式："normal","fast". "fast" 不支持 8s, "v5" 不支持此字段
    "negative_prompt": "不要出现车辆", #负面提示词，限制在2048 Characters 以内
    "quality": "540p", #视频质量："360p","540p","720p","1080p"
    "generate_audio_switch": True, #生成音频开关：只能v5.5与v5.6使用
    "seed": 0, # 可传随机数 0 - 2147483647

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
    "video_id": 385192665709752,
    "credits": 122
  },
  "usage": {
    "total_tokens": 366000,
    "input_tokens": 0,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 366000,
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
    "input": "385192665709752",# 输入请求代码返回的视频ID
  
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
    "id": 385192665709752,
    "prompt": "在晴朗的海边沙滩上，一位约6–8岁的小女孩穿着浅色夏装和哥哥，赤脚在细沙上一边大笑一边奔跑，与2–3位同龄小伙伴追逐玩耍、击掌嬉戏；镜头后景一只金毛犬兴奋地摇尾巴追赶孩子们，时而加速、时而绕圈，沙粒被脚步扬起。天空湛蓝通透，阳光明亮但柔和，远处海面波光粼粼，浪花轻拍岸边；几只海 鸥从画面上方掠过并盘旋，清晰可闻海鸥叫声与海浪声、孩子的笑声、犬吠声。画面风格为真实摄影、电影级质感，色彩自然清新，肤色真实，细节丰富（沙滩纹理、发丝随海风飘动、衣物褶皱、狗毛光泽）。",
    "negative_prompt": "不要出现车辆",
    "url": "https://media.pixverseai.cn/pixverse%2Fmp4%2Fmedia%2Fweb%2Fori%2Fdeca9db0-71bc-4106-b9f4-3580f54e39fb_seed866422.mp4",
    "status": 5,
    "seed": 866422,
    "create_time": "2026-02-04T11:31:50Z",
    "modify_time": "2026-02-04T11:31:56Z",
    "outputWidth": 0,
    "outputHeight": 0,
    "has_audio": false,
    "credits": 122
  }
}
```


<p align="center">
  <small>© 2026 DMXAPI paiwo-v5.6-itv</small>
</p>