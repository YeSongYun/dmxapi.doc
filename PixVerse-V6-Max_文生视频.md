# PixVerse-V6-Max 文生视频 API 使用文档

PixVerse V6 Max（`v6-max`）支持根据文字描述生成视频，可设置 1～15 秒时长、8 种画幅比例，最高输出 1080p 画质，并可开启音频生成。通过 DMXAPI 采用「提交任务 → 获取结果」两步异步模式：先提交生成任务获取 `response_id`，再通过 GET 轮询任务状态及视频结果。

## 模型名称

- `v6-max`

## 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 提交任务 | POST | `https://www.dmxapi.cn/v1/responses` |
| 获取结果 | GET | `https://www.dmxapi.cn/v1/responses/{response_id}` |

::: tip 异步调用说明
创建任务时设置 `background: true`，并保存响应中的顶层 `id`（格式为 `resp_...`）。查询时将它替换到 URL 的 `{response_id}` 位置，不保留花括号；GET 无需请求体，也无需指定查询模型。
:::

::: warning API Key 安全
请妥善保管您的 API Key。示例中的 `YOUR_DMXAPI_API_KEY` 为占位值，实际使用时建议从环境变量或密钥管理服务读取，勿将真实密钥提交到公开代码仓库。
:::

## 文生视频 示例代码


```python
import json

import requests

# ===============================================================
# 步骤1：配置 API 连接信息
# ===============================================================

url = "https://www.dmxapi.cn/v1/responses"
api_key = "YOUR_DMXAPI_API_KEY"  # 请替换为自己的 DMXAPI API Key
request_timeout = 60  # 单次请求超时时间，单位：秒

# ===============================================================
# 步骤2：配置请求头
# ===============================================================

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}",
    "Accept": "application/json",
}

# ===============================================================
# 步骤3：配置请求参数
# ===============================================================

payload = {
    # 【model】(string, 必填) 固定为 v6-max
    "model": "v6-max",

    # 【input】(string, 必填) 视频提示词，最多 5000 个字符
    "input": (
        "10秒电影级写实视频，未来厨房中，一个银白色机器人正在制作拉面。"
        "镜头从沸腾的汤锅特写开始，机器人捞起面条，热气缓缓升起。"
        "摄影机围绕料理台缓慢移动，机器人依次加入鸡蛋、葱花和海苔，"
        "最后把拉面推到镜头前。动作连贯，光影真实，保持物体数量和位置一致，"
        "无文字、无Logo。"
    ),

    # 【duration】(integer, 必填) 1～15 秒
    "duration": 10,

    # 【quality】(string, 必填) 360p / 540p / 720p / 1080p
    "quality": "1080p",

    # 【aspect_ratio】(string, 必填) 文生视频需指定画幅比例
    # 支持 16:9 / 9:16 / 4:3 / 3:4 / 1:1 / 2:3 / 3:2 / 21:9
    "aspect_ratio": "16:9",

    # 【generate_audio_switch】(boolean, 可选) 开启音频生成会增加费用
    "generate_audio_switch": True,

    # 【seed】(integer, 可选) 范围 0～2147483647；需要时取消注释
    # "seed": 12345,
}

# ===============================================================
# 步骤4：发送请求并输出结果
# ===============================================================


def main():
    if not api_key.strip() or api_key == "YOUR_DMXAPI_API_KEY":
        raise ValueError("请先配置自己的 DMXAPI API Key。")
    if payload.get("model") != "v6-max":
        raise ValueError("model 必须为 v6-max。")
    prompt = payload.get("input")
    if not isinstance(prompt, str) or not prompt.strip() or len(prompt) > 5000:
        raise ValueError("input 必须为非空字符串，且不超过 5000 个字符。")
    duration = payload.get("duration")
    if type(duration) is not int or not 1 <= duration <= 15:
        raise ValueError("duration 必须为 1～15 的整数。")
    if payload.get("quality") not in {"360p", "540p", "720p", "1080p"}:
        raise ValueError("quality 不在支持的清晰度范围内。")
    if payload.get("aspect_ratio") not in {
        "16:9", "9:16", "4:3", "3:4", "1:1", "2:3", "3:2", "21:9"
    }:
        raise ValueError("aspect_ratio 不在支持的画幅比例范围内。")

    # background 是 Responses 控制参数，固定为 True，启用异步任务。
    request_body = {**payload, "background": True}
    response = requests.post(
        url, headers=headers, json=request_body, timeout=request_timeout
    )

    print("status_code:", response.status_code)
    request_id = response.headers.get("x-request-id", "")
    if request_id:
        print("header_request_id:", request_id)

    if "text/html" in response.headers.get("Content-Type", "").lower():
        raise RuntimeError("网关返回了 HTML 页面，请检查接口地址及模型服务配置。")
    try:
        result = response.json()
    except ValueError as exc:
        print(response.text)
        raise RuntimeError("网关返回的不是有效 JSON。") from exc

    print(json.dumps(result, indent=2, ensure_ascii=False))
    if not response.ok:
        raise RuntimeError(f"创建文生视频任务失败：HTTP {response.status_code}")
    if not isinstance(result, dict):
        raise RuntimeError("创建响应必须为 JSON 对象。")

    response_id = result.get("id")
    if not isinstance(response_id, str) or not response_id.startswith("resp_") or not response_id[5:]:
        raise RuntimeError("创建响应缺少有效的网关 response_id（resp_...）。")
    if result.get("status") not in {"queued", "in_progress", "completed"}:
        raise RuntimeError(f"创建响应状态异常：{result.get('status')!r}")

    print("网关 response_id:", response_id)
    print("请将该值填入下方 GET 示例的 params['response_id']。")


if __name__ == "__main__":
    main()
```

## 返回示例

以下为创建响应的公共字段结构示意，实际响应可能包含其他字段。

```json
status_code: 200
{
  "background": true,
  "completed_at": null,
  "created_at": 1793963454,
  "error": null,
  "id": "resp_RrqatpEfV1pl02KEUVsLYyJR6pXGF71n",
  "incomplete_details": null,
  "metadata": {
    "retrieval_path": "/v1/responses/resp_RrqatpEfV1pl02KEUVsLYyJR6pXGF71n",
    "task_id": "task_RrqatpEfV1pl02KEUVsLYyJR6pXGF71n",
    "task_status": "queued"
  },
  "model": "v6-max",
  "object": "response",
  "output": [],
  "status": "queued",
  "usage": null
}
网关 response_id: resp_RrqatpEfV1pl02KEUVsLYyJR6pXGF71n
请将该值填入下方 GET 示例的 params['response_id']。
```

## 获取结果 示例代码

```python
import json
import time
from urllib.parse import quote

import requests

# ===============================================================
# 步骤1：配置 API 连接信息
# ===============================================================

url = "https://www.dmxapi.cn/v1/responses"
api_key = "YOUR_DMXAPI_API_KEY"  # 与提交任务时使用的 DMXAPI API Key 一致
poll_interval_seconds = 20
max_wait_seconds = 1800
request_timeout = 60

# ===============================================================
# 步骤2：配置请求头
# ===============================================================

headers = {
    "Authorization": f"Bearer {api_key}",
    "Accept": "application/json",
}

# ===============================================================
# 步骤3：配置路径参数
# ===============================================================

params = {
    # 填入创建任务返回的顶层 id；不要填写整数 video_id 或 x-request-id。
    "response_id": "resp_...",
}

# ===============================================================
# 步骤4：发送 GET 请求，轮询并输出结果
# ===============================================================


def print_result(result):
    if isinstance(result, (dict, list)):
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(result)


def main():
    if not api_key.strip() or api_key == "YOUR_DMXAPI_API_KEY":
        raise ValueError("请先配置自己的 DMXAPI API Key。")
    response_id = params.get("response_id")
    if (
        not isinstance(response_id, str)
        or not response_id.startswith("resp_")
        or not response_id[5:]
        or response_id == "resp_..."
    ):
        raise ValueError("response_id 必须替换为创建任务实际返回的 resp_...。")
    if min(poll_interval_seconds, max_wait_seconds, request_timeout) <= 0:
        raise ValueError("轮询间隔、等待上限和请求超时时间必须大于 0。")

    # params 是本地配置字典；response_id 拼入 URL 路径，不作为查询字符串发送。
    query_url = f"{url}/{quote(response_id, safe='')}"
    deadline = time.monotonic() + max_wait_seconds
    transient_errors = 0

    def wait_before_retry(seconds):
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise TimeoutError("轮询等待已达到上限，请保留 response_id 稍后查询。")
        time.sleep(min(seconds, remaining))

    while True:
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise TimeoutError("轮询等待已达到上限，请保留 response_id 稍后查询。")

        try:
            response = requests.get(
                query_url,
                headers=headers,
                timeout=min(request_timeout, remaining),
            )
        except requests.RequestException as exc:
            transient_errors += 1
            if transient_errors >= 3:
                raise RuntimeError(f"查询连续失败 3 次：{exc}") from exc
            print(f"查询网络异常（{transient_errors}/3），稍后重试：{exc}")
            wait_before_retry(poll_interval_seconds)
            continue

        print("status_code:", response.status_code)
        request_id = response.headers.get("x-request-id", "")
        if request_id:
            print("header_request_id:", request_id)
        try:
            result = response.json()
        except ValueError:
            result = response.text

        if response.status_code in {429, 500, 502, 503, 504}:
            transient_errors += 1
            if transient_errors >= 3:
                print_result(result)
                raise RuntimeError(f"查询连续失败 3 次，当前 HTTP {response.status_code}。")
            retry_after = response.headers.get("Retry-After", "")
            wait_seconds = int(retry_after) if retry_after.isdigit() else poll_interval_seconds
            print(f"查询暂时失败（{transient_errors}/3），{wait_seconds} 秒后重试。")
            wait_before_retry(wait_seconds)
            continue

        if "text/html" in response.headers.get("Content-Type", "").lower():
            raise RuntimeError("网关返回了 HTML 页面，请检查接口地址及模型服务配置。")
        if not response.ok:
            print_result(result)
            raise RuntimeError(f"查询失败：HTTP {response.status_code}")
        if not isinstance(result, dict):
            raise RuntimeError("查询响应必须为 JSON 对象。")
        if result.get("id") != response_id:
            raise RuntimeError("查询响应中的 id 与请求的 response_id 不一致。")
        transient_errors = 0

        status = result.get("status")
        if status == "completed":
            print("任务已完成，完整结果如下：")
            print_result(result)
            return
        if status in {"queued", "in_progress"}:
            print(f"任务处理中（status={status}），{poll_interval_seconds} 秒后继续查询。")
            wait_before_retry(poll_interval_seconds)
            continue
        if status in {"failed", "incomplete"}:
            print_result(result)
            raise RuntimeError(f"任务未成功（status={status}），请查看返回的错误信息。")

        print_result(result)
        raise RuntimeError(f"无法识别的任务状态：{status!r}")


if __name__ == "__main__":
    main()
```

## 返回示例

```json 
status_code: 200
任务处理中（status=in_progress），20 秒后继续查询。
status_code: 200
任务处理中（status=in_progress），20 秒后继续查询。
status_code: 200
任务处理中（status=in_progress），20 秒后继续查询。
status_code: 200
任务已完成，完整结果如下：
{
  "created_at": 1793963454,
  "error": null,
  "id": "resp_RrqatpEfV1pl02KEUVsLYyJR6pXGF71n",
  "incomplete_details": null,
  "instructions": null,
  "metadata": {
    "retrieval_path": "/v1/responses/resp_RrqatpEfV1pl02KEUVsLYyJR6pXGF71n",
    "task_id": "task_RrqatpEfV1pl02KEUVsLYyJR6pXGF71n",
    "task_status": "completed",
    "vendor": "pixverse-v6-max"
  },
  "model": "v6-max",
  "object": "response",
  "output": [
    {
      "content": [
        {
          "annotations": [],
          "id": "content_task_RrqatpEfV1pl02KEUVsLYyJR6pXGF71n_0_0",
          "logprobs": [],
          "text": "<video controls src=\"https://media.pixverseai.cn/pixverse%2Fmp4%2Fmedia%2Fweb%2Fori%2F1789899a-0f37-4143-ba13-c637f9f7f27f_seed2098526161.mp4\"></video>",
          "type": "output_text"
        }
      ],
      "id": "item_task_RrqatpEfV1pl02KEUVsLYyJR6pXGF71n_0",
      "role": "assistant",
      "status": "completed",
      "type": "message"
    }
  ],
  "parallel_tool_calls": true,
  "status": "completed",
  "temperature": 1,
  "tool_choice": "auto",
  "tools": [],
  "top_p": 1,
  "usage": {
    "input_tokens": 0,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 0,
    "output_tokens_details": {
      "reasoning_tokens": 0
    },
    "total_tokens": 0,
    "cost": "¥8.21"
  }
}
```


<p align="center">
  <small>© 2026 DMXAPI PixVerse-V6-Max 文生视频</small>
</p>
