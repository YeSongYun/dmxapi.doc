# kling-4.0 图生视频 API 使用文档

基于可灵 Kling 4.0 的图生视频接口，通过 DMXAPI 网关以异步任务方式调用。没有最外层 `prompt`，提示词和关键帧都写在 `contents` 里。支持首帧、中间帧、尾帧，最少 1 张、最多 10 张；同时传多种帧时按首帧、中间帧、尾帧排列，多张中间帧按出现顺序排列。图片为 jpg / jpeg / png，单张不超过 30MB，宽和高都不小于 300px，宽高比在 2:5～5:2 之间。本接口没有 `aspect_ratio`，传了会被拒绝。时长为 3～30 的整数秒，清晰度支持 720p、1080p。需要参考图、参考视频或主体时，请改用全能参考生视频。

## 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 提交任务 | POST | `https://www.dmxapi.cn/image-to-video/kling-4.0` |
| 获取结果 | GET | `https://www.dmxapi.cn/tasks` |


:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。如果怀疑密钥已泄露，请立即前往 DMXAPI 官网重新生成。
:::

## 模型名称

- `kling-4.0`

## 图生视频示例代码

```python
import requests
import json

# ===============================================================
# 步骤1: 配置 API 连接信息
# ===============================================================

# DMXAPI Kling 4.0 图生视频接口
url = "https://www.dmxapi.cn/image-to-video/kling-4.0"

# DMXAPI 密钥，请替换为您自己的密钥
# 获取方式: 登录 DMXAPI 官网 -> 个人中心 -> API 密钥管理
api_key = "sk-***********************************************"

# ===============================================================
# 步骤2: 配置请求头
# ===============================================================

headers = {
    "Content-Type": "application/json",  # 指定请求体为 JSON 格式
    "Authorization": f"Bearer {api_key}",  # Bearer 认证，填 DMXAPI 密钥
}

# ===============================================================
# 步骤3: 配置请求参数
# ===============================================================

payload = {
    # 【model】(string，必填) 网关用来识别模型，固定填 kling-4.0，要和请求地址最后的模型名一致
    "model": "kling-4.0",

    # 【contents】(array，必填) 素材合集：一项提示词 + 关键帧图片
    #   图生视频没有最外层的 prompt，提示词写在 contents 里
    #   关键帧图片要求（首帧、中间帧、尾帧相同）：
    #     格式 jpg / jpeg / png；单张不超过 30MB；宽和高都不小于 300px；宽高比在 2:5～5:2 之间
    #     图片最少 1 张，最多 10 张
    #     同时传多种帧时，按 首帧 → 中间帧 → 尾帧 的顺序排列；多张中间帧按在视频里出现的先后排列
    #   要用参考图、参考视频、主体等其他素材，请用全能参考
    "contents": [
        {
            # 【type】(string，必填) 提示词固定为 prompt
            "type": "prompt",
            # 【text】(string，必填) 提示词内容，可包含正向描述和负向描述
            #   长度限制：纯英文不超过 26000 个字符；纯非英文不超过 11000 个字符；
            #   中英文混合时，英文字符数 ÷ 26000 + 非英文字符数 ÷ 11000 ≤ 1
            #   用 @编号 引用下面的图片，说明每张图的作用，并按图片出现的先后顺序描述画面变化
            "text": "从 @image_1 的画面开始，图里的水果变身为机甲。",
        },
        {
            # 【type】(string，必填) 图片类型。first_frame 首帧、middle_frame 中间帧、last_frame 尾帧
            "type": "first_frame",
            # 【url】(string，必填) 图片内容。可以填图片网址，也可以填图片的 Base64
            #   Base64 带不带 data:image/png;base64, 这样的开头都可以（jpeg 同理）
            "url": "https://cdn.jsdelivr.net/gh/opencv/opencv/samples/data/fruits.jpg",
            # 【id】(string，可选) 素材编号，提示词里用 @编号 引用。同一次请求内不能重复
            "id": "image_1",
        },
        # 需要中间帧、尾帧时，去掉下面的注释，并换成自己的图片地址
        # {
        #     "type": "middle_frame",
        #     "url": "https://你的地址/middle.png",
        #     "id": "image_2",
        # },
        # {
        #     "type": "last_frame",
        #     "url": "https://你的地址/last.png",
        #     "id": "image_3",
        # },
    ],

    # 【settings】(object，可选) 输出配置。图生视频没有 aspect_ratio，传了会被拒绝
    "settings": {
        # 【resolution】(string，可选) 清晰度。可选 720p、1080p，默认 1080p
        "resolution": "720p",
        # 【duration】(int，可选) 目标时长，单位秒。3～30 的整数
        #   传了就以这里为准，优先于提示词里写的时长
        #   不传时，按提示词里写明的时长（例如“生成一段 15 秒的视频”）；提示词也没写，默认 10 秒
        #   最终采用的时长就是计费时长
        "duration": 3,
    },

    # 【options】(object，可选) 通用配置
    "options": {
        # 【watermark_info】(object，可选) 是否同时生成含水印的结果。暂不支持自定义水印
        "watermark_info": {
            # 【enabled】(boolean，可选) True 生成，False 不生成，默认 False
            "enabled": False,
        },
    },
}

# ===============================================================
# 步骤4: 发送请求并输出结果
# ===============================================================

response = requests.post(url, headers=headers, json=payload)
print("status:", response.status_code)
result = response.json()
print(json.dumps(result, indent=2, ensure_ascii=False))
response.raise_for_status()

# 返回里的 data.id 是视频任务号，data 是对象，不是数组，填到视频任务查询脚本的 task_ids 里查询结果。
```

## 返回示例

```json
status: 200
{
  "code": 0,
  "data": [
    {
      "create_time": 1795069304414,
      "id": "task_9oBcMsRUBvUttprg4527FZCwxQkqVosU",
      "status": "submitted",
      "update_time": 1795069304414
    }
  ],
  "message": "SUCCEED"
}
```

## 获取生成视频 示例代码

```python
import requests
import json
import time

# ===============================================================
# 步骤1: 配置 API 连接信息
# ===============================================================

# DMXAPI Kling 4.0 视频任务查询接口（文生、图生、全能参考共用）
url = "https://www.dmxapi.cn/tasks"

# DMXAPI 密钥，请替换为您自己的密钥。只能查到本账号提交的任务
# 获取方式: 登录 DMXAPI 官网 -> 个人中心 -> API 密钥管理
api_key = "sk-***********************************************"

# ===============================================================
# 步骤2: 配置请求头
# ===============================================================

headers = {
    "Content-Type": "application/json",  # 指定请求体为 JSON 格式
    "Authorization": f"Bearer {api_key}",  # Bearer 认证，填 DMXAPI 密钥
}

# ===============================================================
# 步骤3: 配置请求参数
# ===============================================================

params = {
    # 【task_ids】(string，必填) 视频任务号，填文生视频、图生视频或全能参考提交后返回的 data.id
    #   官网支持用逗号一次查多个；网关一次只能查一个任务号
    #   主体任务号、音色任务号不能在这里查
    "task_ids": "task_9oBcMsRUBvUttprg4527FZCwxQkqVosU",
}

# ===============================================================
# 步骤4: 发送请求并输出结果
# ===============================================================

# 网关会立刻返回任务当前的状态。脚本每 25 秒查一次，期间不打印，任务结束后只输出一次，最多等 600 秒。
end_time = time.time() + 600
while time.time() < end_time:
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    result = response.json()
    data = result.get("data") if isinstance(result, dict) else None
    record = data[0] if isinstance(data, list) and data else data
    record = record if isinstance(record, dict) else {}
    status = str(record.get("status") or "").lower()
    if status in {"succeeded", "failed", "cancelled", "timed_out"}:
        break
    time.sleep(25)
else:
    raise TimeoutError("视频任务在 600 秒内没有结束")

print("status:", response.status_code)
print(json.dumps(result, indent=2, ensure_ascii=False))

# 任务结束后返回的 data 是一个列表，data[0] 里：
#   id          视频任务号
#   status      任务状态：submitted 已提交、processing 处理中、succeeded 成功、failed 失败
#   message     任务失败时的原因
#   video_url       生成的视频地址。30 天后会被清理，请及时下载保存
#   watermark_url   带水印的视频地址。没有生成水印时不返回
#   duration        视频文件的实际时长，单位秒
#   video_id        视频编号
#   create_time / update_time   任务创建、更新时间，毫秒时间戳
#   usage.cost               上游实扣金额。任务刚提交时还没有；资源包扣减不算进这一项
```

## 返回示例

```json
status: 200
{
  "code": 0,
  "data": [
    {
      "create_time": 1795069306727,
      "duration": "3.041",
      "id": "task_9oBcMsRUBvUttprg4527FZCwxQkqVosU",
      "message": "",
      "status": "succeeded",
      "update_time": 1795069562866,
      "usage": {
        "cost": "3"
      },
      "video_id": "task_9oBcMsRUBvUttprg4527FZCwxQkqVosU",
      "video_url": "https://v4-fdl.kechuangai.com/ksc2/vD_1GCFTaSDNOBHQL3Sn3yzCpTy8h95H9w3rHZXR0DcQ92xyoDlwnkiu2M74tiNR54YPMieCKGnQjnpOqypfTnVxDQHrGMTBOBfTorGQ9TZofzgJrKgA0js4Tgf4pmj_PQaDKQ7StD9ENDTYEhguDkUOqcdgQQvj85QGNiJ5Ivvtb8YzpJg-QgowQUYusJdQreu2aj1D4WY1nEyCD8PFWQ.mp4?cacheKey=ChtzZWN1cml0eS5rbGluZy5tZXRhX2VuY3J5cHQSsAEQ-G6CrBVzEx76yp7AJQMeR_pJe-nqm78R8yA-wnhpX1OeRRS8-HjW2F6q1Oz0nbazxGy-sJs_QN0pn-pPKcu3mefXtLwSd0IrZaW7VI47Qik7A88nhw5Rj3xK22NVMWOgUIfAdYC9unOXAB2l_Rl-HMr9yRSu4e47R4z9KK0ZJZUPsuX1kUX6F7_qZyt0Ucy8nDzGCaBDlx5ao_h3jgJsbYcRzdxMKNcj0iaxhKVsuRoSbgFFnrpiqTZzapT733K7iU3CIiA3T3_GwO0DwqkZz7sBgfgFGdyD7gWW5birKE8DcwoGGygFMAE&x-kcdn-pid=112757&pkey=AAXInqQRUqRhwrFgrDij2rzoQdLXTiiQ2YJjsk27XaTpxmSuM6yN2_9eDG7hDklOYCz2cojoMsGJVCvkZMhsPQXuWZf6a7l3Su8dp1rjW0KQM7yvsWKf2X28YjzGfCJ09ZQ"
    }
  ],
  "message": "SUCCEEDED"
}
```

<p align="center">
  <small>© 2026 DMXAPI kling-4.0 图生视频</small>
</p>
