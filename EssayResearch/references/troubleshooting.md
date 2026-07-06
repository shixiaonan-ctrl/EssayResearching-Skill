# 避坑指南与故障排除

> 本文件整合 academic-paper-writer-pro §8 的避坑指南与 ResearchPilot 实践中遇到的实际问题。
> 用途：为 EssayResearch 技能的使用者和维护者提供已知问题的原因分析与解决方案。

---

## 一、Markdown 嵌套加粗解析：正则剥离方案

### 1.1 问题描述

学术论文中常见嵌套加粗用法，例如：

```markdown
**本系统采用 **Transformer** 架构进行特征提取**
```

标准 Markdown 解析器（如 `marked`）的 lexer **不做深度递归**——它从左到右匹配 `**` 对，遇到第一个闭合 `**` 就结束加粗。上述文本会被解析为：

```
<strong>本系统采用 </strong>Transformer** 架构进行特征提取**
```

结果是：加粗在"采用"后就截断了，后面的"Transformer** 架构…"变成了混乱的未闭合标记。这导致下游 DOCX/PDF 排版时格式错乱。

### 1.2 根因分析

| 解析器 | 行为 | 是否深度递归 |
|--------|------|-------------|
| marked.js | 线性扫描 `**` 对，不回溯 | 否 |
| markdown-it | 线性扫描，但有更严格的配对逻辑 | 否（但更鲁棒） |
| CommonMark 规范 | 明确规定不处理嵌套强调 | 否（规范如此） |

CommonMark 规范有意不支持嵌套加粗，因为嵌套加粗的语义不明确（外层加粗内部的加粗应该怎么渲染？）。

### 1.3 解决方案：正则手动切分

在将 Markdown 送入 `marked` 之前，用正则预处理，将嵌套加粗拆解为非嵌套结构：

```javascript
/**
 * 嵌套加粗预处理：将 **外层 **内层** 外层** 拆解为 **外层** 内层(加粗) **外层**
 * 策略：找到嵌套的 ** 对，将外层拆为两段，内层独立加粗
 */
function flattenNestedBold(text) {
  // 匹配 **...**...**...** 模式（4个**，表示嵌套）
  const nestedPattern = /\*\*(.+?)\*\*(.+?)\*\*(.+?)\*\*/g;
  return text.replace(nestedPattern, (match, p1, p2, p3) => {
    // 拆解为：**p1** **p2** **p3**（三段独立加粗，中间不留间隙）
    return `**${p1.trim()}** **${p2.trim()}** **${p3.trim()}**`;
  });
}
```

### 1.4 使用建议

| 场景 | 建议 |
|------|------|
| 用户提交的 MD 文档含嵌套加粗 | 预处理阶段调用 `flattenNestedBold` |
| AI 生成的论文文本 | 生成时即避免嵌套加粗（在 prompt 中约束） |
| 从 DOCX 逆向转换的 MD | 检查并清理嵌套加粗 |

### 1.5 验证方法

```bash
# 测试嵌套加粗解析
echo '**外层 **内层** 外层**' | node -e "
const marked = require('marked');
const input = require('fs').readFileSync('/dev/stdin', 'utf8');
console.log('原始解析:', marked.parse(input));
"
# 预期：加粗在"内层"前截断 → 确认问题存在
# 修复后：三段独立加粗 → 确认问题解决
```

---

## 二、Mermaid 编译器的极端脆弱性与语法清洗

### 2.1 问题描述

Mermaid 是用于在 Markdown 中绘制流程图、时序图、架构图的工具。但 Mermaid 编译器对语法错误**极度敏感**，微小的语法偏差就会导致编译崩溃，且错误信息往往不可读。

### 2.2 已知崩溃场景

| # | 崩溃场景 | 错误现象 | 根因 |
|---|---------|---------|------|
| 1 | subgraph 命名含空格 | `Parse error on line X` | Mermaid 的 subgraph 语法要求名称中不含空格，或必须用引号包裹 |
| 2 | 节点标签含特殊字符 | 图表渲染为空白或报错 | `()`、`{}`、`[]`、`|` 等字符被解释为 Mermaid 语法而非文本 |
| 3 | 引号不配对 | 编译器崩溃 | 单引号/双引号未闭合导致 lexer 状态混乱 |
| 4 | 连线箭头语法错误 | 图表断裂 | `-->` 写成 `->` 或 `---` 缺少箭头 |
| 5 | 中文标点混入 | 渲染异常 | Mermaid 语法使用英文标点，中文全角标点（——、：）导致解析失败 |
| 6 | 节点 ID 含保留字 | 编译失败 | 使用 `end`、`subgraph`、`graph` 等保留字作为节点 ID |

### 2.3 语法清洗方案

在将 Mermaid 代码块送入编译器之前，执行以下清洗步骤：

```javascript
/**
 * Mermaid 语法清洗
 * 在编译前对 Mermaid 源码做容错处理
 */
function sanitizeMermaid(code) {
  return code
    // 1. subgraph 命名中的空格：用下划线替换或加引号
    .replace(/subgraph\s+([^\s\[\]{}]+)\s+([^\n]+)/g, (match, id, label) => {
      // 如果 subgraph 后跟的名称含空格，包裹引号
      const hasSpaceInId = /\s/.test(id);
      if (hasSpaceInId) {
        return `subgraph "${id}" ${label}`;
      }
      return match;
    })
    // 2. 节点标签中的特殊字符：用引号包裹标签文本
    .replace(/(\w+)\[["']?([^"'\]]+)["']?\]/g, (match, id, label) => {
      // 如果标签含特殊字符，用双引号包裹
      if (/[(){}\[\]|]/.test(label)) {
        return `${id}["${label}"]`;
      }
      return match;
    })
    // 3. 清理不配对的引号：删除孤立的引号
    .replace(/(?<!\w)["'](?!["\s])/g, '')
    // 4. 中文标点转英文：在 Mermaid 语法区域
    .replace(/——/g, '--')
    .replace(/：/g, ':')
    // 5. 保留字检测：在节点 ID 后加后缀
    .replace(/\b(end|subgraph|graph|flowchart)\b(?=\[|\{|\(|-->|---)/g, '$1_node');
}
```

### 2.4 Puppeteer --no-sandbox 配置

Mermaid 的渲染依赖 Puppeteer（无头 Chrome），在容器化/沙箱环境中运行时，Chrome 默认启用沙箱会导致启动失败：

```
Error: Failed to launch the browser process!
No usable sandbox!
```

**解决方案**：在 Puppeteer 启动参数中添加 `--no-sandbox`：

```javascript
const browser = await puppeteer.launch({
  args: [
    '--no-sandbox',
    '--disable-setuid-sandbox',
    '--disable-dev-shm-usage',  // 解决容器内 /dev/shm 空间不足
  ],
  headless: 'new',
});
```

**安全提示**：`--no-sandbox` 会降低 Chrome 的安全隔离。仅在受信任的环境中使用（如本地开发、受控的 CI/CD 容器）。不要在处理不受信任输入的生产环境中使用。

### 2.5 Mermaid 故障排查清单

- [ ] subgraph 名称是否含空格？（含空格需加引号）
- [ ] 节点标签是否含特殊字符？（含特殊字符需加引号）
- [ ] 引号是否全部配对？
- [ ] 是否有中文标点混入语法区域？
- [ ] 节点 ID 是否使用了保留字？
- [ ] Puppeteer 是否配置了 `--no-sandbox`？
- [ ] 容器内 `/dev/shm` 空间是否充足？（不足时加 `--disable-dev-shm-usage`）

---

## 三、跨平台正则匹配换行符陷阱

### 3.1 问题描述

Windows 系统使用 `\r\n`（CRLF）作为换行符，Unix/Linux/macOS 系统使用 `\n`（LF）。当正则表达式只匹配 `\n` 而输入文件使用 `\r\n` 时，匹配会失败或产生异常结果。

### 3.2 典型故障

```javascript
// 问题代码：只匹配 \n
const lines = text.split('\n');
// 在 Windows 上，每行末尾会残留一个 \r
// 导致后续的 .trim() 可能漏掉 \r，或字符串比较失败

// 另一个问题：多行正则不匹配
const pattern = /第一章.*?第二章/s;  // s 标志使 . 匹配 \n，但不匹配 \r
// 在 Windows 上，\r\n 中的 \r 不会被 . 匹配，导致跨行匹配失败
```

### 3.3 解决方案

| 方案 | 代码 | 适用场景 |
|------|------|---------|
| 容错正则 | `\r?\n` | 在正则中用 `\r?\n` 匹配可选的 `\r` + `\n` |
| 统一化预处理 | `text.replace(/\r\n/g, '\n').replace(/\r/g, '\n')` | 在处理前将所有换行符统一为 `\n` |
| Node.js readline | `require('readline').createReadStream()` | 逐行读取文件时自动处理换行符差异 |

### 3.4 推荐做法

在 EssayResearch 的所有文本处理入口处，**统一执行换行符归一化**：

```javascript
/**
 * 换行符归一化：将 \r\n 和 \r 统一为 \n
 * 应在所有文本处理的第一步执行
 */
function normalizeNewlines(text) {
  return text
    .replace(/\r\n/g, '\n')   // Windows CRLF → LF
    .replace(/\r/g, '\n');     // 旧 Mac CR → LF（罕见但容错）
}

// 在正则中使用 \r? 而非裸 \n
const paragraphPattern = /([^\n]+)\r?\n\r?\n([^\n]+)/g;
```

### 3.5 验证方法

```bash
# 检测文件的换行符类型
file example.md
# 输出 "ASCII text, with CRLF line terminators" → Windows 格式
# 输出 "ASCII text" → Unix 格式

# 或用 od 查看字节
head -c 100 example.md | od -c | head
# \r\n 出现 → CRLF
# 仅 \n → LF
```

---

## 四、LaTeX 编译常见错误处理

### 4.1 缺少宏包

**现象**：
```
! LaTeX Error: File `hyperref.sty' not found.
! LaTeX Error: File `ctex.sty' not found.
```

**原因**：LaTeX 发行版（如 TeX Live、MiKTeX）未安装对应宏包。

**解决方案**：

| 发行版 | 安装命令 | 说明 |
|--------|---------|------|
| TeX Live (Linux/macOS) | `tlmgr install hyperref ctex` | 需要 root 权限 |
| TeX Live (Windows) | `tlmgr install hyperref ctex` | 在管理员命令提示符中运行 |
| MiKTeX | 自动安装（默认开启）或 `mpm --install=hyperref` | MiKTeX 可配置为按需自动安装宏包 |

**常用宏包清单**（学术论文常用）：

| 宏包 | 用途 | 缺少时的错误关键词 |
|------|------|------------------|
| `ctex` | 中文支持 | `ctex.sty not found` |
| `hyperref` | 超链接/书签 | `hyperref.sty not found` |
| `graphicx` | 插入图片 | `graphicx.sty not found` |
| `amsmath` | 数学公式 | `amsmath.sty not found` |
| `booktabs` | 三线表 | `booktabs.sty not found` |
| `geometry` | 页面尺寸 | `geometry.sty not found` |
| `biblatex` | 参考文献管理 | `biblatex.sty not found` |
| `listings` | 代码高亮 | `listings.sty not found` |

### 4.2 引用未定义

**现象**：
```
! Undefined control sequence.
l.25 \somemacro
```

**原因**：使用了未定义的命令，通常是因为：
- 宏包未加载（如用了 `\href` 但没加载 `hyperref`）
- 命令拼写错误（如 `\tetbf` 应为 `\textbf`）
- 自定义命令未定义

**排查步骤**：
1. 查看错误行号，定位出错命令。
2. 检查该命令所属宏包是否已 `\usepackage{...}` 加载。
3. 检查命令拼写是否正确。
4. 如果是自定义命令，检查是否在 preamble 中 `\newcommand` 定义。

**常见拼写错误**：

| 错误 | 正确 | 说明 |
|------|------|------|
| `\tetbf` | `\textbf` | 粗体 |
| `\fref` | `\ref` | 引用 |
| `\cit` | `\cite` | 文献引用 |
| `\usepacakge` | `\usepackage` | 加载宏包 |

### 4.3 中文字体问题

**现象**：
```
! Package fontspec Error: The font "SimSun" cannot be found.
```

或编译成功但中文显示为方块/乱码。

**原因与解决方案**：

| 编译引擎 | 中文方案 | 常见问题 | 解决方案 |
|---------|---------|---------|---------|
| pdfLaTeX | `CTeX` 宏包 | 找不到中文字体 | 安装 Windows 自带字体（宋体/黑体）或安装 `fandol` 字体包 |
| XeLaTeX | `xeCJK` / `ctex` | 系统未安装指定字体 | `fc-list :lang=zh` 查看已安装中文字体，选择可用的 |
| LuaLaTeX | `luatexja` | 字体名不匹配 | 使用字体的实际文件名或 PostScript 名 |

**字体检测命令**：

```bash
# Linux/macOS：列出已安装的中文字体
fc-list :lang=zh family

# Windows (PowerShell)：列出已安装字体
Get-ChildItem "C:\Windows\Fonts" | Where-Object { $_.Name -match "sim|msyh|msyhbd" }
```

**常见中文字体名称映射**：

| 系统字体 | LaTeX 中的名称 | 说明 |
|---------|---------------|------|
| 宋体 (SimSun) | `SimSun` 或 `宋体` | 正文字体 |
| 黑体 (SimHei) | `SimHei` 或 `黑体` | 标题字体 |
| 微软雅黑 | `Microsoft YaHei` | 无衬线字体 |
| 仿宋 (FangSong) | `FangSong` 或 `仿宋` | 公文常用 |
| 楷体 (KaiTi) | `KaiTi` 或 `楷体` | 引用字体 |

### 4.4 图片路径问题

**现象**：
```
! LaTeX Error: File `figures/arch' not found.
```

或图片未显示在 PDF 中。

**原因**：
- 图片路径使用了反斜杠 `\`（Windows 习惯），LaTeX 要求正斜杠 `/`
- 图片文件名含空格或特殊字符
- 图片路径相对于 `.tex` 文件的位置不正确
- 未指定图片扩展名且有多 个同名不同扩展名的文件

**解决方案**：

```latex
% 正确：使用正斜杠，指定扩展名
\includegraphics[width=0.8\textwidth]{figures/architecture.png}

% 错误：反斜杠路径
\includegraphics[width=0.8\textwidth]{figures\architecture.png}

% 建议在 preamble 中设置图片根目录
\graphicspath{{figures/}{images/}{assets/}}
% 之后可以直接用文件名（不含路径）
\includegraphics[width=0.8\textwidth]{architecture.png}
```

**图片路径排查清单**：
- [ ] 路径是否使用正斜杠 `/`？
- [ ] 文件名是否含空格或特殊字符？（建议用下划线代替空格）
- [ ] 是否指定了图片扩展名？
- [ ] 图片文件是否实际存在于指定路径？
- [ ] 是否设置了 `\graphicspath`？

---

## 五、Pandoc DOCX 导出格式有损提示

### 5.1 问题描述

Pandoc 是强大的文档格式转换工具，可将 Markdown 转换为 DOCX。但 Pandoc 的转换是**有损的**——它会丢失部分格式信息，尤其是学术论文需要的精密排版要素。

### 5.2 已知的格式损失

| 格式要素 | Pandoc 转换后的状态 | 损失程度 |
|---------|-------------------|---------|
| 三线表 | 转为普通表格，丢失三线表的线型规则 | 严重 |
| 多列表格 | 基本保留但列宽可能变化 | 中等 |
| 公式编号 | 公式可转换但编号丢失 | 严重 |
| 交叉引用 | 部分丢失，图/表引用可能变为"??" | 严重 |
| 页眉页脚 | 丢失 | 严重 |
| 页码 | 丢失 | 严重 |
| 分页控制 | 丢失（无法指定章节分页） | 中等 |
| 字体微调 | 丢失（无法指定段内字体变化） | 轻微 |
| 图表标题样式 | 转为普通段落，丢失"图 X"/"表 X"前缀格式 | 中等 |
| 参考文献格式 | 基本保留但与目标格式可能有偏差 | 中等 |

### 5.3 使用建议

| 场景 | 推荐工具 | 原因 |
|------|---------|------|
| 快速预览论文草稿 | Pandoc | 速度快，格式损失可接受 |
| 正式论文排版 | academic-paper-writer-pro | 精密排版，保留全部格式要素 |
| 从 MD 转 DOCX 后需人工调整 | Pandoc + Word 手动修复 | 适合小论文或非正式文档 |
| 学位论文/期刊投稿 | academic-paper-writer-pro | 格式要求严格，Pandoc 无法满足 |

### 5.4 Pandoc 导出时的最佳实践

如果确实需要使用 Pandoc 导出 DOCX，以下措施可减少格式损失：

```bash
# 1. 使用参考文档（reference doc）控制样式
pandoc input.md -o output.docx --reference-doc=reference.docx

# 2. 使用过滤器处理特殊格式
pandoc input.md -o output.docx --filter pandoc-crossref

# 3. 指定数学公式处理方式
pandoc input.md -o output.docx --mathml

# 4. 保留 YAML 元数据
pandoc input.md -o output.docx --metadata title="论文标题"
```

**提示**：即使使用上述措施，Pandoc 导出的 DOCX 仍无法达到学术排版标准。对于精密排版需求，请使用 academic-paper-writer-pro 的逐单元增量生成 DOCX 管道。

---

## 六、LaTeX 环境缺失的检测与引导安装

### 6.1 检测逻辑

EssayResearch 在需要使用 LaTeX 编译时，首先检测系统是否安装了 LaTeX 环境：

```bash
# 检测 LaTeX 是否可用
which pdflatex 2>/dev/null || where pdflatex 2>/dev/null
which xelatex 2>/dev/null || where xelatex 2>/dev/null
which lualatex 2>/dev/null || where lualatex 2>/dev/null

# 检测 TeX 包管理器
which tlmgr 2>/dev/null || where tlmgr 2>/dev/null
which mpm 2>/dev/null || where mpm 2>/dev/null
```

### 6.2 检测结果与引导

| 检测结果 | 状态 | 引导动作 |
|---------|------|---------|
| `pdflatex` / `xelatex` 均存在 | 环境就绪 | 继续编译流程 |
| 仅 `pdflatex` 存在 | 部分就绪 | 中文论文需要 `xelatex`，提示安装完整版 |
| 均不存在但 `tlmgr` 存在 | TeX Live 已装但未配置 PATH | 引导用户将 TeX Live bin 目录加入 PATH |
| 均不存在 | 环境缺失 | 引导用户安装 LaTeX 发行版 |

### 6.3 安装引导

**Windows**：

| 发行版 | 下载地址 | 安装建议 |
|--------|---------|---------|
| TeX Live | https://tug.org/texlive/ | 完整安装（约 5GB），包含所有常用宏包 |
| MiKTeX | https://miktex.org/download | 按需安装（初始约 200MB），使用时自动下载宏包 |

**macOS**：

| 发行版 | 安装命令 | 说明 |
|--------|---------|------|
| MacTeX | `brew install --cask mactex` | 完整安装（约 4GB） |
| BasicTeX | `brew install --cask basictex` | 精简安装（约 100MB），需手动安装宏包 |

**Linux**：

| 发行版 | 安装命令 | 说明 |
|--------|---------|------|
| TeX Live (Ubuntu/Debian) | `sudo apt install texlive-full` | 完整安装 |
| TeX Live (CentOS/RHEL) | `sudo dnf install texlive-scheme-full` | 完整安装 |
| TeX Live (Arch) | `sudo pacman -S texlive` | 完整安装 |

### 6.4 PATH 配置

安装后如果命令行找不到 `pdflatex`，需要配置 PATH：

```bash
# Windows (PowerShell)：将 TeX Live bin 目录加入 PATH
$texpath = "C:\texlive\2024\bin\windows"
[Environment]::SetEnvironmentVariable("Path", $env:Path + ";$texpath", "User")

# macOS/Linux：在 ~/.bashrc 或 ~/.zshrc 中添加
export PATH="/usr/local/texlive/2024/bin/universal-darwin:$PATH"  # macOS
export PATH="/usr/local/texlive/2024/bin/x86_64-linux:$PATH"      # Linux
```

### 6.5 安装验证

```bash
# 验证 LaTeX 安装
pdflatex --version
# 预期输出：pdfTeX 3.x ...

# 验证中文支持
echo '\documentclass{ctexart}\begin{document}测试中文\end{document}' > test.tex
xelatex test.tex
# 预期：生成 test.pdf，中文正常显示
```

---

## 七、质量门禁 3 轮未通过的应对

### 7.1 问题描述

EssayResearch 的质量门禁包含多角色评审（参考 review-rubric.md），评审决策为"小修"或"大修"时需修订后重新评审。最大修订轮次为 3 轮。如果 3 轮修订后仍未达到通过标准（≥80 分），流程会阻塞。

### 7.2 阻塞场景

```
R1 评审 → 大修（55 分）→ 修订 → R2 评审 → 小修（72 分）→ 修订 → R3 评审 → 小修（76 分）
                                                                                          │
                                                                                          └── ⚠️ 已达 3 轮上限，仍未通过
```

### 7.3 应对方案

当 3 轮修订后仍未通过时，系统提供以下选项：

| 选项 | 说明 | 适用场景 |
|------|------|---------|
| A. 手动覆盖-强制通过 | 用户确认已知悉未达标，强制标记为通过 | 论文质量接近达标（75-79），剩余问题不影响核心结论 |
| B. 手动覆盖-小修后通过 | 标记为"小修后通过"，记录剩余待改项 | 论文有少量已知小问题，用户承诺后续修改 |
| C. 终止流程 | 退出自动评审，建议重新审视论文核心内容 | 论文质量差距较大（<70），自动修订无法收敛 |

### 7.4 手动覆盖的记录

手动覆盖不是"静默放行"，所有覆盖操作都会记录在论文元数据中：

```json
{
  "qualityGate": {
    "maxRoundsReached": true,
    "rounds": 3,
    "scoreHistory": [55, 72, 76],
    "finalDecision": "Minor Revision",
    "manualOverride": {
      "applied": true,
      "option": "B",
      "userAcknowledgment": "已知悉评分 76 分（未达 80 分自动通过线），选择小修后通过",
      "remainingIssues": [
        "§4.2 实验缺少消融实验",
        "§5.1 图 3 缺少误差线"
      ],
      "timestamp": "2024-01-15T14:00:00Z"
    }
  }
}
```

### 7.5 预防措施

为避免陷入 3 轮未通过的困境，建议：

| 预防措施 | 说明 |
|---------|------|
| 初稿质量把控 | 在提交评审前，先执行 AI 高频词检测和诚信门禁检查，确保基础质量 |
| 针对性修订 | 每轮修订聚焦审稿意见中分数最低的维度，避免"全面微调"导致收敛慢 |
| 关注分数轨迹 | 观察 review-rubric.md 的追踪表，如果连续 2 轮某维度停滞不前，需改变修订策略 |
| 提前识别硬伤 | 诚信门禁检查（integrity-gate-checklist.md）的 7 项必须在评审前全部通过，硬伤不进入评审轮次 |

---

## 八、QoderWork 平台路径限制

### 8.1 限制说明

QoderWork 平台的 Bash 工具在用户目录下操作，对文件系统访问有以下限制：

| 限制项 | 说明 | 影响 |
|--------|------|------|
| 工作目录限制 | Bash 工具的默认工作目录在用户工作空间下 | 无法直接访问系统级目录（如 `/etc`、`C:\Windows`） |
| 路径格式 | Windows 路径需使用正斜杠或双反斜杠 | 单反斜杠在 Bash 中被解释为转义字符 |
| 权限边界 | 仅对工作空间目录有读写权限 | 无法在用户目录外创建/修改文件 |
| 环境变量 | 工作空间内的环境变量可设置 | 系统级环境变量需通过平台设置 |

### 8.2 路径处理最佳实践

```bash
# 正确：使用正斜杠
ls "C:/Users/Aznnnn/.qoderworkcn/workspace/mr4dfyufy99ee336/EssayResearch/"

# 错误：单反斜杠（Bash 中被解释为转义）
ls "C:\Users\Aznnnn\.qoderworkcn\workspace\mr4dfyufy99ee336\EssayResearch\"
# → bash: eval: line 1: unexpected EOF while looking for matching `"' 错误

# 正确：使用双引号包裹路径（含空格时必须）
cat "C:/Users/Aznnnn/.qoderworkcn/workspace/mr4dfyufy99ee336/my project/file.md"

# 正确：使用变量引用工作空间根目录
WORKSPACE="C:/Users/Aznnnn/.qoderworkcn/workspace/mr4dfyufy99ee336"
ls "$WORKSPACE/EssayResearch/"
```

### 8.3 常见路径错误与修复

| 错误现象 | 原因 | 修复方法 |
|---------|------|---------|
| `unexpected EOF while looking for matching '"'` | Windows 路径中的单反斜杠导致引号不配对 | 将 `\` 替换为 `/` |
| `No such file or directory` | 路径使用了 `~` 但 Bash 未展开 | 使用完整绝对路径 |
| `Permission denied` | 尝试访问工作空间外的目录 | 确保操作在工作空间内 |
| 命令行工具找不到（如 `pdflatex`） | 工具未安装或不在 PATH 中 | 参考 §六 安装并配置 PATH |

### 8.4 跨平台路径适配

EssayResearch 的脚本和配置文件应使用跨平台兼容的路径处理方式：

```javascript
// 使用 Node.js 的 path 模块处理路径（自动适配平台）
const path = require('path');
const projectRoot = path.resolve(__dirname, '..', '..');
const outputFile = path.join(projectRoot, 'outputs', 'paper.pdf');

// 避免：硬编码平台特定分隔符
const badPath = 'outputs\\paper.pdf';  // 仅 Windows 可用
```

```python
# Python 中使用 os.path 或 pathlib
import os
from pathlib import Path

project_root = Path(__file__).parent.parent
output_file = project_root / 'outputs' / 'paper.pdf'
```

### 8.5 工作空间目录结构参考

```
mr4dfyufy99ee336/                     # 工作空间根目录
├── EssayResearch/                    # EssayResearch 技能目录
│   ├── skills/                       # 技能文件
│   │   ├── EssayResearch-zh/         # 中文版技能
│   │   ├── EssayResearch-en/         # 英文版技能
│   │   ├── research[G.9]-format/     # 格式规范
│   │   └── shared/                   # 共享引用文件（本文件所在位置）
│   │       ├── writing-quality/      # 写作质量参考文件
│   │       │   ├── ai-frequency-words.md
│   │       │   ├── integrity-gate-checklist.md
│   │       │   └── review-rubric.md
│   │       ├── format-specs/         # 格式规范参考文件
│   │       └── troubleshooting.md    # 本文件
│   ├── scripts/                      # 脚本文件
│   ├── LICENSE
│   └── logo.png
├── ResearchPilot-Skills/             # ResearchPilot 技能目录
├── outputs/                          # 输出目录
└── uploads/                          # 用户上传目录
```

---

## 九、版本信息

| 项目 | 值 |
|------|-----|
| 文件版本 | 1.0.0 |
| 来源 | academic-paper-writer-pro §8 + ResearchPilot 实践经验 |
| 适用技能 | EssayResearch-zh / EssayResearch-en / ResearchPilot |
| 维护方 | EssayResearch 技能团队 |
