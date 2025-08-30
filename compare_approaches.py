#!/usr/bin/env python3
"""
对比分析：传统方法 vs DeepSeek Agent原生模式

这个脚本用于系统性地对比两种不同的Deep Research实现方式：
1. 传统的程序化调用方式 (deep_researcher.py)
2. DeepSeek Agent原生tool调用方式 (deep_research_agentic_by_deepseek.py)

通过多个测试用例来分析两种方法在效率、准确性、用户体验等方面的差异。
"""

import time
import json
from typing import Dict, List, Any
from deep_researcher import DeepResearcher
from deep_research_agentic_by_deepseek import DeepSeekAgenticResearcher

class ApproachComparator:
    """方法对比器 - 系统性对比两种研究方法"""
    
    def __init__(self):
        self.traditional_researcher = DeepResearcher("deepseek-v3")
        self.agent_researcher = DeepSeekAgenticResearcher("deepseek-v3")
        
        # 测试用例
        self.test_cases = [
            {
                "id": "basic_concept",
                "question": "什么是注意力机制？",
                "category": "基础概念",
                "expected_aspects": ["定义", "原理", "应用", "发展历程"]
            },
            {
                "id": "technical_comparison", 
                "question": "CNN和Transformer在计算机视觉中的优缺点对比",
                "category": "技术对比",
                "expected_aspects": ["架构差异", "性能对比", "适用场景", "计算复杂度"]
            },
            {
                "id": "frontier_research",
                "question": "大语言模型的最新优化技术有哪些？",
                "category": "前沿研究", 
                "expected_aspects": ["最新进展", "技术创新", "性能提升", "未来趋势"]
            }
        ]
        
    def run_comprehensive_comparison(self) -> Dict[str, Any]:
        """运行全面的对比分析"""
        print("🔬 启动全面对比分析")
        print("="*60)
        
        comparison_results = {
            "test_results": [],
            "overall_analysis": {},
            "recommendations": {}
        }
        
        for test_case in self.test_cases:
            print(f"\n📝 测试用例: {test_case['question']}")
            print(f"📂 类别: {test_case['category']}")
            print("-" * 50)
            
            # 执行对比测试
            case_result = self._compare_single_case(test_case)
            comparison_results["test_results"].append(case_result)
            
            print(f"✅ 测试完成: {test_case['id']}")
        
        # 生成整体分析
        comparison_results["overall_analysis"] = self._generate_overall_analysis(
            comparison_results["test_results"]
        )
        
        # 生成使用建议
        comparison_results["recommendations"] = self._generate_recommendations(
            comparison_results["overall_analysis"]
        )
        
        return comparison_results
    
    def _compare_single_case(self, test_case: Dict[str, Any]) -> Dict[str, Any]:
        """对比单个测试用例"""
        question = test_case["question"]
        
        # 测试传统方法
        print("🔧 测试传统方法...")
        traditional_result = self._test_traditional_approach(question)
        
        print("🤖 测试DeepSeek Agent方法...")  
        agent_result = self._test_agent_approach(question)
        
        # 分析结果质量
        quality_analysis = self._analyze_result_quality(
            traditional_result, agent_result, test_case["expected_aspects"]
        )
        
        return {
            "test_case": test_case,
            "traditional_result": traditional_result,
            "agent_result": agent_result,
            "quality_analysis": quality_analysis
        }
    
    def _test_traditional_approach(self, question: str) -> Dict[str, Any]:
        """测试传统方法"""
        try:
            start_time = time.time()
            
            # 重置状态
            self.traditional_researcher.citations = {}
            self.traditional_researcher.citation_counter = 0
            
            result = self.traditional_researcher.research(question)
            end_time = time.time()
            
            return {
                "success": True,
                "result": result,
                "time_cost": end_time - start_time,
                "citations_count": self.traditional_researcher.citation_counter,
                "result_length": len(result),
                "approach": "传统程序化调用"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "time_cost": 0,
                "citations_count": 0,
                "result_length": 0,
                "approach": "传统程序化调用"
            }
    
    def _test_agent_approach(self, question: str) -> Dict[str, Any]:
        """测试Agent方法"""
        try:
            start_time = time.time()
            
            # 重置状态
            self.agent_researcher.citations = {}
            self.agent_researcher.citation_counter = 0
            
            result = self.agent_researcher.research(question)
            end_time = time.time()
            
            return {
                "success": True,
                "result": result,
                "time_cost": end_time - start_time,
                "citations_count": len(self.agent_researcher.citations),
                "result_length": len(result),
                "approach": "DeepSeek Agent原生模式"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "time_cost": 0,
                "citations_count": 0,
                "result_length": 0,
                "approach": "DeepSeek Agent原生模式"
            }
    
    def _analyze_result_quality(self, traditional: Dict, agent: Dict, expected_aspects: List[str]) -> Dict[str, Any]:
        """分析结果质量"""
        quality_metrics = {
            "completeness": {},
            "accuracy": {},
            "structure": {},
            "usability": {}
        }
        
        # 完整性分析
        if traditional["success"] and agent["success"]:
            trad_coverage = self._calculate_aspect_coverage(traditional["result"], expected_aspects)
            agent_coverage = self._calculate_aspect_coverage(agent["result"], expected_aspects)
            
            quality_metrics["completeness"] = {
                "traditional": trad_coverage,
                "agent": agent_coverage,
                "winner": "agent" if agent_coverage > trad_coverage else "traditional" if trad_coverage > agent_coverage else "tie"
            }
        
        # 效率分析
        if traditional["success"] and agent["success"]:
            quality_metrics["efficiency"] = {
                "traditional_time": traditional["time_cost"],
                "agent_time": agent["time_cost"],
                "winner": "agent" if agent["time_cost"] < traditional["time_cost"] else "traditional",
                "time_diff": abs(traditional["time_cost"] - agent["time_cost"])
            }
        
        # 信息丰富度分析
        quality_metrics["information_richness"] = {
            "traditional_citations": traditional["citations_count"],
            "agent_citations": agent["citations_count"],
            "traditional_length": traditional["result_length"],
            "agent_length": agent["result_length"],
            "winner": "agent" if agent["citations_count"] > traditional["citations_count"] else "traditional"
        }
        
        return quality_metrics
    
    def _calculate_aspect_coverage(self, result: str, expected_aspects: List[str]) -> float:
        """计算内容覆盖度"""
        if not result:
            return 0.0
        
        result_lower = result.lower()
        covered_aspects = 0
        
        for aspect in expected_aspects:
            # 简单的关键词匹配检测
            if aspect.lower() in result_lower or self._contains_related_terms(result_lower, aspect.lower()):
                covered_aspects += 1
        
        return covered_aspects / len(expected_aspects) if expected_aspects else 0.0
    
    def _contains_related_terms(self, text: str, aspect: str) -> bool:
        """检查是否包含相关术语"""
        related_terms = {
            "定义": ["概念", "是什么", "定义为", "指的是"],
            "原理": ["工作原理", "机制", "如何工作", "基本原理"],
            "应用": ["应用场景", "使用", "用于", "应用在"],
            "发展历程": ["历史", "发展", "演进", "起源"],
            "架构差异": ["结构", "架构", "模型", "设计"],
            "性能对比": ["性能", "效果", "准确率", "速度"],
            "适用场景": ["适用", "场景", "应用", "使用"],
            "计算复杂度": ["复杂度", "计算量", "效率", "速度"],
            "最新进展": ["最新", "新技术", "最近", "进展"],
            "技术创新": ["创新", "新方法", "突破", "改进"],
            "性能提升": ["提升", "改善", "优化", "增强"],
            "未来趋势": ["趋势", "未来", "方向", "展望"]
        }
        
        if aspect in related_terms:
            return any(term in text for term in related_terms[aspect])
        return False
    
    def _generate_overall_analysis(self, test_results: List[Dict]) -> Dict[str, Any]:
        """生成整体分析"""
        analysis = {
            "success_rates": {},
            "performance_comparison": {},
            "quality_comparison": {},
            "use_case_recommendations": {}
        }
        
        # 成功率统计
        traditional_successes = sum(1 for r in test_results if r["traditional_result"]["success"])
        agent_successes = sum(1 for r in test_results if r["agent_result"]["success"])
        total_tests = len(test_results)
        
        analysis["success_rates"] = {
            "traditional": traditional_successes / total_tests,
            "agent": agent_successes / total_tests,
            "total_tests": total_tests
        }
        
        # 性能对比
        successful_tests = [r for r in test_results if r["traditional_result"]["success"] and r["agent_result"]["success"]]
        
        if successful_tests:
            avg_traditional_time = sum(r["traditional_result"]["time_cost"] for r in successful_tests) / len(successful_tests)
            avg_agent_time = sum(r["agent_result"]["time_cost"] for r in successful_tests) / len(successful_tests)
            
            avg_traditional_citations = sum(r["traditional_result"]["citations_count"] for r in successful_tests) / len(successful_tests)
            avg_agent_citations = sum(r["agent_result"]["citations_count"] for r in successful_tests) / len(successful_tests)
            
            analysis["performance_comparison"] = {
                "average_time": {
                    "traditional": avg_traditional_time,
                    "agent": avg_agent_time,
                    "faster": "agent" if avg_agent_time < avg_traditional_time else "traditional"
                },
                "average_citations": {
                    "traditional": avg_traditional_citations,
                    "agent": avg_agent_citations,
                    "more_comprehensive": "agent" if avg_agent_citations > avg_traditional_citations else "traditional"
                }
            }
        
        return analysis
    
    def _generate_recommendations(self, overall_analysis: Dict) -> Dict[str, Any]:
        """生成使用建议"""
        recommendations = {
            "traditional_approach": {
                "best_for": [],
                "advantages": [],
                "limitations": []
            },
            "agent_approach": {
                "best_for": [],
                "advantages": [],
                "limitations": []
            },
            "selection_guide": {}
        }
        
        # 基于分析结果生成建议
        perf_comp = overall_analysis.get("performance_comparison", {})
        
        # 传统方法建议
        recommendations["traditional_approach"]["advantages"] = [
            "结构化的研究流程",
            "可预测的执行步骤", 
            "易于调试和优化",
            "稳定的输出格式"
        ]
        
        recommendations["traditional_approach"]["best_for"] = [
            "需要标准化输出格式的场景",
            "对执行流程有严格要求的环境",
            "批量处理和自动化集成"
        ]
        
        recommendations["traditional_approach"]["limitations"] = [
            "缺乏真正的智能决策",
            "搜索策略相对固化",
            "难以适应复杂多变的研究需求"
        ]
        
        # Agent方法建议
        recommendations["agent_approach"]["advantages"] = [
            "展现真正的AI推理能力",
            "自主的搜索决策",
            "更自然的交互体验",
            "接近人类研究者的思考过程"
        ]
        
        recommendations["agent_approach"]["best_for"] = [
            "探索性研究任务",
            "需要灵活搜索策略的场景",
            "展示AI Agent能力的Demo",
            "研究复杂或开放性问题"
        ]
        
        recommendations["agent_approach"]["limitations"] = [
            "输出格式可能不够标准化",
            "执行时间可能更长",
            "需要更强的模型推理能力",
            "调试和优化相对困难"
        ]
        
        # 选择指南
        recommendations["selection_guide"] = {
            "choose_traditional_when": [
                "需要稳定可靠的生产环境",
                "对输出格式有严格要求",
                "需要快速响应的应用场景"
            ],
            "choose_agent_when": [
                "展示AI能力和技术创新",
                "处理复杂的研究问题",
                "用户体验和交互性更重要"
            ]
        }
        
        return recommendations
    
    def generate_comparison_report(self, results: Dict[str, Any]) -> str:
        """生成对比分析报告"""
        report = f"""# Deep Research 方法对比分析报告

## 📊 执行摘要

本报告对比了两种Deep Research实现方法：
- **传统程序化调用方式** (deep_researcher.py)
- **DeepSeek Agent原生模式** (deep_research_agentic_by_deepseek.py)

通过{len(results['test_results'])}个测试用例的系统性对比，分析两种方法的优缺点和适用场景。

## 🔍 测试结果概览

### 成功率对比
- **传统方法**: {results['overall_analysis']['success_rates']['traditional']:.1%}
- **Agent方法**: {results['overall_analysis']['success_rates']['agent']:.1%}

### 性能对比
"""
        
        if "performance_comparison" in results['overall_analysis']:
            perf = results['overall_analysis']['performance_comparison']
            report += f"""
**平均执行时间**:
- 传统方法: {perf['average_time']['traditional']:.1f}秒
- Agent方法: {perf['average_time']['agent']:.1f}秒
- 更快的方法: {perf['average_time']['faster']}

**平均引用数量**:
- 传统方法: {perf['average_citations']['traditional']:.1f}篇
- Agent方法: {perf['average_citations']['agent']:.1f}篇  
- 更全面的方法: {perf['average_citations']['more_comprehensive']}
"""
        
        # 详细测试结果
        report += "\n## 📋 详细测试结果\n"
        
        for i, result in enumerate(results['test_results'], 1):
            test_case = result['test_case']
            report += f"""
### {i}. {test_case['question']}
**类别**: {test_case['category']}

**传统方法**:
- 成功: {'✅' if result['traditional_result']['success'] else '❌'}
- 时间: {result['traditional_result']['time_cost']:.1f}秒
- 引用: {result['traditional_result']['citations_count']}篇
- 长度: {result['traditional_result']['result_length']:,}字符

**Agent方法**:
- 成功: {'✅' if result['agent_result']['success'] else '❌'}
- 时间: {result['agent_result']['time_cost']:.1f}秒  
- 引用: {result['agent_result']['citations_count']}篇
- 长度: {result['agent_result']['result_length']:,}字符
"""
        
        # 使用建议
        recommendations = results['recommendations']
        report += f"""
## 🎯 使用建议

### 传统程序化方法 适用场景:
{chr(10).join(f"- {item}" for item in recommendations['traditional_approach']['best_for'])}

**优势**:
{chr(10).join(f"- {item}" for item in recommendations['traditional_approach']['advantages'])}

**局限性**:
{chr(10).join(f"- {item}" for item in recommendations['traditional_approach']['limitations'])}

### DeepSeek Agent原生模式 适用场景:
{chr(10).join(f"- {item}" for item in recommendations['agent_approach']['best_for'])}

**优势**:
{chr(10).join(f"- {item}" for item in recommendations['agent_approach']['advantages'])}

**局限性**:
{chr(10).join(f"- {item}" for item in recommendations['agent_approach']['limitations'])}

## 🚀 选择指南

**选择传统方法当**:
{chr(10).join(f"- {item}" for item in recommendations['selection_guide']['choose_traditional_when'])}

**选择Agent方法当**:
{chr(10).join(f"- {item}" for item in recommendations['selection_guide']['choose_agent_when'])}

## 🔮 结论

两种方法各有优势，应该根据具体使用场景选择：

- **传统方法**更适合生产环境和标准化需求
- **Agent方法**更适合展示AI能力和处理复杂问题

未来的发展方向可能是结合两种方法的优势，既保持Agent的智能决策能力，又提供传统方法的稳定性和可控性。

---

*报告生成时间: {time.strftime('%Y-%m-%d %H:%M:%S')}*
*测试环境: DeepSeek-v3模型*
"""
        
        return report

def main():
    """主函数 - 执行完整的对比分析"""
    print("🚀 Deep Research 方法对比分析")
    print("="*60)
    
    # 创建对比器
    comparator = ApproachComparator()
    
    # 运行对比分析
    results = comparator.run_comprehensive_comparison()
    
    # 生成报告
    report = comparator.generate_comparison_report(results)
    
    # 保存报告
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    filename = f"deep_research_comparison_{timestamp}.md"
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(report)
    
    print(f"\n📊 对比分析完成!")
    print(f"📄 详细报告已保存: {filename}")
    
    # 输出简要结果
    print("\n🎯 简要结论:")
    overall = results['overall_analysis']
    print(f"- 传统方法成功率: {overall['success_rates']['traditional']:.1%}")
    print(f"- Agent方法成功率: {overall['success_rates']['agent']:.1%}")
    
    if "performance_comparison" in overall:
        perf = overall['performance_comparison']
        print(f"- 平均时间对比: 传统 {perf['average_time']['traditional']:.1f}s vs Agent {perf['average_time']['agent']:.1f}s")
        print(f"- 平均引用对比: 传统 {perf['average_citations']['traditional']:.1f} vs Agent {perf['average_citations']['agent']:.1f}")
    
    print(f"\n💡 建议查看完整报告以获取详细分析: {filename}")

if __name__ == "__main__":
    main()