"""检查附件名是不是 .pptx。"""

from checks.checker import Checker


class PptxExtensionChecker(Checker):
    name = "pptx-extension"

    def check_filename(self, file_name, meta):
        if file_name.lower().endswith(".pptx"):
            return {"ok": True, "name": self.name, "detail": file_name}
        return {"ok": False, "name": self.name, "detail": f"后缀不是 .pptx：{file_name}"}
