"""
workflow.py - 搜索工作流 
工作流: Query -> Search -> Summarize
"""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Any, Tuple

sys.path.insert(0, str(Path(__file__).parent.parent))

from .llm import call_llm
from .node import Node, Flow
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



class Workflow():
    def __init__(self, question : str) -> None:
      self.query = QueryNode()
      self.search = SearchNode()
      self.summarize = SummarizeNode()
      self.question = question


    def get_result(self):
      self.query - "search" >> self.search
      self.search - "summarize" >> self.summarize

      flow = Flow(self.query)
      _, result = flow.run(self.question)
      self.result = result
      return self.result




