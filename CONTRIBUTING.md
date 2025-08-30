# 🤝 Contributing to Deep Researcher

感谢您对Deep Researcher项目的兴趣！我们欢迎所有形式的贡献。

## 🚀 快速开始

### 开发环境设置
```bash
# 1. Fork并克隆项目
git clone https://github.com/AGI-Pixel/deepseek-deepresearch.git
cd deepseek-deepresearch

# 2. 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. 安装依赖
pip install -r requirements.txt

# 4. 运行测试
python test_system.py
```

## 📋 贡献类型

### 🐛 Bug报告
发现bug时，请提供：
- 详细的错误描述
- 重现步骤
- 系统环境信息
- 错误日志（如果有）

### ✨ 功能请求
提出新功能时，请说明：
- 功能的具体需求
- 使用场景描述
- 期望的行为表现
- 可能的实现方案

### 💻 代码贡献
提交代码前，请确保：
- [ ] 代码遵循项目风格
- [ ] 通过所有测试用例
- [ ] 添加必要的文档
- [ ] 提交信息清晰明确

## 🔧 开发指南

### 代码风格
- 使用4空格缩进
- 函数和变量使用snake_case
- 类名使用PascalCase
- 添加必要的注释和文档字符串

### 测试要求
- 新功能必须包含测试用例
- 确保所有测试通过
- 测试覆盖率应保持在80%以上

### 提交规范
```bash
# 提交信息格式
<type>(<scope>): <description>

# 示例
feat(search): add multi-language support
fix(web): resolve citation popup positioning
docs(readme): update installation instructions
```

## 🎯 开发优先级

### 高优先级
- [ ] 支持更多LLM提供商（OpenAI, Anthropic）
- [ ] 添加Google Scholar搜索支持
- [ ] 改进搜索算法准确性
- [ ] 增加批量查询功能

### 中优先级
- [ ] 添加可视化图表
- [ ] 支持导出功能（PDF, Word）
- [ ] 实现用户认证系统
- [ ] 添加API速率限制

### 低优先级
- [ ] 多语言界面支持
- [ ] 移动端应用
- [ ] 团队协作功能
- [ ] 高级统计分析

## 📝 文档贡献

### 文档类型
- API文档改进
- 使用指南完善
- 示例代码添加
- 常见问题整理

### 文档标准
- 使用Markdown格式
- 包含代码示例
- 提供清晰的步骤说明
- 定期更新维护

## 🧪 测试指南

### 运行测试
```bash
# 基础功能测试
python quick_test.py

# 完整系统测试
python test_system.py

# 特定组件测试
python -m pytest tests/test_search.py
```

### 测试覆盖范围
- 搜索功能测试
- LLM集成测试
- Web界面测试
- 错误处理测试

## 🔍 Code Review流程

### 提交PR前
1. 确保代码通过所有测试
2. 运行代码格式化工具
3. 更新相关文档
4. 自我审查代码质量

### Review标准
- 代码可读性和维护性
- 功能正确性和完整性
- 性能影响评估
- 安全性考虑

## 🎉 致谢方式

贡献者将被添加到：
- README.md的致谢部分
- 项目贡献者列表
- 发布日志的贡献记录

## 📞 联系方式

- 💬 **讨论**：[GitHub Discussions](https://github.com/AGI-Pixel/deepseek-deepresearch/discussions)
- 🐛 **问题**：[GitHub Issues](https://github.com/AGI-Pixel/deepseek-deepresearch/issues)
- 📧 **邮件**：contact@agi-pixel.com

## ⚖️ 行为准则

请遵循以下准则：
- 尊重所有参与者
- 欢迎新手贡献者
- 建设性地提出建议
- 保持专业和友好的交流

---

感谢您为Deep Researcher项目做出的贡献！🌟