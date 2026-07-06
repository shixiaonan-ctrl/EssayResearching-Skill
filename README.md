EssayResearch
从研究方向到格式完美论文的端到端 AI 科研助手

EssayResearch 是一套面向 AI 编码助手的科研技能集，将完整的学术研究流程拆分为 16 个阶段（A–G.9），从研究方向探索、Idea 深化、实验设计、编码实现，到论文撰写、三层质量门禁审阅、中英翻译和 LaTeX 格式定稿，覆盖科研全链路。
每个阶段是一个独立的 Skill，可单独调用，也可通过入口路由器自动检测项目进度并引导下一阶段。内置 7 种学术格式模板和反幻觉三层防线，确保输出的学术严谨性。
✨ 特性亮点
全链路覆盖 — 16 个阶段从方向探索到 PDF 定稿，每阶段产出明确、可溯源
三层质量门禁 — 反幻觉诚信门禁（7 模式阻断）→ 五维度研究逻辑审阅 → 六角色 100 分量化评议，≥80 分才能进入排版
LaTeX 优先输出 — 内置 IEEE / ACM / NeurIPS / Springer LNCS / 中国学位论文 / APA / MLA 共 7 种格式规范，一键编译 PDF
反幻觉三层防线 — 知识隔离铁律（AI 仅使用项目真实数据）→ 7 模式诚信门禁 → 6 角色自审评分
多平台支持 — QoderWork / Claude Code / OpenAI Codex / CodeBuddy，安装脚本自动适配目标平台
中英双语 — 中文版 18 个技能（含 G.8 中→英翻译），英文版 17 个技能
📋 工作流程

研究方向（模糊）
    │
    ▼
┌─────────────────────────────────────────────────────────┐
│  A 方向探索    →  研究问题（RQ）+ 关键文献              │
│  B Idea 深化   →  Introduction / Related / Method 草稿   │
│  C 实验设计    →  数据集 + 实验方案 + 资源预估           │
│  D 实现设计    →  文件/函数级实现说明                    │
│  E 编码        →  代码 + 开发日志                        │
│  F 代码迭代    →  实验结果 + 调参记录                    │
├─────────────────────────────────────────────────────────┤
│  G.0 论文规划   →  结构 + 图表 + 格式选择                │
│  G.1 Method     →  方法章节手稿                          │
│  G.2 Experiments→  实验章节手稿                          │
│  G.3 Abstract   →  摘要手稿                              │
│  G.4 Introduction→ 引言手稿                             │
│  G.5 Related    →  相关工作手稿                          │
│  G.6 Conclusion →  结论 + 参考文献                      │
│  G.7 整稿审阅   →  三层质量门禁 + 评分                   │
│  G.8 中→英翻译  →  英文 LaTeX 稿（仅中文版）            │
│  G.9 格式定稿   →  PDF + DOCX                           │
└─────────────────────────────────────────────────────────┘
    │
    ▼
格式完美的论文 PDF

📦 安装
前置条件
●已安装目标 AI 编码助手的 CLI 或桌面端
●Bash 环境（Windows 用户推荐使用 Git Bash 或 WSL）
●（可选）LaTeX 发行版（TeX Live / MiKTeX），用于 G.9 阶段 PDF 编译
QoderWork

# 方式 A：使用 skills 命令安装
npx skills add https://github.com/<your-repo>/EssayResearch

# 方式 B：手动复制
cp -r skills/EssayResearch-zh/* ~/.qoderworkcn/skills/
cp -r skills/shared ~/.qoderworkcn/skills/

Claude Code

bash install-zh.sh claude

OpenAI Codex

bash install-zh.sh codex

CodeBuddy

bash install-zh.sh codebuddy    # 在项目目录下运行

英文版安装：将 install-zh.sh 替换为 install-en.sh，技能来源为 EssayResearch-en（不含 G.8 翻译阶段，共 17 个技能）。
验证安装

ls ~/.claude/skills | grep research    # 或对应平台目录
# 应输出 17-18 个 research[*] 目录

🚀 快速开始
场景一：从零开始写论文
向 AI 助手发送研究方向描述：

/research[START] 基于大语言模型的代码漏洞检测方法研究

系统自动从阶段 A 开始，逐步引导完成 A → B → C → D → E → F → G.0 → … → G.9 全流程。
场景二：接续已有工作
如果项目中已有部分产物（docs/idea_report.md、docs/implementation.md 等），直接发送：

/research[START]

系统自动检测 docs/ 目录状态，判断当前所处阶段并告知下一个应使用的 skill。
目录状态	检测结果
idea_report.md 不存在	尚未开始 → 阶段 A
idea_report.md 不含 Part 2	阶段 A 进行中
idea_report.md 含 Part 2，不含 Part 3	阶段 B 进行中
idea_report.md 含 Part 3，implementation.md 不存在	阶段 C 完成 → 阶段 D
implementation.md 存在，dev_log.md 不存在	阶段 D 完成 → 阶段 E
dev_log.md 存在，manuscripts/ 不存在	阶段 E 编码进行中
manuscripts/ 存在	论文撰写进行中（阶段 G）
场景三：独立调用特定阶段
任何阶段 skill 可独立调用。例如已有实验代码和结果，可直接从论文写作开始：

/research[G.0]-plan

📚 技能列表
中文版（18 个技能）
#	Skill	阶段	主要工作	产物
1	research[START]	入口路由	检测当前阶段，引导用户使用对应 skill	阶段检测结果
2	research[A]-exploration	方向探索	从模糊兴趣收敛为明确研究问题（RQ）	idea_report.md Part 1
3	research[B]-idea	Idea 深化	完善 Introduction、Related Works、Method 草稿	idea_report.md Part 2
4	research[C]-experiment	实验设计	数据集选择、实验设计、资源预估	idea_report.md Part 3
5	research[D]-implementation	实现设计	精确到文件/函数的实现说明	implementation.md
6	research[E]-coding	编码	按实现指南编写代码	code/ + dev_log.md
7	research[F]-iteration	代码迭代	实验调参、Bug 修复、结果记录	dev_log.md 迭代记录
8	research[G.0]-plan	论文规划	规划手稿结构、图表布局、选格式模板	手稿架构 + figures.ipynb
9	research[G.1]-method	Method	撰写/修改 Method 章节	Method 手稿
10	research[G.2]-experiments	Experiments	撰写/修改 Experiments 章节	Experiments 手稿
11	research[G.3]-abstract	Abstract	撰写/修改 Abstract	Abstract 手稿
12	research[G.4]-introduction	Introduction	撰写/修改 Introduction	Introduction 手稿
13	research[G.5]-related	Related Works	撰写/修改 Related Works	Related Works 手稿
14	research[G.6]-conclusion	Conclusion	撰写 Conclusion + 整理 References	Conclusion 手稿
15	research[G.7]-review	整稿审阅	三层质量门禁审阅 + 评分	审阅报告 + integrity_report.md
16	research[G.8]-translate	中→英翻译	将中文手稿翻译为英文 LaTeX	paper-en.tex
17	research[G.9]-format	格式定稿	格式合规检查、LaTeX 编译、PDF 验证	outputs/*.pdf
—	shared/	共享资源	格式规范、写作质量规则、避坑指南	—
英文版（EssayResearch-en/）：不包含 research[G.8]-translate，共 17 个技能。
🛡️ 三层质量门禁
G.7 阶段的三层递进式质量门禁是本项目的核心设计：

第一层：反幻觉诚信门禁（7 模式阻断）
  ├─ 通过 → 进入第二层
  └─ 未通过 → 阻断，输出 integrity_report.md
      检查项：编造文献 / 编造实验数据 / 编造数据集统计
             编造基线结果 / 夸大贡献 / 编造方法细节 / 编造引用关系

第二层：五维度研究逻辑审阅
  ├─ 贡献：每个声称的贡献是否有实验支撑
  ├─ 写作清晰度：每段一个核心信息，反向大纲检验
  ├─ 实验充分性：主实验→RQ1，消融→RQ2，附加→RQ3
  ├─ 评估完整性：baseline 公平性，指标有领域依据
  └─ 方法设计合理性：每个设计选择有动机说明

第三层：写作质量评议（6 角色 × 100 分）
  ├─ ≥80 分 → 审阅通过 → G.8/G.9
  ├─ 65–79 分 → 小修
  ├─ 50–64 分 → 大修
  └─ <50 分 → 拒稿（建议重写）

📁 项目结构

EssayResearch/
├── README.md                    # 本文件
├── LICENSE                      # MIT License
├── CHANGELOG.md                 # 版本历史
├── CONTRIBUTING.md              # 贡献指南
├── .gitignore
├── WORKFLOW.md                  # 完整工作流程文档
│
├── install-zh.sh                # 中文版安装脚本
├── install-en.sh                # 英文版安装脚本
├── uninstall.sh                 # 卸载脚本
├── logo.png                     # 项目 Logo
│
├── scripts/                     # 辅助脚本
│   ├── format_check.py          # 格式合规自动检查
│   ├── latex_utils.py           # LaTeX 编译工具
│   └── mermaid_render.py        # Mermaid 图表渲染
│
├── skills/                      # 技能定义
│   ├── EssayResearch-zh/        # 中文版（18 个技能）
│   │   ├── research[START]/
│   │   │   └── SKILL.md
│   │   ├── research[A]-exploration/
│   │   │   ├── SKILL.md
│   │   │   └── references/      # 阶段参考文件
│   │   ├── research[B]-idea/
│   │   ├── research[C]-experiment/
│   │   ├── research[D]-implementation/
│   │   ├── research[E]-coding/
│   │   ├── research[F]-iteration/
│   │   ├── research[G.0]-plan/
│   │   ├── research[G.1]-method/
│   │   │   └── references/examples/  # 写作范例
│   │   ├── research[G.2]-experiments/
│   │   ├── research[G.3]-abstract/
│   │   │   └── references/examples/
│   │   ├── research[G.4]-introduction/
│   │   │   └── references/examples/
│   │   ├── research[G.5]-related/
│   │   ├── research[G.6]-conclusion/
│   │   ├── research[G.7]-review/
│   │   ├── research[G.8]-translate/
│   │   └── research[G.9]-format/
│   │
│   ├── EssayResearch-en/        # 英文版（17 个技能，无 G.8）
│   │   └── ...（与中文版结构一致）
│   │
│   └── shared/                  # 两版共享的资源
│       ├── format-specs/        # 7 种学术格式规范
│       │   ├── ieee.md
│       │   ├── acm.md
│       │   ├── apa7.md
│       │   ├── chinese_thesis.md
│       │   ├── mla.md
│       │   ├── nips.md
│       │   └── springer_lncs.md
│       ├── writing-quality/     # 写作质量参考
│       │   ├── integrity-gate-checklist.md  # 反幻觉检查清单
│       │   ├── review-rubric.md              # 审阅评分表
│       │   └── ai-frequency-words.md         # AI 高频词清单
│       └── troubleshooting.md    # 避坑指南

🌍 生成文件结构
完成全流程后，用户项目目录结构如下：

项目根目录/
├── docs/
│   ├── idea_report.md          # 研究报告（Part 1/2/3）
│   ├── implementation.md       # 编码指南
│   ├── dev_log.md              # 开发日志
│   ├── user_requirements.md    # 用户约束
│   ├── integrity_report.md     # 反幻觉诚信报告
│   ├── papers/                 # 参考论文
│   └── manuscripts/            # 论文稿件
│       ├── paper-zh.tex        # 中文 LaTeX 稿
│       ├── paper-en.tex        # 英文 LaTeX 稿
│       ├── paper.md            # Markdown 稿
│       └── references.bib      # BibTeX 参考文献
├── code/
│   ├── src/                    # 核心代码
│   ├── scripts/                # 运行脚本
│   ├── configs/                # 超参数配置
│   ├── baselines/              # Baseline 实现
│   ├── notebooks/              # 图表生成 notebook
│   └── results/                # 实验结果
├── outputs/                    # G.9 最终产物
│   ├── *.pdf                   # 编译生成的 PDF
│   ├── *.docx                  # DOCX 导出（可选）
│   └── format-checklist.md     # 格式合规报告
└── .gitignore

❓ 常见问题
是否必须按顺序从 A 执行到 G.9？不是。各阶段 skill 可独立调用。例如已有实验代码和结果，可直接从 research[G.0]-plan 开始论文写作。首次使用建议通过 research[START] 让系统检测当前状态。
G.7 审阅未通过怎么办？
总分	决策	后续动作
≥ 80	通过	→ G.8 翻译或 G.9 格式定稿
65–79	小修	列出修改项，修改后重新触发 G.7
50–64	大修	列出结构性问题，修改后重新触发 G.7
< 50	拒稿	建议回到对应 G.1–G.6 重写
最多 3 轮修订。第 3 轮后若仍低于 80 分，可选择手动覆盖通过（标注"人工覆盖"）。
没有 LaTeX 环境可以用 G.9 吗？可以启动 G.9，但编译步骤会被跳过。格式合规预检和 DOCX 导出（需 Pandoc）仍可执行。建议安装 TeX Live（Linux/macOS）或 MiKTeX（Windows）。
中文版和英文版有什么区别？中文版（EssayResearch-zh）包含 research[G.8]-translate 阶段，用于将中文手稿翻译为英文 LaTeX；英文版（EssayResearch-en）不含此阶段，直接用英文写作。两个版本共享相同的 shared/ 资源。
如何自定义目标会议/期刊的格式？在 docs/user_requirements.md 中指定目标会议/期刊名称和格式参数。G.9 会读取 skills/shared/format-specs/ 下对应的格式规范，用户指定值优先。
🙏 致谢
本项目融合了多个优秀开源项目的研究成果与设计理念：
贡献者	项目	贡献内容
https://github.com/LMDHQ-0420 	ResearchPilot-Skills	16 阶段研究流水线（A–G.9），阶段路由与检测逻辑
https://github.com/tfboy1 	academic-paper-writer-pro	排版引擎与质量门禁设计（三层审阅、格式合规检查）
https://github.com/Pengsida 	learning notes	研究方向选择与论文写作的学习笔记与方法论
https://github.com/Master-cai 	Research-Paper-Writing-Skills	五维度审阅体系与 Claim-Evidence 对齐方法
https://github.com/anthropics 	Skills Repository	docx 与 PDF 操作技能的底层实现
📄 License
MIT License — 见 LICENSE 文件。
https://github.com/%3Cyour-repo%3E/EssayResearch/issues  · https://github.com/%3Cyour-repo%3E/EssayResearch/issues  · https://github.com/%3Cyour-repo%3E/EssayResearch/discussions 


