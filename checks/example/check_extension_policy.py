"""模板 1：文件名后缀白名单 / 黑名单。

适用场景：rubric 写"产物必须是 X 格式"或"产物不能是 Y 格式"，且只看文件后缀就足以判定。
比如：
- 产物必须是 .pptx
- 产物不能是 Excel（.xlsx/.xls）
- 产物不能是 Markdown 代码（.md/.markdown）

要点：检查方法用 check_filename，因为这跟 parse 出来的文本无关，纯看文件名。
"""

from checks.checker import Checker


# 改 ALLOWED 走白名单（只允许这几种后缀），改 BLOCKED 走黑名单（这几种后缀就 fail）。
# 二选一，把另一个留空即可。
ALLOWED = []                        # 例：[".pptx", ".pdf"]
BLOCKED = [".xlsx", ".xls"]         # 例：[".md", ".markdown"]


class FilenameExtensionChecker(Checker):
    name = "ext-policy"

    def check_filename(self, file_name, meta):
        ext = meta["ext"]  # parse_and_check 已经把后缀小写了，可以直接比

        if ALLOWED and ext not in ALLOWED:
            return {"ok": False, "name": self.name,
                    "detail": f"后缀 {ext} 不在白名单 {ALLOWED}：{file_name}"}

        if BLOCKED and ext in BLOCKED:
            return {"ok": False, "name": self.name,
                    "detail": f"后缀 {ext} 命中黑名单 {BLOCKED}：{file_name}"}

        return {"ok": True, "name": self.name, "detail": file_name}
