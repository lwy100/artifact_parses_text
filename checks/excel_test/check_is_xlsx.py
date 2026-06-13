"""rubric「产物必须以 .xlsx 后缀提交」：文件名后缀必须是 .xlsx。"""

from checks.checker import Checker


class IsXlsxChecker(Checker):
    name = "is-xlsx"

    def check_filename(self, file_name, meta):
        if meta["ext"] == ".xlsx":
            return {"ok": True, "name": self.name, "detail": file_name}
        return {"ok": False, "name": self.name, "detail": f"后缀不是 .xlsx：{file_name}"}
