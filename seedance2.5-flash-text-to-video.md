# doubao-seedance-2-5-flash 文生视频 API 使用文档

输入一段提示词即可生成视频。提示词可以描述主体、动作、镜头和声音，也可以启用联网搜索。Flash 支持 480p 和 720p、4–30 秒视频，以及六种固定宽高比或自适应画幅。

## 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 提交任务 | POST | `https://www.dmxapi.cn/api/v3/contents/generations/tasks` |
| 获取结果 | GET | `https://www.dmxapi.cn/api/v3/contents/generations/tasks/{task_id}` |

:::warning
请妥善保管 API Key。分享示例或向公开仓库提交代码前，请移除密钥。如果密钥泄露，请前往 DMXAPI 官网重新生成。
:::

:::warning 异步任务，请妥善保存任务 ID
提交成功后，请保存响应体中的 `id`。在本页的“获取生成视频”示例中填入该 ID，使用同一把 API Key 即可查询进度和获取视频。响应头中的请求 ID 用于排查单次 HTTP 请求。
:::

## 模型名称

- `doubao-seedance-2-5-flash-261115`

## 文生视频 示例代码

```python
import json

import requests

# ===============================================================
# 步骤1: 配置 API 连接信息
# ===============================================================

# 通过 POST 向 DMXAPI 网关提交文生视频任务。
url = "https://www.dmxapi.cn/api/v3/contents/generations/tasks"

# DMXAPI 密钥 (请替换为您自己的密钥)
# 获取方式: 登录 DMXAPI 官网 -> 个人中心 -> API 密钥管理
api_key = "sk-请替换为您的DMXAPI密钥"

# ===============================================================
# 步骤2: 配置请求头
# ===============================================================

headers = {
    "Content-Type": "application/json",      # 指定请求体为 JSON 格式
    "Authorization": f"Bearer {api_key}",    # Bearer token 认证方式
}

# ===============================================================
# 步骤3: 配置请求参数
# ===============================================================

payload = {
    # 【content】(object[], 必填) 输入内容列表。
    # 文生视频只放一条文本项，通过 text 描述主体、动作、场景或镜头。
    "content": [
        {
            # 【text】(string, 必填) 文生视频的提示词。
            # 可描述主体、动作、环境、镜头和声音。例如要生成人物对白，可把台词放入双引号。
            # 支持中文、英语、西班牙语、印度尼西亚语、葡萄牙语、日语、马来语、泰语、阿拉伯语、越南语和韩语。
            # 建议中文提示词不超过 500 字、英文不超过 1000 词，过长时模型可能忽略部分细节。
            "text": "小猫对着镜头打哈欠",

            # 【type】(string, 必填) 内容类型，此处固定为 text
            "type": "text",
        }
    ],

    # 【duration】(integer, 可选，默认 -1) 输出视频的目标时长，单位为秒。
    # 可填 4–30（含边界）的整数。省略或填 -1 时，由模型根据内容在该范围内选择整数秒。
    "duration": 5,

    # 【generate_audio】(boolean, 可选，默认 True) 是否生成与画面同步的声音。
    # True 时根据提示词生成双声道音轨，可包含人声、音效和背景音乐。对白可写在双引号中。
    # False 输出无声视频。
    "generate_audio": True,

    # 【model】(string, 必填) doubao-seedance-2-5-flash-261115 的完整模型 ID。
    "model": "doubao-seedance-2-5-flash-261115",

    # 【output_format】(string, 可选，默认 "mp4") 输出视频的容器格式。
    # mp4：通用格式，兼容性最好，采用标准色彩精度，可在网页、移动端、各类播放器及分发平台直接播放。​
    # mov：面向专业场景的高色彩精度格式，更好地保持画面色彩与亮度一致性、适用于调色、抠像、合成等对色彩还原要求高的专业后期加工。推荐在视频编辑、视频延长场景使用 mov 格式作为输入和输出。
    "output_format": "mp4",

    # 【ratio】(string, 可选，默认 "adaptive") 输出视频的宽高比（宽与高之比）。
    # 文生视频可填下表中的任一固定比例。省略此字段或填 "adaptive" 时，模型根据提示词在这六个比例中选择。
    # 例如，720p 搭配 "9:16" 得到 720×1280 的竖屏视频，搭配 "16:9" 得到 1280×720 的横屏视频。
    # ratio    480p       720p
    # 16:9     854×480    1280×720
    # 4:3      752×560    1112×834
    # 1:1      640×640    960×960
    # 3:4      560×752    834×1112
    # 9:16     480×854    720×1280
    # 21:9     992×432    1470×630
    "ratio": "9:16",

    # 【resolution】(string, 可选，默认 "720p") Flash 输出有 "480p" 和 "720p" 两档。
    "resolution": "720p",

    # 【return_last_frame】(boolean, 可选，默认 False) 是否另外返回成片的最后一帧。
    # True 时，成功查询的 content.last_frame_url 提供 JPEG 图片，与成片宽高相同，水印由 watermark 决定。
    # False 时只返回成片。
    "return_last_frame": False,

    # 【watermark】(boolean, 可选，默认 False) True 在成片右下角显示“AI 生成”水印，False 输出无水印画面。
    "watermark": False,

    # 【tools】(object[], 可选) 仅纯文本输入可启用联网搜索，每项的 type 填 web_search。
    # 模型按需搜索，可能增加耗时。查询结果的 usage.tool_usage.web_search 表示实际次数，0 表示没有搜索。
    # "tools": [{"type": "web_search"}],
}

# ===============================================================
# 步骤4: 发送请求并输出结果
# ===============================================================

# 发送请求并格式化输出 JSON，保留响应中的任务 id 供下方查询使用。
response = requests.post(url, headers=headers, json=payload, timeout=(10, 60))
if not response.ok:
    raise SystemExit(f"提交失败（HTTP {response.status_code}）：{response.text[:500]}")
print(json.dumps(response.json(), indent=2, ensure_ascii=False))
```

## 返回示例

```json
{
  "id": "task_J1LIPCgZzZlkaShClGqwFnuZGTqUjce4"
}
```

## 获取生成视频 示例代码


```python
import json
import time
from urllib.parse import quote

import requests

# ===============================================================
# 步骤1: 配置 API 连接信息
# ===============================================================

url = "https://www.dmxapi.cn/api/v3/contents/generations/tasks"
api_key = "sk-请替换为您的DMXAPI密钥"  # 使用提交任务时的 API Key

# ===============================================================
# 步骤2: 配置请求头
# ===============================================================

headers = {"Authorization": f"Bearer {api_key}"}

# ===============================================================
# 步骤3: 填写提交响应中的任务 ID
# ===============================================================

task_id = "task_J1LIPCgZzZlkaShClGqwFnuZGTqUjce4"  # 替换为刚才保存的 id
query_url = f"{url}/{quote(task_id, safe='')}"

# ===============================================================
# 步骤4: 查询任务状态并输出结果
# ===============================================================

# 网络中断、响应体不完整或网关暂时不可用时，使用同一任务 ID 最多再查两次。
consecutive_errors = 0
with requests.Session() as session:
    while True:
        delay = 15
        try:
            response = session.get(query_url, headers=headers, timeout=(10, 60))
            if response.status_code in (429, 500, 502, 503, 504):
                retry_after = response.headers.get("Retry-After", "")
                if retry_after.isdecimal():
                    delay = int(retry_after)
                response.raise_for_status()
            if not response.ok:
                raise SystemExit(f"查询失败（HTTP {response.status_code}）：{response.text[:500]}")
            result = response.json()
        except (requests.RequestException, ValueError) as error:
            consecutive_errors += 1
            if consecutive_errors >= 3:
                raise SystemExit(f"查询连续失败 3 次：{error}") from error
            time.sleep(delay)
            continue

        consecutive_errors = 0
        if result["id"] != task_id:
            raise ValueError("查询返回的 id 与提交时保存的任务 ID 不一致")
        if result["status"] not in ("queued", "running"):
            break
        time.sleep(15)

# 终态只输出一份完整 JSON。成功时读取 content.video_url，失败时查看 error。
print(json.dumps(result, indent=2, ensure_ascii=False))
if result["status"] != "succeeded":
    raise SystemExit(f"任务未成功，状态为 {result['status']}")
```

## 返回示例

```json
{
  "content": {
    "video_url": "https://ark-acg-cn-beijing.tos-cn-beijing.volces.com/doubao-seedance-2-5-flash/2112844032/Video/xs93j-64826142116202-tgc_3f9cb3332e51caffff00000000000000000000585239805597120/cgt-20261124162846-j39sx.mp4?X-Tos-Algorithm=TOS4-HMAC-SHA256&X-Tos-Credential=AKLTYWJkZTExNjA1ZDUyNDc3YzhjNTM5OGIyNjBhNDcyOTQ%2F20261124%2Fcn-beijing%2Ftos%2Frequest&X-Tos-Date=20261124T082930Z&X-Tos-Expires=86400&X-Tos-Max-Requests=100&X-Tos-Signature=945f33b7b4770787ce2f37195ddedb7de03f03eff646143dfd19d4a946a39391&X-Tos-SignedHeaders=host"
  },
  "created_at": 1795508932,
  "draft": false,
  "duration": 5,
  "execution_expires_after": 172800,
  "framespersecond": 24,
  "generate_audio": true,
  "id": "task_J1LIPCgZzZlkaShClGqwFnuZGTqUjce4",
  "model": "doubao-seedance-2-5-flash-261115",
  "output_format": "mp4",
  "priority": 0,
  "ratio": "9:16",
  "resolution": "720p",
  "seed": 97907,
  "service_tier": "default",
  "status": "succeeded",
  "updated_at": 1795508974,
  "usage": {
    "completion_tokens": 108900,
    "total_tokens": 108900
  }
}
```

<!--@include: /.vitepress/includes/seedance-2-5-flash-artifacts.md-->

<p align="center">
  <small>© 2026 DMXAPI doubao-seedance-2-5-flash 文生视频</small>
</p>
