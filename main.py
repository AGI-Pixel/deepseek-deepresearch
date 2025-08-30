#!/usr/bin/env python3
"""
Deep Researcher - 深度研究系统
基于arXiv搜索的深度研究工具，模拟ChatGPT的deep research功能
"""

import sys
import argparse
import time
from deep_researcher import DeepResearcher

def print_banner():
    """打印欢迎横幅"""
    print("""
╔══════════════════════════════════════════════════════════════╗
║                      🔬 Deep Researcher                      ║
║                   基于arXiv的学术深度研究系统                 ║
║                                                              ║
║  ✨ 特性:                                                   ║
║    • 多轮迭代搜索，智能判断是否需要继续                      ║
║    • 基于真实arXiv论文数据                                   ║
║    • 支持学术引用格式 [citation:x]                          ║
║    • 使用DeepSeek-v3等先进大模型                             ║
╚══════════════════════════════════════════════════════════════╝
""")

def interactive_mode():
    """交互模式"""
    print_banner()
    
    print("🎯 进入交互模式")
    print("💡 输入命令：")
    print("   • 直接输入问题开始研究")
    print("   • 'help' 查看帮助")
    print("   • 'examples' 查看示例问题") 
    print("   • 'quit' 或 'exit' 退出")
    print("=" * 60)
    
    # 初始化研究器
    try:
        researcher = DeepResearcher("deepseek-v3")
        print("✅ Deep Researcher 初始化成功")
    except Exception as e:
        print(f"❌ 初始化失败: {e}")
        return
    
    research_count = 0
    
    while True:
        try:
            print(f"\n📝 第 {research_count + 1} 次研究")
            question = input("❓ 请输入您的研究问题: ").strip()
            
            if not question:
                continue
                
            if question.lower() in ['quit', 'exit', 'q']:
                print("👋 感谢使用 Deep Researcher！再见！")
                break
                
            if question.lower() == 'help':
                show_help()
                continue
                
            if question.lower() == 'examples':
                show_examples()
                continue
            
            # 开始研究
            print(f"\n🔬 开始深度研究: {question}")
            print("⏰ 预计耗时: 1-3分钟（取决于问题复杂度）")
            print("=" * 60)
            
            start_time = time.time()
            result = researcher.research(question)
            end_time = time.time()
            
            research_count += 1
            
            # 显示结果
            print("\n" + "=" * 60)
            print("📊 研究完成！")
            print("=" * 60)
            print(result)
            
            # 显示统计信息
            duration = end_time - start_time
            citations_count = result.count('[citation:')
            words_count = len(result)
            
            print(f"\n📈 本次研究统计:")
            print(f"   ⏱️  耗时: {duration:.1f} 秒")
            print(f"   📄 字符数: {words_count:,}")
            print(f"   🔗 引用数: {citations_count}")
            print(f"   🎯 研究质量: {'优秀' if citations_count > 20 else '良好' if citations_count > 10 else '一般'}")
            
            # 询问是否继续
            print("\n" + "=" * 60)
            continue_choice = input("🔄 是否继续研究其他问题？(y/n/help): ").strip().lower()
            if continue_choice in ['n', 'no']:
                print("👋 感谢使用！")
                break
            elif continue_choice == 'help':
                show_help()
                
        except KeyboardInterrupt:
            print("\n\n👋 用户中断，再见！")
            break
        except Exception as e:
            print(f"\n❌ 研究过程中出现错误: {e}")
            retry_choice = input("🔄 是否重试？(y/n): ").strip().lower()
            if retry_choice in ['n', 'no']:
                break

def single_mode(question, max_rounds=5):
    """单次研究模式"""
    print_banner()
    
    print(f"🎯 单次研究模式")
    print(f"📝 研究问题: {question}")
    print(f"🔢 最大搜索轮数: {max_rounds}")
    print("=" * 60)
    
    try:
        researcher = DeepResearcher("deepseek-v3")
        researcher.max_rounds = max_rounds
        print("✅ Deep Researcher 初始化成功")
        
        print(f"\n🔬 开始研究...")
        print("⏰ 预计耗时: 1-3分钟")
        print("=" * 60)
        
        start_time = time.time()
        result = researcher.research(question)
        end_time = time.time()
        
        # 显示结果
        print("\n" + "=" * 60)
        print("📊 研究完成！")
        print("=" * 60)
        print(result)
        
        # 显示统计信息
        duration = end_time - start_time
        citations_count = result.count('[citation:')
        words_count = len(result)
        
        print(f"\n📈 研究统计:")
        print(f"   ⏱️  总耗时: {duration:.1f} 秒")
        print(f"   📄 字符数: {words_count:,}")
        print(f"   🔗 引用数: {citations_count}")
        print(f"   🎯 研究质量: {'优秀' if citations_count > 20 else '良好' if citations_count > 10 else '一般'}")
        
    except Exception as e:
        print(f"❌ 研究失败: {e}")
        sys.exit(1)

def show_help():
    """显示帮助信息"""
    help_text = """
📖 Deep Researcher 使用指南

🎯 核心功能:
• 基于arXiv论文的深度学术研究
• 多轮迭代搜索，自动判断是否需要继续
• 智能查询生成和结果分析
• 支持学术引用格式 [citation:x]

💡 问题技巧:
• 提出具体、清晰的研究问题
• 可以询问技术概念、发展历史、方法比较等
• 支持中英文问题

📝 示例问题类型:
• 概念解释: "什么是Transformer架构？"
• 技术比较: "BERT和GPT的区别是什么？"
• 发展历史: "深度学习的发展历程"
• 应用场景: "强化学习在机器人中的应用"
• 最新进展: "2024年大语言模型的新突破"

⚙️ 系统特点:
• 使用DeepSeek-v3模型进行分析
• 基于真实arXiv论文数据
• 自动生成引用和参考文献
• 支持1-5轮迭代搜索

🔧 性能优化:
• 每轮搜索最多5个查询
• 内容长度自动控制在120k字符内
• 60秒超时保护
• 智能缓存API路径

📞 技术支持:
如遇问题，请检查网络连接和API配置
"""
    print(help_text)

def show_examples():
    """显示示例问题"""
    examples = """
🌟 推荐研究问题示例

🤖 人工智能基础:
  • "什么是注意力机制？"
  • "深度学习和机器学习的区别"
  • "神经网络的发展历史"

🧠 深度学习技术:
  • "Transformer架构的工作原理"
  • "卷积神经网络在计算机视觉中的应用"
  • "循环神经网络处理序列数据的方法"

🔬 前沿研究:
  • "大语言模型的最新进展"
  • "生成对抗网络的应用场景"
  • "强化学习在游戏AI中的突破"

📊 技术对比:
  • "BERT、GPT和T5模型的比较"
  • "不同优化算法的性能对比"
  • "传统机器学习vs深度学习"

🎯 应用导向:
  • "自动驾驶中的计算机视觉技术"
  • "医疗诊断中的AI应用"
  • "金融风控中的机器学习方法"

💡 提示: 问题越具体，研究结果越精准！
"""
    print(examples)

def main():
    parser = argparse.ArgumentParser(
        description="Deep Researcher - 基于arXiv的深度研究系统",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  python main.py                                    # 交互模式
  python main.py "什么是Transformer架构"             # 单次研究
  python main.py "深度学习发展历史" --max-rounds 3    # 限制搜索轮数
  python main.py --examples                         # 查看示例问题
        """
    )
    
    parser.add_argument(
        'question', 
        nargs='?',
        help='要研究的问题（不提供则进入交互模式）'
    )
    
    parser.add_argument(
        '--max-rounds', '-r',
        type=int,
        default=5,
        help='最大搜索轮数 (默认: 5)'
    )
    
    parser.add_argument(
        '--examples', '-e',
        action='store_true',
        help='显示示例问题'
    )
    
    args = parser.parse_args()
    
    if args.examples:
        print_banner()
        show_examples()
        return
    
    if args.question:
        # 单次研究模式
        single_mode(args.question, args.max_rounds)
    else:
        # 交互模式
        interactive_mode()

if __name__ == "__main__":
    main()