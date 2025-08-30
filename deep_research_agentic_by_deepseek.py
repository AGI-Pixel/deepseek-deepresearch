#!/usr/bin/env python3
"""
Deep Research Agentic - 基于DeepSeek原生Tool调用规范的实现

这个版本严格遵循DeepSeek的原生tool调用格式，展现真正的Agent能力：
- 使用DeepSeek标准的<|tool▁calls▁begin|>格式
- 模拟DeepSeek的思考过程和推理链
- 展现原生的多轮搜索决策能力
- 对比分析不同实现方式的优劣
"""

import time
import json
import re
from typing import List, Dict, Any, Optional
from search_tool import ArxivSearchTool, SearchResult
from llm import LLM

class DeepSeekAgenticResearcher:
    """
    基于DeepSeek原生Tool调用规范的学术研究Agent
    
    核心特点：
    1. 使用DeepSeek原生的tool调用格式
    2. 让模型自主决策搜索策略和终止条件
    3. 完全依赖模型的推理能力进行研究流程控制
    4. 模拟真实的DeepSeek Agent交互过程
    """
    
    def __init__(self, llm_model: str = "deepseek-v3"):
        self.llm = LLM(llm_model)
        self.search_tool = ArxivSearchTool()
        self.citations = {}
        self.citation_counter = 0
        self.max_rounds = 5
        
        # 构建系统提示词 - 模拟DeepSeek的原生环境
        self.system_prompt = self._build_system_prompt()
        
    def _build_system_prompt(self) -> str:
        """构建DeepSeek原生风格的系统提示词"""
        current_date = time.strftime("%Y-%m-%d, %A")
        
        return f"""The current date is {current_date}. Your primary task is to solve the user's questions, leveraging the appropriate tools as needed.

[Core Instruction: Language Consistency]
You MUST write your entire response in the same language as the user's question.
If the user asks in Chinese, you must think and write in Chinese.

[Core Instruction: Citation Formatting] 
When referencing academic papers from arxiv search results, you must use the format "[citation:x]", where x is the corresponding paper number.

You must first engage in step-by-step, rigorous thinking and reasoning before using the appropriate tool or providing the final answer.

## Tools
You have access to the following tools:

### arxiv_search
Description: Search arXiv for academic papers. Returns a list of relevant research papers with titles, authors, abstracts, and URLs.

Parameters: {{"type": "object", "properties": {{"queries": {{"type": "string", "description": "Generate up to 5 search queries for arXiv based on the research question:\\n\\n- Separate different queries with \\"||\\". For example: \\"deep learning||neural networks||transformer architecture\\".\\n- Use academic terminology and keywords that are commonly used in research papers.\\n- Keep queries focused and specific to improve relevance.\\n- Avoid overly broad or vague terms.\\n- Use English terms as arXiv is primarily in English.\\n- You can search 1 to 5 queries in parallel each time.\\n- If the research question involves multiple aspects or concepts, split them into separate queries.\\n- Do not re-search for queries that have already been searched."}}}}, "required": ["queries"]}}

IMPORTANT: ALWAYS adhere to this exact format for tool use:
<|tool▁calls▁begin|><|tool▁call▁begin|>tool_call_name<|tool▁sep|>tool_call_arguments<|tool▁call▁end|><|tool▁calls▁end|>

Where:
- `tool_call_name` must be "arxiv_search"
- `tool_call_arguments` must be valid JSON that follows the Parameters Schema
- Multiple tool calls can be chained if needed

After using the search tool, you will receive results in this format:
[paper X begin]
[paper title]Title of the paper
[paper url]https://arxiv.org/abs/...
[paper date published]YYYY-MM-DD
[paper authors]Author1, Author2, etc.
[paper snippet begin]
Abstract/summary content...
[paper snippet end]
[paper X end]

Based on these results, you should:
1. Analyze the current search results
2. Determine if additional searches are needed to fully answer the question
3. If more searches are needed, continue with new queries
4. When sufficient information is gathered, provide a comprehensive academic report

Your final report should be structured as a professional academic research report with:
- Executive Summary
- Background and Current State
- Core Technical Analysis  
- Comparative Analysis
- Practical Implementation Guidance
- Future Trends and Development
- Research Statistics
- Citation Index with clickable references"""

    def research(self, user_question: str) -> str:
        """
        执行基于DeepSeek Agent规范的深度研究
        
        这个方法将用户问题直接传递给DeepSeek模型，让模型自主决策：
        1. 何时搜索
        2. 搜索什么内容  
        3. 何时停止搜索
        4. 如何分析和综合结果
        """
        print(f"🤖 启动DeepSeek Agent研究模式")
        print(f"📝 研究问题: {user_question}")
        print("="*60)
        
        # 构建完整的对话上下文
        full_context = f"""{self.system_prompt}

# The user's message is: {user_question}"""
        
        # 开始Agent对话循环
        conversation_history = ""
        current_context = full_context
        round_count = 0
        
        while round_count < self.max_rounds:
            round_count += 1
            print(f"\n🔄 Agent思考轮次 {round_count}")
            print("-" * 40)
            
            try:
                # 调用DeepSeek进行推理和决策
                response = self.llm.response(current_context)
                print(f"🧠 DeepSeek响应:\n{response[:500]}..." if len(response) > 500 else f"🧠 DeepSeek响应:\n{response}")
                
                # 检查是否包含tool调用
                if self._contains_tool_call(response):
                    print("🔧 检测到工具调用，执行搜索...")
                    
                    # 解析并执行tool调用
                    tool_results = self._execute_tool_calls(response)
                    
                    # 更新对话历史
                    conversation_history += f"\n\nAssistant: {response}"
                    conversation_history += f"\n\nTool Results:\n{tool_results}"
                    
                    # 更新上下文，继续对话
                    current_context = f"{full_context}{conversation_history}"
                    
                else:
                    # 没有tool调用，说明Agent认为已经完成研究
                    print("✅ Agent完成研究，生成最终报告")
                    final_report = self._format_final_report(response, user_question)
                    return final_report
                    
            except Exception as e:
                print(f"❌ Agent处理出错: {e}")
                return self._generate_error_report(user_question, str(e))
        
        # 达到最大轮次限制
        print(f"⚠️  达到最大轮次限制({self.max_rounds}轮)，生成当前结果")
        return self._generate_timeout_report(user_question, conversation_history)
    
    def _contains_tool_call(self, response: str) -> bool:
        """检查响应是否包含DeepSeek格式的tool调用"""
        return "<|tool▁calls▁begin|>" in response and "<|tool▁calls▁end|>" in response
    
    def _execute_tool_calls(self, response: str) -> str:
        """解析并执行DeepSeek格式的tool调用"""
        try:
            # 提取tool调用部分
            tool_pattern = r'<\|tool▁calls▁begin\|>(.*?)<\|tool▁calls▁end\|>'
            tool_matches = re.findall(tool_pattern, response, re.DOTALL)
            
            if not tool_matches:
                return "未找到有效的工具调用"
            
            all_results = []
            
            for tool_call_block in tool_matches:
                # 解析每个工具调用
                call_pattern = r'<\|tool▁call▁begin\|>(.*?)<\|tool▁sep\|>(.*?)<\|tool▁call▁end\|>'
                calls = re.findall(call_pattern, tool_call_block, re.DOTALL)
                
                for tool_name, args_str in calls:
                    if tool_name.strip() == "arxiv_search":
                        # 解析参数
                        try:
                            args = json.loads(args_str.strip())
                            queries_str = args.get("queries", "")
                            queries = [q.strip() for q in queries_str.split("||") if q.strip()]
                            
                            print(f"🔍 执行搜索查询: {queries}")
                            
                            # 执行搜索
                            search_results = []
                            for query in queries:
                                results = self.search_tool.search_papers([query], max_results=5)
                                search_results.extend(results)
                            
                            # 格式化搜索结果为DeepSeek期望的格式
                            formatted_results = self._format_search_results_for_deepseek(search_results)
                            all_results.append(formatted_results)
                            
                        except json.JSONDecodeError as e:
                            print(f"❌ 解析工具参数失败: {e}")
                            all_results.append(f"工具调用参数解析失败: {args_str}")
            
            return "\n\n".join(all_results) if all_results else "搜索未返回结果"
            
        except Exception as e:
            print(f"❌ 执行工具调用失败: {e}")
            return f"工具调用执行失败: {str(e)}"
    
    def _format_search_results_for_deepseek(self, results: List[SearchResult]) -> str:
        """将搜索结果格式化为DeepSeek期望的格式"""
        if not results:
            return "未找到相关论文"
        
        formatted_text = ""
        for i, result in enumerate(results):
            # 分配citation编号
            self.citation_counter += 1
            citation_key = f"citation:{self.citation_counter}"
            self.citations[citation_key] = result
            result.citation = citation_key
            
            formatted_text += f"""[paper {i} begin]
[paper title]{result.title}
[paper url]{result.url}
[paper date published]{result.date_published}
[paper authors]{', '.join(result.authors[:5] if result.authors else [])}
[paper snippet begin]
{result.snippet[:800]}{'...' if len(result.snippet) > 800 else ''}
[paper snippet end]
[paper {i} end]

"""
        
        return formatted_text
    
    def _format_final_report(self, agent_response: str, question: str) -> str:
        """格式化Agent的最终响应为标准研究报告"""
        
        # 添加统计信息
        total_papers = len(self.citations)
        unique_dates = list(set([r.date_published for r in self.citations.values() if r.date_published]))
        
        stats_section = f"""

---

## 📊 研究数据统计

### 🔍 搜索概况
- **检索论文**: {total_papers} 篇学术论文
- **时间覆盖**: {min(unique_dates, default='未知')} 至 {max(unique_dates, default='未知')}

### 📚 论文引用索引
{self._generate_citation_index()}

---

*本报告由DeepSeek Agent原生能力生成，展现了大模型在学术研究中的自主决策和推理能力。*
"""
        
        return agent_response + stats_section
    
    def _generate_citation_index(self) -> str:
        """生成引用索引"""
        if not self.citations:
            return "暂无引用"
        
        index_text = ""
        for citation_key, result in self.citations.items():
            authors_text = ', '.join(result.authors[:3] if result.authors else [])
            if len(result.authors or []) > 3:
                authors_text += '等'
            
            index_text += f"""
**[{citation_key}]** {result.title}  
*{authors_text}* | {result.date_published} | [链接]({result.url})  
{result.snippet[:150]}{'...' if len(result.snippet) > 150 else ''}
"""
        
        return index_text
    
    def _generate_error_report(self, question: str, error: str) -> str:
        """生成错误报告"""
        return f"""# DeepSeek Agent 研究报告

## 执行摘要
在使用DeepSeek Agent原生能力研究"{question}"时遇到技术问题。

## 错误信息
```
{error}
```

## 建议
1. 检查网络连接和API配置
2. 确认模型调用参数正确
3. 重试研究请求

---

*DeepSeek Agent模式 - 展现原生AI推理能力*"""

    def _generate_timeout_report(self, question: str, history: str) -> str:
        """生成超时报告"""
        return f"""# DeepSeek Agent 研究报告

## 执行摘要
使用DeepSeek Agent原生能力研究"{question}"，在{self.max_rounds}轮交互中收集了相关信息。

## 研究过程摘要
Agent进行了多轮自主搜索和分析，收集了{len(self.citations)}篇相关论文。

## 主要发现
基于收集的学术论文，以下是主要研究发现：

{self._generate_citation_index()}

## 技术说明
Agent在规定轮次内完成了信息收集，展现了DeepSeek模型的自主研究能力。

---

*DeepSeek Agent模式 - 原生多轮推理与工具调用*"""

    def compare_with_traditional_approach(self, question: str) -> Dict[str, Any]:
        """
        对比分析DeepSeek Agent模式与传统方法的差异
        
        Returns:
            Dict包含两种方法的详细对比结果
        """
        print("🔬 开始对比实验...")
        print("="*50)
        
        # 使用DeepSeek Agent模式
        start_time = time.time()
        agent_result = self.research(question)
        agent_time = time.time() - start_time
        agent_citations = len(self.citations)
        
        # 重置状态，准备传统方法测试
        traditional_citations_backup = self.citations.copy()
        self.citations = {}
        self.citation_counter = 0
        
        # 导入传统方法进行对比
        try:
            from deep_researcher import DeepResearcher
            traditional_researcher = DeepResearcher("deepseek-v3")
            
            start_time = time.time()
            traditional_result = traditional_researcher.research(question)
            traditional_time = time.time() - start_time
            traditional_citations = traditional_researcher.citation_counter
            
        except Exception as e:
            print(f"传统方法测试失败: {e}")
            traditional_result = "传统方法测试失败"
            traditional_time = 0
            traditional_citations = 0
        
        # 恢复Agent结果
        self.citations = traditional_citations_backup
        
        # 生成对比报告
        comparison = {
            "agent_mode": {
                "approach": "DeepSeek原生Agent模式",
                "result": agent_result,
                "time_cost": agent_time,
                "citations_count": agent_citations,
                "autonomy_level": "高 - 完全自主决策",
                "tool_integration": "原生DeepSeek格式",
                "reasoning_transparency": "高 - 展现完整推理过程"
            },
            "traditional_mode": {
                "approach": "传统程序化调用",
                "result": traditional_result,
                "time_cost": traditional_time,
                "citations_count": traditional_citations,
                "autonomy_level": "中 - 预设流程控制",
                "tool_integration": "Python函数封装",
                "reasoning_transparency": "中 - 结构化步骤展示"
            },
            "analysis": {
                "efficiency_comparison": "Agent模式" if agent_time < traditional_time else "传统模式" + "更高效",
                "information_coverage": "Agent模式" if agent_citations > traditional_citations else "传统模式" + "覆盖更全面",
                "user_experience": "Agent模式展现更自然的推理过程，传统模式提供更可控的结构化输出",
                "technical_innovation": "Agent模式更接近真实AI助手体验，展现原生模型能力"
            }
        }
        
        return comparison

def test_deepseek_agent():
    """测试DeepSeek Agent模式"""
    print("🚀 DeepSeek Agent模式测试")
    print("="*50)
    
    # 创建Agent实例
    agent = DeepSeekAgenticResearcher("deepseek-v3")
    
    # 测试问题
    test_questions = [
        "司美格鲁肽和二甲双瓜，哪一个更利于延长寿命",
        "深度学习和机器学习的区别是什么？",
        "Transformer架构的核心创新点有哪些？"
    ]
    
    for question in test_questions:
        print(f"\n📝 测试问题: {question}")
        print("-" * 30)
        
        try:
            result = agent.research(question)
            print(f"✅ 研究完成")
            print(f"📊 报告长度: {len(result):,} 字符")
            print(f"📚 引用论文: {len(agent.citations)} 篇")
            
            # 保存结果
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"deepseek_agent_test_{timestamp}.md"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(f"# DeepSeek Agent模式测试结果\n\n")
                f.write(f"**问题**: {question}\n\n")
                f.write(f"**生成时间**: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                f.write(result)
            
            print(f"💾 结果已保存: {filename}")
            
        except Exception as e:
            print(f"❌ 测试失败: {e}")
        
        # 重置状态
        agent.citations = {}
        agent.citation_counter = 0
        
        print("\n" + "="*50)

if __name__ == "__main__":
    # 运行测试
    test_deepseek_agent()
    
    print("\n🔬 对比分析测试")
    agent = DeepSeekAgenticResearcher("deepseek-v3")
    
    # 执行对比分析
    comparison = agent.compare_with_traditional_approach("什么是注意力机制？")
    
    print("\n📊 对比分析结果:")
    print(json.dumps(comparison["analysis"], indent=2, ensure_ascii=False))