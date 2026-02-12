# Claude Agent SDK 使用文档 支持交互式对话（多轮对话） 
> 使用 ClaudeSDKClient 实现上下文保持
## 安装所需的包
终端运行下面的指令   
`pip install claude_agent-sdk`

## 示例代码
```python
import asyncio
import os
import sys

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

# ============== 请修改以下配置 ==============
BASE_URL = "https://www.dmxapi.cn"  # API 地址（不含 /v1）
API_KEY = "sk-********************************" # API 密钥
MODEL = "claude-opus-4-6-cc"        # 模型名称
PROXY = None                                 # 代理地址，如 "http://127.0.0.1:7897"
# ==========================================

os.environ["ANTHROPIC_BASE_URL"] = BASE_URL
os.environ["ANTHROPIC_API_KEY"] = API_KEY
if PROXY:
    os.environ["HTTP_PROXY"] = PROXY
    os.environ["HTTPS_PROXY"] = PROXY

from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions, AssistantMessage, TextBlock

TOOLS = ["Read", "Write", "Edit", "Glob", "Grep", "Bash", "WebSearch", "WebFetch"]
SYSTEM_PROMPT = "你是一个友好的AI助手。请用中文回复。"


def create_options() -> ClaudeAgentOptions:
    """创建 ClaudeAgentOptions 配置"""
    env = {"ANTHROPIC_BASE_URL": BASE_URL, "ANTHROPIC_API_KEY": API_KEY}
    if PROXY:
        env["HTTP_PROXY"] = PROXY
        env["HTTPS_PROXY"] = PROXY

    return ClaudeAgentOptions(
        system_prompt=SYSTEM_PROMPT,
        max_turns=10,
        allowed_tools=TOOLS,
        permission_mode="bypassPermissions",
        cwd=".",
        model=MODEL,
        env=env,
    )


async def process_response(client: ClaudeSDKClient) -> str:
    """处理并返回响应文本"""
    response_text = ""

    async for message in client.receive_response():
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock) and block.text:
                    if not response_text:
                        response_text = block.text
        elif hasattr(message, "result") and message.result:
            response_text = message.result

    return response_text or "(无响应)"


async def main():
    print("AI 助手（支持多轮对话）| 输入 'exit' 退出\n")

    options = create_options()

    # 使用 ClaudeSDKClient 创建持久会话
    async with ClaudeSDKClient(options=options) as client:
        print("[已连接到 Claude SDK，开始对话...]\n")

        while True:
            try:
                user_input = input("你: ").strip()
                if not user_input:
                    continue
                if user_input.lower() in ['exit', 'quit']:
                    print("\n再见！")
                    break

                # 在同一会话中发送查询（保持上下文）
                await client.query(user_input)

                # 处理响应
                response = await process_response(client)
                print(f"\nAI: {response}\n")

            except (EOFError, KeyboardInterrupt):
                print("\n再见！")
                break
            except Exception as e:
                print(f"\n错误: {type(e).__name__}: {e}\n")


if __name__ == "__main__":
    asyncio.run(main())
```

## 返回示例
> 可以直接在终端与AI进行聊天了   

![claude_sdk](./img/claude_sdk01.png)


<p align="center">
  <small>© 2026 DMXAPI claude agent sdk</small>
</p>
