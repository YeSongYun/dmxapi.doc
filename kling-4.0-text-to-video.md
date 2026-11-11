# kling-4.0 文生视频 API 使用文档

基于可灵 Kling 4.0 的文生视频接口，通过 DMXAPI 网关以异步任务方式调用。只提交文本提示词，不接收参考图、参考视频或主体；需要参考素材时请改用全能参考生视频。时长为 3～30 秒的整数，分辨率支持 720p / 1080p，画面比例支持 21:9、16:9、9:16、1:1。提交后立即返回网关任务 ID，视频在后台生成，再用该 ID 查询，成功后从 `outputs` 里取视频地址。
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

    # 【prompt】(string, 必填) 文生视频提示词，可同时写正向内容和不希望出现的内容
    # 纯英文最多 26000 个字符；不是纯英文时最多 11000 个字符
    # 中英混合须满足：英文字符数 / 26000 + 非英文字符数 / 11000 ≤ 1
    # 本接口只根据文字生成视频，不能在这里传参考图、参考视频或主体
    "prompt": "海边日落时，一名角色沿着沙滩缓慢走向镜头，电影感镜头运动。",

    # 【settings】(object, 可选) 视频生成设置
    "settings": {
        # 【duration】(integer, 可选) 目标时长，单位秒，只能是 3 到 30 的整数
        # 传入后优先于提示词里写的时长
        # 不传时，若提示词里有明确时长（如“生成 15 秒视频”）则采用该时长，否则默认 10 秒
        # 计费时长以查询结果中的 usage.output_duration 为准
        "duration": 3,

        # 【resolution】(string, 可选) 仅支持 720p 或 1080p，默认 1080p
        "resolution": "720p",

        # 【aspect_ratio】(string, 可选) 仅支持 21:9、16:9、9:16、1:1，默认 16:9
        "aspect_ratio": "16:9",
    },

    # 【options】(object, 可选) 任务选项
    "options": {
        # 【watermark_info.enabled】(boolean, 可选) 是否同时生成带水印的结果，默认 false
        # 不支持自定义水印图案
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
    "create_time": 1794371461594,
    "id": "task_mxRdA1aN3jHD1tjgWneI3rhywscaZFh6",
    "message": "",
    "status": "submitted",
    "update_time": 1794371461594
  },
  "message": "SUCCEED",
  "request_id": "745f860c-ebaf-425b-8b76-dcc38b0d4d2b"
}
task_id: task_mxRdA1aN3jHD1tjgWneI3rhywscaZFh6
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
      "create_time": 1794371461594,
      "id": "task_mxRdA1aN3jHD1tjgWneI3rhywscaZFh6",
      "message": "",
      "status": "succeeded",
      "update_time": 1794371563557,
      "video_id": "949336802920777097",
      "video_url": "https://v4-fdl.kechuangai.com/ksc2/ZGPEahtOZWyHOqwvyi9keDMJ96g-MXnSlEN9ed-x9OmUvigDiYMEg0g9Fhuh3y3WHfQzACX8_ElB8bmZFACmtmoQeAbCuswC7eyUhqRVLle7k0T25mmUhSXEtd_dKnMHkp8DhO8Gg5aBJ0hDyVHzQvxqNdgUFBJn8sJrguIs5iXmFDDYFJFpFdiLnLaobb9zQyxqBebAZTpV-h0Y2obCdQ.mp4?cacheKey=ChtzZWN1cml0eS5rbGluZy5tZXRhX2VuY3J5cHQSsAH6M1nNJA54Mb2NdNd8uACvGg9Oh-11EvaEOPRSWC9lkWlaZDWA-1g-xQttQncIRZ2yLVNWEoV2_nfuKnY8xW-slLeSCKtsbJZXdL07YjKnl_50jY2nK5BaJat0DxF4LNZE1c4Qcr74KL40AvBQveMMxtFvb1pg_MFgiYlF5AlKlEvB0kt2wb7a91vgrAuZ3_vaKw6Pg5HYR_noi9H7lFEvuu_wmbIjmQl0DMGEsoG84hoSK9DDR3Zts0AO39BBzVqoebvyIiBgx_tEvFOOugF09eVMSvuOk4y-j7BQtv7p4sD2FnnNLigFMAE&x-kcdn-pid=112757&pkey=AAX-sBfXFDG_OW6VdSmECXIfyqH3e7auz0--ocYbB690bFj4Hzfeyfex_seYFlde3xqw6ic8BpwU-nnInYJbGnTqEQWofSKX2UBdCWehHqp1s8o61jPo10nRzUF-X4U9ess"
    }
  ],
  "message": "",
  "request_id": "202611110433057709831968268d9d6j38xZuRl"
}
```
<p align="center">
  <small>© 2026 DMXAPI Kling-4.0 文生视频</small>
</p>
