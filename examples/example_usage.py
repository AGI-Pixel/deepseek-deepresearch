#!/usr/bin/env python3
"""
Deep Researcher 使用示例
展示如何使用Python API进行学术研究
"""

from deep_researcher import DeepResearcher
import time

def example_basic_research():
    """基础研究示例"""
    print("🔬 基础研究示例")
    print("-" * 40)
    
    # 创建研究器实例
    researcher = DeepResearcher("deepseek-v3")
    researcher.max_rounds = 2  # 限制搜索轮数
    
    # 进行研究
    question = "什么是注意力机制"
    print(f"研究问题: {question}")
    
    start_time = time.time()
    result = researcher.research(question)
    end_time = time.time()
    
    # 显示结果
    print(f"\n研究完成，耗时: {end_time - start_time:.1f} 秒")
    print(f"结果长度: {len(result):,} 字符")
    print(f"包含引用: {result.count('[citation:')}) 个")
    
    # 保存结果
    with open("examples/attention_mechanism_research.md", "w", encoding="utf-8") as f:
        f.write(f"# 研究报告：{question}\n\n")
        f.write(f"生成时间：{time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(result)
    
    print("✅ 结果已保存到 examples/attention_mechanism_research.md")

def example_technical_research():
    """技术研究示例"""
    print("\n🛠️ 技术研究示例")
    print("-" * 40)
    
    researcher = DeepResearcher("deepseek-v3")
    researcher.max_rounds = 3
    
    question = "深度学习模型压缩技术对比"
    print(f"研究问题: {question}")
    
    try:
        result = researcher.research(question)
        
        # 分析报告质量
        sections = result.split("##")
        citations = result.count("[citation:")
        
        print(f"\n报告质量分析:")
        print(f"- 章节数: {len([s for s in sections if s.strip()])}")
        print(f"- 引用数: {citations}")
        print(f"- 包含技术分析: {'✅' if '技术' in result else '❌'}")
        print(f"- 包含实践指导: {'✅' if '实践' in result else '❌'}")
        
        # 提取关键信息
        if "## 1. 执行摘要" in result:
            summary_start = result.find("## 1. 执行摘要")
            summary_end = result.find("## 2.", summary_start)
            if summary_end == -1:
                summary_end = summary_start + 300
            summary = result[summary_start:summary_end].strip()
            print(f"\n📋 执行摘要预览:")
            print(summary[:200] + "..." if len(summary) > 200 else summary)
        
    except Exception as e:
        print(f"❌ 研究失败: {e}")

def example_batch_research():
    """批量研究示例"""
    print("\n📚 批量研究示例")
    print("-" * 40)
    
    researcher = DeepResearcher("deepseek-v3")
    researcher.max_rounds = 2
    
    questions = [
        "卷积神经网络的发展历程",
        "生成对抗网络的应用场景",
        "强化学习在游戏AI中的突破"
    ]
    
    results = {}
    
    for i, question in enumerate(questions, 1):
        print(f"\n[{i}/{len(questions)}] 研究: {question}")
        
        try:
            start_time = time.time()
            result = researcher.research(question)
            end_time = time.time()
            
            results[question] = {
                'content': result,
                'duration': end_time - start_time,
                'citations': result.count('[citation:'),
                'length': len(result)
            }
            
            print(f"  ✅ 完成 ({end_time - start_time:.1f}s, {len(result):,}字符)")
            
        except Exception as e:
            print(f"  ❌ 失败: {e}")
            results[question] = {'error': str(e)}
    
    # 生成批量报告摘要
    print(f"\n📊 批量研究摘要:")
    total_time = sum([r.get('duration', 0) for r in results.values()])
    total_citations = sum([r.get('citations', 0) for r in results.values()])
    successful = len([r for r in results.values() if 'content' in r])
    
    print(f"- 总耗时: {total_time:.1f} 秒")
    print(f"- 总引用: {total_citations} 个")
    print(f"- 成功率: {successful}/{len(questions)}")

def example_custom_config():
    """自定义配置示例"""
    print("\n⚙️ 自定义配置示例")
    print("-" * 40)
    
    # 创建自定义配置的研究器
    researcher = DeepResearcher("deepseek-v3")
    
    # 自定义搜索参数
    researcher.max_rounds = 1  # 单轮搜索
    
    # 覆盖搜索工具的参数
    original_search = researcher.search_tool.search_papers
    def custom_search(queries, max_results=3, **kwargs):
        """自定义搜索：限制结果数量"""
        print(f"  🎯 自定义搜索: 每个查询最多{max_results}篇论文")
        return original_search(queries, max_results, **kwargs)
    
    researcher.search_tool.search_papers = custom_search
    
    # 进行研究
    question = "Transformer架构优化技术"
    print(f"研究问题: {question}")
    
    try:
        result = researcher.research(question)
        print(f"✅ 自定义配置研究完成")
        print(f"   结果长度: {len(result):,} 字符")
        print(f"   引用数量: {result.count('[citation:')}")
        
    except Exception as e:
        print(f"❌ 研究失败: {e}")

if __name__ == "__main__":
    print("🚀 Deep Researcher 使用示例")
    print("=" * 60)
    
    # 运行示例
    example_basic_research()
    example_technical_research()
    example_batch_research()
    example_custom_config()
    
    print(f"\n🎉 所有示例运行完成！")
    print("💡 更多使用方法请参考 README.md")