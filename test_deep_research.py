#!/usr/bin/env python3
"""
测试Deep Researcher的完整功能
"""

from deep_researcher import DeepResearcher

def test_simple_question():
    print("🔬 测试简单问题的深度研究")
    print("=" * 50)
    
    researcher = DeepResearcher("deepseek-v3")
    researcher.max_rounds = 5  # 限制轮数
    
    question = "什么是注意力机制"
    print(f"问题: {question}")
    
    try:
        result = researcher.research(question)
        print("\n" + "=" * 50)
        print("📊 研究结果:")
        print("=" * 50)
        print(result)
        
        # 统计信息
        print(f"\n📈 统计信息:")
        print(f"- 字符总数: {len(result)}")
        print(f"- 引用数量: {result.count('[citation:')}")
        print(f"- 包含关键词: {'✅' if '注意力' in result or 'attention' in result else '❌'}")
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")

def test_cs_question():
    print("\n🧪 测试计算机科学问题")
    print("=" * 50)
    
    researcher = DeepResearcher("deepseek-v3") 
    researcher.max_rounds = 2
    
    question = "深度学习中的梯度下降算法"
    print(f"问题: {question}")
    
    try:
        result = researcher.research(question)
        print("\n" + "=" * 50)
        print("📊 研究结果:")
        print("=" * 50)
        print(result[:1000] + "..." if len(result) > 1000 else result)
        
        print(f"\n📈 统计信息:")
        print(f"- 字符总数: {len(result)}")
        print(f"- 引用数量: {result.count('[citation:')}")
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")

if __name__ == "__main__":
    print("🚀 Deep Researcher 功能测试")
    print("使用模型: deepseek-v3")
    print("=" * 60)
    
    test_simple_question()
    #test_cs_question()
    
    print("\n✅ 测试完成！")