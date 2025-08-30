import requests
import xml.etree.ElementTree as ET
from typing import List, Dict, Any
from dataclasses import dataclass
import time
import re
from urllib.parse import quote

@dataclass
class SearchResult:
    title: str
    url: str
    snippet: str
    content: str = ""
    date_published: str = ""
    authors: List[str] = None
    categories: List[str] = None
    paper_id: str = ""

class ArxivSearchTool:
    def __init__(self):
        self.search_history = []
        self.searched_queries = set()
        self.base_url = "http://export.arxiv.org/api/query"
    
    def generate_search_queries(self, question: str, max_queries: int = 5) -> List[str]:
        """
        根据问题生成arXiv搜索查询
        """
        queries = []
        
        # 清理问题，移除中文停用词
        stop_words = ['什么', '如何', '为什么', '哪个', '怎么', '谁', '什么时候', '在哪里', '的', '是', '在', '有']
        question_cleaned = question
        for word in stop_words:
            question_cleaned = question_cleaned.replace(word, '')
        
        # 生成主查询
        main_query = question_cleaned.strip()
        if main_query and main_query not in self.searched_queries:
            queries.append(main_query)
        
        # 如果是中文查询，也尝试英文关键词
        if re.search(r'[\u4e00-\u9fff]', question):
            # 这里可以添加中英文术语对照表
            english_terms = self._translate_to_english_terms(question)
            for term in english_terms:
                if term not in self.searched_queries and len(queries) < max_queries:
                    queries.append(term)
        
        # 生成更具体的查询
        words = question_cleaned.split()
        if len(words) >= 2:
            for i in range(min(3, len(words)-1)):
                sub_query = ' '.join(words[i:i+2])
                if sub_query and sub_query not in self.searched_queries and len(queries) < max_queries:
                    queries.append(sub_query)
        
        return queries[:max_queries]
    
    def _translate_to_english_terms(self, chinese_text: str) -> List[str]:
        """
        将中文术语转换为英文搜索词
        """
        # 常见学术术语对照表
        term_map = {
            '深度学习': 'deep learning',
            '机器学习': 'machine learning', 
            '人工智能': 'artificial intelligence',
            '神经网络': 'neural network',
            '自然语言处理': 'natural language processing',
            '计算机视觉': 'computer vision',
            '强化学习': 'reinforcement learning',
            '大语言模型': 'large language model',
            '变换器': 'transformer',
            '注意力机制': 'attention mechanism',
            '卷积神经网络': 'convolutional neural network',
            '生成对抗网络': 'generative adversarial network',
        }
        
        english_terms = []
        for chinese, english in term_map.items():
            if chinese in chinese_text:
                english_terms.append(english)
        
        return english_terms
    
    def search_papers(self, queries: List[str], max_results: int = 10, 
                     date_from: str = None, categories: List[str] = None) -> List[SearchResult]:
        """
        搜索arXiv论文
        """
        all_results = []
        
        for query in queries:
            if query in self.searched_queries:
                continue
                
            self.searched_queries.add(query)
            print(f"🔍 搜索arXiv论文: {query}")
            
            try:
                results = self._search_arxiv_api(query, max_results, date_from, categories)
                all_results.extend(results)
                print(f"   找到 {len(results)} 篇相关论文")
                
                # 避免API频率限制
                time.sleep(1)
                
            except Exception as e:
                print(f"   搜索出错: {e}")
                continue
        
        self.search_history.extend(queries)
        return all_results
    
    def _search_arxiv_api(self, query: str, max_results: int, 
                         date_from: str = None, categories: List[str] = None) -> List[SearchResult]:
        """
        调用arXiv API搜索论文
        """
        # 构建搜索查询
        search_query = f'all:{query}'
        
        # 添加类别过滤
        if categories:
            cat_query = ' OR '.join([f'cat:{cat}' for cat in categories])
            search_query = f'({search_query}) AND ({cat_query})'
        
        # API参数
        params = {
            'search_query': search_query,
            'start': 0,
            'max_results': max_results,
            'sortBy': 'relevance',
            'sortOrder': 'descending'
        }
        
        # 发送请求
        response = requests.get(self.base_url, params=params, timeout=10)
        response.raise_for_status()
        
        # 解析XML响应
        return self._parse_arxiv_response(response.text)
    
    def _parse_arxiv_response(self, xml_content: str) -> List[SearchResult]:
        """
        解析arXiv API的XML响应
        """
        results = []
        
        try:
            root = ET.fromstring(xml_content)
            
            # arXiv API使用Atom命名空间
            ns = {
                'atom': 'http://www.w3.org/2005/Atom',
                'arxiv': 'http://arxiv.org/schemas/atom'
            }
            
            entries = root.findall('atom:entry', ns)
            
            for entry in entries:
                # 提取基本信息
                title = entry.find('atom:title', ns)
                title_text = title.text.strip().replace('\n', ' ') if title is not None else ""
                
                summary = entry.find('atom:summary', ns)
                summary_text = summary.text.strip().replace('\n', ' ') if summary is not None else ""
                
                # 提取URL
                id_elem = entry.find('atom:id', ns)
                paper_url = id_elem.text if id_elem is not None else ""
                
                # 提取论文ID
                paper_id = paper_url.split('/')[-1] if paper_url else ""
                
                # 提取发布日期
                published = entry.find('atom:published', ns)
                pub_date = published.text[:10] if published is not None else ""
                
                # 提取作者
                authors = []
                author_elems = entry.findall('atom:author', ns)
                for author in author_elems:
                    name_elem = author.find('atom:name', ns)
                    if name_elem is not None:
                        authors.append(name_elem.text)
                
                # 提取类别
                categories = []
                category_elems = entry.findall('atom:category', ns)
                for cat in category_elems:
                    term = cat.get('term')
                    if term:
                        categories.append(term)
                
                # 创建搜索结果
                result = SearchResult(
                    title=title_text,
                    url=paper_url,
                    snippet=summary_text[:300] + "..." if len(summary_text) > 300 else summary_text,
                    content=summary_text,
                    date_published=pub_date,
                    authors=authors,
                    categories=categories,
                    paper_id=paper_id
                )
                
                results.append(result)
                
        except ET.ParseError as e:
            print(f"XML解析错误: {e}")
        except Exception as e:
            print(f"响应处理错误: {e}")
        
        return results
    
    def download_paper(self, paper_id: str) -> Dict[str, Any]:
        """
        下载论文详细信息
        """
        try:
            # 获取论文详细信息
            params = {
                'id_list': paper_id,
                'max_results': 1
            }
            
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            
            results = self._parse_arxiv_response(response.text)
            
            if results:
                paper = results[0]
                return {
                    'success': True,
                    'paper': paper,
                    'pdf_url': f"https://arxiv.org/pdf/{paper_id}.pdf"
                }
            else:
                return {'success': False, 'error': '论文未找到'}
                
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def get_search_history(self) -> List[str]:
        """获取搜索历史"""
        return self.search_history.copy()
    
    def clear_history(self):
        """清除搜索历史"""
        self.search_history.clear()
        self.searched_queries.clear()