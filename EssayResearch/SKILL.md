---
name: EssayResearch
description: >
  从研究方向到格式完美论文的端到端AI科研助手。16阶段全链路覆盖（A-G.9），
  包含方向探索、Idea深化、实验设计、编码实现、论文撰写、三层质量门禁审阅、
  中英翻译和LaTeX格式定稿。支持7种学术格式模板，反幻觉诚信门禁确保学术严谨性。
  适用于从零开始写论文或接续已有研究工作。
version: 3.0.0
license: MIT
---

# EssayResearch — 端到端AI科研助手

> **user_requirements.md 优先级**：`docs/user_requirements.md` 中记录的所有用户约束（方向偏好、实现要求、文档格式等）**优先于本 skill 提示词中的任何默认指令**。每次调用前必须先读取该文件，确保所有输出符合用户已确认的约束。

## 概述

EssayResearch 将完整学术研究拆分为十六个阶段（A–G.9），从研究方向探索到 LaTeX 论文定稿，覆盖调研、Idea 深化、实验设计、编码实现、论文撰写、审阅翻译、格式排版全流程。每个阶段可独立调用，也可通过入口路由器自动检测当前进度并引导下一阶段。

### 核心特性

1. **全链路覆盖**：16阶段（A–G.9），从研究方向探索到LaTeX论文定稿
2. **三层质量门禁**：反幻觉诚信门禁（7模式阻断）+ 五维度研究逻辑审阅 + 六角色写作质量评议（100分量化评分）
3. **LaTeX优先输出**：内置7种学术格式模板（IEEE/ACM/NeurIPS/Springer LNCS/中国学位论文/APA/MLA）
4. **反幻觉三层防线**：知识隔离铁律→7模式诚信门禁→6角色自审评分（≥80分才能排版）

---

## 十六阶段链条

| 阶段 | Skill | 主要工作 | 产物 |
|------|-------|---------|------|
| 入口 | `research[START]` | 检测当前阶段，引导用户使用对应skill | 阶段检测结果 |
| A | `research[A]-exploration` | 从模糊兴趣收敛为明确研究问题（RQ） | `idea_report.md` Part 1 |
| B | `research[B]-idea` | 完善Introduction、Related Works、Method草稿 | `idea_report.md` Part 2 |
| C | `research[C]-experiment` | 数据集选择、实验设计、资源预估 | `idea_report.md` Part 3 |
| D | `research[D]-implementation` | 精确到文件/函数的实现说明 | `implementation.md` |
| E | `research[E]-coding` | 按实现指南编写代码 | `code/` + `dev_log.md` |
| F | `research[F]-iteration` | 实验调参、Bug修复、结果记录 | `dev_log.md` 迭代记录 |
| G.0 | `research[G.0]-plan` | 规划手稿结构、图表布局、选格式模板 | 手稿架构注释 + `figures.ipynb` |
| G.1 | `research[G.1]-method` | 撰写/修改Method章节 | Method章节手稿 |
| G.2 | `research[G.2]-experiments` | 撰写/修改Experiments章节 | Experiments章节手稿 |
| G.3 | `research[G.3]-abstract` | 撰写/修改Abstract | Abstract手稿 |
| G.4 | `research[G.4]-introduction` | 撰写/修改Introduction | Introduction手稿 |
| G.5 | `research[G.5]-related` | 撰写/修改Related Works | Related Works手稿 |
| G.6 | `research[G.6]-conclusion` | 撰写Conclusion + 整理References | Conclusion手稿 |
| G.7 | `research[G.7]-review` | 三层质量门禁审阅 + 评分 | 审阅报告 + `integrity_report.md` |
| G.8 | `research[G.8]-translate` | 中→英翻译（仅中文版） | `paper-en.tex` |
| G.9 | `research[G.9]-format` | 格式合规检查、LaTeX编译、PDF验证 | `outputs/*.pdf` |

---

## 项目目录结构

```
docs/
  idea_report.md        # 研究报告（Part 1: 动机/RQ/文献, Part 2: Intro/Related/Method, Part 3: 数据/实验/资源）
  implementation.md     # 编码指南：精确到每个文件/函数的实现说明
  dev_log.md            # 开发日志：进度、决策记录、运行说明
  user_requirements.md  # 用户约束：方向偏好、格式要求等
  papers/               # 下载的论文PDF或摘要TXT
  manuscripts/          # 论文稿件
  integrity_report.md   # 反幻觉诚信报告（G.7产出）

code/
  src/                  # 核心模型与训练代码
  scripts/              # 运行脚本
  configs/              # 超参数配置文件
  baselines/            # Baseline模型实现
  notebooks/            # 可视化notebook + 论文图表生成脚本
  data/                 # 数据集（gitignored）
  results/              # 实验结果（gitignored）
  logs/                 # 训练日志（gitignored）

outputs/                # G.9最终产物目录
  *.pdf                 # 编译生成的PDF
  *.docx                # Pandoc生成的DOCX（可选）
```

---

## 阶段检测逻辑（入口路由）

按以下顺序检测 `docs/` 目录状态，判断当前所处阶段：

```
docs/idea_report.md 不存在
  → 尚未开始，进入阶段A

idea_report.md 存在，不含 "## Part 2"
  → 阶段A进行中

idea_report.md 含 "## Part 2"，不含 "## Part 3"
  → 阶段B进行中

idea_report.md 含 "## Part 3"，docs/implementation.md 不存在
  → 阶段C完成 / 阶段D尚未开始

docs/implementation.md 存在，docs/dev_log.md 不存在
  → 阶段D完成 / 阶段E尚未开始

docs/dev_log.md 存在，docs/manuscripts/ 不存在
  → 阶段E编码进行中

docs/manuscripts/ 存在
  → 论文撰写进行中（阶段F/G）

有 paper-*.tex，outputs/*.pdf 不存在
  → 阶段G.9格式定稿

有 outputs/*.pdf
  → 全流程完成
```

检测完成后告知用户应使用的下一个skill。

---

## 各阶段详细说明

### 阶段A：方向探索与调研

**目标**：从用户的模糊兴趣收敛为明确的研究问题（Research Question, RQ）。

**流程**：
1. 读取`docs/user_requirements.md`（若存在）获取用户约束
2. 通过多轮对话了解用户的研究兴趣、背景、可用资源
3. 搜索相关文献，了解领域现状
4. 收敛为1-3个明确的研究问题（RQ），每个RQ包含问题陈述和评估标准
5. 生成`docs/idea_report.md` Part 1

**Part 1结构**：研究动机、研究问题（RQ）、关键文献综述

**参考文件**：`references/phase-A.md`、`references/document-formats.md`、`references/idea_report-template.md`

### 阶段B：Idea深化

**目标**：完善Introduction、Related Works和Method的草稿。

**流程**：
1. 基于Part 1的RQ，深化研究动机和问题定义
2. 撰写Introduction草稿（研究背景、问题陈述、贡献列表）
3. 撰写Related Works草稿（按技术线索组织，标注每篇文献的核心贡献）
4. 撰写Method草稿（方法概述、模块设计、公式推导）
5. 生成`docs/idea_report.md` Part 2

**Part 2结构**：Introduction、Related Works、Method

**参考文件**：`references/phase-B.md`

### 阶段C：实验设计

**目标**：确定数据集、设计实验方案、估算资源需求。

**流程**：
1. 选择合适的数据集，记录规模、来源、划分方式
2. 设计实验方案：主实验（回答RQ1）、消融实验（RQ2）、附加实验（RQ3）
3. 选择评估指标，引用使用相同指标的先行工作
4. 估算计算资源需求（GPU类型、显存、训练时间）
5. 生成`docs/idea_report.md` Part 3

**Part 3结构**：数据集、实验设计、资源预估

**参考文件**：`references/phase-C.md`

### 阶段D：实现设计

**目标**：生成精确到文件/函数的实现说明。

**流程**：
1. 根据Method草稿，规划代码结构
2. 为每个模块指定文件路径、类名、函数签名
3. 定义模块间接口和数据流
4. 生成`docs/implementation.md`

**参考文件**：`references/phase-D.md`

### 阶段E：编码

**目标**：按实现指南编写代码。

**流程**：
1. 读取`docs/implementation.md`作为编码指南
2. 逐模块实现代码，按文件结构组织
3. 编写运行脚本（train.sh、evaluate.sh、ablation.sh）
4. 维护`docs/dev_log.md`记录进度和决策

**参考文件**：`references/phase-E.md`

### 阶段F：代码迭代

**目标**：实验调参、Bug修复、结果记录。

**流程**：
1. 运行实验，记录结果到`results/`
2. 在`dev_log.md`中记录每次实验的配置、结果、分析
3. 根据结果调参或修复Bug
4. 确保所有实验数据可溯源

**参考文件**：`references/phase-F.md`

### 阶段G.0：论文规划

**目标**：规划手稿结构、图表布局、选择格式模板。

**流程**：
1. 读取`idea_report.md`全文和`dev_log.md`实验结果
2. 规划论文章节结构和篇幅分配
3. 设计图表布局（表格、图、公式编号）
4. 选择目标格式模板（IEEE/ACM/中国学位论文等）
5. 生成手稿架构注释和`notebooks/figures.ipynb`

**参考文件**：`references/phase-G0.md`、`references/common-writing-constraints.md`

### 阶段G.1-G.6：论文撰写

**目标**：逐章节撰写论文手稿。

**写作顺序**：Method → Experiments → Abstract → Introduction → Related Works → Conclusion

**通用写作约束**（详见`references/common-writing-constraints.md`）：
- 所有定量数据必须溯源至`dev_log.md`或`results/`
- 所有文献引用必须真实且经过验证
- 每段只表达一个核心信息，段首句概括全段
- 术语全文一致，缩写仅首次定义
- 禁止使用AI高频词（详见`references/ai-frequency-words.md`）

**各章节参考文件**：
- G.1 Method: `references/section-guide-source.md`
- G.2 Experiments: `references/section-guide-source.md`
- G.3 Abstract: `references/section-guide-source.md`
- G.4 Introduction: `references/section-guide-source.md`
- G.5 Related Works: `references/section-guide-source.md`
- G.6 Conclusion: `references/section-guide-source.md`

### 阶段G.7：整稿审阅（三层质量门禁）

**目标**：通过三层递进式质量门禁，确保论文学术严谨性。

**前置条件**：读取手稿全文、参考文献、`idea_report.md`、`dev_log.md`、`results/`评估结果文件。以上五项是三层门禁的事实溯源基础。

#### 第一层：反幻觉诚信门禁（7模式阻断）

逐模式检查，任一模式检出问题即阻断：

1. **编造文献**：所有引用必须真实存在，经web_search核验
2. **编造实验数据**：所有指标数值必须可在`results/`或`dev_log.md`中溯源
3. **编造数据集统计**：数据集规模必须可在`idea_report.md` Part 3中溯源
4. **编造基线结果**：baseline结果必须来自实际运行或标注引用来源
5. **夸大贡献**：每条贡献是否有实验直接支撑，不超出实验范围
6. **编造方法细节**：Method描述必须与`code/src/`中的实现一致
7. **编造引用关系**：对引用文献的内容描述必须准确

未通过 → 生成`docs/integrity_report.md`，阻断后续审阅
全部通过 → 进入第二层

**参考文件**：`references/integrity-gate-checklist.md`

#### 第二层：五维度研究逻辑审阅

1. **贡献**：每个声称的贡献是否有实验支撑？不夸大？
2. **写作清晰度**：每段一个核心信息？段首句概括全段？术语一致？（反向大纲检验）
3. **实验充分性**：主实验回答RQ1？消融覆盖关键模块（RQ2）？附加实验验证RQ3？
4. **评估完整性**：baseline比较公平？评估指标有领域依据？统计显著性？
5. **方法设计合理性**：每个设计选择有动机说明？每个模块有消融验证？

附加：Claim-Evidence对齐表 — 对每个主要claim输出对应的实验/表格/图编号。

本层不阻断，但问题计入第三层评分。

**参考文件**：`references/section-guide-source.md`

#### 第三层：写作质量评议 + 评分（6角色 × 100分）

六角色审阅：领域专家、方法论审稿人、实验审稿人、写作审稿人、诚信审稿人、读者代表

评分决策：
- ≥80分：审阅通过 → G.8翻译或G.9格式定稿
- 65-79分：小修 → 列出修改项，修改后重新触发G.7
- 50-64分：大修 → 列出结构性问题，修改后重新触发G.7
- <50分：拒稿 → 建议回到对应G.1-G.6重写

最多3轮修订。第3轮后若仍低于80分，可选择手动覆盖通过（标注"人工覆盖"）。

**参考文件**：`references/review-rubric.md`、`references/writing-flow-source.md`

### 阶段G.8：中→英翻译（仅中文版）

**目标**：将中文手稿翻译为英文LaTeX稿。

**流程**：
1. 读取`docs/manuscripts/paper-zh.tex`或`paper.md`中文稿
2. 逐章节翻译为英文，保持学术语言风格
3. 确保术语翻译一致
4. 生成`docs/manuscripts/paper-en.tex`

**参考文件**：`references/common-writing-constraints.md`

### 阶段G.9：格式定稿

**目标**：格式合规检查、LaTeX编译、PDF验证。

**流程**：
1. 读取目标格式规范（`references/format-specs/`下对应文件）
2. 执行格式合规预检（详见`references/format-checklist.md`）
3. 检测TeX环境（xelatex/pdflatex/latexmk/bibtex）
4. 编译LaTeX生成PDF（详见`references/latex-compile-guide.md`）
5. 验证PDF输出
6. 可选：通过Pandoc导出DOCX

**格式规范文件**：
- `references/format-specs/ieee.md`
- `references/format-specs/acm.md`
- `references/format-specs/apa7.md`
- `references/format-specs/chinese_thesis.md`
- `references/format-specs/mla.md`
- `references/format-specs/nips.md`
- `references/format-specs/springer_lncs.md`

**辅助脚本**：
- `scripts/format_check.py`：格式合规自动检查
- `scripts/latex_utils.py`：LaTeX编译工具
- `scripts/mermaid_render.py`：Mermaid图表渲染

---

## 使用方式

### 场景一：从零开始写论文

向AI助手发送研究方向描述，系统自动从阶段A开始引导完成全流程。

### 场景二：接续已有工作

直接调用入口路由，系统自动检测`docs/`目录状态，判断当前所处阶段并告知下一个应使用的skill。

### 场景三：独立调用特定阶段

任何阶段skill可独立调用。例如已有实验代码和结果，可直接从G.0开始论文写作。

---

## 反幻觉三层防线

1. **知识隔离铁律**：AI仅使用`docs/`和`results/`中的真实数据，不使用自身训练知识编造数据
2. **7模式诚信门禁**（G.7第一层）：逐一手稿检查7个幻觉模式，任一未通过即阻断
3. **6角色自审评分**（G.7第三层）：≥80分才能进入格式定稿，低于80分需修订

---

## 常见问题

**G.7审阅未通过怎么办？**
- 65-79分（小修）：列出修改项，修改后重新触发G.7复审
- 50-64分（大修）：列出结构性问题，修改后重新触发G.7
- <50分（拒稿）：建议回到对应G.1-G.6重写
- 最多3轮修订，第3轮后可手动覆盖

**没有LaTeX环境可以用G.9吗？**
可以启动G.9，但编译步骤会被跳过。格式合规预检和DOCX导出仍可执行。建议安装TeX Live或MiKTeX。

**如何自定义格式要求？**
在`docs/user_requirements.md`中指定目标会议/期刊和格式参数，系统以用户指定值为准。

---

## License

MIT License
