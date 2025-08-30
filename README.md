# 🔬 Deep Researcher

一个基于arXiv的学术深度研究系统，模拟ChatGPT的Deep Research功能，为技术研发人员提供专业的学术研究报告。

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Flask](https://img.shields.io/badge/Flask-2.3+-green.svg)](https://flask.palletsprojects.com/)

## ✨ 核心特性

### 🎯 智能研究流程
- **多轮迭代搜索**：自动判断是否需要继续深入搜索
- **真实学术数据**：基于arXiv API的实时论文检索
- **专业报告生成**：7个结构化章节，面向研发人员
- **中英文支持**：智能关键词转换和搜索优化

### 🌐 多种使用方式
- **Web界面**：美观的实时研究进度展示
- **命令行工具**：支持交互模式和单次查询
- **Python API**：可集成到其他项目中

### 📚 增强的引用系统
- **可点击引用**：[citation:x] 格式支持弹窗详情
- **完整索引**：论文标题、作者、摘要、链接
- **统计分析**：研究领域、时间跨度、引用数量

## 🚀 快速开始

### 环境要求
- Python 3.8+
- 网络连接（用于访问arXiv API和LLM服务）

### 安装依赖
```bash
pip install flask requests xml
```

### 基本使用

#### 1. 命令行模式
```bash
# 交互模式
python main.py

# 单次查询
python main.py "什么是Transformer架构"

# 限制搜索轮数
python main.py "深度学习最新进展" --max-rounds 3
```

#### 2. Web界面模式
```bash
# 启动Web服务
python web_interface.py

# 访问界面
打开浏览器访问 http://localhost:8081
```

#### 3. Python API
```python
from deep_researcher import DeepResearcher

researcher = DeepResearcher("deepseek-v3")
result = researcher.research("大语言模型的安全性研究")
print(result)
```

## 📋 项目结构

```
deepseek-deepresearch/
├── 📄 README.md                    # 项目说明文档
├── 📄 requirements.txt             # 依赖清单
├── 📄 CLAUDE.md                    # Claude Code 配置
├── 🔧 Core Components/
│   ├── llm.py                      # LLM接口封装
│   ├── search_tool.py              # arXiv搜索工具
│   ├── deep_researcher.py          # 核心研究引擎
│   └── main.py                     # 命令行入口
├── 🌐 Web Interface/
│   ├── web_interface.py            # Flask Web服务
│   └── templates/
│       └── index.html              # Web界面模板
├── 🧪 Testing/
│   ├── test_system.py              # 完整系统测试
│   ├── test_enhanced.py            # 增强功能测试
│   ├── test_optimized.py           # 优化版本测试
│   └── quick_test.py               # 快速功能测试
├── 📖 Documentation/
│   ├── README_WEB.md               # Web界面使用指南
│   ├── todo.txt                    # 项目需求文档
│   ├── search_help.html            # 搜索逻辑参考
│   └── arixv_search_tool.html      # arXiv工具文档
└── 🎯 Examples/
    └── example_outputs/            # 示例输出结果
```

## 🎮 功能演示

### 命令行界面
```bash
$ python main.py "什么是注意力机制"

🔬 开始深度研究: 什么是注意力机制
==================================================
🧠 第一步：逐步思考和推理
...
🔍 第1轮搜索
搜索查询: ['attention mechanism', 'self-attention', 'multi-head attention']
📄 找到 15 篇相关论文
...
📊 研究完成！
```

### Web界面特性
- 🎯 **实时进度条**：显示研究进度百分比
- 📊 **步骤追踪**：逐步展示搜索和分析过程
- 🔗 **可点击引用**：hover效果和弹窗详情
- 📱 **响应式设计**：支持桌面和移动设备

### 报告示例结构
```markdown
# 学术研究报告

## 1. 执行摘要
- 核心发现和技术要点
- 对研发工作的主要启示

## 2. 技术背景与现状
- 学术研究现状分析
- 关键技术挑战识别

## 3. 核心技术分析
- 主要方法和算法分析
- 创新点和技术突破

## 4. 对比分析与评估
- 方法优缺点比较
- 适用场景分析

## 5. 实践应用指导
- 工程实现建议
- 技术选型推荐

## 6. 前沿趋势与发展
- 最新研究动态
- 未来发展方向

### 📖 论文引用索引
**[citation:1]** Paper Title
*Authors* | Date | [Link](url)
Abstract preview...
```

## 🔧 配置说明

### LLM配置
修改 `llm.py` 中的配置：
```python
# 支持的模型
model_name = "deepseek-v3"  # 或 "gpt-4o", "claude", "gemini"

# API配置
url = 'your-llm-gateway-url'
API_KEY = 'your-api-key'
```

### 搜索参数
在 `deep_researcher.py` 中调整：
```python
self.max_rounds = 5          # 最大搜索轮数
max_results = 10             # 每轮最大论文数
timeout = 120               # API超时时间(秒)
```

### Web界面配置
在 `web_interface.py` 中修改：
```python
app.run(debug=True, host='0.0.0.0', port=8081)
```

## 🧪 测试与验证

### 运行测试套件
```bash
# 基础功能测试
python quick_test.py

# 完整系统测试
python test_system.py

# 优化版本测试
python test_optimized.py

# Web界面测试
python web_interface.py
# 然后在浏览器中测试各项功能
```

### 测试用例
- ✅ LLM连接测试
- ✅ arXiv搜索功能
- ✅ 多轮迭代逻辑
- ✅ 引用格式处理
- ✅ Web界面交互
- ✅ 错误处理机制

## 🎯 使用场景

### 学术研究
- 📚 文献综述和现状分析
- 🔍 技术调研和竞品分析
- 📊 研究趋势和发展方向

### 技术开发
- 🛠️ 技术选型和架构设计
- ⚡ 性能优化和最佳实践
- 🔒 安全性分析和风险评估

### 教育培训
- 👨‍🎓 专业知识学习
- 📖 概念理解和原理分析
- 🎓 学术论文阅读指导

## 🔄 系统架构

### 核心组件
```
用户查询 → 思考分析 → 查询生成 → arXiv搜索 → 结果分析 → 迭代判断 → 报告生成
    ↓           ↓           ↓           ↓           ↓           ↓           ↓
   LLM        LLM      优化算法      API调用      LLM        智能判断      分步处理
```

### 技术特点
- **分步处理**：避免长上下文导致的API失败
- **容错设计**：多级fallback机制确保可用性
- **智能判断**：自动决定是否需要继续搜索
- **实时反馈**：Web界面提供实时进度更新

## 📈 性能优化

### 已实现优化
- ⚡ **API调用优化**：缓存成功路径，120秒超时
- 🎯 **内容长度控制**：论文摘要200字符限制
- 🔄 **分步生成**：核心报告与引用索引分离
- 💾 **智能缓存**：搜索历史和查询去重

### 性能指标
- 🕒 **平均响应时间**：2-3分钟（取决于问题复杂度）
- 📄 **论文处理能力**：单次最多40篇论文
- 🔍 **搜索轮数**：1-5轮智能迭代
- 📊 **成功率**：>95%（包含备用机制）

## 🤝 贡献指南

### 开发环境设置
```bash
git clone https://github.com/your-username/deepseek-deepresearch.git
cd deepseek-deepresearch
pip install -r requirements.txt
```

### 贡献方式
1. 🍴 Fork 项目
2. 🌟 创建特性分支
3. 💻 提交代码更改
4. 🧪 运行测试套件
5. 📝 提交Pull Request

### 开发优先级
- [ ] 支持更多LLM提供商
- [ ] 添加更多学术数据库
- [ ] 改进搜索算法
- [ ] 增加可视化功能
- [ ] 支持团队协作

## 📜 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 📞 联系方式

- 🐛 **问题报告**：[GitHub Issues](https://github.com/your-username/deepseek-deepresearch/issues)
- 💡 **功能建议**：[Discussions](https://github.com/your-username/deepseek-deepresearch/discussions)
- 📧 **联系邮箱**：your.email@example.com

## 🙏 致谢

- 感谢 [arXiv](https://arxiv.org/) 提供的开放学术数据
- 感谢 DeepSeek 团队的大语言模型支持
- 感谢开源社区的贡献和反馈

---

**⭐ 如果这个项目对您有帮助，请给我们一个星标！**