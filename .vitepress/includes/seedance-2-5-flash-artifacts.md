::: details 下载视频与尾帧（可选）

要将视频保存到本地，将下面的代码接在本页的查询脚本末尾运行。它使用上一步的 `result`、`task_id` 和 `headers`，从网关获取视频和可选的尾帧。如果网关暂时无法提供文件，脚本会尝试查询结果中的 HTTPS 临时地址。文件保存在当前目录的 `output` 文件夹。

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 获取产物清单 | GET | `https://www.dmxapi.cn/v1/tasks/{task_id}/artifacts` |
| 下载指定产物 | GET | `https://www.dmxapi.cn/v1/tasks/{task_id}/artifacts/{key}/content` |

`{key}` 填 `video` 或 `last_frame`。临时视频和尾帧地址有效期为 24 小时，每个临时视频地址最多可下载 100 次。启用尾帧时，产物清单示例如下。

```json
{
  "artifacts": [
    { "key": "video", "mime_type": "video/mp4" },
    { "key": "last_frame", "mime_type": "image/jpeg" }
  ]
}
```

```python
from pathlib import Path
from tempfile import NamedTemporaryFile
from urllib.parse import urlsplit

artifacts_url = f"https://www.dmxapi.cn/v1/tasks/{quote(task_id, safe='')}/artifacts"
output_dir = Path("output")
output_dir.mkdir(exist_ok=True)
content = result.get("content") or {}

# 清单给出可下载的产物 key 和媒体类型。遇到临时错误时仍可按已知 key 尝试下载。
try:
    with requests.get(artifacts_url, headers=headers, timeout=(10, 60)) as response:
        response.raise_for_status()
        listed = {item["key"]: item.get("mime_type") for item in response.json()["artifacts"]}
except (requests.RequestException, KeyError, TypeError, ValueError):
    listed = {}

extensions = {
    "video": {"video/mp4": ".mp4", "video/quicktime": ".mov"},
    "last_frame": {"image/jpeg": ".jpg", "image/png": ".png"},
}


def save_file(response, key, expected_type, direct_url):
    """校验媒体类型及长度，完整写入后再替换目标文件。"""
    response.raise_for_status()
    if response.status_code != 200:
        raise ValueError(f"下载 {key} 需要完整文件，收到 HTTP {response.status_code}")
    media_type = response.headers.get("Content-Type", "").split(";", 1)[0].strip().lower()
    if media_type in ("", "application/octet-stream", "binary/octet-stream", "application/binary"):
        path = urlsplit(direct_url or "").path.lower()
        if key == "video":
            media_type = "video/quicktime" if path.endswith(".mov") else "video/mp4"
        else:
            media_type = "image/png" if path.endswith(".png") else "image/jpeg"
    if media_type not in extensions[key]:
        raise ValueError(f"{key} 返回了意外的媒体类型 {media_type!r}")
    # 网关可能将 MOV 也标成 video/mp4。优先按任务结果或清单中声明的格式命名。
    if expected_type in extensions[key]:
        media_type = expected_type
    name = "".join(c if c.isalnum() or c in "-_" else "_" for c in task_id)
    target = output_dir / f"{name}_{key}{extensions[key][media_type]}"
    temp_path = None
    size = 0
    try:
        with NamedTemporaryFile(dir=output_dir, suffix=".part", delete=False) as file:
            temp_path = Path(file.name)
            for chunk in response.iter_content(chunk_size=1024 * 1024):
                if not chunk:
                    continue
                if size == 0 and chunk.lstrip().startswith((b"<", b"{", b"[")):
                    raise ValueError(f"{key} 下载地址返回了文本内容")
                file.write(chunk)
                size += len(chunk)
        if size == 0:
            raise ValueError(f"{key} 下载结果为空")
        length = response.headers.get("Content-Length", "")
        if not response.headers.get("Content-Encoding") and length.isdecimal() and size != int(length):
            raise ValueError(f"{key} 下载不完整，预期 {length} 字节，收到 {size} 字节")
        temp_path.replace(target)
    finally:
        if temp_path is not None and temp_path.exists():
            temp_path.unlink()


for key in ("video", "last_frame"):
    direct_url = content.get(f"{key}_url")
    if key == "last_frame" and key not in listed and not direct_url:
        continue
    expected_type = listed.get(key)
    if key == "video":
        video_types = {"mp4": "video/mp4", "mov": "video/quicktime"}
        expected_type = video_types.get(result.get("output_format")) or expected_type

    try:
        with requests.get(f"{artifacts_url}/{key}/content", headers=headers, stream=True, timeout=(10, 120)) as response:
            save_file(response, key, expected_type, direct_url)
    except (requests.RequestException, ValueError):
        parts = urlsplit(direct_url or "")
        if parts.scheme != "https" or not parts.hostname or parts.username is not None or parts.password is not None:
            raise
        # 临时地址已带下载凭据，直接请求时只向文件服务获取内容。
        with requests.get(direct_url, stream=True, timeout=(10, 120)) as response:
            save_file(response, key, expected_type, direct_url)
```
:::

::: details 查询状态与返回字段

如果只想查询一次，将提交时使用的 API Key 和返回的 `id` 分别设为环境变量 `DMXAPI_API_KEY` 和 `TASK_ID`，然后运行以下命令。

```bash
curl --request GET \
  --header "Authorization: Bearer ${DMXAPI_API_KEY}" \
  "https://www.dmxapi.cn/api/v3/contents/generations/tasks/${TASK_ID}"
```

| 字段 | 说明 |
|------|------|
| `status` | `queued` 排队中，`running` 执行中，`succeeded` 已生成。其余终态为 `failed` 失败、`cancelled` 已取消、`expired` 已过期 |
| `error.code`、`error.message` | HTTP 200 也可能返回失败终态。使用这两个字段查看失败原因。任务类型与参数冲突时可能返回 `InvalidParameter.TaskTypeConstraint`，提示词意图与指定任务类型不符时可能返回 `InvalidParameter.TaskTypeMismatch` |
| `created_at`、`updated_at` | 创建和更新时间，均为 Unix 秒级时间戳 |
| `execution_expires_after` | 从创建起允许排队和执行的总秒数 |
| `content.video_url`、`content.last_frame_url` | 成片地址和可选的 JPEG 尾帧地址。尾帧与成片同尺寸 |
| `duration`、`framespersecond` | 时长和帧率。时长取实际帧数除以 24 后向下取整的秒数 |
| `resolution`、`ratio` | 成片的分辨率档位和实际宽高比 |
| `generate_audio`、`output_format`、`seed` | 是否含同步音频、实际文件格式和随机种子 |
| `usage.completion_tokens`、`usage.total_tokens` | 实际计费的视频 token，两项数值相同。有参考视频且触发最低用量时，返回值包含最低用量 |
| `usage.tool_usage.web_search` | 启用联网搜索的纯文生视频任务可能返回此项，表示实际搜索次数 |

方舟侧的普通视频任务自创建起可查询 7 天。成功任务按 `completion_tokens × 每百万 token 单价 ÷ 1,000,000` 计费。含参考视频时单价为 28 元，其余为 46 元。网关按有效用量结算，缺少有效用量时沿用预扣。失败、取消或过期会退回预扣。

接口字段可查阅火山方舟的[创建视频生成任务](https://docs.volcengine.com/docs/ark/create-video-generation-task-api?lang=zh)和[查询视频生成任务](https://docs.volcengine.com/docs/ark/get-video-generation-task-api?lang=zh)。
:::
