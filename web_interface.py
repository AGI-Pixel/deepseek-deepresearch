#!/usr/bin/env python3
"""
Deep Researcher Web界面
基于Flask的实时研究结果展示
"""

from flask import Flask, render_template, request, jsonify, Response
from deep_researcher import DeepResearcher
import json
import time
import threading
from queue import Queue
import uuid

app = Flask(__name__)

# 存储研究会话
research_sessions = {}

class ResearchSession:
    def __init__(self, session_id):
        self.session_id = session_id
        self.researcher = DeepResearcher("deepseek-v3")
        self.researcher.max_rounds = 5
        self.progress_queue = Queue()
        self.is_running = False
        self.result = None
        
    def add_progress(self, step, content, progress=None):
        """添加进度信息"""
        self.progress_queue.put({
            'step': step,
            'content': content,
            'progress': progress,
            'timestamp': time.strftime("%H:%M:%S")
        })

def conduct_research_with_progress(session_id, question):
    """带进度反馈的研究函数"""
    session = research_sessions[session_id]
    session.is_running = True
    
    try:
        session.add_progress('start', f'🔬 开始研究问题: {question}', 5)
        
        # 初步思考
        session.add_progress('thinking', '🧠 正在进行初步思考和分析...', 10)
        initial_analysis = session.researcher._initial_thinking(question, time.strftime("%Y-%m-%d, %A"))
        session.add_progress('thinking_result', f'📋 初步分析完成:\n{initial_analysis[:300]}...', 20)
        
        # 生成查询
        session.add_progress('query_gen', '🔍 正在生成搜索查询...', 25)
        first_queries = session.researcher._extract_first_search_queries(question, initial_analysis)
        session.add_progress('queries', f'📝 生成搜索查询: {", ".join(first_queries)}', 30)
        
        all_search_results = []
        search_round = 1
        current_queries = first_queries
        
        while current_queries and search_round <= session.researcher.max_rounds:
            # 搜索进度 - 确保每轮搜索占用合理的进度区间
            total_rounds = min(session.researcher.max_rounds, 3)  # 预估最多3轮
            progress_per_round = 50 / total_rounds  # 50%的进度用于搜索
            progress_base = 30 + (search_round - 1) * progress_per_round
            
            session.add_progress('search_start', f'🔍 第{search_round}轮搜索开始', int(progress_base))
            session.add_progress('search_queries', f'搜索查询: {", ".join(current_queries)}', int(progress_base + progress_per_round * 0.1))
            
            # 执行搜索
            try:
                round_results = session.researcher._conduct_search_round(current_queries)
                all_search_results.extend(round_results)
                
                session.add_progress('search_results', f'📄 找到 {len(round_results)} 篇论文', int(progress_base + progress_per_round * 0.3))
                
                # 显示部分论文标题
                if round_results:
                    titles = [r.title[:50] + "..." if len(r.title) > 50 else r.title for r in round_results[:3]]
                    session.add_progress('paper_titles', f'关键论文:\n• ' + '\n• '.join(titles), int(progress_base + progress_per_round * 0.4))
                
                # 分析结果
                session.add_progress('analysis', f'📊 正在分析第{search_round}轮搜索结果...', int(progress_base + progress_per_round * 0.5))
                analysis_and_queries = session.researcher._analyze_results_and_generate_queries(
                    question, round_results, search_round
                )
                
                session.add_progress('analysis_result', f'✅ 第{search_round}轮分析完成', int(progress_base + progress_per_round * 0.7))
                
                # 检查是否继续
                next_queries = analysis_and_queries.get('next_queries')
                if next_queries:
                    session.add_progress('continue', f'🔮 发现需要进一步研究: {", ".join(next_queries[:2])}...', int(progress_base + progress_per_round * 0.8))
                    current_queries = next_queries
                    search_round += 1
                else:
                    session.add_progress('search_complete', '✅ 搜索完成，信息已足够全面', int(progress_base + progress_per_round * 0.9))
                    break
                    
            except Exception as e:
                session.add_progress('search_error', f'⚠️ 第{search_round}轮搜索出现问题: {str(e)}', int(progress_base + progress_per_round * 0.5))
                break
        
        # 生成最终答案
        session.add_progress('final_gen', '📝 正在生成最终研究报告...', 85)
        final_answer = session.researcher._generate_final_answer(question, all_search_results, search_round)
        
        session.add_progress('complete', '🎉 研究完成！', 100)
        session.result = final_answer
        
    except Exception as e:
        session.add_progress('error', f'❌ 研究过程出现错误: {str(e)}', 100)
        session.result = f"研究失败: {str(e)}"
    
    finally:
        session.is_running = False

@app.route('/')
def index():
    """首页"""
    return render_template('index.html')

@app.route('/research', methods=['POST'])
def start_research():
    """开始研究"""
    data = request.get_json()
    question = data.get('question', '').strip()
    
    if not question:
        return jsonify({'error': '请输入研究问题'}), 400
    
    # 创建新的研究会话
    session_id = str(uuid.uuid4())
    session = ResearchSession(session_id)
    research_sessions[session_id] = session
    
    # 在后台线程中开始研究
    research_thread = threading.Thread(
        target=conduct_research_with_progress,
        args=(session_id, question)
    )
    research_thread.daemon = True
    research_thread.start()
    
    return jsonify({'session_id': session_id})

@app.route('/progress/<session_id>')
def get_progress(session_id):
    """获取研究进度（SSE流）"""
    def generate_progress():
        if session_id not in research_sessions:
            yield f"data: {json.dumps({'error': '会话不存在'})}\n\n"
            return
        
        session = research_sessions[session_id]
        
        try:
            while session.is_running or not session.progress_queue.empty():
                try:
                    if not session.progress_queue.empty():
                        progress_data = session.progress_queue.get_nowait()
                        yield f"data: {json.dumps(progress_data, ensure_ascii=False)}\n\n"
                    else:
                        time.sleep(0.5)  # 短暂等待
                        # 发送心跳保持连接
                        yield f"data: {json.dumps({'step': 'heartbeat'})}\n\n"
                except Exception as e:
                    print(f"Progress queue error: {e}")
                    break
            
            # 发送最终结果
            if session.result:
                yield f"data: {json.dumps({'step': 'result', 'content': session.result, 'progress': 100}, ensure_ascii=False)}\n\n"
            
            yield f"data: {json.dumps({'step': 'done'})}\n\n"
            
        except GeneratorExit:
            # 客户端断开连接
            print(f"Client disconnected from session {session_id}")
        except Exception as e:
            print(f"SSE error: {e}")
            yield f"data: {json.dumps({'error': str(e)})}\n\n"
    
    response = Response(generate_progress(), mimetype='text/event-stream')
    response.headers['Cache-Control'] = 'no-cache'
    response.headers['Connection'] = 'keep-alive'
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@app.route('/result/<session_id>')
def get_result(session_id):
    """获取研究结果"""
    if session_id not in research_sessions:
        return jsonify({'error': '会话不存在'}), 404
    
    session = research_sessions[session_id]
    return jsonify({
        'is_running': session.is_running,
        'result': session.result
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8081)