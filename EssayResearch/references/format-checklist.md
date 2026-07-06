# 格式合规检查表模板

> 本文件为 G.9 步骤 1（格式合规预检）的详细参考。包含完整检查项列表、各会议/期刊规范文件索引、每项检查的读取方法、以及自动修复能力说明。

---

## 1. 完整检查项表

执行 G.9 步骤 1 时，按以下表格逐项检查。根据 `docs/user_requirements.md` 中记录的目标会议/期刊，从 `skills/shared/format-specs/` 对应文件中读取"要求值"列。从 `.tex` 文件中读取"当前状态"列。

| 检查项 | 要求值 | 当前状态 | 结果 | 备注 |
|--------|--------|---------|------|------|
| 纸张大小 | _见下方各会议规范_ | _从 .tex 读取_ | ✅/⚠️/❌ | _差异说明_ |
| 上边距 | _见下方各会议规范_ | _从 .tex 读取_ | ✅/⚠️/❌ | _差异说明_ |
| 下边距 | _见下方各会议规范_ | _从 .tex 读取_ | ✅/⚠️/❌ | _差异说明_ |
| 左边距 | _见下方各会议规范_ | _从 .tex 读取_ | ✅/⚠️/❌ | _差异说明_ |
| 右边距 | _见下方各会议规范_ | _从 .tex 读取_ | ✅/⚠️/❌ | _差异说明_ |
| 正文字体 | _见下方各会议规范_ | _从 .tex 读取_ | ✅/⚠️/❌ | _差异说明_ |
| 正文字号 | _见下方各会议规范_ | _从 .tex 读取_ | ✅/⚠️/❌ | _差异说明_ |
| 行距 | _见下方各会议规范_ | _从 .tex 读取_ | ✅/⚠️/❌ | _差异说明_ |
| 分栏 | _见下方各会议规范_ | _从 .tex 读取_ | ✅/⚠️/❌ | _差异说明_ |
| 栏间距 | _见下方各会议规范_ | _从 .tex 读取_ | ✅/⚠️/❌ | _差异说明_ |
| 一级标题样式 | _见下方各会议规范_ | _从 .tex 读取_ | ✅/⚠️/❌ | _差异说明_ |
| 二级标题样式 | _见下方各会议规范_ | _从 .tex 读取_ | ✅/⚠️/❌ | _差异说明_ |
| 三级标题样式 | _见下方各会议规范_ | _从 .tex 读取_ | ✅/⚠️/❌ | _差异说明_ |
| 图注前缀格式 | _见下方各会议规范_ | _从 .tex 读取_ | ✅/⚠️/❌ | _差异说明_ |
| 图注字号 | _见下方各会议规范_ | _从 .tex 读取_ | ✅/⚠️/❌ | _差异说明_ |
| 图注位置 | _见下方各会议规范_ | _从 .tex 读取_ | ✅/⚠️/❌ | _差异说明_ |
| 表注前缀格式 | _见下方各会议规范_ | _从 .tex 读取_ | ✅/⚠️/❌ | _差异说明_ |
| 表注字号 | _见下方各会议规范_ | _从 .tex 读取_ | ✅/⚠️/❌ | _差异说明_ |
| 表注位置 | _见下方各会议规范_ | _从 .tex 读取_ | ✅/⚠️/❌ | _差异说明_ |
| 参考文献格式 | _见下方各会议规范_ | _从 .tex 读取_ | ✅/⚠️/❌ | _差异说明_ |
| 参考文献字号 | _见下方各会议规范_ | _从 .tex 读取_ | ✅/⚠️/❌ | _差异说明_ |
| 页眉内容 | _见下方各会议规范_ | _从 .tex 读取_ | ✅/⚠️/❌ | _差异说明_ |
| 页脚内容 | _见下方各会议规范_ | _从 .tex 读取_ | ✅/⚠️/❌ | _差异说明_ |
| 页码格式 | _见下方各会议规范_ | _从 .tex 读取_ | ✅/⚠️/❌ | _差异说明_ |
| 页码位置 | _见下方各会议规范_ | _从 .tex 读取_ | ✅/⚠️/❌ | _差异说明_ |
| 首行缩进 | _见下方各会议规范_ | _从 .tex 读取_ | ✅/⚠️/❌ | _差异说明_ |
| 段前间距 | _见下方各会议规范_ | _从 .tex 读取_ | ✅/⚠️/❌ | _差异说明_ |
| 段后间距 | _见下方各会议规范_ | _从 .tex 读取_ | ✅/⚠️/❌ | _差异说明_ |
| 摘要样式 | _见下方各会议规范_ | _从 .tex 读取_ | ✅/⚠️/❌ | _差异说明_ |
| 公式编号格式 | _见下方各会议规范_ | _从 .tex 读取_ | ✅/⚠️/❌ | _差异说明_ |

### 结果标注规范

| 标注 | 含义 | 处理方式 |
|------|------|---------|
| ✅ | 当前值与要求值一致 | 无需处理 |
| ⚠️ | 当前值与要求值不一致，但可通过修改 .tex 参数自动修复 | 直接修改 .tex 文件，修改后告知用户 |
| ❌ | 当前值与要求值不一致，且无法通过参数修改自动修复 | 列出操作步骤，指导用户手动修改后重新检查 |

---

## 2. 各会议/期刊格式规范文件索引

根据目标会议/期刊，读取对应的格式规范文件获取"要求值"：

| 目标会议/期刊 | 格式规范文件 | 关键格式特征摘要 |
|-------------|------------|----------------|
| IEEE 会议/期刊 | `skills/shared/format-specs/ieee.md` | US Letter、双栏、Times New Roman 10pt、标题罗马数字全大写（I. INTRODUCTION）、图注"Fig. N."加粗、表注"TABLE N"全大写 |
| ACM 会议/期刊 | `skills/shared/format-specs/acm.md` | 视具体会议而定、ACM 参考文献格式 |
| NeurIPS | `skills/shared/format-specs/nips.md` | US Letter、单栏、Times New Roman 11pt |
| Springer LNCS | `skills/shared/format-specs/springer_lncs.md` | A4、单栏、Times New Roman 10pt、LNCS 参考文献格式 |
| APA 第 7 版 | `skills/shared/format-specs/apa7.md` | A4、双倍行距、Times New Roman 12pt、悬挂缩进引用 |
| MLA | `skills/shared/format-specs/mla.md` | US Letter、双倍行距、Times New Roman 12pt |
| 中文学位论文 | `skills/shared/format-specs/chinese_thesis.md` | A4、单栏、宋体小四号、1.5 倍行距 |

若目标会议/期刊不在以上列表中：
1. 检查 `skills/shared/format-specs/` 目录是否有对应文件
2. 若无，从 `user_requirements.md` 读取用户指定的格式要求
3. 若用户未指定，询问用户提供格式规范文档或官方模板

---

## 3. 各检查项的读取方法

### 3.1 纸张大小

**从 .tex 读取**：检查 `\documentclass` 选项和 `geometry` 宏包声明。

```latex
\documentclass[letterpaper, 10pt]{article}    % → US Letter
\documentclass[a4paper, 11pt]{article}         % → A4
\usepackage[a4paper]{geometry}                 % → A4（geometry 优先级高于 documentclass）
```

常见值对照：

| LaTeX 选项 | 纸张尺寸 | 实际尺寸 |
|-----------|---------|---------|
| `letterpaper` | US Letter | 8.5" × 11" (216mm × 279mm) |
| `a4paper` | A4 | 210mm × 297mm |
| `legalpaper` | US Legal | 8.5" × 14" (216mm × 356mm) |
| `a5paper` | A5 | 148mm × 210mm |

### 3.2 页边距

**从 .tex 读取**：检查 `geometry` 宏包参数。

```latex
\usepackage[margin=1in]{geometry}                            % 四边等距 1 inch
\usepackage[top=1in, bottom=1in, left=1in, right=1in]{geometry}  % 分别指定
```

若未使用 `geometry` 宏包，LaTeX 默认边距约为 1.5 inch 左右（视文档类而定）。

### 3.3 正文字体

**从 .tex 读取**：检查 `fontspec` / `ctex` / `mathptmx` 等字体宏包声明。

```latex
% XeLaTeX 方式
\usepackage{fontspec}
\setmainfont{Times New Roman}

% pdfLaTeX 方式
\usepackage{mathptmx}       % Times New Roman（含数学符号）
\usepackage{newtxtext}      % New Times 文本字体

% 中文方式
\usepackage[fontset=windows]{ctex}    % 自动设置中文字体
\setCJKmainfont{SimSun}               % 手动指定中文字体
```

若未声明任何字体宏包，LaTeX 默认使用 Computer Modern 字体（不符合大多数会议/期刊要求）。

### 3.4 正文字号

**从 .tex 读取**：检查 `\documentclass` 选项。

```latex
\documentclass[10pt]{article}     % → 10pt
\documentclass[11pt]{article}     % → 11pt
\documentclass[12pt]{article}     % → 12pt
```

LaTeX 标准字号选项仅支持 10pt、11pt、12pt 三种。若需其他字号（如 9pt），需使用 `extarticle` 文档类或 `\fontsize` 命令。

### 3.5 行距

**从 .tex 读取**：检查 `\linespread`、`\setstretch` 或 `\baselinestretch` 声明。

```latex
\linespread{1.0}     % 单倍行距
\linespread{1.5}     % 1.5 倍行距
\linespread{2.0}     % 双倍行距

\usepackage{setspace}
\setstretch{1.5}     % 1.5 倍行距（setspace 方式）
```

若未声明，LaTeX 默认行距为 1.0（单倍行距）。

### 3.6 分栏

**从 .tex 读取**：检查 `\documentclass` 选项和正文中的 `\twocolumn` / `\onecolumn` 命令。

```latex
\documentclass[twocolumn]{article}    % 全文双栏
\documentclass[onecolumn]{article}    % 全文单栏（默认）
\twocolumn                            % 从此处开始双栏
\onecolumn                            % 从此处开始单栏
```

### 3.7 栏间距

**从 .tex 读取**：检查 `\columnsep` 长度设置。

```latex
\setlength{\columnsep}{0.25in}    % 栏间距 0.25 inch
\setlength{\columnsep}{20pt}      % 栏间距 20pt
```

若未设置，LaTeX 默认栏间距为 10pt。

### 3.8 一级标题样式

**从 .tex 读取**：检查文档类和标题格式宏包（`titlesec` 等）。

标准文档类的默认格式：
- `article`：`\section` 输出为阿拉伯数字编号 + 标题文本，加粗，大写
- `IEEEtran`：`\section` 输出为罗马数字编号 + 全大写标题，居中
- `acmart`：`\section` 输出为阿拉伯数字编号 + 标题文本

检查方式：
```bash
grep -n "\\\\section" paper-en.tex    # 查看所有一级标题
```

### 3.9 二级标题样式

**从 .tex 读取**：检查 `\subsection` 的输出格式。

标准文档类默认：字母编号（A.、B.、...），斜体，左对齐。
IEEE 模板：字母编号，斜体，左对齐。

### 3.10 三级标题样式

**从 .tex 读取**：检查 `\subsubsection` 的输出格式。

标准文档类默认：阿拉伯数字编号（1)、2)、...)，斜体，缩进。

### 3.11 图注前缀格式

**从 .tex 读取**：检查 `caption` 宏包的 `\captionsetup` 声明。

```latex
\usepackage{caption}
\captionsetup[figure]{labelformat=simple, labelsep=period, font=small}
% labelformat=simple → 编号为 "1", "2"
% labelsep=period   → 编号与文字间为句号："Fig. 1."
% labelsep=colon    → 编号与文字间为冒号："Figure 1:"
% font=small        → 字号为 \small（约 8-9pt）
% font=normalsize   → 字号为正常大小
```

各会议/期刊常见图注前缀：

| 会议/期刊 | 前缀格式 | labelsep |
|---------|---------|---------|
| IEEE | `Fig. 1.` | period |
| NeurIPS | `Figure 1:` | colon |
| Springer LNCS | `Fig. 1.` | period |
| APA 7 | `Figure 1` | space |
| 中文论文 | `图 1` | space |

### 3.12 图注位置

**从 .tex 读取**：检查 `\caption` 在 `figure` 环境中的位置。

```latex
\begin{figure}
    \includegraphics{...}
    \caption{...}        % ← caption 在 includegraphics 之后 = 图下方
    \label{...}
\end{figure}
```

绝大多数会议/期刊要求图注在图片下方。

### 3.13 表注前缀格式

同图注前缀格式（3.11），但检查 `\captionsetup[table]` 的设置。

各会议/期刊常见表注前缀：

| 会议/期刊 | 前缀格式 |
|---------|---------|
| IEEE | `TABLE I`（罗马数字，全大写） |
| NeurIPS | `Table 1:` |
| Springer LNCS | `Table 1.` |
| 中文论文 | `表 1` |

### 3.14 表注位置

**从 .tex 读取**：检查 `\caption` 在 `table` 环境中相对于 `\begin{tabular}` 的位置。

```latex
\begin{table}
    \caption{...}        % ← caption 在 tabular 之前 = 表上方
    \begin{tabular}{...}
        ...
    \end{tabular}
\end{table}
```

各会议/期刊要求：

| 会议/期刊 | 表注位置 |
|---------|---------|
| IEEE | 表上方 |
| NeurIPS | 表上方 |
| Springer LNCS | 表上方 |
| APA 7 | 表上方（标题）+ 表下方（注释） |

### 3.15 参考文献格式

**从 .tex 读取**：检查 `\bibliographystyle` 声明。

```latex
\bibliographystyle{IEEEtran}              % IEEE 格式
\bibliographystyle{ACM-Reference-Format}  % ACM 格式
\bibliographystyle{plain}                 % 通用格式（按字母排序）
\bibliographystyle{unsrt}                 % 按引用顺序排列
\bibliographystyle{alpha}                 % 键名标签
```

若使用 `biblatex`：
```latex
\usepackage[style=ieee, backend=biber]{biblatex}
\usepackage[style=authoryear, backend=biber]{biblatex}
```

### 3.16 页眉页脚

**从 .tex 读取**：检查 `\pagestyle` 和 `fancyhdr` 宏包设置。

```latex
\pagestyle{empty}       % 无页眉页脚
\pagestyle{plain}       % 仅页码（底部居中）
\pagestyle{headings}    % 页眉显示章节信息

\usepackage{fancyhdr}
\pagestyle{fancy}
\fancyhf{}                              % 清空所有
\fancyhead[L]{Author Name}              % 左页眉
\fancyhead[R]{Paper Title (Short)}      % 右页眉
\fancyfoot[C]{\thepage}                 % 中页脚（页码）
```

### 3.17 页码格式

**从 .tex 读取**：检查 `\pagenumbering` 命令。

```latex
\pagenumbering{arabic}    % 阿拉伯数字 1, 2, 3
\pagenumbering{roman}     % 小写罗马数字 i, ii, iii
\pagenumbering{Roman}     % 大写罗马数字 I, II, III
\pagenumbering{alph}      % 字母 a, b, c
```

部分论文使用混合页码：前言部分用罗马数字，正文从阿拉伯数字重新开始：

```latex
\frontmatter              % 罗马数字页码（仅 book 类）
\pagenumbering{roman}
% ... 前言内容 ...
\mainmatter               % 阿拉伯数字页码（仅 book 类）
\pagenumbering{arabic}
\setcounter{page}{1}      % 重置页码为 1
```

### 3.18 首行缩进

**从 .tex 读取**：检查 `\parindent` 和 `\indent` / `\noindent` 使用。

```latex
\setlength{\parindent}{15pt}     % 首行缩进 15pt（约 0.2 inch）
\setlength{\parindent}{0pt}      % 无首行缩进
\setlength{\parindent}{1em}      % 首行缩进 1 个字宽
```

若未设置，LaTeX 默认首行缩进为 15pt（`article` 文档类）。

### 3.19 段间距

**从 .tex 读取**：检查 `\parskip` 长度设置。

```latex
\setlength{\parskip}{0pt}        % 无段间距
\setlength{\parskip}{6pt}        % 段间距 6pt
\setlength{\parskip}{0.5em}      % 段间距 0.5 字宽
```

若未设置，LaTeX 默认段间距为 0pt（靠首行缩进区分段落）。

---

## 4. 自动修复能力说明

### 4.1 可自动修复的检查项

以下检查项可通过直接修改 `.tex` 文件中的参数声明自动修复，无需修改文档内容：

| 检查项 | 修复方式 | 修改示例 |
|--------|---------|---------|
| 纸张大小 | 修改 `\documentclass` 选项或 `geometry` 参数 | `[letterpaper]` → `[a4paper]` |
| 上/下/左/右边距 | 修改 `geometry` 宏包参数 | `margin=0.8in` → `margin=1in` |
| 字号 | 修改 `\documentclass` 选项 | `[11pt]` → `[10pt]` |
| 行距 | 修改 `\linespread` 或 `\setstretch` 值 | `\linespread{1.0}` → `\linespread{1.5}` |
| 分栏 | 修改 `\documentclass` 选项 | `[onecolumn]` → `[twocolumn]` |
| 栏间距 | 修改 `\columnsep` 值 | `10pt` → `0.25in` |
| 图注前缀格式 | 修改 `\captionsetup[figure]` 参数 | `labelsep=space` → `labelsep=period` |
| 图注字号 | 修改 `\captionsetup[figure]` 的 `font` 参数 | `font=normalsize` → `font=small` |
| 表注前缀格式 | 修改 `\captionsetup[table]` 参数 | 同图注 |
| 表注字号 | 修改 `\captionsetup[table]` 的 `font` 参数 | 同图注 |
| 表注位置 | 移动 `\caption` 在 `table` 环境中的位置 | 从 tabular 后移到前 |
| 参考文献格式 | 修改 `\bibliographystyle` 声明 | `{plain}` → `{IEEEtran}` |
| 页眉页脚 | 修改 `\pagestyle` 和 `\fancyhf` 设置 | `plain` → `fancy` + 添加 fancyhf |
| 页码格式 | 修改 `\pagenumbering` 命令 | `{roman}` → `{arabic}` |
| 首行缩进 | 修改 `\parindent` 值 | `0pt` → `15pt` |
| 段间距 | 修改 `\parskip` 值 | `0pt` → `6pt` |
| 摘要样式 | 修改 `abstract` 环境的 `\renewenvironment` 参数 | 调整字号、缩进 |

### 4.2 需手动处理的检查项

以下检查项无法通过简单参数修改修复，需要用户手动干预：

| 检查项 | 需手动处理的原因 | 指导用户执行的操作 |
|--------|----------------|------------------|
| 正文字体 | 需确认系统已安装目标字体；需选择正确的字体声明方式 | 安装对应字体；添加 `fontspec` + `\setmainfont` 或使用 `ctex` 宏包 |
| 一级标题样式 | 标题编号格式由文档类（`.cls`）控制，无法仅通过参数修改 | 更换为会议/期刊官方文档类（如 `IEEEtran.cls`、`acmart.cls`） |
| 二级标题样式 | 同上 | 同上，或使用 `titlesec` 宏包重定义 |
| 三级标题样式 | 同上 | 同上 |
| 公式编号格式 | 由文档类和 `amsmath` 宏包控制 | 使用 `\tag` 手动编号，或切换文档类 |

### 4.3 自动修复执行流程

1. 识别所有标记为"⚠️"的检查项
2. 逐一修改 `.tex` 文件中对应的参数声明
3. 记录每项修改的内容（原值 → 新值）
4. 所有修改完成后，告知用户修改摘要
5. 修改后的 `.tex` 文件将用于步骤 2 的 LaTeX 编译

### 4.4 手动处理项的告知格式

对标记为"❌"的检查项，按以下格式输出操作指引：

```
❌ 需手动处理的检查项：

1. [正文字体] 当前使用 Computer Modern（默认字体），要求 Times New Roman
   原因：需确认系统已安装 Times New Roman 字体后才能声明
   操作步骤：
   a. 确认字体已安装（Linux: fc-list | grep "Times New Roman"）
   b. 在导言区添加：
      \usepackage{fontspec}
      \setmainfont{Times New Roman}
   c. 若使用 pdflatex，改用 \usepackage{mathptmx}
   d. 修改后重新执行 /research[G.9]-format

2. [一级标题样式] 当前使用 article 默认样式，要求 IEEE 罗马数字全大写居中
   原因：标题编号格式由文档类控制，无法通过参数修改
   操作步骤：
   a. 下载 IEEEtran.cls 模板
   b. 将 IEEEtran.cls 放入 docs/manuscripts/templates/ 目录
   c. 修改 \documentclass 为 \documentclass[conference]{IEEEtran}
   d. 根据 IEEEtran 模板调整导言区
   e. 修改后重新执行 /research[G.9]-format
```

用户完成手动修改后，需重新执行 `/research[G.9]-format`，步骤 1 会重新检查所有项，确认手动处理项已修复后方可继续步骤 2 编译。
