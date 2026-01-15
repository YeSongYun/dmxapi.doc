# suno音乐生成 API使用指南（异步）

Suno 专注于 AI 音频创作与语音合成，支持多语种生成与细腻的情感表达，可灵活应用于播客制作、品牌营销、语音娱乐等多种场景，提升内容生产效率与表现力，进一步拓展语音内容的呈现形态与创作边界。


## 🌍请求地址

```
https://www.dmxapi.cn/suno/submit/music
```
## 🚗查询结果地址

```
https://www.dmxapi.cn/suno/fetch/{task_id}
```

## ☀️模型列表

- `chirp-v5` 

## 🎩suno音乐生成-灵感模式 示例代码

```python
# ========================================
# Suno AI 音乐生成接口 - 灵感模式
# ========================================

import requests

# -------------------- 配置信息 --------------------
url = "https://www.dmxapi.cn/suno/submit/music"
key = "sk-************************************************"

# -------------------- 请求头 --------------------
headers = {
    "Accept": "application/json",
    "Authorization": f"Bearer {key}",
    "Content-Type": "application/json"
}

# -------------------- 请求参数 --------------------
data = {
    "gpt_description_prompt": "一首动听的情歌",  # [必需] 创作描述提示词，仅用于灵感模式
    "make_instrumental": False,                  # [可选] 是否生成纯音乐版本，True 表示生成纯音乐
    "mv": "chirp-v5",                            # [必需] 模型选择，可选 chirp-v5
    "notify_hook": ""                            # [可选] 任务完成后的回调通知地址
}

# -------------------- 发送请求 --------------------
response = requests.post(url, headers=headers, json=data)
print(response.json())

```

## ✈️返回示例

```json
{"code":"success","data":"9618ab08-a5db-4908-9850-01cfab68755b","message":""}
```

## 🚀查询生成结果

```python
# 导入所需模块
import http.client  # 用于发送 HTTP 请求
import json  # 用于处理 JSON 数据

# 创建 HTTPS 连接到 dmxapi 服务器
conn = http.client.HTTPSConnection("www.dmxapi.cn")

# 要查询的任务 ID
task_id = "9618ab08-a5db-4908-9850-01cfab68755b"

# 设置请求头
headers = {
   'Authorization': 'sk-******************************',  # API 认证令牌
   'Content-Type': 'application/json'  # 指定请求体格式为 JSON
}

# 发送 GET 请求查询任务结果
conn.request("GET", f"/suno/fetch/{task_id}", headers=headers)

# 获取响应
res = conn.getresponse()

# 读取响应数据
data = res.read()

# 解析 JSON 响应
result = json.loads(data.decode("utf-8"))

# 检查请求是否成功
if result.get("code") == "success":
    task_data = result.get("data", {})
    status = task_data.get("status", "UNKNOWN")
    progress = task_data.get("progress", "0%")

    print(f"任务状态: {status}")
    print(f"生成进度: {progress}")

    # 如果生成成功，显示音频 URL
    if status == "SUCCESS":
        print("\n" + "=" * 50)
        print("生成完成！音频下载地址：")
        print("=" * 50)
        songs = task_data.get("data", [])
        for i, song in enumerate(songs, 1):
            title = song.get("title", "未知")
            duration = song.get("duration", 0)
            audio_url = song.get("audio_url", "")
            image_url = song.get("image_url", "")

            minutes = int(duration // 60)
            seconds = int(duration % 60)

            print(f"\n【歌曲 {i}】{title}")
            print(f"  时长: {minutes}分{seconds}秒")
            print(f"  音频: {audio_url}")
            print(f"  封面: {image_url}")
    else:
        print(f"\n任务进行中，请稍后再查询...")
else:
    print(f"查询失败: {result.get('message', '未知错误')}")


```

## 🚢返回示例

```json
任务状态: SUCCESS
生成进度: 100%

==================================================
生成完成！音频下载地址：
==================================================

【歌曲 1】在你眼中慢慢沉没
  时长: 3分16秒
  音频: https://cdn1.suno.ai/caaffbcb-0ddf-4f35-9d15-43d0a68e2084.mp3
  封面: https://cdn2.suno.ai/image_caaffbcb-0ddf-4f35-9d15-43d0a68e2084.jpeg

【歌曲 2】在你眼中慢慢沉没
  时长: 3分37秒
  音频: https://cdn1.suno.ai/49c06f76-63b2-4f98-8eb8-d8a9dcd521ce.mp3
  封面: https://cdn2.suno.ai/image_49c06f76-63b2-4f98-8eb8-d8a9dcd521ce.jpeg
```

## 🌻suno音乐生成-自定义模式 示例代码


```python
# ========================================
# Suno AI 音乐生成接口 - 自定义模式
# ========================================

import requests

# -------------------- 配置信息 --------------------
url = "https://www.dmxapi.cn/suno/submit/music"
key = "sk-**************************************************"

# -------------------- 请求头 --------------------
headers = {
    "Accept": "application/json",
    "Authorization": f"Bearer {key}",
    "Content-Type": "application/json"
}

# -------------------- 请求参数 --------------------
data = {
    "prompt": """[Verse]
Move your paws
Left and right
Jump around
Feel the light
Whiskers twitch
Tails in the air
Dancing cats
Everywhere

[Chorus]
Cat dance
Oh
Let's go!
Swing your tails
Don't say no (don't say no!)
Purr and twirl
Like a show
Cat dance
Let's steal the glow

[Verse 2]
Tiptoe steps
Soft and sweet
Tiny paws
Unbeatable beat
Meow to the rhythm
Claws precise
Every move
Feline paradise

[Chorus]
Cat dance
Oh
Let's go!
Swing your tails
Don't say no (don't say no!)
Purr and twirl
Like a show
Cat dance
Let's steal the glow

[Bridge]
Ooh-ooh
Bounce and sway (ooh-ooh!)
Moonlit grooves
Night turns to day
Lean and stretch
Strike your pose
Every kitty steals the show

[Chorus]
Cat dance
Oh
Let's go!
Swing your tails
Don't say no (don't say no!)
Purr and twirl
Like a show
Cat dance
Let's steal the glow""",  # [必需] 自定义的完整歌词
    "mv": "chirp-v5",         # [必需] 模型版本号
    "title": "Cat Dance",     # [必需] 歌曲标题
    "tags": "romantic raga"   # [可选] 歌曲风格
}

# -------------------- 发送请求 --------------------
response = requests.post(url, headers=headers, json=data)
print(response.json())

```

## 🐯返回示例

```json
{"code":"success","data":"0957ffd1-c2aa-4264-b77b-b998ecaa22fb","message":""}

```

## 🐶查询生成结果

```python
# 导入所需模块
import http.client  # 用于发送 HTTP 请求
import json  # 用于处理 JSON 数据

# 创建 HTTPS 连接到 dmxapi 服务器
conn = http.client.HTTPSConnection("www.dmxapi.cn")

# 要查询的任务 ID
task_id = "0957ffd1-c2aa-4264-b77b-b998ecaa22fb"

# 设置请求头
headers = {
   'Authorization': 'sk-******************************',  # API 认证令牌
   'Content-Type': 'application/json'  # 指定请求体格式为 JSON
}

# 发送 GET 请求查询任务结果
conn.request("GET", f"/suno/fetch/{task_id}", headers=headers)

# 获取响应
res = conn.getresponse()

# 读取响应数据
data = res.read()

# 解析 JSON 响应
result = json.loads(data.decode("utf-8"))

# 检查请求是否成功
if result.get("code") == "success":
    task_data = result.get("data", {})
    status = task_data.get("status", "UNKNOWN")
    progress = task_data.get("progress", "0%")

    print(f"任务状态: {status}")
    print(f"生成进度: {progress}")

    # 如果生成成功，显示音频 URL
    if status == "SUCCESS":
        print("\n" + "=" * 50)
        print("生成完成！音频下载地址：")
        print("=" * 50)
        songs = task_data.get("data", [])
        for i, song in enumerate(songs, 1):
            title = song.get("title", "未知")
            duration = song.get("duration", 0)
            audio_url = song.get("audio_url", "")
            image_url = song.get("image_url", "")

            minutes = int(duration // 60)
            seconds = int(duration % 60)

            print(f"\n【歌曲 {i}】{title}")
            print(f"  时长: {minutes}分{seconds}秒")
            print(f"  音频: {audio_url}")
            print(f"  封面: {image_url}")
    else:
        print(f"\n任务进行中，请稍后再查询...")
else:
    print(f"查询失败: {result.get('message', '未知错误')}")


```

## ✨返回示例

```json
任务状态: SUCCESS
生成进度: 100%

==================================================
生成完成！音频下载地址：
==================================================

【歌曲 1】Cat Dance
  时长: 1分57秒
  音频: https://cdn1.suno.ai/7a4bfba4-bd1f-473b-abab-6bde6800d76d.mp3
  封面: https://cdn2.suno.ai/image_7a4bfba4-bd1f-473b-abab-6bde6800d76d.jpeg

【歌曲 2】Cat Dance
  时长: 2分12秒
  音频: https://cdn1.suno.ai/78cf3a81-965c-46d4-a369-e37c1e977d71.mp3
  封面: https://cdn2.suno.ai/image_78cf3a81-965c-46d4-a369-e37c1e977d71.jpeg
```



#### API 密钥安全

⚠️ **重要**：示例代码中的 API 密钥仅供演示，请务必：

- 使用您自己的 API 密钥
- 不要将密钥硬编码在代码中
- 建议通过环境变量管理密钥
- 不要将包含真实密钥的代码提交到公开仓库


---

<p align="center">
  <small>© 2025 DMXAPI suno音乐模型</small>
</p> 