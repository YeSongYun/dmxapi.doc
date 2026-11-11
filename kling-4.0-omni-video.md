# kling-4.0 全能参考生视频 API 使用文档

基于可灵 Kling 4.0 的全能参考生视频接口，通过 DMXAPI 网关以异步任务方式调用。提示词和参考素材都放在 `contents` 里，没有最外层 `prompt`。可引用图片主体、视频主体、参考图、关键帧、特征参考视频和待编辑视频。时长为 3～30 秒的整数，分辨率支持 720p / 1080p，画面比例支持 21:9、16:9、9:16、1:1、`adaptive`。

主体不能在本接口里现传图片或视频创建。正确顺序是：

1. 调用图片主体创建或视频主体创建，拿到 `data.task_id`。
2. 用主体任务查询轮询该 `task_id`，直到 `task_status` 为 `succeed`。
3. 读取 `data.task_result.elements[0].element_id`。
4. 把这个 `element_id` 写入下面 `type` 为 `element` 的素材。图片主体和视频主体的 ID 都这样用。

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

# DMXAPI 密钥 (请替换为您自己的密钥)
# 获取方式: 登录 DMXAPI 官网 -> 个人中心 -> API 密钥管理
api_key = "sk-***********************************************"

# ===============================================================
# 步骤2: 配置请求头
# ===============================================================

headers = {
    "Content-Type": "application/json",       # 指定请求体为 JSON 格式
    "Authorization": f"Bearer {api_key}",     # Bearer 认证
}

# ===============================================================
# 步骤3: 配置请求参数
# ===============================================================

payload = {
    # 【model】(string, 必填) 模型名称，固定为 kling-4.0
    "model": "kling-4.0",

    # 【contents】(array, 必填) 提示词和参考素材。没有最外层 prompt
    # 图片、视频、主体都要设置本请求内唯一的 id，提示词用 @id 说明各自用途
    # 主体数量最多 7 个，其中视频主体最多 3 个
    # 有视频主体时，视频主体与参考视频合计最多 5 个
    # 图片、视频、主体合计最多 15 个
    "contents": [
        {
            # 【type】(string, 必填) 提示词固定为 prompt
            "type": "prompt",
            # 【text】(string, 必填) 用 @id 引用下面的素材，id 必须和 contents 里的 id 一致
            # 纯英文最多 26000 个字符；不是纯英文时最多 11000 个字符
            # 中英混合须满足：英文字符数 / 26000 + 非英文字符数 / 11000 ≤ 1
            # 要写清每个素材保留什么、动作参考什么；不写用途时，模型会自行猜测
            "text": "@element_1 保持图片主体的外观，动作参考 @element_2，镜头保持电影感跟拍。",
        },
        {
            # 【type】(string, 必填) 主体固定为 element。图片主体和视频主体都用这一类型
            "type": "element",
            # 【element_id】(string, 必填) 主体任务查询返回的 element_id
            # 不是创建接口返回的 task_id，也不是下面的 id
            "element_id": "ke_be3ce0dbe4d4184a",
            # 【id】(string, 必填) 提示词里的引用名，本次请求内不能重复
            "id": "element_1",
        },
        {
            # 【type】(string, 必填) 视频主体同样是 element
            "type": "element",
            # 【element_id】(string, 必填) 视频主体查询返回的 element_id
            "element_id": "ke_f4e39ac61477c381",
            "id": "element_2",
        },
    ],

    # 【settings】(object, 可选) 视频生成设置
    "settings": {
        # 【duration】(integer, 可选) 3 到 30 的整数，单位秒
        # 传入后优先于提示词里写的时长
        # 不传且提示词也没有明确时长时：有 base_video 则四舍五入其时长，否则默认 10 秒
        # 计费时长以查询结果中的 usage.output_duration 为准
        "duration": 5,

        # 【resolution】(string, 可选) 仅支持 720p 或 1080p，默认 1080p
        "resolution": "1080p",

        # 【aspect_ratio】(string, 可选) 21:9、16:9、9:16、1:1、adaptive，默认 adaptive
        # 设为具体比例时，优先于提示词里写的比例
        # adaptive 或省略时，依次尝试：提示词中的明确比例、base_video、关键帧、feature_video；都没有则为 16:9
        "aspect_ratio": "16:9",
    },

    # 【options】(object, 可选) 任务选项
    "options": {
        # 【watermark_info.enabled】(boolean, 可选) 是否同时生成带水印的结果，默认 false
        "watermark_info": {"enabled": False},
    },
}

# ===============================================================
# 步骤4: 发送请求并输出结果
# ===============================================================

response = requests.post(url, headers=headers, json=payload)
print("status:", response.status_code)
result = response.json()
print(json.dumps(result, indent=2, ensure_ascii=False))

# 异步任务的网关 task_id 在 result["data"]["id"]，交给下面的视频任务查询
data = result.get("data") if isinstance(result, dict) else None
if isinstance(data, dict):
    print("task_id:", data.get("id"))

response.raise_for_status()
```
## 返回示例

```json
status: 200
{
  "code": 0,
  "data": {
    "create_time": 1794374616629,
    "id": "task_am0WuqIh7CWwhF9H0bTmV04IN5gMh1LD",
    "message": "",
    "status": "submitted",
    "update_time": 1794374616629
  },
  "message": "SUCCEED"
}
task_id: task_am0WuqIh7CWwhF9H0bTmV04IN5gMh1LD
```

## 获取生成视频 示例代码

```python
import requests
import json
import time

# ===============================================================
# 步骤1: 配置 API 连接信息
# ===============================================================

# DMXAPI Kling 4.0 视频任务查询接口
# 文生视频、图生视频、全能参考生视频共用此接口
url = "https://www.dmxapi.cn/tasks"

# DMXAPI 密钥 (请替换为您自己的密钥)
api_key = "sk-***********************************************"

# ===============================================================
# 步骤2: 配置请求头
# ===============================================================

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}",
}

# ===============================================================
# 步骤3: 配置请求参数
# ===============================================================

params = {
    # 【task_ids】(string, 必填) 填写视频创建接口返回的 data.id
    # 与 external_task_ids 二选一，不能同时传
    # 支持英文逗号分隔的批量查询；本示例每次只查一个任务
    "task_ids": "task_RZlT1eybOQHadzUuWjc2h16j4raRovqa",
}

# ===============================================================
# 步骤4: 轮询直到任务结束
# ===============================================================

# 查询接口会立刻返回当前状态。视频仍在生成时 status 为 submitted 或 processing。
# 每 25 秒查询一次，最多等待 600 秒；等待期间不打印，结束后只输出一次。
# 视频任务成功状态是 succeeded。失败时看该条记录的 message。
end_time = time.time() + 600
while time.time() < end_time:
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    result = response.json()
    data = result.get("data") if isinstance(result, dict) else None
    record = data[0] if isinstance(data, list) and data else data
    record = record if isinstance(record, dict) else {}
    status = str(record.get("status") or record.get("task_status") or "").lower()
    if status in {"succeeded", "succeed", "failed", "cancelled", "timed_out"}:
        break
    time.sleep(25)
else:
    raise TimeoutError("视频任务在 600 秒内没有结束")

print("status:", response.status_code)
print("request_id:", result.get("request_id", "未返回") if isinstance(result, dict) else "未返回")
print(json.dumps(result, indent=2, ensure_ascii=False))

# 成功时，视频地址在 data[0].outputs 里 type 为 video 的 url
# 地址带防盗链，生成结果保留 30 天，请及时转存
outputs = record.get("outputs") if isinstance(record.get("outputs"), list) else []
for item in outputs:
    if isinstance(item, dict) and item.get("type") == "video" and item.get("url"):
        print("video_url:", item.get("url"))
```

## 返回示例

```json
status: 200
{
  "code": 0,
  "data": [
    {
      "create_time": 1794374616629,
      "id": "task_am0WuqIh7CWwhF9H0bTmV04IN5gMh1LD",
      "message": "",
      "status": "succeeded",
      "update_time": 1794374730160,
      "video_id": "949342633099922731",
      "video_url": "https://v2-fdl.kechuangai.com/ksc2/ZVopZC-bkj5h8kYWAcSgG8rXfJsNJLdoTDopgFI9Sx4Ua6XxrquRfLOZ4i1Fvjx_1T-UR_8kgeCVEIjMuzwJtdvngHh-P8N_eQJ6K0NitJvgDcPdFufTpTjy0oI2yznPnm6SGxzisuOtF9UwJ8tZvA7gLL4Jkk51uYvjMcp0_Bol7daCXhZl9HpasDFcnvNRwKfyl9UCoXK_2juAJIJ-6w.mp4?cacheKey=ChtzZWN1cml0eS5rbGluZy5tZXRhX2VuY3J5cHQSsAFLOLubWnoHiNQJNJLCgT46u4EFLifG2K63wCc1Tqvo4eGMDw1pHGs4E9gbDFmoDQHYOT5-z4LFTFz_JHF2VOH8BjjjftsFQCcQfwBKhGEMMZF30Jpt4yRlJtNm17Gz6w1X2QX7IM2KJifyhZGbvWcHV1HLoxxa6tJ6emOsSRvdIZGfm2WIA1xokM367cX8IqBVxHLCNoDrEScUFHAZoL5z5vb272zBOPEWaDV-s6XTYhoSk8Q9wF5iLa3FHD-a4yQLv8RpIiDv42xR-T___jYGGtTF6X-95A4XGfVG0uhqiMHSPj3pVigFMAE&x-kcdn-pid=112757&pkey=AAVZNpEpNFY35O7YG8DIMi9cqAUAjjUElQ7EaPAjyduBmGpwJJ0bTAqwJoM0W2czzkFCY1S3EC-PPFVKZ7uJYXKh3KWrHu3ytlQPAidIdiWALU8yNR6mXE1P1BgpERtQL3w"
    }
  ],
  "message": ""
}
```
`outputs[].url` 是成片地址。计费使用的输出时长看 `usage.output_duration`，单位秒。生成结果保留 30 天。
<p align="center">
  <small>© 2026 DMXAPI Kling-4.0 全能参考生视频</small>
</p>
