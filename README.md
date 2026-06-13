# artifact_parses_text

把任意文件类型的产物（xlsx / docx / pdf / pptx / html / md）解析成一份 `.md` 文本，再用一组 Python「校验脚本」对这份文本（或文件名）跑规则检查，输出可读的终端结果 + 一份带时间戳的 JSON 报告。

主要用途：把那些**可以靠文本判定**的 rubric（关键词是否出现、是否禁用某种格式、数值是否在区间内……）从人工评分里搬出来，写成稳定可重跑的脚本。

整体流程：

```
附件 → parser 抽文本 → check_*.py 跑规则 → stdout 汇总 + JSON 报告
```

## 安装

```bash
git clone https://github.com/lwy100/artifact_parses_text.git
cd artifact_parses_text

# 推荐用 uv（最简洁）
uv sync

# 或 pip
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

一句话判断：**这条 rubric 的判定，能不能在解析后的纯文本（或文件名）里逐字对上？** 能就适合脚本化，不能就留给人或视觉模型。

常见可脚本化的 rubric 形态（每种都有现成模板可抄）：

| 形态 | 模板 |
| --- | --- |
| 文件名 / 格式约束 | [`checks/example/check_extension_policy.py`](checks/example/check_extension_policy.py) |
| 一组关键词必须全部出现 | [`checks/example/check_all_keywords_present.py`](checks/example/check_all_keywords_present.py) |
| 一组关键词出现任一即可 | [`checks/example/check_any_keyword_present.py`](checks/example/check_any_keyword_present.py) |
| 禁词 / 反向约束 | [`checks/example/check_forbidden_keywords.py`](checks/example/check_forbidden_keywords.py) |
| 数量阈值（≥ N 个标题、关键词出现 ≥ N 次等） | [`checks/example/check_min_count.py`](checks/example/check_min_count.py) |
| 数值范围 / 异常值 | [`checks/example/check_number_range.py`](checks/example/check_number_range.py) |

涉及视觉信号的 rubric 不适合脚本化——版式、颜色、线型、坐标位置、嵌套关系、视觉感受、主观打分，这些 parse 后看不到，**别强行写**。如果 rubric 数据里 `visual_depend: 是`，基本就是这种。

> 端到端示例：[`checks/rubric_baoyu_diagram_7641/`](checks/rubric_baoyu_diagram_7641/) 从一条海报类 task 的 rubric 里挑了 10 条改写成 check_*.py，可直接 `python3 parse_and_check.py --file <候选海报> --script checks/rubric_baoyu_diagram_7641` 一次性跑完。

> 脚本化只是把可机判的部分搬出去，剩下需要人判的部分仍然要保留人判，两条路线互为补充——以脚本结果替代整体评分会漏掉真正决定产物质量的视觉/结构问题。

## 写一个校验脚本

> **想直接起步**：[`checks/example/`](checks/example/) 下面的 6 个模板覆盖了上一节列出的常见模式。复制一份、改 docstring 顶部的 `REQUIRED` / `BLOCKED` / `FORBIDDEN` / `MIN_COUNT` 等常量，就能成为你自己的 check。

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
