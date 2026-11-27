# yinchao-v3.5 提示词生成歌曲 API 使用文档

用 `yinchao-v3.5` 按提示词生成一首带人声的歌曲。省略 `lyric` 时，模型按 `prompt` 自动作词。添加 `lyric` 后，模型会演唱您提供的歌词。生成采用异步方式，完成后可下载 MP3。

## 接口地址

| 接口 | 请求方式 | URL |
| --- | --- | --- |
| 提示词生成歌曲 | POST | `https://www.dmxapi.cn/yinchao/api/v1/song/generate` |
| 查询生成结果 | GET | `https://www.dmxapi.cn/yinchao/api/v1/task/query` |

## 模型名称

`yinchao-v3.5`

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
    # 【prompt】(string, 必填) 描述主题、曲风、配器或人声，1 至 1000 个字符。
    "prompt": "木吉他和口琴伴奏的轻快民谣，唱一个人搭上末班车回家的故事。",

    # 【lyric】(string, 可选) 演唱指定歌词时取消下一行注释。
    # 省略时自动作词，填写时最多 3000 个字符，用 \n 换行。
    # "lyric": "[Verse]\n最后一班车穿过山岗\n[Chorus]\n留一盏灯，等我回家",

    # 【model】(string, 必填) 网关模型名称。
    "model": "yinchao-v3.5",

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

下面是一次真实请求的原始返回。顶层 `id` 是网关任务 ID，`choices[].id` 是单首歌曲的 ID。刚提交时 `status` 为 `NOT_START`，`choices` 也可能为空。

```json
{
  "choices": [
    {
      "audio_url": "",
      "create_at": 1795752802,
      "duration": 0,
      "error": "",
      "error_code": 0,
      "finish_at": 0,
      "id": "22ed315e-d076-4e1d-a30d-610d0a845bfe",
      "lyric": "",
      "pipe_url": "",
      "size": 0,
      "status": "pending",
      "title": ""
    }
  ],
  "create_at": 1795752802,
  "id": "task_cFiZLgdxAsezNWigtKv2BrPSiFy3YV0g",
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
      "audio_url": "https://www.dmxapi.cn/v1/tasks/task_cFiZLgdxAsezNWigtKv2BrPSiFy3YV0g/artifacts/audio-22ed315e-d076-4e1d-a30d-610d0a845bfe/content?access=EXAMPLE_SIGNATURE",
      "create_at": 1795752802,
      "duration": 192.235,
      "error": "",
      "error_code": 0,
      "finish_at": 1795752907,
      "id": "22ed315e-d076-4e1d-a30d-610d0a845bfe",
      "lyric": "[intro]\n[verse]\n末班车在九点四十 晃过旧钟楼的影\n我数着车窗的雨痕 一路往南行\n卖花阿婆收起板凳 街灯啪地亮起\n扶手还留着谁的余温 像一句没说完的叮咛\n[prechorus]\n木椅吱呀 摇过三个站\n我把外套 往身上裹紧一点\n[chorus]\n末班车 带我回家\n穿过熄了灯的红绿灯 和打烊的茶摊\n末班车 慢慢摇啊\n摇碎一天的重 摇回一扇亮着的窗\n[verse]\n斜对座睡着个少年 书包趴在他膝盖\n耳机线垂到地板上 漏出半句节拍\n我摸出口袋里的硬币 买了瓶热豆浆\n倒影里那个赶路的人 终于肯松一松肩膀\n[prechorus]\n报站的声音 轻了一半\n我数着台阶 等那扇门开\n[chorus]\n末班车 带我回家\n穿过熄了灯的红绿灯 和打烊的茶摊\n末班车 慢慢摇啊\n摇碎一天的重 摇回一扇亮着的窗\n[bridge]\n窗外有人推着推车 收走最后一批灯\n我也把心里的账 一笔一笔收拢\n下一站就到 下一站就到\n鞋底沾着一天的灰 也能拍拍就轻\n[chorus]\n末班车 带我回家\n穿过熄了灯的红绿灯 和打烊的茶摊\n末班车 慢慢摇啊\n摇碎一天的重 摇回一扇亮着的窗\n摇回那扇 亮着的窗\n[outro]",
      "pipe_url": "",
      "size": 7690975,
      "status": "done",
      "title": "末班车，亮着的窗"
    }
  ],
  "create_at": 1795752802,
  "id": "task_cFiZLgdxAsezNWigtKv2BrPSiFy3YV0g",
  "status": "SUCCESS",
  "task_type": "normal"
}
```


<p align="center">
  <small>© 2026 DMXAPI yinchao-v3.5 提示词生成歌曲</small>
</p>

