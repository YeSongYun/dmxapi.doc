# gpt-image-2.6 文生图 API 使用文档

通过 `/v1/images/generations` 接口提交文本提示词，使用 `gpt-image-2.6-sunburst` 或 `gpt-image-2.6-flare` 生成图片。
## 接口地址
| 接口 | 请求方式 | URL |
|------|---------|-----|
| 文生图 | POST | `https://www.dmxapi.cn/v1/images/generations` |
:::warning
请妥善保管 DMXAPI API Key，勿在前端代码、公开仓库或日志中暴露。运行前，将示例中 `api_key` 引号内的星号占位内容替换为你的完整 API 令牌。
:::

## 模型名称

| 模型 ID | 官方定位 | 使用选择 |
|------|------|------|
| `gpt-image-2.6-sunburst-ssvip` | 原价模型稳定性高 | 更关注最终编辑效果与细节时选用 |
| `gpt-image-2.6-flare-ssvip` | 原价模型稳定性高 | 更关注编辑速度时选用 |
| `gpt-image-2.6-sunburst` | 以图像质量为重点的基础模型 | 更关注最终编辑效果与细节时选用 |
| `gpt-image-2.6-flare` | 以生成速度为重点的小模型 | 更关注编辑速度时选用 |

## 文生图示例代码

```python
import base64
from datetime import datetime
from pathlib import Path

import requests

# API 配置
url = "https://www.dmxapi.cn/v1/images/generations"
api_key = "sk-*****************************************"  # 在引号内粘贴完整 API 令牌

# 请求头：JSON 请求体 + Bearer 鉴权
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}",
}

# 请求参数
# 新特性备注基于 2026-11-05 对 DMXAPI 两款 2.6 模型的实际请求结果
payload = {
    # 【model】(string, 必填) 使用的图像生成模型名称
    # 可选值:
    #   "gpt-image-2.6-sunburst"  (以图像质量为重点的基础模型，示例默认)
    #   "gpt-image-2.6-flare"     (以生成速度为重点的小模型)
    "model": "gpt-image-2.6-sunburst",

    # 【prompt】(string, 必填) 期望生成图像的文本描述
    # GPT image 系列模型最大长度 32000 字符
    # 描述越具体、越场景化，生成效果越接近预期
    "prompt": "赛博朋克城市雨夜，霓虹招牌特写，电影画幅",

    # 【n】(integer, 可选) 单次请求生成图像的张数
    # 取值范围: [1, 10]，默认值为 1
    "n": 1,

    # 【size】(string, 可选) 生成图像的分辨率，格式为 "宽x高"
    # GPT image 系列常用尺寸:
    #   "auto"       (自动选择最佳尺寸，默认值)
    #   "1024x1024"  (正方形)
    #   "1536x1024"  (横版/landscape)
    #   "1024x1536"  (竖版/portrait)
    #   "2048x2048"  (2K/方形1:1)
    #   "2048x1152"  (2K/横版16:9)
    #   "3840x2160"  (4K/横版16:9)
    #   "2160x3840"  (4K/竖版9:16)
    # 自定义约束: 宽高必须都是 16 的倍数；长短边比不能超过 3:1
    #   最大边长 <= 3840px；总像素在 655,360 到 8,294,400 之间
    # GIF 的 size 是每一帧的尺寸，官方示例为 512x512；帧数、帧尺寸和 n 必须同时落在模型限制与总像素预算内
    # 使用 auto 可让 API 在 GIF 限制范围内选择帧尺寸
    "size": "1024x1024",

    # 【output_format】(string, 可选) 指定输出文件格式
    # 可选值: "png"(默认) / "jpeg" / "webp" / "gif"(2.6 动画，文生图和图片编辑都支持) / "svg"(仅文生图)
    # 若选择 jpeg 或 webp，可再配合 output_compression 调整压缩率
    # GIF 不支持 streaming、partial images、mask、output_compression
    # SVG 仅支持文生图，要求 n=1；不支持 streaming、partial images、prompt_rewriter、output_compression
    # 官方规则：渠道开启 SVG model selection 时必须传 svg.model，未开启时不要传 svg 对象
    # 当前渠道已开启，只传 output_format=svg 会返回 400，参数为 svg.model
    # svg.model 是编写 SVG 的语言模型，顶层 model 只生成参考图
    # GIF 请在 prompt 中描述主体、动作与循环方式
    "output_format": "png",

    # 【svg】(object) output_format 为 svg 时由 main() 自动补上，不必手写
    # 需要换作者模型时再取消注释；reasoning.effort 可选：none / minimal / low / medium / high / xhigh / max
    # "svg": {"model": "gpt-6.1-sol", "reasoning": {"effort": "low"}},

    # 【frame_count】(integer, 可选) 仅 output_format 为 gif 时使用
    # 取值范围: 2 <= x <= 16，省略时默认 9
    # "frame_count": 9,

    # 【frame_duration_ms】(integer, 可选) 仅 output_format 为 gif 时使用
    # 指南范围: 20 <= x <= 2000，按 10ms 取整，默认 200
    # API reference 另将编码延迟上限记为 655350ms
    # "frame_duration_ms": 200,

    # 【quality】(string, 可选) 生成图像的质量等级
    # 可选值:
    #   "auto"      (自动选择最佳质量，默认值)
    #   "low"       (低质量，生成更快成本更低，适合草稿与快速迭代)
    #   "medium"    (中等质量)
    #   "high"      (高质量)
    #   "xhigh"     (超高质量)
    #   "max"       (最高质量，耗时与成本最高)
    "quality": "high",

    # 【complexity】(string, 可选) 2.6 新增：为控制渲染前的规划投入
    # 可选值:
    #   "low"       (较少规划，适合简单构图与快速迭代)
    #   "medium"    (中等规划投入)
    #   "high"      (更多规划，适合复杂布局与多条件提示词，默认值)
    # 与 quality 独立：complexity 控制规划投入，quality 控制渲染细节
    "complexity": "high",

    # 【output_compression】(integer, 可选) 输出压缩率
    # 仅在 output_format 为 jpeg 或 webp 时使用
    # 取值范围: 0 <= x <= 100，默认 100
    # PNG 输出不需要该参数，保持注释即可
    # "output_compression": 100,

    # 【moderation】(string, 可选) 内容审核强度
    # 可选值: "auto"(默认) / "low"(更宽松，不表示关闭审核)
    "moderation": "low",

    # 【background】(string, 可选) 输出图像的背景模式
    # 可选值:
    #   "auto"         (自动选择背景，默认值)
    #   "opaque"       (不透明背景)
    #   "transparent"  (透明背景；静态位图请选择 png 或 webp)
    "background": "auto",
}


def main():
    body = dict(payload)

    # 发起同步请求；图片生成耗时较长，timeout 给足
    response = requests.post(url, headers=headers, json=body, timeout=1000)
    print("status:", response.status_code)
    response.raise_for_status()

    # 解析响应 JSON；非 JSON 通常是渠道或网关报错
    try:
        result = response.json()
    except ValueError as exc:
        raise RuntimeError("接口未返回有效 JSON，请检查响应与渠道配置") from exc

    # 图片结果位于 data 数组，每个元素对应一张图
    items = result.get("data") if isinstance(result, dict) else None
    if not isinstance(items, list) or not items:
        raise RuntimeError("响应中没有非空 data 数组")

    # 按 output_format 决定保存扩展名（jpeg 统一写成 .jpg）
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    extension = payload.get("output_format", "png").lower()
    if extension == "jpeg":
        extension = "jpg"

    for index, item in enumerate(items, start=1):
        if not isinstance(item, dict):
            raise RuntimeError(f"第 {index} 个图片结果不是对象")
        if item.get("b64_json"):
            # 上游 GPT Image 默认返回 Base64 图片，优先解码
            image_bytes = base64.b64decode(item["b64_json"], validate=True)
        elif item.get("url"):
            # 沿用 DMXAPI 参考页的兼容分支，不表示官方模型保证返回 URL
            download = requests.get(item["url"], timeout=120)
            download.raise_for_status()
            image_bytes = download.content
        else:
            raise RuntimeError(f"第 {index} 个图片结果缺少有效图片内容")

        # 以时间戳 + 序号命名，写入当前工作目录
        output_path = Path(f"output_{timestamp}_{index}.{extension}")
        output_path.write_bytes(image_bytes)
        print(f"saved {output_path}")


if __name__ == "__main__":
    main()
```
## 返回示例
```text
status: 200
saved output_20261105_153823_1.png
```
<p align="center">
  <small>© 2026 DMXAPI gpt-image-2.6 文生图</small>
</p>
