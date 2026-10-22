# 版式、模板和文件

## RS 默认版式

下面是随附通用模板的默认版式；用户指定参考稿时以该稿为准，先读取全文与实际页面。

| 元素 | 参数 |
|---|---|
| 页面 | A4、单栏、一个节；四边 72 pt（2.54 cm） |
| 页眉/脚距边 | 32.4 pt |
| 标题 | Times New Roman，14 pt，加粗、黑色；单倍行距、段后 8 pt |
| 作者信息 | Times New Roman，9 pt；姓名、单位、网站超链接 |
| 一级标题 | Times New Roman，11 pt，加粗；段前 7 pt、段后 4 pt、与下段同页 |
| 正文 | Times New Roman，11 pt；1.05 倍行距、段后 5 pt；两端对齐、不缩进、孤行控制 |
| 页眉 | 9 pt；作者左侧、Research Statement 右侧，用右对齐制表位 |
| 页脚 | 9 pt，作者与真实 PAGE 域，右对齐 |
| 外观 | 简洁黑白、连续叙述，无额外封面、装饰图表或复杂列表 |

正文最后一行自然左对齐，不使用分散对齐。不硬分页强制两个研究方向各占一页，不整段 keep-with-next 导致空缺。通常两页，但官方字数/页数限制优先。

`assets/research_statement_template.docx` 保留样式、节、页眉页脚及字段，正文已替换为双花括号占位符：

- `RS_TITLE`；`APPLICANT_NAME` / `AFFILIATION` / `WEBSITE_LABEL`。
- `VISION`；`PAST_RESEARCH` / `CURRENT_RESEARCH`。
- `DIRECTION_ONE_QUESTION` / `DIRECTION_ONE_METHOD` / `DIRECTION_ONE_EVALUATION`。
- `DIRECTION_TWO_QUESTION` / `DIRECTION_TWO_METHOD` / `DIRECTION_TWO_EVALUATION`。
- `STAGED_PLAN` / `RESEARCH_FIT`。

尽量在 run 中替换文字；替换段落时保留 pPr，新增段落克隆对应格式。作者在页眉页脚也要替换；网站显示文字和关系目标分别更新，不能保留 example.org。保留 PAGE 域；交付前全文、超链接不得残留占位符。

## 套磁信 Word

修复既有文件时保留字号和标题层级。新建可用 `assets/cover_letter_template.docx`：

- A4，上 1.85 cm、下 1.8 cm、左右 2 cm，页脚距边 0.8 cm。
- 正文 11 pt，1.12 倍行距、段后 7 pt；标题 21 pt、段后 5 pt；小标题 12 pt 加粗、段前 10 pt、段后 5 pt。
- 拉丁文字 Times New Roman，中文宋体（SimSun），含标题、链接、页眉页脚。分别设置 ASCII/hAnsi/cs 和 eastAsia 字体，并移除冲突主题字体，仅 font.name 不够。
- 中英文正文两端对齐；To、Subject、称呼、署名、标题及短元信息自然左对齐。设置 `doNotExpandShiftReturn`，避免手动换行的署名出现拉伸。
- 英语通常一页，中文说明另起页，按实际信息量自然续页，不删重要申请细节强凑两页。
- 官方招聘页、导师页、研究证据均为可点击链接，核验目标及换行。

模板占位符：`APPLICANT_NAME`、`ADVISOR_NAME`、`INSTITUTION`、`LAB_NAME`、`RECIPIENT_OR_CHANNEL`、`EMAIL_SUBJECT`、`SALUTATION`，以及 `OPENING`、`RELEVANT_BACKGROUND`、`RESEARCH_CONNECTION`、`PROPOSED_DIRECTION`、`CLOSING`、`SIGNATURE`。

中文页为 `CHECK_DATE_AND_WINDOW`、`USAGE_NOTES_ZH`、`APPLICATION_REQUIREMENTS_ZH`、`TAILORING_NOTES_ZH`、`SOURCE_ATTRIBUTION_ZH`，含待替换的申请页、导师页和研究链接。没有公开申请页时删掉该链接，不编 URL。

## CV 版式保护

- 继承最新原件字体、字号、页面与图文布局。套磁信的中英文字体要求不能扩大成 CV 整体改版。
- 修改前记录文字框、位置/尺寸、图片/标志与页数，确定允许编辑对象。对象 ID 随文件重新识别，不复用导入工具某次生成的 ID。
- Profile 和 Core Competencies 各正文段落两端对齐；Interest 保留列表；技能标签仍加粗。
- 内容充实完整，不把长段落整体搬页导致中间空白，不拉大间距凑页。局部改后检查下方标题、图片与正文碰撞。
- 原 PPTX 不变。工作副本留构建目录，导师目录只放 CV.pdf，不放 CV PPTX、源 DOCX 或多份旧 CV。

## 导出与验证

1. 从环境查询依赖，使用可用的 Python、Office/PDF 库和字体，不硬编码当前缓存版本路径。
2. DOCX 用可用渲染工具导出；缺少 LibreOffice 而本机有 Word 时，可用独立隐藏 Word 实例只读打开目标、重新分页、导出 PDF，不保存回原模板。不能确认实例归属时不执行 Quit 或批量关闭。
3. 文件真实生成且可读才称已导出。源文件生成成功或控制台打印 completed 不能代替最终产物验证，进程非零退出须排查。
4. 检查 RS DOCX/PDF 内容一致；套磁信字体、对齐、原文及链接正确。格式修复前后全文应一致。原始输入哈希不变，冻结 CV 区域内容保持。
5. 每份最终 PDF 逐页渲染查看；套磁信可导出私有检查 PDF。检查裁切、重叠、乱码、字距、页眉页脚、标题孤悬、空白页、链接换行及中间大片空白。可用整页拼图查全批布局，疑似问题与混排細节放大看原页；XML 检查不能代替视觉检查。
6. 核验各导师自己的字数/页数/大小要求、题目和状态一致、目录齐全。不能统一断言 RS 必须两页。

只有实际失败或新修改需要时才追加检查，不循环重写认可部分。记录、PNG、临时导出、工作源与证据均放构建目录，不塞入申请文件夹。

默认每位目录四文件：`CV.pdf`、`Research_Statement.docx`、`Research_Statement.pdf`、`套磁信.docx`。需要导师名单时每位四行：“编号 University | Lab”“姓名”“官网链接”“邮箱”，按参考图可用项目符号，链接可点，编号与目录一一对应。增补延续映射。
