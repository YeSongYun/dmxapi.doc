# kling-4.0 全能参考生视频 API 使用文档

基于可灵 Kling 4.0 的全能参考生视频接口，通过 DMXAPI 网关以异步任务方式调用。提示词、图片、视频、主体和音色都放在 `contents` 里，没有最外层 `prompt`，且必须有一项提示词。数量上限：图片最多 10 张，参考视频最多 5 个（其中待编辑视频最多 1 个），主体最多 7 个（其中视频主体最多 3 个；有视频主体时，视频主体与参考视频合计最多 5 个），音色最多 3 个，图片、视频、主体、音色合计最多 15 个。用 `@编号` 引用素材，并写明每个素材的用途。时长为 3～30 的整数秒，清晰度支持 720p、1080p，画面比例支持 21:9、16:9、9:16、1:1、4:3、3:4 和 adaptive（默认 adaptive）。主体编号来自主体任务查询或官方主体列表，音色编号来自音色查询或官方音色列表。

## 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 提交任务 | POST | `https://www.dmxapi.cn/omni-video/kling-4.0` |
| 获取结果 | GET | `https://www.dmxapi.cn/tasks` |


:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。如果怀疑密钥已泄露，请立即前往 DMXAPI 官网重新生成。
:::

## 模型名称

- `kling-4.0`

## 全能参考生视频示例代码

```python
import requests
import json

# ===============================================================
# 步骤1: 配置 API 连接信息
# ===============================================================

# DMXAPI Kling 4.0 全能参考生视频接口
url = "https://www.dmxapi.cn/omni-video/kling-4.0"

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
    #   官网的请求体里没有这一项，这是网关要求多带的
    "model": "kling-4.0",

    # 【contents】(array，必填) 素材合集：提示词、图片、视频、主体、音色。全能参考没有最外层的 prompt
    #   数量上限：
    #     图片（首帧、中间帧、尾帧、参考图）最多 10 张
    #     参考视频最多 5 个，其中待编辑视频 base_video 最多 1 个
    #     主体最多 7 个，其中视频主体最多 3 个；有视频主体时，视频主体 + 参考视频合计最多 5 个
    #     音色最多 3 个
    #     图片 + 视频 + 主体 + 音色 合计最多 15 个
    "contents": [
        {
            # 【type】(string，必填) 提示词固定为 prompt。contents 里必须有一项提示词
            "type": "prompt",
            # 【text】(string，必填) 提示词内容，可包含正向描述和负向描述
            #   长度限制：纯英文不超过 26000 个字符；纯非英文不超过 11000 个字符；
            #   中英文混合时，英文字符数 ÷ 26000 + 非英文字符数 ÷ 11000 ≤ 1
            #   用 @编号 引用下面的素材，并说明每个素材的用途，例如“保持 @image_1 中人物的面孔、发型与服装”
            #   只引用不说明用途时，模型会自己推断，结果可能和预期不一致
            #   建议按“素材用途 + 整体设定 + 分段事件 + 声音要求”来写；做视频编辑时写清楚要改什么、保留什么
            "text": "@element_1 对着镜头，用 @voice_1 的声音说：今天天气真好。",
        },
        {
            # 【type】(string，必填) 主体固定为 element
            "type": "element",
            # 【element_id】(string，必填) 主体编号。填主体任务查询返回的 element_id，或官方主体列表里的 element_id
            "element_id": "326873913635102",
            # 【id】(string，必填) 素材编号，提示词里用 @编号 引用。同一次请求内不能重复
            "id": "element_1",
        },
        {
            # 【type】(string，必填) 音色固定为 voice
            "type": "voice",
            # 【voice_id】(string，必填) 音色编号。填音色查询返回的 voice_id，或官方音色列表里的 voice_id
            "voice_id": "951071228826487641",
            # 【id】(string，必填) 素材编号，提示词里用 @编号 引用。同一次请求内不能重复
            "id": "voice_1",
        },

        # ---- 下面是其余几种素材。需要时去掉注释，并换成自己的地址 ----

        # 图片素材：first_frame 首帧、middle_frame 中间帧、last_frame 尾帧、refer_image 参考图
        #   【type】必填；【url】必填；【id】可选，但有多张 middle_frame 或多张 refer_image 时每张都必须填
        #   url 可以填图片网址，也可以填图片的 Base64（带不带 data:image/png;base64, 这样的开头都可以）
        #   格式 jpg / jpeg / png；单张不超过 30MB；宽和高都不小于 300px；宽高比在 2:5～5:2 之间
        #   同时有首帧、尾帧、参考图时，首帧放在图片里的第一张，尾帧放在最后一张
        # {"type": "first_frame", "url": "https://你的地址/first.png", "id": "image_1"},
        # {"type": "middle_frame", "url": "https://你的地址/middle.png", "id": "image_2"},
        # {"type": "last_frame", "url": "https://你的地址/last.png", "id": "image_3"},
        # {"type": "refer_image", "url": "https://你的地址/refer.png", "id": "image_4"},

        # 视频素材：feature_video 特征参考视频（参考它的动作、运镜、节奏等）、base_video 待编辑视频（在它上面修改）
        #   【type】必填；【url】必填，只能填视频网址，不支持 Base64；【id】可选
        #   格式 mp4 / mov；单个不超过 300MB
        #   单个视频时长和视频总时长都要在 3～30 秒之间（总时长包含参考视频、待编辑视频和视频主体）
        #   宽和高都在 700px～4553px 之间，像素总面积不超过 8294400，宽高比在 2:5～5:2 之间
        #   帧率 24～60 fps；生成的视频固定为 24 fps
        # {"type": "feature_video", "url": "https://你的地址/feature.mp4", "id": "video_1"},
        # {"type": "base_video", "url": "https://你的地址/base.mp4", "id": "video_2"},
    ],

    # 【settings】(object，可选) 输出配置
    "settings": {
        # 【audio】(string，可选) 声音处理方式，默认 native
        #   native：音画同出，生成和画面匹配的声音
        #   original：保留输入视频的原声。必须至少传一段 base_video 或 feature_video，并且不能同时引用音色
        #             有 base_video 时用它的原声；没有时用 contents 里第一段 feature_video 的原声
        "audio": "native",
        # 【resolution】(string，可选) 清晰度。可选 720p、1080p，默认 1080p
        "resolution": "720p",
        # 【aspect_ratio】(string，可选) 画面宽高比（宽:高）。可选 21:9、16:9、9:16、1:1、4:3、3:4、adaptive，默认 adaptive
        #   填具体比例时以这里为准，优先于提示词里写的比例
        #   不传或填 adaptive 时：先按提示词里写明的比例；提示词没写，就依次取 待编辑视频、关键帧图片（优先首帧）、
        #   参考视频 的比例，取到第一个为止（有多个参考视频时用 16:9）；都没有则用 16:9
        "aspect_ratio": "9:16",
        # 【duration】(int，可选) 目标时长，单位秒。3～30 的整数
        #   传了就以这里为准，优先于提示词里写的时长
        #   不传时：先按提示词里写明的时长；提示词没写，有 base_video 就取它的时长四舍五入，否则默认 10 秒
        #   最终采用的时长是输出计费时长；带参考视频或视频主体时，输入视频的时长也要计费
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
{
  "code": 0,
  "data": [
    {
      "create_time": 1795154984019,
      "id": "task_1G38ZFxRkTIFPdKTW5T8q6htCKhtXQVB",
      "status": "submitted",
      "update_time": 1795154984019
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
    "task_ids": "task_1G38ZFxRkTIFPdKTW5T8q6htCKhtXQVB",
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
      "create_time": 1795154985432,
      "duration": "3.041",
      "id": "task_1G38ZFxRkTIFPdKTW5T8q6htCKhtXQVB",
      "message": "",
      "status": "succeeded",
      "update_time": 1795155070450,
      "usage": {
        "cost": "6.102"
      },
      "video_id": "task_1G38ZFxRkTIFPdKTW5T8q6htCKhtXQVB",
      "video_url": "https://v4-fdl.kechuangai.com/ksc2/4ypnEvwbClF79mO3wXste2ZoirEol-fu1DaOIS8TieXe83-WM6Ds1kQF9y0JtgZAeWh6l-cfyKakH9W393D5aGeZsmkWy7v3Ev1wrnuoLdnYWJ1JUM_K8skEOv5tEDFdfzK3-MpymCFxBtjRCKAqIvjKS8f31k6mtUGrLaXEOS1Ybc6pygpjN38bRBZl28s1K7KW0kTEQrS7RzUqboiohQ.mp4?cacheKey=ChtzZWN1cml0eS5rbGluZy5tZXRhX2VuY3J5cHQSsAEMo_xyIyTO-ydZ7T9g8uBe7Gr6QnDWDGB5Y0gBsDSHzeYZlrP_xQaz5Fy7sl0hScYHhVsrIwMCY0VnZIm05_Or2d97gow6sHTFladsGdxgNjnCgMoxwG8hFvsmM0tgXAfJDl028Ts8bEDQmK-j2GL9acdQ5hO1UJav7lJf-DEIzF4qNssPMoyBfF5iLKg5xkHl4QOZqSDMtKDwSyT9mhosYGLRnr527aRlJr7RxC6olBoS49Uq9aOrf5yDPqUQkY5LD-iDIiDUYrg7Ut4yp2HDNRka9oT8Hsu1JfPUyldpcIfO8iPaoigFMAE&x-kcdn-pid=112757&pkey=AAVpySGzXvMOCp00NmFixl-hraPcQWiwAeX2fej38CzHsSJCNZv8xrFKAjKdxbI8s0P2fFwdRkoE-GW2yQPIGRezijmXSU_xmMgZjdiLOHT0Yj_trh5wEQfyBoN0wlAo0H4"
    }
  ],
  "message": "SUCCEEDED"
}
```

<p align="center">
  <small>© 2026 DMXAPI kling-4.0 全能参考生视频</small>
</p>
