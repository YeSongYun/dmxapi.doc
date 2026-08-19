# 创建令牌

通过平台管理接口创建 API Key。

## 接口

- 方法：`POST`
- 地址：`https://www.dmxapi.cn/api/token/`
- 认证：`SYSTEM_TOKEN` + `USER_ID`，详见 [系统令牌与用户 ID](security_token_ID.md)


## Python 示例

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
remain_quota = 1  # 额度金额，单位 CNY；unlimited_quota=False 时生效，无限额度时忽略
model_limits_enabled = False  # 是否启用模型限制
model_limits = ""  # 允许的模型 ID，用英文逗号分隔
allow_ips = ""  # IP 白名单；换行分隔，留空表示不限制
rate_limits_enabled = True  # 是否启用单令牌限流
rate_limits_time = 60  # 限流时间窗口，单位为秒
rate_limits_count = 60  # 每个窗口允许的最大请求数
rate_limits_content = ""  # 超出限流时返回的提示语
quantity = 1  # 要创建的令牌数量

# 下面无需修改
BASE_URL = "https://www.dmxapi.cn"
expired_time = -1 if expired_time == -1 else int(time.time() + expired_time * 86400)
headers = {
    "Authorization": f"Bearer {SYSTEM_TOKEN}",
    "Dmx-Api-User": str(USER_ID),
}

payload = {
    "expired_time": expired_time,
    "remain_quota": int(remain_quota * 500000),  # 1 元 = 500000 原始额度
    "unlimited_quota": unlimited_quota,
    "model_limits_enabled": model_limits_enabled,
    "model_limits": model_limits,
    "allow_ips": allow_ips,
    "group": "default",
    "rate_limits_enabled": rate_limits_enabled,
    "rate_limits_time": rate_limits_time,
    "rate_limits_count": rate_limits_count,
    "rate_limits_content": rate_limits_content,
}

for index in range(quantity):
    created_name = name if quantity == 1 else f"{name}-{secrets.token_hex(2)}"
    payload["name"] = created_name
    response = requests.post(
        f"{BASE_URL}/api/token/",
        headers=headers,
        json=payload,
        timeout=30,
    )
    response.raise_for_status()
    result = response.json()
    if not result.get("success"):
        raise RuntimeError(result.get("message") or "创建令牌失败")
    print(f"[{index + 1}/{quantity}] 创建成功：{created_name}")
    print(f"服务器响应：{response.text}")
```

## 控制台输出

以下内容由脚本打印；服务器响应会原样显示接口返回的 JSON，具体字段以实际返回为准。

```text
[1/1] 创建成功：DMXAPI创建测试
服务器响应：<接口实际返回的 JSON>
```

当前已验证的创建响应只返回成功状态，不包含完整 API Key。创建后可通过平台的完整 Key 专用读取接口获取；使用时应只在可信设备上临时查看，避免写入日志或截图。普通令牌列表和搜索接口只返回脱敏 Key。

<p align="center">
  <small>© 2026 DMXAPI 创建令牌</small>
</p>
