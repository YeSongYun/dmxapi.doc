# yinchao-v4.5 生成纯音乐 API 使用文档

用 `yinchao-v4.5` 按提示词生成一首无人声的器乐作品。可以指定主奏乐器、节奏和编曲变化。提交后会得到任务 ID，生成完成后可下载 MP3。

## 接口地址

| 接口 | 请求方式 | URL |
| --- | --- | --- |
| 生成纯音乐 | POST | `https://www.dmxapi.cn/yinchao/api/v1/song/instrumental` |
| 查询生成结果 | GET | `https://www.dmxapi.cn/yinchao/api/v1/task/query` |

## 模型名称

`yinchao-v4.5`

## 生成纯音乐示例代码

```python
import requests
import json

# ===============================================================
# 步骤1: 配置 API 连接信息
# ===============================================================

url = "https://www.dmxapi.cn/yinchao/api/v1/song/instrumental"
api_key = "sk-******************************************"  # 填写自己的 DMXAPI 密钥

# ===============================================================
# 步骤2: 配置请求头
# ===============================================================

headers = {
    "Content-Type": "application/json",
    "Authorization": f"{api_key}",
}

# ===============================================================
# 步骤3: 配置请求参数
# ===============================================================

payload = {
    # 【prompt】(string, 必填) 描述乐器、曲风、速度和使用场景，1 至 3000 个字符。
    "prompt": "雨夜咖啡馆里的慢速爵士，钢琴演奏主旋律，低音提琴和刷鼓伴奏，全曲无人声。",

    # 【model】(string, 必填) 网关模型名称。
    "model": "yinchao-v4.5",

    # 【callback】(string, 可选) 可接收进度通知的公网 HTTP(S) 地址。
    # "callback": "https://your-domain.example/yinchao/order-001",
}

# ===============================================================
# 步骤4: 发送请求并输出结果
# ===============================================================

def main():
    response = requests.post(url, headers=headers, json=payload)
    if not response.ok:
        print(response.text)
        response.raise_for_status()
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
```

## 提交返回示例

下面是一次真实请求的原始返回。顶层 `id` 是网关任务 ID，`choices[].id` 是单首歌曲的 ID。刚提交时 `status` 为 `NOT_START`，`choices` 也可能为空。

```json
{
  "choices": [
    {
      "audio_url": "",
      "create_at": 1795746231,
      "duration": 0,
      "error": "",
      "error_code": 0,
      "finish_at": 0,
      "id": "f3a3eb5a-7be8-4793-be1a-08f6298867e6",
      "lyric": "",
      "pipe_url": "",
      "size": 0,
      "status": "running",
      "title": ""
    }
  ],
  "create_at": 1795746231,
  "id": "task_hhDmlZRNA2jMGf3x0KzEFRYTtn84DbFV",
  "status": "NOT_START",
  "task_type": "instrumental"
}
```

## 获取生成音乐示例代码


```python
import requests
import json
import time
from pathlib import Path

# ===============================================================
# 步骤1: 配置 API 连接信息
# ===============================================================

url = "https://www.dmxapi.cn/yinchao/api/v1/task/query"
api_key = "sk-******************************************"  # 填写自己的 DMXAPI 密钥
output_dir = Path("输出")  # 文件保存在 输出/<网关任务ID>/ 下
poll_interval = 3  # 两次查询之间的间隔，单位为秒
wait_timeout = 600  # 最长轮询时间，单位为秒

# ===============================================================
# 步骤2: 配置请求头
# ===============================================================

headers = {"Authorization": f"{api_key}"}

# ===============================================================
# 步骤3: 配置请求参数
# ===============================================================

params = {
    # 【task_id】(string, 必填) 上方纯音乐生成提交响应顶层的 id。
    "task_id": "task_替换为生成任务ID",
}

# ===============================================================
# 步骤4: 发送请求并输出结果
# ===============================================================

def main():
    deadline = time.monotonic() + wait_timeout
    while time.monotonic() < deadline:
        try:
            response = requests.get(url, headers=headers, params=params)
        except requests.RequestException:
            # 网络抖动（如连接被重置）时稍后重试，不打断轮询
            time.sleep(poll_interval)
            continue
        if response.status_code in (429, 502, 503, 504):
            time.sleep(poll_interval)
            continue
        if not response.ok:
            print(response.text)
            response.raise_for_status()
        result = response.json()
        if result["status"] in ("SUCCESS", "FAILURE"):
            break
        time.sleep(poll_interval)
    else:
        raise TimeoutError(f"等待超时，可用原任务 ID {params['task_id']} 再次查询。")

    formatted = json.dumps(result, indent=2, ensure_ascii=False)
    print(formatted)
    task_dir = output_dir / params["task_id"]
    task_dir.mkdir(parents=True, exist_ok=True)
    (task_dir / "result.json").write_text(formatted, encoding="utf-8")
    if result["status"] == "FAILURE":
        raise RuntimeError(result.get("fail_reason") or "生成失败，详情见 result.json。")

    for song in result["choices"]:
        if song["status"] != "done":
            continue
        # audio_url 已带下载签名，直接 GET 即可。仅查询接口需要 DMXAPI 密钥。
        audio = requests.get(song["audio_url"])
        audio.raise_for_status()
        mime_type = audio.headers.get("Content-Type", "").split(";", 1)[0].strip().lower()
        if not (mime_type.startswith("audio/") or mime_type == "application/octet-stream") or not audio.content:
            raise ValueError("下载地址未返回音频，请检查本次查询结果。")
        output_path = task_dir / f"{song['id']}.mp3"
        output_path.write_bytes(audio.content)


if __name__ == "__main__":
    main()
```

## 查询返回示例

下面是任务完成后同一次真实请求的原始返回（仅把 `access` 签名替换成了 `EXAMPLE_SIGNATURE`）。下载 `audio_url` 时不要再带 Authorization。

```json
{
  "choices": [
    {
      "audio_url": "https://www.dmxapi.cn/v1/tasks/task_hhDmlZRNA2jMGf3x0KzEFRYTtn84DbFV/artifacts/audio-f3a3eb5a-7be8-4793-be1a-08f6298867e6/content?access=EXAMPLE_SIGNATURE",
      "create_at": 1795746231,
      "duration": 173.14,
      "error": "",
      "error_code": 0,
      "finish_at": 1795746339,
      "id": "f3a3eb5a-7be8-4793-be1a-08f6298867e6",
      "lyric": "",
      "pipe_url": "",
      "size": 6926982,
      "status": "done",
      "title": "雨打琴键的午夜"
    }
  ],
  "create_at": 1795746231,
  "id": "task_hhDmlZRNA2jMGf3x0KzEFRYTtn84DbFV",
  "status": "SUCCESS",
  "task_type": "instrumental"
}
```

<p align="center">
  <small>© 2026 DMXAPI yinchao-v4.5 生成纯音乐</small>
</p>

