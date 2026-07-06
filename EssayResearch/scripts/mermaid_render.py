#!/usr/bin/env python3
"""Mermaid 架构图高清渲染脚本 - EssayResearch G.0/G.1 阶段使用

功能：
1. 从 Markdown/LaTeX 文件中提取 Mermaid 代码块
2. 清洗常见语法问题（subgraph 空格、引号等）
3. 调用 npx mmdc 渲染为高清 PNG
4. 自动重试与语法自愈
"""

import subprocess
import sys
import os
import re
import json
from pathlib import Path


def extract_mermaid_blocks(file_path):
    """从文件中提取 Mermaid 代码块
    
    Args:
        file_path: .md 或 .tex 文件路径
    
    Returns:
        list: [{index, code, start_line, end_line}]
    """
    content = Path(file_path).read_text(encoding="utf-8")
    blocks = []
    
    # Markdown 代码块: ```mermaid ... ```
    pattern_md = r"```mermaid\r?\n([\s\S]*?)```"
    for i, match in enumerate(re.finditer(pattern_md, content)):
        blocks.append({
            "index": i,
            "code": match.group(1).strip(),
            "start_line": content[:match.start()].count("\n") + 1,
            "end_line": content[:match.end()].count("\n") + 1,
            "type": "markdown"
        })
    
    # LaTeX 注释块: % mermaid: ... % end
    pattern_tex = r"%\s*mermaid:\s*\n([\s\S]*?)%\s*end"
    for i, match in enumerate(re.finditer(pattern_tex, content)):
        blocks.append({
            "index": len(blocks),
            "code": match.group(1).strip(),
            "start_line": content[:match.start()].count("\n") + 1,
            "end_line": content[:match.end()].count("\n") + 1,
            "type": "latex"
        })
    
    return blocks


def sanitize_mermaid(code):
    """清洗 Mermaid 代码中的常见语法问题
    
    Returns:
        tuple: (sanitized_code, fixes_applied)
    """
    fixes = []
    sanitized = code
    
    # 1. 将旧语法 usecaseDiagram 替换为 flowchart
    if re.search(r"^\s*usecaseDiagram", sanitized, re.MULTILINE):
        sanitized = re.sub(r"usecaseDiagram", "flowchart", sanitized)
        fixes.append("usecaseDiagram → flowchart")
    
    # 2. subgraph 命名中的空格替换为下划线
    subgraph_pattern = r"subgraph\s+([^\[\]]+?)(\s*\[)"
    def replace_subgraph(m):
        name = m.group(1).strip().replace(" ", "_")
        return f"subgraph {name}{m.group(2)}"
    sanitized = re.sub(subgraph_pattern, replace_subgraph, sanitized)
    if sanitized != code:
        fixes.append("subgraph 命名空格 → 下划线")
    
    # 3. 移除实体属性中的危险引号
    sanitized = re.sub(r'(\w+)\s*""', r'\1', sanitized)
    
    # 4. 统一换行符为 \n
    sanitized = sanitized.replace("\r\n", "\n").replace("\r", "\n")
    
    return sanitized, fixes


def render_mermaid(mmd_file, output_png, config_file=None):
    """渲染 Mermaid 文件为 PNG
    
    Args:
        mmd_file: .mmd 文件路径
        output_png: 输出 .png 路径
        config_file: Puppeteer 配置文件（可选）
    
    Returns:
        dict: {success, output_path, error}
    """
    # 确保 Puppeteer 配置存在
    if config_file is None:
        config_file = "puppeteer-config.json"
        with open(config_file, "w") as f:
            json.dump({"args": ["--no-sandbox", "--disable-setuid-sandbox"]}, f)
    
    cmd = [
        "npx", "mmdc",
        "-i", mmd_file,
        "-o", output_png,
        "-b", "transparent",
        "-p", config_file,
        "-w", "2400"  # 高分辨率
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            return {"success": True, "output_path": output_png}
        else:
            return {"success": False, "error": result.stderr}
    except subprocess.TimeoutExpired:
        return {"success": False, "error": "渲染超时（60秒）"}
    except FileNotFoundError:
        return {
            "success": False,
            "error": "未检测到 npx。请安装 Node.js: https://nodejs.org/"
        }


def render_with_auto_heal(code, output_dir, index=0):
    """渲染 Mermaid 代码块，带语法自愈
    
    Args:
        code: Mermaid 代码
        output_dir: 输出目录
        index: 图编号
    
    Returns:
        dict: {success, png_path, fixes_applied, attempts}
    """
    os.makedirs(output_dir, exist_ok=True)
    
    mmd_file = Path(output_dir) / f"fig_{index}.mmd"
    png_file = Path(output_dir) / f"fig_{index}.png"
    
    max_attempts = 3
    all_fixes = []
    
    for attempt in range(max_attempts):
        # 清洗语法
        sanitized, fixes = sanitize_mermaid(code)
        all_fixes.extend(fixes)
        
        # 写入 .mmd 文件
        mmd_file.write_text(sanitized, encoding="utf-8")
        
        # 尝试渲染
        result = render_mermaid(str(mmd_file), str(png_file))
        
        if result["success"]:
            return {
                "success": True,
                "png_path": str(png_file),
                "fixes_applied": all_fixes,
                "attempts": attempt + 1
            }
        
        # 渲染失败，尝试更激进的修复
        if attempt == 0:
            # 移除所有引号
            code = code.replace('"', '').replace("'", "")
            all_fixes.append("移除所有引号")
        elif attempt == 1:
            # 简化 subgraph 为普通节点
            code = re.sub(r"subgraph\s+", "%% ", code)
            all_fixes.append("subgraph → 注释（降级处理）")
    
    return {
        "success": False,
        "error": result.get("error", "未知错误"),
        "fixes_applied": all_fixes,
        "attempts": max_attempts
    }


def process_file(file_path, output_dir="resources/figures"):
    """处理文件中的所有 Mermaid 代码块
    
    Args:
        file_path: 输入文件路径
        output_dir: 图片输出目录
    
    Returns:
        dict: {total, rendered, failed, details}
    """
    blocks = extract_mermaid_blocks(file_path)
    
    if not blocks:
        return {"total": 0, "rendered": 0, "failed": 0, "details": []}
    
    results = []
    rendered = 0
    failed = 0
    
    for block in blocks:
        result = render_with_auto_heal(block["code"], output_dir, block["index"])
        
        if result["success"]:
            rendered += 1
            results.append({
                "index": block["index"],
                "status": "success",
                "png_path": result["png_path"],
                "fixes": result["fixes_applied"],
                "attempts": result["attempts"]
            })
        else:
            failed += 1
            results.append({
                "index": block["index"],
                "status": "failed",
                "error": result["error"],
                "fixes": result["fixes_applied"]
            })
    
    return {
        "total": len(blocks),
        "rendered": rendered,
        "failed": failed,
        "details": results
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python mermaid_render.py <file.md|file.tex> [--output-dir resources/figures]")
        sys.exit(1)
    
    file_path = sys.argv[1]
    output_dir = "resources/figures"
    
    if "--output-dir" in sys.argv:
        output_dir = sys.argv[sys.argv.index("--output-dir") + 1]
    
    result = process_file(file_path, output_dir)
    print(json.dumps(result, indent=2, ensure_ascii=False))
