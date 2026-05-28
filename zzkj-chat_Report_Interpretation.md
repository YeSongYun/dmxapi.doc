# zzkj-chat 报告解读 API 使用文档

基于智诊科技 zzkj-chat 医疗大模型的报告解读接口，通过 `/v1/responses` 端点提交医学影像或体检报告图片（最多 5 张），由模型结合本地知识库、专家知识库、中医知识库与医学专网搜索四类医学知识源进行智能解读。接口支持基于个人健康档案（既往史、过敏史、家族史等）的个性化分析，可通过 `topic_id` 实现多轮上下文对话，并按 OpenAI Responses 标准以流式（SSE）方式实时返回解读内容与健康产品推荐。

## 🌐 请求地址

```
https://www.dmxapi.cn/v1/responses
```
:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。如果怀疑密钥已泄露，请立即前往 DMXAPI 官网重新生成。
:::

## 🤖 模型名称

- `zzkj-chat`

## 💻 报告解读示例代码

```python
import requests
import json
import time

# ═══════════════════════════════════════════════════════════════
# 步骤1: 配置 API 连接信息
# ═══════════════════════════════════════════════════════════════

# DMXAPI 服务端点地址（Responses 端点）
url = "https://www.dmxapi.cn/v1/responses"

# DMXAPI 密钥 (请替换为您自己的密钥)
# 获取方式: 登录 DMXAPI 官网 -> 个人中心 -> API 密钥管理
api_key = "sk-**********************************************"

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

    # 【model】(string, 必填) 模型名称，报告解读固定使用 zzkj-chat
    "model": "zzkj-chat",

    # 【task_name】(string, 必填) 任务类型
    # 可选值: "chat"(智能问诊聊天) / "photo_read"(图片健康解读) / "calories"(食物热量识别)
    # 报告解读场景固定为 "photo_read"
    "task_name": "photo_read",

    # 【image_list】(array, 可选) 图片 URL 列表，最多 5 张
    # 仅在 task_name 为 "photo_read" 或 "calories" 时生效
    # photo_read 任务下为必传项: 传入待解读的报告/影像图片 URL
    "image_list": [
        "https://inews.gtimg.com/om_bt/Oh7_hsqc1BAABDK26C9BDs2kqR-0na-NU_R57s2VZcpekAA/641"  # 替换为真实图片 URL
    ],

    # 【input】(array, 必填) 消息数组，每个元素含 role 与 content 两个字段
    # 结构等同于官方 messages 字段（Responses 端点入参字段名为 input）
    # role 可选值: "user"(用户) / "assistant"(助手) / "system"(系统)
    # 若不传入 system 消息，将使用内置默认 system
    "input": [
        {"role": "user", "content": "帮我解读一下这份体检报告"}
    ],

    # ───────── 会话管理 ─────────
    # 【topic_id】(string, 可选) 会话 ID，用于上下文管理
    # 不传入时: 不进行会话管理，需客户端自行拼接多轮对话
    # 传入时: 自动管理会话上下文，每次仅需传入一轮 user prompt
    # 传入新 system 时: 该 topic 整组会话的 system 将被更新
    "topic_id": "demo_photo_001",

    # 【request_id】(string, 可选) 请求唯一标识，不传入时将自动生成
    # 建议使用毫秒时间戳: str(int(time.time() * 1000))
    "request_id": str(int(time.time() * 1000)),

    # 【user_id】(string, 可选) 用户唯一标识
    "user_id": "test_user_001",

    # ───────── 健康档案 ─────────
    # 【member_id】(string, 可选) 健康档案 ID（如 sample_1）
    # 健康档案生效需同时满足: use_health_record=1 且 member_id 有效
    "member_id": "sample_1",

    # 【use_health_record】(integer, 可选) 是否启用健康档案，默认 1
    # 可选值: 1(启用) / 0(关闭)
    # 启用后 AI 将结合用户档案（既往史/过敏史/家族史等）提供个性化建议
    "use_health_record": 1,

    # ───────── 知识库与检索 ─────────
    # 【query_understand】(integer, 可选) 是否进行查询理解分析，默认 1
    # 参数联动规则:
    #   query_understand=1 时，必须至少启用一个知识源(local_DB / expert_DB / web_engine)，否则不生效
    #   query_understand=0 时，所有知识库参数自动关闭，即使设为 1 也不生效
    "query_understand": 1,

    # 【local_DB】(integer, 可选) 是否使用本地知识库，默认 1。可选值: 1 / 0
    "local_DB": 1,

    # 【use_ch_medicine】(integer, 可选) 是否启用中医知识库，默认 1。可选值: 1 / 0
    # 需同时启用 local_DB 才生效
    "use_ch_medicine": 0,

    # 【expert_DB】(integer, 可选) 是否使用专家知识库，默认 1。可选值: 1 / 0
    "expert_DB": 1,

    # 【web_engine】(integer, 可选) 是否开启医学专网搜索，默认 1。可选值: 1 / 0
    "web_engine": 0,

    # ───────── 其他 ─────────
    # 【product_open】(integer, 可选) 是否开启商品推荐，默认 1
    # 可选值: 1(开启) / 0(关闭)
    "product_open": 1,

    # 【language】(string, 可选) 语言代码，默认 "zh"
    # 可选值: "zh"(中文) / "en"(英文) / "id"(印尼语) / "ar"(阿拉伯语) 等
    # 非中文语言仅支持聊天任务；photo_read 报告解读仅支持中文
    "language": "zh",

    # 【stream】(boolean, 可选) 是否启用流式输出（官方文档未明确说明）
    # 设为 True 时，按 OpenAI Responses streaming 标准以 SSE 方式实时返回
    "stream": True,

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

## 📤 返回示例

```text
看到这份近一年前的病历，我能理解你对烫伤恢复和疤痕问题的持续关注。时间过得真快，从记录来看，现在距离那次烫伤已经快一年了，疤痕也进入了相对稳定的阶段。咱们一起来仔细看看当时的情况，再结合现在的状态，给你一些更针对性的建议。

### 📄 病历核心信息解读（2025-07-12）

**1. 伤情判断**
- **诊断：二度烫伤 + 瘢痕形成**  
  这说明当时的烫伤深度达到了真皮层，所以愈合后留下了疤痕。你腹部那个约2×1.5厘米的结痂，正是伤口在自然修复过程中的表现。

**2. 治疗建议分析**
- **点阵激光（需5次以上）**：这是一种通过微创方式刺激皮肤再生，改善疤痕凹凸和颜色的有效方法，但需要多次治疗才能达到最佳效果。
- **硅酮凝胶类药膏**：像芭克、美皮护这类产品，能软化疤痕组织、减少增生，需要长期坚持涂抹（通常3-6个月）。
- **重要提示**：“不能完全恢复至正常皮肤”——这是基于医学现实的客观描述，深度烫伤留下的疤痕很难彻底消除，但通过规范治疗可以显著改善外观和触感。

---

### 💡 结合当前时间（2026-05-27）的个性化建议

**疤痕现状推测与应对：**
由于这份记录是近1年前的，疤痕的最终形态通常在伤后6-18个月稳定。这意味着你现在的情况可能是：
- **如果已完成治疗**：疤痕可能已趋于稳定，颜色接近肤色，但可能仍有轻微凹凸。
- **如果未开始治疗**：疤痕可能已定型，此时再进行点阵激光仍有效果，但改善程度可能不如早期干预。

**日常护理重点：**
- **防晒！防晒！防晒！**  
  新生皮肤对紫外线极其敏感，外出时务必用衣物/帽子遮挡+SPF30+防晒霜，避免疤痕变黑。
- **温和清洁与保湿**  
  避免用力搓揉疤痕处，每天涂抹无香精身体乳（如Cerave、丝塔芙），保持皮肤柔软。
- **观察变化**  
  注意疤痕是否有发红、瘙痒、疼痛或快速增厚（这可能是疤痕增生的信号）。

---

### ❓ 需要你补充的信息（帮助更精准建议）
1. **疤痕现状**：现在疤痕的颜色是偏红、暗沉还是接近肤色？触摸起来是平坦、凸起还是凹陷？
2. **治疗执行情况**：是否按医嘱做过点阵激光或涂抹过祛疤药膏？如果有，大概做了几次？
3. **症状反馈**：现在疤痕区域会有瘙痒、刺痛，或者影响活动（比如弯腰时紧绷感）吗？

---

### ❤️ 心理支持小贴士
烫伤留疤确实会让人焦虑，尤其是影响美观时。但请记住：
✅ 规范治疗能让疤痕变得“低调”很多  
✅ 很多疤痕随时间推移会逐渐淡化  
✅ 如果实在介意，现在还有微针、药物注射等进阶方案可以咨询医生  

你愿意和我聊聊现在疤痕的具体情况吗？我会根据你的描述给出更具体的应对策略~

=== Usage ===
{
  "input_tokens": 1681,
  "input_tokens_details": {
    "cached_tokens": 0
  },
  "output_tokens": 966,
  "output_tokens_details": {
    "reasoning_tokens": 0
  },
  "total_tokens": 2647
}
```

<p align="center">
  <small>© 2026 DMXAPI zzkj-chat 报告解读</small>
</p>
