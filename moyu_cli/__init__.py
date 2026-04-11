"""
Moyu CLI - 摸鱼命令行工具
"""
import argparse
import os
import sys
import shutil
import subprocess

SKILLS_DIR = os.path.join(os.path.dirname(__file__), "..", "skills")


def get_available_skills():
    """获取可用的 skills 列表"""
    skills = []
    if os.path.exists(SKILLS_DIR):
        for item in os.listdir(SKILLS_DIR):
            skill_path = os.path.join(SKILLS_DIR, item, "SKILL.md")
            if os.path.exists(skill_path):
                skills.append(item)
    return sorted(skills)


def check_claude_code():
    """检测 Claude Code 是否安装"""
    # 检查 claude 命令是否在 PATH 中
    if shutil.which("claude"):
        return True

    # 常见安装路径
    common_paths = [
        "/Applications/Claude.app/Contents/Resources/claude",
        os.path.expanduser("~/Applications/Claude.app/Contents/Resources/claude"),
    ]

    for path in common_paths:
        if os.path.exists(path):
            return True

    return False


def run_skill(skill_name, task):
    """运行指定的 skill"""
    skill_path = os.path.join(SKILLS_DIR, skill_name, "SKILL.md")

    if not os.path.exists(skill_path):
        print(f"Error: Skill '{skill_name}' not found")
        print(f"Available skills: {', '.join(get_available_skills())}")
        sys.exit(1)

    # 检测 Claude Code
    if not check_claude_code():
        print("\n" + "=" * 60)
        print("ERROR: Claude Code 未安装或不在 PATH 中")
        print("=" * 60)
        print("\n请先安装 Claude Code：")
        print("  1. 访问 https://claude.ai/code 下载")
        print("  2. 或使用 npm 安装: npm install -g @anthropic-ai/claude-code")
        print("  3. 安装后重新打开终端")
        print("\n或者你也可以直接在 Claude Code 或 CodeBuddy 中使用 skills。")
        print("=" * 60 + "\n")
        sys.exit(1)

    # 读取 skill 内容
    with open(skill_path, "r", encoding="utf-8") as f:
        skill_content = f.read()

    # 构建 prompt
    prompt = f"""你是一个摸鱼大师。现在有一个任务需要你执行。

## 任务
{task}

## Skill 规范
请严格按照以下规范执行：

{skill_content}

## 要求
1. 仔细阅读 Skill 规范
2. 按照规范生成或修改代码
3. 确保代码可以运行
4. 保持摸鱼风格
5. 任务完成后输出总结
"""

    print(f"\n{'='*60}")
    print(f"🎯 任务: {task}")
    print(f"📦 Skill: {skill_name}")
    print(f"{'='*60}\n")

    # 调用 Claude Code
    try:
        result = subprocess.run(
            ["claude", "--print", prompt],
            capture_output=False,
            text=True
        )
        return result.returncode
    except Exception as e:
        print(f"\nError: Failed to run Claude Code: {e}")
        return 1


def main():
    parser = argparse.ArgumentParser(
        description="Moyu CLI - 摸鱼命令行工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  moyu over-engineering "把删除用户功能过度工程化"
  moyu shit-code-generator "把登录模块转成屎山代码"
  moyu bug-generator "在订单模块里加难以发现的bug"
  moyu meeting-turbulence "生成一些代码审查意见"

可用 Skills:
  - over-engineering    (过度工程化引擎)
  - shit-code-generator (屎山代码生成器)
  - bug-generator       (Bug制造机)
  - meeting-turbulence  (技术争论制造机)
  - crud-generator      (CRUD代码生成器)

注意: 需要先安装 Claude Code (https://claude.ai/code)
        """
    )

    parser.add_argument(
        "skill",
        nargs="?",
        help="要使用的 skill 名称"
    )
    parser.add_argument(
        "task",
        nargs="?",
        help="要执行的任务描述"
    )

    args = parser.parse_args()

    # 如果没有提供参数，显示帮助
    if not args.skill:
        parser.print_help()
        print("\n" + "=" * 60)
        print("可用 Skills:")
        for skill in get_available_skills():
            print(f"  - {skill}")
        print("=" * 60)
        return 0

    # 如果没有提供任务
    if not args.task:
        print(f"Error: missing task argument")
        print(f"\n使用方法: moyu {args.skill} <任务描述>")
        print(f"\n示例: moyu {args.skill} \"把删除功能过度工程化\"")
        return 1

    return run_skill(args.skill, args.task)


if __name__ == "__main__":
    sys.exit(main() or 0)
