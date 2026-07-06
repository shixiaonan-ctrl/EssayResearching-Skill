# LaTeX 编译指南

> 本文件为 G.9 步骤 2（LaTeX 编译）和步骤 4（DOCX 导出）的详细参考。包含 TeX 环境检测、编译命令、常见错误诊断与修复、Pandoc DOCX 转换详解。

---

## 1. TeX 环境检测

### 1.1 检测命令

编译前必须逐一执行以下命令，确认对应工具已安装：

```bash
# 检测 XeLaTeX（中文编译必需）
xelatex --version

# 检测 pdfLaTeX（英文编译常用）
pdflatex --version

# 检测 latexmk（自动化编译工具，推荐）
latexmk --version

# 检测 BibTeX（参考文献处理）
bibtex --version
```

### 1.2 输出判断

| 命令 | 成功输出特征 | 失败表现 |
|------|------------|---------|
| `xelatex --version` | 输出 `XeTeX 3.x.x` 和 `TeX Live` 或 `MiKTeX` 版本信息 | `command not found` 或 `不是内部或外部命令` |
| `pdflatex --version` | 输出 `pdfTeX 3.x.x` 和发行版信息 | 同上 |
| `latexmk --version` | 输出 `Latexmk, version x.x` | 同上 |
| `bibtex --version` | 输出 `bibtex (Web2C 2024)` 或类似 | 同上 |

### 1.3 TeX 发行版识别

通过版本输出中的关键词判断本机安装的 TeX 发行版：

- **TeX Live**（Linux/macOS 常见）：版本输出包含 `TeX Live 2024` 或类似年份标识。包管理器为 `tlmgr`。
- **MiKTeX**（Windows 常见）：版本输出包含 `MiKTeX` 字样。包管理器为 MiKTeX Console 或 `mpm`。
- **MacTeX**：macOS 上的 TeX Live 发行版，功能与 TeX Live 一致。

### 1.4 环境缺失时的安装指引

**全部工具缺失时，终止编译流程，告知用户安装方法：**

| 操作系统 | 推荐发行版 | 安装命令 |
|---------|-----------|---------|
| Ubuntu/Debian | TeX Live | `sudo apt install texlive-full` |
| CentOS/RHEL | TeX Live | `sudo dnf install texlive-scheme-full` |
| macOS | MacTeX | `brew install --cask mactex` 或从 https://tug.org/mactex 下载 |
| Windows | MiKTeX | 从 https://miktex.org/download 下载安装 |
| 任意系统 | TeX Live | 从 https://tug.org/texlive/ 下载安装 |

安装完成后需重新运行检测命令确认。

---

## 2. 编译流程

### 2.1 中文论文编译（paper-zh.tex）

中文论文必须使用 `xelatex` 引擎，因为只有 XeTeX 引擎原生支持 Unicode 和中文字体。

#### 方式 A：latexmk 自动化（推荐）

```bash
cd docs/manuscripts
latexmk -xelatex -interaction=nonstopmode -file-line-error paper-zh.tex
```

`latexmk` 会自动判断需要编译几遍，自动调用 `bibtex`，无需手动管理编译次数。

#### 方式 B：手动多遍编译

```bash
cd docs/manuscripts

# 第 1 遍：生成 .aux 文件（记录交叉引用键和文献引用键）
xelatex -interaction=nonstopmode -file-line-error paper-zh.tex

# BibTeX：处理 .aux 中的文献引用，生成 .bbl 文件
bibtex paper-zh

# 第 2 遍：将 .bbl 内容和交叉引用信息写入正文
xelatex -interaction=nonstopmode -file-line-error paper-zh.tex

# 第 3 遍：确定最终页码和引用编号
xelatex -interaction=nonstopmode -file-line-error paper-zh.tex
```

**多遍编译原理说明：**

| 遍次 | 作用 | 跳过后果 |
|------|------|---------|
| 第 1 遍 xelatex | 生成 `.aux` 文件，记录所有 `\cite` 键和 `\label` 键 | BibTeX 无输入文件，参考文献无法处理 |
| bibtex | 读取 `.aux`，从 `.bib` 中提取对应文献，生成 `.bbl` | References 章节为空或显示 `[?]` |
| 第 2 遍 xelatex | 读取 `.bbl` 和 `.aux`，将文献内容和交叉引用写入正文 | 参考文献有内容但编号可能不正确 |
| 第 3 遍 xelatex | 确定最终页码，修正所有引用编号 | 图表引用页码可能错位 |

### 2.2 英文论文编译（paper-en.tex）

英文论文默认使用 `pdflatex` 引擎。若手稿导言区使用了 `\usepackage{fontspec}` 或 `\setmainfont` 等 OpenType 字体命令，则必须改用 `xelatex`。

#### 方式 A：latexmk 自动化（推荐）

```bash
cd docs/manuscripts
latexmk -pdf -interaction=nonstopmode -file-line-error paper-en.tex
```

#### 方式 B：手动多遍编译

```bash
cd docs/manuscripts

pdflatex -interaction=nonstopmode -file-line-error paper-en.tex
bibtex paper-en
pdflatex -interaction=nonstopmode -file-line-error paper-en.tex
pdflatex -interaction=nonstopmode -file-line-error paper-en.tex
```

#### 方式 C：英文稿使用 xelatex（条件性）

当 `paper-en.tex` 导言区包含以下任一命令时，必须使用 `xelatex`：

```latex
\usepackage{fontspec}
\setmainfont{...}
\setsansfont{...}
\setmonofont{...}
```

编译命令与中文稿相同（将 `paper-en.tex` 替换 `paper-zh.tex`）。

### 2.3 编译参数说明

| 参数 | 作用 |
|------|------|
| `-interaction=nonstopmode` | 遇到错误时不暂停等待用户输入，直接继续编译。必须使用，否则编译遇错时会卡住。 |
| `-file-line-error` | 错误信息以 `文件名:行号: 错误内容` 格式输出，便于快速定位。 |
| `-xelatex`（latexmk） | 指定 latexmk 使用 xelatex 引擎。 |
| `-pdf`（latexmk） | 指定 latexmk 使用 pdflatex 引擎生成 PDF。 |

### 2.4 中间文件说明

编译过程会产生以下中间文件，均在 `docs/manuscripts/` 目录下：

| 文件 | 用途 | 是否可删除 |
|------|------|-----------|
| `.aux` | 辅助文件，记录交叉引用和文献引用键 | 编译完成后可删除，但下次编译需重新生成 |
| `.bbl` | BibTeX 生成的参考文献列表 | 可删除，但需重新运行 bibtex |
| `.log` | 编译日志，包含所有错误和警告信息 | **不可删除**，步骤 3 验证需要读取 |
| `.out` | hyperref 宏包生成的 PDF 书签数据 | 可删除 |
| `.toc` | 目录数据 | 可删除 |
| `.fls` | latexmk 记录的文件依赖关系 | 可删除 |
| `.fdb_latexmk` | latexmk 的数据库 | 可删除 |
| `.synctex.gz` | SyncTeX 同步数据（编辑器正反向搜索用） | 可删除 |

建议使用 `latexmk -c` 清理中间文件（保留 PDF 和 `.log`）：

```bash
cd docs/manuscripts
latexmk -c    # 清理中间文件，保留 PDF
```

---

## 3. 常见错误诊断与修复

### 3.1 缺少宏包

**错误表现：**

```
! LaTeX Error: File 'algorithmic.sty' not found.
```

或

```
! LaTeX Error: File 'algorithm2e.sty' not found.
```

**诊断方法：**

从 `.log` 文件中提取 `.sty` 文件名，确认是哪个宏包缺失。

**修复方案：**

1. **宏包已安装但未在导言区声明**：在 `.tex` 文件导言区添加 `\usepackage{宏包名}`。
2. **宏包未安装**：

   TeX Live：
   ```bash
   tlmgr install 宏包名
   ```
   注意：`tlmgr` 需要管理员权限。某些宏包名与 `.sty` 文件名不同（如 `algorithm2e.sty` 对应宏包名 `algorithm2e`，但 `algorithmic.sty` 对应宏包名 `algorithmic`）。

   MiKTeX：MiKTeX 默认开启自动安装功能，首次编译时缺少宏包会自动提示安装。也可通过 MiKTeX Console 手动安装。

3. **安装后重新编译**：
   ```bash
   xelatex -interaction=nonstopmode -file-line-error paper-zh.tex
   ```

### 3.2 未定义引用

**错误表现：**

```
LaTeX Warning: Reference `fig:overview' on page 3 undefined on input line 87.
```

或

```
LaTeX Warning: Citation `smith2023' on page 5 undefined on input line 142.
```

**诊断方法：**

区分两类未定义引用：

| 类型 | 表现 | 原因 |
|------|------|------|
| 交叉引用未定义 | `Reference 'xxx' undefined` | `\ref{xxx}` 找不到对应的 `\label{xxx}` |
| 文献引用未定义 | `Citation 'xxx' undefined` | `\cite{xxx}` 在 `.bib` 文件中找不到对应条目 |

**修复方案：**

1. **交叉引用**：
   - 检查 `\label` 和 `\ref` 的键名是否完全一致（区分大小写）
   - 确认 `\label` 在 `\caption` 或章节命令之后（顺序错误会导致引用为空）
   - 多遍编译（通常 2-3 遍即可消除）

2. **文献引用**：
   - 检查 `.bib` 文件中是否存在对应 `@article{xxx, ...}` 条目
   - 确认 `\cite{xxx}` 的键名与 `.bib` 中 `@article` 后的键名完全一致
   - 确认 `\bibliography{references}` 声明的 `.bib` 文件名正确（不含扩展名）
   - 确认运行了 `bibtex` 命令（手动编译时容易遗漏）
   - 修复后重新执行完整的多遍编译

### 3.3 图片未找到

**错误表现：**

```
! LaTeX Error: File 'Fig_1' not found.
```

**诊断方法：**

检查 `.log` 文件中 LaTeX 搜索了哪些路径。LaTeX 默认搜索当前目录和 `TEXMF` 路径。

**修复方案：**

1. **路径错误**：`\includegraphics{Fig_1}` 中若图片在子目录，需写完整相对路径：
   ```latex
   \includegraphics{notebooks/fig/Fig_1}
   ```
   或在导言区声明图片根目录：
   ```latex
   \graphicspath{{notebooks/fig/}{figures/}}
   ```

2. **文件名错误**：确认实际文件名与 `.tex` 中引用的名称一致。注意大小写敏感（尤其在 Linux 上）。

3. **扩展名问题**：LaTeX 会自动尝试 `.pdf`、`.png`、`.jpg` 等扩展名。若图片格式不在默认列表中，需在导言区声明：
   ```latex
   \DeclareGraphicsExtensions{.pdf,.png,.jpg,.eps,.svg}
   ```

4. **图片确实不存在**：检查 `notebooks/fig/` 目录，确认对应图片已由 `figures.ipynb` 生成。

### 3.4 中文字体问题

**错误表现：**

```
! fontspec error: cannot find font "SimSun".
```

或

```
! Package fontspec Error: The font "Noto Serif CJK SC" cannot be found.
```

**诊断方法：**

检查 `.tex` 文件中的字体声明：

```latex
\setCJKmainfont{SimSun}      % ctex 方式
% 或
\setmainfont{Noto Serif CJK SC}  % fontspec 方式
```

确认系统是否安装了对应字体。

**修复方案：**

1. **使用 ctex 宏包默认字体**（最省事）：
   ```latex
   \usepackage[fontset=windows]{ctex}   % Windows 自动使用系统中文字体
   \usepackage[fontset=mac]{ctex}       % macOS 自动使用系统中文字体
   \usepackage[fontset=fandol]{ctex}    % 使用 Fandol 开源中文字体（跨平台）
   ```

2. **安装缺失字体**：
   - SimSun（宋体）：Windows 系统自带。Linux/macOS 需单独安装。
   - Noto Serif CJK SC / Noto Sans CJK SC：Google 开源字体，从 https://fonts.google.com 下载。
   - Fandol：TeX Live 自带，无需额外安装。

3. **改用系统已有字体**：列出系统已安装的中文字体：
   ```bash
   fc-list :lang=zh    # Linux/macOS
   ```
   从列表中选择可用字体替换。

4. **fontspec 与 ctex 混用注意**：若同时使用 `ctex` 和 `fontspec` 的 `\setmainfont`，中文字体声明应使用 `\setCJKmainfont`（ctex 提供），而非 `\setmainfont`（后者仅影响西文字体）。

### 3.5 Overfull hbox

**错误表现：**

```
Overfull \hbox (12.34567pt too wide) in paragraph at lines 142--145
```

**说明：**

Overfull hbox 表示某行内容超出了页面边距。这不是致命错误（编译会继续），但会导致 PDF 中文字超出页面边界。

**修复方案（按严重程度排序）：**

| 溢出宽度 | 严重程度 | 修复方案 |
|---------|---------|---------|
| < 5pt | 忽略 | 正常现象，LaTeX 断行算法的微小误差，不影响阅读 |
| 5-10pt | 轻微 | 尝试在该段落使用 `\sloppy` 或局部 `\tolerance=2000` |
| 10-30pt | 中等 | 调整文字（缩短句子、改写表述）、使用 `\linebreak` 手动断行 |
| > 30pt | 严重 | 检查是否有过长的单词/URL/公式，或表格列宽设置不当 |

**常见原因与对应修复：**

1. **长 URL 或路径不可断行**：
   ```latex
   \usepackage{xurl}  % 允许 URL 在任意字符处断行
   \url{https://very-long-url-that-causes-overfull-box.example.com/path}
   ```

2. **表格列过宽**：
   - 使用 `p{宽度}` 列类型替代 `c`/`l`
   - 使用 `\resizebox{\textwidth}{!}{表格内容}` 缩放
   - 使用 `tabularx` 宏包的自适应列宽

3. **行内公式过长**：
   - 改为行间公式 `\[ ... \]`
   - 使用 `\displaystyle` 在行内显示大型公式

4. **全局容忍度调整**（慎用，可能影响整体排版质量）：
   ```latex
   \setlength{\emergencystretch}{3em}  % 允许额外拉伸 3em
   ```

### 3.6 其他常见错误

| 错误 | 表现 | 修复 |
|------|------|------|
| 数学模式错误 | `! Missing $ inserted` | 在数学符号前后补充 `$` 或 `\[ \]` |
| 括号不匹配 | `! Missing } inserted` | 检查 `{}` 和 `\begin{}`/`\end{}` 配对 |
| 表格格式错误 | `! Extra alignment tab` | 检查 `&` 数量是否与列声明一致 |
| 重复定义 | `! LaTeX Error: Command \xxx already defined` | 使用 `\providecommand` 或 `\renewcommand` |
| 文档类冲突 | `! Class conflict` | 检查是否同时加载了冲突的文档类选项 |

---

## 4. Pandoc DOCX 转换

### 4.1 检测 Pandoc

```bash
pandoc --version
```

成功时输出 `pandoc x.x.x` 版本号。失败时 `command not found`。

**安装方法：**

| 操作系统 | 安装命令 |
|---------|---------|
| Ubuntu/Debian | `sudo apt install pandoc` |
| CentOS/RHEL | `sudo dnf install pandoc` |
| macOS | `brew install pandoc` |
| Windows | `choco install pandoc` 或从 https://pandoc.org/installing.html 下载 |
| 任意系统（Conda） | `conda install -c conda-forge pandoc` |

### 4.2 基本转换命令

```bash
cd docs/manuscripts

# 基本转换：LaTeX → DOCX，附带参考文献
pandoc paper-en.tex -o ../../outputs/paper-en.docx --bibliography=references.bib
```

**参数说明：**

| 参数 | 作用 |
|------|------|
| `paper-en.tex` | 输入文件（LaTeX 源文件） |
| `-o ../../outputs/paper-en.docx` | 输出文件路径 |
| `--bibliography=references.bib` | 指定参考文献文件，Pandoc 会将 `\cite` 替换为实际引用内容 |

### 4.3 带参考模板的转换

若用户提供了 DOCX 模板文件（包含期望的样式：字体、字号、行距、标题样式等），可使用 `--reference-doc` 参数让 Pandoc 继承模板样式：

```bash
cd docs/manuscripts

pandoc paper-en.tex -o ../../outputs/paper-en.docx \
  --bibliography=references.bib \
  --reference-doc=templates/template.docx
```

**`--reference-doc` 说明：**

- Pandoc 会从模板文件中提取以下样式信息：正文样式、标题 1-6 样式、引用段落样式、图注/表注样式等。
- 模板文件需要是用 Word 创建的 `.docx` 文件，其中定义了上述样式。
- 模板中的具体文字内容不会被复制，只提取样式定义。
- 若模板中某样式不存在，Pandoc 使用默认样式。

### 4.4 常用附加参数

| 参数 | 作用 | 示例 |
|------|------|------|
| `--number-sections` | 自动编号章节标题 | `--number-sections` |
| `--toc` | 生成目录 | `--toc --toc-depth=3` |
| `--cite-method` | 引用处理方式 | `--cite-method=citeproc`（默认） |
| `--bibliography-format` | 参考文献格式 | `--csl=ieee.csl`（使用 CSL 样式文件） |
| `--mathml` | 数学公式用 MathML（部分浏览器支持） | `--mathml` |

### 4.5 CSL 样式文件

Pandoc 默认使用 Chicago 作者-日期格式渲染参考文献。若需匹配特定会议/期刊格式，使用 CSL（Citation Style Language）文件：

```bash
# 使用 IEEE 格式
pandoc paper-en.tex -o ../../outputs/paper-en.docx \
  --bibliography=references.bib \
  --csl=ieee.csl

# 使用 ACM 格式
pandoc paper-en.tex -o ../../outputs/paper-en.docx \
  --bibliography=references.bib \
  --csl=acm.csl
```

CSL 文件可从 https://www.zotero.org/styles 下载（搜索对应期刊/会议名称）。

### 4.6 已知局限性与替代方案

| 局限性 | 详细说明 | 影响程度 |
|--------|---------|---------|
| 三线表无法精确还原 | LaTeX 的 `\toprule`/`\midrule`/`\bottomrule` 在 DOCX 中变为普通全边框表格 | 高（影响学术排版质量） |
| 数学公式转换偏差 | 简单行内公式转换正确；复杂公式（矩阵 `vmatrix`、多行对齐 `align`、自定义宏 `\newcommand`）可能丢失格式或转为图片 | 中-高 |
| 双栏排版丢失 | LaTeX 的 `twocolumn` 文档类选项在 DOCX 中无对应，输出为单栏 | 中（影响视觉一致性） |
| 页面布局不一致 | 页边距、页眉页脚、页码位置等由 DOCX 默认样式决定，与 LaTeX PDF 不同 | 中 |
| 浮动体位置变化 | LaTeX 的图表浮动算法（`[h]`/`[t]`/`[b]`）在 DOCX 中无效，图表按出现顺序 inline 排列 | 低-中 |
| 自定义宏不识别 | `\newcommand` 定义的自定义命令可能无法正确转换 | 中 |
| 颜色和背景 | `\colorbox`、`\textcolor` 等颜色命令在 DOCX 中可能丢失 | 低 |

**替代方案**：若用户对 DOCX 格式有精确要求（如投稿系统要求 DOCX 且需严格的三线表、公式排版），建议告知用户使用独立的 `academic-paper-writer-pro` skill。该 skill 专门针对 DOCX 学术论文排版进行了优化，支持逐单元增量生成 DOCX、双单元质量核查、智能配图裁剪等功能，能够实现比 Pandoc 更精确的 DOCX 输出。
