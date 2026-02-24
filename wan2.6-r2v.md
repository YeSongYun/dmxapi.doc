# wan2.6 参考生视频文档
万相-参考生视频模型支持多模态输入（文本/图像/视频），可将人或物体作为主角，生成单角色表演或多角色互动视频。模型还支持智能分镜，生成多镜头视频。

## 请求地址

```
https://www.dmxapi.cn/v1/responses
```

## 模型名称

- `wan2.6-r2v`

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
api_key = "sk-*******************************"
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
    "model": "wan2.6-r2v",
    "input": {

        # 【prompt】文本提示词。用来描述生成视频中期望包含的元素和视觉特点。
        #  支持中英文，每个汉字、字母、标点占一个字符，超过部分会自动截断。wan2.6-r2v：长度不超过1500个字符。
        #  角色引用说明：通过“character1、character2”这类标识引用参考角色，每个参考（视频或图像）仅包含单一角色。模型仅通过此方式识别参考中的角色。
        #  示例值：character1在沙发上开心地看电影。

        # 提示词公式：
        # 万相2.6支持参考输入视频中的主角生成视频，可参考主角的外观形象、动态特征和音色（如有声音）。主角类型不限，包括人物、卡通、宠物或道具等。
        # 提示词 = 主角 + 动作 + 台词 + 场景
        # 主角：通过“character1”等标识引用参考主角，最多可同时参考3个主角，每个主角可在提示词中多次引用，实现对其行为的精准控制。
        # 动作：描述主角或其他元素的运动状态，包括静止、表情情绪变化、肢体动作、外力动作和位移变化等。
        # 台词：主角的说话内容，支持单主角说话或多主角对话。
        # 场景：主角所在的环境，包括背景和前景，既可以是真实空间，也可以是虚构场景。
        # 示例：这是一个充满童趣的童话场景。character1在草地上蹦跳着玩耍，character2在旁边的一颗苹果树下弹奏钢琴，一颗苹果掉到了character2的头上，
        # character1开心地指着character2说：“你要变成科学家了！”。
        # (其中，character1的参考视频是一只兔子，character2的参考视频是一只狗，且每个参考视频仅包含单一角色。)
        "prompt": 'Character2 坐在靠窗的椅子上，手持 character3，在 character4 旁演奏一首舒缓的美国乡村民谣。Character1 对Character2开口说道："听起来不错"',

        # 【reference_urls】:上传的参考文件 URL 数组，支持传入视频和图像。用于提取角色形象与音色（如有），以生成符合参考特征的视频
        #    每个 URL 可指向 一张图像 或 一段视频：
        #     图像数量：0～5; 视频数量：0～3; 总数限制：图像 + 视频 ≤ 5。
        #     传入多个参考文件时，按照数组顺序定义角色的顺序。即第 1 个 URL 对应 character1，第 2 个对应 character2，以此类推。
        #     每个参考文件仅包含一个主体角色。例如 character1 为小女孩，character2 为闹钟。
        # 支持输入的格式：
        #     公网URL:
        #         支持 HTTP 或 HTTPS 协议。
        #         示例值：https://cdn.translate.alibaba.com/xxx.png。
        # 参考视频要求：
        #     格式：MP4、MOV; 
        #     时长：1s～30s。
        #     视频大小：不超过100MB。
        # 参考图像要求：
        #     格式：JPEG、JPG、PNG（不支持透明通道）、BMP、WEBP。
        #     分辨率：宽高均需在 [240, 5000]像素之间。
        #     图像大小：不超过10MB。
        #     示例值：["https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/xxx.mp4", "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/xxx.jpg"]。
        "reference_urls": [
            "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/hfugmr/wan-r2v-role1.mp4",
            "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/qigswt/wan-r2v-role2.mp4",
            "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/qpzxps/wan-r2v-object4.png",
            "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/wfjikw/wan-r2v-backgroud5.png"
        ],
        "negative_prompt": ""
    },
    "parameters": {
        # 【size】：指定生成的视频分辨率，格式为宽*高
        # wan2.6-r2v：默认值为 1920*1080（1080P）。可选分辨率：720P、1080P对应的所有分辨率。

        # 720P档位：可选的视频分辨率及其对应的视频宽高比为：
        #   1280*720：16:9。
        #   720*1280：9:16。
        #   960*960：1:1。
        #   1088*832：4:3。
        #   832*1088：3:4。
        
        # 1080P档位：可选的视频分辨率及其对应的视频宽高比为：
        #   1920*1080： 16:9。
        #   1080*1920： 9:16。
        #   1440*1440： 1:1。
        #   1632*1248： 4:3。
        #   1248*1632： 3:4。
        "size": "1280*720",

        # 【duration】:生成视频的时长，单位为秒。
        # wan2.6-r2v：取值为[2, 10]之间的整数。默认值为5。
        "duration": 10,

        # 【shot_type】：指定生成视频的镜头类型，即视频是由一个连续镜头还是多个切换镜头组成。
        # 参数优先级：shot_type > prompt。例如，若 shot_type设置为"single"，即使 prompt 中包含“生成多镜头视频”，模型仍会输出单镜头视频。
        # 可选值：
        #   single：默认值，单镜头视频。
        #   multi：多镜头视频。
        # 说明：当希望严格控制视频的叙事结构（如产品展示用单镜头、故事短片用多镜头），可通过此参数指定。
        "shot_type": "multi",

        "watermark": True, # 是否添加水印标识，水印位于视频右下角，文案固定为“AI生成”。
        "seed": 666 # 随机数种子，取值范围为[0, 2147483647]，未指定时，系统自动生成随机种子。由于模型生成具有概率性，即使用相同 seed，也不能保证每次生成结果完全一致。
    }
    
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
  "request_id": "70e69e91-8cf1-4056-843d-4530d726d1e1",
  "output": [
    {
      "type": "message",
      "content": [
        {
          "type": "output_text",
          "text": "{\"task_id\":\"6454ca2a-e80c-414f-a75e-877abcc443c1\",\"task_status\":\"RUNNING\"}"
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
api_key = "sk-****************************************"
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
    "input": "6454ca2a-e80c-414f-a75e-877abcc443c1",
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
  "request_id": "f76a22f1-cb53-4246-8dd3-e21de51d5307",
  "output": [
    {
      "type": "message",
      "content": [
        {
          "type": "output_text",
          "text": "{\"end_time\":\"2026-02-11 13:51:05.234\",\"orig_prompt\":\"Character2 坐在靠窗的椅子上，手持 character3，在 character4 旁演奏一首舒缓的美国乡村民谣。Character1 对Character2开口说道：\\\"听起来不错\\\"\",\"scheduled_time\":\"2026-02-11 13:48:14.735\",\"submit_time\":\"2026-02-11 13:48:14.703\",\"task_id\":\"6454ca2a-e80c-414f-a75e-877abcc443c1\",\"task_status\":\"SUCCEEDED\",\"video_url\":\"https://dashscope-result-sh.oss-accelerate.aliyuncs.com/1d/69/20260211/ca49cc2b/6454ca2a-e80c-414f-a75e-877abcc443c1.mp4?Expires=1770875456\\u0026OSSAccessKeyId=LTAI5tPxpiCM2hjmWrFXrym1\\u0026Signature=5o7T0DZ4xU8bGWwVO9XVxkYheB0%3D\"}"
        }
      ]
    }
  ],
  "usage": {
    "total_tokens": 75000,
    "input_tokens": 75000,
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
https://dashscope-result-sh.oss-accelerate.aliyuncs.com/1d/69/20260211/ca49cc2b/6454ca2a-e80c-414f-a75e-877abcc443c1.mp4?Expires=1770875456&OSSAccessKeyId=LTAI5tPxpiCM2hjmWrFXrym1&Signature=5o7T0DZ4xU8bGWwVO9XVxkYheB0%3D  
==================================================

```




<p align="center">
  <small>© 2026 DMXAPI wan2.6-t2v</small>
</p>
