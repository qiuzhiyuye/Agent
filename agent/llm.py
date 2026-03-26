from __future__ import annotations

import os
from typing import Any

from openai import OpenAI


def call_llm(
    prompt: str | None = None,
    messages: list[dict[str, Any]] | None = None,
    tools: list[dict[str, Any]] | None = None,
    system_prompt: str | None = None,
) -> str | dict[str, Any]:

    # 尝试加载 API Key: 环境变量 -> 本地 key.txt
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        # 假设当前文件在 Agent/agent/llm.py，向上两级找到 Agent/key.txt
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)
        key_file = os.path.join(project_root, "key.txt")
        if os.path.exists(key_file):
            with open(key_file, "r", encoding="utf-8") as f:
                api_key = f.read().strip()

    
    base_url = os.environ.get("OPENAI_BASE_URL", "https://open.bigmodel.cn/api/paas/v4/")

    client = OpenAI(
        api_key=api_key,
        base_url=base_url,
    )

    if messages is not None:
        msgs = list(messages)
    elif prompt is not None:
        msgs = [{"role": "user", "content": prompt}]
    else:
        raise ValueError("Either prompt or messages must be provided")

    if system_prompt:
        msgs = [{"role": "system", "content": system_prompt}, *msgs]

    kwargs: dict[str, Any] = {
        "model": os.environ.get("LLM_MODEL", "glm-4-flash"),
        "messages": msgs,
    }
    if tools:
        kwargs["tools"] = tools
        kwargs["tool_choice"] = "auto"

    response = client.chat.completions.create(**kwargs)
    message = response.choices[0].message

    # 兼容老示例（chatbot/workflow）: 只要是简单 prompt 模式就返回字符串
    if messages is None and tools is None and system_prompt is None:
        return message.content or ""

    result: dict[str, Any] = {
        "role": "assistant",
        "content": message.content or "",
    }

    reasoning_content = getattr(message, "reasoning_content", None)
    if reasoning_content:
        result["reasoning_content"] = reasoning_content

    if message.tool_calls:
        result["tool_calls"] = [tool_call.model_dump() for tool_call in message.tool_calls]

    return result


if __name__ == "__main__":
    print("Basic:", call_llm("用一句话解释什么是 Agent。"))
