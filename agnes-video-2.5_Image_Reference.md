# agnes-video-2.5 图片参考 API 使用文档

基于 Agnes Video 2.5 的图片参考接口，通过 DMXAPI 网关以异步任务调用。`mode` 固定为 `reference`，把图片作为角色、风格或构图参考，生成结果可能重新构图，而不是把图片当成成片首帧。本示例必须填写 `images`，最多 8 张；在提示词中用 `<Picture 1>`、`<Picture 2>` 按数组顺序指代，编号从 1 开始。图片支持公网 URL 或 Base64（Base64 需要带前缀，如 `data:image/png;base64,iVBOR...`），单张小于 15MB，宽高各 256～5760 像素，单次总大小小于 50MB。图片前 5 张免费，第 6 张起 ¥0.03/张。分辨率支持 `720P`、`1080P`、`1K`、`2K`，画幅支持 `21:9`、`16:9`、`4:3`、`1:1`、`3:4`、`9:16`（默认 `16:9`）。

## 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 提交任务 | POST | `https://www.dmxapi.cn/v1/videos` |
| 获取结果 | GET | `https://www.dmxapi.cn/v1/videos/{task_id}` |

:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。如果怀疑密钥已泄露，请立即前往 DMXAPI 官网重新生成。
:::

## 模型名称

- `agnes-video-2.5`

## 输出视频尺寸

以下为各画幅比例的输出像素映射，实际宽高以 API 响应为准。`1K` 固定输出 `1024x1024`，未列入下表。

| `aspect_ratio` | 720P | 1080P | 2K（720P 的 2 倍） | 推荐场景 |
|------|------|------|------|------|
| `21:9` | `1470x630` | `2206x946` | `2940x1260` | 超宽银幕、电影感场景。 |
| `16:9` | `1280x720` | `1920x1080` | `2560x1440` | 横版视频、产品展示，默认比例。 |
| `4:3` | `1112x834` | `1664x1248` | `2224x1668` | 通用横版和传统画幅内容。 |
| `1:1` | `960x960` | `1440x1440` | `1920x1920` | 社交媒体信息流和方形内容。 |
| `3:4` | `834x1112` | `1248x1664` | `1668x2224` | 竖版展示和人物内容。 |
| `9:16` | `720x1280` | `1080x1920` | `1440x2560` | 移动端短视频和竖屏内容。 |

## 图片参考示例代码

```python
import json

import requests

# ===============================================================
# 步骤1：配置 API 连接信息
# ===============================================================

url = "https://www.dmxapi.cn/v1/videos"

# DMXAPI API Key（请替换为您自己的密钥；这里只放占位值）
api_key = "sk-请替换为您自己的密钥"


# ===============================================================
# 步骤2：配置请求头
# ===============================================================

headers = {
    "Content-Type": "application/json",  # JSON 请求体
    "Authorization": f"Bearer {api_key}",  # DMXAPI 网关鉴权
    "Accept": "application/json",  # 返回 JSON
}

# ===============================================================
# 步骤3：配置请求参数
# ===============================================================

payload = {
    # 【model】(string, 必填) 固定为 agnes-video-2.5
    "model": "agnes-video-2.5",

    # 【prompt】(string, 必填) 视频提示词；用 <Picture 1>、<Picture 2> 指代下面的参考图片
    # 长度没有具体限制，但超长 prompt 会拖慢生成，并影响视频生成效果
    "prompt": "<Picture 1> 的女孩开始跳舞。",

    # 【mode】(string, 必填) 图片参考固定为 reference
    "mode": "reference",

    # 【seconds】(string, 可选) 输出视频时长，"4" 到 "12"，不填默认 "5"
    "seconds": "5",

    # 【size】(string, 可选) 输出尺寸：720P、1080P、1K 或 2K
    "size": "720P",

    # 【aspect_ratio】(string, 可选) 画幅比例：21:9、16:9、4:3、1:1、3:4 或 9:16，不填默认 16:9
    "aspect_ratio": "16:9",

    # 【images】(array, 必填) 参考图片，公网 URL 或 Base64 均可，最多 8 张；前 5 张免费，超出每张加收。
    # Base64 需要带前缀，如 data:image/png;base64,iVBOR...
    "images": [
        "https://vigen-video.oss-cn-shanghai.aliyuncs.com/demo_image/image_demo_input.png",
    ],

    # 【seed】(integer, 可选) 随机种子；需要时取消注释
    # "seed": 12345,
}


def read_result(response):
    """优先解析 JSON，解析失败时保留原始文本。"""
    try:
        return response.json()
    except ValueError:
        return response.text


def print_result(result):
    """格式化输出 JSON 或纯文本结果。"""
    if isinstance(result, (dict, list)):
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(result)


def check_config():
    """提交前检查用户配置，避免把明显错误的参数发给网关。"""
    if not api_key.strip() or api_key.startswith("{{") or "请替换" in api_key:
        raise RuntimeError("请先在步骤1配置区填写真实的 api_key。")
    if payload.get("model") != "agnes-video-2.5":
        raise ValueError("payload['model'] 必须是 agnes-video-2.5。")
    prompt = payload.get("prompt")
    if not isinstance(prompt, str) or not prompt.strip():
        raise ValueError("payload['prompt'] 不能为空。")
    if payload.get("mode") not in {"text", "keyframe", "reference"}:
        raise ValueError("payload['mode'] 必须是 text、keyframe 或 reference。")
    seconds = payload.get("seconds")
    if seconds is not None and seconds not in {str(value) for value in range(4, 13)}:
        raise ValueError("payload['seconds'] 必须是 \"4\" 到 \"12\" 的字符串。")
    size = payload.get("size")
    if size is not None and size not in {"720P", "1080P", "1K", "2K"}:
        raise ValueError("payload['size'] 不是该模型支持的尺寸。")
    aspect_ratio = payload.get("aspect_ratio")
    if aspect_ratio is not None and aspect_ratio not in {"21:9", "16:9", "4:3", "1:1", "3:4", "9:16"}:
        raise ValueError("payload['aspect_ratio'] 不是支持的画幅比例。")
    if payload.get("mode") != "reference":
        raise ValueError("图片参考的 mode 必须是 reference。")
    images = payload.get("images") or []
    if not images:
        raise ValueError("图片参考必须填写 images。")
    if len(images) > 8:
        raise ValueError("参考图片最多 8 张。")


# ===============================================================
# 步骤4：发送请求并输出结果
# ===============================================================

def main():
    check_config()

    response = requests.post(
        url,
        headers=headers,
        json=payload,
    )

    header_request_id = response.headers.get("x-request-id", "")
    print("status_code:", response.status_code)
    if header_request_id:
        print("header_request_id:", header_request_id)

    content_type = response.headers.get("Content-Type", "")
    if "text/html" in content_type.lower():
        raise RuntimeError(
            f"网关返回了 HTML 页面而不是接口结果（HTTP {response.status_code}），"
            "请检查 url 是否正确、该站点是否已上传 agnes-video 插件。"
        )

    result = read_result(response)
    print_result(result)

    if not response.ok:
        request_id_detail = f"，request_id={header_request_id}" if header_request_id else ""
        raise RuntimeError(f"创建图片参考任务失败：HTTP {response.status_code}{request_id_detail}")
    if not isinstance(result, dict):
        raise RuntimeError("网关返回的不是 JSON 对象。")

    task_id = result.get("id")
    if not isinstance(task_id, str) or not task_id.startswith("task_") or not task_id[5:]:
        raise RuntimeError("创建响应缺少有效的任务 id（task_...）。")
    if result.get("status") == "failed":
        raise RuntimeError("创建任务失败：" + json.dumps(result.get("error"), ensure_ascii=False))
    if result.get("status") not in {"queued", "in_progress", "completed"}:
        raise RuntimeError(f"创建响应的 status 无法识别：{result.get('status')!r}")


if __name__ == "__main__":
    main()
```

## 返回示例

```json
status_code: 200
{
  "id": "task_y2uAt3I4npzjqbMoqTdgEfVebtMyMXsN",
  "object": "video",
  "model": "agnes-video-2.5",
  "status": "queued",
  "progress": 0,
  "created_at": 1794549599
}
```

## 查询视频 示例代码

```python
import json
import time
from urllib.parse import quote

import requests

# ===============================================================
# 步骤1：配置 API 连接信息
# ===============================================================

# 查询视频的网关地址。创建时走官方 POST /v1/videos，查询时走网关 GET /v1/videos/{id}
# 不要改成厂商的 /agnesapi，网关会自己向上游查询
url = "https://www.dmxapi.cn/v1/videos"

# DMXAPI API Key（请替换为您自己的密钥；这里只放占位值）
api_key = "sk-请替换为您自己的密钥"

# 轮询间隔，单位：秒。官方建议 1-2 秒，这里放宽到 5 秒
poll_interval_seconds = 5

# 最长等待时间，单位：秒
max_wait_seconds = 1800


# ===============================================================
# 步骤2：配置请求头
# ===============================================================

headers = {
    "Authorization": f"Bearer {api_key}",  # DMXAPI 网关鉴权
    "Accept": "application/json",  # 返回 JSON
}

# ===============================================================
# 步骤3：配置请求参数
# ===============================================================

params = {
    # 【task_id】(string, 必填) 创建接口返回的 id，形如 task_...
    "task_id": "task_y2uAt3I4npzjqbMoqTdgEfVebtMyMXsN",
}


def read_result(response):
    """优先解析 JSON，解析失败时保留原始文本。"""
    try:
        return response.json()
    except ValueError:
        return response.text


def print_result(result):
    """格式化输出 JSON 或纯文本结果。"""
    if isinstance(result, (dict, list)):
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(result)


def check_config():
    """查询前检查用户配置。"""
    if not api_key.strip() or api_key.startswith("{{") or "请替换" in api_key:
        raise RuntimeError("请先在步骤1配置区填写真实的 api_key。")
    task_id = params.get("task_id")
    if not isinstance(task_id, str) or not task_id.startswith("task_") or not task_id[5:]:
        raise ValueError("params['task_id'] 必须是创建接口返回的 task_...。")
    if "请替换" in task_id:
        raise ValueError("请先把 params['task_id'] 换成创建接口返回的 id。")
    if poll_interval_seconds <= 0 or max_wait_seconds <= 0:
        raise ValueError("poll_interval_seconds 和 max_wait_seconds 必须大于 0。")


def retry_after_seconds(response):
    """读取 Retry-After 秒数，读取失败时使用轮询间隔。"""
    try:
        return max(0.0, float(response.headers.get("Retry-After", "")))
    except ValueError:
        return float(poll_interval_seconds)


def error_message(result):
    """提取错误信息。"""
    error = result.get("error") if isinstance(result, dict) else None
    if isinstance(error, dict) and (error.get("code") or error.get("message")):
        return f"{error.get('code')}: {error.get('message')}"
    return json.dumps(result, ensure_ascii=False) if isinstance(result, dict) else str(result)


# ===============================================================
# 步骤4：发送请求并输出结果
# ===============================================================

def main():
    check_config()

    task_id = params["task_id"]
    query_url = f"{url}/{quote(task_id, safe='')}"
    deadline = time.monotonic() + max_wait_seconds
    transient_errors = 0

    while True:
        try:
            response = requests.get(query_url, headers=headers)
        except requests.RequestException as exc:
            transient_errors += 1
            if transient_errors >= 3:
                raise RuntimeError(f"查询连续网络失败：{exc}") from exc
            time.sleep(poll_interval_seconds)
            continue

        content_type = response.headers.get("Content-Type", "")
        if "text/html" in content_type.lower():
            raise RuntimeError(
                f"网关返回了 HTML 页面而不是接口结果（HTTP {response.status_code}），"
                "请检查 url 是否正确、该站点是否已上传 agnes-video 插件。"
            )

        result = read_result(response)

        if response.status_code in {429, 500, 502, 503, 504}:
            transient_errors += 1
            if transient_errors >= 3:
                print_result(result)
                raise RuntimeError(f"查询连续返回 HTTP {response.status_code}，已停止。")
            time.sleep(retry_after_seconds(response))
            continue

        if not response.ok:
            print_result(result)
            raise RuntimeError(f"查询失败：HTTP {response.status_code}")
        if not isinstance(result, dict):
            raise RuntimeError("网关返回的不是 JSON 对象。")
        transient_errors = 0

        if result.get("id") != task_id:
            raise RuntimeError(f"查询响应的 id 与请求不一致：{result.get('id')!r}")

        status = result.get("status")
        if status == "completed":
            print_result(result)
            return
        if status in {"queued", "in_progress"}:
            if time.monotonic() >= deadline:
                raise TimeoutError(f"任务轮询超时（{max_wait_seconds} 秒）。")
            time.sleep(poll_interval_seconds)
            continue
        if status in {"failed", "incomplete"}:
            print_result(result)
            raise RuntimeError(f"任务未成功（status={status}）：{error_message(result)}")
        raise RuntimeError(f"无法识别的 status：{status!r}")


if __name__ == "__main__":
    main()
```

## 返回示例

```json
{
  "completed_at": 1794549951,
  "created_at": 1794549599,
  "error": null,
  "expires_at": null,
  "id": "task_y2uAt3I4npzjqbMoqTdgEfVebtMyMXsN",
  "model": "agnes-video-2.5",
  "object": "video",
  "progress": 100,
  "quality": "standard",
  "seconds": "5",
  "size": "720P",
  "started_at": 1794549815,
  "status": "completed",
  "url": "https://cos-platform-outputs.agnes-ai.cn/videos/agnes-video-2.5/task_mVq3cIl196DDMMfshicURRn7YgK4cGFm.mp4",
  "usage": {
    "input_audio_seconds": 0,
    "input_image_count": 1,
    "input_seconds": 0
  }
}
```

<p align="center">
  <small>© 2026 DMXAPI agnes-video-2.5 图片参考</small>
</p>
