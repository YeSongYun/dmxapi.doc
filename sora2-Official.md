# OpenAI 视频模型 Sora-2 官方接口请求格式 API使用文档

## 模型名称
`sora-2`

## 接口地址
调用 `sora-2` 官方接口需分两步：  
1. 提交视频生成任务  
2. 根据返回的 `ID` 查询结果  

| 功能 | 端点 |
|------|------|
| 提交视频任务 | `https://www.dmxapi.cn/v1/videos` |
| 查询视频结果 | `https://www.dmxapi.cn/v1/videos/{VIDEO_ID}/content` |
## 可选参数
- `seconds`：视频时长（单位：秒），可选值：`4` / `8` / `12`  
- `size`：分辨率，可选值：
  - `720x1280`（竖屏）
  - `1280x720`（横屏）
  - `1024x1792`（竖屏）
  - `1792x1024`（横屏）
:::tip
视频仅保存两个小时，请在有效期内提取
:::

## python 请求发送示例代码
```python
"""
========================================
Sora-2 官方示例脚本（调用 DMXAPI 生成视频）
----------------------------------------
用途
- 使用 `requests` 向 `DMXAPI` 的 `/v1/videos` 接口发起请求，生成短视频。

运行前准备
- 安装依赖：`pip install requests`
- 推荐使用环境变量管理配置，避免把密钥写进代码：
  - `API_URL`：接口地址，默认 `https://www.dmxapi.cn/v1/videos`
  - `API_TOKEN`：访问令牌，用于 `Authorization: <TOKEN>`

安全提示
- 生产环境请务必通过环境变量或密钥管理方案注入 Token，不要硬编码在仓库中。
========================================
"""
import os
import requests

# 接口地址与访问令牌（优先读取环境变量）
API_URL = os.environ.get("API_URL", "https://www.dmxapi.cn/v1/videos")
# 警告：默认值仅用于示例，请改为使用环境变量传入真实令牌
TOKEN = os.environ.get("API_TOKEN", "sk-****************************************") # 请替换为您的DMXAPI的令牌

# HTTP 请求头，使用 Token 进行鉴权
headers = {
    "Authorization": f"{TOKEN}",
}

# 表单参数说明：
# - prompt：文生视频的自然语言描述
# - model：模型名称（此处示例为 `sora-2`）
# - seconds：视频时长（单位秒）
# - size：分辨率，格式为 `宽x高`
files = {
    "prompt": (None, "一个充满科技感的店铺，招牌上写着 DMXAPI 。店铺里很多机器人在招待顾客。"),  # 视频描述
    "model": (None, "sora-2"), # 模型名称
    "seconds": (None, "12"), # 视频时长（单位秒），可选4,8,12
    "size": (None, "720x1280"), # 分辨率，可选720x1280,1280x720,1024x1792,1792x1024
}

# 发送请求并输出结果（优先尝试解析 JSON）
response = requests.post(API_URL, headers=headers, files=files, timeout=60)
print(response.status_code)
try:
    print(response.json())
except ValueError:
    # 若返回非 JSON 内容，则直接输出原始文本
    print(response.text)
```
### 返回示例
```json
200
{
  "id": "video_690489c662148190bbf1edc3bd807379channel1547", # 视频任务ID，下一步需要使用
  "object": "video",
  "created_at": 1761905094,
  "status": "queued",
  "completed_at": null,
  "error": null,
  "expires_at": null,
  "model": "sora-2",
  "progress": 0,
  "remixed_from_video_id": null,
  "seconds": "12",
  "size": "720x1280"
}
```


## python 视频获取示例代码
::: tip 注意
- 视频生成需要一定时间，建议先在任务日志 https://www.dmxapi.cn/task 中确认完成后再下载。
- 您需要使用请求返回的 `id` 来获取视频文件。
:::

```python
"""
DMXAPI sora-2 视频内容下载脚本

功能概述：
- 通过指定的视频任务 ID 从 DMXAPI 拉取最终视频文件。
- 实时展示百分比、速度、已下载大小、剩余时间与累计用时。

使用说明：
1) 将环境变量 `OPENAI_API_KEY` 设置为你的令牌（或直接在下方变量中填写）。
2) 可选：设置环境变量 `OPENAI_API_BASE` 指定接口地址，默认 `https://www.dmxapi.cn`。
3) 将 `VIDEO_ID` 替换为需要下载的视频任务 ID。
4) 运行脚本后，文件会保存到当前脚本同目录下的 `output/` 文件夹。
"""

import os
import sys
import re
import requests
import time
import threading

# 视频任务 ID：请替换为你需要下载的目标任务 ID
VIDEO_ID = "video_690489c662148190bbf1edc3bd807379channel1547" # 请替换为您需要提前的视频任务ID

# DMXAPI 令牌：优先从环境变量读取，未设置时可在此填入占位符
api_key = os.getenv("OPENAI_API_KEY", "sk-************************************") # 请替换为您的DMXAPI的令牌

# DMXAPI 接口地址：可通过环境变量覆盖，默认使用官网地址
base_url = os.getenv("OPENAI_API_BASE", "https://www.dmxapi.cn")

def human_bytes(n):
    """
    将字节数或数字转换为人类友好的字符串（B/KB/MB/GB/TB）。

    参数：
        n: 数字或字节数。

    返回：
        带单位的字符串，例如 "512 B"、"1.23 MB"。
    """
    try:
        n = float(n)
    except Exception:
        return f"{n} B"
    units = ["B", "KB", "MB", "GB", "TB"]
    for u in units:
        if n < 1024 or u == "TB":
            return f"{n:.2f} {u}" if u != "B" else f"{int(n)} B"
        n /= 1024

def format_seconds(s):
    """
    将秒数格式化为时间字符串。

    规则：
    - 当小时数为 0 时，显示为 "MM:SS"；否则显示 "HH:MM:SS"。
    """
    s = int(s)
    h = s // 3600
    m = (s % 3600) // 60
    sec = s % 60
    if h:
        return f"{h:02d}:{m:02d}:{sec:02d}"
    return f"{m:02d}:{sec:02d}"

def queue_progress(stop_event, total_seconds=300, bar_len=30):
    """
    在排队阶段绘制进度条（非阻塞）。

    说明：
    - 该线程会一直更新进度，直到 `stop_event` 被设置。
    - `total_seconds` 用于估算排队时长，仅用于显示，不影响逻辑。
    - `bar_len` 控制进度条的宽度（字符数）。
    """
    start = time.time()
    while not stop_event.is_set():
        elapsed = time.time() - start
        progress = min(elapsed / total_seconds, 1.0)
        filled = int(bar_len * progress)
        bar = "█" * filled + "-" * (bar_len - filled)
        percent = progress * 100
        sys.stdout.write(f"\r排队中：[{bar}] {percent:.1f}%")
        sys.stdout.flush()
        time.sleep(0.2)
    # 停止时瞬间填满到100%
    sys.stdout.write(f"\r排队中：[{'█' * bar_len}] 100.0%")
    sys.stdout.flush()

 

def main():
    """
    主流程：校验令牌，发起下载请求，显示进度并保存文件。

    流程概览：
    1) 校验并构造请求参数与头部；
    2) 启动排队进度线程；
    3) 以流式方式下载数据并写入本地文件；
    4) 根据是否提供 `Content-Length` 选择显示不同的进度信息；
    5) 下载完成或异常时，优雅地结束进度线程并给出提示。
    """
    if not api_key:
        print("请先将环境变量 OPENAI_API_KEY 设置为你的令牌。")
        sys.exit(1)

    # 构造下载链接与请求头
    url = f"{base_url}/v1/videos/{VIDEO_ID}/content"
    headers = {"Authorization": f"{api_key}"}

    try:
        # 预计排队时长仅用于友好提示，不影响实际下载速度
        print("开始下载，预计需要300s")

        # 启动排队进度线程：直到收到首个数据块后再停止它
        stop_event = threading.Event()
        t = threading.Thread(target=queue_progress, args=(stop_event, 300, 30), daemon=True)
        t.start()

        # 发起流式下载请求，允许重定向；`stream=True` 使我们可以逐块写入文件
        resp = requests.get(url, headers=headers, stream=True, allow_redirects=True)
        resp.raise_for_status()

        # 从响应头尝试解析文件名；若无则使用默认 `VIDEO_ID.mp4`
        filename = f"{VIDEO_ID}.mp4"
        cd = resp.headers.get("Content-Disposition")
        if cd:
            m = re.search(r'filename="?([^";]+)"?', cd)
            if m:
                filename = m.group(1)

        # 准备输出目录与最终文件路径
        output_dir = os.path.join(os.path.dirname(__file__), "output")
        os.makedirs(output_dir, exist_ok=True)
        filepath = os.path.join(output_dir, filename)

        # 获取总大小用于精确进度显示；若缺失则退化为不含百分比的显示
        total = resp.headers.get("Content-Length")
        total = int(total) if total and total.isdigit() else 0
        downloaded = 0
        bar_len = 30
        start_time = None

        # 按块写入下载数据；首次收到数据时切换为下载进度并停止排队显示
        with open(filepath, "wb") as f:
            first_data = True
            for chunk in resp.iter_content(chunk_size=8192):
                if not chunk:
                    continue
                if first_data:
                    first_data = False
                    # 排队进度条瞬间100%，然后换行进入下载进度
                    stop_event.set()
                    t.join(timeout=1)
                    sys.stdout.write("\n")
                    sys.stdout.flush()
                    start_time = time.time()
                f.write(chunk)
                downloaded += len(chunk)
                elapsed = time.time() - start_time if start_time else 0
                speed = downloaded / elapsed if elapsed > 0 else 0
                if total > 0:
                    # 已知总大小时，计算百分比、ETA 与进度条填充
                    filled = int(bar_len * downloaded / total)
                    filled = min(filled, bar_len)
                    bar = "█" * filled + "-" * (bar_len - filled)
                    pct = downloaded * 100 / total
                    eta = (total - downloaded) / speed if speed > 0 else 0
                    line = (
                        f"\r下载进度 [{bar}] {pct:.1f}% "
                        f"{human_bytes(downloaded)}/{human_bytes(total)} | "
                        f"速度 {human_bytes(speed)}/s | "
                        f"剩余 {format_seconds(eta)} | 用时 {format_seconds(elapsed)}"
                    )
                    sys.stdout.write(line)
                    sys.stdout.flush()
                else:
                    # 未知总大小时，仅显示已下载与当前速度
                    line = (
                        f"\r已下载 {human_bytes(downloaded)} | "
                        f"速度 {human_bytes(speed)}/s | 用时 {format_seconds(elapsed)}"
                    )
                    sys.stdout.write(line)
                    sys.stdout.flush()

            # 如果没有收到任何数据，也结束排队进度条
            if first_data:
                stop_event.set()
                t.join(timeout=1)
                sys.stdout.write("\n")
                sys.stdout.flush()

        print()
        print(f"下载成功，已保存到: {filepath}")
    except requests.HTTPError as e:
        # 网络或服务端错误：确保结束排队线程并打印详细错误信息
        try:
            stop_event.set()
            t.join(timeout=1)
            sys.stdout.write("\n")
            sys.stdout.flush()
        except Exception:
            pass
        print(f"请求失败: {e} - {getattr(e.response, 'text', '')}")
        sys.exit(2)
    except Exception as e:
        # 其他异常：同样优雅地结束排队线程并退出
        try:
            stop_event.set()
            t.join(timeout=1)
            sys.stdout.write("\n")
            sys.stdout.flush()
        except Exception:
            pass
        print(f"发生错误: {e}")
        sys.exit(3)

if __name__ == "__main__":
    main()
```

### 返回示例
```json
开始下载，预计需要300s
排队中：[██████████████████████████████] 100.0%
下载进度 [██████████████████████████████] 100.0% 8.63 MB/8.63 MB | 速度 25.36 MB/s | 剩余 00:00 | 用时 00:01
下载成功，已保存到: c:\Users\98317\Desktop\xiangmu\kefang\output\video_690489c662148190bbf1edc3bd807379_video.mp4
```

---

<p align="center">
  <small>© 2025 DMXAPI sora-2</small>
</p>