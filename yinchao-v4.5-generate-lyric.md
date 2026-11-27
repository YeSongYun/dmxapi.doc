# yinchao-v4.5 独立作词 API 使用文档

在 `prompt` 中描述歌词主题、曲风或段落结构，接口会在本次请求中返回歌词 `lyric`。如果同时生成了歌名，响应中还会包含 `title`。

## 接口地址

| 接口 | 请求方式 | URL |
| --- | --- | --- |
| 独立作词 | POST | `https://www.dmxapi.cn/yinchao/api/v1/lyric/generate` |

## 模型名称

`yinchao-v4.5`

## 独立作词示例代码


```python
import requests
import json
from pathlib import Path

# ===============================================================
# 步骤1: 配置 API 连接信息
# ===============================================================

url = "https://www.dmxapi.cn/yinchao/api/v1/lyric/generate"
api_key = "sk-******************************************"  # 填写自己的 DMXAPI 密钥
output_path = Path("输出/yinchao-v4.5/歌词.txt")  # 歌词保存位置

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
    # 【prompt】(string, 必填) 歌词主题、风格或段落结构，1 至 2000 个字符。
    "prompt": "为一首中速灵魂乐写中文歌词，描写清晨的第一班渡轮，主歌由一人演唱，副歌适合两人合唱。",

    # 【model】(string, 可选) 网关默认使用 yinchao-v4.5。
    "model": "yinchao-v4.5",
}

# ===============================================================
# 步骤4: 发送请求并输出结果
# ===============================================================

def main():
    response = requests.post(url, headers=headers, json=payload)
    if not response.ok:
        print(response.text)
        response.raise_for_status()

    result = response.json()
    print(json.dumps(result, indent=2, ensure_ascii=False))
    lyric = result["lyric"]
    title = result.get("title")
    text = f"{title}\n\n{lyric}" if title else lyric
    # 同时把歌词保存到步骤 1 配置的 output_path
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
```

## 独立作词返回示例

下面是一次真实请求的原始返回，`usage.cost` 是网关按站点价格给出的本次费用。

```json
{
  "lyric": "[intro]\n[verse]\n天还没亮透 码头灯发黄\n我手里攥着 一张旧船票\n铁链在响 水面起白雾\n对岸的烟囱 刚刚才醒来\n\n[prechorus]\n船笛低低唤 像谁在答应\n我把围巾拉紧 走上跳板\n\n[chorus]\n第一班渡轮 载着未醒的城\n你在船尾 我在船头相望\n第一班渡轮 划开灰蓝的早晨\n把昨夜的沉默 留在岸上\n\n[verse]\n穿工装的人 靠着栏杆打盹\n卖报的少年 数着零钱轻哼\n你拎着热豆浆 从下层走上来\n递给我一杯 说不必客气\n\n[prechorus]\n船身轻轻晃 像一句承诺\n天边慢慢亮 照见彼此脸庞\n\n[chorus]\n第一班渡轮 载着未醒的城\n你在船尾 我在船头相望\n第一班渡轮 划开灰蓝的早晨\n把昨夜的沉默 留在岸上\n\n[bridge]\n手里的豆浆 暖得刚好\n你问我今天 要往哪儿去\n我说不管哪儿 只要有这趟船\n多绕一段 也不算远\n\n[chorus]\n第一班渡轮 载着赶路的人\n你在身旁 我们一起哼唱\n第一班渡轮 划开灰蓝的早晨\n把昨夜的沉默 留在岸上\n\n[outro]",
  "title": "第一班渡轮",
  "usage": {
    "cost": "¥0.07"
  }
}
```



<p align="center">
  <small>© 2026 DMXAPI yinchao-v4.5 独立作词</small>
</p>
