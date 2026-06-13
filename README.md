# artifact_parses_text

把文件类型的产物（xlsx / docx / pdf / pptx / html / md）解析成文本，并可选地用「校验脚本」检查解析后的文本是否符合预期。

## 安装

```bash
uv pip install -e .
# 或
pip install -e .
```

依赖：`openpyxl` · `python-docx` · `pdfplumber` · `python-pptx` · `beautifulsoup4`。

## 使用

```bash
# 只解析，不检查 → 跟附件同目录写出 <basename>.md
python3 parse_and_check.py --file artifact_validation_data/word/foo.docx

# 解析 + 一项检查 → 同时在 check_result/ 落一个时间戳前缀的 report，stdout 打印汇总
python3 parse_and_check.py --file foo.docx --script checks/example/check_all_keywords_present.py

# --script 也可以是一个目录：里面顶层所有 check_*.py 会按文件名升序依次跑
python3 parse_and_check.py --file foo.docx --script checks/example
```

### CLI

| 参数 | 必填 | 说明 |
| --- | --- | --- |
| `--file` | ✅ | 单个附件路径，后缀决定 parser |
| `--script` | ❌ | 校验脚本路径，可重复传；可以是单个 `.py` 文件，也可以是一个目录（顶层 `check_*.py` 按文件名升序依次跑，不递归）。不传则只解析不检查 |
| `--out` | ❌ | 解析文本输出路径，默认 `<file>.md`（与附件同目录、同 basename）|
| `--report` | ❌ | JSON 报告输出位置；可传目录（落到 `<dir>/<时间戳>__<file_name>.report.json`）或直接传 `.json` 文件路径。默认 `check_result/<时间戳>__<file_name>.report.json`，**永远不覆盖**（同名时自动追加 `-2 / -3 / …`）。只在传了 `--script` 时生成 |

`--out` 直接覆盖；`--report` 不覆盖（自动追加序号）。

如果 `--script` 是目录：

- 顶层不是 `check_*.py` 的 `.py` 文件会被跳过，并打一行 `warning: …` 到 stderr。
- 目录里某个 `check_*.py` import / 语法报错时，**不会拖死整个 run**：该项以 `[ERR]` 行出现在 stdout、`status: "error"` 出现在 report，其他 check 照常跑。
- 目录里一个 `check_*.py` 都没有时直接 exit 2。

### 退出码

| code | 含义 |
| ---: | --- |
| `0` | 解析成功，且所有 check 都 `ok=True`（或者根本没传 `--script`）|
| `1` | 解析成功，但某 check 返回 `ok=False` 或抛了异常 |
| `2` | 主脚本本身出错：文件不存在 / 不支持的后缀 / parser 异常 / `--script` 路径无法 import |

## 哪些 rubric 适合做成脚本？

这套工具的核心限制是：**只能看到 parse 出的文本和文件名**，看不到版式、颜色、线型、位置、嵌套关系这些视觉信号。所以一条 rubric 适不适合改写成脚本，本质上是看它能不能用「文本/文件名能否唯一判定」这把尺子量出来。

### 适合（但不限于）改写成脚本的 rubric 模式

| 模式 | 典型 rubric 提法 | 模板 |
| --- | --- | --- |
| 文件名 / 格式硬约束 | "产物不是 Excel"、"产物必须是 .pptx"、"不要给我 Markdown 代码" | [`checks/example/check_extension_policy.py`](checks/example/check_extension_policy.py) |
| 必备要素清单（all-of） | "三档落点：基础看护/标准安防/全面守护"、"三层架构：感知层/网络层/应用层"、"路径起点四要素：年龄/独居/户型/预算" | [`checks/example/check_all_keywords_present.py`](checks/example/check_all_keywords_present.py) |
| 同义/同类近义（any-of） | "至少有一处『结论 / 结语 / 总结』"、"出现 5G / 6G / 移动通信 任一即可" | [`checks/example/check_any_keyword_present.py`](checks/example/check_any_keyword_present.py) |
| 禁词 / 反向约束 | "不能写具体型号"、"不能出现 TBD/TODO/待定"、"不要 Mermaid/Markdown 代码块" | [`checks/example/check_forbidden_keywords.py`](checks/example/check_forbidden_keywords.py) |
| 数量阈值 | "至少四类风险"、"≥ 3 个章节标题"、"关键词出现 ≥ N 次" | [`checks/example/check_min_count.py`](checks/example/check_min_count.py) |
| 数值范围 / 异常值 | "价格在 [200, 5000]"、"年龄 [0, 120]"、"先剔除负值再画图" | [`checks/example/check_number_range.py`](checks/example/check_number_range.py) |
| 文本结构信号 | "决策树主路径包含『卧室+卫生间各 1 个雷达，床头+卫生间各 1 个按钮』"、"案例卡含『朝阳/78/60/2800/3秒/15分钟』六要素" | 把 all-of 模板里的关键词换成这一组即可 |

工程信号：rubric 的『1分情况』里写的判定条件**全部能在解析后的纯文本里找到对应的字符串**，且不依赖『出现在哪个分区/什么颜色/线型如何』这种视觉位置——就改成脚本。

> 一个真实的端到端示例放在 [`checks/rubric_baoyu_diagram_7641/`](checks/rubric_baoyu_diagram_7641/)：从一条海报类 task 的 rubric 里挑出 10 条改写成 check_*.py，能直接 `python3 parse_and_check.py --file <候选海报> --script checks/rubric_baoyu_diagram_7641` 一次性跑完。

### 不要尝试改写成脚本的 rubric 模式

这些只能靠人 / 视觉模型去看，强行写脚本要么误判要么自欺欺人：

- **位置 / 分区**："放在海报左侧"、"在底部"、"右侧设侧栏" —— parse 后只剩文本流，没有 2D 坐标。
- **图形元素**："包含判断菱形 / 步骤矩形 / 旁注气泡 / 案例卡"、"用实线 / 虚线 / 不同颜色绘制" —— 这些是几何/样式信号，文本里看不到。
- **结构关系**："案例卡用虚线回连到推荐路径"、"主决策树第一层并列分叉"、"三层架构横向贯穿主图" —— 是节点之间的连接和层级关系，光看文字看不出连线指向哪。
- **视觉感受**："信息密度合理"、"贴墙扫读友好"、"一眼能识别"、"短句呈现" —— 主观体感，没有客观文本指标。
- **依据 / 来源**："风险优先级梯依据《独居老人家庭安全隐患与事故统计》制作" —— 哪份附件支撑哪段结论，文本里通常不会带『依据』标签，需要交叉比对。
- **打分制软约束**：rubric 是 0/1/2/3/4 分而不是二元 0/1 的，本质是评分员主观尺度，脚本顶多做兜底（"≥ 0 分"），分不出 3 和 4。

简单识别：rubric 里出现 "**位置 / 颜色 / 线型 / 形状 / 分区 / 排版 / 醒目 / 视觉**" 这些词，或者它在数据里 `visual_depend` 标了 `是` —— 大概率不要硬塞脚本里。

## 写一个校验脚本

> **想直接起步**：[`checks/example/`](checks/example/) 下面的 6 个模板覆盖了上一节列出的所有"推荐"模式（白/黑名单后缀、all-of、any-of、禁词、数量阈值、数值范围）。复制一份、改 docstring 顶部的 `REQUIRED` / `BLOCKED` / `FORBIDDEN` / `MIN_COUNT` 等常量，就能成为你自己的 check。

校验脚本通过继承 `Checker` 基类来定义。`Checker` 上有两个方法，按检查类型**二选一**改写：

| 改写哪个方法 | 用途 | 收到的输入 |
| --- | --- | --- |
| `check_filename(file_name, meta)` | 文件名 / meta 检查（不需要解析后的文本） | 文件名 + meta |
| `check_content(text, meta)` | 解析后正文检查 | 解析文本 + meta |

每个 `--script` 文件**只放一个**具体的 `Checker` 子类，命名随意（`MyChecker`、`HasTitleChecker` 都行）；运行器按"在该文件里直接定义、且不是基类本身"挑出唯一一个，自动实例化并调用对应方法。同时改写两个方法会被加载器拒绝。

### 内容检查（最常见）

```python
# checks/check_my_rule.py
from checks.checker import Checker


class HasConclusionChecker(Checker):
    name = "has-conclusion"          # 可选；不写就取类名去掉 Checker 后缀小写

    def check_content(self, text, meta):
        ok = "结论" in text
        return {
            "ok": ok,
            "name": self.name,
            "detail": "" if ok else "缺少『结论』段",
        }
```

### 文件名检查

```python
# checks/check_id_prefix.py
from checks.checker import Checker


class IdPrefixChecker(Checker):
    name = "id-prefix"

    def check_filename(self, file_name, meta):
        ok = file_name.startswith("ZH_")
        return {"ok": ok, "name": self.name, "detail": file_name}
```

### 返回值约定

- `ok` 必填，bool。
- `name` 可选，短标识；不传就取 `Checker` 子类的 `name` 类属性。
- `detail` 可选，给人看的一句话原因。
- 抛异常 / 返回不是 dict / 缺 `ok` → 该项记为 `error`，整体退出码 1。
- 同一文件里出现 ≥2 个 `Checker` 子类、或者一个 `Checker` 子类同时改写了 `check_filename` 和 `check_content`，都会被运行器拒绝（避免歧义），请拆成多个 `--script`。

向后兼容：旧的纯函数式 `def check(text, meta) -> dict` 仍然能用，但新写法推荐继承 `Checker`。

## 解析格式速览

| 后缀 | 库 | 输出形态 |
| --- | --- | --- |
| `.xlsx` | openpyxl | 每 sheet 一段 `## sheet: <name>` + 行 tab 分隔 |
| `.docx` | python-docx | 段落原文；`Heading N` 转 `#…`；表格转 markdown 表 |
| `.pdf` | pdfplumber | 每页 `--- page N ---` 分段，文本拼接 |
| `.pptx` | python-pptx | 每张幻灯片 `## slide N: <title>`，正文转 bullet，备注以 `> notes:` 前缀 |
| `.html` `.htm` | beautifulsoup4 | 去掉 `<script>/<style>/<noscript>`，`get_text` 后压掉空行 |
| `.md` `.markdown` | 内置 | 原文返回 |

不支持的后缀直接退出码 2。
