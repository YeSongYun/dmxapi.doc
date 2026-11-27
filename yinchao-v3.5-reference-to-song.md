# yinchao-v3.5 参考音频仿写 API 使用文档

提供一段参考音频，再用提示词描述希望保留的节奏、曲风或想更换的乐器，`yinchao-v3.5` 会生成一首新歌。也可以提供自己的歌词。`prompt` 和 `lyric` 至少填写一个。

## 接口地址

| 接口 | 请求方式 | URL |
| --- | --- | --- |
| 提交仿写 | POST | `https://www.dmxapi.cn/yinchao/api/v1/song/generate` |
| 查询新作品 | GET | `https://www.dmxapi.cn/yinchao/api/v1/task/query` |


## 模型名称

`yinchao-v3.5`



## 仿写示例代码


```python
import requests
import json
from uuid import UUID

# ===============================================================
# 步骤1: 配置 API 连接信息
# ===============================================================

url = "https://www.dmxapi.cn/yinchao/api/v1/song/generate"
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

# 填上传或生成响应中的顶层 id，也可以换成公网音频直链或已完成曲目的 ID。
audio_source = "task_替换为参考来源的网关任务ID"

payload = {
    # 【prompt】(string, 条件必填) 仿写方向，最多 1000 个字符。prompt 与 lyric 至少填一项。
    "prompt": "保留参考音频的切分节奏，把配器换成钢琴和低音提琴，副歌加入和声。",

    # 【lyric】(string, 条件必填) 自定义歌词，最多 3000 个字符。
    # "lyric": "[Verse]\n雨落在旧琴键上\n[Chorus]\n让这段旋律陪你回家",

    # 【reference_audio】(object, 必填) 仿写的音频来源。
    "reference_audio": {
        # 【audio_content】(string, 必填) 步骤3填写的来源。
        "audio_content": audio_source,
        # 【audio_type】(string, 必填) 步骤4会在发送前填入 task_id、audio_url 或 audio_id。
    },

    # 【similarity】(number, 可选) 相似度，可填 0.2、0.8、1.3 或 1.5。
    "similarity": 0.8,

    # 【source_task_id】(string, 可选) 使用歌曲 UUID 时，可填原网关任务 ID 以核对曲目归属。
    # "source_task_id": "task_替换为原作品的网关任务ID",

    # 【model】(string, 必填) 仿写使用 yinchao-v3.5。
    "model": "yinchao-v3.5",

    # 【task_type】(string, 必填) 仿写固定填写 reference。
    "task_type": "reference",

    # 【callback】(string, 可选) 可接收进度通知的公网 HTTP(S) 地址。
    # "callback": "https://your-domain.example/yinchao/order-001",
}

# ===============================================================
# 步骤4: 发送请求并输出结果
# ===============================================================

def main():
    if audio_source.startswith("task_"):
        audio_type = "task_id"
    elif audio_source.startswith(("https://", "http://")):
        audio_type = "audio_url"
    else:
        try:
            UUID(audio_source)
        except ValueError:
            raise ValueError("请填写网关任务 ID、音频直链或音潮歌曲 UUID。") from None
        audio_type = "audio_id"
    payload["reference_audio"]["audio_type"] = audio_type

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
      "create_at": 1795752807,
      "duration": 0,
      "error": "",
      "error_code": 0,
      "finish_at": 0,
      "id": "079d2838-8415-4da8-9ea0-de899c7f29e9",
      "lyric": "",
      "pipe_url": "",
      "size": 0,
      "status": "pending",
      "title": ""
    }
  ],
  "create_at": 1795752807,
  "id": "task_nB3gjIgb75fl8k9QEA3zVEmTKOCWXvmU",
  "status": "NOT_START",
  "task_type": "reference"
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
    # 【task_id】(string, 必填) 上方仿写提交响应顶层的 id。
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
      "audio_url": "https://www.dmxapi.cn/v1/tasks/task_nB3gjIgb75fl8k9QEA3zVEmTKOCWXvmU/artifacts/audio-079d2838-8415-4da8-9ea0-de899c7f29e9/content?access=EXAMPLE_SIGNATURE",
      "create_at": 1795752807,
      "duration": 180.454,
      "error": "",
      "error_code": 0,
      "finish_at": 1795753103,
      "id": "079d2838-8415-4da8-9ea0-de899c7f29e9",
      "lyric": "[intro]\n[verse]\n清晨站台上铁轨还潮着\n你递来半杯豆浆手心冒着热\n广播催了两遍谁都没先动\n鞋尖轻轻点着数秒针的拍\n[prechorus]\n钟声卡在闸口风把衣角掀开\n我们把告别说成下次再来\n[chorus]\n数着心跳等车来\n一拍一拍把话都敲开\n数着心跳等车来\n你笑我慢我笑你走太快\n[verse]\n那年旧站牌漆掉了一小块\n你拿钥匙刻下两个人的名字\n后来雨下了几场字迹淡成灰\n我还能认出那一横一撇\n[prechorus]\n钟声卡在闸口风把衣角掀开\n我们把告别说成下次再来\n[chorus]\n数着心跳等车来\n一拍一拍把话都敲开\n数着心跳等车来\n你笑我慢我笑你走太快\n[bridge]\n如果站台再长一点\n我就能把那句留下\n如果车门关得慢一点\n我们还能再数一次节拍\n[chorus]\n数着心跳等车来\n一拍一拍把旧事敲开\n数着心跳等车来\n你往前走我在原地等拍\n[outro]",
      "pipe_url": "",
      "size": 7219726,
      "status": "done",
      "title": "数着心跳等车来"
    }
  ],
  "create_at": 1795752807,
  "id": "task_nB3gjIgb75fl8k9QEA3zVEmTKOCWXvmU",
  "status": "SUCCESS",
  "task_type": "reference"
}
```



<p align="center">
  <small>© 2026 DMXAPI yinchao-v3.5 参考音频仿写</small>
</p>
