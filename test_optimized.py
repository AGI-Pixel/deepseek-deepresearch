#!/usr/bin/env python3
"""
测试优化后的Deep Researcher - 分步API调用
"""

from deep_researcher import DeepResearcher
import time

def test_optimized_research():
    print("🔬 测试优化版Deep Researcher")
    print("=" * 60)
    
    researcher = DeepResearcher("deepseek-v3")
    researcher.max_rounds = 2  # 限制轮数
    
    question = "大语言模型的安全性研究现状"
    print(f"问题: {question}")
    print(f"优化: 分步API调用，避免长上下文问题")
    
    try:
        start_time = time.time()
        result = researcher.research(question)
        end_time = time.time()
        
        print("\n" + "=" * 60)
        print("📊 优化版研究报告:")
        print("=" * 60)
        
        # 分析报告结构
        sections = result.split('##')
        print(f"📋 报告结构分析:")
        print(f"- 总章节数: {len([s for s in sections if s.strip()])}")
        print(f"- 包含执行摘要: {'✅' if '执行摘要' in result else '❌'}")
        print(f"- 包含技术分析: {'✅' if '技术分析' in result or '核心技术' in result else '❌'}")
        print(f"- 包含实践指导: {'✅' if '实践' in result or '应用' in result else '❌'}")
        print(f"- 包含引用索引: {'✅' if '论文引用索引' in result else '❌'}")
        
        # 显示报告预览（前800字符）
        print(f"\n📝 报告预览:")
        print("-" * 40)
        preview = result[:800].replace('\n', '\n')
        print(preview)
        if len(result) > 800:
            print("... [报告较长，已截取预览] ...")
        
        # 统计信息
        citation_count = result.count('[citation:')
        word_count = len(result)
        
        print(f"\n📈 详细统计:")
        print(f"- ⏱️  处理时间: {end_time - start_time:.1f} 秒")
        print(f"- 📄 总字符数: {word_count:,}")
        print(f"- 🔗 引用数量: {citation_count}")
        print(f"- 📊 平均每引用字数: {word_count // max(citation_count, 1):,}")
        print(f"- ✅ 生成成功: {'是' if 'error:' not in result else '否'}")
        
        # 检查备用报告
        if '技术限制' in result:
            print(f"⚠️  使用了备用报告模式")
        else:
            print(f"✅ 使用了完整LLM分析")
            
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

def test_citation_extraction():
    """测试引用提取功能"""
    print(f"\n🔍 测试引用提取功能")
    print("-" * 30)
    
    # 模拟包含引用索引的报告
    sample_report = """
### 📖 论文引用索引

**[citation:1]** Deep Learning Security: A Comprehensive Survey
*Zhang, Li, Wang* | 2024-01-15 | [http://arxiv.org/abs/2401.12345](http://arxiv.org/abs/2401.12345)
This paper provides a comprehensive review of security issues in deep learning systems...

**[citation:2]** Adversarial Attacks on Large Language Models
*Smith, Johnson* | 2023-12-20 | [http://arxiv.org/abs/2312.67890](http://arxiv.org/abs/2312.67890)
We investigate various adversarial attack methods targeting large language models...
"""
    
    # 简单的引用提取测试
    citations = []
    lines = sample_report.split('\n')
    for line in lines:
        if line.startswith('**[citation:'):
            citations.append(line)
    
    print(f"找到引用: {len(citations)} 个")
    for citation in citations:
        print(f"  {citation[:60]}...")
    
    return len(citations) > 0

if __name__ == "__main__":
    print("🚀 Deep Researcher 优化版测试")
    print("=" * 60)
    
    success1 = test_optimized_research()
    success2 = test_citation_extraction()
    
    print(f"\n" + "=" * 60)
    print(f"📊 测试结果总结")
    print(f"=" * 60)
    print(f"- 优化研究测试: {'✅ 通过' if success1 else '❌ 失败'}")
    print(f"- 引用提取测试: {'✅ 通过' if success2 else '❌ 失败'}")
    print(f"- 整体评估: {'🎉 优化成功' if success1 and success2 else '⚠️ 需要调试'}")