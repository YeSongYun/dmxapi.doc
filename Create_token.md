# 创建令牌

通过平台管理接口创建 API Key。一个 `POST /api/token/` 请求只创建一个令牌；后台界面的“数量”是批量操作，需要客户端循环发送多次请求。

## 接口

- 方法：`POST`
- 地址：`https://www.dmxapi.cn/api/token/`
- 认证：`SYSTEM_TOKEN` + `USER_ID`
- Content-Type：`application/json`

## HTTP JSON 参数

| 字段 | 类型 | 发送建议 | 说明 |
| --- | --- | --- | --- |
| `name` | string | 本示例显式提供 | 令牌名称；建议非空，批量创建时使用简短基础名称并添加随机后缀 |
| `expired_time` | integer | 本示例填写 `-1` 或正整数天数 | 接口接收 Unix 秒时间戳；本示例会将正整数天数自动转换为时间戳，`-1` 表示永不过期 |
| `remain_quota` | integer | `unlimited_quota=false` 时填写金额 | 接口接收原始额度；本示例按 CNY 输入并自动换算，填写 `1` 表示 `1 CNY` |
| `unlimited_quota` | boolean | 建议显式提供 | 是否无限额度；为 `true` 时通常将 `remain_quota` 设为 `0` |
| `model_limits_enabled` | boolean | 建议显式提供 | 是否启用模型限制 |
| `model_limits` | string | 建议显式提供 | 允许模型的英文逗号分隔字符串；关闭限制时传空字符串 |
| `allow_ips` | string | 建议显式提供 | 每行一个 IP/CIDR；空字符串表示不限制 |
| `group` | string | 固定发送 | 当前只有 `default` 分组，用户无需设置 |
| `rate_limits_enabled` | boolean | 建议显式提供 | 是否启用单令牌限流 |
| `rate_limits_time` | integer | 建议显式提供 | 时间窗口，单位为秒 |
| `rate_limits_count` | integer | 建议显式提供 | 窗口内最大请求次数 |
| `rate_limits_content` | string | 可选 | 超限提示语；后台 UI 标注留空时使用默认提示，最多 1024 字节 |

::: warning “数量”不是调用次数
后台“数量”表示一次创建多个 API Key，不是令牌调用次数限制。当前令牌对象不存在 `unlimited_count` 或 `remain_count` 字段。
:::

## Python 示例

修改代码顶部的参数后直接运行即可。`quantity` 只控制发送多少次创建请求，不会进入 HTTP JSON。

```python
import secrets
import time
import requests

# 只需修改这里
SYSTEM_TOKEN = "请在这里填写系统访问令牌"  # 管理接口使用的系统访问令牌
USER_ID = "请在这里填写用户 ID"  # 与系统访问令牌同账号的用户 ID

name = "DMXAPI创建测试"  # 令牌名称
expired_time = -1  # 填 -1 表示永不过期；填正整数表示多少天后过期
unlimited_quota = True  # True 表示不限制令牌额度
remain_quota = 1  # 额度金额，单位 CNY；False 时生效
model_limits_enabled = False  # 是否启用模型限制
model_limits = ""  # 允许的模型 ID，用英文逗号分隔
allow_ips = ""  # IP 白名单；换行分隔，留空表示不限制
rate_limits_enabled = True  # 是否启用单令牌限流
rate_limits_time = 60  # 限流时间窗口，单位为秒
rate_limits_count = 60  # 每个窗口允许的最大请求数
rate_limits_content = ""  # 超出限流时返回的提示语
quantity = 1  # 要创建的令牌数量

# 下面无需修改
QUOTA_PER_CNY = 500_000  # 额度换算比例：500000 原始额度 = 1 CNY
BASE_URL = "https://www.dmxapi.cn"  # 平台管理接口地址
expired_time = -1 if expired_time == -1 else int(time.time() + expired_time * 86400)
headers = {
    "Authorization": f"Bearer {SYSTEM_TOKEN}",  # 使用系统访问令牌认证
    "Dmx-Api-User": str(USER_ID),  # 指定请求所属的用户 ID
    "Content-Type": "application/json",  # 请求体使用 JSON 格式
}

for index in range(quantity):
    created_name = name if quantity == 1 else f"{name}-{secrets.token_hex(2)}"
    payload = {
        "name": created_name,
        "expired_time": expired_time,
        "remain_quota": int(remain_quota * QUOTA_PER_CNY),  # 将 CNY 金额换算为接口原始额度
        "unlimited_quota": unlimited_quota,
        "model_limits_enabled": model_limits_enabled,
        "model_limits": model_limits,
        "allow_ips": allow_ips,
        "group": "default",  # 当前只有 default 分组，无需用户设置
        "rate_limits_enabled": rate_limits_enabled,
        "rate_limits_time": rate_limits_time,
        "rate_limits_count": rate_limits_count,
        "rate_limits_content": rate_limits_content,
    }
    response = requests.post(
        f"{BASE_URL}/api/token/",
        headers=headers,
        json=payload,
        timeout=30,  # 单次请求最多等待 30 秒
    )
    response.raise_for_status()
    result = response.json()
    if not result.get("success"):
        raise RuntimeError(result.get("message") or "创建令牌失败")
    print(f"[{index + 1}/{quantity}] 创建成功：{created_name}")
```

## 成功响应

```json
[1/1] 创建成功：DMXAPI创建测试
```

当前已验证的创建响应只返回成功状态，不包含完整 API Key。创建后可通过平台的完整 Key 专用读取接口获取；使用时应只在可信设备上临时查看，避免写入日志或截图。普通令牌列表和搜索接口只返回脱敏 Key。

## 字段联动

- `unlimited_quota=true`：令牌不受额度限制，`remain_quota` 不决定可用余额。
- `unlimited_quota=false`：`remain_quota` 决定令牌额度；示例中的数字 `1` 表示 `1 CNY`。
- `expired_time`：填写 `-1` 表示永不过期，填写正整数表示多少天后过期。
- `group`：当前固定为 `default`，用户无需设置。
- `model_limits_enabled=true`：`model_limits` 必须包含允许的模型 ID。
- `model_limits_enabled=false`：将 `model_limits` 设为空字符串。
- `allow_ips`：使用换行分隔，支持单 IP 和 CIDR；留空表示不限制。
- `rate_limits_enabled=true`：应同时配置 `rate_limits_time`、`rate_limits_count` 和可选提示语。
- 后台界面说明成功和失败请求都会计入窗口次数，并标注提示语留空时使用默认文案；本文未用高频模型请求压测这两项运行时行为。

## 下一步

- [获取所有令牌](/Get_all_tokens)
- [搜索令牌](/Search_token)
- [更新令牌](/Update_token)

<p align="center">
  <small>© 2026 DMXAPI 创建令牌</small>
</p>
