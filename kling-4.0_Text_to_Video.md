# kling-4.0 文生视频 API 使用文档

基于可灵 Kling 4.0 的文生视频接口，通过 DMXAPI 网关以异步任务方式调用。只提交文本提示词，不接收参考图、参考视频或主体；要用图片、视频或主体做参考，请改用全能参考生视频。时长为 3～30 的整数秒，清晰度支持 720p、1080p（默认 1080p），画面宽高比支持 21:9、16:9、9:16、1:1、4:3、3:4（默认 16:9）。提交后，用返回的任务号调用下方查询接口。成功后视频地址在 `data[0].video_url`，请及时下载。

## 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 提交任务 | POST | `https://www.dmxapi.cn/text-to-video/kling-4.0` |
| 获取结果 | GET | `https://www.dmxapi.cn/tasks` |


:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。如果怀疑密钥已泄露，请立即前往 DMXAPI 官网重新生成。
:::

## 模型名称

- `kling-4.0`

## 文生视频示例代码

```python
import requests
import json

# ===============================================================
# 步骤1: 配置 API 连接信息
# ===============================================================

# DMXAPI Kling 4.0 文生视频接口
url = "https://www.dmxapi.cn/text-to-video/kling-4.0"

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

    # 【prompt】(string，必填) 文本提示词，可包含正向描述和负向描述
    #   可以描述角色、场景、视觉风格、光线、主体动作、镜头运动和事件的先后顺序
    #   长度限制：纯英文不超过 26000 个字符；纯非英文不超过 11000 个字符；
    #   中英文混合时，英文字符数 ÷ 26000 + 非英文字符数 ÷ 11000 ≤ 1
    #   本接口只用文字生成视频。要用图片、视频或主体做参考，请用全能参考
    "prompt": "海边日落时，一名角色沿着沙滩缓慢走向镜头，电影感镜头运动。哈苏镜头效果",

    # 【settings】(object，可选) 输出配置
    "settings": {
        # 【resolution】(string，可选) 清晰度。可选 720p、1080p，默认 1080p
        "resolution": "720p",
        # 【aspect_ratio】(string，可选) 画面宽高比（宽:高）。可选 21:9、16:9、9:16、1:1、4:3、3:4，默认 16:9
        "aspect_ratio": "16:9",
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
            "enabled": True,
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

HTTP 200

```json
{
  "code": 0,
  "data": [
    {
      "create_time": 1795068865683,
      "id": "task_2yOALvHwSlvLi90B9s69fA9fxIHA5gqA",
      "status": "submitted",
      "update_time": 1795068865683
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
    # 【task_ids】(string，必填) 视频任务号，填上方提交示例得到的 task_id
    #   官网支持用逗号一次查多个；网关一次只能查一个任务号
    #   主体任务号、音色任务号不能在这里查
    "task_ids": "task_2yOALvHwSlvLi90B9s69fA9fxIHA5gqA",
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
  "data": [
    {
      "create_time": 1795068866891,
      "duration": "3.041",
      "id": "task_2yOALvHwSlvLi90B9s69fA9fxIHA5gqA",
      "message": "",
      "status": "succeeded",
      "update_time": 1795069036890,
      "usage": {
        "cost": "3"
      },
      "video_id": "task_2yOALvHwSlvLi90B9s69fA9fxIHA5gqA",
      "video_url": "https://v4-fdl.kechuangai.com/ksc2/06FnZarsK5C2HKV6hsoPxHJnIsH-q55A8jID-4BK-cmTWnuTQQ6720FLXyDMfq4YNi6mdjeLdCexcnu4JcikERaMnYi2I0iCju7SxCFq03Z3gl_2kC8iAnZZ7yMRSgpbPOy20ab-Pw8ZROjTKdQUf4WuTnKj-Ge9sTHTnjXIiUCciAMURw_ob_mN95ScIjkWHcSXbvb_xvA-iZNLopI-uw.mp4?cacheKey=ChtzZWN1cml0eS5rbGluZy5tZXRhX2VuY3J5cHQSsAG8Dj9J8aWbIY7EZpme9_AJ9r5QsRCGu5T78WkQEvwYiB2gKZiGqDuxTY3CSSR1bEIPFV2z6FGA3Je2JLvgOuHMoF4Jzwb8u4MNnCR45hGveYvLZMWR_O_86yFu0Uw6xQV3c6gUXfZmmkmc4ss64rojYdmI7mNCWa4nvGaiq4qwqjfiuQYvOqP-wXLKSfOXzIdknBUYc9ykIMh5zDKta9FbekTPhEZIcdZaMh_HfDz07RoSj4dfrTYhUzYe6jlYP2ZR__D3IiA67y7KvC8VA1RQ2FLI8YzMeC33vC3UO-8DyiQ3ENWXJygFMAE&x-kcdn-pid=112757&pkey=AAWNuPhrYY1aEsXB3XcEmhHLk5Tx0mAnXbHythOrZCkjGlNm0z1Ntif5di-wZM8KVmZKRmDrSC7tKYjchI3UIAX_FSnvisALK7RXJnE1idWHqS7JdAaN-kxbIhoY_aLsR94",
      "watermark_url": "https://v4-fdl.kechuangai.com/ksc2/X7MbmXscFKZMTOaGm2wQVprtj2Hfzes8t9IsUj6KKCH_vWner1OBitjixIpPwTDFHzV6r3liQYWZBXC1YpqOmx3Oe5ml0IZP2aO9wK8FiLnsZ5TVL1czuWG1pKTpjc4-?cacheKey=ChtzZWN1cml0eS5rbGluZy5tZXRhX2VuY3J5cHQScPW8YVpx47mbwfZjBbFm8CS0sHkPWuYAP-dYxVXhe1-avTd8zsZbZ2rqUTh3uYJjmHZ42qgNThCSvInzXF4h9WqQVIZa_cTHuOE649n9oL7xGDSls3BbH1FThpc3vjay5eYBewpHdHIcihILYAAn-zEaEruG_UhL5UhSygvcpQENm2giSCIgscemxqufGjioZtqBJlJ-49tDVF3uc2iVC4nZjd0CAHAoBTAB&x-kcdn-pid=112757&pkey=AAU5GwyoAEmQhoBvESvVzBn9_VIImSfYcE0uU6hCY65BBSCwKNFE7lCmUerJDXUB75pBcAogabGnsyLq1KMpbx4z7upA1Tsw2Xaxeu-CssPgk29t-xvdAT2ShE16R_4lynM"
    }
  ],
  "message": "SUCCEEDED"
}
```

<p align="center">
  <small>© 2026 DMXAPI kling-4.0 文生视频</small>
</p>
