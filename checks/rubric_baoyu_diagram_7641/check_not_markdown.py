"""rubric「产物不是Markdown代码」：后缀不能是 .md/.markdown。"""

from checks.checker import Checker


class NotMarkdownChecker(Checker):
    name = "not-markdown"

    def check_filename(self, file_name, meta):
        lower = file_name.lower()
        if lower.endswith(".md") or lower.endswith(".markdown"):
            return {"ok": False, "name": self.name, "detail": f"产物是 Markdown：{file_name}"}
        return {"ok": True, "name": self.name, "detail": file_name}
