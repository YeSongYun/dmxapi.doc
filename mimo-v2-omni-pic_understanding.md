# mimo-v2-omni 图片理解 API 使用文档

基于 Xiaomi MiMo `mimo-v2-omni` 模型的图片理解接口，支持通过 `chat/completions` 方式同时输入图片与文本内容，对图像进行描述、分类、对比分析等多模态理解任务。该能力支持公网图片 URL 和 Base64 编码两种图片输入方式，单张图片大小上限为 10 MB，适合图片描述、视觉问答、多图对比等场景。

## 🌐 请求地址

```bash
https://www.dmxapi.cn/v1/chat/completions
```


## 🧠 模型名称

- `mimo-v2-omni`

## 🖼️ 图片理解 示例代码

```python
import requests

url = "https://www.dmxapi.cn/v1/chat/completions"

# API Key，建议通过环境变量或密钥管理服务注入
API_KEY = "sk-**************************************"

headers = {
    # 【api-key】(string, 必填) API 认证密钥
    # 用于服务端鉴权，请通过请求头传递，不要硬编码到生产代码或提交到仓库
    "Authorization": API_KEY,
    "Content-Type": "application/json"
}

payload = {
    # 【model】(string, 必填) 要调用的模型名称
    "model": "mimo-v2-omni",
    # 【messages】(array, 必填) 对话消息列表，按顺序描述多轮输入
    # 图片理解场景下，可在 user 消息中混合传入图片与文本内容
    "messages": [
        {
            # 【role】(string, 必填) 消息角色
            # 可选值: "system"(系统提示) / "user"(用户输入) / "assistant"(助手回复)
            "role": "system",
            # 【content】(string, 必填) system 消息内容
            # 用于设定助手行为、身份或回复风格
            "content": "You are MiMo, an AI assistant developed by Xiaomi. Today is date: Tuesday, December 16, 2025. Your knowledge cutoff date is December 2024."
        },
        {
            # 【role】(string, 必填) 消息角色
            # user 表示当前消息来自用户
            "role": "user",
            # 【content】(array, 必填) 多模态内容列表
            # 可在同一条 user 消息中组合图片输入块与文本输入块
            "content": [
                {
                    # 【type】(string, 必填) 内容块类型
                    # 此处为 image_url，表示通过图片地址传入图像
                    "type": "image_url",
                    "image_url": {
                        # 【url】(string, 必填) 图片地址或 Base64 数据地址
                        # URL 方式要求图片可被公网访问；单张图片文件大小不能超过 10 MB
                        # 也可使用 data:{MIME_TYPE};base64,$BASE64_IMAGE 格式传入 Base64 编码图片
                        "url": "https://example-files.cnbj1.mi-fds.com/example-files/image/image_example.png"
                    }
                },
                {
                    # 【type】(string, 必填) 内容块类型
                    # 此处为 text，表示附加给模型的文本指令
                    "type": "text",
                    # 【text】(string, 必填) 文本提示内容
                    # 用于告诉模型如何理解、描述或比较图片
                    "text": "，完整精确地描述图片内容"
                }
            ]
        }
    ],
    # 【max_completion_tokens】(integer, 必填) 本次生成允许使用的最大输出 Token 数量
    # 默认值为 32768
    "max_completion_tokens": 1024
}

resp = requests.post(url, json=payload, headers=headers, timeout=60)
resp.raise_for_status()
print(resp.json())
```

## 📦 返回示例

```json
{
  "id": "2bc560c203ed4730abd1d11533d2b49b",
  "choices": [
    {
      "finish_reason": "length",
      "index": 0,
      "message": {
        "content": "这是一幅充满静谧生机的原始林间晨景图：\n\n前景处，河岸被厚实鲜亮的翠绿色苔藓完全覆盖，几块圆润的深灰调鹅卵石错落分布在浅溪边缘，石面湿润，带着 水汽的光泽。画面左侧，大片蕨类植物舒展着叶片，叶片呈现深绿与浅绿交织的自然纹理，叶脉清晰，尽显蓬勃生机。\n\n中景是一条蜿蜒的浅溪，清澈的溪水从林间深处流淌而来，漫过溪底的石块，在晨光的映照下，水面泛着细碎的金色波光，能隐约看到水下的石质纹理。溪流两岸的苔藓同样厚实，右侧生长着几丛叶片圆润的灌木，新生的嫩绿色叶片在光线里显得格外鲜亮，叶片仿佛还带着晨露的湿润感。\n\n背景是高大的古树林，粗壮的树干带着粗糙的纹理，虬结的树根裸露在地面，遒劲的枝干向四周肆意伸展。林间弥漫着轻薄的晨雾，清晨的阳光穿透枝叶与雾气，形成清晰的丁达尔光束，光束中能看到细小的水汽或尘埃微粒在缓缓浮动，远处的树木在雾气中显得朦胧柔和，为整个场景增添了梦幻感。\n\n整体氛围清新治愈，温暖柔和的光线、湿润",
        "role": "assistant",
        "tool_calls": null,
        "reasoning_content": "用户现在需要完整精确描述这张图片，首先先看整体场景：这是一处被晨雾笼罩的原始林间溪流场景，光线是清晨的阳光。先从前景开始说：\n\n前景是铺满翠绿色苔藓的河岸，几块深灰带点绿的圆润鹅卵石错落分布在浅溪边缘，石头表面湿润，带着水光。左侧是大片的蕨类植物，叶片是深绿和浅绿相间，纹理清晰，叶片舒展，带着自然的生机。\n\n然后是中景：一条清澈的浅溪从画面深处蜿蜒流向前景，溪水在阳光照射下泛着细碎的金色波光，水流漫过溪底的石块，能看到水下的纹理。溪流两岸覆盖着厚实的苔藓，右侧是几丛叶片圆润、带着嫩绿色新叶的灌木，叶片在光线下显得鲜亮。\n\n背景是高大的古树，树干粗壮，树皮纹理粗糙，树根虬结裸露在地面，枝干向四周伸展，交错的枝叶间，清晨的阳光形成清晰的丁达尔光束，穿透林间的薄雾，光束里能看到细小的尘埃或水汽微粒在浮动，整个背景的树林被薄雾笼罩，营造出朦胧、静谧的氛围，远处的树木在雾气里显得柔和模糊。\n\n整体氛围：静谧、清新，充满原始自然的生机，光线温暖柔和，雾气增添了梦幻感，像是清晨的森林秘境，每一处细节都透着自然的湿润和生机，苔藓、蕨类、溪流、古树和阳光雾气共同构成了治愈的自然场景。\n\n现在把这些整理成连贯的描述，确保细节都到位：\n\n这是一幅充满静谧生机的原始林间晨景图：\n\n前景处，河岸被厚实鲜亮的翠绿色苔藓完全覆盖，几块圆润的深灰调鹅卵石错落分布在浅溪边缘，石面湿润，带着水汽的光泽。画面左侧，大片蕨类植物舒展着叶片，叶片呈现深绿与浅绿交织的自然纹理，叶脉清晰，尽显蓬勃生机。\n\n中景是一条蜿蜒的浅溪，清澈的溪水从林间深处流淌而来，漫过溪底的石块，在晨光的映照下，水面泛着细碎的金色波光，能隐约看到水下的石质纹理。溪流两岸的苔藓同样厚实，右侧生长着几丛叶片圆润的灌木，新生的嫩绿色叶片在光线里显得格外鲜亮，叶片上仿佛还带着晨露的湿润感。\n\n背景是高大的古树林，粗壮的树干带着粗糙的纹理，虬结的树根裸露在地面，遒劲的枝干向四周肆意伸展。林间弥漫着轻薄的晨雾，清晨的阳光穿透枝叶与雾气，形成清晰的丁达尔光束，光束中能看到细小的水汽或尘埃微粒在缓缓浮动，远处的树木在雾气中显得朦胧柔和，为整个场景增添了梦幻感。\n\n整体氛围清新治愈，温暖柔和的光线、湿润的植被、潺潺的溪流与朦胧的雾气，共同营造出原始森林清晨独有的静谧、生机与自然之美。"
      }
    }
  ],
  "created": 1774607219,
  "model": "mimo-v2-omni",
  "object": "chat.completion",
  "usage": {
    "completion_tokens": 1024,
    "prompt_tokens": 1085,
    "total_tokens": 2109,
    "completion_tokens_details": {
      "reasoning_tokens": 714
    },
    "prompt_tokens_details": {
      "cached_tokens": 7,
      "image_tokens": 1024
    }
  }
}
```


<p align="center">
  <small>© 2026 DMXAPI mimo-v2-omni 图片理解</small>
</p>
