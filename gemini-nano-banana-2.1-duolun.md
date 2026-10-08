# Gemini Nano Banana 2.1 多轮图片修改 API 文档

Gemini Nano Banana 2.1 支持通过多轮对话生成并持续调整图片。你可以先描述画面生成初稿，再基于完整对话历史修改背景、文字、配色或人物细节。本文使用 DMXAPI 兼容的 Gemini 原生调用格式，演示“生成图片 → 保存历史 → 多轮修改”的完整流程。

:::tip 多轮一致性升级
Google 官方说明，Nano Banana 2.1 改善了多轮角色一致性、提示遵循及文字呈现；支持 1K / 2K / 4K 分辨率和 `minimal` / `medium` / `high` 思考等级，默认 `medium`。
:::

## 接口地址

```
https://www.dmxapi.cn/v1beta/models/gemini-nano-banana-2.1:generateContent
```
:::warning 注意
请妥善保管 DMXAPI API Key，不要将真实密钥提交到公开仓库。示例需要安装 `requests`。历史文件包含原图数据和对话内容，请按需要在本地保存。
:::

## 模型名称

### Gemini Nano Banana 2.1

- **模型名称**：`gemini-nano-banana-2.1`
- **别名**：Nano Banana 2.1
- **特点**：支持多轮对话式图片修改，每轮结合历史内容继续调整。
- **配置**：支持 1K / 2K / 4K 分辨率，不支持 512；思考等级默认 `medium`。
## 示例代码
::: code-group

```python [生成图片]
"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║            DMXAPI 多轮图片修改 (gemini-nano-banana-2.1 · 生成图片)             ║
║                                                                               ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║  功能说明:                                                                    ║
║  ────────                                                                     ║
║    • 使用 requests 库直接调用 DMXAPI 的 Gemini 原生兼容接口                   ║
║    • 首轮文生图，并保存完整对话历史供后续轮次使用                             ║
║    • 生成的图片自动保存到 output 文件夹                                       ║
║    • 本脚本会新建并覆盖历史文件，之后请运行「多轮修改」脚本                   ║
║                                                                               ║
║  使用模型: gemini-nano-banana-2.1                                             ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""

# ══════════════════════════════════════════════════════════════════════════════
#                                    依赖导入                                   
# ══════════════════════════════════════════════════════════════════════════════
import requests                # HTTP 请求库，用于调用 API 接口
import base64                  # Base64 编解码，用于处理图片数据
import json                    # JSON 编解码，用于读写对话历史文件
from datetime import datetime  # 日期时间处理，用于生成带时间戳的文件名
from pathlib import Path       # 文件路径处理，用于创建输出目录、保存图片

# 提示: 请先安装依赖: pip install requests

# ══════════════════════════════════════════════════════════════════════════════
#                                    API 配置                                   
# ══════════════════════════════════════════════════════════════════════════════
API_KEY = "sk-****************************************"  # DMXAPI 密钥，请替换为你自己的密钥
BASE_URL = "https://www.dmxapi.cn/v1beta"                # DMXAPI 基础地址
MODEL_NAME = "gemini-nano-banana-2.1"                    # 模型名称，可按需修改 (多轮调用必须使用相同模型)

# 完整的 API 端点由基础地址和模型名称拼接而成，无需手动填写完整地址
API_URL = f"{BASE_URL}/models/{MODEL_NAME}:generateContent"

# 完整对话历史文件，首轮生成和后续多轮修改共用同一个文件
HISTORY_PATH = Path("base64_data/history.json")

# ══════════════════════════════════════════════════════════════════════════════
#                                HTTP 请求头配置                                
# ══════════════════════════════════════════════════════════════════════════════
headers = {
    "x-goog-api-key": API_KEY,           # 身份验证: Gemini 原生格式的密钥请求头
    "Content-Type": "application/json",  # 内容类型: JSON 数据格式
}

# ══════════════════════════════════════════════════════════════════════════════
#                                  构建请求参数                                 
# ══════════════════════════════════════════════════════════════════════════════
user_content = {
    # 【必填】role: 当前输入来自用户
    "role": "user",
    # 【必填】parts[].text: 首轮生成提示词
    "parts": [{"text": "一只可爱的小猫在愉快地玩耍。"}],
}

payload = {
    # 【必填】contents: 首轮只包含用户输入
    "contents": [user_content],

    # generationConfig: 生成配置 (HTTP JSON 使用驼峰命名)
    "generationConfig": {
        # responseModalities: 设置返回内容的类型
        # - 多轮场景同时返回文字和图片，文字部分也可能携带思考签名
        "responseModalities": ["TEXT", "IMAGE"],

        # imageConfig: 图片输出配置
        "imageConfig": {
            # aspectRatio: 设置输出图片的宽高比
            #
            # ┌────────────────────────────────────────────────────────────┐
            # │ gemini-nano-banana-2.1                                     │
            # ├──────────┬─────────────┬────────┬─────────────┬────────────┤
            # │ 宽高比   │ 1K 分辨率   │ 1K令牌 │ 2K 分辨率   │ 4K 分辨率  │
            # ├──────────┼─────────────┼────────┼─────────────┼────────────┤
            # │ 1:1      │ 1024x1024   │ 1120   │ 2048x2048   │ 4096x4096  │
            # │ 1:4      │ 512x2048    │ 1120   │ 1024x4096   │ 2048x8192  │
            # │ 1:8      │ 384x3072    │ 1120   │ 768x6144    │ 1536x12288 │
            # │ 2:3      │ 848x1264    │ 1120   │ 1696x2528   │ 3392x5056  │
            # │ 3:2      │ 1264x848    │ 1120   │ 2528x1696   │ 5056x3392  │
            # │ 3:4      │ 896x1200    │ 1120   │ 1792x2400   │ 3584x4800  │
            # │ 4:1      │ 2048x512    │ 1120   │ 4096x1024   │ 8192x2048  │
            # │ 4:3      │ 1200x896    │ 1120   │ 2400x1792   │ 4800x3584  │
            # │ 4:5      │ 928x1152    │ 1120   │ 1856x2304   │ 3712x4608  │
            # │ 5:4      │ 1152x928    │ 1120   │ 2304x1856   │ 4608x3712  │
            # │ 8:1      │ 3072x384    │ 1120   │ 6144x768    │ 12288x1536 │
            # │ 9:16     │ 768x1376    │ 1120   │ 1536x2752   │ 3072x5504  │
            # │ 16:9     │ 1376x768    │ 1120   │ 2752x1536   │ 5504x3072  │
            # │ 21:9     │ 1584x672    │ 1120   │ 3168x1344   │ 6336x2688  │
            # └──────────┴─────────────┴────────┴─────────────┴────────────┘
            # 注: 1K/2K/4K令牌分别为1120/1680/3780
            "aspectRatio": "1:1",

            # imageSize: 设置输出图片的分辨率
            # - "1K": 1K 分辨率 (默认值)
            # - "2K": 2K 分辨率
            # - "4K": 4K 分辨率
            # 注意: K 必须大写，不能写成 1k；本模型不支持 512
            "imageSize": "1K",
        },

        # thinkingConfig: 思考等级配置 (思考过程默认启用，无法完全关闭)
        "thinkingConfig": {
            # thinkingLevel: 生成图片前的思考深度
            # - "MINIMAL": 较少思考，速度最快
            # - "MEDIUM":  均衡模式 (默认值)
            # - "HIGH":    深度思考，复杂画面质量更稳定
            "thinkingLevel": "MEDIUM",
        },
    },

    # tools: Google 搜索工具（可选）
    # - 使用实时信息生成图像（如根据最新资讯添加元素等）
    # "tools": [{"google_search": {}}]
    #
    # 本模型同时支持 Image Search（图片搜索）：
    # "tools": [{"google_search": {"search_types": {"web_search": {}, "image_search": {}}}}]
}

# ══════════════════════════════════════════════════════════════════════════════
#                                   主程序执行                                  
# ══════════════════════════════════════════════════════════════════════════════
# ┌─────────────────────────────────────────────────────────────────────────┐
# │ 步骤 1: 发送 API 请求                                                   │
# │         向 DMXAPI 发送 POST 请求，地址由 BASE_URL 和 MODEL_NAME 拼接    │
# └─────────────────────────────────────────────────────────────────────────┘
response = requests.post(API_URL, headers=headers, json=payload)
response.raise_for_status()  # 检查 HTTP 状态码，若有错误则抛出异常
result = response.json()

# 响应中没有候选结果时直接报错，便于排查问题
if not result.get("candidates"):
    raise ValueError(f"响应中没有候选结果：{result}")

# ┌─────────────────────────────────────────────────────────────────────────┐
# │ 步骤 2: 保存完整对话历史                                                │
# │         原样保存模型 content，不丢弃文字、图片、思考部分或签名          │
# └─────────────────────────────────────────────────────────────────────────┘
model_content = result["candidates"][0]["content"]
history = [user_content, model_content]

HISTORY_PATH.parent.mkdir(exist_ok=True)
HISTORY_PATH.write_text(
    json.dumps(history, ensure_ascii=False, indent=2),
    encoding="utf-8",
)

# ┌─────────────────────────────────────────────────────────────────────────┐
# │ 步骤 3: 保存本轮生成的图片                                              │
# │         保存最终图片时跳过 thought=true 的部分；历史中的这些部分仍然保留│
# └─────────────────────────────────────────────────────────────────────────┘
output_dir = Path("output")
output_dir.mkdir(exist_ok=True)

for part in model_content.get("parts", []):
    if part.get("thought"):
        continue

    # 文字片段直接打印
    if "text" in part:
        print(part["text"])

    # 图片片段 (inlineData 内嵌 Base64 图片数据)
    elif "inlineData" in part:
        image = part["inlineData"]

        # 按返回的 MIME 类型确定文件扩展名 (image/png -> png)
        extension = image["mimeType"].split("/")[-1]

        # 生成带时间戳的文件名，格式: generated_image_20261008_120000.png
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"output/generated_image_{timestamp}.{extension}"

        # 解码 Base64 数据并写入图片文件
        Path(filename).write_bytes(base64.b64decode(image["data"]))

        # 输出保存成功的提示信息
        print(f"图片已保存到 {filename}")

print(f"完整对话历史已保存到 {HISTORY_PATH}")
```

```python [多轮修改]
"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║            DMXAPI 多轮图片修改 (gemini-nano-banana-2.1 · 多轮修改)             ║
║                                                                               ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║  功能说明:                                                                    ║
║  ────────                                                                     ║
║    • 使用 requests 库直接调用 DMXAPI 的 Gemini 原生兼容接口                   ║
║    • 读取首轮保存的完整对话历史，在历史基础上继续修改图片                     ║
║    • 本轮的输入和输出会追加回历史文件，可反复运行持续调整                     ║
║    • 修改后的图片自动保存到 output 文件夹                                     ║
║                                                                               ║
║  使用模型: gemini-nano-banana-2.1                                             ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""

# ══════════════════════════════════════════════════════════════════════════════
#                                    依赖导入                                   
# ══════════════════════════════════════════════════════════════════════════════
import requests                # HTTP 请求库，用于调用 API 接口
import base64                  # Base64 编解码，用于处理图片数据
import json                    # JSON 编解码，用于读写对话历史文件
from datetime import datetime  # 日期时间处理，用于生成带时间戳的文件名
from pathlib import Path       # 文件路径处理，用于创建输出目录、保存图片

# 提示: 请先安装依赖: pip install requests

# ══════════════════════════════════════════════════════════════════════════════
#                                    API 配置                                   
# ══════════════════════════════════════════════════════════════════════════════
API_KEY = "sk-****************************************"  # DMXAPI 密钥，请替换为你自己的密钥
BASE_URL = "https://www.dmxapi.cn/v1beta"                # DMXAPI 基础地址
MODEL_NAME = "gemini-nano-banana-2.1"                    # 模型名称，可按需修改 (多轮调用必须使用相同模型)

# 完整的 API 端点由基础地址和模型名称拼接而成，无需手动填写完整地址
API_URL = f"{BASE_URL}/models/{MODEL_NAME}:generateContent"

# 完整对话历史文件，首轮生成和后续多轮修改共用同一个文件
HISTORY_PATH = Path("base64_data/history.json")

# ══════════════════════════════════════════════════════════════════════════════
#                                HTTP 请求头配置                                
# ══════════════════════════════════════════════════════════════════════════════
headers = {
    "x-goog-api-key": API_KEY,           # 身份验证: Gemini 原生格式的密钥请求头
    "Content-Type": "application/json",  # 内容类型: JSON 数据格式
}

# ══════════════════════════════════════════════════════════════════════════════
#                                  构建请求参数                                 
# ══════════════════════════════════════════════════════════════════════════════
# 读取已有完整历史，保留各个 parts 的内容、顺序、MIME 类型和签名
# 注意: 请先运行「生成图片」脚本创建历史文件
history = json.loads(HISTORY_PATH.read_text(encoding="utf-8"))

user_content = {
    # 【必填】role: 当前轮的用户输入
    "role": "user",
    # 【必填】parts[].text: 基于上一轮结果提出修改要求
    "parts": [{
        "text": "给这只小猫加一顶红色帽子，帽子上写着 Jonathan，保持小猫外貌和背景不变。",
    }],
}

payload = {
    # 【必填】contents: 全部历史 + 当前用户输入
    "contents": [*history, user_content],

    # generationConfig: 生成配置 (HTTP JSON 使用驼峰命名)
    "generationConfig": {
        # responseModalities: 设置返回内容的类型
        # - 多轮场景同时返回文字和图片，文字部分也可能携带思考签名
        "responseModalities": ["TEXT", "IMAGE"],

        # imageConfig: 图片输出配置
        "imageConfig": {
            # aspectRatio: 设置输出图片的宽高比
            #
            # ┌────────────────────────────────────────────────────────────┐
            # │ gemini-nano-banana-2.1                                     │
            # ├──────────┬─────────────┬────────┬─────────────┬────────────┤
            # │ 宽高比   │ 1K 分辨率   │ 1K令牌 │ 2K 分辨率   │ 4K 分辨率  │
            # ├──────────┼─────────────┼────────┼─────────────┼────────────┤
            # │ 1:1      │ 1024x1024   │ 1120   │ 2048x2048   │ 4096x4096  │
            # │ 1:4      │ 512x2048    │ 1120   │ 1024x4096   │ 2048x8192  │
            # │ 1:8      │ 384x3072    │ 1120   │ 768x6144    │ 1536x12288 │
            # │ 2:3      │ 848x1264    │ 1120   │ 1696x2528   │ 3392x5056  │
            # │ 3:2      │ 1264x848    │ 1120   │ 2528x1696   │ 5056x3392  │
            # │ 3:4      │ 896x1200    │ 1120   │ 1792x2400   │ 3584x4800  │
            # │ 4:1      │ 2048x512    │ 1120   │ 4096x1024   │ 8192x2048  │
            # │ 4:3      │ 1200x896    │ 1120   │ 2400x1792   │ 4800x3584  │
            # │ 4:5      │ 928x1152    │ 1120   │ 1856x2304   │ 3712x4608  │
            # │ 5:4      │ 1152x928    │ 1120   │ 2304x1856   │ 4608x3712  │
            # │ 8:1      │ 3072x384    │ 1120   │ 6144x768    │ 12288x1536 │
            # │ 9:16     │ 768x1376    │ 1120   │ 1536x2752   │ 3072x5504  │
            # │ 16:9     │ 1376x768    │ 1120   │ 2752x1536   │ 5504x3072  │
            # │ 21:9     │ 1584x672    │ 1120   │ 3168x1344   │ 6336x2688  │
            # └──────────┴─────────────┴────────┴─────────────┴────────────┘
            # 注: 1K/2K/4K令牌分别为1120/1680/3780
            "aspectRatio": "1:1",

            # imageSize: 设置输出图片的分辨率
            # - "1K": 1K 分辨率 (默认值)
            # - "2K": 2K 分辨率
            # - "4K": 4K 分辨率
            # 注意: K 必须大写，不能写成 1k；本模型不支持 512
            "imageSize": "2K",
        },

        # thinkingConfig: 思考等级配置 (思考过程默认启用，无法完全关闭)
        "thinkingConfig": {
            # thinkingLevel: 生成图片前的思考深度
            # - "MINIMAL": 较少思考，速度最快
            # - "MEDIUM":  均衡模式 (默认值)
            # - "HIGH":    深度思考，复杂画面质量更稳定
            "thinkingLevel": "MEDIUM",
        },
    },

    # tools: Google 搜索工具（可选）
    # - 使用实时信息修改图像（如根据最新资讯添加元素等）
    # "tools": [{"google_search": {}}]
    #
    # 本模型同时支持 Image Search（图片搜索）：
    # "tools": [{"google_search": {"search_types": {"web_search": {}, "image_search": {}}}}]
}

# ══════════════════════════════════════════════════════════════════════════════
#                                   主程序执行                                  
# ══════════════════════════════════════════════════════════════════════════════
# ┌─────────────────────────────────────────────────────────────────────────┐
# │ 步骤 1: 发送 API 请求                                                   │
# │         向 DMXAPI 发送 POST 请求，地址由 BASE_URL 和 MODEL_NAME 拼接    │
# └─────────────────────────────────────────────────────────────────────────┘
response = requests.post(API_URL, headers=headers, json=payload)
response.raise_for_status()  # 检查 HTTP 状态码，若有错误则抛出异常
result = response.json()

# 响应中没有候选结果时直接报错，便于排查问题
if not result.get("candidates"):
    raise ValueError(f"响应中没有候选结果：{result}")

# ┌─────────────────────────────────────────────────────────────────────────┐
# │ 步骤 2: 将本轮内容追加到历史                                            │
# │         本轮成功后，把用户输入和完整模型输出一起追加到历史文件          │
# └─────────────────────────────────────────────────────────────────────────┘
model_content = result["candidates"][0]["content"]
history.extend([user_content, model_content])

HISTORY_PATH.write_text(
    json.dumps(history, ensure_ascii=False, indent=2),
    encoding="utf-8",
)

# ┌─────────────────────────────────────────────────────────────────────────┐
# │ 步骤 3: 保存本轮修改后的图片                                            │
# │         保存最终图片时跳过 thought=true 的部分；历史中的这些部分仍然保留│
# └─────────────────────────────────────────────────────────────────────────┘
output_dir = Path("output")
output_dir.mkdir(exist_ok=True)

for part in model_content.get("parts", []):
    if part.get("thought"):
        continue

    # 文字片段直接打印
    if "text" in part:
        print(part["text"])

    # 图片片段 (inlineData 内嵌 Base64 图片数据)
    elif "inlineData" in part:
        image = part["inlineData"]

        # 按返回的 MIME 类型确定文件扩展名 (image/png -> png)
        extension = image["mimeType"].split("/")[-1]

        # 生成带时间戳的文件名，格式: edited_image_20261008_120000.png
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"output/edited_image_{timestamp}.{extension}"

        # 解码 Base64 数据并写入图片文件
        Path(filename).write_bytes(base64.b64decode(image["data"]))

        # 输出保存成功的提示信息
        print(f"修改后的图片已保存到 {filename}")

print(f"完整对话历史已更新到 {HISTORY_PATH}")
```

:::

## 返回示例

::: code-group

```text [生成图片]
图片已保存到 output/generated_image_20261008_120000.jpeg
完整对话历史已保存到 base64_data/history.json
```

```text [多轮修改]
修改后的图片已保存到 output/edited_image_20261008_120100.jpeg
完整对话历史已更新到 base64_data/history.json
```

:::
---

<p align="center">
  <small>© 2026 DMXAPI gemini-nano-banana-2.1 多轮图片修改</small>
</p>
