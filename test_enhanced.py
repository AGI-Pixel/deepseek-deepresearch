#!/usr/bin/env python3
"""
测试增强版Deep Researcher
"""

from deep_researcher import DeepResearcher

def test_enhanced_report():
    print("🔬 测试增强版研究报告生成")
    print("=" * 60)
    
    researcher = DeepResearcher("deepseek-v3")
    researcher.max_rounds = 2  # 限制轮数节约时间
    
    question = "什么是Transformer架构的核心创新"
    print(f"问题: {question}")
    
    try:
        result = researcher.research(question)
        
        print("\n" + "=" * 60)
        print("📊 增强版研究报告:")
        print("=" * 60)
        
        # 显示前1500字符预览
        print(result[:1500])
        if len(result) > 1500:
            print("\n... [报告已截取前1500字符预览] ...")
        
        # 统计信息
        print(f"\n📈 报告统计:")
        print(f"- 总字符数: {len(result):,}")
        print(f"- 引用数量: {result.count('[citation:')}")
        print(f"- 包含结构: {'✅' if '##' in result else '❌'}")
        print(f"- 包含链接: {'✅' if '](http' in result else '❌'}")
        print(f"- 专业术语: {'✅' if '技术' in result or '算法' in result else '❌'}")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

if __name__ == "__main__":
    success = test_enhanced_report()
    print(f"\n{'✅ 测试成功' if success else '❌ 测试失败'}")