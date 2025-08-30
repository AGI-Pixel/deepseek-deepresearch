#!/usr/bin/env python3
"""
快速测试脚本
"""

from search_tool import ArxivSearchTool
from llm import LLM

def test_arxiv_search():
    print("🔍 测试arXiv搜索...")
    search_tool = ArxivSearchTool()
    
    # 测试简单搜索
    results = search_tool.search_papers(["transformer"], max_results=3)
    
    print(f"找到 {len(results)} 篇论文:")
    for i, result in enumerate(results, 1):
        print(f"{i}. 标题: {result.title}")
        print(f"   作者: {', '.join(result.authors[:3]) if result.authors else '未知'}")
        print(f"   日期: {result.date_published}")
        print(f"   URL: {result.url}")
        print(f"   摘要: {result.snippet[:100]}...")
        print()

def test_simple_llm():
    print("🤖 测试LLM简单对话...")
    llm = LLM("deepseek-v3")
    
    questions = [
        "什么是Transformer？请简短回答。",
        "列举3个深度学习的应用领域",
        "arXiv是什么？"
    ]
    
    for q in questions:
        print(f"问: {q}")
        response = llm.response(q)
        print(f"答: {response}")
        print("-" * 50)

if __name__ == "__main__":
    print("🚀 快速功能测试")
    print("=" * 40)
    
    test_simple_llm()
    print()
    test_arxiv_search()