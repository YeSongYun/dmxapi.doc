# kling-4.0-flash 图生视频 API 使用文档

基于可灵 Kling 4.0 Flash 的图生视频接口，通过 DMXAPI 网关以异步任务方式调用。没有最外层 `prompt`。Flash 只支持首帧图生视频：`contents` 里只能有一项提示词和 1 张 `first_frame`，不支持中间帧和尾帧。图片为 jpg / jpeg / png，不超过 30MB，宽和高都不小于 300px，宽高比在 2:5～5:2 之间。本接口没有 `aspect_ratio`，传了会被拒绝。只支持 720p，时长为 3～20 的整数秒。需要参考图、参考视频或主体时，请改用全能参考生视频。

## 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 提交任务 | POST | `https://www.dmxapi.cn/image-to-video/kling-4.0-flash` |
| 获取结果 | GET | `https://www.dmxapi.cn/tasks` |


:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。如果怀疑密钥已泄露，请立即前往 DMXAPI 官网重新生成。
:::

## 模型名称

- `kling-4.0-flash`

## 图生视频示例代码

```python
import requests
import json

# ===============================================================
# 步骤1: 配置 API 连接信息
# ===============================================================

# DMXAPI Kling 4.0 Flash 图生视频接口
url = "https://www.dmxapi.cn/image-to-video/kling-4.0-flash"

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
    # 【model】(string，必填) 网关用来识别模型，固定填 kling-4.0-flash，要和请求地址最后的模型名一致
    #   官网的请求体里没有这一项，这是网关要求多带的
    "model": "kling-4.0-flash",

    # 【contents】(array，必填) 素材合集：一项提示词 + 一张首帧图
    #   图生视频没有最外层的 prompt，提示词写在 contents 里
    #   Flash 只支持首帧图生视频：只能传 1 张 first_frame，不支持中间帧和尾帧
    #   要用参考图、参考视频、主体等其他素材，请用全能参考
    "contents": [
        {
            # 【type】(string，必填) 提示词固定为 prompt
            "type": "prompt",
            # 【text】(string，必填) 提示词内容，可包含正向描述和负向描述
            #   长度限制：纯英文不超过 26000 个字符；纯非英文不超过 11000 个字符；
            #   中英文混合时，英文字符数 ÷ 26000 + 非英文字符数 ÷ 11000 ≤ 1
            #   描述首帧之后发生的内容：角色或物体接下来怎么动、镜头怎么运动、场景怎么变化
            "text": "她微笑着向镜头挥手。",
        },
        {
            # 【type】(string，必填) 首帧固定为 first_frame
            "type": "first_frame",
            # 【url】(string，必填) 图片内容。可以填图片网址，也可以填图片的 Base64
            #   Base64 带不带 data:image/png;base64, 这样的开头都可以（jpeg 同理）
            #   格式 jpg / jpeg / png；不超过 30MB；宽和高都不小于 300px；宽高比在 2:5～5:2 之间
            "url": "https://viapi-test.oss-cn-shanghai.aliyuncs.com/viapi-3.0domepic/facebody/CompareFace/CompareFace-right1.png",
        },
    ],

    # 【settings】(object，可选) 输出配置。图生视频没有 aspect_ratio，传了会被拒绝
    "settings": {
        # 【resolution】(string，可选) 清晰度。Flash 仅支持 720p，默认 720p
        "resolution": "720p",
        # 【duration】(int，可选) 目标时长，单位秒。Flash 为 3～20 的整数
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

# 本页返回示例的任务号在 data[0].id。若 data 为对象，则取 data.id。
data = result.get("data")
task = data[0] if isinstance(data, list) and data else data
if not isinstance(task, dict) or not task.get("id"):
    raise ValueError("提交响应中缺少视频任务号")
task_id = task["id"]
print("task_id:", task_id)
```

## 返回示例

```json
{
  "code": 0,
  "data": [
    {
      "create_time": 1781080778802,
      "id": "task_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
      "status": "submitted",
      "update_time": 1781080778802
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

# DMXAPI Kling 4.0 Flash 视频任务查询接口（文生、图生、全能参考共用）
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
    # 【task_ids】(string，必填) 视频任务号，填上方提交示例得到的 task_id
    #   官网支持用逗号一次查多个；网关一次只能查一个任务号
    #   主体任务号不能在这里查
    "task_ids": "task_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
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
{
  "code": 0,
  "message": "",
  "request_id": "example-request-id",
  "data": [
    {
      "id": "task_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
      "status": "succeeded",
      "message": "",
      "video_url": "https://example.com/result.mp4",
      "duration": "3.04",
      "video_id": "100000000000000001",
      "create_time": 1781080778802,
      "update_time": 1781080794151,
      "usage": {
        "cost": "0.00"
      }
    }
  ]
}
```

<p align="center">
  <small>© 2026 DMXAPI kling-4.0-flash 图生视频</small>
</p>
