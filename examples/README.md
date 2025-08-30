# 📚 Deep Researcher 使用示例

本目录包含Deep Researcher的各种使用示例，帮助您快速上手。

## 📋 示例列表

### 🐍 Python API示例
- **example_usage.py** - 完整的Python API使用示例
  - 基础研究示例
  - 技术研究示例  
  - 批量研究示例
  - 自定义配置示例

### 💻 命令行示例

#### 基础用法
```bash
# 交互模式
python main.py

# 单次查询
python main.py "什么是深度学习"

# 限制搜索轮数
python main.py "机器学习算法比较" --max-rounds 3

# 查看示例问题
python main.py --examples
```

#### 推荐问题类型

**🤖 AI基础概念**
```bash
python main.py "什么是注意力机制"
python main.py "深度学习和机器学习的区别"  
python main.py "神经网络的发展历史"
```

**🔬 前沿技术研究**
```bash
python main.py "大语言模型的最新进展"
python main.py "生成对抗网络的创新应用"
python main.py "强化学习在自动驾驶中的应用"
```

**⚙️ 技术实现对比**
```bash
python main.py "BERT和GPT模型架构对比"
python main.py "不同优化算法的性能比较"
python main.py "CNN和Vision Transformer的优缺点"
```

**🏭 工业应用场景**
```bash
python main.py "计算机视觉在医疗诊断中的应用"
python main.py "自然语言处理在金融风控的实践"
python main.py "推荐系统的深度学习方法"
```

### 🌐 Web界面示例

#### 启动Web服务
```bash
python web_interface.py
```

#### 功能演示
1. **实时研究进度** - 观察搜索和分析过程
2. **可点击引用** - 点击[citation:x]查看论文详情
3. **响应式界面** - 支持桌面和移动设备
4. **统计分析** - 查看研究数据统计

#### Web界面截图功能
- 🎯 问题输入和推荐
- 📊 实时进度条
- 📝 步骤化展示
- 🔗 可点击引用
- 📈 统计面板

## 🎓 学习路径

### 初学者
1. 运行 `python main.py --examples` 查看示例问题
2. 尝试简单概念查询："什么是机器学习"
3. 使用Web界面体验完整流程

### 进阶用户  
1. 运行 `examples/example_usage.py` 了解API
2. 尝试技术对比问题："CNN vs Transformer"
3. 自定义搜索参数和轮数

### 开发者
1. 阅读 `deep_researcher.py` 源码
2. 修改搜索策略和报告格式  
3. 集成到自己的项目中

## 📊 示例输出格式

### 研究报告结构
```markdown
# 学术研究报告

## 1. 执行摘要
- 核心发现和技术要点
- 对研发工作的启示

## 2. 技术背景与现状  
- 学术研究现状分析
- 关键技术挑战

## 3. 核心技术分析
- 主要方法和算法
- 创新点和突破

## 4. 对比分析与评估
- 方法优缺点比较
- 适用场景分析

## 5. 实践应用指导
- 工程实现建议
- 技术选型推荐

## 6. 前沿趋势与发展
- 最新研究动态
- 未来发展方向

## 📊 研究数据统计
- 搜索轮数、论文总数
- 时间覆盖、研究领域

## 📖 论文引用索引  
- 完整的论文列表
- 标题、作者、链接
```

### 引用格式示例
```markdown
**[citation:1]** Attention Is All You Need
*Vaswani, Shazeer, Parmar* | 2017-06-12 | [链接](url)
We propose a new simple network architecture, the Transformer...
```

## ⚡ 性能优化建议

### 提高效率
- 使用 `--max-rounds 2` 限制搜索轮数
- 对于简单问题，单轮搜索即可
- 批量查询时合理设置间隔

### 获得更好结果  
- 使用具体、清晰的问题描述
- 包含关键技术术语
- 指定特定的应用领域或时间范围

### 故障排除
- 检查网络连接
- 确认API密钥配置
- 查看错误日志信息

## 🔧 自定义配置

### 修改搜索参数
```python
researcher = DeepResearcher("deepseek-v3")
researcher.max_rounds = 3        # 最大搜索轮数
researcher.search_tool.max_results = 5  # 每轮最大论文数
```

### 自定义报告格式
```python
# 覆盖报告生成方法
def custom_report_generator(question, results):
    return f"自定义报告格式: {question}"

researcher._generate_final_answer = custom_report_generator
```

## 🚀 最佳实践

1. **问题设计**
   - 使用专业术语
   - 明确研究范围
   - 避免过于宽泛的问题

2. **结果利用**
   - 重点关注引用论文
   - 验证关键结论
   - 深入研读相关文献

3. **效率提升**
   - 缓存常用查询结果
   - 批量处理相关问题
   - 根据需求调整搜索深度

---

💡 **提示**: 如果您是第一次使用，建议从Web界面开始体验，然后逐步尝试命令行和API方式。