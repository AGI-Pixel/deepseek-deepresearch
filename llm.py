# 支持 gemini, claude, gpt-4o, deepseek-v3 等模型
import os
import requests
import json
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 从环境变量读取配置
url = os.getenv('LLM_API_URL')
API_KEY = os.getenv('LLM_API_KEY')

class LLM:
    def __init__(self, model_name="deepseek-v3"):
        self.model_name = model_name
        self.successful_path = None  # 缓存成功的API路径

    def response(self, query):
        try:
            # 使用原始格式
            payload = json.dumps({
                "max_tokens": 128000,  # 增加token数量以获得更详细的回复
                "message": query,
                "model": self.model_name,
                "stream": False
            })
            
            # 使用Bearer令牌认证
            headers = {
                'Authorization': f'Bearer {API_KEY}',
                'Content-Type': 'application/json'
            }

            # API路径列表
            api_paths = [
                'v1/chat/completions',
                'chat/completions', 
                'v1/completions',
                'completions',
                'api/v1/chat/completions'
            ]
            
            # 如果之前成功过，先尝试成功的路径
            if self.successful_path:
                api_paths = [self.successful_path] + [p for p in api_paths if p != self.successful_path]
            
            for path in api_paths:
                complete_url = url + path
                
                response = requests.request("POST", complete_url, headers=headers, data=payload, timeout=120)  # 增加到60秒超时
                
                if response.status_code == 200:
                    # 成功找到正确的API路径，缓存它
                    self.successful_path = path
                    try:
                        result = response.json()
                        if "choices" in result and len(result["choices"]) > 0:
                            content = result["choices"][0]["message"]["content"]
                            # 限制内容长度到120k字符
                            if len(content) > 120000:
                                content = content[:120000] + "\n\n[内容过长，已截断到120k字符]"
                            return content
                        else:
                            print(f"响应格式异常: {result}")
                            continue
                    except json.JSONDecodeError:
                        print(f"JSON解析失败，原始响应: {response.text}")
                        continue
                else:
                    print(f"API路径 {path} 失败，状态码: {response.status_code}")
            
            # 如果所有路径都失败
            return f"所有API路径都请求失败，请检查API密钥和URL"
        except Exception as e:
            print(f"发生错误: {e}")
            return f"error: {str(e)}"

# 测试用的代码可以注释掉
if __name__ == "__main__":
    llm = LLM("deepseek-v3")
    res = llm.response("你是谁？请简短回答。")
    print("测试回复:", res)