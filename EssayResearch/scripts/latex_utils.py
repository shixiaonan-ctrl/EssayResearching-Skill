#!/usr/bin/env python3
"""LaTeX 编译辅助脚本 - EssayResearch G.9 阶段使用

功能：
1. 检测 TeX 环境（TeX Live / MiKTeX / MacTeX）
2. 根据论文语言选择编译引擎（xelatex 中文 / pdflatex 英文）
3. 执行多遍编译（处理交叉引用）
4. 捕获并解析编译错误
"""

import subprocess
import sys
import os
import re
import json
from pathlib import Path


def detect_tex_environment():
    """检测系统中是否安装了 LaTeX 环境"""
    engines = {
        "xelatex": None,
        "pdflatex": None,
        "latexmk": None,
        "bibtex": None,
    }
    
    for engine in engines:
        try:
            result = subprocess.run(
                [engine, "--version"],
                capture_output=True, text=True, timeout=10
            )
            if result.returncode == 0:
                first_line = result.stdout.strip().split("\n")[0]
                engines[engine] = first_line
        except (FileNotFoundError, subprocess.TimeoutExpired):
            engines[engine] = None
    
    installed = {k: v for k, v in engines.items() if v is not None}
    
    if not installed:
        return {
            "installed": False,
            "engines": {},
            "message": "未检测到 LaTeX 环境。请安装 TeX Live (推荐) 或 MiKTeX。\n"
                       "  Windows: https://miktex.org/download\n"
                       "  macOS: brew install --cask mactex\n"
                       "  Linux: sudo apt install texlive-full"
        }
    
    return {
        "installed": True,
        "engines": installed,
        "message": f"检测到 LaTeX 环境：{', '.join(installed.keys())}"
    }


def compile_latex(tex_file, engine="xelatex", output_dir="outputs"):
    """编译 LaTeX 文件
    
    Args:
        tex_file: .tex 文件路径
        engine: 编译引擎 (xelatex / pdflatex)
        output_dir: 输出目录
    
    Returns:
        dict: 编译结果 {success, pdf_path, errors, warnings, log}
    """
    tex_path = Path(tex_file)
    if not tex_path.exists():
        return {"success": False, "error": f"文件不存在: {tex_file}"}
    
    os.makedirs(output_dir, exist_ok=True)
    
    # 使用 latexmk（如果可用）或手动多遍编译
    latexmk_available = subprocess.run(
        ["latexmk", "--version"], capture_output=True, timeout=10
    ).returncode == 0
    
    if latexmk_available:
        cmd = [
            "latexmk",
            f"-{engine}",
            f"-output-directory={output_dir}",
            "-interaction=nonstopmode",
            "-halt-on-error",
            str(tex_path)
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    else:
        # 手动多遍编译
        base_cmd = [
            engine,
            f"-output-directory={output_dir}",
            "-interaction=nonstopmode",
            "-halt-on-error",
            str(tex_path)
        ]
        
        # 第 1 遍
        subprocess.run(base_cmd, capture_output=True, text=True, timeout=120)
        # bibtex
        aux_file = Path(output_dir) / (tex_path.stem + ".aux")
        if aux_file.exists():
            subprocess.run(
                ["bibtex", str(aux_file)],
                capture_output=True, text=True, timeout=60
            )
        # 第 2-3 遍
        subprocess.run(base_cmd, capture_output=True, text=True, timeout=120)
        result = subprocess.run(base_cmd, capture_output=True, text=True, timeout=120)
    
    # 检查 PDF 是否生成
    pdf_path = Path(output_dir) / (tex_path.stem + ".pdf")
    
    # 解析日志
    log_file = Path(output_dir) / (tex_path.stem + ".log")
    log_content = ""
    if log_file.exists():
        log_content = log_file.read_text(encoding="utf-8", errors="ignore")
    
    errors = _parse_errors(log_content, result.stderr)
    warnings = _parse_warnings(log_content)
    
    return {
        "success": pdf_path.exists(),
        "pdf_path": str(pdf_path) if pdf_path.exists() else None,
        "errors": errors,
        "warnings": warnings,
        "log_excerpt": log_content[-2000:] if log_content else result.stderr[-2000:]
    }


def _parse_errors(log_content, stderr):
    """从日志中提取错误信息"""
    errors = []
    
    # 常见 LaTeX 错误模式
    error_patterns = [
        (r"! LaTeX Error: (.*?)(?:\n\n|\nl\.)", "LaTeX Error"),
        (r"! Package (.*?) Error: (.*?)(?:\n\n|\nl\.)", "Package Error"),
        (r"! Undefined control sequence\.\n.*?\n.*?(.*?)\n", "Undefined control sequence"),
        (r"! File not found: (.*?)\n", "File not found"),
        (r"! Font .*\? (.*?)\n", "Font error"),
        (r"! Emergency stop\.\n(.*?)\n", "Emergency stop"),
        (r"! Missing (.*?) inserted\.\n", "Missing element"),
    ]
    
    for pattern, error_type in error_patterns:
        matches = re.findall(pattern, log_content, re.DOTALL)
        for match in matches:
            msg = match.strip() if isinstance(match, str) else match[0].strip()
            errors.append({"type": error_type, "message": msg})
    
    if not errors and "Fatal error" in log_content:
        errors.append({"type": "Fatal error", "message": "编译过程中发生致命错误"})
    
    return errors


def _parse_warnings(log_content):
    """从日志中提取警告信息"""
    warnings = []
    
    warning_patterns = [
        (r"LaTeX Warning: (.*?)(?:\n\n|\nl\.)", "LaTeX Warning"),
        (r"Package (.*?) Warning: (.*?)(?:\n\n|\nl\.)", "Package Warning"),
        (r"Overfull \\hbox \((.*?) detected\)", "Overfull hbox"),
        (r"Underfull \\hbox \((.*?) detected\)", "Underfull hbox"),
        (r"Citation `(.*?)' undefined", "Undefined citation"),
        (r"Reference `(.*?)' undefined", "Undefined reference"),
    ]
    
    for pattern, warning_type in warning_patterns:
        matches = re.findall(pattern, log_content, re.DOTALL)
        for match in matches:
            msg = match.strip() if isinstance(match, str) else match[0].strip()
            warnings.append({"type": warning_type, "message": msg})
    
    return warnings


def auto_fix_common_errors(tex_file, errors):
    """尝试自动修复常见 LaTeX 错误
    
    Returns:
        dict: {fixed: [...], manual: [...]}
    """
    fixed = []
    manual = []
    
    tex_path = Path(tex_file)
    content = tex_path.read_text(encoding="utf-8")
    modified = False
    
    for error in errors:
        msg = error["message"]
        
        # 缺少宏包
        if "File not found" in msg or "Package" in msg and "not found" in msg.lower():
            manual.append({
                "error": error,
                "suggestion": f"请安装缺失的宏包。使用 tlmgr install <package-name>"
            })
        
        # 未定义引用 - 多遍编译可修复
        elif "Undefined" in error.get("type", ""):
            fixed.append({
                "error": error,
                "action": "通过多遍编译自动修复"
            })
        
        # 字体问题
        elif "Font" in error.get("type", ""):
            manual.append({
                "error": error,
                "suggestion": "请检查字体是否安装。中文论文建议使用 ctex 宏包。"
            })
        
        else:
            manual.append({
                "error": error,
                "suggestion": "请查看完整日志定位问题。"
            })
    
    return {"fixed": fixed, "manual": manual}


def export_docx_pandoc(tex_file, bib_file=None, output_path=None, reference_doc=None):
    """使用 Pandoc 将 LaTeX 转为 DOCX
    
    Args:
        tex_file: .tex 文件路径
        bib_file: .bib 文件路径（可选）
        output_path: 输出 .docx 路径
        reference_doc: 参考样式 .docx（可选）
    
    Returns:
        dict: {success, docx_path, message}
    """
    # 检测 Pandoc
    try:
        subprocess.run(["pandoc", "--version"], capture_output=True, timeout=10)
    except FileNotFoundError:
        return {
            "success": False,
            "message": "未检测到 Pandoc。请安装：\n"
                       "  Windows: https://pandoc.org/installing.html\n"
                       "  macOS: brew install pandoc\n"
                       "  Linux: sudo apt install pandoc"
        }
    
    if output_path is None:
        output_path = Path(tex_file).with_suffix(".docx")
    
    cmd = ["pandoc", tex_file, "-o", output_path]
    
    if bib_file:
        cmd.extend(["--bibliography", bib_file])
    
    if reference_doc:
        cmd.extend(["--reference-doc", reference_doc])
    
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    
    if result.returncode == 0:
        return {
            "success": True,
            "docx_path": output_path,
            "message": "DOCX 导出成功。注意：Pandoc 转换可能有格式损失。"
                       "如需精密排版，建议使用 academic-paper-writer-pro 技能。"
        }
    else:
        return {
            "success": False,
            "message": f"Pandoc 转换失败: {result.stderr}"
        }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python latex_utils.py <tex_file> [--engine xelatex|pdflatex] [--output-dir outputs]")
        print("      python latex_utils.py --detect")
        print("      python latex_utils.py --docx <tex_file> [--bib references.bib]")
        sys.exit(1)
    
    if sys.argv[1] == "--detect":
        env = detect_tex_environment()
        print(json.dumps(env, indent=2, ensure_ascii=False))
        sys.exit(0 if env["installed"] else 1)
    
    if sys.argv[1] == "--docx":
        tex = sys.argv[2]
        bib = None
        if "--bib" in sys.argv:
            bib = sys.argv[sys.argv.index("--bib") + 1]
        result = export_docx_pandoc(tex, bib)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        sys.exit(0 if result["success"] else 1)
    
    # 默认编译
    tex_file = sys.argv[1]
    engine = "xelatex"
    output_dir = "outputs"
    
    if "--engine" in sys.argv:
        engine = sys.argv[sys.argv.index("--engine") + 1]
    if "--output-dir" in sys.argv:
        output_dir = sys.argv[sys.argv.index("--output-dir") + 1]
    
    result = compile_latex(tex_file, engine, output_dir)
    print(json.dumps(result, indent=2, ensure_ascii=False))
