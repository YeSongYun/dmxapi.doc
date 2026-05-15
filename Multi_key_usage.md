# 多 Key 用量监控

当你把多个令牌（Key）分发给不同的人、不同的项目或不同的客户使用时，常常需要回答这些问题：**每个 Key 累计花了多少？这个月谁用得最多？某个 Key 今天调了哪些模型？余额还够吗？** 本文档提供一份完整的多 Key 用量全景方案，一次性输出汇总对账表与逐 Key 调用明细，覆盖累计、本月、本周、今日四个时间维度，方便对账、排查异常调用与控制成本。

## 认证参数说明

| 参数 | 说明 |
|------|------|
| `SYSTEM_TOKEN` | 系统令牌，获取路径：登录 DMXAPI → 工作台 → 个人设置 → 更多选项 → 系统令牌 |
| `USER_ID` | 当前用户 ID，获取路径：登录 DMXAPI → 工作台 → 个人设置 |

:::warning
请妥善保管您的系统令牌！SYSTEM_TOKEN 拥有账户管理权限，严禁泄露给他人或提交到公开仓库。
:::

## 实现思路

本方案组合调用以下三个平台接口，按"令牌名称"`token_name` 作为筛选条件实现按 Key 维度的用量统计：

| 接口 | 用途 | 用到的字段 |
|------|------|------|
| `GET /api/token/` | 获取账号下全部令牌 | `name`、`key`、`status`、`used_quota`、`remain_quota`、`unlimited_quota`、`accessed_time` |
| `GET /api/log/self/stat` | 按时间范围聚合消耗 | 查询参数 `token_name` 实现按 Key 筛选 |
| `GET /api/log/self` | 获取调用明细记录 | 查询参数 `token_name` 实现按 Key 筛选 |

:::tip 关键约定
所有"按 Key 筛选"都通过 `token_name`（令牌名称）字段进行，不是 Key 本身。**强烈建议分发 Key 时给每个 Key 取有意义的名字**（例如 `客户A`、`项目X-生产`、`员工-张三`），这样统计自然按业务分组。
:::

## 接口说明

- 请求方式：`GET`
- 请求地址（依次调用）：
  - `https://www.dmxapi.cn/api/token/`
  - `https://www.dmxapi.cn/api/log/self/stat`
  - `https://www.dmxapi.cn/api/log/self`
- 认证头：`Authorization: Bearer {SYSTEM_TOKEN}` + `Rix-Api-User: {USER_ID}`
- 用途：组合查询多 Key 的累计/分时段用量、剩余额度与最近调用记录

## 主要参数说明

下表列出脚本配置区可调整的参数：

| 参数 | 必填 | 说明 |
|------|------|------|
| `SYSTEM_TOKEN` | 是 | 系统令牌 |
| `USER_ID` | 是 | 用户 ID |
| `KEY_NAME_FILTER` | 否 | 仅统计名称包含该关键字的令牌，留空表示统计全部令牌 |
| `RECENT_LOG_LIMIT` | 否 | 每个 Key 在明细报告中保留的最近调用记录数，默认 `20` 条 |
| `EXPORT_CSV` | 否 | 是否导出汇总 CSV 对账表，默认 `True` |
| `EXPORT_TXT` | 否 | 是否导出详细 TXT 报告，默认 `True` |
| `CSV_FILENAME` | 否 | CSV 文件名，默认 `多Key用量汇总.csv` |
| `TXT_FILENAME` | 否 | TXT 文件名，默认 `多Key用量明细报告.txt` |

## 代码示例

```python
import requests
import csv
import os
from datetime import datetime, timedelta

# ===== 只需修改这里 =====

# 【SYSTEM_TOKEN】(string, 必填) 系统令牌
# 获取路径：登录 DMXAPI → 工作台 → 个人设置 → 更多选项 → 系统令牌
SYSTEM_TOKEN = "你的系统令牌"

# 【USER_ID】(string, 必填) 当前用户 ID
# 获取路径：登录 DMXAPI → 工作台 → 个人设置
USER_ID = "你的用户id"

# 【KEY_NAME_FILTER】(string, 可选) 令牌名称过滤关键字
# 留空表示统计账号下全部令牌；填值后只统计名称中包含该关键字的令牌
# 示例: "客户" 只统计名称含"客户"的所有令牌
KEY_NAME_FILTER = ""

# 【RECENT_LOG_LIMIT】(int, 可选) 每个 Key 保留的最近调用记录数
# 用于 TXT 报告的明细层；过大会拖慢生成速度
RECENT_LOG_LIMIT = 20

# 【EXPORT_CSV】(bool, 可选) 是否导出汇总 CSV 对账表
EXPORT_CSV = True

# 【EXPORT_TXT】(bool, 可选) 是否导出详细 TXT 报告
EXPORT_TXT = True

# 【CSV_FILENAME】(string, 可选) 汇总 CSV 文件名
CSV_FILENAME = "多Key用量汇总.csv"

# 【TXT_FILENAME】(string, 可选) 详细 TXT 报告文件名
TXT_FILENAME = "多Key用量明细报告.txt"

# ========================

# 以下为自动处理逻辑，无需修改

BASE_URL = "https://www.dmxapi.cn"
HEADERS = {
    "Authorization": f"Bearer {SYSTEM_TOKEN}",
    "Rix-Api-User": USER_ID,
    "Accept": "application/json",
}

# 额度换算系数：原始 quota 值 / 500000 = 人民币元
QUOTA_DIVISOR = 500000


def fmt_time(ts):
    """格式化时间戳"""
    if ts is None or ts == -1:
        return "永不过期"
    if ts == 0:
        return "未设置"
    return datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")


def fmt_money(quota_raw):
    """将原始 quota 值换算为人民币元"""
    return quota_raw / QUOTA_DIVISOR


def mask_key(key):
    """对 Key 进行脱敏显示，仅保留首尾 4 位"""
    if not key:
        return ""
    if len(key) <= 8:
        return f"sk-{key}"
    return f"sk-{key[:4]}{'*' * 24}{key[-4:]}"


def get_all_tokens():
    """获取账号下全部令牌列表"""
    resp = requests.get(f"{BASE_URL}/api/token/", headers=HEADERS)
    resp.raise_for_status()
    result = resp.json()
    if not result.get("success"):
        print(f"获取令牌列表失败: {result.get('message')}")
        return []
    return result["data"].get("items", [])


def get_period_quota(token_name, start_ts, end_ts):
    """
    查询指定令牌在指定时间范围内的消耗额度

    Args:
        token_name: 令牌名称（按此字段筛选）
        start_ts: 开始时间戳（秒）
        end_ts: 结束时间戳（秒）

    Returns:
        float: 期间消耗的人民币金额；查询失败返回 0
    """
    params = {
        "type": 0,
        "token_name": token_name,
        "token_group": "",
        "model_name": "",
        "start_timestamp": start_ts,
        "end_timestamp": end_ts,
    }
    resp = requests.get(f"{BASE_URL}/api/log/self/stat", headers=HEADERS, params=params)
    if resp.status_code != 200:
        return 0.0
    result = resp.json()
    if not result.get("success"):
        return 0.0
    return fmt_money(result.get("data", {}).get("quota", 0))


def get_recent_logs(token_name, start_ts, end_ts, page_size=50):
    """获取指定令牌的最近调用明细（取第 1 页，最多 page_size 条）"""
    params = {
        "p": 1,
        "page_size": page_size,
        "type": 0,
        "token_name": token_name,
        "start_timestamp": start_ts,
        "end_timestamp": end_ts,
    }
    resp = requests.get(f"{BASE_URL}/api/log/self", headers=HEADERS, params=params)
    if resp.status_code != 200:
        return []
    result = resp.json()
    if not result.get("success"):
        return []
    return result["data"].get("items", [])


def aggregate_by_model(items):
    """按模型分组汇总调用记录"""
    stats = {}
    for item in items:
        model = item.get("model_name") or "(未知)"
        quota = fmt_money(item.get("quota", 0))
        prompt = item.get("prompt_tokens", 0)
        completion = item.get("completion_tokens", 0)

        if model not in stats:
            stats[model] = {"quota": 0.0, "count": 0, "prompt": 0, "completion": 0}
        stats[model]["quota"] += quota
        stats[model]["count"] += 1
        stats[model]["prompt"] += prompt
        stats[model]["completion"] += completion

    # 按消耗倒序排列
    return dict(sorted(stats.items(), key=lambda x: x[1]["quota"], reverse=True))


def get_time_ranges():
    """生成今日/本周/本月三个时间范围的时间戳元组"""
    now = datetime.now()
    today = now.replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = today.replace(hour=23, minute=59, second=59)
    week_start = today - timedelta(days=6)
    month_start = today - timedelta(days=29)
    return {
        "today": (int(today.timestamp()), int(today_end.timestamp())),
        "week": (int(week_start.timestamp()), int(now.timestamp())),
        "month": (int(month_start.timestamp()), int(now.timestamp())),
    }


def build_key_report(token, ranges):
    """
    构建单个 Key 的完整用量报告

    Returns:
        dict: 包含汇总数据和明细数据的字典
    """
    name = token["name"]

    # 累计已用额度（直接从令牌信息读取，不需要再查接口）
    total_used = fmt_money(token.get("used_quota", 0))

    # 剩余额度
    if token.get("unlimited_quota"):
        remain_str = "无限"
        remain_value = None
    else:
        remain_value = fmt_money(token.get("remain_quota", 0))
        remain_str = f"{remain_value:.4f} 元"

    # 分时段消耗（调用统计接口）
    today_quota = get_period_quota(name, *ranges["today"])
    week_quota = get_period_quota(name, *ranges["week"])
    month_quota = get_period_quota(name, *ranges["month"])

    # 最近调用明细（取月范围内的第 1 页数据）
    recent_items = get_recent_logs(name, *ranges["month"], page_size=max(50, RECENT_LOG_LIMIT))
    model_stats = aggregate_by_model(recent_items)
    recent_items = recent_items[:RECENT_LOG_LIMIT]

    return {
        "id": token.get("id"),
        "name": name,
        "key_masked": mask_key(token.get("key", "")),
        "status": "启用" if token.get("status") == 1 else "禁用",
        "group": token.get("group", "default"),
        "total_used": total_used,
        "today_quota": today_quota,
        "week_quota": week_quota,
        "month_quota": month_quota,
        "remain_str": remain_str,
        "remain_value": remain_value,
        "created_time": fmt_time(token.get("created_time")),
        "accessed_time": fmt_time(token.get("accessed_time")),
        "expired_time": fmt_time(token.get("expired_time")),
        "model_stats": model_stats,
        "recent_items": recent_items,
    }


def print_summary_table(reports):
    """终端输出汇总表"""
    print("=" * 110)
    print(f"{'令牌名称':<20} {'状态':<6} {'累计(元)':>12} {'本月(元)':>12} {'本周(元)':>12} {'今日(元)':>12} {'剩余':<14} {'最后访问':<20}")
    print("-" * 110)
    for r in reports:
        print(
            f"{r['name'][:18]:<20} "
            f"{r['status']:<6} "
            f"{r['total_used']:>12.4f} "
            f"{r['month_quota']:>12.4f} "
            f"{r['week_quota']:>12.4f} "
            f"{r['today_quota']:>12.4f} "
            f"{r['remain_str']:<14} "
            f"{r['accessed_time']:<20}"
        )
    print("=" * 110)

    total_cum = sum(r["total_used"] for r in reports)
    total_month = sum(r["month_quota"] for r in reports)
    total_today = sum(r["today_quota"] for r in reports)
    print(f"共 {len(reports)} 个 Key  |  累计合计: {total_cum:.4f} 元  |  本月合计: {total_month:.4f} 元  |  今日合计: {total_today:.4f} 元")
    print()


def export_csv(reports, filepath):
    """导出汇总 CSV 对账表"""
    headers = [
        "令牌ID", "令牌名称", "Key(脱敏)", "状态", "分组",
        "累计已用(元)", "本月消耗(元)", "本周消耗(元)", "今日消耗(元)",
        "剩余额度", "创建时间", "最后访问", "过期时间",
    ]
    with open(filepath, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        for r in reports:
            writer.writerow([
                r["id"], r["name"], r["key_masked"], r["status"], r["group"],
                f"{r['total_used']:.4f}",
                f"{r['month_quota']:.4f}",
                f"{r['week_quota']:.4f}",
                f"{r['today_quota']:.4f}",
                r["remain_str"],
                r["created_time"], r["accessed_time"], r["expired_time"],
            ])
    print(f"汇总 CSV 已保存至: {filepath}")


def export_txt(reports, filepath):
    """导出详细 TXT 报告（每个 Key 一节，包含模型分组消耗 + 最近调用记录）"""
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("=" * 80 + "\n")
        f.write("                  多 Key 用量明细报告\n")
        f.write("=" * 80 + "\n")
        f.write(f"报告生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"令牌数量: {len(reports)}\n\n")

        # 总览
        f.write("-" * 80 + "\n")
        f.write("【总览】\n")
        f.write("-" * 80 + "\n")
        total_cum = sum(r["total_used"] for r in reports)
        total_month = sum(r["month_quota"] for r in reports)
        total_week = sum(r["week_quota"] for r in reports)
        total_today = sum(r["today_quota"] for r in reports)
        f.write(f"  累计已用: {total_cum:.4f} 元\n")
        f.write(f"  本月消耗: {total_month:.4f} 元\n")
        f.write(f"  本周消耗: {total_week:.4f} 元\n")
        f.write(f"  今日消耗: {total_today:.4f} 元\n\n")

        # 各 Key 明细
        for idx, r in enumerate(reports, 1):
            f.write("=" * 80 + "\n")
            f.write(f"  [{idx}] {r['name']}\n")
            f.write("=" * 80 + "\n")
            f.write(f"  ID         : {r['id']}\n")
            f.write(f"  Key        : {r['key_masked']}\n")
            f.write(f"  状态       : {r['status']}\n")
            f.write(f"  分组       : {r['group']}\n")
            f.write(f"  累计已用   : {r['total_used']:.4f} 元\n")
            f.write(f"  本月消耗   : {r['month_quota']:.4f} 元\n")
            f.write(f"  本周消耗   : {r['week_quota']:.4f} 元\n")
            f.write(f"  今日消耗   : {r['today_quota']:.4f} 元\n")
            f.write(f"  剩余额度   : {r['remain_str']}\n")
            f.write(f"  创建时间   : {r['created_time']}\n")
            f.write(f"  最后访问   : {r['accessed_time']}\n")
            f.write(f"  过期时间   : {r['expired_time']}\n\n")

            # 按模型分组
            if r["model_stats"]:
                f.write("  --- 近 30 天按模型消耗排行 ---\n")
                for model, s in r["model_stats"].items():
                    f.write(f"    {model:<35} 消耗 {s['quota']:>10.4f} 元  调用 {s['count']:>4} 次  "
                            f"输入 {s['prompt']:>8} token  输出 {s['completion']:>8} token\n")
                f.write("\n")
            else:
                f.write("  近 30 天内无调用记录\n\n")

            # 最近调用记录
            if r["recent_items"]:
                f.write(f"  --- 最近 {len(r['recent_items'])} 条调用记录 ---\n")
                f.write(f"  {'序号':>4}  {'模型':<30} {'消耗(元)':>10} {'输入':>8} {'输出':>8} {'耗时(ms)':>9} {'时间':<20}\n")
                for i, item in enumerate(r["recent_items"], 1):
                    model = (item.get("model_name") or "(未知)")[:28]
                    quota = fmt_money(item.get("quota", 0))
                    prompt = item.get("prompt_tokens", 0)
                    completion = item.get("completion_tokens", 0)
                    use_time = item.get("use_time", 0)
                    created = item.get("created_at", 0)
                    time_str = datetime.fromtimestamp(created).strftime("%Y-%m-%d %H:%M:%S") if created else "N/A"
                    f.write(f"  {i:>4}  {model:<30} {quota:>10.6f} {prompt:>8} {completion:>8} {use_time:>9} {time_str:<20}\n")
                f.write("\n")

        f.write("=" * 80 + "\n")
    print(f"明细 TXT 报告已保存至: {filepath}")


def main():
    # 第一步：获取全部令牌
    print("正在获取令牌列表...")
    tokens = get_all_tokens()
    if not tokens:
        print("没有可统计的令牌")
        return

    # 按名称过滤
    if KEY_NAME_FILTER:
        tokens = [t for t in tokens if KEY_NAME_FILTER in t.get("name", "")]
        print(f"按关键字 '{KEY_NAME_FILTER}' 过滤后剩余 {len(tokens)} 个令牌")

    if not tokens:
        print("过滤后无匹配令牌")
        return

    # 第二步：为每个令牌构建用量报告
    ranges = get_time_ranges()
    reports = []
    for i, token in enumerate(tokens, 1):
        print(f"  [{i}/{len(tokens)}] 正在统计: {token['name']}")
        reports.append(build_key_report(token, ranges))

    # 按本月消耗倒序排列
    reports.sort(key=lambda r: r["month_quota"], reverse=True)

    print()
    print_summary_table(reports)

    # 第三步：导出报告
    script_dir = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
    if EXPORT_CSV:
        export_csv(reports, os.path.join(script_dir, CSV_FILENAME))
    if EXPORT_TXT:
        export_txt(reports, os.path.join(script_dir, TXT_FILENAME))


if __name__ == "__main__":
    main()
```

## 终端输出示例

```text
正在获取令牌列表...
  [1/3] 正在统计: 客户A
  [2/3] 正在统计: 客户B
  [3/3] 正在统计: 内部测试

==============================================================================================================
令牌名称                状态   累计(元)       本月(元)       本周(元)       今日(元)     剩余           最后访问
--------------------------------------------------------------------------------------------------------------
客户A                   启用     1245.6720      224.1485       86.3210       12.4536     无限           2026-05-15 14:32:11
客户B                   启用      856.2310      102.5678       33.1245        2.0815     50.0000 元     2026-05-14 18:09:45
内部测试                启用       12.4536        8.9012        2.1108        0.0000     无限           2026-05-13 09:21:30
==============================================================================================================
共 3 个 Key  |  累计合计: 2114.3566 元  |  本月合计: 335.6175 元  |  今日合计: 14.5351 元

汇总 CSV 已保存至: ./多Key用量汇总.csv
明细 TXT 报告已保存至: ./多Key用量明细报告.txt
```

## CSV 对账表示例

| 令牌ID | 令牌名称 | Key(脱敏) | 状态 | 分组 | 累计已用(元) | 本月消耗(元) | 本周消耗(元) | 今日消耗(元) | 剩余额度 | 创建时间 | 最后访问 | 过期时间 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 51371 | 客户A | sk-qlL6************************xjEX | 启用 | default | 1245.6720 | 224.1485 | 86.3210 | 12.4536 | 无限 | 2026-03-25 21:09:25 | 2026-05-15 14:32:11 | 永不过期 |
| 51276 | 客户B | sk-lEm8************************PoLd | 启用 | default | 856.2310 | 102.5678 | 33.1245 | 2.0815 | 50.0000 元 | 2026-03-25 17:44:34 | 2026-05-14 18:09:45 | 永不过期 |
| 51107 | 内部测试 | sk-A1B2************************Z9Y8 | 启用 | default | 12.4536 | 8.9012 | 2.1108 | 0.0000 | 无限 | 2026-03-25 13:16:47 | 2026-05-13 09:21:30 | 永不过期 |

## TXT 明细报告示例

```text
================================================================================
                  多 Key 用量明细报告
================================================================================
报告生成时间: 2026-05-15 15:00:23
令牌数量: 3

--------------------------------------------------------------------------------
【总览】
--------------------------------------------------------------------------------
  累计已用: 2114.3566 元
  本月消耗: 335.6175 元
  本周消耗: 121.5563 元
  今日消耗: 14.5351 元

================================================================================
  [1] 客户A
================================================================================
  ID         : 51371
  Key        : sk-qlL6************************xjEX
  状态       : 启用
  分组       : default
  累计已用   : 1245.6720 元
  本月消耗   : 224.1485 元
  本周消耗   : 86.3210 元
  今日消耗   : 12.4536 元
  剩余额度   : 无限
  创建时间   : 2026-03-25 21:09:25
  最后访问   : 2026-05-15 14:32:11
  过期时间   : 永不过期

  --- 近 30 天按模型消耗排行 ---
    claude-opus-4-7                     消耗   114.9335 元  调用  139 次  输入      227 token  输出    35910 token
    claude-opus-4-7-cc                  消耗   103.6920 元  调用  176 次  输入   568446 token  输出    69660 token
    doubao-seedream-5.0-lite            消耗     1.9800 元  调用    5 次  输入        5 token  输出    19800 token
    gemini-2.5-flash-image-ssvip        消耗     1.4438 元  调用    9 次  输入     4175 token  输出     6551 token

  --- 最近 20 条调用记录 ---
   序号  模型                             消耗(元)     输入     输出  耗时(ms) 时间
      1  claude-opus-4-7                  3.176290        3        9         6 2026-05-15 14:32:11
      2  claude-opus-4-7                  0.153382        1      182         8 2026-05-15 14:30:03
      3  claude-opus-4-7                  0.438954        1     1335        32 2026-05-15 14:25:54
      ...
================================================================================
```

## 使用说明

1. 将代码中的 `SYSTEM_TOKEN` 和 `USER_ID` 替换为你自己的认证信息。
2. 如果只想统计部分 Key，把这些 Key 在名称上加同样的前缀（如 `客户-A`、`客户-B`），然后将 `KEY_NAME_FILTER` 设为 `客户-`。
3. 运行脚本：`python multi_key_usage.py`。
4. 脚本完成后会在同级目录生成两份文件：
   - `多Key用量汇总.csv`：横向对比表，可直接用 Excel 打开发给客户或财务对账。
   - `多Key用量明细报告.txt`：纵深排查报告，含每个 Key 的模型分组消耗与最近调用记录。

## 注意事项

- 接口的额度单位为 `quota` 原始值，**人民币金额 = quota / 500000**，脚本已自动换算。
- 若令牌设置为「无限额度」，剩余额度显示为「无限」，CSV 同样按字符串展示，便于对账。
- "本月"指最近 30 天滚动窗口，"本周"指最近 7 天滚动窗口，并非自然月/自然周。如需自然月统计，可自行修改 `get_time_ranges()` 函数。
- 调用次数与令牌数量呈线性关系（每个 Key 需要 3~4 次 API 请求），令牌数较多时（例如超过 50 个）建议分批运行或加入 `time.sleep()` 控制频率。
- 所有"按 Key 筛选"都依赖 `token_name` 字段，**令牌重名时统计会出现合并**。请确保分发时每个令牌的名称唯一。
- 若 Key 在统计周期内无任何调用，分时段消耗显示为 `0.0000`，属正常情况。

<p align="center">
  <small>© 2026 DMXAPI 多 Key 用量监控</small>
</p>
