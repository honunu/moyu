#!/usr/bin/env python3
"""
shitify.py - 把正常代码转换为屎山代码的辅助脚本

用法:
  python3 shitify.py <input_file> [--level mild|medium|heavy|hell] [--lang auto]

支持语言: python, javascript, typescript, java, go, php, cpp, c
"""

import sys
import re
import random
import os
import argparse
from typing import Optional

# ============ 魔法数字 ============
LEVEL_MAP = {
    "mild": 0.3,
    "medium": 0.6,
    "heavy": 0.9,
    "hell": 1.0
}

# 拼音替换词典（常见变量名 -> 拼音）
PINYIN_MAP = {
    "user": "yonghu",
    "data": "shuju",
    "result": "jieguo",
    "count": "shuliang",
    "name": "mingzi",
    "value": "zhilian",
    "index": "suoyin",
    "item": "yuansu",
    "list": "liebiao",
    "error": "cuowu",
    "message": "xinxi",
    "config": "peizhi",
    "manager": "guanliyuan",
    "service": "fuwu",
    "handler": "chulizhe",
    "response": "huifu",
    "request": "qingqiu",
    "output": "shucchu",
    "input": "shuru",
    "total": "zong",
    "flag": "biaozhidan",
}

# 无意义替换名
MEANINGLESS_NAMES = [
    "tmp", "temp", "data2", "val", "x1", "xx", "abc",
    "foo", "bar", "baz", "qux", "aaa", "res2", "obj1",
    "thing", "stuff", "doStuff", "processData", "handleThing",
    "kk", "zz", "pp", "ww", "qq"
]

DEAD_CODE_SNIPPETS = {
    "python": [
        '''
def _internal_check_deprecated(x, y=None, z=0):
    """
    TODO: remove this after refactoring
    FIXME: this doesn't work correctly
    """
    # HACK: temporary fix from the old version
    tmp = x
    result = []
    for i in range(len(tmp)):
        if tmp[i] is not None:
            result.append(tmp[i])
    # NOTE: y and z are reserved for future use
    return result if result else None
''',
        '''
# ===== 以下代码暂时禁用 =====
# def calculate_score_v1(data):
#     total = 0
#     for d in data:
#         total += d.get('score', 0) * 1.5
#     return total / len(data) if data else 0
# ===========================
''',
    ],
    "javascript": [
        '''
// TODO: refactor this entire function
// FIXME: breaks on edge cases
function _legacyHelper(data, options) {
  var result = [];
  var i = 0;
  while (i < data.length) {
    if (data[i] != null && data[i] != undefined) {
      result.push(data[i]);
    }
    i++;
  }
  // NOTE: options parameter reserved for future use
  return result.length > 0 ? result : null;
}
''',
    ],
    "java": [
        '''
    // TODO: remove this deprecated helper after migration
    @Deprecated
    private Object _doLegacyProcess(Object data, int flag) {
        Object tmp = null;
        // FIXME: null pointer risk here
        if (data != null) {
            tmp = data;
        }
        // NOTE: flag is reserved
        return tmp;
    }
''',
    ],
    "go": [
        '''
// _legacyHelper TODO: remove after refactor
func _legacyHelper(data interface{}) interface{} {
	// FIXME: this is broken
	tmp := data
	_ = tmp
	return nil
}
''',
    ],
}

MISLEADING_COMMENTS = [
    "// 这里不要动！动了会出大问题",
    "// 警告：删除此行会导致系统崩溃（已验证）",
    "// 这段逻辑很关键，千万别优化",
    "// TODO: fix this later（2019年留下，至今未修）",
    "// HACK: 临时方案，等下个版本再改",
    "// 此处有坑，小心",
    "// 不知道为什么，但去掉就报错",
    "// 参考：https://stackoverflow.com/questions/XXXXXX",
    "// 这里的逻辑是故意的，不是bug",
    "// 绝对不要修改这个数字",
]

def detect_language(filename: str, content: str) -> str:
    """检测代码语言"""
    ext_map = {
        ".py": "python",
        ".js": "javascript",
        ".ts": "typescript",
        ".jsx": "javascript",
        ".tsx": "typescript",
        ".java": "java",
        ".go": "go",
        ".php": "php",
        ".cpp": "cpp",
        ".cc": "cpp",
        ".c": "c",
    }
    _, ext = os.path.splitext(filename.lower())
    if ext in ext_map:
        return ext_map[ext]
    # 通过内容猜测
    if "def " in content and "import " in content:
        return "python"
    if "function " in content or "const " in content or "let " in content:
        return "javascript"
    if "public class " in content or "private void " in content:
        return "java"
    if "func " in content and "package " in content:
        return "go"
    return "unknown"


def add_magic_numbers(code: str, lang: str) -> str:
    """将命名常量替换为魔法数字的提示"""
    # 这个转换主要由 AI 完成，脚本提供辅助标记
    return code


def inject_dead_code(code: str, lang: str) -> str:
    """注入死代码片段"""
    snippets = DEAD_CODE_SNIPPETS.get(lang, DEAD_CODE_SNIPPETS.get("python", []))
    if not snippets:
        return code
    snippet = random.choice(snippets)
    # 找一个合适的位置插入（第一个函数/类定义之前）
    lines = code.split("\n")
    insert_pos = min(10, len(lines) // 3)
    lines.insert(insert_pos, snippet)
    return "\n".join(lines)


def add_misleading_comment(code: str) -> str:
    """在随机位置插入误导性注释"""
    lines = code.split("\n")
    if len(lines) < 5:
        return code
    comment = random.choice(MISLEADING_COMMENTS)
    pos = random.randint(1, min(len(lines)-1, len(lines)//2))
    lines.insert(pos, comment)
    return "\n".join(lines)


def generate_transformation_prompt(code: str, lang: str, level: str, rules_content: str) -> str:
    """生成给 AI 的转换提示词"""
    level_desc = {
        "mild": "轻度屎山（刚入职的菜鸟写的，有一些小问题）",
        "medium": "中度屎山（经历了多次需求变更，代码凑合能用）",
        "heavy": "重度屎山（祖传代码，接手就想辞职）",
        "hell": "地狱级屎山（三个不同水平的人轮流维护了5年，每人都有独特的屎山风格）"
    }

    intensity = LEVEL_MAP.get(level, 0.6)
    rule_sample_count = max(3, int(10 * intensity))

    prompt = f"""你是一个屎山代码生成专家。请将以下 {lang} 代码转换为{level_desc[level]}。

## 转换要求

转换强度：{level}（{level_desc[level]}）
目标语言：{lang}

## 必须应用的屎山技巧（根据强度选择 {rule_sample_count} 种以上）：

### 命名混乱
- 将有意义的变量名替换为单字母（a, b, x, tmp）或拼音（yonghu, shuju, jieguo）
- 将函数名改为无法描述功能的名称（doStuff, processData2, handleThings）
- 混用驼峰命名和下划线命名（同一文件里 userName 和 user_name 都出现）
- 布尔变量用双重否定命名（isNotInvalid, notDisabled）

### 魔法数字
- 将所有命名常量替换为裸数字，且同一个数字在不同地方出现时，有一处悄悄写错一点点
- 硬编码字符串、URL、路径到逻辑深处

### 冗余代码
- 将同一段逻辑复制粘贴 2-3 遍（稍微改几个变量名，让人分不清是同一逻辑）
- 声明变量但从不使用（或赋值后立刻被覆盖）
- 导入/引用从未使用的模块

### 死代码
- 定义 1-2 个完整的函数（要有实现，不是空函数），但从不调用它们
- 留下大量注释掉的旧代码（和现有代码很像但有细微差别）
- 添加永远不会为 true 的条件判断
- 堆积 TODO/FIXME 注释（其中有些已经"解决"了但注释还在）

### 逻辑混乱
- 将扁平逻辑改为 4-6 层深度嵌套的"箭头形代码"
- 反向条件判断（`if not (x is None)` 代替 `if x is not None`）
- 一行能写完的逻辑，拆成 8 行写
- 循环内部做不必要的重复计算

### 注释误导
- 在某些位置加注释，但注释描述的是别的逻辑
- 每行加废话注释（`i = i + 1 // 把 i 加 1`）
- 保留已经不适用的旧注释
- 加入神秘警告（"不知道为什么，但去掉就报错"）

{"### 全局变量滥用（重度/地狱级才加）" if intensity >= 0.6 else ""}
{"- 通过全局变量传递本来应该是参数的值" if intensity >= 0.6 else ""}
{"- 函数内部悄悄修改全局状态" if intensity >= 0.6 else ""}

{"### 结构混乱（地狱级才加）" if intensity >= 0.9 else ""}
{"- 将多个独立逻辑堆进一个超长函数" if intensity >= 0.9 else ""}
{"- 混用多种完全不同的写法实现同一件事" if intensity >= 0.9 else ""}
{"- 参数顺序容易混淆，且参数数量 8 个以上" if intensity >= 0.9 else ""}
{"- 异常处理用 except: pass 静默吞掉所有错误" if intensity >= 0.9 else ""}

## 重要原则

1. **代码必须仍然能运行**：转换后的代码逻辑上仍然正确（除了那些故意的死代码），只是写法很烂
2. **保留原有功能**：函数的实际功能必须保留，只是实现方式变得很糟糕
3. **自然混乱**：要让人感觉像真的是某个人写出来的，而不是故意搞破坏
4. **注释语言**：中英文注释混用，有些注释用中文写，有些用英文写（都是废话或误导）

## 原始代码

```{lang}
{code}
```

请直接输出转换后的屎山代码，不要加任何解释。只输出代码块内容。"""
    return prompt


def main():
    parser = argparse.ArgumentParser(description="屎山代码转换工具")
    parser.add_argument("input", help="输入文件路径")
    parser.add_argument("--level", choices=["mild", "medium", "heavy", "hell"],
                        default="medium", help="屎山强度")
    parser.add_argument("--lang", default="auto", help="代码语言（auto自动检测）")
    parser.add_argument("--output", help="输出文件路径（不指定则输出到stdout）")
    args = parser.parse_args()

    # 读取输入文件
    try:
        with open(args.input, "r", encoding="utf-8") as f:
            code = f.read()
    except FileNotFoundError:
        print(f"错误：找不到文件 {args.input}", file=sys.stderr)
        sys.exit(1)

    # 检测语言
    lang = args.lang if args.lang != "auto" else detect_language(args.input, code)

    # 读取规则文件
    script_dir = os.path.dirname(os.path.abspath(__file__))
    rules_path = os.path.join(script_dir, "..", "references", "shitcode_rules.md")
    rules_content = ""
    if os.path.exists(rules_path):
        with open(rules_path, "r", encoding="utf-8") as f:
            rules_content = f.read()

    # 生成转换提示词（供AI使用）
    prompt = generate_transformation_prompt(code, lang, args.level, rules_content)

    # 输出提示词（实际转换由调用此脚本的 AI 完成）
    print("=== SHITIFY PROMPT ===")
    print(prompt)
    print("=== END PROMPT ===")
    print(f"\n[INFO] Language: {lang}, Level: {args.level}")
    print(f"[INFO] Original lines: {len(code.splitlines())}")


if __name__ == "__main__":
    main()
