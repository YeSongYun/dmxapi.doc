# yinchao-v3.5 独立作词 API 使用文档

在 `prompt` 中描述歌词主题、曲风或段落结构，接口会在本次请求中返回歌词 `lyric`。如果同时生成了歌名，响应中还会包含 `title`。

## 接口地址

| 接口 | 请求方式 | URL |
| --- | --- | --- |
| 独立作词 | POST | `https://www.dmxapi.cn/yinchao/api/v1/lyric/generate` |

## 模型名称

`yinchao-v3.5`

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
output_path = Path("输出/yinchao-v3.5/歌词.txt")  # 歌词保存位置

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
    "prompt": "写一首关于坐末班车回家的中文民谣歌词，分主歌和副歌，副歌以“留一盏灯”收尾。",

    # 【model】(string, 可选) 省略时网关默认使用 yinchao-v4.5，使用 v3.5 作词请保留此值。
    "model": "yinchao-v3.5",
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
  "lyric": "[intro]\n[verse]\n打卡机吐出最后一声\n电梯沉到底 整层楼都关了灯\n便利店暖气扑在脸上\n买一罐咖啡 捂热冻红的掌心\n[prechorus]\n站牌下只剩我和影子\n风把围巾吹成一截尾巴\n[chorus]\n末班车摇摇晃晃载着晚归的人\n车窗上贴着一张张疲倦的脸\n穿过空荡的街 穿过熄了的店\n到我家巷口 别忘了留一盏灯\n[verse]\n前排的人抱着纸箱打盹\n后排的人翻着接不完的消息\n报站声忽近忽远像一句叹息\n我数着窗外的门牌 一站一站靠近\n[prechorus]\n巷子深处有咳嗽声传来\n哪扇窗还醒着 替夜班的人等\n[chorus]\n末班车摇摇晃晃载着晚归的人\n车窗上贴着一张张疲倦的脸\n穿过空荡的街 穿过熄了的店\n到我家巷口 别忘了留一盏灯\n[bridge]\n我想起出门时没关的台灯\n妈妈发来的话还亮在屏幕里\n说回来了就热一热锅里的饭\n门别怕 手扶着墙慢慢推开\n[chorus]\n末班车摇摇晃晃载着晚归的人\n这一次我听见巷口有脚步声\n穿过安静的路 穿过睡了的天\n有人还在窗边 一直留着那盏灯\n[outro]",
  "title": "末班车口的灯",
  "usage": {
    "cost": "¥0.07"
  }
}
```


<p align="center">
  <small>© 2026 DMXAPI yinchao-v3.5 独立作词</small>
</p>
