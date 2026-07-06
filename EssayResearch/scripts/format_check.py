#!/usr/bin/env python3
"""格式合规检查脚本 - EssayResearch G.9 阶段使用

功能：
1. 读取目标格式预设（IEEE/ACM/NeurIPS/中国学位论文等）
2. 解析 LaTeX 源文件，提取当前格式参数
3. 逐项对比，输出合规检查表
"""

import re
import sys
import json
from pathlib import Path


# 格式预设参数（从 skills/shared/format-specs/ 读取）
FORMAT_SPECS_DIR = Path(__file__).parent.parent / "skills" / "shared" / "format-specs"

# 内置默认检查项
DEFAULT_CHECKS = [
    {"item": "纸张大小", "key": "paper", "latex_patterns": [
        r"\\documentclass.*?(?:a4|letter|A4|Letter)",
        r"\\usepackage.*?geometry.*?paper=(\w+)",
    ]},
    {"item": "页边距", "key": "margins", "latex_patterns": [
        r"\\usepackage.*?geometry.*?(?:margin|top|bottom|left|right)",
        r"\\setlength.*?(?:topmargin|bottommargin|leftmargin|rightmargin|oddsidemargin)",
    ]},
    {"item": "字体", "key": "font", "latex_patterns": [
        r"\\usepackage.*?(?:fontspec|ctex|times|mathptmx)",
        r"\\setmainfont\{([^}]+)\}",
        r"\\setCJKmainfont\{([^}]+)\}",
    ]},
    {"item": "字号", "key": "fontsize", "latex_patterns": [
        r"\\documentclass.*?\[(\d+)pt\]",
        r"\\documentclass.*?(?:10pt|11pt|12pt)",
    ]},
    {"item": "行距", "key": "linespacing", "latex_patterns": [
        r"\\linespread\{([\d.]+)\}",
        r"\\usepackage.*?setspace.*?\\setstretch\{([\d.]+)\}",
        r"\\baselinestretch",
    ]},
    {"item": "分栏", "key": "columns", "latex_patterns": [
        r"\\documentclass.*?(?:twocolumn|onecolumn)",
        r"\\twocolumn",
        r"\\onecolumn",
    ]},
    {"item": "标题层级", "key": "headings", "latex_patterns": [
        r"\\title\{([^}]+)\}",
        r"\\section\{",
        r"\\subsection\{",
        r"\\subsubsection\{",
    ]},
    {"item": "图注格式", "key": "figure_caption", "latex_patterns": [
        r"\\caption\{",
        r"\\captionsetup",
        r"\\usepackage.*?caption",
    ]},
    {"item": "表格格式", "key": "table_format", "latex_patterns": [
        r"\\usepackage.*?booktabs",
        r"\\toprule",
        r"\\midrule",
        r"\\bottomrule",
    ]},
    {"item": "参考文献格式", "key": "references", "latex_patterns": [
        r"\\bibliographystyle\{([^}]+)\}",
        r"\\usepackage.*?(?:biblatex|natbib)",
    ]},
    {"item": "页眉页脚", "key": "headers", "latex_patterns": [
        r"\\usepackage.*?fancyhdr",
        r"\\pagestyle\{([^}]+)\}",
        r"\\lhead|\\rhead|\\lfoot|\\rfoot|\\cfoot",
    ]},
    {"item": "页码", "key": "pagenumber", "latex_patterns": [
        r"\\pagenumbering\{([^}]+)\}",
        r"\\pagestyle\{([^}]+)\}",
    ]},
    {"item": "首行缩进", "key": "indent", "latex_patterns": [
        r"\\setlength\{\\parindent\}\{([^}]+)\}",
        r"\\usepackage.*?indentfirst",
    ]},
]


def load_format_spec(format_name):
    """从 format-specs/ 目录加载格式预设"""
    spec_file = FORMAT_SPECS_DIR / f"{format_name}.md"
    if not spec_file.exists():
        return None
    content = spec_file.read_text(encoding="utf-8")
    # 简单解析：提取表格中的参数
    spec = {"format_name": format_name, "raw": content}
    return spec


def parse_latex(tex_file):
    """解析 LaTeX 源文件，提取格式参数"""
    content = Path(tex_file).read_text(encoding="utf-8")
    
    extracted = {}
    
    for check in DEFAULT_CHECKS:
        item = check["item"]
        found = []
        for pattern in check["latex_patterns"]:
            matches = re.findall(pattern, content, re.DOTALL)
            if matches:
                found.extend(matches if isinstance(matches, list) else [matches])
        extracted[item] = found if found else None
    
    # 额外提取
    # documentclass
    doc_match = re.search(r"\\documentclass(?:\[([^\]]*)\])?\{([^}]+)\}", content)
    if doc_match:
        extracted["documentclass_options"] = doc_match.group(1)
        extracted["documentclass"] = doc_match.group(2)
    
    # 统计表格数量
    table_count = len(re.findall(r"\\begin\{table", content))
    # 检查是否使用 booktabs
    has_booktabs = "\\toprule" in content
    extracted["tables_total"] = table_count
    extracted["tables_use_booktabs"] = has_booktabs
    
    # 统计图片数量
    figure_count = len(re.findall(r"\\begin\{figure", content))
    extracted["figures_total"] = figure_count
    
    # 统计公式数量
    equation_count = len(re.findall(r"\\begin\{equation", content))
    inline_math_count = len(re.findall(r"\$[^\$]+\$", content))
    extracted["equations_total"] = equation_count
    extracted["inline_math_total"] = inline_math_count
    
    # 检查是否有未定义引用
    undefined_refs = re.findall(r"\?\?(?:ref|cite)", content)
    extracted["undefined_references"] = len(undefined_refs)
    
    return extracted


def run_compliance_check(tex_file, format_name):
    """运行格式合规检查
    
    Args:
        tex_file: LaTeX 文件路径
        format_name: 目标格式名称 (ieee/acm/neurips/chinese_thesis/...)
    
    Returns:
        list: 检查结果列表
    """
    spec = load_format_spec(format_name)
    extracted = parse_latex(tex_file)
    
    results = []
    
    for check in DEFAULT_CHECKS:
        item = check["item"]
        current = extracted.get(item)
        
        if current:
            status = "✅"
            note = f"检测到: {current[0] if isinstance(current, list) else current}"
        else:
            status = "⚠️"
            note = "未检测到相关设置，可能需要手动确认"
        
        results.append({
            "item": item,
            "status": status,
            "current": str(current) if current else "未检测到",
            "note": note
        })
    
    # 额外检查
    # booktabs 检查
    if extracted.get("tables_total", 0) > 0:
        if extracted.get("tables_use_booktabs"):
            results.append({
                "item": "三线表规范",
                "status": "✅",
                "current": "使用 booktabs",
                "note": "所有表格使用 booktabs 格式"
            })
        else:
            results.append({
                "item": "三线表规范",
                "status": "❌",
                "current": "未使用 booktabs",
                "note": "建议使用 \\usepackage{booktabs} 并用 \\toprule/\\midrule/\\bottomrule"
            })
    
    # 未定义引用检查
    undef = extracted.get("undefined_references", 0)
    if undef > 0:
        results.append({
            "item": "引用完整性",
            "status": "❌",
            "current": f"{undef} 个未定义引用",
            "note": "需要多遍编译或检查 .bib 文件"
        })
    else:
        results.append({
            "item": "引用完整性",
            "status": "✅",
            "current": "0 个未定义引用",
            "note": "所有引用已定义"
        })
    
    return results


def print_report(results, format_name):
    """打印格式合规检查报告"""
    print(f"\n{'='*60}")
    print(f"格式合规检查报告")
    print(f"目标格式: {format_name}")
    print(f"{'='*60}\n")
    
    pass_count = sum(1 for r in results if r["status"] == "✅")
    warn_count = sum(1 for r in results if r["status"] == "⚠️")
    fail_count = sum(1 for r in results if r["status"] == "❌")
    
    print(f"{'检查项':<20} {'结果':<6} {'当前状态':<30} {'备注'}")
    print("-" * 90)
    
    for r in results:
        print(f"{r['item']:<20} {r['status']:<6} {r['current'][:28]:<30} {r['note']}")
    
    print(f"\n{'='*60}")
    print(f"总计: {pass_count} 通过, {warn_count} 需确认, {fail_count} 不合规")
    print(f"{'='*60}\n")
    
    return pass_count, warn_count, fail_count


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("用法: python format_check.py <tex_file> <format_name>")
        print("格式选项: ieee, acm, neurips, chinese_thesis, springer_lncs, apa7, mla")
        sys.exit(1)
    
    tex_file = sys.argv[1]
    format_name = sys.argv[2]
    
    results = run_compliance_check(tex_file, format_name)
    p, w, f = print_report(results, format_name)
    
    sys.exit(0 if f == 0 else 1)
