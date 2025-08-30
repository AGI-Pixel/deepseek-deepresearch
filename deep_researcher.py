import time
from typing import List, Dict, Any, Optional
from search_tool import ArxivSearchTool, SearchResult
from llm import LLM

class DeepResearcher:
    def __init__(self, llm_model: str = "gpt-4o"):
        self.llm = LLM(llm_model)
        self.search_tool = ArxivSearchTool()
        self.citations = {}  # citation编号到结果的映射
        self.citation_counter = 0
        self.max_rounds = 5  # 最多搜索轮数
        
    def research(self, user_question: str) -> str:
        """
        执行深度研究，完全基于search_help.html的流程和prompt
        """
        print(f"🔬 开始深度研究: {user_question}")
        print("=" * 50)
        
        current_date = time.strftime("%Y-%m-%d, %A")
        
        # 第一步：初步思考和规划
        print("🧠 第一步：逐步思考和推理")
        initial_analysis = self._initial_thinking(user_question, current_date)
        print(initial_analysis)
        
        all_search_results = []
        search_round = 1
        current_queries = None
        
        # 从初步分析中提取第一轮搜索查询
        first_queries = self._extract_first_search_queries(user_question, initial_analysis)
        current_queries = first_queries
        
        # 开始迭代搜索循环
        while current_queries and search_round <= self.max_rounds:
            print(f"\n🔍 第{search_round}轮搜索")
            print(f"搜索查询: {current_queries}")
            
            # 执行当前轮搜索
            round_results = self._conduct_search_round(current_queries)
            all_search_results.extend(round_results)
            
            # 分析当前轮结果并生成后续查询
            analysis_and_queries = self._analyze_results_and_generate_queries(
                user_question, all_search_results, search_round
            )
            
            print(f"📊 第{search_round}轮分析：")
            print(analysis_and_queries['analysis'])
            
            # 检查是否有后续查询
            next_queries = analysis_and_queries.get('next_queries')
            if next_queries:
                print(f"🔮 发现需要进一步搜索: {next_queries}")
                current_queries = next_queries
                search_round += 1
            else:
                print("✅ 搜索完成，未发现需要进一步研究的问题")
                break
        
        # 生成最终答案
        print(f"\n📝 基于{len(all_search_results)}篇论文生成最终答案...")
        final_answer = self._generate_final_answer(user_question, all_search_results, search_round)
        
        return final_answer
    
    def _initial_thinking(self, question: str, current_date: str) -> str:
        """
        初步思考和推理，完全参考search_help.html的风格
        """
        thinking_prompt = f"""当前日期是{current_date}。你的主要任务是解决用户的问题，根据需要利用适当的工具。

[核心指令：语言一致性]
你必须用与用户问题相同的语言写你的整个回答。
如果用户用中文提问，你必须用中文思考和写作。

你必须首先进行逐步、严格的思考和推理，然后规划搜索策略。

用户的问题是：{question}

请进行逐步分析：
1. 理解问题的核心要求
2. 分解问题的各个关键方面
3. 识别需要搜索的关键信息点
4. 制定搜索策略

请详细分析并说明你的推理过程："""
        
        try:
            return self.llm.response(thinking_prompt)
        except Exception as e:
            return f"初步分析失败: {e}"
    
    def _extract_first_search_queries(self, question: str, analysis: str) -> List[str]:
        """
        从初步分析中提取第一轮搜索查询
        """
        query_prompt = f"""基于以下问题和分析，生成第一轮arXiv搜索查询：

问题：{question}

分析：{analysis}

生成要求（严格遵循search_help.html的规则）：
- 用"||"分隔不同查询，例如："deep learning||neural networks||transformer"
- 使用通用的、搜索引擎友好的、易于检索的关键词
- 避免相对或模糊术语
- 保持查询简短，去除助词、连词和疑问词
- 主要使用关键词组合（空格分隔），不超过15个字符
- 避免特殊标点符号
- 如果涉及多个实体或子问题，分拆为单独查询
- 生成1-5个查询

请只返回查询字符串，无其他内容："""
        
        try:
            response = self.llm.response(query_prompt)
            queries = [q.strip() for q in response.split('||') if q.strip()]
            return queries[:5]
        except Exception as e:
            print(f"提取查询失败: {e}")
            return [question]  # 回退方案
    
    def _conduct_search_round(self, queries: List[str]) -> List[SearchResult]:
        """
        执行一轮搜索
        """
        round_results = []
        
        for query in queries:
            try:
                results = self.search_tool.search_papers([query], max_results=5)
                
                # 为结果分配citation
                for result in results:
                    self.citation_counter += 1
                    citation_key = f"citation:{self.citation_counter}"
                    self.citations[citation_key] = result
                    result.citation = citation_key
                
                round_results.extend(results)
                print(f"  📄 '{query}': {len(results)}篇论文")
                
            except Exception as e:
                print(f"  ❌ '{query}': {e}")
        
        return round_results
    
    def _analyze_results_and_generate_queries(self, question: str, results: List[SearchResult], round_num: int) -> Dict[str, Any]:
        """
        分析搜索结果并自动生成后续查询（如果需要）
        这是关键：LLM自动判断是否需要继续搜索
        """
        if not results:
            return {'analysis': '本轮未找到相关论文。', 'next_queries': None}
        
        # 构建搜索结果信息
        results_text = self._format_search_results(results)
        
        # 关键prompt：让LLM分析并自动决定是否生成后续查询
        analysis_prompt = f"""基于以下第{round_num}轮arXiv搜索结果分析问题：{question}

搜索结果：
{results_text}

请提供：
1. 对当前搜索结果的分析
2. 基于现有信息对问题的回答
3. **重要**：如果当前信息不足以完整回答问题，或发现需要深入研究的新方向，请生成2-3个后续搜索查询

格式要求：
分析：[你的分析内容]

后续查询：[如果需要继续搜索，用"||"分隔查询，例如："query1||query2||query3"。如果不需要继续搜索，写"无"]

请用中文回答："""
        
        try:
            response = self.llm.response(analysis_prompt)
            
            # 解析响应，提取分析和后续查询
            analysis_part = ""
            next_queries = None
            
            if "后续查询：" in response:
                parts = response.split("后续查询：")
                analysis_part = parts[0].replace("分析：", "").strip()
                query_part = parts[1].strip()
                
                if query_part and query_part != "无" and "无" not in query_part:
                    next_queries = [q.strip() for q in query_part.split('||') if q.strip()]
            else:
                analysis_part = response
            
            return {
                'analysis': analysis_part,
                'next_queries': next_queries
            }
            
        except Exception as e:
            return {
                'analysis': f"分析失败: {e}",
                'next_queries': None
            }
    
    def _format_search_results(self, results: List[SearchResult]) -> str:
        """
        格式化搜索结果，参考search_help.html格式，并控制长度
        """
        formatted_text = ""
        for i, result in enumerate(results):
            citation = getattr(result, 'citation', f'citation:{i+1}')
            # 限制每个论文摘要长度
            snippet = result.snippet[:500] + "..." if len(result.snippet) > 500 else result.snippet
            
            paper_info = f"""[paper {i} begin]
[paper title]{result.title}
[paper url]{result.url}
[paper date published]{result.date_published}
[paper authors]{', '.join((result.authors or [])[:5])}  # 最多显示5个作者
[paper snippet begin]
{snippet}
[paper snippet end]
[paper {i} end]

"""
            # 如果总长度超过80k字符，停止添加更多论文
            if len(formatted_text + paper_info) > 80000:
                formatted_text += "\n[更多论文信息已省略，避免内容过长]\n"
                break
            formatted_text += paper_info
            
        return formatted_text
    
    def _generate_final_answer(self, question: str, all_results: List[SearchResult], total_rounds: int) -> str:
        """
        生成最终答案 - 分步处理避免长上下文问题
        """
        if not all_results:
            return "抱歉，未找到相关的学术论文来回答您的问题。"
        
        # 第一步：生成核心研究报告（精简论文信息避免超长）
        core_report = self._generate_core_report(question, all_results)
        
        # 第二步：单独生成引用索引（不依赖LLM）
        citation_index = self._generate_citation_index(all_results)
        
        # 第三步：生成统计信息
        stats_section = self._generate_stats_section(all_results, total_rounds)
        
        # 组合最终报告
        final_report = f"""{core_report}

---

{stats_section}

### 📖 论文引用索引
{citation_index}

---

*本报告基于arXiv学术数据库的实时搜索结果生成，由DeepSeek-v3大语言模型分析整理。*
"""
        
        return final_report
    
    def _generate_core_report(self, question: str, all_results: List[SearchResult]) -> str:
        """
        生成核心研究报告 - 使用精简的论文信息
        """
        # 精简论文信息，只保留关键内容
        simplified_papers = []
        for i, result in enumerate(all_results[:20], 1):  # 最多处理20篇论文
            citation = getattr(result, 'citation', f'citation:{i}')
            simplified_papers.append(f"""
[{citation}] {result.title}
发布: {result.date_published} | 作者: {', '.join((result.authors or [])[:2])}{'等' if len(result.authors or []) > 2 else ''}
摘要: {result.snippet[:200]}{'...' if len(result.snippet) > 200 else ''}
""")
        
        papers_text = '\n'.join(simplified_papers)
        
        # 精简的prompt，专注于核心分析
        report_prompt = f"""基于以下arXiv论文，为技术研发人员生成专业的学术研究报告。

研究问题：{question}

相关论文（精选）：
{papers_text}

请按以下结构生成报告：

# 学术研究报告

## 1. 执行摘要
简明回答问题，总结核心发现和对研发工作的启示。

## 2. 技术背景与现状
分析问题的学术研究现状、关键挑战和发展轨迹。

## 3. 核心技术分析
基于论文证据分析主要技术方法、创新点和实验结果。

## 4. 对比分析与评估
比较不同方法的优缺点、适用场景和技术限制。

## 5. 实践应用指导
提供工程实现建议、技术选型和风险评估。

## 6. 前沿趋势与发展
总结最新动态、未来趋势和技术路线建议。

要求：
- 使用[citation:x]格式引用论文
- 提供具体技术细节
- 面向研发人员，突出实用性
- 用中文撰写，保持专业性

请生成详细报告："""
        
        try:
            return self.llm.response(report_prompt)
        except Exception as e:
            # 如果还是失败，生成基础报告
            return self._generate_fallback_report(question, all_results, str(e))
    
    def _generate_fallback_report(self, question: str, all_results: List[SearchResult], error: str) -> str:
        """
        生成备用报告（当LLM调用失败时）
        """
        return f"""# 学术研究报告

## 执行摘要
基于搜索到的{len(all_results)}篇arXiv论文，针对"{question}"进行了系统性文献调研。

## 搜索结果概览
本次研究共检索了{len(all_results)}篇相关学术论文，涵盖了以下时间范围：
- 最早论文：{min([r.date_published for r in all_results if r.date_published], default='未知')}
- 最新论文：{max([r.date_published for r in all_results if r.date_published], default='未知')}

## 关键发现
通过文献调研发现了以下关键论文：

{self._format_key_findings(all_results[:10])}

## 技术说明
由于模型处理长文本时遇到技术限制（{error}），本报告采用了精简模式。
完整的技术分析请参考下方的论文引用索引，每篇论文都提供了详细的摘要和链接。

## 建议
1. 优先关注近期发表的高相关性论文
2. 深入研究被频繁引用的经典论文
3. 关注不同研究团队的方法对比"""
    
    def _format_key_findings(self, results: List[SearchResult]) -> str:
        """格式化关键发现"""
        findings = ""
        for i, result in enumerate(results, 1):
            citation = getattr(result, 'citation', f'citation:{i}')
            findings += f"\n**{citation}** {result.title}\n*发布于 {result.date_published}*\n{result.snippet[:150]}{'...' if len(result.snippet) > 150 else ''}\n"
        return findings
    
    def _generate_stats_section(self, all_results: List[SearchResult], total_rounds: int) -> str:
        """生成统计信息部分"""
        unique_dates = list(set([r.date_published for r in all_results if r.date_published]))
        unique_categories = list(set([cat for r in all_results for cat in (r.categories or [])]))
        
        return f"""## 📊 研究数据统计

### 🔍 搜索概况
- **搜索轮数**: {total_rounds} 轮迭代搜索
- **检索论文**: {len(all_results)} 篇学术论文
- **时间覆盖**: {min(unique_dates, default='未知')} 至 {max(unique_dates, default='未知')}
- **研究领域**: {len(unique_categories)} 个研究方向

### 📚 主要研究领域
{self._format_categories(unique_categories)}"""
    
    def _generate_citation_index(self, all_results: List[SearchResult]) -> str:
        """生成可点击的论文引用索引"""
        index_text = ""
        for i, result in enumerate(all_results, 1):
            citation = getattr(result, 'citation', f'citation:{i}')
            # 提取citation编号
            citation_num = citation.replace('citation:', '')
            
            authors_text = ', '.join(result.authors[:3] if result.authors else []) + ('等' if len(result.authors or []) > 3 else '')
            
            index_text += f"""
**[{citation}]** {result.title}  
*{authors_text}* | {result.date_published} | [{result.url}]({result.url})  
{result.snippet[:150]}{'...' if len(result.snippet) > 150 else ''}
"""
        
        return index_text
    
    def _format_categories(self, categories: List[str]) -> str:
        """格式化研究领域分类"""
        if not categories:
            return "- 未分类"
        
        # 按频率排序并限制显示数量
        category_text = ""
        for i, cat in enumerate(categories[:8], 1):
            category_text += f"- **{cat}**\n"
        
        if len(categories) > 8:
            category_text += f"- 其他 {len(categories) - 8} 个领域...\n"
        
        return category_text