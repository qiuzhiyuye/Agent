"""
workflow 节点测试
工作流: Query -> Search -> Summarize
"""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Any, Tuple

sys.path.insert(0, str(Path(__file__).parent.parent))

from agent.workflow import Workflow
from agent.llm import call_llm
from agent.node import Node, Flow

from tools.builtins.search import search as search_ddgs



def main() -> None:
    """运行工作流"""

    workflow = Workflow("C++ 最新版本是多少")
    result = workflow.get_result()
    print("Workflow 输出：", result)


if __name__ == "__main__":
    main()
