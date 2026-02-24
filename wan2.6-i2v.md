# wan2.6 首帧生视频文档
万相-图生视频模型根据首帧图像和文本提示词，生成一段流畅的视频。

## 请求地址

```
https://www.dmxapi.cn/v1/responses
```

## 模型名称

- `wan2.6-i2v`

## 提交视频任务

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
api_key = "sk-****************************"
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
    "model": "wan2.6-i2v",
    "input": {
        # 【prompt】:文本提示词。用来描述生成图像中期望包含的元素和视觉特点。支持中英文，每个汉字/字母占一个字符，超过部分会自动截断。
        # wan2.6-i2v长度不超过1500个字符
        "prompt": "一幅都市奇幻艺术的场景。一个充满动感的涂鸦艺术角色。一个由喷漆所画成的少年，正从一面混凝土墙上活过来。他一边用极快的语速演唱一首英文rap，一边摆着一个经典的、充满活力的说唱歌手姿势。场景设定在夜晚一个充满都市感的铁路桥下。灯光来自一盏孤零零的街灯，营造出电影般的氛围，充满高能量和惊人的细节。视频的音频部分完全由他的rap构成，没有其他对话或杂音。",

        # 【img_url】: 首帧图像的URL或 Base64 编码数据。
        # 图像限制：
        # 1. 图像格式：JPEG、JPG、PNG（不支持透明通道）、BMP、WEBP。
        # 2. 图像分辨率：图像的宽度和高度范围为[360, 2000]，单位为像素。
        # 3. 文件大小：不超过10MB

        # 支持输入的格式：
        #   公网URL:
        #     支持 HTTP 或 HTTPS 协议。
        #     示例值：https://cdn.translate.alibaba.com/r/wanx-demo-1.png。
        #   Base64 编码图像后的字符串：
        #     数据格式：data:{MIME_type};base64,{base64_data}。
        #     示例值：data:image/png;base64,GDU7MtCZzEbTbmRZ......。（编码字符串过长，仅展示片段）
        "img_url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/wpimhv/rap.png",

        #【audio_url】:音频文件的 URL，模型将使用该音频生成视频。
        # 支持输入的格式：
        #    公网URL:
        #      支持 HTTP 或 HTTPS 协议。
        #      示例值：https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/xxx.mp3。
        # 音频限制：
        #     格式：wav、mp3
        #     时长：3～30s
        #     文件大小：不超过15MB
        #     超限处理：若音频长度超过 duration 值（5秒或10秒），自动截取前5秒或10秒，其余部分丢弃。若音频长度不足
        #      视频时长，超出音频长度部分为无声视频。例如，音频为3秒，视频时长为5秒，输出视频前3秒有声，后2秒无声。
        #  示例值：https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/ozwpvi/rap.mp3
        "audio_url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/ozwpvi/rap.mp3",

        # 【negative_prompt】: 反向提示词，用来描述不希望在视频画面中看到的内容，可以对视频画面进行限制.支持中英文，长度不超过500个字符，超过部分会自动截断。
        # 示例值：低分辨率、错误、最差质量、低质量、残缺、多余的手指、比例不良等。
        "negative_prompt": "",

    },
    "parameters": {
        # 【resolution】: 指定生成的视频分辨率档位，用于调整视频的清晰度（总像素）。
        #   模型根据选择的分辨率档位，自动缩放至相近总像素,视频宽高比将尽量与输入图像 img_url 的宽高比保持一致
        #   wan2.6-i2v ：可选值：720P、1080P。默认值为1080P。
        #  Q.常见问题：如何生成特定宽高比（如3:4）的视频？
        #  A.回答：输出视频的宽高比由输入首帧图像（img_url）决定，但无法保证精确比例（如严格3:4），会存在一定偏差。
        #     为什么会有偏差：模型会以您输入图像的比例为基准，结合设置的分辨率档位（resolution）总像素，自动计算出最接近的合法分辨率。由于要求视频的长和宽必须是 16 的倍数，模型会对最终分辨率做微调，因此无法保证输出比例严格等于 3:4，但会非常接近。
        #     例如：输入图像750×1000（宽高比 3:4 = 0.75），并设置 resolution = "720P"（目标总像素约 92 万），实际输出816×1104（宽高比 ≈ 0.739，总像素约90万）。
        #     实践建议：
        #        1.输入控制：尽量使用与目标比例一致的图片作为首帧输入。
        #        2.后期处理：如果您对比例有严格要求，建议在视频生成后，使用编辑工具进行简单的裁剪或黑边填充。
        "resolution": "720P",

        # 【prompt_extend】：是否开启prompt智能改写。开启后使用大模型对输入prompt进行智能改写。对于较短的prompt生成效果提升明显，但会增加耗时。
        # true：默认值，开启智能改写；false：不开启智能改写。
        "prompt_extend": True,

        # 【duration】:生成视频的时长，单位为秒。
        #  wan2.6-i2v：取值为[2, 15]之间的整数。默认值为5。
        "duration": 10,

        # 【shot_type】: 指定生成视频的镜头类型，即视频是由一个连续镜头还是多个切换镜头组成。
        # 生效条件：仅当"prompt_extend": true 时生效。
        # 参数优先级：shot_type > prompt。例如，若 shot_type设置为"single"，即使 prompt 中包含“生成多镜头视频”，模型仍会输出单镜头视频。
        # single：默认值，输出单镜头视频
        # multi：输出多镜头视频。
        "shot_type": "multi",

        "watermark" : False, # 是否添加水印标识，水印位于视频右下角，文案固定为“AI生成”。默认值flase
        "seed" : 666 # 随机数种子，取值范围为[0, 2147483647]。未指定时，系统自动生成随机种子。请注意，由于模型生成具有概率性，即使使用相同 seed，也不能保证每次生成结果完全一致。
    },
   
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

---

## 返回示例

```json
{
  "request_id": "cfd47dd3-74b4-4489-aad4-43f7e6f816c3",
  "output": [
    {
      "type": "message",
      "content": [
        {
          "type": "output_text",
          "text": "{\"task_id\":\"b209fc05-8298-4139-b951-b48e90a4fd41\",\"task_status\":\"PENDING\"}"
        }
      ]
    }
  ],
  "usage": {
    "total_tokens": 60000,
    "input_tokens": 0,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 60000,
    "output_tokens_details": {
      "reasoning_tokens": 0
    }
  }
}
```
## 查询任务结果
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
api_key = "sk-******************************"
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
    "model": "wan2.6-get",
    "input": "b209fc05-8298-4139-b951-b48e90a4fd41",
}
# ═══════════════════════════════════════════════════════════════
# 📤 步骤4: 发送请求并输出结果
# ═══════════════════════════════════════════════════════════════

# 发送 POST 请求到 API 服务器
response = requests.post(url, headers=headers, json=payload)
result = response.json()

# 格式化输出 JSON 响应
# - indent=2: 缩进 2 空格，便于阅读
# - ensure_ascii=False: 正确显示中文字符
print(json.dumps(result, indent=2, ensure_ascii=False))
# ═══════════════════════════════════════════════════════════════
# 🎬 步骤5: 提取并输出可直接使用的视频链接
# ═══════════════════════════════════════════════════════════════

if "output" in result and len(result["output"]) > 0:
    content = result["output"][0].get("content", [])
    if content and "text" in content[0]:
        inner_data = json.loads(content[0]["text"])
        task_status = inner_data.get("task_status")
        if task_status == "SUCCEEDED":
            print("\n" + "="*50)
            print("✅ 视频生成成功！可直接复制的链接：")
            print(inner_data.get("video_url"))
            print("="*50)
        elif task_status == "PENDING" or task_status == "RUNNING":
            print(f"\n⏳ 任务状态: {task_status}，请稍后再次查询")
        elif task_status == "FAILED":
            print(f"\n❌ 任务失败: {inner_data.get('message', '未知错误')}")
        else:
            print(f"\n任务状态: {task_status}")
```

## 返回示例
```json
{
  "request_id": "af9d400c-0dd2-44ee-9191-3360ad29713b",
  "output": [
    {
      "type": "message",
      "content": [
        {
          "type": "output_text",
          "text": "{\"end_time\":\"2026-02-11 13:53:22.447\",\"orig_prompt\":\"一幅都市奇幻艺术的场景。一个充满动感的涂鸦艺术角色。一个由喷漆所画成的少年，正从一面混凝土墙上活过来。他一边用极快的语速演唱一首英文rap，一边摆着一个经典的、充满活力的说唱歌手姿势。场景设定在夜晚一个充满都市感的铁路桥下。灯光来自一盏孤零零的街灯，营造出电影般的氛围，充满高能量和惊人的细节。视频的音频部分完全由他的rap构成，没有其他对话或杂音。\",\"scheduled_time\":\"2026-02-11 13:52:04.346\",\"submit_time\":\"2026-02-11 13:51:54.593\",\"task_id\":\"b209fc05-8298-4139-b951-b48e90a4fd41\",\"task_status\":\"SUCCEEDED\",\"video_url\":\"https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/1d/3c/20260211/79e83f7c/36064048-b209fc05-8298-4139-b951-b48e90a4fd41.mp4?Expires=1770875591\\u0026OSSAccessKeyId=LTAI5tPxpiCM2hjmWrFXrym1\\u0026Signature=4IAz6Bhokdw%2BAg1RWKJA4CTOCRA%3D\"}"
        }
      ]
    }
  ],
  "usage": {
    "total_tokens": 60000,
    "input_tokens": 60000,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 0,
    "output_tokens_details": {
      "reasoning_tokens": 0
    }
  }
}
==================================================
✅ 视频生成成功！可直接复制的链接：
https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/1d/3c/20260211/79e83f7c/36064048-b209fc05-8298-4139-b951-b48e90a4fd41.mp4?Expires=1770875591&OSSAccessKeyId=LTAI5tPxpiCM2hjmWrFXrym1&Signature=4IAz6Bhokdw%2BAg1RWKJA4CTOCRA%3D
==================================================
```



<p align="center">
  <small>© 2026 DMXAPI wan2.6-i2v</small>
</p>
