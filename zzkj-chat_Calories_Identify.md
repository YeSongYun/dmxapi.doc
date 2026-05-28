# zzkj-chat 热量识别 API 使用文档

基于智诊科技 WiseDiag 智能体工作流的热量识别（calories）任务接口，支持用户上传 1-5 张食物图片（正餐、零食、饮品等），由 AI 模型自动识别食物种类、估算每份食物的热量与营养成分，并结合用户健康档案给出个性化的饮食建议。。

## 📌 请求地址

```
https://www.dmxapi.cn/v1/responses
```

:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。如果怀疑密钥已泄露，请立即前往 DMXAPI 官网重新生成。
:::

## 🍱 模型名称

- `zzkj-chat`

## 💻 热量识别 示例代码

```python
import requests
import json
import time

# ═══════════════════════════════════════════════════════════════
# 步骤1: 配置 API 连接信息
# ═══════════════════════════════════════════════════════════════

# DMXAPI 服务端点地址
url = "https://www.dmxapi.cn/v1/responses"

# DMXAPI 密钥 (请替换为您自己的密钥)
# 获取方式: 登录 DMXAPI 官网 -> 个人中心 -> API 密钥管理
api_key = "sk-***********************************************"

# ═══════════════════════════════════════════════════════════════
# 步骤2: 配置请求头
# ═══════════════════════════════════════════════════════════════

headers = {
    "Content-Type": "application/json",      # 指定请求体为 JSON 格式
    "Authorization": f"{api_key}",           # token 认证方式
}

# ═══════════════════════════════════════════════════════════════
# 步骤3: 配置请求参数
# ═══════════════════════════════════════════════════════════════

payload = {
    # 【model】(string, 必填) 模型名称，固定为 zzkj-chat
    # 可选值: "zzkj-chat"(智诊科技智能体工作流模型)
    "model": "zzkj-chat",

    # 【task_name】(string, 必填) 任务类型标识，决定本次请求执行哪种业务能力
    # 可选值:
    #   "chat"(智能问诊聊天，提供个性化健康咨询与建议)
    #   "photo_read"(图片健康解读，智能分析医学影像与健康相关图片)
    #   "calories"(热量识别，识别食物并计算营养成分)
    # 本文档场景为热量识别，固定传 "calories"
    "task_name": "calories",

    # 【image_list】(array, 必填于 calories/photo_read 任务) 食物图片 URL 列表
    # 单次请求最多上传 5 张图片
    # 支持 JPG、JPEG、PNG 等常见格式，需提供可公开访问的 URL
    # 仅在 task_name 为 "photo_read" 或 "calories" 时生效
    "image_list": [
        "https://tse4.mm.bing.net/th/id/OIP.gXQv-qjaf5wAwJCdkjmTFAHaE8?r=0&rs=1&pid=ImgDetMain&o=7&rm=3"  # 替换为真实食物图片 URL
    ],

    # 【input】(array, 必填) 消息数组，承载用户提问与多轮对话上下文
    "input": [
        {"role": "user", "content": "这顿饭大概多少热量?我血糖偏高能吃吗?"}
    ],

    # ─── 会话管理 ───
    # 【request_id】(string, 可选) 请求唯一标识，便于日志追踪与问题排查
    # 建议使用毫秒时间戳: str(int(time.time() * 1000))
    # 不传入时将自动生成
    "request_id": str(int(time.time() * 1000)),

    # 【user_id】(string, 可选) 用户唯一标识，用于平台侧用户级别的会话/统计聚合
    "user_id": "test_user_001",

    # ─── 健康档案 ───
    # 【member_id】(string, 可选) 健康档案 ID（如 "sample_1"）
    # 启用档案以提供"该用户能不能吃"的个性化建议
    # 健康档案生效需同时满足: use_health_record=1 且 member_id 有效
    "member_id": "sample_1",

    # 【use_health_record】(integer, 可选) 是否启用健康档案
    # 取值: 1=启用 / 0=关闭，默认值为 1
    # 启用后 AI 将结合用户基础信息、既往史、过敏史等给出个性化建议
    "use_health_record": 1,

    # ─── 知识库与检索 ───
    # 热量识别本身不依赖医学 RAG，关闭知识库节省耗时
    #
    # 【query_understand】(integer, 可选) 是否进行查询理解分析
    # 取值: 1=开启 / 0=关闭，默认值为 1
    # 联动规则: query_understand=1 时必须至少启用一个知识源（local_DB/expert_DB/web_engine）才会生效
    # 联动规则: query_understand=0 时所有知识库参数将自动关闭，即使设置为 1 也不会生效
    "query_understand": 0,

    # 【local_DB】(integer, 可选) 是否使用本地知识库
    # 取值: 1=开启 / 0=关闭，默认值为 1
    # 受 query_understand 联动控制
    "local_DB": 0,

    # 【use_ch_medicine】(integer, 可选) 是否启用中医知识库
    # 取值: 1=开启 / 0=关闭，默认值为 1
    # 需同时启用 local_DB 才会生效
    "use_ch_medicine": 0,

    # 【expert_DB】(integer, 可选) 是否使用专家知识库
    # 取值: 1=开启 / 0=关闭，默认值为 1
    # 受 query_understand 联动控制
    "expert_DB": 0,

    # 【web_engine】(integer, 可选) 是否开启医学专网搜索
    # 取值: 1=开启 / 0=关闭，默认值为 1
    # 受 query_understand 联动控制
    "web_engine": 0,

    # ─── 其他 ───
    # 【product_open】(integer, 可选) 是否开启商品推荐
    # 取值: 1=开启 / 0=关闭，默认值为 1
    # 关闭后输出中不会附带相关健康产品/营养品推荐
    "product_open": 0,

    # 【language】(string, 可选) 语言代码
    # 可选值: "zh"(中文，所有功能完整支持) / "en"(英文，仅支持聊天) / "id"(印尼语，仅支持聊天) / "ar"(阿拉伯语，仅支持聊天)
    # 默认值为 "zh"
    # 非中文语言仅支持聊天任务，calories 仅支持中文
    "language": "zh",

    # 【stream】(boolean, 可选) 是否启用流式输出
    # true=按 OpenAI Responses streaming 标准事件逐段返回 / false=一次性返回完整结果
    # 默认值为 false（具体由 DMXAPI /v1/responses 端点行为决定）
    # 热量识别建议开启以提升用户感知速度
    "stream": True
}


# ═══════════════════════════════════════════════════════════════
# 步骤4: 发送请求并输出结果
# ═══════════════════════════════════════════════════════════════

# 发送 POST 请求到 API 服务器（流式）
usage = None
with requests.post(url, headers=headers, json=payload, stream=True) as response:
    if response.status_code != 200:
        print(f"请求失败,状态码: {response.status_code}, {response.text}")
    else:
        for line in response.iter_lines():
            if not line:
                continue
            raw = line.decode("utf-8")
            # DMXAPI /v1/responses 在 stream:true 下按 OpenAI Responses streaming
            # 标准事件转发：每个事件含两行—"event: response.xxx" 与 "data: {...}"，
            # 客户端只看 data: 行，跳过 event: 行
            if not raw.startswith("data:"):
                continue
            data_str = raw[5:].strip()
            if data_str == "[DONE]":
                break
            try:
                evt = json.loads(data_str)
            except json.JSONDecodeError:
                continue
            t = evt.get("type", "")
            if t == "response.output_text.delta":
                # 文本片段在 delta 字段（不是 content / reasoning_content）
                print(evt.get("delta", ""), end="", flush=True)
            elif t == "response.completed":
                # usage 嵌在 response 对象里（不是事件顶层）
                usage = (evt.get("response") or {}).get("usage")
        print()
        if usage:
            print(f"\n=== Usage ===")
            print(json.dumps(usage, indent=2, ensure_ascii=False))
```

## 📊 返回示例

```text
康小鹿，你好呀！我是好小伴，很高兴为你解答。看到你上传的这份色彩缤纷的蔬菜沙拉，我来帮你分析一下热量和血糖方面的问题吧~ 🌈

### 📊 1. 这顿饭的热量大概有多少？
根据图片分析结果，这份蔬菜沙拉的总热量大约在 **110 - 140 大卡** 之间。主要热量来源是那瓶沙拉酱（约占总热量的40%-55%）和玉米粒。

### 🍎 2. 血糖偏高能吃吗？
可以吃，但需要注意几个关键点，让它更适合你的血糖状况：

*   **优点：** 沙拉本身蔬菜丰富，富含膳食纤维，有助于延缓糖分吸收，对控制血糖是有利的。整体热量也不高，属于轻食范畴。
*   **需要注意的地方：**
    *   **沙拉酱是重点！** 部分沙拉酱（尤其是奶油基底的，如凯撒酱、千岛酱）含糖和脂肪较高，会间接影响血糖。建议你选择 **油醋汁、柠檬汁+黑胡椒** 等低脂、低糖的酱料，或者将酱料减半使用。
    *   **玉米粒要注意：** 现在的沙拉里有20克熟玉米粒，它属于升糖指数（GI）较高的食物。如果你特别在意血糖，可以适当减少玉米粒的量，或者用黄瓜丁、彩椒丁等更低GI的蔬菜来替代一部分。

**总结一下：** 这份沙拉本身是健康的选择，只要**调整一下酱料**，就非常适合血糖偏高的你食用。记得吃完后留意一下自己的身体感觉哦！

### 💪 给你的个性化小建议：
考虑到你的基础健康信息（32岁男性，BMI 17.3，属于偏瘦；有类风湿关节炎病史；家族有糖尿病和心脏病史），我还有几点额外的贴心提醒：

1.  **增加蛋白质，更均衡：** 你的BMI偏低，这顿沙拉作为正餐可能稍显"单薄"。强烈建议你在沙拉里加入一些**优质蛋白质**，比如：
    *   一份水煮鸡胸肉（约80-100g）
    *   一个水煮蛋
    *   或者半块豆腐
    这样不仅能让你更饱腹，帮助增肌，还能使餐后的血糖曲线更平稳。

2.  **关注关节健康：** 你正在服用艾拉莫德片治疗类风湿关节炎。这份沙拉里的蔬菜富含维生素和抗氧化物质，对减轻关节炎症很有好处。继续保持多吃蔬菜的好习惯！

3.  **安全第一，避开过敏原：** 分析显示沙拉中没有发现你已知的海鲜或牛奶过敏原，可以放心享用。但请注意，如果使用的沙拉酱含有乳清粉等奶制品成分，可能会引发过敏，所以选择酱料时务必看清配料表。

希望这些分析对你有帮助！吃得开心，也要吃得安心哦！😊 如果还有其他问题，随时问我~

=== Usage ===
{
  "input_tokens": 1681,
  "input_tokens_details": {
    "cached_tokens": 0
  },
  "output_tokens": 1044,
  "output_tokens_details": {
    "reasoning_tokens": 0
  },
  "total_tokens": 2725
}
```

<p align="center">
  <small>© 2026 DMXAPI zzkj-chat 热量识别</small>
</p>
