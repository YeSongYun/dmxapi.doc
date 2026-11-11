# kling-4.0 图片主体创建 API 使用文档

基于可灵 Kling 4.0 主体管理接口，通过 DMXAPI 网关创建多图主体。图片主体使用 `reference_type = image_refer`：1 张正面图，再加 1～3 张不同于正面的其他角度或特写。创建接口立即返回 `data.task_id`，这时还没有 `element_id`。用主体任务查询等到 `task_status` 为 `succeed` 后，取 `data.task_result.elements[0].element_id`。

这个 `element_id` 只用于全能参考生视频：在 `contents` 里加一条 `type` 为 `element` 的素材，并在提示词中用对应的 `@id` 引用。图片主体和视频主体拿到的都是这种 ID，引用方式相同。

## 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 提交任务 | POST | `https://www.dmxapi.cn/kling-4-0/v1/general/advanced-custom-elements` |
| 查询主体 | GET | `https://www.dmxapi.cn/kling-4-0/v1/general/advanced-custom-elements/{task_id}` |

:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。如果怀疑密钥已泄露，请立即前往 DMXAPI 官网重新生成。
:::

## 模型名称

- `kling-4.0`

## 图片主体创建示例代码

```python
import requests
import json

# ===============================================================
# 步骤1: 配置 API 连接信息
# ===============================================================

# DMXAPI Kling 4.0 图片主体创建接口
# 与视频主体创建是同一个地址，用 reference_type 区分
url = "https://www.dmxapi.cn/kling-4-0/v1/general/advanced-custom-elements"

# DMXAPI 密钥 (请替换为您自己的密钥)
# 获取方式: 登录 DMXAPI 官网 -> 个人中心 -> API 密钥管理
api_key = "sk-***********************************************"

# ===============================================================
# 步骤2: 配置请求头
# ===============================================================

headers = {
    "Content-Type": "application/json",       # 指定请求体为 JSON 格式
    "Authorization": f"Bearer {api_key}",     # Bearer 认证
}

# ===============================================================
# 步骤3: 配置请求参数
# ===============================================================

payload = {
    # 【model】(string, 必填) 模型名称，固定为 kling-4.0
    "model": "kling-4.0",

    # 【element_name】(string, 必填) 主体名称，最多 20 个字符
    "element_name": "女孩",

    # 【element_description】(string, 必填) 主体描述，最多 100 个字符
    "element_description": "用于视频生成的主体参考",

    # 【reference_type】(string, 必填) 图片主体必须填写 image_refer
    # image_refer 的外观由 element_image_list 定义
    # 图片主体和视频主体可使用的能力范围不同
    "reference_type": "image_refer",

    # 【element_image_list】(object, 必填) reference_type 为 image_refer 时必填
    # 至少 1 张正面图，外加 1～3 张与正面不同的参考图
    # 支持 jpg、jpeg、png 的 HTTP(S) 地址，或 JPEG/PNG 的 data URL，不能只贴裸 Base64
    # 单张不超过 10MB，宽和高都不小于 300px，宽高比在 1:2.5 到 2.5:1 之间
    "element_image_list": {
        # 【frontal_image】(string, 必填) 正面参考图
        "frontal_image": "https://viapi-test.oss-cn-shanghai.aliyuncs.com/viapi-3.0domepic/facebody/CompareFace/CompareFace-right1.png",
        # 【refer_images】(array, 必填) 其他角度或特写，1～3 张
        "refer_images": [
            {"image_url": "https://viapi-test.oss-cn-shanghai.aliyuncs.com/viapi-3.0domepic/facebody/CompareFace/CompareFace-left1.png"},
        ],
    },

    # 【tag_list】(array, 可选) 标签对象。一个主体可以有多个标签
    # tag_id 取值：
    #   o_101 最热 / o_102 人物 / o_103 动物 / o_104 道具
    #   o_105 服饰 / o_106 场景 / o_107 特效 / o_108 其他
    "tag_list": [{"tag_id": "o_102"}],
}

# ===============================================================
# 步骤4: 发送请求并输出结果
# ===============================================================

response = requests.post(url, headers=headers, json=payload)
print("status:", response.status_code)
result = response.json()
print(json.dumps(result, indent=2, ensure_ascii=False))

# 主体创建返回的是 data.task_id，不是 element_id
# 把 task_id 放到主体查询 URL 的最后一段，等到 succeed 后再取 element_id
data = result.get("data") if isinstance(result, dict) else None
if isinstance(data, dict):
    print("task_id:", data.get("task_id"))

response.raise_for_status()
```

## 返回示例

```json
status: 200
{
  "code": 0,
  "data": {
    "task_id": "task_DXuawHxBD9GPUw5wx46ftF21YixqM9lp",
    "task_status": "submitted"
  },
  "message": "",
  "request_id": "bb502612-2484-44d6-a52c-55d979f53c6e"
}
task_id: task_DXuawHxBD9GPUw5wx46ftF21YixqM9lp
```
## 查询主体任务 示例代码

```python
import requests
import json
import time

# ===============================================================
# 步骤1: 配置 API 连接信息
# ===============================================================

# 创建接口返回的 data.task_id。路径参数使用 task_id 或 external_task_id，二者只能填一个
task_id = "task_LdsX7XEpIpOiu6rBHEDFEDOgXwsuXq5G"

# DMXAPI Kling 4.0 主体任务查询接口
# 图片主体和视频主体共用此接口，task_id 写在路径最后
url = f"https://www.dmxapi.cn/kling-4-0/v1/general/advanced-custom-elements/{task_id}"

# DMXAPI 密钥 (请替换为您自己的密钥)
api_key = "sk-***********************************************"

# ===============================================================
# 步骤2: 配置请求头
# ===============================================================

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}",
}

# ===============================================================
# 步骤3: 轮询直到任务结束
# ===============================================================

# 查询接口会立刻返回当前状态。每 25 秒查询一次，最多等待 600 秒。
# 主体任务成功状态是 succeed。失败时看 data.task_status_msg。
end_time = time.time() + 600
while time.time() < end_time:
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    result = response.json()
    data = result.get("data") if isinstance(result, dict) else None
    status = str(data.get("task_status") or data.get("status") or "").lower() if isinstance(data, dict) else ""
    if status in {"succeeded", "succeed", "failed", "cancelled", "timed_out"}:
        break
    time.sleep(25)
else:
    raise TimeoutError("主体任务在 600 秒内没有结束")

print("status:", response.status_code)
print(json.dumps(result, indent=2, ensure_ascii=False))

# 成功后，把 element_id 填入全能参考生视频 contents 里 type=element 的 element_id
if status in {"succeeded", "succeed"} and isinstance(data, dict):
    task_result = data.get("task_result", {})
    elements = task_result.get("elements", []) if isinstance(task_result, dict) else []
    if elements:
        print("element_id:", elements[0].get("element_id"))
```

## 返回示例

```json
status: 200
{
  "code": 0,
  "data": {
    "task_id": "task_DXuawHxBD9GPUw5wx46ftF21YixqM9lp",
    "task_result": {
      "elements": [
        {
          "element_id": "ke_9f582e36f4a41802",
          "reference_type": "image_refer",
          "status": "succeed"
        }
      ]
    },
    "task_status": "succeed",
    "task_status_msg": ""
  },
  "message": "",
  "request_id": "0c50ee0e-f0b9-44d4-bc3c-c8f4a48950cc"
}
element_id: ke_9f582e36f4a41802
```
<p align="center">
  <small>© 2026 DMXAPI Kling-4.0 图片主体创建</small>
</p>
