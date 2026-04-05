"""
Node 节点测试
工作流: Query -> Search -> Summarize
"""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Any, Tuple

sys.path.insert(0, str(Path(__file__).parent.parent))

from agent.llm import call_llm
from agent.node import Node, Flow
from tools.builtins.search import search as search_ddgs


class QueryNode(Node):
    """查询节点"""

    def exec(self, payload: Any) -> Tuple[str, Any]:
        return "search", str(payload)


class SearchNode(Node):
    """搜索节点"""

    def exec(self, payload: Any) -> Tuple[str, Any]:
        results = search_ddgs(str(payload), max_results=3)
        titles = [r.get("title") or r.get("body") or "" for r in results]
        summary_input = " | ".join([t for t in titles if t])
        return "summarize", summary_input


class SummarizeNode(Node):
    """总结节点"""

    def exec(self, payload: Any) -> Tuple[str, Any]:
        prompt = f"基于以下要点写一句话摘要：{payload}"
        text = call_llm(prompt)
        return "default", text


def main() -> None:
    """运行工作流"""

    query = QueryNode()
    search = SearchNode()
    summarize = SummarizeNode()

    query - "search" >> search
    search - "summarize" >> summarize

    flow = Flow(query)
    _, result = flow.run("大模型是什么")
    print("Workflow 输出：", result)


if __name__ == "__main__":
    main()
