# FLUX.2 PRO

文生图 | 图片编辑 | 多图融合

## 接口信息

| 项目 | 说明 |
|------|------|
| 请求地址 | `https://www.dmxapi.cn/flux/v1/flux-2-pro` |
| 模型名称 | `flux-2-pro` |


## 示例代码

```python
# -*- coding: utf-8 -*-
"""
DMXAPI FLUX.2 PRO 图像生成/编辑示例
支持文生图和图片编辑功能
"""

import requests
import json
import os
from datetime import datetime
import time
import base64

# ============================================================================
# 配置部分
# ============================================================================

# DMXAPI 密钥（替换为你的密钥）
API_KEY = "sk-*****************************************"

# API 基础 URL
BASE_URL = "https://www.dmxapi.cn"

# ============================================================================
# 图像生成/编辑参数
# ============================================================================

# 生成提示词（必填）
prompt = "一只可爱的橘猫在阳光下打盹"

# 图片尺寸（可选，默认为 0 表示自动）
width = 1024
height = 1024

# 随机种子（可选，用于复现结果）
seed = None

# 安全容忍度（0-5，0 最严格，5 最宽松）
safety_tolerance = 2

# 输出格式（jpeg 或 png）
output_format = "jpeg"

# ============================================================================
# 图片编辑参数（可选）
# 如果需要图片编辑功能，请提供输入图片
# 支持 URL 或 Base64 编码的图片
# ============================================================================

input_image = None      # 第 1 张输入图片
input_image_2 = None    # 第 2 张输入图片
input_image_3 = None    # 第 3 张输入图片
input_image_4 = None    # 第 4 张输入图片
input_image_5 = None    # 第 5 张输入图片（Kontext 实验性多参考）
input_image_6 = None    # 第 6 张输入图片（Kontext 实验性多参考）
input_image_7 = None    # 第 7 张输入图片（Kontext 实验性多参考）
input_image_8 = None    # 第 8 张输入图片（Kontext 实验性多参考）


# ============================================================================
# 辅助函数
# ============================================================================

def image_to_base64(image_path):
    """将本地图片转换为 Base64 编码"""
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def build_request_body():
    """构建请求体"""
    body = {"prompt": prompt}

    # 添加可选参数
    if width and width > 0:
        body["width"] = width
    if height and height > 0:
        body["height"] = height
    if seed is not None:
        body["seed"] = seed
    if safety_tolerance is not None:
        body["safety_tolerance"] = safety_tolerance
    if output_format:
        body["output_format"] = output_format

    # 添加输入图片（如果有）
    image_params = [
        ("input_image", input_image),
        ("input_image_2", input_image_2),
        ("input_image_3", input_image_3),
        ("input_image_4", input_image_4),
        ("input_image_5", input_image_5),
        ("input_image_6", input_image_6),
        ("input_image_7", input_image_7),
        ("input_image_8", input_image_8),
    ]
    for param_name, param_value in image_params:
        if param_value:
            body[param_name] = param_value

    return body


# ============================================================================
# 步骤 1: 提交生成任务
# ============================================================================

print("=" * 60)
print("FLUX.2 PRO 图像生成")
print("=" * 60)
print(f"\n提示词: {prompt}")
print(f"尺寸: {width}x{height}")
print(f"输出格式: {output_format}")

# 构建请求
url = f"{BASE_URL}/flux/v1/flux-2-pro"
headers = {
    "Content-Type": "application/json",
    "x-key": API_KEY
}
body = build_request_body()

print("\n正在提交生成任务...")
response = requests.post(url, headers=headers, json=body)
result = response.json()

print("\n任务提交响应:")
print(json.dumps(result, indent=4, ensure_ascii=False))

# 检查是否成功
if "id" not in result:
    print("\n任务提交失败!")
    exit(1)

task_id = result["id"]
polling_url = result.get("polling_url", f"{BASE_URL}/flux/v1/get_result?id={task_id}")

print(f"\n任务 ID: {task_id}")
print(f"轮询 URL: {polling_url}")

# ============================================================================
# 步骤 2: 轮询获取结果
# ============================================================================

print("\n正在等待生成完成...")

max_attempts = 60  # 最大尝试次数
attempt = 0
poll_interval = 3  # 轮询间隔（秒）

while attempt < max_attempts:
    attempt += 1
    time.sleep(poll_interval)

    poll_response = requests.get(polling_url, headers={"x-key": API_KEY})
    poll_result = poll_response.json()

    status = poll_result.get("status", "Unknown")
    print(f"  尝试 {attempt}: 状态 = {status}")

    if status == "Ready":
        print("\n生成完成!")
        print("\n完整响应:")
        print(json.dumps(poll_result, indent=4, ensure_ascii=False))
        break
    elif status in ["Error", "Failed", "Content Moderated"]:
        print(f"\n生成失败: {status}")
        print(json.dumps(poll_result, indent=4, ensure_ascii=False))
        exit(1)
else:
    print("\n超时: 任务未在预期时间内完成")
    exit(1)

# ============================================================================
# 步骤 3: 下载并保存图片
# ============================================================================

sample_url = poll_result.get("result", {}).get("sample")

if not sample_url:
    print("\n未找到图片 URL")
    exit(1)

# 创建 output 文件夹
output_dir = os.path.join(os.path.dirname(__file__), "output")
os.makedirs(output_dir, exist_ok=True)

# 生成带时间戳的文件名
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
ext = "png" if output_format == "png" else "jpeg"
filename = f"flux2pro_{timestamp}.{ext}"
filepath = os.path.join(output_dir, filename)

# 下载图片
print(f"\n正在下载图片...")
print(f"  URL: {sample_url[:80]}...")

img_response = requests.get(sample_url)

with open(filepath, "wb") as f:
    f.write(img_response.content)

print(f"\n图片已保存到: {filepath}")
print("\n" + "=" * 60)
print("完成!")
print("=" * 60)
```

## 调用流程

1. **提交任务**：POST 请求提交生成任务，获取任务 ID 和轮询地址
2. **轮询状态**：GET 请求轮询任务状态，等待生成完成
3. **获取结果**：状态为 `Ready` 时，从响应中获取图片 URL 并下载

## 运行示例
```json
============================================================
FLUX.2 PRO 图像生成
============================================================

提示词: 一只可爱的橘猫在阳光下打盹
尺寸: 1024x1024
输出格式: jpeg

正在提交生成任务...

任务提交响应:
{
    "id": "38b4e501-344b-4d19-9ffa-a566b7f36b1c",
    "polling_url": "https://api.eu2.bfl.ai/v1/get_result?id=38b4e501-344b-4d19-9ffa-a566b7f36b1c",
    "cost": 3.0,
    "input_mp": 0.0,
    "output_mp": 1.0
}

任务 ID: 38b4e501-344b-4d19-9ffa-a566b7f36b1c
轮询 URL: https://api.eu2.bfl.ai/v1/get_result?id=38b4e501-344b-4d19-9ffa-a566b7f36b1c

正在等待生成完成...
  尝试 1: 状态 = Pending
  尝试 2: 状态 = Ready

生成完成!

完整响应:
{
    "id": "38b4e501-344b-4d19-9ffa-a566b7f36b1c",
    "status": "Ready",
    "result": {
        "start_time": 1764253858.8486362,
        "prompt": "photorealistic close-up of a cute chubby orange tabby cat napping in warm sunlight, curled up on a soft light-colored blanket near a window, eyes gently closed, paws tucked under its chin, sunbeams streaming in from the right and creating soft highlights on its fur, faint dust motes visible in the light, cozy home interior blurred in the background, soft focus and warm golden tones, calm and peaceful atmosphere",
        "seed": 1601288383,
        "sample": "https://bfldeliveryprodeu4.blob.core.windows.net/results/2025/11/27/d7284623db024a59af022e8ab8a1737c_sample.jpeg?se=2025-11-27T14%3A41%3A06Z&sp=r&sv=2024-11-04&sr=b&rsct=image/jpeg&sig=Pbvl8WELsEU1nz6Xgh%2BLNADnPgI6M/PJKyAzF5RzcFI%3D"      
    },
    "progress": null,
    "details": null,
    "preview": null
}

正在下载图片...
  URL: https://bfldeliveryprodeu4.blob.core.windows.net/results/2025/11/27/d7284623db02...

图片已保存到: output\flux2pro_20251127_223107.jpeg

============================================================
完成!
============================================================
```