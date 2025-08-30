#!/usr/bin/env python3
"""
Deep Researcher 系统测试脚本
使用deepseek-v3模型进行真实测试
"""

import sys
import time
from deep_researcher import DeepResearcher

def test_llm_connection():
    """测试LLM连接"""
    print("🔗 测试LLM连接...")
    try:
        from llm import LLM
        llm = LLM("deepseek-v3")
        response = llm.response("你好，请简短回复确认你能正常工作。")
        print(f"✅ LLM连接成功，回复: {response}")
        return True
    except Exception as e:
        print(f"❌ LLM连接失败: {e}")
        return False

def test_arxiv_search():
    """测试arXiv搜索功能"""
    print("\n🔍 测试arXiv搜索功能...")
    try:
        from search_tool import ArxivSearchTool
        search_tool = ArxivSearchTool()
        
        # 测试查询生成
        queries = search_tool.generate_search_queries("深度学习", max_queries=3)
        print(f"✅ 查询生成成功: {queries}")
        
        # 测试搜索功能
        results = search_tool.search_papers(["deep learning"], max_results=3)
        print(f"✅ 搜索成功，找到 {len(results)} 篇论文")
        
        if results:
            print(f"   示例论文: {results[0].title}")
        
        return True
    except Exception as e:
        print(f"❌ arXiv搜索测试失败: {e}")
        return False

def test_simple_research():
    """测试简单研究功能"""
    print("\n🧪 测试简单研究功能...")
    try:
        researcher = DeepResearcher("deepseek-v3")
        researcher.max_rounds = 2  # 限制轮数以节省时间
        
        test_question = "什么是Transformer架构"
        print(f"测试问题: {test_question}")
        
        result = researcher.research(test_question)
        
        print("✅ 研究完成！")
        print("📊 结果长度:", len(result), "字符")
        
        if len(result) > 100:
            print("📝 结果预览:", result[:200] + "...")
        else:
            print("📝 完整结果:", result)
            
        return True
    except Exception as e:
        print(f"❌ 简单研究测试失败: {e}")
        return False

def test_complex_research():
    """测试复杂研究功能"""
    print("\n🎯 测试复杂研究功能...")
    try:
        researcher = DeepResearcher("deepseek-v3")
        researcher.max_rounds = 3
        
        test_question = "大语言模型在代码生成任务中的最新进展和挑战"
        print(f"测试问题: {test_question}")
        
        start_time = time.time()
        result = researcher.research(test_question)
        end_time = time.time()
        
        print(f"✅ 复杂研究完成！耗时: {end_time - start_time:.1f} 秒")
        print("📊 结果统计:")
        print(f"   - 字符数: {len(result)}")
        print(f"   - 引用数: {result.count('[citation:')}")
        
        # 显示结果的关键部分
        lines = result.split('\n')
        print("📝 结果摘要:")
        for line in lines[:5]:
            if line.strip():
                print(f"   {line[:100]}...")
                
        return True
    except Exception as e:
        print(f"❌ 复杂研究测试失败: {e}")
        return False

def interactive_test():
    """交互式测试"""
    print("\n🎮 进入交互式测试模式")
    print("💡 你可以输入任何问题来测试系统")
    print("📝 输入 'quit' 退出交互测试")
    print("-" * 50)
    
    researcher = DeepResearcher("deepseek-v3")
    researcher.max_rounds = 3
    
    while True:
        try:
            question = input("\n❓ 请输入测试问题: ").strip()
            
            if not question:
                continue
                
            if question.lower() in ['quit', 'exit', 'q']:
                print("👋 退出交互测试")
                break
            
            print(f"\n🔬 开始研究: {question}")
            print("=" * 50)
            
            start_time = time.time()
            result = researcher.research(question)
            end_time = time.time()
            
            print("\n" + "=" * 50)
            print("📊 测试结果")
            print("=" * 50)
            print(result)
            print(f"\n⏱️ 耗时: {end_time - start_time:.1f} 秒")
            
        except KeyboardInterrupt:
            print("\n\n👋 用户中断测试")
            break
        except Exception as e:
            print(f"\n❌ 测试过程出错: {e}")

def main():
    print("🚀 Deep Researcher 系统测试")
    print("使用模型: deepseek-v3")
    print("=" * 50)
    
    # 运行所有测试
    tests = [
        ("LLM连接测试", test_llm_connection),
        ("arXiv搜索测试", test_arxiv_search),
        ("简单研究测试", test_simple_research),
        ("复杂研究测试", test_complex_research),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n🧪 执行 {test_name}...")
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"❌ {test_name} 执行异常: {e}")
            results.append((test_name, False))
    
    # 显示测试总结
    print("\n" + "=" * 50)
    print("📊 测试总结")
    print("=" * 50)
    
    passed = 0
    for test_name, success in results:
        status = "✅ 通过" if success else "❌ 失败"
        print(f"{test_name}: {status}")
        if success:
            passed += 1
    
    print(f"\n总计: {passed}/{len(results)} 测试通过")
    
    # 询问是否进入交互测试
    if passed > 0:
        try:
            choice = input(f"\n🎮 是否进入交互式测试模式？(y/n): ").strip().lower()
            if choice in ['y', 'yes']:
                interactive_test()
        except KeyboardInterrupt:
            print("\n👋 测试结束")

if __name__ == "__main__":
    main()