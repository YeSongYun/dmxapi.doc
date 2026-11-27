# yinchao-v4.5 提示词生成歌曲 API 使用文档

用 `yinchao-v4.5` 按提示词生成一首带人声的歌曲。省略 `lyric` 时，模型按 `prompt` 自动作词。添加 `lyric` 后，模型会演唱您提供的歌词。生成采用异步方式，完成后可下载 MP3。

## 接口地址

| 接口 | 请求方式 | URL |
| --- | --- | --- |
| 提示词生成歌曲 | POST | `https://www.dmxapi.cn/yinchao/api/v1/song/generate` |
| 查询生成结果 | GET | `https://www.dmxapi.cn/yinchao/api/v1/task/query` |


## 模型名称

`yinchao-v4.5`

## 提示词生成歌曲示例代码


```python
import requests
import json

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

payload = {
    # 【prompt】(string, 必填) 描述主题、曲风、配器或人声，1 至 3000 个字符。
    "prompt": "写一首中速灵魂乐，电钢琴和贝斯伴奏，唱清晨第一班渡轮出港，副歌由两人合唱。",

    # 【lyric】(string, 可选) 演唱指定歌词时取消下一行注释。
    # 省略时自动作词，填写时最多 5000 个字符，用 \n 换行。
    # "lyric": "[Verse]\n渡轮的灯摇过港湾\n[Chorus]\n趁天色初亮，我们出发",

    # 【model】(string, 必填) 网关模型名称。
    "model": "yinchao-v4.5",

    # 【task_type】(string, 必填) 提示词生歌固定填写 normal。
    "task_type": "normal",

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

顶层 `id` 是网关任务 ID，`choices[].id` 是单首歌曲的 ID。下面列出这次提交需要保存的字段。刚提交时，`choices` 也可能为空。

```json
{
  "choices": [
    {
      "audio_url": "",
      "create_at": 1795752804,
      "duration": 0,
      "error": "",
      "error_code": 0,
      "finish_at": 0,
      "id": "4608559e-41d1-4028-9e86-272ecf2db69c",
      "lyric": "",
      "pipe_url": "",
      "size": 0,
      "status": "running",
      "title": ""
    }
  ],
  "create_at": 1795752804,
  "id": "task_PHhukAvTDmz2hEnbrajxbXjiAPWU1dDL",
  "status": "NOT_START",
  "task_type": "normal"
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
    # 【task_id】(string, 必填) 上方歌曲生成提交响应顶层的 id。
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
      "audio_url": "https://www.dmxapi.cn/v1/tasks/task_PHhukAvTDmz2hEnbrajxbXjiAPWU1dDL/artifacts/audio-4608559e-41d1-4028-9e86-272ecf2db69c/content?access=EXAMPLE_SIGNATURE",
      "create_at": 1795752804,
      "duration": 165.277,
      "error": "",
      "error_code": 0,
      "finish_at": 1795752906,
      "id": "4608559e-41d1-4028-9e86-272ecf2db69c",
      "lyric": "[intro]\n[verse]\n码头还压着夜色的凉\n铁索在指间一寸寸收\n第一盏灯亮在船头上\n江面的雾像没醒透\n[prechorus]\n我数着跳板震动的响\n你把票根握在掌中\n[chorus]\n第一班渡轮出港\n载着还没醒的天光\n你在左\n我在右\n把清晨划成两半\n第一班渡轮出港\n不谈从前\n不问远方\n汽笛一响\n我们并肩\n往对岸去\n[verse]\n推车的老人靠在栏杆\n热豆浆的味道慢慢散\n学生把书包抱在怀里面\n打盹也跟着船身晃\n[prechorus]\n你笑着说风有点凉\n把外套搭在我的肩上\n[chorus]\n第一班渡轮出港\n载着还没醒的天光\n你在左\n我在右\n把清晨划成两半\n第一班渡轮出港\n不谈从前\n不问远方\n汽笛一响\n我们并肩\n往对岸去\n[bridge]\n船头剪开一整片白\n身后的岸越来越窄\n有些路只走这一次\n也够我记很久\n[chorus]\n第一班渡轮出港\n载着慢慢亮起的天光\n你还在\n我也在\n把清晨完整地走完\n第一班渡轮出港\n不谈从前\n不问远方\n汽笛再响\n我们并肩\n往对岸去\n[outro]",
      "pipe_url": "",
      "size": 6612468,
      "status": "done",
      "title": "第一班渡轮"
    }
  ],
  "create_at": 1795752804,
  "id": "task_PHhukAvTDmz2hEnbrajxbXjiAPWU1dDL",
  "status": "SUCCESS",
  "task_type": "normal"
}
```


<p align="center">
  <small>© 2026 DMXAPI yinchao-v4.5 提示词生成歌曲</small>
</p>

