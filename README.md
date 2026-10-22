# Research Statement Skill

根据导师近期研究、公开申请要求和申请者最新 CV，制作英文博后套磁信、Research Statement 和定制 CV。英文信可直接复制到邮件或表单，Word 后续页保留中文申请说明及证据链接。

A reusable Codex skill for evidence-based postdoctoral outreach, research statements, and CV tailoring. The skill identifier remains `cover-letter`. This public package contains generic instructions and placeholder templates; applicant records are supplied separately at runtime.

## 功能

- 核验导师当前单位、官方联系方式、最近滚动 12 个月的相关研究及申请要求。
- 区分公开招聘、一般联系、过期广告和未确认岗位，不将研究匹配写成招聘承诺。
- 将申请人的已完成工作、当前研究与拟开展计划分开表述。
- 为每位导师建立研究问题、方法、实验及评价的具体连接。
- 保护 CV 的教育、论文、项目、图片、荣誉和推荐人，仅定制允许的文字区域。
- 导出后检查全文、链接、页数和每一页的视觉排版，保留原始文件。

## 安装

下载本仓库，或使用 Git 克隆。将仓库内容放在 Codex 的 `skills/cover-letter/` 目录，使入口为 `skills/cover-letter/SKILL.md`。使用自定义 `CODEX_HOME` 时，以该位置为准；默认位置通常是用户主目录下的 `.codex/skills/cover-letter/`。

已有同名技能时，先保留原版本及其中的私人配置，再自行决定是否替换。公开包不包含任何个人工作区配置。

```text
cover-letter/
  SKILL.md
  agents/openai.yaml
  assets/
    cover_letter_template.docx
    research_statement_template.docx
  references/
    research-and-writing.md
    layout-and-files.md
    workspace-setup.md
  scripts/format_letter.py
```

## 使用示例

在支持该技能的 Codex 环境中提供最新 CV、目标导师的官方主页及输出目录：

```text
$cover-letter
根据我提供的最新 CV 和这位导师的官方主页，核查近期研究和申请要求，
制作完整博后申请包。保留 CV 的教育、论文与项目，只定制 Profile、
Interests 和 Skills。请将未确认的岗位信息写在中文申请说明中。
```

批量任务可以补充原始编号范围、保留/删除项、国家或学科条件。需要在信中加入论文或视频链接时，请明确提供链接及论文的最新状态。

默认每位导师一个 `NN_Advisor_Name` 文件夹，包含：

| 文件 | 用途 |
|---|---|
| `CV.pdf` | 局部定制后的简历 |
| `Research_Statement.docx` | 可编辑研究陈述 |
| `Research_Statement.pdf` | 投递用研究陈述 |
| `套磁信.docx` | 英文邮件正文与后续中文申请说明 |

用户指定范围和官方申请要求优先。需要额外一页摘要、固定主题或在线表单时逐位适配。中文说明仅供申请者参考，不混入发给导师的正文。

## 模板与格式脚本

两份 DOCX 都只有占位内容，保留页眉、页脚、页码域和样式。使用前须替换全部双花括号占位符、页眉页脚作者信息，以及 `example.org` 链接；模板本身不能作为申请材料发送。

`format_letter.py` 仅统一既有 Word 套磁信的字体及正文对齐，不研究导师、不改写正文、不生成完整申请包。运行脚本需要 Python 和 `lxml`：

```bash
python -m pip install -r requirements.txt
python scripts/format_letter.py input.docx formatted.docx
```

明确需要原位修改时使用 `--in-place`。自定义标题或署名可通过 `--keep-style`、`--keep-prefix` 保护：

```bash
python scripts/format_letter.py input.docx formatted.docx --keep-style CustomHeading --keep-prefix "Hi "
```

完整申请包由技能指导代理结合当前环境的文档、PDF 和演示文稿工具完成。本仓库不附带 Office、PDF 渲染器或字体；字体缺失会影响版式，需要核对实际导出页面。

## 隐私与执行范围

仓库不含真实 CV、联系方式、推荐人、私人申请记录或绝对工作区路径。模板已去除作者信息、旧缩略图和无用自定义 XML。实际使用中的私人资料属于用户提供的输入，应留在独立工作区；工具平台如何处理输入取决于运行环境。

技能本身不授权发送邮件、提交表单或上传 CV。更多说明见 [PRIVACY.md](PRIVACY.md)。
