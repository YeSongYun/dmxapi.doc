# 模型周期消耗统计
使用该接口将返回当天(或自定义时间周期)的模型用量统计

## 请求地址
`https://www.dmxapi.cn/api/data/self`

:::tip 注意
系统令牌在工作台->个人设置->更多选项->生成系统访问令牌获取  
:::

## 示例代码
```python
"""
================================================================================
DMXAPI 模型用量查询工具
================================================================================

功能说明:
    查询指定时间范围内的模型调用消耗数据，并以表格形式展示。

使用方法:
    1. 将 SYSTEM_TOKEN 替换为你的系统令牌
    2. 将 USER_ID 替换为你的用户 ID（在个人设置中获取）
    3. 设置查询时间范围（可选）:
       - START_TIME: 开始时间，格式 "2025-12-09 11:00"，留空则默认今天零点
       - END_TIME: 结束时间，格式 "2025-12-09 15:00"，留空则默认当前时间
    4. 运行脚本: python test.py

================================================================================
"""

import requests
from datetime import datetime

# ============================================================================
# 配置信息
# ============================================================================

# API 接口地址
URL = "https://www.dmxapi.cn/api/data/self"

# 认证信息 - 请替换为你自己的信息
SYSTEM_TOKEN = "*************************************"  # 系统令牌，用于身份验证
USER_ID = "*****"                                  # 用户 ID，在「个人设置」中获取

# ----------------------------------------------------------------------------
# 查询时间范围配置（可选）
# ----------------------------------------------------------------------------
# 格式: "YYYY-MM-DD HH:MM"，例如 "2025-12-09 11:00"
# 留空 "" 则使用默认值:
#   - START_TIME 为空: 默认为今天 00:00
#   - END_TIME 为空: 默认为当前时间
# ----------------------------------------------------------------------------
START_TIME = ""  # 开始时间，例如: "2025-12-09 11:00"
END_TIME = ""    # 结束时间，例如: "2025-12-09 15:00"


# ============================================================================
# 核心函数
# ============================================================================

def parse_time(time_str: str) -> int:
    """
    将时间字符串解析为时间戳

    Args:
        time_str (str): 时间字符串，格式 "YYYY-MM-DD HH:MM"

    Returns:
        int: Unix 时间戳（秒级）
    """
    return int(datetime.strptime(time_str, "%Y-%m-%d %H:%M").timestamp())


def get_model_usage(start_timestamp: int, end_timestamp: int, default_time: str = "day"):
    """
    获取模型消耗分布数据

    通过调用 DMXAPI 接口，查询指定时间范围内的模型调用记录。

    Args:
        start_timestamp (int): 查询开始时间戳（秒级）
        end_timestamp (int): 查询结束时间戳（秒级）
        default_time (str): 时间粒度，可选值:
                            - "day": 按天统计（默认）
                            - "hour": 按小时统计

    Returns:
        list: 包含模型使用数据的字典列表，每个字典包含:
              - model_name: 模型名称
              - quota: 消耗额度
              - date: 格式化后的日期时间
    """
    # 构建请求头
    headers = {
        "Accept": "application/json",
        "Authorization": f"{SYSTEM_TOKEN}",  # Token 认证
        "Rix-Api-User": USER_ID,                    # 用户标识
    }

    # 构建查询参数
    params = {
        "start_timestamp": start_timestamp,
        "end_timestamp": end_timestamp,
        "default_time": default_time
    }

    # 发送 GET 请求
    response = requests.get(URL, headers=headers, params=params)

    # 检查 HTTP 状态码
    if response.status_code != 200:
        print(f"请求失败: {response.status_code}")
        return []

    # 解析 JSON 响应
    result = response.json()

    # 检查业务状态
    if not result.get("success"):
        print(f"接口返回错误: {result.get('message')}")
        return []

    # 提取并格式化数据
    data = []
    for item in result.get("data", []):
        data.append({
            "model_name": item.get("model_name"),          # 模型名称
            "quota": item.get("quota"),                    # 消耗额度（原始值）
            "date": datetime.fromtimestamp(               # 格式化时间戳
                item.get("created_at")
            ).strftime("%Y-%m-%d %H:%M")
        })

    return data


def get_display_width(text: str) -> int:
    """
    计算字符串的显示宽度（中文字符占2个宽度）

    Args:
        text (str): 输入字符串

    Returns:
        int: 显示宽度
    """
    width = 0
    for char in text:
        # 中文字符及全角字符占2个宽度
        if '\u4e00' <= char <= '\u9fff' or '\u3000' <= char <= '\u303f' or '\uff00' <= char <= '\uffef':
            width += 2
        else:
            width += 1
    return width


def pad_to_width(text: str, width: int) -> str:
    """
    将字符串填充到指定的显示宽度

    Args:
        text (str): 输入字符串
        width (int): 目标显示宽度

    Returns:
        str: 填充后的字符串
    """
    current_width = get_display_width(text)
    padding = width - current_width
    return text + ' ' * max(0, padding)


def print_usage(data: list):
    """
    格式化输出模型使用数据

    以表格形式打印查询结果，额度值会除以 500000 转换为美元单位。

    Args:
        data (list): get_model_usage() 返回的数据列表
    """
    if not data:
        print("没有数据")
        return

    # 定义列宽
    col_model = 40   # 模型名称列宽
    col_quota = 10   # 额度列宽
    col_date = 18    # 日期列宽

    # 打印表头
    header_model = pad_to_width("模型名称", col_model)
    header_quota = "额度".rjust(col_quota)
    header_date = pad_to_width("日期", col_date)
    print(f"{header_model} {header_quota} {header_date}")
    print("-" * (col_model + col_quota + col_date + 2))

    # 打印数据行（额度除以 500000 转换单位）
    for item in data:
        model_name = pad_to_width(item['model_name'], col_model)
        quota = f"{item['quota'] / 500000:>12.4f}"
        date = pad_to_width(item['date'], col_date)
        print(f"{model_name} {quota} {date}")


# ============================================================================
# 主程序入口
# ============================================================================

if __name__ == "__main__":
    import time

    # ------------------------------------------------------------------------
    # 设置查询时间范围
    # ------------------------------------------------------------------------

    # 解析开始时间：如果配置了 START_TIME 则使用，否则默认今天零点
    if START_TIME:
        start_timestamp = parse_time(START_TIME)
    else:
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        start_timestamp = int(today.timestamp())

    # 解析结束时间：如果配置了 END_TIME 则使用，否则默认当前时间
    if END_TIME:
        end_timestamp = parse_time(END_TIME)
    else:
        end_timestamp = int(time.time())

    # ------------------------------------------------------------------------
    # 执行查询并输出结果
    # ------------------------------------------------------------------------

    print(f"查询时间范围: {datetime.fromtimestamp(start_timestamp)} 至 {datetime.fromtimestamp(end_timestamp)}")
    print()

    # 调用 API 获取数据
    data = get_model_usage(start_timestamp, end_timestamp)

    # 格式化输出结果
    print_usage(data)

```
## 返回示例
```json
查询时间范围: 2025-12-09 00:00:00 至 2025-12-09 15:48:05

模型名称                                         额度 日期
----------------------------------------------------------------------
claude-opus-4-5-20251101                       0.1883 2025-12-09 11:00
claude-opus-4-5-20251101-cc                   12.0887 2025-12-09 12:00
claude-opus-4-5-20251101-cc                    4.6873 2025-12-09 14:00
claude-opus-4-5-20251101                       0.0306 2025-12-09 14:00
qwen-max-latest                                0.0001 2025-12-09 15:00
claude-opus-4-5-20251101-cc                    4.8696 2025-12-09 15:00
```